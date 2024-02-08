from rest_framework.generics import ListAPIView, CreateAPIView

from v1.core.models import (CapacityLevelOfTheAuditorium, Style)
from v1.core.serializers import CapacityLevelOfTheAuditoriumGetSerializer, NewspaperMetaDataPostSerializer, \
    StyleGetSerializer
from v1.utils.permissions import IsManager, IsAdmin
from rest_framework.response import Response


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


class TextMetaDataPostApi(CreateAPIView):
    permission_classes = [IsAdmin | IsManager]

    def post(self, request, *args, **kwargs):
        source_type = request.data.get('source_type')
        if not source_type or source_type not in ('newspaper',):
            return Response({
                "status": True,
                "error": "Source type not exists or not found!!!"
            }, status=400)
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        source_type = self.request.data.get('source_type')
        if source_type == 'newspaper':
            return NewspaperMetaDataPostSerializer

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)


