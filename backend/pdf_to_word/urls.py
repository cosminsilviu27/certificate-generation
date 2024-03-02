from django.urls import path
from .views import list_word_files, upload_pdf, download_word, delete_word, user_data

urlpatterns = [
    path('list-words/', list_word_files, name='list_words'),
    path('upload-pdf/', upload_pdf, name='upload_pdf'),
    path('download-word/<int:pk>/', download_word, name='download_word'), 
    path('delete-word/<int:pk>/', delete_word, name='delete-word'),
    path('user-data//<str:email>/', user_data, name='user-data'),
]
