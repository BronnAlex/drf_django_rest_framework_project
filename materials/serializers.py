from rest_framework import serializers

from materials.models import CourseModel, LessonModel


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = "__all__"
