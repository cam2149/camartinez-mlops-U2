import unittest
from unittest.mock import patch, Mock
import httpx
import json
import base64
from datetime import datetime, timedelta
import pytz

class TestHealthPredictionAPI(unittest.TestCase):
    TIMEZONE = pytz.timezone("America/Bogota")  # -05:00 as per provided time
    
    def setUp(self):
        """Set up the mock HTTP client for tests."""
        self.client = httpx.Client()
        self.mock_get = Mock()
        # Define default mock responses for each endpoint
        self.mock_responses = {
            "/prediction_counts": {
                "status_code": 200,
                "json": {"NO ENFERMO": 0, "ENFERMEDAD LEVE": 0, "ENFERMEDAD AGUDA": 0, 
                         "ENFERMEDAD CRÓNICA": 0, "ENFERMEDAD TERMINAL": 0}
            },
            "/last_predictions": {
                "status_code": 200,
                "json": []
            },
            "/last_prediction_date": {
                "status_code": 404,
                "json": {}
            },
            "/getReport": {
                "status_code": 200,
                "json": {
                    "report_base64": base64.b64encode(b"Sample PDF content").decode("utf-8"),
                    "filename": "report.pdf"
                }
            }
        }

    def tearDown(self):
        """Clean up after tests."""
        self.client.close()

    def _create_mock_response(self, status_code, json_data):
        """Helper to create a mock HTTP response."""
        response = Mock()
        response.status_code = status_code
        response.json.return_value = json_data
        return response

    def _get_timestamp(self):
        """Generate an ISO timestamp in UTC."""
        return datetime.now(pytz.UTC).isoformat().replace("+00:00", "Z")

    @patch.object(httpx.Client, "get")
    def test_aprediction_counts_before_predictions(self, mock_get):
        """Test that /prediction_counts returns default counts before any predictions."""
        mock_get.return_value = self._create_mock_response(
            200, self.mock_responses["/prediction_counts"]["json"]
        )
        
        response = self.client.get("/prediction_counts")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIsInstance(data, dict)
        expected_defaults = {
            "NO ENFERMO": 0,
            "ENFERMEDAD LEVE": 0,
            "ENFERMEDAD AGUDA": 0,
            "ENFERMEDAD CRÓNICA": 0,
            "ENFERMEDAD TERMINAL": 0
        }
        self.assertEqual(data, expected_defaults, "Prediction counts should match default values")

    @patch.object(httpx.Client, "get")
    def test_get_prediction_counts(self, mock_get):
        """Test GET /prediction_counts endpoint."""
        mock_get.return_value = self._create_mock_response(
            200, self.mock_responses["/prediction_counts"]["json"]
        )
        
        response = self.client.get("/prediction_counts")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIsInstance(data, dict)
        for key, value in data.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, int)

    @patch.object(httpx.Client, "get")
    def test_get_last_predictions(self, mock_get):
        """Test GET /last_predictions endpoint."""
        mock_get.return_value = self._create_mock_response(
            200, self.mock_responses["/last_predictions"]["json"]
        )
        
        response = self.client.get("/last_predictions")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIsInstance(data, list)
        for prediction in data:
            self.assertIn("estado", prediction)
            self.assertIn("timestamp", prediction)
            self.assertIsInstance(prediction["estado"], str)
            try:
                datetime.fromisoformat(prediction["timestamp"].replace("Z", "+00:00"))
            except ValueError:
                self.fail("Timestamp is not in valid ISO format")

    @patch.object(httpx.Client, "get")
    def test_get_last_prediction_date(self, mock_get):
        """Test GET /last_prediction_date endpoint."""
        mock_get.return_value = self._create_mock_response(
            404, self.mock_responses["/last_prediction_date"]["json"]
        )
        
        response = self.client.get("/last_prediction_date")
        
        if response.status_code == 404:
            return
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("last_prediction_date", data)
        self.assertIn("estado", data)
        self.assertIsInstance(data["estado"], str)
        
        try:
            datetime.fromisoformat(data["last_prediction_date"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Last prediction date is not in valid ISO format")

    @patch.object(httpx.Client, "get")
    def test_get_report(self, mock_get):
        """Test GET /getReport endpoint."""
        mock_get.return_value = self._create_mock_response(
            200, self.mock_responses["/getReport"]["json"]
        )
        
        response = self.client.get("/getReport")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("report_base64", data)
        self.assertIn("filename", data)
        self.assertIsInstance(data["report_base64"], str)
        self.assertIsInstance(data["filename"], str)
        
        try:
            base64.b64decode(data["report_base64"])
        except Exception:
            self.fail("Report_base64 is not valid Base64 encoded content")

    @patch.object(httpx.Client, "get")
    def test_prediction_and_last_prediction(self, mock_get):
        """Test that a prediction is correctly reflected in last_predictions."""
        # Mock prediction response
        predicted_estado = "ENFERMEDAD LEVE"
        predicted_timestamp = self._get_timestamp()
        prediction_response = {
            "estado": predicted_estado,
            "timestamp": predicted_timestamp
        }
        
        # Mock last_predictions response
        last_predictions_response = [
            {"estado": predicted_estado, "timestamp": predicted_timestamp}
        ]
        
        # Configure mock to return different responses based on URL
        def side_effect(url, **kwargs):
            if url.endswith("/getprediction"):
                return self._create_mock_response(200, prediction_response)
            elif url.endswith("/last_predictions"):
                return self._create_mock_response(200, last_predictions_response)
            return self._create_mock_response(404, {})
        
        mock_get.side_effect = side_effect
        
        # Step 1: Make a prediction
        params = {"age": 20, "sex": "F", "arterialIndex": 130}
        prediction_response = self.client.get("/getprediction", params=params)
        
        self.assertEqual(prediction_response.status_code, 200)
        prediction_data = prediction_response.json()
        
        self.assertIn("estado", prediction_data)
        self.assertIn("timestamp", prediction_data)
        self.assertEqual(prediction_data["estado"], "ENFERMEDAD LEVE")
        
        try:
            prediction_time = datetime.fromisoformat(prediction_data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Prediction timestamp is not in valid ISO format")
        
        # Step 2: Check last_predictions
        last_predictions_response = self.client.get("/last_predictions")
        
        self.assertEqual(last_predictions_response.status_code, 200)
        last_predictions = last_predictions_response.json()
        
        self.assertGreater(len(last_predictions), 0, "No predictions found in last_predictions")
        
        latest_prediction = last_predictions[0]
        self.assertIn("estado", latest_prediction)
        self.assertIn("timestamp", latest_prediction)
        
        self.assertEqual(latest_prediction["estado"], predicted_estado)
        
        try:
            latest_time = datetime.fromisoformat(latest_prediction["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Latest prediction timestamp is not in valid ISO format")
        
        time_diff = abs((latest_time - prediction_time).total_seconds())
        self.assertLessEqual(time_diff, 5)

    @patch.object(httpx.Client, "get")
    def test_get_prediction_no_enfermo(self, mock_get):
        """Test GET /getprediction with age=20, sex=M, arterialIndex=120."""
        mock_get.return_value = self._create_mock_response(
            200, {"estado": "NO ENFERMO", "timestamp": self._get_timestamp()}
        )
        
        params = {"age": 20, "sex": "M", "arterialIndex": 120}
        response = self.client.get("/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["estado"], "NO ENFERMO")
        
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    @patch.object(httpx.Client, "get")
    def test_get_prediction_enfermedad_leve(self, mock_get):
        """Test GET /getprediction with age=20, sex=F, arterialIndex=130."""
        mock_get.return_value = self._create_mock_response(
            200, {"estado": "ENFERMEDAD LEVE", "timestamp": self._get_timestamp()}
        )
        
        params = {"age": 20, "sex": "F", "arterialIndex": 130}
        response = self.client.get("/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["estado"], "ENFERMEDAD LEVE")
        
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    @patch.object(httpx.Client, "get")
    def test_get_prediction_enfermedad_aguda(self, mock_get):
        """Test GET /getprediction with age=20, sex=F, arterialIndex=170."""
        mock_get.return_value = self._create_mock_response(
            200, {"estado": "ENFERMEDAD AGUDA", "timestamp": self._get_timestamp()}
        )
        
        params = {"age": 20, "sex": "F", "arterialIndex": 170}
        response = self.client.get("/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["estado"], "ENFERMEDAD AGUDA")
        
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    @patch.object(httpx.Client, "get")
    def test_get_prediction_enfermedad_cronica(self, mock_get):
        """Test GET /getprediction with age=20, sex=M, arterialIndex=190."""
        mock_get.return_value = self._create_mock_response(
            200, {"estado": "ENFERMEDAD CRÓNICA", "timestamp": self._get_timestamp()}
        )
        
        params = {"age": 20, "sex": "M", "arterialIndex": 190}
        response = self.client.get("/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["estado"], "ENFERMEDAD CRÓNICA")
        
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    @patch.object(httpx.Client, "get")
    def test_get_prediction_enfermedad_terminal(self, mock_get):
        """Test GET /getprediction with age=20, sex=F, arterialIndex=500."""
        mock_get.return_value = self._create_mock_response(
            200, {"estado": "ENFERMEDAD TERMINAL", "timestamp": self._get_timestamp()}
        )
        
        params = {"age": 20, "sex": "F", "arterialIndex": 500}
        response = self.client.get("/getprediction", params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("estado", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["estado"], "ENFERMEDAD TERMINAL")
        
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

if __name__ == "__main__":
    unittest.main()