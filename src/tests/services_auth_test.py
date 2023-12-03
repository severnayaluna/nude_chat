import unittest

from models import User

from services import auth
from services.exceptions import *


class AuthTest(unittest.TestCase):
    def testreg_or_login(self):
        self.assertRaises(WrongType, auth.reg_or_login, 12345)
