from django import test
from user import forms
from user import models
from django.conf import settings
import os


class RegistrationTest(test.TestCase):

    def setUp(self):
        self.test_data_form = {
            "not_error": {
                "email": "amelchenko.dmitriy@outlook.com",
                "password": "LbvfbDbnz2Xfirb",
                "password_repeat": "LbvfbDbnz2Xfirb",
                "agreement": True
            },
            "email_error": {
                "email": "amelchenko.dmitriy",
                "password": "LbvfbDbnz2Xfirb",
                "password_repeat": "LbvfbDbnz2Xfirb",
                "agreement": True
            },
            "password_error": {
                "email": "amelchenko.dmitriy1@outlook.com",
                "password": "hello",
                "password_repeat": "hello",
                "agreement": True
            },
            "password_repeat_error": {
                "email": "amelchenko.dmitriy2@outlook.com",
                "password": "LbvfbDbnz2Xfirb",
                "password_repeat": "hello",
                "agreement": True
            },
            "agreement_error": {
                "email": "amelchenko.dmitriy3@outlook.com",
                "password": "LbvfbDbnz2Xfirb",
                "password_repeat": "LbvfbDbnz2Xfirb",
                "agreement": False
            },
        }

        self.all_files = os.listdir(settings.SALT_PATH)

    def test_not_error(self):
        http_client = test.client.Client()
        response = http_client.post("/user/registration/", self.test_data_form["not_error"])
        self.assertEqual(response.status_code, 200)

    # def test_email_error(self):
    #     form_registration = forms.RegistrationUser(
    #         initial=self.test_data_form["email_error"]
    #     )
    #     self.assertFalse(form_registration.is_valid())

    # def test_password_error(self):
    #     form_registration = forms.RegistrationUser(
    #         initial=self.test_data_form["password_error"]
    #     )
    #     self.assertFalse(form_registration.is_valid())

    # def test_password_repeat_error(self):
    #     form_registration = forms.RegistrationUser(
    #         initial=self.test_data_form["password_repeat_error"]
    #     )
    #     self.assertFalse(form_registration.is_valid())

    # def test_agreement_error(self):
    #     form_registration = forms.RegistrationUser(
    #         initial=self.test_data_form["agreement_error"]
    #     )
    #     self.assertFalse(form_registration.is_valid())

    # def test_form_save(self):
    #     form_registration = forms.RegistrationUser(
    #         initial=self.test_data_form["not_error"]
    #     )
    #     with self.assertRaises(Exception) as exc:
    #         form_registration.save()
    #     self.assertNotEqual(exc, Exception)

    def tearDown(self):
        new_file = os.listdir(settings.SALT_PATH)
        for file in new_file:
            if file not in self.all_files:
                os.unlink("{0}/{1}".format(settings.SALT_PATH, file))


class UserModelSave(test.TestCase):

    def setUp(self):
        self.test_user_data = {
            "email": "amelchenko.dmitriy@outlook.com",
            "password": "LbvfbDbnz2Xfirb",
        }
        self.all_files = os.listdir(settings.SALT_PATH)

    def test_form_test(self):
        user = models.User(
            login=self.test_user_data["email"],
            password=self.test_user_data["password"]
        )
        with self.assertRaises(Exception) as exc:
            user.save()
        self.assertNotEqual(exc, Exception)

    def tearDown(self):
        new_file = os.listdir(settings.SALT_PATH)
        for file in new_file:
            if file not in self.all_files:
                os.unlink("{0}/{1}".format(settings.SALT_PATH, file))
