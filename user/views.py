import datetime
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.views.generic.base import TemplateView

from .forms import UserRoleForm, UserProfileForm
from .models import UserRole, UserProfile
from core.mixin import MunicipalityAdministratorMixin
from core.models import HouseSetting, Municipality, Country, Province
from utils.helpers import get_lower_level_groups_only, get_lower_level_users_only, country_level_user_name, \
    district_level_user_name, province_level_user_name, get_lower_level_user_roles_only
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from utils.helpers import is_in_municipality_group, is_in_ward_group

User = get_user_model()

success_message = 'success'
failure_message = 'failure'


class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = "users/confirm-user-delete.html"
    success_url = "/user/list"
    model = User
    permission_required = 'auth.delete_user'


class AssignUserRole(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
        Assign a role to a user.
        'get_form_kwargs()' is passing the currently logged in user to the UserRoleForm.
        This makes sure that while assigning a role to a user for a municipality/ward, the authenticated user cannot
        see other municipality/ward he/she is not a part of.
    """
    form_class = UserRoleForm
    template_name = "users/assign-user.html"
    success_url = "/user/role/list"
    permission_required = 'user.change_userrole'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user_id': self.request.user.id})
        return kwargs


class UnassignUserRole(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
        Remove a user role of an user from a municipality or ward.
        Won't actually remove the user role but will set ended_at to the removed date.
    """
    template_name = "src/components/confirm_delete.html"
    model = UserRole
    success_url = "/user/role/list"
    permission_required = 'user.delete_userrole'

    # def get_object(self, *args, **kwargs):
    #     return get_object_or_404(self.model, pk=self.kwargs.get('pk'))
    #
    # def get(self, request, *args, **kwargs):
    #     role = UserRole.objects.get(id=self.kwargs.get('pk'))
    #     role.delete()
    #     return HttpResponseRedirect(reverse('user-roles-list'))


class ListUserRole(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
        List user according to the roles assigned to a municipality or ward.
    """
    model = UserRole
    template_name = "users/roles-list.html"
    context_object_name = "roles"
    permission_required = 'user.view_userrole'
    order_by = '-started_at'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return UserRole.objects.filter(ended_at__isnull=True)
        else:
            return get_lower_level_user_roles_only(self.request.user)


class EditUserProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
        Edit the profile of logged in user.
    """
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = "/user/profile/edit"
    # success_message = " %(middle_name)'s User Profile was updated successfully!"
    success_message = "User Profile %(middle_name)s was Updated successfully"

    def get_object(self, *args, **kwargs):
        user_profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return user_profile

    def form_valid(self, form):
        first_name = self.request.POST.get('first_name', '')
        last_name = self.request.POST.get('last_name', '')
        # status = self.request.POST.get('status', '')
        user = self.request.user
        changed = False
        if not user.first_name == first_name:
            user.first_name = first_name
            changed = True
        if not user.last_name == last_name:
            user.last_name = last_name
            changed = True
        if changed:
            user.save()

        return super().form_valid(form)


@permission_required('auth.change_user')
def edit_user_status(request, pk):
    if request.method == "POST":
        user_status = request.POST.get('user_status')
        user = User.objects.get(id=pk)
        user.is_active = user_status
        user.save()
        messages.info(request, message="Status Updated!", extra_tags=success_message)
        return HttpResponseRedirect("/user/list")
    else:
        return HttpResponseRedirect("/user/list")


@permission_required('auth.add_user')
def create_user(request):
    country = Country.objects.last()
    provinces = Province.objects.filter(country=country)
    if request.user.is_superuser:
        municipalities = Municipality.objects.all()
    else:
        municipalities = Municipality.objects.filter(roles__user_id=request.user.id)
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = get_lower_level_groups_only(request.user)
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        user_country = request.POST.get("country", "")
        province = request.POST.get("province", "")
        district = request.POST.get("district", "")
        municipality = request.POST.get("municipality", "")
        ward = request.POST.get("ward", "")
        group = request.POST.get("group", "")
        if username == "":
            error = "Username required"
            return render(request, "users/add-user.html", {
                "error": error,
                "username": username,
                "email": email,
                'municipality': municipalities,
                'groups': groups,
                'country': country,
                'provinces': provinces
            })
        if password == "":
            error = "Password required"
            return render(request, "users/add-user.html", {
                "error": error,
                "username": username,
                "email": email,
                'municipality': municipalities,
                'groups': groups,
                'country': country,
                'provinces': provinces
            })
        if password != password2:
            error = "Password mismatch"
            return render(request, "users/add-user.html", {
                "error": error,
                "username": username,
                "email": email,
                'municipality': municipalities,
                'groups': groups,
                'country': country,
                'provinces': provinces
            })
        if User.objects.filter(Q(username=username) | Q(email=email)).exists() and not email == "":
            error = "User with this email or username already exists."
            return render(request, "users/add-user.html", {
                "error": error,
                "username": username,
                "email": email,
                'municipality': municipalities,
                'groups': groups,
                'country': country,
                'provinces': provinces
            })
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)

            user.save()
            try:
                group_obj = Group.objects.get(id=group)
                # user.groups = group_obj
                group_obj.user_set.add(user)
            except:
                if ward:
                    UserRole.objects.create(user=user, municipality_id=municipality, ward_id=ward, group_id=group)
                else:
                    UserRole.objects.create(user=user, municipality_id=municipality, group_id=group)
            if group_obj.name == country_level_user_name:
                UserRole.objects.create(user=user, country_id=user_country, group_id=group)
            elif group_obj.name == province_level_user_name:
                UserRole.objects.create(user=user, country_id=user_country, group_id=group, province_id=province)
            elif group_obj.name == district_level_user_name:
                UserRole.objects.create(
                    user=user,
                    country_id=user_country,
                    group_id=group,
                    province_id=province,
                    district_id=district)
            elif is_in_municipality_group(group_obj.name):
                UserRole.objects.create(user=user, municipality_id=municipality, group_id=group)
            elif is_in_ward_group(group_obj.name):
                    UserRole.objects.create(user=user, municipality_id=municipality, ward_id=ward, group_id=group)
            else:
                if isinstance(ward, int):
                    UserRole.objects.create(user=user, municipality_id=municipality, ward_id=ward, group_id=group)
                else:
                    UserRole.objects.create(user=user, municipality_id=municipality, group_id=group)
            return HttpResponseRedirect("/user/list")
    else:
        return render(request, "users/add-user.html", {
            'municipality': municipalities,
            'groups': groups,
            'country': country,
            'provinces': provinces
        })


def user_creation_invalid_response(error, request, username, email, municipalities, groups, country, provinces):
    error = error
    return render(request, "users/add-user.html", {
        "error": error,
        "username": username,
        "email": email,
        'municipality': municipalities,
        'groups': groups,
        'country': country,
        'provinces': provinces
    })


class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    all the admin users above 'municipality administrator including 'municipality administrator'
    itself has this permission'
    """
    model = User
    context_object_name = "users"
    template_name = "users/user-list.html"
    permission_required = 'auth.view_user'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            users = User.objects.filter(Q(is_superuser=True) | Q(id=-1)).values_list('id', flat=True)
            queryset = User.objects.filter(~Q(id__in=list(users))).order_by('-date_joined')
        else:
            # municipality = self.request.user.roles.municipality
            # if municipality:
            #     queryset = User.objects.filter(roles__municipality=municipality)
            # else:
            #     qumunicipalityeryset = None
            queryset = get_lower_level_users_only(self.request.user)
        return queryset
