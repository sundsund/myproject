import unittest
from unittest.mock import patch, MagicMock
import json
import io

# Import the lambda handler function
from S3_File_Upload_lambda import lambda_handler

class TestS3FileUploadLambda(unittest.TestCase):

    def _create_sample_s3_event(self, bucket_name="test-bucket", object_key="test.csv"):
        """Helper function to create a sample S3 event."""
        return {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": bucket_name
                        },
                        "object": {
                            "key": object_key
                        }
                    }
                }
            ]
        }

    @patch('S3_File_Upload_lambda.s3_client.get_object')
    @patch('builtins.print')
    def test_successful_csv_processing(self, mock_print, mock_get_object):
        # Mock S3 get_object response
        csv_data = "Header1,Header2,Header3\n2023,50000,15000\n2024,10000,25000"
        mock_s3_response_body = MagicMock()
        mock_s3_response_body.read.return_value = csv_data.encode('utf-8')
        mock_get_object.return_value = {"Body": mock_s3_response_body}

        sample_event = self._create_sample_s3_event()
        expected_bucket = sample_event['Records'][0]['s3']['bucket']['name']
        expected_key = sample_event['Records'][0]['s3']['object']['key']

        response = lambda_handler(sample_event, None)

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], json.dumps('File processed successfully!'))

        mock_get_object.assert_called_once_with(Bucket=expected_bucket, Key=expected_key)

        # Check print calls
        expected_print_calls = [
            unittest.mock.call(f"Bucket: {expected_bucket}, Key: {expected_key}"),
            unittest.mock.call("Year: 2023, Mileage: 50000, Price: 15000"),
            unittest.mock.call("Year: 2024, Mileage: 10000, Price: 25000")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

    @patch('S3_File_Upload_lambda.s3_client.get_object')
    @patch('builtins.print')
    def test_error_during_get_object(self, mock_print, mock_get_object):
        # Mock S3 get_object to raise an exception
        error_message = "Simulated S3 error"
        mock_get_object.side_effect = Exception(error_message)

        sample_event = self._create_sample_s3_event()
        expected_bucket = sample_event['Records'][0]['s3']['bucket']['name']
        expected_key = sample_event['Records'][0]['s3']['object']['key']

        response = lambda_handler(sample_event, None)

        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(response['body'], json.dumps(f'Error processing file: {error_message}'))

        mock_get_object.assert_called_once_with(Bucket=expected_bucket, Key=expected_key)
        # Check that the error was printed
        # The first print is always Bucket/Key, the second is the exception object
        printed_error = False
        for call_args in mock_print.call_args_list:
            arg = call_args[0][0]
            if isinstance(arg, Exception) and str(arg) == error_message:
                printed_error = True
                break
        self.assertTrue(printed_error, f"Exception with message '{error_message}' was not printed. Actual calls: {mock_print.call_args_list}")


    @patch('S3_File_Upload_lambda.s3_client.get_object')
    @patch('builtins.print')
    def test_error_during_csv_processing_malformed_data(self, mock_print, mock_get_object):
        # Mock S3 get_object response with malformed CSV (not enough columns)
        csv_data = "Header1,Header2,Header3\n2023,50000" # Missing one column
        mock_s3_response_body = MagicMock()
        mock_s3_response_body.read.return_value = csv_data.encode('utf-8')
        mock_get_object.return_value = {"Body": mock_s3_response_body}

        sample_event = self._create_sample_s3_event()

        response = lambda_handler(sample_event, None)

        self.assertEqual(response['statusCode'], 500)
        # The exact error message might vary, so we check for a part of it.
        # This error would be an IndexError: list index out of range
        self.assertTrue("Error processing file" in response['body'])
        self.assertTrue("list index out of range" in response['body'])

        # Check that the specific exception was printed
        # The first print is Bucket/Key, the second is the exception object itself
        # We can check that print was called with an IndexError instance
        printed_error = False
        for call_args in mock_print.call_args_list:
            if isinstance(call_args[0][0], IndexError):
                printed_error = True
                break
        self.assertTrue(printed_error, "IndexError was not printed")

if __name__ == '__main__':
    unittest.main()
