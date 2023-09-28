import unittest
import json
import time
from app import app, keys  # Import your Flask app instance and keys dictionary


class TestServer(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()

    def test_jwks_endpoint(self):
        # Test the /auth/.well-known/jwks.json endpoint with valid keys
        response = self.app.get("/auth/.well-known/jwks.json")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains valid keys
        data = json.loads(response.data)
        self.assertIn("keys", data)
        self.assertTrue(len(data["keys"]) > 0)
        self.assertTrue(all(key in keys for key in data["keys"]))

    def test_jwks_endpoint_expired_keys(self):
        # Test the /auth/.well-known/jwks.json endpoint with expired keys
        # Simulate keys with expiry in the past
        for key_id in keys:
            keys[key_id]["key_expiry"] = int(time.time()) - 3600

        response = self.app.get("/auth/.well-known/jwks.json")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains an empty "keys" array
        data = json.loads(response.data)
        self.assertListEqual(data["keys"], [])

    def test_auth_endpoint(self):
        # Test the /auth endpoint
        response = self.app.post("/auth")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains an "access_token"
        data = json.loads(response.data)
        self.assertIn("access_token", data)

    # Add more test cases as needed to cover different scenarios and code paths

    def tearDown(self):
        # Reset keys to their original state for subsequent tests
        for key_id in keys:
            keys[key_id]["key_expiry"] = keys[key_id]["original_expiry"]


if __name__ == "__main__":
    unittest.main()
