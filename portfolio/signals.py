from django.core.cache import cache
from django.db.models import Model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ai_chat.prompts.models import SystemPrompt

from portfolio import models
from portfolio.constants import AI_CHAT_CACHE_KEY

models_to_clear_cache_for = [
    model
    for model in models.__dict__.values()
    if isinstance(model, type)
    and issubclass(model, Model)
    and model is not models.Contact
]


@receiver([post_save, post_delete])
def clear_cache(sender, **kwargs):
    if sender in models_to_clear_cache_for:
        cache.clear()


@receiver([post_save, post_delete], sender=SystemPrompt)
def clear_ai_chat_cache(sender, instance, **kwargs):
    cache.delete(AI_CHAT_CACHE_KEY)
