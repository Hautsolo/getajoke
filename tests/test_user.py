from rest_framework import status
from rest_framework.test import APITestCase
from getajokeapi.models import User
from getajokeapi.views.userview import UserSerializer

class UserTests(APITestCase):
    fixtures = ['users']  # Loading predefined data

    def setUp(self):
        self.user_data = {
            "name": "test_user",
            "username": "test_username",
            "uid": "testUid123"
        }

    def test_create_user(self):
        """Test creating a new user"""
        url = "/users"
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        new_user = User.objects.last()
        expected = UserSerializer(new_user)
        self.assertEqual(expected.data, response.data)

    def test_get_user(self):
        """Test retrieving a single user"""
        user = User.objects.create(**self.user_data)
        url = f'/users/{user.uid}'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = UserSerializer(user)
        self.assertEqual(expected.data, response.data)

    def test_list_users(self):
        """Test listing all users"""
        User.objects.create(**self.user_data)
        url = "/users"
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), User.objects.count())

    def test_update_user(self):
        """Test updating a user"""
        user = User.objects.create(**self.user_data)
        url = f'/users/{user.id}'

        updated_data = {
            "name": "updated_name",
            "username": "updated_username",
            "uid": "updatedUid123"
        }

        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        user.refresh_from_db()
        self.assertEqual(user.name, updated_data['name'])
        self.assertEqual(user.username, updated_data['username'])
        self.assertEqual(user.uid, updated_data['uid'])

    def test_destroy_user(self):
        """Test deleting a user"""
        user = User.objects.create(**self.user_data)
        url = f'/users/{user.id}'
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(User.objects.filter(id=user.id).exists())
