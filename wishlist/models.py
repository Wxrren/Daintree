from django.db import models
from profiles.models import UserProfile
from products.models import Product

from django.core.exceptions import ValidationError


class Wishlist(models.Model):
    """
    A model for handling user wishlists.
    """
    class Meta:
        verbose_name_plural = 'Wishlists'

    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wishlists'
    )
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s wishlist"

    def clean(self):
        if self.pk:
            existing_wishlist = Wishlist.objects.filter(
                user_profile=self.user_profile,
                product=self.product).exclude(pk=self.pk)
            if existing_wishlist.exists():
                raise ValidationError(
                    "A wishlist entry for this product already exists."
                    )
        else:
            existing_wishlist = Wishlist.objects.filter(
                user_profile=self.user_profile,
                product=self.product
                )
            if existing_wishlist.exists():
                raise ValidationError(
                    "This product is already in your wishlist."
                    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        pass
