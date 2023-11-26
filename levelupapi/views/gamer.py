"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer


class GamerView(ViewSet):
    """Level up gamer types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single gamer
        Returns:
            Response -- JSON serialized gamer
        """
        try:
          gamer = Gamer.objects.get(pk=pk)
          serializer = GamerSerializer(gamer)
          return Response(serializer.data)
        except Gamer.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all gamer types
        Returns:
            Response -- JSON serialized list of gamer types
        """

        gamer = Gamer.objects.all()
        serializer = Gamer(gamer, many=True)
        return Response(serializer.data)

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Gamer
        fields = ('id', 'uid', 'bio')