from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_login(self):
        self.client.post(self.register_url, self.user_data)
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        def test_invalid_login(self):
            response = self.client.post(self.token_url, {
                'email': 'wrong@example.com',
                'password': 'wrongpass'
            })
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn('detail', response.data) 


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        
        self.task1 = Task.objects.create(
            title='Task 1',
            description='Description 1',
            user=self.user,
            status='New'
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            description='Description 2',
            user=self.other_user,
            status='Active Task'
        )
        
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', kwargs={'pk': self.task1.id})
        self.complete_url = reverse('task-complete', kwargs={'pk': self.task1.id})
        
        token_response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'user@example.com',
            'password': 'testpass123'
        })
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_tasks_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'New'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.last().user, self.user)

    def test_update_task(self):
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'Active Task'
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1) 

    def test_complete_task_action(self):
        response = self.client.post(self.complete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'Done')

    def test_cannot_access_other_users_task(self):
        other_task_url = reverse('task-detail', kwargs={'pk': self.task2.id})
        response = self.client.get(other_task_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_status(self):
        Task.objects.create(
            title='Task 3',
            description='Description 3',
            user=self.user,
            status='Done'
        )
        
        response = self.client.get(self.list_url, {'status': 'Done'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'Done')


class AdminTaskTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='userpass123'
        )
        
        Task.objects.create(
            title='Admin Task',
            description='Admin Description',
            user=self.admin,
            status='New'
        )
        Task.objects.create(
            title='User Task',
            description='User Description',
            user=self.user,
            status='Active Task'
        )
        
        token_response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'admin@example.com',
            'password': 'adminpass123'
        })
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.list_url = reverse('task-list')

    def test_admin_sees_all_tasks(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) 




        