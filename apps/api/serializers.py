from rest_framework import serializers
from apps.api.models import Project

class ProjectSerializer(serializers.Serializer):
    pid = serializers.IntegerField(read_only=True)
    pname = serializers.CharField(max_length=150, allow_null=False, allow_blank=False)
    description = serializers.CharField(max_length=255)
    owner_id = serializers.IntegerField(allow_null=False)
    start_time = serializers.DateField(required=False, allow_null=True)
    end_time = serializers.DateField(required=False, allow_null=True)
    deadline = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.pname = validated_data.get('pname')
        instance.description = validated_data.get('description')
        instance.save()
        return instance

