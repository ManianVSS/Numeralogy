from rest_framework import serializers

from .models import NameEntry


class NameEntrySerializer(serializers.ModelSerializer):
    sum = serializers.IntegerField(read_only=True)
    recursive_sum = serializers.IntegerField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = NameEntry
        fields = [
            'id',
            'name',
            'sum',
            'recursive_sum',
            'source_file',
            'uploaded_at',
        ]


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    name = serializers.CharField(required=False, allow_blank=True)
    names = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('file') and not data.get('name') and not data.get('names'):
            raise serializers.ValidationError('Please provide a file, a name, or names text.')
        return data
