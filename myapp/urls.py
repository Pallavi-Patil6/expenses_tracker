from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('',views.home,name="home"),
    path('login/', views.login_view, name='login'),
     path('register/', views.register_view, name='register'), 
       path('logout/', views.logout_view, name='logout'),

    path('add/', views.add_expense, name='add_expense'),
    path('update/<int:pk>/', views.update_expense, name='update_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),

    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('register/', views.register, name='register'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)