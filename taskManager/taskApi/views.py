# taskApi/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
import pandas as pd
import os
from rest_framework.decorators import action
from rest_framework import status
from django.conf import settings

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # upload excel
    @action(detail=False, methods=['POST'])
    def upload_excel(self, request):
        # Print debugging information
        print(f"Keys in request.FILES: {request.FILES.keys()}")

        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            file_path = os.path.join(settings.MEDIA_ROOT, excel_file.name)

            # Print debugging information
            print(f"File path: {file_path}")

            with open(file_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)

            df = pd.read_excel(file_path)

            # Print column names
            print(f"Column names in Excel file: {df.columns}")

            tasks = []

            for index, row in df.iterrows():
                print(f"Row {index}: {row}")
                task_data = {
                    'name': row[' Name'],
                    'description': row[' Description '],
                    'location': row['Location '],
                    'price': row['Price'],
                    'color': row['Color'],
                }
                print(f"Task data: {task_data}")
                task_serializer = TaskSerializer(data=task_data)
                if task_serializer.is_valid():
                    task_serializer.save()
                    tasks.append(task_serializer.data)

            return Response({'message': 'Excel file uploaded successfully', 'tasks': tasks})
        else:
            return Response({'error': 'No Excel file provided'})

    # update by ID
    @action(detail=True, methods=['PUT'])
    def update_task(self, request, pk=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get all
    @action(detail=False, methods=['GET'])
    def get_all(self, request):
        tasks = Task.objects.all()
        task_serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks': task_serializer.data})

    # get one by ID
    @action(detail=True, methods=['GET'])
    def get_one(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
            task_serializer = TaskSerializer(task, many=False)
            return Response({'task': task_serializer.data})
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=True, methods=['DELETE'])
    def delete_task(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({'message': 'Task deleted successfully'})
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)