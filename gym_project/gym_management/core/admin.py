from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Subscription, UserSubscription
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'postnom', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'postnom', 'email', 'address')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'postnom')
    ordering = ('username',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'get_duration_display']
    list_filter = ['duration']
    search_fields = ['name', 'description']

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'start_date', 'end_date', 'paid', 'is_active']
    list_filter = ['subscription', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email', 'subscription__name']
    raw_id_fields = ['user', 'subscription']
    date_hierarchy = 'start_date'
    # list_editable = ['paid']  # Permet de modifier le statut de paiement directement depuis la liste
    
    fieldsets = (
        (None, {
            'fields': ('user', 'subscription', 'start_date', 'end_date')
        }),
        (_('Statut de paiement'), {
            'fields': ('paid',),
            'description': _("Cochez cette case si l'abonnement a été payé.")
        }),
        (_('Statut de l\'abonnement'), {
            'fields': ('is_active',),
            'description': _("Decocher la case pour resilier l'abonnement de ce membre.")
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Édition d'un objet existant
            return ('user', 'subscription', 'start_date', 'end_date')
        return ()  # Pas de champs en lecture seule lors de la création