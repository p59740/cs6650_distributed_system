import logging
import logging.handlers  # Needed for rotating logs
import boto3
import time

# ✅ Step 1: Create a logger
logger = logging.getLogger("s3_test_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent duplicate logs

# ✅ Step 2: Add a rotating file handler
log_file = "s3_rotating_test.log"
file_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=500_000, backupCount=2  # 🔹 Reduce file size to 500KB, keep only 2 backups
)
console_handler = logging.StreamHandler()  # Print logs to console

# ✅ Step 3: Apply same format to both handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# ✅ Step 4: Attach handlers
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# ✅ Step 5: Test Logging
logger.info("This is a test log message!")
for i in range(5000):  # Simulate many log entries
    if i % 100 == 0:  # 🔹 Log only every 100 iterations
        logger.info(f"Log entry {i}")
    time.sleep(0.1)