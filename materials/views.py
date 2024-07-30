from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = (~IsModerator,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModerator,)
        return super().get_permissions()


class LessonCreate(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated,)


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner, ]


class LessonRetrieve(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonDelete(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator,)
