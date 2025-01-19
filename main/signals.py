from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import User  

@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def clear_user_cache(sender,instance, **kwargs):
    cache.delete('users') 
    cache.delete(f'user_{instance.id}') 
