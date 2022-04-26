from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *


urlpatterns = [
    path('assign-role/', AssignUserRole.as_view(), name="assign-user-role"),
    path('unassign-role/<int:pk>', UnassignUserRole.as_view(), name="unassign-user-role"),
    path('role/list/', ListUserRole.as_view(), name="user-roles-list"),
    path('add/', login_required(create_user), name="create-user"),
    path('list/', UserList.as_view(), name="user-list"),

    path('edit-status/<int:pk>', edit_user_status, name="user-status-edit"),
    path('profile/edit', EditUserProfile.as_view(), name="profile-edit"),
    path('delete/<int:pk>', DeleteUser.as_view(), name="delete-user"),
]
