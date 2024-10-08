from PIL import Image
from PIL.PngImagePlugin import PngInfo
import re
import json
import base64

class PreserveImageMetadata:
    "Preserve the metadata from the original image, resaving the changed image with the metadata"
    def __init__(self):
        self.image_metadata = {}
        self.text_processor = TextProcessor()  # Initialize TextProcessor object
    
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
    
    def modify_metadata(self):
        chara_data = self.image_metadata.get('chara', None)
        if chara_data:
            decoded_json = json.loads(base64.b64decode(chara_data).decode('utf-8'))
            modified_json = self.modify_json_values(decoded_json)
            encoded_json = base64.b64encode(json.dumps(modified_json).encode('utf-8')).decode('utf-8')
            self.image_metadata['chara'] = encoded_json
    
    def modify_json_values(self, json_data):
        # Apply text processing to specific fields
        fields_to_process = ['first_mes', 'alternate_greetings', 'mes_example']
        for field in fields_to_process:
            if field in json_data['data']:
                if field == 'alternate_greetings':
                    json_data['data'][field] = [
                        self.text_processor.process_passage_based_on_content(greeting)
                        for greeting in json_data['data'][field]
                    ]
                elif field == 'mes_example':
                    json_data['data'][field] = self.text_processor.process_example_mes(json_data['data'][field])
                else:
                    json_data['data'][field] = self.text_processor.process_passage_based_on_content(json_data['data'][field])
        return json_data

class MetadataError(Exception):
    """Exception raised for errors in the input image metadata."""
    def __init__(self, message="Metadata is missing or corrupt"):
        self.message = message
        super().__init__(self.message)


# Process String
class TextProcessor:
    def __init__(self):
        # Initialize any necessary attributes (if needed)
        pass

    def add_quotes_to_unenclosed_text(self, passage):
        # Regex pattern to match text within asterisks and outside
        pattern = r"\*[^*]+\*|([^\*]+(?=\*)|(?<=\*)[^\*]+)"
        # List to hold the new string parts
        new_string_parts = []

        # Find all matches according to the pattern
        for match in re.finditer(pattern, passage):
            match_text = match.group()
            if match_text.startswith('*') and match_text.endswith('*'):
                new_string_parts.append(match_text)
            else:
                leading_whitespace = re.match(r'\s*', match_text).group()
                trailing_whitespace = re.search(r'\s*$', match_text).group()
                core_text = match_text.strip()
                if core_text:
                    new_string_parts.append(f'{leading_whitespace}\"{core_text}\"{trailing_whitespace}')
                else:
                    new_string_parts.append(match_text)
        return ''.join(new_string_parts)

    def strip_asterisks(self, passage):
        # Removes all asterisks from the passage
        return passage.replace('*', '')

    def process_example_mes(self, passage):
        # Regex to match <START>|{{char}}:|{{user}}: followed by content
        pattern = r"(<START>|{{char}}:|{{user}}:)(.*?)(?=(<START>|{{char}}:|{{user}}:)|$)"
        new_passage = ""

        for match in re.finditer(pattern, passage, re.DOTALL):
            group1 = match.group(1)
            group2 = match.group(2)

            # Apply string processing only to group2
            processed_group2 = self.process_passage_based_on_content(group2)

            # Rebuild the passage with processed group2
            new_passage += f"{group1}{processed_group2}"

        return new_passage

    def process_passage_based_on_content(self, passage):
        # Check for an odd number of either asterisks or quotes
        if passage.count('"') % 2 != 0 or passage.count('*') % 2 != 0:
            return passage  # Return unaltered if there's an odd number of quotes or asterisks
        
        # Check if the passage contains both quotes and asterisks
        if '"' in passage and '*' in passage:
            # If both quotes and asterisks exist, check if the passage only contains these enclosed texts
            # using the provided regex to strip all and check if it leaves an empty string.
            if re.sub(r"([\"*])(?:(?=(\\?))\2.)*?\1", "", passage).strip() == "":
                return self.strip_asterisks(passage)  # Remove all asterisks
            return passage  # Return unaltered if quotes and asterisks exist, but not fully enclosed
        elif '"' in passage:
            return passage  # Return unaltered, only quotes exist
        elif '*' in passage:
            # If only asterisks exist, process it by adding quotes and stripping asterisks
            processed_text = self.add_quotes_to_unenclosed_text(passage)
            return self.strip_asterisks(processed_text)  # Additionally, strip all asterisks
        else:
            return passage  # No quotes or asterisks, return unaltered

