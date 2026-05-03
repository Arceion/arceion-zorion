from rest_framework.response import Response as APIResponse
from rest_framework.status import HTTP_200_OK

__all__ = ['ModelResponse']


class ModelResponse:

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'is_valid'):
            self.is_valid = lambda raise_exception: True
        if not hasattr(self, 'data'):
            self.data = {}

    def json(self, status: int = HTTP_200_OK):
        if self.is_valid(raise_exception=False):
            pass
        return APIResponse(self.data, status=status)
