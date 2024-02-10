from django.urls import path
from v1.core.views import (
    LevelOfAuditoriumGetApi, TextMetaDataPostApi, StyleGetApi, TextTypeGetAPi, FieldOfApplicationGetAPi,
    LiteraryGenreGetApi
)


urlpatterns = [
    path('literary-genre/', LiteraryGenreGetApi.as_view()),
    path('field-of-application/', FieldOfApplicationGetAPi.as_view()),
    path('text-type/', TextTypeGetAPi.as_view()),
    path('style/', StyleGetApi.as_view()),
    path('level-of-auditorium/', LevelOfAuditoriumGetApi.as_view()),
    path('text/', TextMetaDataPostApi.as_view()),
]
