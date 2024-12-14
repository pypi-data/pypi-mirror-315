class S3Error(Exception):
    """Base class for all S3 exceptions."""


class S3InvalidBucketNameError(S3Error):
    """Exception raised for invalid S3 bucket names."""


class InvalidObjectKeyError(S3Error):
    """Exception raised for invalid S3 object keys."""


class InvalidFileUploadError(S3Error):
    """Exception raised for invalid S3 file uploads."""


class S3FileNotFoundError(S3Error, FileNotFoundError):
    """Exception raised for file not found."""


class S3BucketPolicyGetError(S3Error):
    """Exception raised for S3 bucket policy get errors."""


class S3BucketPolicyUpdateError(S3Error):
    """Exception raised for S3 bucket policy update errors."""


class S3LambdaPermissionAddError(S3Error):
    """Exception raised for S3 lambda permission add errors."""


class S3LambdaNotificationAddError(S3Error):
    """Exception raised for S3 lambda notification add errors."""


class S3LambdaNotificationRemoveError(S3Error):
    """Exception raised for S3 lambda notification remove errors."""
