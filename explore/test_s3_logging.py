import boto3
import time
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set logging level to INFO

# Create file handler (saves logs to a file)
file_handler = logging.FileHandler("s3_test.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Create stream handler (prints logs to the terminal)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Generate a unique bucket name
bucket_name = f"my-test-bucket-{int(time.time())}"
test_file = "testfile.txt"
downloaded_file = "downloaded_testfile.txt"

# Create an S3 client
s3 = boto3.client("s3")

try:
    logger.info(f"Creating S3 bucket: {bucket_name}")
    s3.create_bucket(Bucket=bucket_name)

    logger.info("Creating a test file")
    with open(test_file, "w") as f:
        f.write("Hello, AWS S3!")

    logger.info("Uploading test file to S3")
    s3.upload_file(test_file, bucket_name, test_file)

    logger.info("Listing files in S3 bucket")
    objects = s3.list_objects_v2(Bucket=bucket_name)
    if "Contents" in objects:
        for obj in objects["Contents"]:
            logger.info(f" - {obj['Key']}")

    logger.info("Downloading file from S3 to verify")
    s3.download_file(bucket_name, test_file, downloaded_file)

    logger.info("Checking file contents")
    with open(downloaded_file, "r") as f:
        logger.info(f.read())

    logger.info("Deleting test file from S3")
    s3.delete_object(Bucket=bucket_name, Key=test_file)

    logger.info("Deleting S3 bucket")
    s3.delete_bucket(Bucket=bucket_name)

    logger.info("✅ S3 test completed successfully!")

except Exception as e:
    logger.error(f"❌ Error: {e}")