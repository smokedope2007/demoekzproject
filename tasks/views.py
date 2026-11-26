from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm

# 1. СПИСОК ЗАДАЧ
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5  # Пагинация по 5 штук

    def get_queryset(self):
        # Показываем ТОЛЬКО задачи текущего пользователя
        qs = super().get_queryset().filter(owner=self.request.user)
        
        # Фильтрация по статусу (если передан параметр ?status=todo)
        status = self.request.GET.get('status')
        if status in ['todo', 'in_progress', 'done']:
            qs = qs.filter(status=status)
            
        return qs

# 2. ПРОСМОТР ОДНОЙ ЗАДАЧИ
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        # Защита: нельзя посмотреть чужую задачу
        return super().get_queryset().filter(owner=self.request.user)

# 3. СОЗДАНИЕ ЗАДАЧИ
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        # Автоматически назначаем владельца - текущего юзера
        form.instance.owner = self.request.user
        return super().form_valid(form)

# 4. РЕДАКТИРОВАНИЕ
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def get_queryset(self):
        # Защита: нельзя редактировать чужую задачу
        return super().get_queryset().filter(owner=self.request.user)

# 5. УДАЛЕНИЕ
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')

    def get_queryset(self):
        # Защита: нельзя удалить чужую задачу
        return super().get_queryset().filter(owner=self.request.user)