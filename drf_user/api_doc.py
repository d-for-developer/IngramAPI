from drf_yasg import openapi

string_type = openapi.Schema(type=openapi.TYPE_STRING, )
object_type = openapi.Schema(type=openapi.TYPE_OBJECT)
bool_type = openapi.Schema(type=openapi.TYPE_BOOLEAN)

otp_destination = openapi.Schema(type=openapi.TYPE_STRING,
                                 description="Either use Mobile Number or Email address as destination")
password_updated = openapi.Schema(type=openapi.TYPE_STRING, title='Password Updated')

bad_email = openapi.Schema(type=openapi.TYPE_STRING, title='This field may not be blank', )
bad_password = openapi.Schema(type=openapi.TYPE_STRING, title='This field may not be blank')

property_choices = openapi.Schema(type=openapi.TYPE_STRING, title='prop', enum=['username', 'email', 'mobile'])

# For LoginView
login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password'],
    properties={
        'username': string_type,
        'password': string_type,
    }
)

# For Login Success
login_success = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['token'],
    properties={
        'token': string_type,
    }
)

# For OTP login
otp_login_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    description="If you want to just validate the OTP, set `is_login` to false. `verify_otp` is required when "
                "validating the OTP.",
    required=['destination'],
    properties={
        'destination': otp_destination,
        'is_login': bool_type,
        'verify_otp': string_type
    }
)

# For OTP login
otp_login_success = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    description="When OTP is used to login this is the response that will be returned",
    required=['destination'],
    properties={
        'session': string_type,
        'token': string_type,
    }
)

# For IsUnique
is_unique_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['prop', 'value'],
    properties={
        'prop': property_choices,
        'value': string_type,
    }
)

# For UpdatePassword View
update_password_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['password', 'new_password'],
    properties={
        'password': string_type,
        'new_password': string_type
    }
)

# For 201 OTP Sent
otp_sent = openapi.Schema(type=openapi.TYPE_OBJECT,
                          properties={'success': bool_type,
                                      'message': string_type})

# Json Response
json_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'detail': string_type
    }
)
