from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from game.models import Game, Question, Quiz, Referral, Player 
from game.api.serializers import GameSerializer
from django.db.models import Sum, Q, F

class GameList(generics.ListAPIView):
    serializer_class = GameSerializer
    model = Game
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Game.objects.filter(user_id=user.id)


class GameCreate(generics.CreateAPIView):
    serializer_class = GameSerializer
    model = Game
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        try:
            player = Player.objects.get(user=user)
        except Player.DoesNotExist:
            player = Player.objects.create(user=user, is_hacker=False)
        
        game = Game(user=user, player=player)
        serializer = GameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        # save user/player is hacker in player table
        is_hacker = serializer.validated_data['is_hacker']
        
        if is_hacker and player.is_hacker == False: 
            player.is_hacker = True
            player.save()
        
        serializer.save()
        return Response({ 'message': 'Game saved' }, status=status.HTTP_201_CREATED)
    

class GameUpdate(generics.UpdateAPIView):
    serializer_class = GameSerializer
    model = Game
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        game_id = self.request.data['id']
        return Game.objects.get(pk=game_id)

    def update(self, request, *args, **kwargs):
        user = request.user
        game = self.get_object()
        
        if user.id != game.user.id:
            return Response(data={ 'status': False, 'message': 'You cannot play other user game' }, status=status.HTTP_400_BAD_REQUEST)

        serializer = GameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({ 'success': True, 'message': 'Game updated' }, status=status.HTTP_200_OK)
        


class GameLeaderboard(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_games(self):

        # explain below query
        # Game.objects.select_related('user', 'player') - from game table get user and player foreign key data
        # .filter(player__is_hacker=False) - filter is_hacker false from player is  tablename + __ + column name is_hacker
        # .annotate(username=F('user__username'), email=F('user__email')) - rename user table user_name from user__username to username like that user__email to email
        # .values('user', 'username', 'email', 'player') - select columns
        # .annotate(total_score=Sum('score')) - calculate sum of score by grouping by user
        #  sample result is 
        # .order_by('-total_score') - descending order by total_score
        # [
        #     {
        #         "user": 16,
        #         "player": 7,
        #         "username": "deepak+10",
        #         "email": "deepak.g+10@krds.fr",
        #         "total_score": 86
        #     },
        #     {
        #         "user": 17,
        #         "player": 9,
        #         "username": "deepak+11",
        #         "email": "deepak.g+11@krds.fr",
        #         "total_score": 156
        #     },
        #     {
        #         "user": 15,
        #         "player": 10,
        #         "username": "deepak+9",
        #         "email": "deepak.g+9@krds.fr",
        #         "total_score": 136
        #     }
        # ]

        return Game.objects.select_related('user', 'player').filter(player__is_hacker=False).annotate(username=F('user__username'), email=F('user__email')).values('user', 'username', 'email', 'player').annotate(total_score=Sum('score')).order_by('-total_score')

    def list(self, request, *args, **kwargs):
        games = self.get_games()

        for index, game in enumerate(games):
            game['rank'] = index + 1

        return Response(games)


    