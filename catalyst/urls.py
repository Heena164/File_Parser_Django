from django.urls import path
from catalyst.views import register, login, UploadDataView, QueryBuilderView, UsersView, UsersView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('upload/', UploadDataView.as_view(), name='upload_data'),
    path('query/', QueryBuilderView.as_view(), name='query_builder'),
    path('users/', UsersView.as_view(), name='users'),

]
