from django.urls import path
from .views import sign_in,sign_up,activate_user,sign_out,create_group,assign_role,group_list,user_list,update_group,delete_group

app_name='users'
urlpatterns = [
    path("sign-out/",sign_out, name="sign-out"),
    path('activate/<int:id>/<str:token>/',activate_user),
    path('sign-in/',sign_in,name='sign-in'),
    path('sign-up/',sign_up,name='sign-up'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/update-group/<int:group_id>/',update_group,name='update-group'),
    path('admin/delete-group/<int:group_id>/',delete_group,name='delete-group'),
    path('admin/<int:user_id>/assign-role',assign_role,name='assign-role'),
    path('admin/group-list',group_list,name='group-list'),
    path('admin/user-list',user_list,name='user-list'),
]
