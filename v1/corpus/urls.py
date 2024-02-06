from django.urls import path
from v1.corpus.views import CorpusGetApi


urlpatterns = [
    path('', CorpusGetApi.as_view())
]
