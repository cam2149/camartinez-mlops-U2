import unittest
import httpx
import json
import base64
from datetime import datetime, timedelta
import pytz
from unittest.mock import patch

class TestHealthPredictionAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    TIMEZONE = pytz.timezone("America/Bogota")  # -05:00 as per provided time
    
    def setUp(self):
        """Set up the HTTP client for tests."""
        self.client = httpx.Client()

    def tearDown(self):
        """Close the HTTP client after tests."""
        self.client.close()

    def test_aprediction_counts_before_predictions(self):
        """Test that /prediction_counts is empty before any predictions."""
        response = self.client.get(f"{self.BASE_URL}/prediction_counts")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response is a dictionary
        self.assertIsInstance(data, dict)
        
        # Expect an empty dictionary if no predictions have been made
        self.assertEqual(data, {}, "Prediction counts should be empty before any predictions")
        
        # Note: If the app initializes prediction files with default counts (e.g., {"NO ENFERMO": 0, ...}),
        # uncomment the following to test for default values instead:
        # expected_defaults = {
        #     "NO ENFERMO": 0,
        #     "ENFERMEDAD LEVE": 0,
        #     "ENFERMEDAD AGUDA": 0,
        #     "ENFERMEDAD CRÓNICA": 0
        # }
        # self.assertEqual(data, expected_defaults, "Prediction counts should match default values")
    
    def test_get_prediction_counts(self):
        """Test GET /prediction_counts endpoint."""
        response = self.client.get(f"{self.BASE_URL}/prediction_counts")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response is a dictionary
        self.assertIsInstance(data, dict)
        
        # Validate keys are strings and values are integers
        for key, value in data.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, int)

    def test_get_last_predictions(self):
        """Test GET /last_predictions endpoint."""
        response = self.client.get(f"{self.BASE_URL}/last_predictions")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response is a list
        self.assertIsInstance(data, list)
        
        # Validate each prediction has estado and timestamp
        for prediction in data:
            self.assertIn("estado", prediction)
            self.assertIn("timestamp", prediction)
            self.assertIsInstance(prediction["estado"], str)
            try:
                datetime.fromisoformat(prediction["timestamp"].replace("Z", "+00:00"))
            except ValueError:
                self.fail("Timestamp is not in valid ISO format")

    def test_get_last_prediction_date(self):
        """Test GET /last_prediction_date endpoint."""
        response = self.client.get(f"{self.BASE_URL}/last_prediction_date")
        
        # Allow for 404 if no predictions exist
        if response.status_code == 404:
            return
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response structure
        self.assertIn("last_prediction_date", data)
        self.assertIn("estado", data)
        self.assertIsInstance(data["estado"], str)
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(data["last_prediction_date"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Last prediction date is not in valid ISO format")

    def test_get_report(self):
        """Test GET /getReport endpoint."""
        response = self.client.get(f"{self.BASE_URL}/getReport")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response structure
        self.assertIn("report_base64", data)
        self.assertIn("filename", data)
        self.assertIsInstance(data["report_base64"], str)
        self.assertIsInstance(data["filename"], str)
        
        # Validate base64 content
        try:
            base64.b64decode(data["report_base64"])
        except Exception:
            self.fail("Report_base64 is not valid Base64 encoded content")

    def test_prediction_and_last_prediction(self):
        """Test that a prediction is correctly reflected in last_predictions."""
        # Step 1: Make a prediction
        params = {"age": 20, "sex": "F", "arterialIndex": 130}
        prediction_response = self.client.get(f"{self.BASE_URL}/getprediction", params=params)
        
        self.assertEqual(prediction_response.status_code, 200)
        prediction_data = prediction_response.json()
        
        # Validate prediction response
        self.assertIn("estado", prediction_data)
        self.assertIn("timestamp", prediction_data)
        predicted_estado = prediction_data["estado"]
        predicted_timestamp = prediction_data["timestamp"]
        
        # Verify it's a disease state
        self.assertNotEqual(predicted_estado, "NO ENFERMO", "Prediction should indicate a disease state")
        self.assertEqual(predicted_estado, "ENFERMEDAD LEVE", "Expected ENFERMEDAD LEVE for given parameters")
        
        # Validate timestamp format
        try:
            prediction_time = datetime.fromisoformat(predicted_timestamp.replace("Z", "+00:00"))
        except ValueError:
            self.fail("Prediction timestamp is not in valid ISO format")
        
        # Step 2: Check last_predictions
        last_predictions_response = self.client.get(f"{self.BASE_URL}/last_predictions")
        
        self.assertEqual(last_predictions_response.status_code, 200)
        last_predictions = last_predictions_response.json()
        
        # Validate that last_predictions is not empty
        self.assertGreater(len(last_predictions), 0, "No predictions found in last_predictions")
        
        # Get the most recent prediction
        latest_prediction = last_predictions[0]  # Assumes sorted by timestamp descending
        
        # Validate structure
        self.assertIn("estado", latest_prediction)
        self.assertIn("timestamp", latest_prediction)
        
        # Verify the latest prediction matches
        self.assertEqual(latest_prediction["estado"], predicted_estado, 
                        f"Latest prediction estado ({latest_prediction['estado']}) does not match predicted estado ({predicted_estado})")
        
        # Validate timestamp is close to prediction time (within 5 seconds to account for delays)
        try:
            latest_time = datetime.fromisoformat(latest_prediction["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Latest prediction timestamp is not in valid ISO format")
        
        time_diff = abs((latest_time - prediction_time).total_seconds())
        self.assertLessEqual(time_diff, 5, 
                           f"Latest prediction timestamp ({latest_prediction['timestamp']}) is too far from prediction timestamp ({predicted_timestamp})")

    def test_get_prediction_no_enfermo(self):
        """Test GET /getprediction with age=20, sex=M, arterialIndex=120."""
        params = {"age": 20, "sex": "M", "arterialIndex": 120}
        response = self.client.get(f"{self.BASE_URL}/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response structure
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        
        # Validate expected estado
        self.assertEqual(data["estado"], "NO ENFERMO", 
                         f"Expected estado 'NO ENFERMO', got '{data['estado']}'")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    def test_get_prediction_enfermedad_leve(self):
        """Test GET /getprediction with age=20, sex=F, arterialIndex=130."""
        params = {"age": 20, "sex": "F", "arterialIndex": 130}
        response = self.client.get(f"{self.BASE_URL}/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response structure
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        
        # Validate expected estado
        self.assertEqual(data["estado"], "ENFERMEDAD LEVE", 
                         f"Expected estado 'ENFERMEDAD LEVE', got '{data['estado']}'")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    def test_get_prediction_enfermedad_aguda(self):
        """Test GET /getprediction with age=20, sex=F, arterialIndex=170."""
        params = {"age": 20, "sex": "F", "arterialIndex": 170}
        response = self.client.get(f"{self.BASE_URL}/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response structure
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        
        # Validate expected estado
        self.assertEqual(data["estado"], "ENFERMEDAD AGUDA", 
                         f"Expected estado 'ENFERMEDAD AGUDA', got '{data['estado']}'")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    def test_get_prediction_enfermedad_cronica(self):
        """Test GET /getprediction with age=20, sex=M, arterialIndex=190."""
        params = {"age": 20, "sex": "M", "arterialIndex": 190}
        response = self.client.get(f"{self.BASE_URL}/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response structure
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        
        # Validate expected estado
        self.assertEqual(data["estado"], "ENFERMEDAD CRÓNICA", 
                         f"Expected estado 'ENFERMEDAD CRÓNICA', got '{data['estado']}'")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    def test_get_prediction_enfermedad_terminal(self):
        """Test GET /getprediction with age=20, sex=F, arterialIndex=500."""
        params = {"age": 20, "sex": "F", "arterialIndex": 500}
        response = self.client.get(f"{self.BASE_URL}/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Validate response structure
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        
        # Validate expected estado
        self.assertEqual(data["estado"], "ENFERMEDAD TERMINAL", 
                         f"Expected estado 'ENFERMEDAD TERMINAL', got '{data['estado']}'")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")


if __name__ == "__main__":
    unittest.main()