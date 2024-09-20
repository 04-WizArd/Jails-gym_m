from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    postnom = models.CharField(_("Post-nom"), max_length=100, blank=True)
    address = models.TextField(_("Adresse"), blank=True)

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")

class Subscription(models.Model):
    SUBSCRIPTION_TYPES = [
        ('W', _('Hebdomadaire')),
        ('M', _('Mensuel')),
        ('Y', _('Annuel')),
    ]
    name = models.CharField(_("Nom"), max_length=100)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Prix [$]"), max_digits=10, decimal_places=2)
    duration = models.CharField(_("Durée"), max_length=1, choices=SUBSCRIPTION_TYPES)
    
    def __str__(self):
        return f"{self.name} - {self.get_duration_display()} ({self.price}$)"

    class Meta:
        verbose_name = _("Abonnement")
        verbose_name_plural = _("Abonnements")

class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=_("Utilisateur"), on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, verbose_name=_("Abonnement"), on_delete=models.CASCADE)
    start_date = models.DateField(_("Date de début"))
    end_date = models.DateField(_("Date de fin"))
    paid = models.BooleanField(_("Payé"), default=False)
    is_active = models.BooleanField(_("Actif"), default=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription.name} ({'Payé' if self.paid else 'Non payé'})"

    class Meta:
        verbose_name = _("Abonnement utilisateur")
        verbose_name_plural = _("Abonnements utilisateurs")