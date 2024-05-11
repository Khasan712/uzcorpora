from django.db.models import Q, Sum, Count, Subquery, OuterRef, Case, When
from django.db.models.functions import Coalesce
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from v1.core.models import (
    CapacityLevelOfTheAuditorium, Style, Text, TextType, FieldOfApplication, LiteraryGenre, LangText
)
from v1.core.serializers import (
    CapacityLevelOfTheAuditoriumGetSerializer, NewspaperMetaDataPostSerializer, StyleGetSerializer,
    TextGetSerializer, OfficialTextMetaDataPostSerializer, TextTypeGetSerializer, JournalMetaDataPostSerializer,
    FieldOfApplicationGetSerializer, InternetInfoMetaDataPostSerializer, BookMetaDataPostSerializer,
    LiteraryGenreGetSerializer, ArticleMetaDataPostSerializer
)
from v1.utils.permissions import IsManager, IsAdmin
from rest_framework.validators import ValidationError
from rest_framework.response import Response


class TextStatisticsApiV1(APIView):
    permission_classes = (IsAdmin,)
    queryset = Text.objects.select_related(
        'style', 'text_type', 'field_of_application', 'literary_genre'
    ).prefetch_related('level_of_auditorium').order_by('-id')

    def get_queryset(self):
        params = self.request.query_params
        search_param = params.get('q')
        corpus_id = params.get('corpus_id')
        source_type = params.get('source_type')

        try:
            from_date = params.get('from_date')
            from_date = datetime.strptime(str(from_date), '%Y-%m-%d')
        except:
            from_date = None

        try:
            to_date = params.get('to_date')
            to_date = datetime.strptime(str(to_date), '%Y-%m-%d')
        except:
            to_date = None

        filter_data = Q()

        if search_param:
            filter_data &= (
                Q(number__icontains=search_param) | Q(net_address__icontains=search_param) |
                Q(theme__icontains=search_param) | Q(author__icontains=search_param) |
                Q(author_type__icontains=search_param) | Q(name__icontains=search_param) |
                Q(auditorium_age__icontains=search_param) | Q(document_type__icontains=search_param) |
                Q(document_owner__icontains=search_param) | Q(document_namely__icontains=search_param) |
                Q(publisher__icontains=search_param) | Q(text_number__icontains=search_param) |
                Q(issn__icontains=search_param) | Q(authors__icontains=search_param) |
                Q(time_and_place_of_the_event__icontains=search_param) | Q(isbn__icontains=search_param) |
                Q(name_of_article__icontains=search_param)
            )
        if corpus_id and str(corpus_id).replace(',', '').isdigit():
            filter_data &= Q(corpus_id__in=corpus_id.split(','))
        if source_type:
            filter_data &= Q(source_type__in=source_type.split(','))
        if from_date:
            filter_data &= Q(created_at__gte=from_date)
        if to_date:
            filter_data &= Q(created_at__lte=to_date)

        return self.queryset.filter(filter_data).annotate(
            word_qty=Coalesce(Subquery(self.get_word_qty()), 0),
            sentence_qty=Coalesce(Subquery(self.get_sentence_qty()), 0),
        )

    def get_word_qty(self):
        return LangText.objects.select_related('text_obj', 'lang').filter(
            text_obj_id=OuterRef('id'), lang__is_main=True
        ).values('word_qty')

    def get_sentence_qty(self):
        return LangText.objects.select_related('text_obj', 'lang').filter(
            text_obj_id=OuterRef('id'), lang__is_main=True
        ).values('sentence_qty')

    def get_statistics(self):
        return self.get_queryset().aggregate(
            total_text=Count('id'), total_word=Sum('word_qty'), total_sentence=Sum('sentence_qty')
        )

    def get(self, request):
        return Response(self.get_statistics())


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


class TextMetaDataApi(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAdmin | IsManager]
    queryset = Text.objects.select_related(
        'style', 'text_type', 'field_of_application', 'literary_genre'
    ).prefetch_related('level_of_auditorium').order_by('-id')
    http_method_names = ["get", "post", "patch", "head", "options", "trace"]

    def get_queryset(self):
        params = self.request.query_params
        search_param = params.get('q')
        corpus_id = params.get('corpus_id')
        source_type = params.get('source_type')

        try:
            from_date = params.get('from_date')
            from_date = datetime.strptime(str(from_date), '%Y-%m-%d')
        except Exception:
            from_date = None

        try:
            to_date = params.get('to_date')
            to_date = datetime.strptime(str(to_date), '%Y-%m-%d')
        except:
            to_date = None

        filter_data = Q(creator_id=self.request.user.id) if self.request.user.role == 'manager' else Q()

        if search_param:
            filter_data &= (
                Q(number__icontains=search_param) | Q(net_address__icontains=search_param) |
                Q(theme__icontains=search_param) | Q(author__icontains=search_param) |
                Q(author_type__icontains=search_param) | Q(name__icontains=search_param) |
                Q(auditorium_age__icontains=search_param) | Q(document_type__icontains=search_param) |
                Q(document_owner__icontains=search_param) | Q(document_namely__icontains=search_param) |
                Q(publisher__icontains=search_param) | Q(text_number__icontains=search_param) |
                Q(issn__icontains=search_param) | Q(authors__icontains=search_param) |
                Q(time_and_place_of_the_event__icontains=search_param) | Q(isbn__icontains=search_param) |
                Q(name_of_article__icontains=search_param)
            )
        if corpus_id and str(corpus_id).replace(',', '').isdigit():
            filter_data &= Q(corpus_id__in=corpus_id.split(','))
        if source_type:
            filter_data &= Q(source_type__in=source_type.split(','))
        if from_date:
            filter_data &= Q(created_at__gte=from_date)
        if to_date:
            filter_data &= Q(created_at__lte=to_date)

        if self.request.method == 'GET' and not self.kwargs.get('pk'):
            return super().get_queryset().filter(filter_data).annotate(
                word_qty=Coalesce(Subquery(self.get_word_qty()), 0),
                sentence_qty=Coalesce(Subquery(self.get_sentence_qty()), 0),
                file=Coalesce(self.get_file(), None)
            )

        return super().get_queryset().filter(filter_data)

    def get_word_qty(self):
        return LangText.objects.select_related('text_obj', 'lang').filter(
            text_obj_id=OuterRef('id'), lang__is_main=True
        ).values('word_qty')

    def get_sentence_qty(self):
        return LangText.objects.select_related('text_obj', 'lang').filter(
            text_obj_id=OuterRef('id'), lang__is_main=True
        ).values('sentence_qty')

    def get_file(self):
        return LangText.objects.select_related('text_obj', 'lang').filter(
            text_obj_id=OuterRef('id'), lang__is_main=True
        ).values('file')

    def validate_get_serializer(self):
        request_method = self.request.method
        if request_method in ['POST', 'PATCH'] or (request_method == 'GET' and self.kwargs.get('pk')):
            source_type = self.request.query_params.get('source_type')
            if source_type not in (
                    'newspaper', 'official_text', 'journal', 'internet_info', 'book', 'article', 'other'
            ):
                raise ValidationError({
                    "status": False,
                    "error": "Ukajon q'oy chiranma!!! 😎"
                    # "error": "Source type not given or given type not exists!!!"
                })
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
        elif request_method == 'GET':
            return TextGetSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['kwargs'] = self.kwargs
        return context

    def get_serializer_class(self):
        return self.validate_get_serializer()

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)


