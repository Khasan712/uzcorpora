from rest_framework.generics import ListAPIView
from v1.corpus.models import Corpus
from v1.corpus.serializers import CorpusGetSerializer


class CorpusGetApi(ListAPIView):
    queryset = Corpus.objects.select_related('parent').order_by('-id')
    serializer_class = CorpusGetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        corpus_id = self.request.query_params.get('parent_id')
        if corpus_id and str(corpus_id).isdigit():
            return queryset.filter(parent_id=corpus_id)
        return queryset.filter(parent__isnull=True)


