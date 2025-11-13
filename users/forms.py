from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group,Permission
from django import forms
import re

class StyledFormMixin:
    """Mixin to apply style to form fields"""

    default_classes = "text-black border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():

            # ----- TextInput -----
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })

            # ----- Textarea -----
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })

            # ----- SelectDateWidget -----
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500"
                })

            # ----- CheckboxSelectMultiple -----
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })

            # ----- Select -----
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500 mt-3"
                })

            #  ----- Image / File Input -----
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({
                    'class': "block w-full text-sm text-gray-700 border-2 border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:border-green-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-green-100 file:text-green-700 hover:file:bg-green-200",
                })

            # ----- Default case -----
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })



class UserRegisterForm(StyledFormMixin,forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'id':'password'}),label='Passwod')
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'id':'confirm_password'}),label='Confirm Password')
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','confirm_password']

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com' }),
            'password1':forms.PasswordInput(attrs={'placeholder': 'Password' }),
            'confirm_password':forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
            }

    def clean_password1(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('confirm_password')
        errors=[]
        if len(password1) < 8:
             errors.append('password must be 8 caracter')

        if (password1 and password2) and (password1!=password2):
            errors.append('password Ae Not same')

        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    def clean_email(self):
        email=self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('ths email already exists')
        return email
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()
 
        
        
class AssignRoleForm(StyledFormMixin,forms.Form):
    role=forms.ModelChoiceField(queryset=Group.objects.all(),empty_label='Select a Role')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()





class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
    queryset=Permission.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False,
    label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()


class AssignRole(StyledFormMixin,forms.Form):
    role=forms.ModelChoiceField(queryset=Group.objects.all(),empty_label='Select a Role')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()

