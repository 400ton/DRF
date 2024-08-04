from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validates_url


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[validates_url])

    class Meta:
        model = Lesson
        fields = ('course', 'title', 'description', 'url')


class CourseSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[validates_url], read_only=True)
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return bool(Subscription.objects.filter(user=user, course=obj))

    class Meta:
        model = Course
        fields = ('title', 'description', 'lesson_count', 'lessons', 'url', 'is_subscribed')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'course')
