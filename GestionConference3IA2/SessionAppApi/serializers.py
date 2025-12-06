from rest_framework import serializers 
from SessionApp.models import Session
class SessionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Session
        fields='__all__'
        
        