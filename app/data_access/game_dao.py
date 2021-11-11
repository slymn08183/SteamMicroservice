from core.models import Game
from core.models.price import Price
from core.serializers import GameSerializer


class GameDAO:

    @staticmethod
    def update(query, data):
        serializer = GameSerializer(query, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def create(data):
        serializer = GameSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update_price(self, query, data, name):
        price = Price.objects.create(**data)
        price.save()
        query.prices.add(price)
        query.save()

        return GameSerializer(self.get_by_name(name=name)).data

    @staticmethod
    def get_all():
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return serializer.data

    @staticmethod
    def get_by_name(name):
        try:
            return Game.objects.get(name=name)
        except Game.DoesNotExist:
            return None
