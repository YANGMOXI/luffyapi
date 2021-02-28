# -*- coding: utf-8 -*-
# date: 2020/11/29 18:33

def get_token(user):
    from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
    payload = jwt_payload_handler(user)  # 通过user对象获得payload荷载
    token = jwt_encode_handler(payload)  # payload获得token
    return token