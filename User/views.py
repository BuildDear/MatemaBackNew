from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import default_storage

from Task.models import Task
from Task.serializer import TaskSerializer
from User.serializers import UserPhotoSerializer, UserScoreSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


class UserPhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        user = request.user

        if user.photo:
            # Return the photo URL or other information
            return Response({'photo_url': user.photo.url}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not have a photo'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.photo:
            user.photo.delete()

        photo = request.data.get('photo')

        # Extract the original file extension
        original_extension = photo.name.split('.')[-1]

        # Generate a new file name with the original extension
        file_name = f"{user.username}_ID{user.id}.{original_extension}"

        # Save the photo with the new file name
        user.photo.save(file_name, photo)

        # Save the user instance
        user.save()

        # Pass the user instance to the serializer
        serializer = UserPhotoSerializer(user)

        # Return the serialized data directly
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user

        if user.photo:
            try:
                # Delete the photo file from storage
                file_path = user.photo.path
                default_storage.delete(file_path)

                # Delete the photo field in the User model
                user.photo = None
                user.save()

                return Response({'message': 'User photo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except ImproperlyConfigured as e:
                return Response({'message': f'Error deleting photo: {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'User does not have a photo'}, status=status.HTTP_404_NOT_FOUND)


class UserScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        serializer = UserScoreSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetTaskView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
