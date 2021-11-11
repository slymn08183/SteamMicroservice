from drf_writable_nested import WritableNestedModelSerializer

from core.models import Game
from core.serializers.description import DescriptionSerializer
from core.serializers.developer import DeveloperSerializer
from core.serializers.feature import FeatureSerializer
from core.serializers.genre import GenreSerializer
from core.serializers.picture import PictureSerializer
from core.serializers.price import PriceSerializer
from core.serializers.publisher import PublisherSerializer
from core.serializers.specification import SpecificationSerializer
from core.serializers.video import VideoSerializer


class GameSerializer(WritableNestedModelSerializer):

    description = DescriptionSerializer()
    specification = SpecificationSerializer()

    developers = DeveloperSerializer(many=True)
    features = FeatureSerializer(many=True)
    genres = GenreSerializer(many=True)
    pictures = PictureSerializer(many=True)
    publishers = PublisherSerializer(many=True)
    videos = VideoSerializer(many=True)

    prices = PriceSerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'

