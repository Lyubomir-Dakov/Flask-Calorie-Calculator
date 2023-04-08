from marshmallow import fields, validates_schema
from werkzeug.exceptions import BadRequest

from schemas.bases import RequestUserBaseSchema


class RequestUserRegisterSchema(RequestUserBaseSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class RequestUserLoginSchema(RequestUserBaseSchema):
    pass


class RequestUserUpdateSchema(RequestUserBaseSchema):
    new_email = fields.String()
    new_password = fields.String()
    new_first_name = fields.String()
    new_last_name = fields.String()
    retype_new_password = fields.String()

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        new_password = data.get('new_password')
        retype_new_password = data.get('retype_new_password')
        if not retype_new_password:
            raise BadRequest('You need to retype your new password if you want to change your password')
        if new_password and retype_new_password and new_password != retype_new_password:
            raise BadRequest('New password and retype password do not match')
