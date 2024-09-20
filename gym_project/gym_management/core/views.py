from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Subscription, UserSubscription
from django.utils import timezone
from django.utils.translation import gettext as _


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
user = settings.AUTH_USER_MODEL

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('core:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'core/index.html', {'form': form})

@login_required
def profile(request):
    available_subscriptions = Subscription.objects.all()
    user_subscription = UserSubscription.objects.filter(
        user=request.user, 
        end_date__gte=timezone.now().date(),
        is_active=True
    ).first()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'core/profile.html', {
        'form': form,
        'available_subscriptions': available_subscriptions,
        'user_subscription': user_subscription
        })

@login_required
def subscriptions(request):
    available_subscriptions = Subscription.objects.all()
    user_subscription = UserSubscription.objects.filter(
        user=request.user, 
        end_date__gte=timezone.now().date(),
        is_active=True
    ).first()
    return render(request, 'core/subscriptions.html', {
        'available_subscriptions': available_subscriptions,
        'user_subscription': user_subscription
    })


@login_required
def subscribe(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    # Désactiver tous les abonnements actifs existants
    UserSubscription.objects.filter(
        user=request.user, 
        is_active=True
    ).update(is_active=False, end_date=timezone.now().date())
    
    # Créer le nouvel abonnement
    start_date = timezone.now().date()
    if subscription.duration == 'W':
        end_date = start_date + timezone.timedelta(weeks=1)
    elif subscription.duration == 'M':
        end_date = start_date + timezone.timedelta(days=30)
    else:  # Yearly
        end_date = start_date + timezone.timedelta(days=365)
    
    UserSubscription.objects.create(
        user=request.user,
        subscription=subscription,
        start_date=start_date,
        end_date=end_date,
        is_active=True
    )
    messages.success(request, _("Vous avez souscrit avec succès à l'abonnement {}.").format(subscription.name))
    return redirect('core:subscriptions')

@login_required
def cancel_subscription(request):
    user_subscription = get_object_or_404(UserSubscription, user=request.user, is_active=True, end_date__gte=timezone.now().date())
    
    if request.method == 'POST':
        user_subscription.is_active = False
        user_subscription.end_date = timezone.now().date()
        user_subscription.save()
        messages.success(request, _("Votre abonnement a été résilié avec succès."))
        return redirect('core:profile')
    
    return render(request, 'core/cancel_subs.html', {'subscription': user_subscription})

# supprimer completemet l'abonnemet
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
# from django.contrib import messages
# from django.utils import timezone
# from django.utils.translation import gettext as _
# from .models import UserSubscription

# @login_required
# def cancel_subscription(request):
#     user_subscriptions = UserSubscription.objects.filter(
#         user=request.user, 
#         end_date__gte=timezone.now().date()
#     )
    
#     if not user_subscriptions.exists():
#         messages.warning(request, _("Vous n'avez pas d'abonnement actif à résilier."))
#         return redirect('core:subscriptions')
    
#     if request.method == 'POST':
#         deleted_count = user_subscriptions.delete()[0]
#         if deleted_count > 0:
#             messages.success(request, _("Votre abonnement a été résilié et supprimé avec succès."))
#         else:
#             messages.error(request, _("Une erreur s'est produite lors de la résiliation de votre abonnement."))
#         return redirect('core:subscriptions')
    
#     return render(request, 'core/cancel_subscription.html', {'subscriptions': user_subscriptions})
####
# def superuser_required(user):
#     return user.is_superuser

# @login_required
# @user_passes_test(superuser_required)

def sell_view(request, view_type):
    if view_type == 'cardio':
        return render(request, 'core/cardio.html')  # Template pour le profil
    elif view_type == 'collectif':
        return render(request, 'core/collectif.html')  # Template pour les abonnements
    elif view_type == 'group':
        return render(request, 'core/group.html')
    elif view_type == 'personal':
        return render(request, 'core/perso.html')

@login_required
def member_details(request, member_id):
    subscription = UserSubscription.objects.get(user__id=member_id)
    return render(request, 'core/member_details.html', {'subscription': subscription})



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie.")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('/')