import unittest
import json
from app import app  # Import your Flask app instance


class TestServer(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()

    def tearDown(self):
        pass  # Clean up resources if needed

    def test_jwks_endpoint(self):
        # Test the /jwks endpoint
        response = self.app.get("/jwks")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains a "keys" field
        data = json.loads(response.data)
        self.assertIn("keys", data)

        # Add more assertions as needed to validate the response data

    def test_auth_endpoint(self):
        # Test the /auth endpoint
        response = self.app.post("/auth")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains an "access_token"
        data = json.loads(response.data)
        self.assertIn("access_token", data)

        # Add more assertions as needed to validate the response data

    def test_auth_endpoint_no_expired_param(self):
        # Test the /auth endpoint without the "expired" query parameter
        response = self.app.post("/auth")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains an "access_token"
        data = json.loads(response.data)
        self.assertIn("access_token", data)

    def test_auth_endpoint_expired_param(self):
        # Test the /auth endpoint with the "expired" query parameter
        response = self.app.post("/auth?expired=true")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains an "access_token"
        data = json.loads(response.data)
        self.assertIn("access_token", data)

    def test_invalid_input(self):
        # Test the /auth endpoint with invalid input data
        invalid_data = {"username": "user", "password": "pass"}
        response = self.app.post(
            "/auth", data=json.dumps(invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        # Verify that the response contains an error message
        data = json.loads(response.data)
        self.assertIn("error", data)

    # Add more test cases as needed to cover different scenarios and code paths


if __name__ == "__main__":
    unittest.main()
