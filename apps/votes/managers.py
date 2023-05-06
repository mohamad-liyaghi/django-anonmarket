from django.db import models


class VoteManager(models.Manager):
    '''Count the likes of an object'''
    
    def likes(self):
        return self.filter(vote="l").count()
    
    def dislikes(self):
        return self.filter(vote="d").count()