from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import os
from models import ResponseStatus
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api-v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings=Depends(get_settings)):
    # Validate File (e.g., extension, size, etc.)
    # This better be done in a separate utility function/module (controller)
    data_controller = DataController()
    is_valid, status_msg = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": status_msg})
    # else:
    #     return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": status_msg})

    # # Save File to Project Directory
    # project_folder_path = ProjectController().get_project_path(project_id=project_id)
    # saved_file_path = os.path.join(project_folder_path, file.filename)

    # Get unique file path instead   
    saved_file_path = data_controller.create_unique_filename(original_filename=file.filename, project_id=project_id)
    
    # Save the uploaded file asynchronously
    # Wrap in try-except for better error handling in production code
    try:
        async with aiofiles.open(saved_file_path, 'wb') as out_file:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):  # Read file in chunks
                await out_file.write(chunk)  # Write chunk to destination file
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"msg": ResponseStatus.FILE_UPLOAD_FAILED.value + f" Error: {str(e)}"})

    return JSONResponse(content={"msg": ResponseStatus.FILE_UPLOAD_SUCCESS.value})

