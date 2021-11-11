from app.data_access.game_dao import GameDAO
from core.models.price import Price
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Game
from core.serializers.game import GameSerializer


class GameAPIPriceView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DAO = GameDAO()

    # def put(self, request):
    #     query = self.DAO.get_by_name(request.data.get('name'))
    #     if query is None:
    #         return Response({'error': 'Not found : {}'.
    #                         format(request.data.get('name'))},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(
    #         self.DAO.update_price(query,
    #                               request.data.get('prices'),
    #                               request.data.get('name'))
    #     )
