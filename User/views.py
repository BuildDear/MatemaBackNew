from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode


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


