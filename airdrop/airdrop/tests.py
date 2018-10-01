from django import test
from .libs import email


class SendEmail(test.TestCase):

    def test_email(self):
        message = "Test"
        to_address = "amelchenko.dmitriy@outlook.com"
        teme = "test"
        exc = None
        try:
            email.send_email(to_address, teme, message)
        except Exception as exc:
            pass
        self.assertNotEqual(exc, Exception)

