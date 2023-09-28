import unittest
import json
from your_server import app  # Import your Flask app instance


class TestServer(unittest.TestCase):
    # ...existing test cases...

    def test_auth_endpoint_no_expired_param(self):
        # Test the /auth endpoint without the "expired" query parameter
        response = self.app.post("/auth")
        self.assertEqual(response.status_code, 200)

        # Verify that the response contains an access_token
        data = json.loads(response.data)
        self.assertIn("access_token", data)

    # Add more test cases as needed to cover different scenarios and code paths


if __name__ == "__main__":
    unittest.main()
