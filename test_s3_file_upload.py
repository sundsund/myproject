import unittest
from unittest.mock import patch, MagicMock, mock_open
import importlib
import sys

class TestS3FileUpload(unittest.TestCase):

    @patch('boto3.resource') # Patch boto3.resource globally for the duration of the test
    @patch('builtins.open', new_callable=mock_open, read_data=b"test data") # Patch builtins.open
    def test_upload_success(self, mock_file_open, mock_boto_resource):
        # Ensure a clean import if s3_file_upload was somehow already imported
        if 's3_file_upload' in sys.modules:
            del sys.modules['s3_file_upload']

        # Setup mock S3 resource and bucket
        mock_s3_instance = MagicMock()
        mock_bucket = MagicMock()
        mock_boto_resource.return_value = mock_s3_instance
        mock_s3_instance.Bucket.return_value = mock_bucket

        # Import the module under test HERE, after mocks are active
        import s3_file_upload

        # Assertions
        mock_boto_resource.assert_called_once_with(
            's3',
            aws_access_key_id=s3_file_upload.ACCESS_KEY_ID,
            aws_secret_access_key=s3_file_upload.ACCESS_SECRET_KEY,
            config=unittest.mock.ANY
        )

        mock_s3_instance.Bucket.assert_called_once_with(s3_file_upload.BUCKET_NAME)

        mock_file_open.assert_called_once_with(s3_file_upload.FILE_NAME, 'rb')

        # The 'Body' should be the file handle returned by the mocked 'open'
        # which is mock_file_open.return_value
        mock_bucket.put_object.assert_called_once_with(
            Key=s3_file_upload.FILE_NAME,
            Body=mock_file_open.return_value,
            ACL='public-read'
        )

        # It's good practice to ensure the mocked file was closed if the original script did.
        # The provided script does not explicitly close the file.
        # If it did, e.g., with 'with open(...)', then mock_file_open.return_value.close.assert_called_once()
        # would be relevant.

if __name__ == '__main__':
    unittest.main()
