#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature


def generate_confirm_token(raw, secret_key, expiration=3600):
    # TODO: save token to cache server
    s = Serializer(secret_key, expiration)
    return s.dumps({'confirm': raw})


def token_confirm(token, secret_key):
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except BadSignature:
        return False

    return data.get('confirm')
