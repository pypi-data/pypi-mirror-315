from .celery_config import make_celery, configure_celery
from .generate_task import register_tasks
from .replicatecode import process_image_and_mask
from .cloudinary_config import initialize_cloudinary, upload_to_cloudinary
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize Cloudinary (automatically on import)
initialize_cloudinary()

# Expose these symbols for external use
__all__ = ["make_celery", "configure_celery", "register_tasks", " process_image_and_mask", "initialize_cloudinary", "upload_to_cloudinary"]
