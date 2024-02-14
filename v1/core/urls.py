from django.urls import path
from v1.core.views import (
    LevelOfAuditoriumGetApi, TextMetaDataApi, StyleGetApi, TextTypeGetAPi, FieldOfApplicationGetAPi,
    LiteraryGenreGetApi
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('text', TextMetaDataApi)


urlpatterns = [
    path('literary-genre/', LiteraryGenreGetApi.as_view()),
    path('field-of-application/', FieldOfApplicationGetAPi.as_view()),
    path('text-type/', TextTypeGetAPi.as_view()),
    path('style/', StyleGetApi.as_view()),
    path('level-of-auditorium/', LevelOfAuditoriumGetApi.as_view()),
]+router.urls
