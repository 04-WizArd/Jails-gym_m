from django.urls import path
from . import views

app_name = 'core'

# du jeudi passee a lundi:20.000 (jeudi vendredi:38000,32000 bierres)
# du mardi a aujourd'hui:22.000
# aujourd'hui: versement de 240$ pour achat 20 sacs ciment et compacteur(8$)

urlpatterns = [ 
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscribe/<int:subscription_id>/', views.subscribe, name='subscribe'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sell_view/<str:view_type>/', views.sell_view, name='sell_view'),
    
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('member/<int:member_id>/', views.member_details, name='member_details'),
]