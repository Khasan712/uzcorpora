from django.urls import path
from v1.core.views import (
    LevelOfAuditoriumGetApi, TextMetaDataApi, StyleGetApi, TextTypeGetAPi, FieldOfApplicationGetAPi,
    LiteraryGenreGetApi, TextStatisticsApiV1, LanguageApi
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('text', TextMetaDataApi)
router.register('lang', LanguageApi)


urlpatterns = [
    path('literary-genre/', LiteraryGenreGetApi.as_view()),
    path('field-of-application/', FieldOfApplicationGetAPi.as_view()),
    path('text-type/', TextTypeGetAPi.as_view()),
    path('style/', StyleGetApi.as_view()),
    path('level-of-auditorium/', LevelOfAuditoriumGetApi.as_view()),
    path('statistics/', TextStatisticsApiV1.as_view()),
]+router.urls
