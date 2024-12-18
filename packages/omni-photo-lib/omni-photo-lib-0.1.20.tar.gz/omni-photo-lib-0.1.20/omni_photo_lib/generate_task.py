from PIL import Image
import requests
from together import Together
import os
import logging
import replicate
import base64
import os
from .cloudinary_config import upload_to_cloudinary


logger = logging.getLogger(__name__)

# Ensure output folder exists
OUTPUT_FOLDER = os.path.abspath("output_files")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# The Celery app will be initialized externally and injected here
def register_tasks(celery):
    """
    Register tasks with an external Celery instance.
    """
    @celery.task(name="omni_photo_lib.process_image_and_mask_task")
    def process_image_and_mask_task(image_path, mask_path, prompt, upload_option=False):
        """
        Celery task to process an image and mask with the replicate API.

        Args:
            image_path (str): Path to the image file.
            mask_path (str): Path to the mask file.
            prompt (str): Prompt for the API.

        Returns:
            list: A list of output file paths where the processed images are saved.
        """
        import replicate
        import base64
        import os

        try:
            # Fetch the API token from the environment
            REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
            if not REPLICATE_API_TOKEN:
                raise ValueError("Please set the REPLICATE_API_TOKEN in your environment variables or .env file.")

            # Set the token for replicate
            replicate.Client(api_token=REPLICATE_API_TOKEN)

            # Encode image and mask to base64
            with open(image_path, 'rb') as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            with open(mask_path, 'rb') as mask_file:
                mask_data = base64.b64encode(mask_file.read()).decode('utf-8')

            # Prepare input for replicate API
            input_data = {
                "mask": f"data:application/octet-stream;base64,{mask_data}",
                "image": f"data:application/octet-stream;base64,{image_data}",
                "prompt": prompt,
            }

            # Call the replicate API
            output = replicate.run("black-forest-labs/flux-fill-dev", input=input_data)

            # Save output images locally and return file paths
            output_paths = []
            for index, item in enumerate(output):
                output_path = os.path.join("output_files", f"output_{index}.png")
                with open(output_path, "wb") as f:
                    f.write(item.read())  # Write the file to disk
                output_paths.append(output_path)  # Collect the output file path
            
            # Conditionally upload to Cloudinary
            if upload_option:
               cloudinary_urls = [upload_to_cloudinary(path, folder="inpainting_outputs") for path in output_paths]
               return {"file_paths": output_paths, "cloudinary_urls": cloudinary_urls}
            return {"file_paths": output_paths}

        except Exception as e:
            # Handle any errors and return an appropriate error message
            return {"error": str(e)}
    



   

    @celery.task(name="omni_photo_lib.generate_image_task")
    def generate_image_task(
        model_name,
        prompt,
        runtime,
        aspect_ratio,
        num_images,
        image_url=None,
        mask_url=None,
        task_type=None,
        style=None,
        seed=None,
        upload_option:False
    ):
        """
        Celery task to generate images using Together API.
        """
        try:

            def parse_aspect_ratio(aspect_ratio, base_size=512):
  
                try:
                    if ":" in aspect_ratio:
                         width_ratio, height_ratio = map(float, aspect_ratio.split(":"))
                         width = int(base_size * width_ratio)
                         height = int(base_size * height_ratio)
                    else:
                         width = height = base_size  # Default to square if aspect ratio is invalid
                    return width, height
                except Exception:
                       logger.warning("Invalid aspect ratio provided. Using default square dimensions.")
                       return base_size, base_size


            def get_runtime_parameters(runtime):
                if runtime == "short":
                   return 10
                elif runtime == "medium":
                     return 50
                elif runtime == "long":
                     return 100
                else:
                     return 50  # Default to medium


            # Parse aspect ratio and runtime parameters
            width, height = parse_aspect_ratio(aspect_ratio)
            steps = get_runtime_parameters(runtime)         

            TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
            if not TOGETHER_API_KEY:
                raise ValueError("Please set the TOGETHER_API_KEY in your environment variables or .env file.")
            # Replace 'YOUR_API_KEY' with a dynamic value from environment variables
            client = Together(api_key=TOGETHER_API_KEY)

            # Build request payload
            request_payload = {
                "model": model_name,
                "width": width,
                "height": height,
                "steps": steps,
                "prompt": prompt,
                "n": num_images,
                "style": style,
                "seed": seed
            }

            # Add specific parameters for task type
            if task_type == "depth_to_image" and image_url:
                request_payload["image_url"] = image_url
            elif task_type == "inpainting" and image_url and mask_url:
                request_payload["image_url"] = image_url
                request_payload["mask_url"] = mask_url

            # Generate images
            response = client.images.generate(**request_payload)

            # Save generated images locally
            image_paths = []
            if hasattr(response, "data") and isinstance(response.data, list):
                for idx, img_data in enumerate(response.data):
                    if hasattr(img_data, "url"):
                        output_path = os.path.join(
                            OUTPUT_FOLDER, f"{task_type}_output_{idx}.png"
                        )
                        img = Image.open(requests.get(img_data.url, stream=True).raw)
                        img.save(output_path)
                        image_paths.append(output_path)
                    else:
                        raise ValueError("Missing 'url' in API response")
            
            if upload_option:
               cloudinary_urls = [upload_to_cloudinary(path, folder="generated_outputs") for path in image_paths]
               return {"file_paths": image_paths, "cloudinary_urls": cloudinary_urls}
            return {"file_paths": image_paths}
          

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return str(e)

    return generate_image_task
