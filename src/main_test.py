import unittest

import settings

from models import User

settings.TEST_DB.create_tables([User,])

import tests.services_auth_test


unittest.main(tests.services_auth_test)
