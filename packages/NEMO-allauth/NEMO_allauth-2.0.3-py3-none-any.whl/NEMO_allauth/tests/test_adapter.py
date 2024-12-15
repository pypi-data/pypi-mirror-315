from django.test import TestCase
from NEMO.tests.test_utilities import create_user_and_project

from NEMO_allauth.admin import send_user_email_confirmation


class AdapterTest(TestCase):

    def test_send_verification_email(self):
        user, project = create_user_and_project()
        send_user_email_confirmation(None, None, [user])
