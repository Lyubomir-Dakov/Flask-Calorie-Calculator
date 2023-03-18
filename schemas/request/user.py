from marshmallow import fields

from schemas.bases import RequestUserBaseSchema


class RequestUserRegisterSchema(RequestUserBaseSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class RequestUserLoginSchema(RequestUserBaseSchema):
    pass
