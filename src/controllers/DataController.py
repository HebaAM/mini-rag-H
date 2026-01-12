from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseStatus
import os
import re



class DataController(BaseController):
    def __init__(self):
        super().__init__()  # Call the constructor of BaseController (CALL the parent constructor)
        self.size_scale = 1024 * 1024  # Convert MB to Bytes

    # Implement file validation logic here
    def validate_uploaded_file(self, file: UploadFile) -> bool:
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:   #file.size is bytes
            return False, ResponseStatus.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseStatus.FILE_VALIDATED_SUCCESS.value
    
    def get_clean_filename(self, original_filename: str) -> str:
                
        # removes everything except: letters (including Unicode), digits, underscore, and dot
        # strip leading/trailing spaces
        cleaned_filename = re.sub(r'[^\w.]', '', original_filename.strip())

        # replace spaces with underscores
        cleaned_filename.replace(' ', '_')

        return cleaned_filename 
        
    def create_unique_filename(self, original_filename: str, project_id: str) -> str:
        random_filename = self.generate_random_string()

        #Get folder where the file is stored
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.get_clean_filename(original_filename)

        unique_filename = os.path.join(project_path, random_filename + '_' + cleaned_filename)

        while os.path.exists(unique_filename):
            random_filename = self.generate_random_string()
            unique_filename = os.path.join(project_path, random_filename + '_' + cleaned_filename)

        return unique_filename







# removes everything except: letters (including Unicode), digits, underscore, and dot

        name, ext = os.path.splitext(original_filename)
        safe_name = ''.join(c for c in name if c.isalnum() or c in ('_', '.')).rstrip()
        random_str = self.generate_random_string(8)
        unique_filename = f"{safe_name}_{random_str}{ext}"
        return unique_filename



