from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('ticker/<str:id>',views.ticker,name='ticker'),
    path('',views.index,name='index'),

    path('account/', views.account, name='account'),
    path('register/', views.registerPg, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='templates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='templates/logout.html'), name='logout'),
    path('test/',views.test,name='test'),
    path('about/',views.about,name = 'about'),
    path('delete/<str:id>',views.delete,name = 'delete'),
    path('suggest/',views.suggest,name = 'suggest'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)