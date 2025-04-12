from backend.utils.config_loader import get_secret_key
from typing import Optional, List
from backend.knowledge.knowledge_manager import KnowledgeManager
from backend.dao.management_dao import ManagementDAO
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Form, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from io import BytesIO

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        management_dao = ManagementDAO()
        app.state.knowledge = KnowledgeManager(management_dao)
        logger.info("Resources initialized successfully.")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Cleaning up resources...")


app = FastAPI(
    title="Knowledge Management System API",
    lifespan=lifespan
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Config
SECRET_KEY = get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(credentials.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_knowledge(app: FastAPI = Depends()):
    return app.state.knowledge


router = APIRouter()


# signup
@router.post("/kms/auth/signup")
async def sign_up(
        email: str = Form(...),
        password: str = Form(...),
        name: str = Form(...),
        department_id: str = Form(...),
        roles: List[str] = Form(...),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    success = knowledge.sign_up(
        email=email,
        password=password,
        name=name,
        department_id=department_id,
        roles=roles
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User creation failed. Possibly due to duplicate email or invalid data."
        )

    return {"message": "User created successfully"}


# login
@router.post("/kms/auth/login")
async def login(
        email: str = Form(...),
        password: str = Form(...),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    if not knowledge.login(email.strip(), password.strip()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(data={"sub": email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "message": "login successfully",
        "access_token": token,
        "token_type": "bearer"
    }


# upload document
@router.post("/kms/document")
async def upload_document(
        document: UploadFile = File(...),
        name: Optional[str] = Form(None),
        doc_type: Optional[str] = Form(None),
        department_id: Optional[str] = Form(None),
        tags: Optional[List[str]] = Form([]),
        owner: Optional[str] = Form(None),
        category: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        university: Optional[str] = Form(None),
        _: None = Depends(verify_token),  # verify token
        knowledge: KnowledgeManager = Depends(get_knowledge)

):
    name = name or document.filename
    content = await document.read()
    content_io = BytesIO(content)

    try:
        result = knowledge.upload(
            content=content_io,
            name=name,
            doc_type=doc_type,
            department_id=department_id,
            tags=tags,
            owner=owner,
            category=category,
            description=description,
            university=university
        )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# get current user
@router.get("/kms/auth/me")
async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        payload = decode_token(credentials.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user = knowledge.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# get document metadata
@router.get("/kms/document/{document_id}")
async def get_document_meta(
    document_id: str,
    user_id: str,
    _: None = Depends(verify_token),
    knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        metadata = knowledge.get_metadata(document_id=document_id, user_id=user_id)
        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found or access denied"
            )
        return metadata
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# get document content
@router.get("/kms/document/{document_id}/content")
async def get_document_content(
        document_id: str,
        user_id: str,
        _: None = Depends(verify_token),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        content = knowledge.get_content(document_id=document_id, user_id=user_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document content not found or access denied"
            )
        return {'content': content}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# update document metadata
@router.put("/kms/document/{document_id}")
async def update_document_meta(
        modified_by: str,
        document_id: str,
        new_name: str = Body(...),
        new_department_id: str = Body(...),
        new_tags: List[str] = Body(...),
        new_owner: str = Body(...),
        new_category: str = Body(...),
        new_description: str = Body(...),
        new_university: str = Body(...),
        _: None = Depends(verify_token),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        success = knowledge.update_metadata(
            modified_by=modified_by,
            document_id=document_id,
            new_name=new_name.strip(),
            new_department_id=new_department_id.strip(),
            new_tags=new_tags,
            new_owner=new_owner.strip(),
            new_category=new_category.strip(),
            new_description=new_description.strip(),
            new_university=new_university.strip()
        )
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        return {'message': 'update document metadata successfully'}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# update document content
@router.put("/kms/document/{document_id}/content")
async def update_document_content(
        document_id: str,
        modified_by: str = Form(...),
        document: UploadFile = File(...),
        _: None = Depends(verify_token),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        content = await document.read()
        content_io = BytesIO(content)

        success = knowledge.update_content(
            document_id=document_id,
            modified_by=modified_by,
            new_content=content_io
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found or update failed"
            )

        return {'message': 'update document content successfully'}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# delete document
@router.delete("/kms/document/{document_id}")
async def delete_document(
        deleted_by: str,
        document_id: str,
        _: None = Depends(verify_token),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        success = knowledge.delete(deleted_by=deleted_by, document_id=document_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found or deletion failed"
            )

        return {"message": "delete document successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# get all versions
@router.get("/kms/document/{document_id}/versions")
async def get_document_versions(
        user_id: str,
        document_id: str,
        _: None = Depends(verify_token),
        knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        versions = knowledge.get_all_versions(user_id=user_id, document_id=document_id)

        if not versions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No versions found for the given document ID or access denied"
            )

        return {"versions": versions}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# get specific version
@router.get("/kms/document/{document_id}/versions/{version_id}")
async def get_specific_document_version(
    user_id: str,
    document_id: str,
    version_number: str,
    _: None = Depends(verify_token),
    knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        document = knowledge.get_specific_version(user_id=user_id, document_id=document_id, version_number=version_number)

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document version not found or access denied"
            )

        return {'document': document}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/kms/document/{document_id}/versions/{version_id}")
async def restore_document_version(
    document_id: str,
    version_number: str = Form(...),
    restored_by: str = Form(...),
    _: None = Depends(verify_token),
    knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        success = knowledge.restore_version(
            document_id=document_id,
            restored_by=restored_by,
            version_number=version_number
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Failed to restore version. Document or version not found or access denied."
            )

        return {"message": "Version restored successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# share permission
@router.post("/kms/document/permission")
async def share_document_permission(
    shared_by: str = Form(...),
    shared_to: str = Form(...),
    document_id: str = Form(...),
    permissions: List[str] = Form(...),
    _: None = Depends(verify_token),
    knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        success = knowledge.share_permissions(
            shared_by=shared_by,
            shared_to=shared_to,
            document_id=document_id,
            permissions=permissions
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to share permissions. Check if user or document exists or access denied."
            )

        return {"message": f"Permissions shared with user {shared_to} on document {document_id} by {shared_by}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/kms/document/permission")
async def remove_document_permission(
    removed_by: str = Form(...),
    removed_to: str = Form(...),
    document_id: str = Form(...),
    permissions: List[str] = Form(...),
    _: None = Depends(verify_token),
    knowledge: KnowledgeManager = Depends(get_knowledge)
):
    try:
        success = knowledge.remove_permissions(
            removed_by=removed_by,
            removed_to=removed_to,
            document_id=document_id,
            permissions=permissions
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove permissions. Check if user or document exists or access denied."
            )

        return {"message": f"Permissions removed for user {removed_to} on document {document_id} by {removed_by}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Register router
app.include_router(router)
