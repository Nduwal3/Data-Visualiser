from django.urls import path
from . import views


app_name = 'graph'

urlpatterns = [
    path('', views.home , name='home'),
    path('upload_file', views.upload_file , name='upload_file'),
    path('chart',views.get_x_and_y_columns, name='get_x_and_y_columns')

]
