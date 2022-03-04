from django.utils.text import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView

from drf_user import api_doc


class UserView(RetrieveAPIView):
    from .serializers import UserDetailsSerializer
    from .models import User

    from rest_framework.permissions import IsAuthenticated

    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'created_by'

    def get_object(self):
        return self.request.user


class RegisterView(CreateAPIView):
    """
    Register View

    Register a new user.
    """
    from .serializers import UserSerializer
    from rest_framework.permissions import AllowAny
    from rest_framework.renderers import JSONRenderer

    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        from .models import User

        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            name=serializer.validated_data['name'],
            password=serializer.validated_data['password'],
            mobile=serializer.validated_data['mobile'])
        serializer = self.get_serializer(user)


class LoginView(APIView):
    """
    Login View

    This view can be used to login and retrieve a jwt token.
    """
    from rest_framework_jwt.serializers import JSONWebTokenSerializer
    from rest_framework.permissions import AllowAny
    from rest_framework.renderers import JSONRenderer

    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = JSONWebTokenSerializer

    def validated(self, serialized_data, *args, **kwargs):
        from rest_framework_jwt.settings import api_settings

        from django.utils import timezone

        from .models import AuthTransaction

        from drfaddons.utils import get_client_ip

        from rest_framework.response import Response

        user = serialized_data.object.get('user') or self.request.user
        token = serialized_data.object.get('token')
        response_data = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token, user,
                                                                  self.request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (timezone.now() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)

        user.last_login = timezone.now()
        user.save()

        AuthTransaction(created_by=user, token=token,
                        ip_address=get_client_ip(self.request),
                        session=user.get_session_auth_hash()).save()

        return response

    @swagger_auto_schema(
        request_body=api_doc.login_request_body,
        responses={
            '200': api_doc.login_success,
            '400': api_doc.json_response,
            '401': api_doc.json_response,
        },
        operation_description='Login using email and password. username field can be either username, mobile or email',
    )
    def post(self, request):
        from drfaddons.utils import JsonResponse

        from rest_framework import status

        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            return self.validated(serialized_data=serialized_data)
        else:
            print(serialized_data.errors)
            if "non_field_errors" in serialized_data.errors.keys() and \
                    serialized_data.errors['non_field_errors'][0] == "Unable to log in with provided credentials.":
                return JsonResponse("Unable to log in with provided credentials.",
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse(serialized_data.errors,
                                    status=status.HTTP_400_BAD_REQUEST)


class CheckUniqueView(APIView):
    """
    Check Unique API View

    This view checks if the given property -> value pair is unique (or
    doesn't exists yet)
    'prop' -- A property to check for uniqueness (username/email/mobile)
    'value' -- Value against property which is to be checked for.
    """
    from .serializers import CheckUniqueSerializer
    from rest_framework.permissions import AllowAny
    from rest_framework.renderers import JSONRenderer

    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = CheckUniqueSerializer

    @swagger_auto_schema(
        request_body=api_doc.is_unique_body,
        responses={
            '200': api_doc.json_response,
            '400': api_doc.json_response,
        },
        operation_description='Checks if the given property-value pair is unique.',
    )
    def post(self, request):
        from .utils import check_unique
        from drfaddons.utils import JsonResponse
        from rest_framework import status

        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            print(serialized_data.validated_data)
            return JsonResponse(check_unique(serialized_data.validated_data['prop'],
                                             serialized_data.validated_data['value']),
                                status.HTTP_200_OK)
        else:
            return JsonResponse(serialized_data.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class OTPView(APIView):
    """
    OTP Validate | OTP Login
    """
    from .serializers import OTPSerializer

    from rest_framework.permissions import AllowAny

    permission_classes = (AllowAny,)
    serializer_class = OTPSerializer

    @swagger_auto_schema(
        request_body=api_doc.otp_login_body,
        responses={
            '201': api_doc.otp_sent,
            '202': api_doc.otp_login_success,
            '403': api_doc.json_response,
            '404': api_doc.json_response
        },
        operation_description='Validate or Login with OTP.',
    )
    def post(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status

        from rest_framework.exceptions import APIException

        from .utils import validate_otp, login_user, generate_otp, send_otp

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        destination = serializer.validated_data.get('destination')
        prop = serializer.validated_data.get('prop')
        user = serializer.validated_data.get('user')
        email = serializer.validated_data.get('email')
        is_login = serializer.validated_data.get('is_login')

        if 'verify_otp' in request.data.keys():
            if validate_otp(destination, request.data.get('verify_otp')):
                if is_login:
                    return Response(login_user(user, self.request),
                                    status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        data={'data': 'OTP Validated successfully!'},
                        status=status.HTTP_202_ACCEPTED)
        else:
            otp_obj = generate_otp(prop, destination)
            sentotp = send_otp(destination, otp_obj, email)

            if sentotp['success']:
                otp_obj.send_counter += 1
                otp_obj.save()

                return Response(sentotp, status=status.HTTP_201_CREATED)
            else:
                raise APIException(
                    detail=_('A Server Error occurred: ' + sentotp['message']))


class RetrieveUpdateUserAccountView(RetrieveUpdateAPIView):
    """
    Retrieve Update User Account View

    get: Fetch Account Details
    put: Update all details
    patch: Update some details
    """
    from .serializers import UserSerializer
    from .models import User

    from rest_framework.permissions import IsAuthenticated

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'created_by'

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        if 'password' in request.data.keys():
            self.request.user.set_password(request.data.pop('password'))
            self.request.user.save()

        return super(RetrieveUpdateUserAccountView, self).update(request,
                                                                 *args,
                                                                 **kwargs)


class OTPLoginView(APIView):
    """
    OTP Login View

    Used to register/login to a system where User may not be required
    to pre-login but needs to login in later stage or while doing a
    transaction.

    View ensures a smooth flow by sending same OTP on mobile as well as
    email.

    name -- Required
    email -- Required
    mobile -- Required
    verify_otp -- Not Required (only when verifying OTP)
    """

    from rest_framework.permissions import AllowAny
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser

    from .serializers import OTPLoginRegisterSerializer

    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
    serializer_class = OTPLoginRegisterSerializer

    @swagger_auto_schema(
        request_body=OTPLoginRegisterSerializer,
        responses={
            '202': api_doc.otp_login_success
        },
        operation_description='Can be used to login or register a user. If user exist it will login else create a '
                              'new user account.',
    )
    def post(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status

        from rest_framework.exceptions import APIException

        from .utils import validate_otp, generate_otp, send_otp
        from .utils import login_user
        from .models import User
        from .variables import EMAIL, MOBILE

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_otp = serializer.validated_data.get('verify_otp', None)
        name = serializer.validated_data.get('name')
        mobile = serializer.validated_data.get('mobile')
        email = serializer.validated_data.get('email')
        user = serializer.validated_data.get('user', None)

        message = {}

        if verify_otp:
            if validate_otp(email, verify_otp):
                if not user:
                    user = User.objects.create_user(
                        name=name, mobile=mobile, email=email, username=mobile,
                        password=User.objects.make_random_password()
                    )
                    user.is_active = True
                    user.save()
                return Response(login_user(user, self.request),
                                status=status.HTTP_202_ACCEPTED)
            return Response(data={'OTP': [_('OTP Validated successfully!'), ]},
                            status=status.HTTP_202_ACCEPTED)

        else:
            otp_obj_email = generate_otp(EMAIL, email)
            otp_obj_mobile = generate_otp(MOBILE, mobile)

            # Set same OTP for both Email & Mobile
            otp_obj_mobile.otp = otp_obj_email.otp
            otp_obj_mobile.save()

            # Send OTP to Email & Mobile
            sentotp_email = send_otp(email, otp_obj_email, email)
            sentotp_mobile = send_otp(mobile, otp_obj_mobile, email)

            if sentotp_email['success']:
                otp_obj_email.send_counter += 1
                otp_obj_email.save()
                message['email'] = {
                    'otp': _("OTP has been sent successfully.")
                }
            else:
                message['email'] = {
                    'otp': _("OTP sending failed {}".format(
                        sentotp_email['message']))
                }

            if sentotp_mobile['success']:
                otp_obj_mobile.send_counter += 1
                otp_obj_mobile.save()
                message['mobile'] = {
                    'otp': _("OTP has been sent successfully.")
                }
            else:
                message['mobile'] = {
                    'otp': _("OTP sending failed {}".format(
                        sentotp_mobile['message']))
                }

            if sentotp_email['success'] or sentotp_mobile['success']:
                curr_status = status.HTTP_201_CREATED
            else:
                raise APIException(
                    detail=_(
                        'A Server Error occurred: ' + sentotp_mobile['message']
                    ))

            return Response(data=message, status=curr_status)


class PasswordResetView(APIView):
    from rest_framework.permissions import AllowAny

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        from drfaddons.utils import JsonResponse
        from rest_framework import status
        from drf_user.utils import validate_otp

        from .models import User
        from .serializers import PasswordResetSerializer

        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])

        if validate_otp(serializer.validated_data['email'], serializer.validated_data['otp']):
            # OTP Validated, Change Password
            user.set_password(serializer.validated_data['password'])
            user.save()
            return JsonResponse(content="Password Updated Successfully.", status=status.HTTP_202_ACCEPTED)


class UploadImageView(APIView):
    from .models import User
    from .serializers import ImageSerializer
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.parsers import MultiPartParser

    queryset = User.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated,)
    parser_class = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        from .serializers import ImageSerializer
        from rest_framework.response import Response
        from rest_framework import status

        image_serializer = ImageSerializer(data=request.data)

        if image_serializer.is_valid():
            image_serializer.update(instance=request.user, validated_data=image_serializer.validated_data)
            return Response("{\"message\": \"Uploaded Successfully\"}", status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

