from django.db import models
from profiles.models import UserProfile
from products.models import Product


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

    def __str__(self):
        return (
            f"{self.user_profile.user.username}'s "
            f"wishlist item: {self.product.name}"
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)