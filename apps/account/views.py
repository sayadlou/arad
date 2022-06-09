from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView

from .forms import MyAuthenticationForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm, UserRegisterForm, \
    UserUpdateForm
from .models import UserProfile


class Login(LoginView):
    form_class = MyAuthenticationForm
    template_name = 'account/login.html'


class Logout(LogoutView):
    template_name = 'account/logged_out.html'


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    form_class = MyPasswordChangeForm


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class PasswordReset(PasswordResetView):
    subject_template_name = 'account/password_reset_subject.txt'
    email_template_name = 'account/password_reset_email.html'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    form_class = MyPasswordResetForm


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:password_reset_complete')
    template_name = 'account/password_reset_confirm.html'
    form_class = MySetPasswordForm


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class SignUp(CreateView):
    template_name = 'account/signup.html'
    model = UserProfile
    form_class = UserRegisterForm

    def get_success_url(self):
        login(self.request, self.object)
        return reverse_lazy('account:profile')


class Profile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserUpdateForm
    login_url = reverse_lazy('account:login')
    template_name = "account/profile.html"
    context_object_name = "user"
    success_url = reverse_lazy('account:profile')


    def get_initial(self):
        return self.request.user.__dict__

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data["purchase"] = self.get_user_purchased_item()
        return data

    def get_user_purchased_item(self):
        user_purchased_product = set()
        user_purchased_base_product = self.request.user.productbasemodel_set.all()
        for base_product in user_purchased_base_product:
            user_purchased_product.add(base_product.get_child())
        return user_purchased_product
