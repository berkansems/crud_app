from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from tasks.models import Task
from django.urls import reverse
from django.utils import timezone
from tasks.serializers import TaskSerializer
from rest_framework import status

TASK_URL = reverse('task:task-list')


def create_default_task(**params):
    defaults = {
        'title': 'Default Task',
        'price': Decimal('20.25'),
        'due_date': timezone.now(),
    }
    defaults.update(params)
    task = Task.objects.create(**defaults)
    return task


def get_detail_url(task_id):
    return reverse('task:task-detail', args=[task_id])


class TaskApiTests(TestCase):
    '''Test Task api requests'''
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tasks(self):
        create_default_task()
        create_default_task(due_date=timezone.now())
        create_default_task(title='Test Task 2')
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_create_task(self):
        payload = {
            'title': 'Default Task 2',
            'price': Decimal('50.25'),
            'due_date': timezone.now(),
        }
        res = self.client.post(TASK_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=res.data['id'])
        for key, value in payload.items():
            print(getattr(task, key))
            self.assertEqual(getattr(task, key), value)
        self.assertEqual(task.completed, False)

    def test_full_update(self):
        '''Test full update of task'''
        task = create_default_task()
        payload = {
            'title': 'Default Task 2',
            'price': Decimal('50.25'),
            'due_date': timezone.now(),
        }
        url = get_detail_url(task.id)
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(task, key), value)

    def test_partial_update(self):
        task = create_default_task()
        url = get_detail_url(task.id)
        payload = {'completed': True}
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.completed)
        self.assertEqual(task.completed, payload['completed'])

    def test_task_deletion(self):
        task = create_default_task()
        url = get_detail_url(task.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.exists())
