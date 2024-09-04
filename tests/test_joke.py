from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from getajokeapi.models import Joke, User, Tag

class JokeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name="Test User", username="testuser", uid="12345")
        self.tag1 = Tag.objects.create(label="Science")
        self.tag2 = Tag.objects.create(label="Puns")
        self.joke1 = Joke.objects.create(
            content="Why don't scientists trust atoms? Because they make up everything!",
            user=self.user
        )
        self.joke1.tags.add(self.tag1, self.tag2)

    def test_joke_list(self):
        url = reverse('jokes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_joke_create(self):
        url = reverse('jokes-list')
        data = {
            'content': 'Test joke',
            'uid': self.user.uid,  # Use uid instead of user id
            'tags': [self.tag1.id],
            'newTags': ['Funny']  # Add a new tag
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # Keep this for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Joke.objects.count(), 2)
        self.assertEqual(Joke.objects.last().content, 'Test joke')

    def test_joke_retrieve(self):
        url = reverse('jokes-detail', args=[self.joke1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_joke_update(self):
        url = reverse('jokes-detail', args=[self.joke1.id])
        data = {
            'content': 'Updated joke content',
            'tags': [self.tag1.id],
            'newTags': ['New Tag']
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.joke1.refresh_from_db()
        self.assertEqual(self.joke1.content, 'Updated joke content')

    def test_joke_delete(self):
        url = reverse('jokes-detail', args=[self.joke1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Joke.objects.count(), 0)

    def test_joke_upvote(self):
        url = reverse('joke-upvote', args=[self.joke1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.joke1.refresh_from_db()
        self.assertEqual(self.joke1.upvotes_count, 1)