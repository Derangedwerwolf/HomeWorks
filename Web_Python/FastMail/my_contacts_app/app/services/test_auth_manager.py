import unittest
import jwt

from unittest.mock import MagicMock
from services.auth_manager import AuthManager
from sqlalchemy.orm import Session


class TestVerifyPassword(unittest.TestCase):
    def setUp(self):
        self.auth_manager = AuthManager()
        self.pwd_context_mock = MagicMock()
        self.auth_manager.pwd_context = self.pwd_context_mock
        self.session_mock = MagicMock(spec=Session)
        self.auth_manager._db = self.session_mock

        self.test_data = {"sub": "test@example.com"}
        self.encoded_token = jwt.encode(
            self.test_data, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        self.expected_token = self.encoded_token

    def test_verify_password_correct(self):
        plain_password = "password"
        hashed_password = "bcrypted_password"
        self.pwd_context_mock.verify.return_value = True
        self.assertTrue(
            self.auth_manager.verify_password(plain_password, hashed_password)
        )

    def test_verify_password_incorrect(self):
        plain_password = "wrong_password"
        hashed_password = "bcrypted_password"
        self.pwd_context_mock.verify.return_value = False
        self.assertFalse(
            self.auth_manager.verify_password(plain_password, hashed_password)
        )

    def test_verify_password_empty_password(self):
        plain_password = ""
        hashed_password = "bcrypted_password"
        self.pwd_context_mock.verify.return_value = False
        self.assertFalse(
            self.auth_manager.verify_password(plain_password, hashed_password)
        )

    def test_verify_password_empty_hashed_password(self):
        plain_password = "password"
        hashed_password = ""
        self.pwd_context_mock.verify.return_value = False
        self.assertFalse(
            self.auth_manager.verify_password(plain_password, hashed_password)
        )

    def test_get_password_hash_correct(self):
        password = "password"
        expected_hash = "bcrypted_password"
        self.pwd_context_mock.hash.return_value = expected_hash
        self.assertEqual(self.auth_manager.get_password_hash(password), expected_hash)

    def test_get_password_hash_empty_password(self):
        password = ""
        self.pwd_context_mock.hash.return_value = None
        self.assertIsNone(self.auth_manager.get_password_hash(password))

    def test_get_password_hash_invalid_password(self):
        password = "invalid_password"
        self.pwd_context_mock.hash.return_value = None
        self.assertIsNone(self.auth_manager.get_password_hash(password))

    def test_create_access_token_correct(self):
        expires_delta = 30

        actual_token = self.auth_manager.create_access_token(
            self.test_data, expires_delta
        )

        self.assertEqual(actual_token, self.expected_token)

    def test_create_access_token_incorrect_data(self):
        data = {}
        expires_delta = 30

        with self.assertRaises(ValueError):
            self.auth_manager.create_access_token(data, expires_delta)

    def test_create_access_token_incorrect_expires_delta(self):
        data = {"sub": "test@example.com"}
        expires_delta = -1

        with self.assertRaises(ValueError):
            self.auth_manager.create_access_token(data, expires_delta)

    def test_create_refresh_token_correct(self):
        expires_delta = 7

        actual_token = self.auth_manager.create_refresh_token(
            self.test_data, expires_delta
        )

        self.assertEqual(actual_token, self.expected_token)

    def test_create_refresh_token_incorrect_data(self):
        data = {}
        expires_delta = 7

        with self.assertRaises(ValueError):
            self.auth_manager.create_refresh_token(data, expires_delta)

    def test_create_refresh_token_incorrect_expires_delta(self):
        data = {"sub": "test@example.com"}
        expires_delta = -1

        with self.assertRaises(ValueError):
            self.auth_manager.create_refresh_token(data, expires_delta)
