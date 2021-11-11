from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.bussines.game_manager import GameManager
from app.data_access.game_dao import GameDAO


class GameAPIView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DAO = GameDAO()

    def get(self, request):
        return Response(self.DAO.get_all())

    # def post(self, request):
    #     return Response(self.DAO.create(request.data))

    def patch(self, request):
        try:
            GameManager(request.data.get("is_update"))
            return Response({})
        except Exception as e:
            return Response({'error': '{}'.format(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     query = self.DAO.get_by_name(request.data.get('name'))
    #     if query is None:
    #         return Response({'error': 'Not found : {}'.
    #                         format(request.data.get('name'))},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(self.DAO.update(query, request.data))

