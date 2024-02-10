from rest_framework.generics import ListAPIView, ListCreateAPIView
from v1.core.models import (
    CapacityLevelOfTheAuditorium, Style, Text, TextType, FieldOfApplication, LiteraryGenre
)
from v1.core.serializers import (
    CapacityLevelOfTheAuditoriumGetSerializer, NewspaperMetaDataPostSerializer, StyleGetSerializer,
    TextGetSerializer, OfficialTextMetaDataPostSerializer, TextTypeGetSerializer, JournalMetaDataPostSerializer,
    FieldOfApplicationGetSerializer, InternetInfoMetaDataPostSerializer, BookMetaDataPostSerializer,
    LiteraryGenreGetSerializer, ArticleMetaDataPostSerializer
)
from v1.utils.permissions import IsManager, IsAdmin
from rest_framework.response import Response


class LiteraryGenreGetApi(ListAPIView):
    queryset = LiteraryGenre.objects.order_by('-id').select_related('parent')
    serializer_class = LiteraryGenreGetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        corpus_id = self.request.query_params.get('parent_id')
        if corpus_id and str(corpus_id).isdigit():
            return queryset.filter(parent_id=corpus_id)
        return queryset.filter(parent__isnull=True)


class FieldOfApplicationGetAPi(ListAPIView):
    queryset = FieldOfApplication.objects.order_by('-id')
    serializer_class = FieldOfApplicationGetSerializer


class TextTypeGetAPi(ListAPIView):
    queryset = TextType.objects.order_by('-id')
    serializer_class = TextTypeGetSerializer


class StyleGetApi(ListAPIView):
    queryset = Style.objects.order_by('-id')
    serializer_class = StyleGetSerializer


class LevelOfAuditoriumGetApi(ListAPIView):
    queryset = CapacityLevelOfTheAuditorium.objects.select_related('parent').order_by('-id')
    serializer_class = CapacityLevelOfTheAuditoriumGetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        corpus_id = self.request.query_params.get('parent_id')
        if corpus_id and str(corpus_id).isdigit():
            return queryset.filter(parent_id=corpus_id)
        return queryset.filter(parent__isnull=True)


class TextMetaDataPostApi(ListCreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    queryset = Text.objects.select_related(
        'style', 'text_type', 'field_of_application', 'literary_genre').prefetch_related(
        'level_of_auditorium').order_by('-id')

    def get_queryset(self):
        return super().get_queryset().filter(creator_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        source_type = request.data.get('source_type')
        if not source_type or source_type not in (
                'newspaper', 'official_text', 'journal', 'internet_info', 'book', 'article', 'other'
        ):
            return Response({
                "status": True,
                "error": "Source type not exists or not found!!!"
            }, status=400)
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        source_type = self.request.data.get('source_type')
        if self.request.method == 'POST':
            if source_type == 'newspaper':
                return NewspaperMetaDataPostSerializer
            elif source_type == 'official_text':
                return OfficialTextMetaDataPostSerializer
            elif source_type == 'journal':
                return JournalMetaDataPostSerializer
            elif source_type == 'internet_info':
                return InternetInfoMetaDataPostSerializer
            elif source_type == 'book' or source_type == 'other':
                return BookMetaDataPostSerializer
            else:
                return ArticleMetaDataPostSerializer
        elif self.request.method == 'GET':
            return TextGetSerializer

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)


