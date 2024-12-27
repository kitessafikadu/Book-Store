from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

handler404 = 'bookstore.views.custom_404_view'

urlpatterns = [

# Forgor password URL's
  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

# Shared URL's
 path('', views.login_form, name='home'),
 path('login/', views.loginView, name='login'),
 path('logout/', views.logoutView, name='logout'),
 path('regform/', views.register_form, name='regform'),
 path('register/', views.registerView, name='register'),
 path('profile/', views.profile, name='profile'),
 path('profile/update/', views.update_profile, name='update_profile'),

 # Publisher URL's
 path('books/', views.books_by_category, name='books_by_category'),

 path('publisher/', views.UBookListView.as_view(), name='publisher'),
 path('uabook_form/', views.uabook_form, name='uabook_form'),
 path('uabook/', views.uabook, name='uabook'),
 path('ucchat/', views.UCreateChat.as_view(), name='ucchat'),
 path('ulchat/', views.UListChat.as_view(), name='ulchat'),
 path('request_form/', views.request_form, name='request_form'),
 path('delete_request/', views.delete_request, name='delete_request'),
 path('feedback_form/', views.feedback_form, name='feedback_form'),
 path('send_feedback/', views.send_feedback, name='send_feedback'),
 path('about/', views.about, name='about'),
 path('usearch/', views.usearch, name='usearch'),


 # Admin URL's
 path('dashboard/', views.dashboard, name='dashboard'),
 path('acchat/', views.ACreateChat.as_view(), name='acchat'),
 path('alchat/', views.AListChat.as_view(), name='alchat'),
 path('aabook_form/', views.aabook_form, name='aabook_form'),
 path('aabook/', views.aabook, name='aabook'),
 path('albook/', views.ABookListView.as_view(), name='albook'),
 path('ambook/', views.AManageBook.as_view(), name='ambook'),
 path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),
 path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
 path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
 path('adrequest/', views.ADeleteRequest.as_view(), name='adrequest'),
 path('afeedback/', views.AFeedback.as_view(), name='afeedback'),
 path('asearch/', views.asearch, name='asearch'),
 path('adbookk/<int:pk>', views.ADeleteBookk.as_view(), name='adbookk'),
 path('create_user_form/', views.create_user_form, name='create_user_form'),
 path('user_list/', views.ListUserView.as_view(), name='aluser'),
 path('create_use/', views.create_user, name='create_user'),
 path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
 path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
 path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
]

