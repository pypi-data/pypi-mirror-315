import os
import cloudinary
import cloudinary.uploader
import logging
from dotenv import load_dotenv 

logger = logging.getLogger(__name__)

load_dotenv()

def initialize_cloudinary():
    """
    Initialize Cloudinary configuration using environment variables.
    """
    try:
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")

        if not cloud_name or not api_key or not api_secret:
            raise ValueError("Cloudinary configuration is incomplete. Ensure CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET are set.")

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        logger.info("Cloudinary initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing Cloudinary: {e}")
        raise ValueError("Failed to initialize Cloudinary configuration.")

def upload_to_cloudinary(file_path, folder="default_folder"):
    """
    Upload an image file to Cloudinary and return the public URL.
    """
    try:
        result = cloudinary.uploader.upload(file_path, folder=folder)
        return result["url"]  # Return the public URL of the uploaded image
    except Exception as e:
        logger.error(f"Error uploading to Cloudinary: {e}")
        raise ValueError("Failed to upload image to Cloudinary")
