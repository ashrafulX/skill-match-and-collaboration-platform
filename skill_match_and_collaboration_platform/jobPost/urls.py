from django.urls import path
from .views import AddJobPostView, EditJobPostView, DeleteJobPostView, application_detail_view, detail, application_view, application_view, manage_application, notifications_view

urlpatterns = [
    path('add-job/', AddJobPostView.as_view(), name='add_job'),
    path('edit-job/<int:id>/', EditJobPostView.as_view(), name='edit_job'),
    path('delete-job/<int:id>/', DeleteJobPostView.as_view(), name='delete_job'),
    path('job/<int:id>/', detail, name='job_detail'),
    path('job/<int:id>/apply/', application_view, name='apply_job'),
    path('application/<int:application_id>/', application_detail_view, name='application_detail'),
    path('application/<int:application_id>/<str:action>/', manage_application, name='manage_application'),
    path('notifications/', notifications_view, name='notifications'),
]
