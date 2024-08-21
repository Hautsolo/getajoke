from django.db import models
from .user import User
from .joke import Joke


class Comment(models.Model):
    joke = models.ForeignKey(Joke, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]