from rest_framework import serializers

from game.models import Game, Quiz, Question, Referral

import logging

logger = logging.getLogger(__name__)


class GameSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Game
        fields = ["start_time", "end_time", "score", "user"]

    # Use this method for the custom field
    def get_user(self, obj):
        return self.context['request'].user.id


    def validate(self, data):
        if data['score'] > 100:
            data['is_hacker'] = True
        else:
            data['is_hacker'] = False

        return data

