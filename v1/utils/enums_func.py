from v1.commons.enums import SourceType


def get_source_types():
    return [source_type[0] for source_type in list(SourceType.choices())]
