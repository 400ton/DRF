from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validates_url


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[validates_url])

    class Meta:
        model = Lesson
        fields = ('course', 'title', 'description', 'url')


class CourseSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[validates_url])
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('title', 'description', 'lesson_count', 'lessons', 'url')
