from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from getajokeapi.models import Comment, User, Joke, Tag

class CommentTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create(username="testuser", name="Test User", uid="12345")
        
        # Create a test joke
        cls.joke = Joke.objects.create(content="Test joke", user=cls.user)
        
        # Create some tags
        cls.tag1 = Tag.objects.create(label="Science")
        cls.tag2 = Tag.objects.create(label="Funny")
        
        # Add tags to the joke
        cls.joke.tags.add(cls.tag1, cls.tag2)
        
        # Create some test comments
        Comment.objects.create(joke=cls.joke, user=cls.user, content="This joke is hilarious!")
        Comment.objects.create(joke=cls.joke, user=cls.user, content="I couldn't stop laughing!")

    def test_comment_list(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We expect 2 comments

    def test_comment_list_for_specific_joke(self):
        url = reverse('comment-list')
        response = self.client.get(url, {'joke_id': self.joke.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both comments are for our test joke

    def test_comment_retrieve(self):
        comment = Comment.objects.first()
        url = reverse('comment-detail', args=[comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "This joke is hilarious!")

    def test_comment_create(self):
        url = f"{reverse('comment-list')}?joke_id={self.joke.id}"
        data = {
            "content": "New test comment",
            "user_id": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)  # 2 initial + 1 new
        self.assertEqual(response.data['content'], "New test comment")

    def test_comment_create_without_joke_id(self):
        url = reverse('comment-list')
        data = {
            "content": "New test comment",
            "user_id": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update(self):
        comment = Comment.objects.first()
        url = reverse('comment-detail', args=[comment.id])
        data = {
            "content": "Updated comment content"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "Updated comment content")

    def test_comment_delete(self):
        comment = Comment.objects.first()
        url = reverse('comment-detail', args=[comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1)  # 2 initial - 1 deleted

    def test_comment_create_invalid_user(self):
        url = f"{reverse('comment-list')}?joke_id={self.joke.id}"
        data = {
            "content": "New test comment",
            "user_id": 9999  # Non-existent user ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_create_invalid_joke(self):
        url = f"{reverse('comment-list')}?joke_id=9999"  # Non-existent joke ID
        data = {
            "content": "New test comment",
            "user_id": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)