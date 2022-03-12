from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Item
# @receiver(post_save, sender=Item)
# def item_created(sender, instance, created, **kwargs):
#     if created:
      
#         Item.objects.create(item=instance)
       
        

@receiver(post_save, sender=Item)
def save_item_slug(sender, instance, **kwargs):
        if instance.slug=="":
            post_save.disconnect(save_item_slug, sender=sender)
            instance.slug=instance.title + '-' + str(instance.id)
            instance.save()
            post_save.connect(save_item_slug, sender=sender)

        
    