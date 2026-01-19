from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_marksheet, name='upload_marksheet'),
    path('results/<int:upload_id>/', views.view_results, name='view_results'),
    
    # CSV Downloads
    path('download/csv/<int:upload_id>/', views.download_csv, name='download_csv'),
    path('download/csv-detailed/<int:upload_id>/', views.download_detailed_csv, name='download_detailed_csv'),
    
    # Excel Downloads
    path('download/excel/<int:upload_id>/', views.download_excel, name='download_excel'),
    path('download/excel-detailed/<int:upload_id>/', views.download_detailed_excel, name='download_detailed_excel'),
]
