from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models

from votes.models import Vote


class Comment(models.Model):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                            related_name="comments")

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                related_name="children")   

    date = models.DateTimeField(auto_now_add=True)                                
    body = models.TextField()

    is_edited = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # TODO update votes for comments
    # votes = GenericRelation(Vote)

    def __str__(self) -> str:
        if not self.parent:
            return f"Comment by {self.user}: {self.content[:20]}"

        return f"Reply by {self.user}: {self.content[:20]}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.is_edited = True
            return super().save(*args, **kwargs)
    



