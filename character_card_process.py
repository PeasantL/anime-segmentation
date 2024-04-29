from PIL import Image
from PIL.PngImagePlugin import PngInfo

class PreserveImageMetadata:
    "Preserve the metadata from the original image, resaving the changed image with the metadata"
    def __init__(self):
        self.image_metadata = {}
    
    def extract_image_metadata(self, original_image_path):
        try:
            with Image.open(original_image_path) as image:
                image.load()
                if 'chara' not in image.info:
                    raise MetadataError("PNG is not a valid character card")
                self.image_metadata = dict(image.info)

        except IOError as e:
            print(f"Failed to load image {original_image_path}: {e}")
        except MetadataError as e:
            raise
        
    def valid_metadata(self):
        return self.image_metadata
    
    def save_image_with_metadata(self, altered_image_path):
        try:
            with Image.open(altered_image_path) as image:
                image.load()
                metadata = PngInfo()
                for key, value in self.image_metadata.items():
                    metadata.add_text(key, value)
                image.save(altered_image_path, pnginfo=metadata)

        except IOError as e:
            print(f"Failed to load image {altered_image_path}: {e}")

class MetadataError(Exception):
    """Exception raised for errors in the input image metadata."""
    def __init__(self, message="Metadata is missing or corrupt"):
        self.message = message
        super().__init__(self.message)