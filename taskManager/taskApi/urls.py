from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-excel/', TaskViewSet.as_view({'post': 'upload_excel'}), name='upload_excel'),
    path('delete/<int:pk>/', TaskViewSet.as_view({'delete': 'delete_task'}), name='delete_task'),
    path('update/<int:pk>/', TaskViewSet.as_view({'put': 'update_task'}), name='update_task'),
    path('get_one/<int:pk>/', TaskViewSet.as_view({'get': 'get_one'}), name='get_one'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
