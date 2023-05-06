from django.db import models


class VoteManager(models.Manager):
    '''Count the Upvotes and downvotes'''
    
    def upvotes_count(self):
        return self.filter(choice="u").count()
    
    def downvotes_count(self):
        return self.filter(choice="d").count()