from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from getajokeapi.models import Tag

class TagTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some initial tags for testing
        cls.tag1 = Tag.objects.create(label="country")
        cls.tag2 = Tag.objects.create(label="city")

    def test_tag_list(self):
        url = reverse('tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We expect 2 tags

    def test_tag_retrieve(self):
        url = reverse('tag-detail', args=[self.tag1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], "country")

    def test_tag_create(self):
        url = reverse('tag-list')
        data = {"label": "new_tag"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 3)  # 2 initial + 1 new
        self.assertEqual(response.data['label'], "new_tag")

    def test_tag_update(self):
        url = reverse('tag-detail', args=[self.tag1.id])
        data = {"label": "updated_tag"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.label, "updated_tag")

    def test_tag_delete(self):
        url = reverse('tag-detail', args=[self.tag1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 1)  # 2 initial - 1 deleted

    def test_tag_retrieve_nonexistent(self):
        url = reverse('tag-detail', args=[999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tag_update_nonexistent(self):
        url = reverse('tag-detail', args=[999])  # Non-existent ID
        data = {"label": "updated_tag"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tag_delete_nonexistent(self):
        url = reverse('tag-detail', args=[999])  # Non-existent ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)