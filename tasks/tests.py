from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            title='Тестовая задача',
            description='Описание',
            status='todo',
            owner=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Тестовая задача')
        self.assertEqual(self.task.owner, self.user)

class TaskListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        for i in range(12):
            Task.objects.create(title=f'Задача {i}', owner=self.user)

    def test_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 302)  

    def test_list_view_pagination(self):
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(len(response.context['tasks']), 5)  

    def test_only_owner_tasks(self):
        other_user = User.objects.create_user(username='other', password='pass123')
        Task.objects.create(title='Чужая задача', owner=other_user)
        
        response = self.client.get(reverse('tasks:list'))
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 5)  

class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_create_task(self):
        response = self.client.post(reverse('tasks:create'), {
            'title': 'Новая задача',
            'description': 'Описание',
            'status': 'todo'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Task.objects.filter(title='Новая задача').exists())

    def test_create_task_validation(self):
        response = self.client.post(reverse('tasks:create'), {
            'title': '',  
            'status': 'todo'
        })
        self.assertEqual(response.status_code, 200)  

class TaskAccessTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.task = Task.objects.create(title='Задача user1', owner=self.user1)
        
        self.client = Client()
        self.client.login(username='user2', password='pass123')

    def test_cannot_view_other_task(self):
        response = self.client.get(reverse('tasks:detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 404)  

    def test_cannot_edit_other_task(self):
        response = self.client.get(reverse('tasks:update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 404)