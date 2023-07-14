from rest_framework import serializers
from apps.models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields ="__all__"


class BookingSerializer(serializers.ModelSerializer):
    event_name = serializers.SerializerMethodField('get_event')
    user = serializers.SerializerMethodField('get_user')

    def get_event(self,data):
        result = Event.objects.get(id=data.event_id).name
        return result 

    def get_user(self,data):
        result = User_Profile.objects.get(id=data.user_id).email
        return result 
    
    class Meta:
        model = BookingMaster
        fields ="__all__"