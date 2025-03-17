from django.urls import path

from users.views import ChangePassword,CustomLoginView,ProfileView,PasswordReset,PasswordResetConfirm,EditProfileView,ActiveUser,AdminDashboard,AssignRole,CreateGroup,GroupList,SignUpView

from django.contrib.auth.views import LogoutView,PasswordChangeDoneView


urlpatterns = [
    path('sign-up/',SignUpView.as_view(), name='sign-up'),
    # path('sign-in/',sign_in, name='sign-in'),
    path('sign-in/',CustomLoginView.as_view(), name='sign-in'),
    # path('sign-out/',sign_out, name='logout'),
    path('sign-out/',LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/',ActiveUser.as_view()),
    path('admin/dashboard',AdminDashboard.as_view(), name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/',AssignRole.as_view(), name='assign-role'),
    path('admin/create-group/', CreateGroup.as_view(), name='create-group'),
    path('admin/group-list/', GroupList.as_view(), name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/',ChangePassword.as_view(), name='password_change'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset', PasswordReset.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
]
