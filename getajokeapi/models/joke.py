from django.db import models
from .user import User
from .tag import Tag

class Joke(models.Model):
    content = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', through='PostTag')
    upvotes_count = models.IntegerField(default=0)  # Track upvotes as an integer
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

    def upvote(self):
        """Increments the upvotes_count by 1"""
        self.upvotes_count += 1
        self.save()
