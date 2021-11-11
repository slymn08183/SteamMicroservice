from rest_framework.response import Response
from rest_framework.views import APIView
from core.models.success import Success


class HealthCheckView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get(request):
        return Response(Success().get())

