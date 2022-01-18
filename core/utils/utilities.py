"""Doc."""
from flask import jsonify
__author__ = 'Murphy'


class ParamsRequired(Exception):
    """Doc."""

    def __init__(self, value):
        """Doc."""
        self.message = "It is required parameter {0}".format(value)

    def __str__(self):
        """Doc."""
        return repr(self.message)


class ValueExist(Exception):
    """Doc."""

    def __init__(self, value):
        """Doc."""
        self.message = "This {0} is already used".format(value)

    def __str__(self):
        """Doc."""
        return repr(self.message)


class ValueRejected(Exception):
    """Doc."""

    def __init__(self, current, expected):
        """Doc."""
        self.message = "This value wasn't accepted. '{0}'. Was expected {1}".format(current, expected)

    def __str__(self):
        """Doc."""
        return repr(self.message)


class Message():
    """Doc."""

    def __init__(self):
        """Doc."""
        pass

    @staticmethod
    def failed(message="Bad request", e="Unexpected Error"):
        """Doc."""
        return jsonify({
            'ok': False,
            'code': 422,
            'error': e.message,
            'message': message
        })

    @staticmethod
    def successful(message="Successful request", data=None):
        """Doc."""
        return jsonify({
            'ok': True,
            'code': 200,
            'message': message,
            'data': data
        })
