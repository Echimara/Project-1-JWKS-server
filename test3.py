import unittest
import json
from your_server import app  # Import your Flask app instance


class TestServer(unittest.TestCase):
    # ...existing test cases...

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

    # Add more test cases as needed to cover different scenarios and code paths


if __name__ == "__main__":
    unittest.main()
