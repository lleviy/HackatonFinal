

from django.urls import path, include, re_path
from .views import SpaceView, SpaceListView, SpaceCreateView, \
    SpaceUpdateView, SpaceDeleteView, MapView, consumption_upload, index, get_map, AverageIncomeView, OborotView, \
    PotrebView

app_name = 'spaces'

urlpatterns = [
    path('spaces/<int:space_id>/', SpaceView.as_view(), name='space'),
    path('spaces/map/<int:space_id>/', MapView.as_view(), name='map'),
    path('spaces/edit/<int:space_id>/', SpaceUpdateView.as_view(), name='space_edit'),
    path('spaces/delete/<int:pk>/', SpaceDeleteView.as_view(), name='space_delete'),
    path('spaces/create/', SpaceCreateView.as_view(), name='space_create'),
    path('average_income/', AverageIncomeView.as_view(), name='average_income'),
    path('oborot/', OborotView.as_view(), name='oborot'),
    path('potreb/', PotrebView.as_view(), name='potreb'),
    path('spaces/', SpaceListView.as_view(), name='spaces'),
    path('upload_csv/', consumption_upload, name='upload'),
    path('', index, name='index'),
    path('map/', get_map, name='get_map'),
]