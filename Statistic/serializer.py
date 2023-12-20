from rest_framework import serializers


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
