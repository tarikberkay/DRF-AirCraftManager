from django.urls import path
from aircraft.views import (
    PersonelView,
    PersonelDetailView,

    TeamListView,
    TeamDetailView,

    PartView,
    PartListCreateView,
    PartProduceView,
    PartRecycleView,

    AircraftListCreateView,
    AircraftAssembleView,
)

app_name = 'aircraft'


urlpatterns = [
    path('personel/', PersonelView.as_view(), name='personel-list'),
    path('personel/<int:pk>/', PersonelDetailView.as_view(), name='personel-detail'),

    path('team/', TeamListView.as_view(), name='team-list'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),

    path('parts/', PartView.as_view(), name='part-list'),
    path('part/', PartListCreateView.as_view(), name='part-list-create'),
    path('part/<int:pk>/produce/', PartProduceView.as_view(), name='part-produce'),
    path('part/<int:pk>/recycle/', PartRecycleView.as_view(), name='part-recycle'),

    path('aircraft/', AircraftListCreateView.as_view(),
         name='aircraft-list-create'),
    path('aircraft/<int:pk>/assemble/',
         AircraftAssembleView.as_view(), name='aircraft-assemble'),
]
