from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("list_items/", views.list_items, name="list_items"),
    path("add_items/", views.add_items, name="add_items"),
    path("add_category/", views.add_category, name="add_category"),
    path("update_items/<str:pk>/", views.update_items, name="update_items"),
    path("view_items/<str:pk>/", views.view_items, name="view_items"),
    path("delete_items/<str:pk>/", views.delete_items, name="delete_items"),
    
    path('export_to_csv/',
         views.export_to_csv, name='export_to_csv'),
    path('pdf_report_create/',
         views.pdf_report_create, name='pdf_report_create'),
    path('pdf_report_item/<str:pk>/',
         views.pdf_report_item, name='pdf_report_item'),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),

]
