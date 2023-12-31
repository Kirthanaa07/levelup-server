"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer
from rest_framework.decorators import action

from levelupapi.models.event_gamer import EventGamer


class EventView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """

        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        game = request.query_params.get("game", None)
        if game is not None:
            events = events.filter(game_id=game)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized event instance
        """
        game = Game.objects.get(pk=request.data["game"])
        gamer = Gamer.objects.get(uid=request.data["userId"])

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=gamer,
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game

        gamer = Gamer.objects.get(pk=request.data["organizer"])
        event.organizer = gamer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.data["userId"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(gamer=gamer, event=event)
        return Response({"message": "Gamer added"}, status=status.HTTP_201_CREATED)
        """Level up game view"""

    @action(methods=["delete"], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.data["userId"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.get(gamer=gamer, event=event)
        attendee.delete()
        return Response({"message": "Gamer left"}, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    class Meta:
        model = Event
        fields = ("id", "game", "description", "date", "time", "organizer")
        depth = 2
