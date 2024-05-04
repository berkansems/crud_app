from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from tasks.models import Task


def create_default_task(**params):
    defaults = {
        'title': 'Default Task',
        'price': Decimal('20.25'),
        'due_date': timezone.now() + timedelta(days=5),
    }
    defaults.update(params)
    task = Task.objects.create(**defaults)
    return task


class ModelTests(TestCase):

    def test_create_task(self):
        task = Task.objects.create(
            title='Test Task',
            price=Decimal('10.50'),
            due_date=timezone.now(),
        )
        self.assertEqual(str(task), 'Test Task')
