from rest_framework import serializers
from v1.corpus.models import Corpus


class CorpusGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Corpus
        fields = ('id', 'name')

