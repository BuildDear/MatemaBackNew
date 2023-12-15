from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode

from Task.models import Task
from Task.serializer import TaskSerializer
from User.serializers import UserPhotoSerializer, UserScoreSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from User.models import User



def activate_account(request, uidb64, token):
    """
    Activate a user account.

    This function is used to activate a user account through an email confirmation process.
    It takes a request, a base64 encoded user ID (uidb64), and a token as parameters.

    Parameters:
    - request: The HTTP request object.
    - uidb64: A base64 encoded string representing the user's ID. This is typically sent to the user's email.
    - token: A token generated for the user to verify their email. This is also sent to the user's email.

    The function decodes the uidb64 to get the user's ID and attempts to fetch the corresponding user from the database.
    If the user exists and the token is valid, the user's 'is_active' field is set to True, effectively activating the account.

    Returns:
    - An HttpResponse indicating whether the activation was successful or not. If successful, it notifies the user that
      they can now log in. If not, it informs them that the activation link is invalid.
    """
    try:
        # Decode the base64 encoded user ID and fetch the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        # If decoding fails or user does not exist, set user to None
        user = None

    # Check if user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        # Activate the user's account
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        # If user does not exist or token is invalid, return an error message
        return HttpResponse('Activation link is invalid!')


def check_user_active(request, username):
    try:
        user = User.objects.get(username=username)
        if user.is_active:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)
    except User.DoesNotExist:
        return HttpResponse("User does not exist", status=404)


class UserPhotoCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

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


class UserPhotoDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

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


class UserPhotoRetrieveView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        if user.photo:
            # Return the photo URL or other information
            return Response({'photo_url': user.photo.url}, status=status.HTTP_200_OK)
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