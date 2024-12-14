import cloudinary
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

def initialize_cloudinary(cloud_name, api_key, api_secret):
    """
    Initialize Cloudinary configuration.
    """
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        logger.info("Cloudinary initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing Cloudinary: {e}")
        raise ValueError("Failed to initialize Cloudinary configuration")

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
