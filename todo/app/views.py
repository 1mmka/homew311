from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView 
from django.contrib.auth.models import User
from app.forms import UserRegistrationForm,UserAuthenticationForm,EditTaskForm,CreateTaskForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView,UpdateView,CreateView
from app.models import TodoList
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

# Create your views here.
class UserRegistrationView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
class UserAuthenticationView(LoginView):
    form_class = UserAuthenticationForm
    success_url = reverse_lazy('list-tasks')

class UserLogoutView(LoginRequiredMixin,LogoutView):
    next_page = reverse_lazy('login')
    login_url = reverse_lazy('login')

def ResetUserPasswordView(request):
    if request.method == 'POST':
        email = request.POST.get('email','ne nashel')
        
        if email != 'ne nashel':
            user = User.objects.get(email = email)
            user_token = default_token_generator.make_token(user)
            create_verify_url = request.build_absolute_uri(f'/reset-pass/{user.pk}/{user_token}/')
            
            created_message = '''
            hi {0}
            your password reset url : \n\n{1}
            '''.format(user.username,create_verify_url)
            
            send_mail('reset user password',created_message,'',[str(user.email)])
            return HttpResponse('check your email')
    else:
        return render(request,'reset_password.html')
    
def checkResetDatas(request,user_pk,user_token):
    user = User.objects.get(id=user_pk)
    
    if request.method == 'POST':
        if default_token_generator.check_token(user,user_token) == bool(1):
            sended_new_password = request.POST.get('password1')
            
            user.set_password(sended_new_password)
            user.save()
            
            return redirect('login')
        else:
            return HttpResponse('token checker said error')
    else:
        return render(request,'new_password.html')
    

# Просмотр всех задач у определенного пользователя (в разметке написано условие)
class ListTasks(LoginRequiredMixin,ListView):
    model = TodoList
    template_name = 'view_tasks.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    
    paginate_by = 3
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        data = TodoList.objects.all()
        
        paginator_object = Paginator(data,self.paginate_by) # по 3 записи на одной странице
        page_number = self.request.GET.get('page') # берем номер страницы по ключу ?page в URL страницы
        
        page = paginator_object.get_page(page_number) # берем данные по странице
        context['page'] = page
        
        return context
        
        
# Детальная информация про задание пользователя при нажатии на Action(More Info)
class DetailTaskView(LoginRequiredMixin,DetailView): 
    model = TodoList
    template_name = 'detail_task.html'
    pk_url_kwarg = 'detail_id'
    context_object_name = 'taskInfo'
    login_url = reverse_lazy('login')

# Редактирование задания пользователя
class EditTaskView(LoginRequiredMixin,UpdateView):
    model = TodoList
    form_class = EditTaskForm
    template_name = 'update_task.html'
    pk_url_kwarg = 'update_id'
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        task = TodoList.objects.get(id = self.kwargs['update_id'])
    
        context['task'] = task # чтобы в форме показывать предыдущие значения таска
        context['detail_id'] = self.kwargs['update_id'] # чтобы вернуться к детальному просмотру при нажатии на Back
        
        return context
    
    def get_success_url(self) -> str: # при успешном сохранении перенаправление к детальному просмотру таска
        update_id = self.kwargs['update_id']
        success_url = reverse_lazy('detail-task',kwargs={'detail_id':update_id})
        
        return success_url
    
# Удаление задания пользователя
def DeleteTaskView(request,delete_id):
    task = get_object_or_404(TodoList,id=delete_id)
    task.delete()
    
    return redirect('list-tasks')

# Создание нового таска для пользователя
class CreateTaskView(LoginRequiredMixin,CreateView):
    template_name = 'create_task.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('list-tasks')
    login_url = reverse_lazy('login')
    