from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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


class UserPhotoSerializer:
    pass


class UserPhotoCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.photo:
            user.photo.delete()

        photo = request.data.get('photo')

        file_name = f"{user.username}_user{user.id}"

        user.photo.save(file_name, photo)

        serializer = UserPhotoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserPhotoDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        user = request.user

        if user.photo:
            # Delete the photo file from storage
            file_path = user.photo.path
            default_storage.delete(file_path)

            # Delete the photo field in the User model
            user.photo = None
            user.save()

            return Response({'message': 'User photo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'User does not have a photo'}, status=status.HTTP_404_NOT_FOUND)
