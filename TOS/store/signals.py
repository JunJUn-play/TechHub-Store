from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    """Signal handler for when an order is created."""
    if created:
        print(f"Order {instance.id} created for user {instance.customer.username}")