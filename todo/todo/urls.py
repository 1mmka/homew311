from django.contrib import admin
from django.urls import path
from app.views import UserAuthenticationView,UserRegistrationView,ResetUserPasswordView,checkResetDatas,ListTasks,UserLogoutView,DetailTaskView,EditTaskView,DeleteTaskView,CreateTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',UserAuthenticationView.as_view(),name='login'),
    path('register',UserRegistrationView.as_view(),name='register'),
    path('reset-password',ResetUserPasswordView,name='reset-password'),
    path('reset-pass/<int:user_pk>/<str:user_token>/',checkResetDatas,name='check-datas'),
    path("logout/",UserLogoutView.as_view(), name="logout"),
    
    # todo - paths
    
    path('list-tasks/',ListTasks.as_view(),name='list-tasks'),
    path('detail-task/<int:detail_id>',DetailTaskView.as_view(),name='detail-task'),
    path('update-task/<int:update_id>',EditTaskView.as_view(),name='update-task'),
    path('delete-task/<int:delete_id>',DeleteTaskView,name='delete-task'),
    path('create-task/',CreateTaskView.as_view(),name='create-task'),
]
