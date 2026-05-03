from rest_framework import serializers
from rest_framework.response import Response as APIResponse
from rest_framework.status import HTTP_200_OK

__all__ = ['Response']


class Response(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)
        self.is_valid(raise_exception=True)

    def json(self, status: int = HTTP_200_OK):
        return APIResponse(self.validated_data, status=status)
