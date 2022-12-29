from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models

from vote.models import Vote


class Comment(models.Model):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                            related_name="comments")

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                related_name="children")   

    date = models.DateTimeField(auto_now_add=True)                                
    content = models.TextField()

    edited = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    vote = GenericRelation(Vote)


    def __str__(self) -> str:
        if not self.parent:
            return f"Comment by {self.user}: {self.content[:20]}"

        return f"Reply by {self.user}: {self.content[:20]}"

    @property
    def is_edited(self):
        return self.edited
    



