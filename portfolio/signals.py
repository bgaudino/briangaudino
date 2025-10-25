from django.core.cache import cache
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from portfolio import models

models_to_clear_cache_for = [
    model
    for model in models.__dict__.values()
    if isinstance(model, type)
    and issubclass(model, Model)
    and model is not models.Contact
]


@receiver(post_save)
def clear_cache(sender, **kwargs):
    if sender in models_to_clear_cache_for:
        cache.clear()
