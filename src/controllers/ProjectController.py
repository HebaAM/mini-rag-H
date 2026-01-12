from .BaseController import BaseController
import os


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()  # Call the constructor of BaseController (CALL the parent constructor)

    def get_project_path(self, project_id: str):
        # Implement logic to check if the project folder exists
        
        project_dir = os.path.join(self.files_dir, project_id)

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        return project_dir