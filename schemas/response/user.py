from marshmallow import Schema, fields

from schemas.bases import ResponseUserBaseSchema


class ResponseUserRegisterSchema(ResponseUserBaseSchema):
    pass


class ResponseUserLoginSchema(ResponseUserBaseSchema):
    pass


class ResponseUserUpdateSchema(Schema):
    message = fields.String(required=True)


class ResponseUserDeleteSchema(ResponseUserUpdateSchema):
    pass
