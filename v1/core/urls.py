from django.urls import path
from v1.core.views import LevelOfAuditoriumGetApi, TextMetaDataPostApi


urlpatterns = [
    path('level-of-auditorium/', LevelOfAuditoriumGetApi.as_view()),
    path('text/', TextMetaDataPostApi.as_view()),
]
