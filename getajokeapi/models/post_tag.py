from django.db import models
from .joke import Joke
from .tag import Tag


class PostTag(models.Model):

    joke = models.ForeignKey(Joke, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
