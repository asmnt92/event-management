from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .forms import UserRegisterForm,CreateGroupForm,AssignRole
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test, permission_required
from event_app.views import is_admin
from django.db.models import Prefetch

# Create your views here.
def sign_up(request):
    form=UserRegisterForm()
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            

            return redirect('users:sign-in')
            
    return render(request,'registation/sign-up.html',{'form':form})

def sign_in(request):
    if request.method=='POST':
        u=request.POST.get('username',None)
        p=request.POST.get('password',None)

        user=authenticate(request=request,username=u,password=p)
        if user:
            login(request,user)
            return redirect('guest-page')
        messages.error(request,'Invalid Username or Password')
    return render(request,'registation/sign-in.html')


def activate_user(request,id,token):
    try:
        user=User.objects.get(id=id)
        if default_token_generator.check_token(user,token):
            if not user.is_active:
                user.is_active=True
                user.save()
            return redirect('users:sign-in')
        else:
            return HttpResponse('Invalid User and Token')
        
    except Exception as e:
        return HttpResponse(f"invalid user ")
    
    
@login_required(login_url='users:sign-in')
def sign_out(request):
    logout(request)

    return redirect('users:sign-in')

@login_required(login_url='users:sign-in')   
@user_passes_test(is_admin,login_url='guest-page')
def create_group(request):
    form=CreateGroupForm()

    if request.method=='POST':
        form=CreateGroupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Successfully group Created')
            return redirect('users:group-list')
    
    context={
        'forms':form,
        'role':'Admin',
        'page':'create-group'
    }
    return render(request,'group/create-group.html',context)

@login_required(login_url='users:sign-in')   
@user_passes_test(is_admin,login_url='guest-page')
def update_group(request,group_id):
    group=Group.objects.get(id=group_id)
    form=CreateGroupForm(instance=group)

    if request.method=='POST':
        form=CreateGroupForm(request.POST,instance=group)

        if form.is_valid():
            form.save()
            messages.success(request,f'Successfully {group.name} group Updated')
            return redirect('users:group-list')
    
    context={
        'forms':form,
        'role':'Admin',

    }
    return render(request,'group/create-group.html',context)


@login_required(login_url='users:sign-in')   
@user_passes_test(is_admin,login_url='guest-page')
def delete_group(request,group_id):
    try:
        group=Group.objects.get(id=group_id)
        group.delete()
        messages.success(request,f'Successfully  group Deleted')
    except Group.DoesNotExist as e:
        messages.error(request,f'This  {e}')

   
    return redirect('users:group-list')
    


@login_required(login_url='users:sign-in')   
@user_passes_test(is_admin,login_url='guest-page')
def assign_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignRole(initial={'role': user.groups.first()})
    if request.method=='POST':
        form=AssignRole(request.POST)
        if form.is_valid():
            
            group=form.cleaned_data
            user.groups.clear()
            user.groups.add(group['role'])
            messages.success(request,f'Successfully user:{user.first_name} role Assigned')
            return redirect('users:user-list')
        
    context={
        'forms':form,
        'role':'Admin'
    }
            
    return render(request,'group/assign-role.html',context)

@login_required(login_url='users:sign-in')   
@user_passes_test(is_admin,login_url='guest-page')
def group_list(request):
    groups=Group.objects.prefetch_related('permissions').all()

    context={
        'groups':groups,
        'role':'Admin',
        'page':'group-list'
    }
    return render(request,'group/group-list.html',context)

@login_required(login_url='users:sign-in')   
@user_passes_test(is_admin,login_url='guest-page')
def user_list(request):
    users=User.objects.prefetch_related('groups').all().order_by('-date_joined')


    context={
        'users':users,
        'role':'Admin',
        'page':'user-list'
    }
    return render(request,'user/user-list.html',context)