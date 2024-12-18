from uuid import (
    uuid4,
)

from django.urls.base import (
    reverse,
)
from django.utils import (
    timezone,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITestCase,
)

from edu_async_tasks.core.models import (
    AsyncTaskStatus,
    AsyncTaskType,
    RunningTask,
)


class RunningTaskViewsetTestCase(APITestCase):

    def setUp(self) -> None:
        self.list_url = reverse('async-tasks-list')

        self.task_types = AsyncTaskType.get_model_enum_values()
        self.task_statuses = AsyncTaskStatus.get_model_enum_values()

        self.tasks = [
            RunningTask(
                id=uuid4(),
                name=f'edu_async_tasks.core.tasks.Foo{idx:02d}',
                task_type_id=self.task_types[idx].key,
                description=f'Задача номер {idx:02d}',
                status_id=self.task_statuses[idx].key,
                queued_at=timezone.now(),
                options=None,
            ) for idx in range(10)
        ]

        RunningTask.objects.bulk_create(self.tasks)

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)

        self.assertEqual(len(response.data['results']), len(self.tasks))

    def test_list_ordering(self):
        for param in ('queued_at', 'description', 'name', 'status'):
            with self.subTest(param):
                response1 = self.client.get(self.list_url, {'ordering': param})
                response2 = self.client.get(self.list_url, {'ordering': f'-{param}'})

                for response in (response1, response2):
                    self.assertEqual(len(response.data['results']), len(self.tasks))

                self.assertEqual(response1.data['results'], list(reversed(response2.data['results'])))

    def test_list_filtering(self):
        task = self.tasks[0]

        expected_result = self.client.get(reverse('async-tasks-detail', args=[task.id])).data

        response = self.client.get(self.list_url, {'queued_at': task.queued_at.date()})
        self.assertEqual(len(response.data['results']), 10)
        self.assertIn(expected_result, response.data['results'])

        response = self.client.get(self.list_url, {'name': task.name})
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn(expected_result, response.data['results'])

        response = self.client.get(self.list_url, {'status': task.status.key})
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn(expected_result, response.data['results'])
