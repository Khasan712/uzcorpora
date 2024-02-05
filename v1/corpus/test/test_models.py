import pytest
from v1.corpus.models import Corpus


@pytest.mark.parametrize('name', [('corpus1'), ('corpus2')])
def test_corpus_model_create(db, name):
    corpus = Corpus.objects.create(name='test')
    assert hasattr(corpus, 'id')
