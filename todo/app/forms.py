from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from app.models import TodoList,Category
from django.forms import ModelForm

class UserRegistrationForm(UserCreationForm): # форма для регистрации пользователя
    username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    
    password1 = forms.CharField(
        label="Password",
        strip=False, # не будем удалять символы-пробел
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'}),
        strip=False,
    )
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        
class UserAuthenticationForm(AuthenticationForm): # для аутентификации пользователя
    class Meta:
        model = User
        fields = ('username','password')
        
# форма для изменения задачи
class EditTaskForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                widget=forms.widgets.Select(attrs={'size':5})) # чтобы выбрать можно было из 5 вариантов
    class Meta:
        model = TodoList
        fields = ['title','content','due_date','category']

# форма для создания задачи
class CreateTaskForm(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                widget=forms.widgets.Select(attrs={'size':5}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                widget=forms.widgets.Select(attrs={'size':5}))
    class Meta:
        model = TodoList
        fields = ('title','content','created','due_date','category','user')
        
    widgets = {
        'created': forms.DateInput(attrs={'type': 'date'}),
    }