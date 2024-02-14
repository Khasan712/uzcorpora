from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


def rander_response(data: dict, status=200):
    response = Response(data, status=status)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response
