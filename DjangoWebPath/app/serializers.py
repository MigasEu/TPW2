from app.models import Story, Piece, DecisionPiece, ChoicePiece, WinPiece, LosePiece
from rest_framework import serializers

class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ('pId','story','text','next')

class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionPiece
        fields = ('pId','story')

class WinSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinPiece
        fields = ('pId','story','text','next')

class LoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LosePiece
        fields = ('pId','story','text','next')

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoicePiece
        fields = ('text','next')