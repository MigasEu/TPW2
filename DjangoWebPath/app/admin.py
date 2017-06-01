from django.contrib import admin
from app.models import *

admin.site.register(Story)
admin.site.register(Piece)
admin.site.register(DecisionPiece)
admin.site.register(ChoicePiece)
admin.site.register(WinPiece)
admin.site.register(LosePiece)
