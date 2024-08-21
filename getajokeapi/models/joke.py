from django.db import models
from .user import User
from .tag import Tag

class Joke(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name='upvoted_jokes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through='PostTag', related_name='posts')

    @property
    def user_id(self):
        return self.user.id
    
    def __str__(self) -> str:
        return self.content[:50]

    def get_upvote_count(self):
        return self.upvotes.count()

    def upvote(self, user):
        """Add an upvote from a user if they haven't already upvoted."""
        if not self.upvotes.filter(id=user.id).exists():
            self.upvotes.add(user)
            self.save()
            return True
        return False
