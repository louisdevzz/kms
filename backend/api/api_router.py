from backend.utils.config_loader import get_secret_key
from typing import Optional, List
from backend.knowledge.knowledge_manager import KnowledgeManager
from backend.dao.user_module.user import User
from fastapi import HTTPException, Depends, status, APIRouter, Form, UploadFile, File, Body, Query
import logging
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from io import BytesIO
from backend.api.iapi_router import IAPIRouter
from fastapi.responses import StreamingResponse


logger = logging.getLogger(__name__)

# JWT Config
SECRET_KEY = get_secret_key()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()


class KMS_APIRouter(IAPIRouter):
    def __init__(self, knowledge_manager: KnowledgeManager):
        self.router = APIRouter()
        self.knowledge = knowledge_manager
        self._register_routes()

    def _register_routes(self):
        # auth routes
        self.router.post("/kms/auth/signup")(self.sign_up)
        self.router.post("/kms/auth/login")(self.login)
        self.router.get("/kms/auth/me")(self.get_current_user)

        # doc routes
        self.router.post("/kms/document")(self.upload_document)
        self.router.get("/kms/document/ids")(self.get_doc_ids)
        self.router.get('/kms/document/search')(self.search_doc_by_name)

        # specific doc routes
        self.router.get("/kms/document/{document_id}")(self.get_document_meta)
        self.router.get("/kms/document/{document_id}/content")(self.get_document_content)
        self.router.put("/kms/document/{document_id}")(self.update_document_meta)
        self.router.put("/kms/document/{document_id}/content")(self.update_document_content)
        self.router.delete("/kms/document/{document_id}")(self.delete_document)

        # versioning routes
        self.router.get("/kms/document/{document_id}/versions")(self.get_document_versions)
        self.router.get("/kms/document/{document_id}/versions/{version_id}")(self.get_specific_document_version)
        self.router.post("/kms/document/{document_id}/versions/{version_id}")(self.restore_document_version)

        # permission routes
        self.router.post("/kms/document/permission")(self.share_document_permission)
        self.router.delete("/kms/document/permission")(self.remove_document_permission)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def get_user_from_token(self, credentials):
        payload = self.decode_token(credentials.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        current_user = self.knowledge.get_user_by_email(email)
        return current_user

    async def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            token = credentials.credentials
            payload = KMS_APIRouter.decode_token(token)
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # signup
    async def sign_up(
            self,
            email: str = Form(...),
            password: str = Form(...),
            name: str = Form(...),
            department_id: str = Form(...),
            roles: List[str] = Form(...)
    ):
        success = self.knowledge.sign_up(
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
    async def login(
            self,
            email: str = Form(...),
            password: str = Form(...)
    ):
        if not self.knowledge.login(email.strip(), password.strip()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        token = self.create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {
            "message": "login successfully",
            "access_token": token,
        }

    # upload document
    async def upload_document(
            self,
            document: UploadFile = File(...),
            name: Optional[str] = Form(None),
            doc_type: Optional[str] = Form(None),
            department_id: Optional[str] = Form(None),
            tags: Optional[List[str]] = Form([]),
            owner: Optional[str] = Form(None),
            category: Optional[str] = Form(None),
            description: Optional[str] = Form(None),
            university: Optional[str] = Form(None),
            _: None = Depends(verify_token)  # verify token
    ):
        content = await document.read()
        content_io = BytesIO(content)
        try:
            result = self.knowledge.upload(
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
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            user = self.get_user_from_token(credentials)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            return user
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # search doc by name
    async def search_doc_by_name(
        self,
        name: str,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            current_user = self.get_user_from_token(credentials)
            metadata = self.knowledge.get_doc_by_name(
                name=name,
                user_id=current_user.userId
            )
            if not metadata:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found or access denied"
                )
            return metadata
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    # get document metadata
    async def get_document_meta(
        self,
        document_id: str,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            current_user = self.get_user_from_token(credentials)
            metadata = self.knowledge.get_metadata(
                document_id=document_id,
                user_id=current_user.userId
            )
            if not metadata:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found or access denied"
                )
            return metadata
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    # get document content
    async def get_document_content(
            self,
            document_id: str,
            credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            current_user = self.get_user_from_token(credentials)
            content = self.knowledge.get_content(
                document_id=document_id,
                user_id=current_user.userId
            )
            if not content:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document content not found or access denied"
                )

            file_content = content.read()
            content.close()

            return StreamingResponse(
                BytesIO(file_content),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f"attachment; filename={document_id}"
                }
            )

        except PermissionError as pe:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(pe)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    # get all document content
    async def get_doc_ids(
            self,
            credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            current_user = self.get_user_from_token(credentials)
            doc_ids = self.knowledge.get_doc_ids(user_id=current_user.userId)

            if not doc_ids:
                return {"messgae": "Not Found"}
                # raise HTTPException(
                #     status_code=status.HTTP_404_NOT_FOUND,
                #     detail="No accessible documents found"
                # )

            return doc_ids

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve document IDs: {str(e)}"
            )

    # update document metadata
    async def update_document_meta(
            self,
            modified_by: str,
            document_id: str,
            new_name: str = Body(...),
            new_department_id: str = Body(...),
            new_tags: List[str] = Body(...),
            new_owner: str = Body(...),
            new_category: str = Body(...),
            new_description: str = Body(...),
            new_university: str = Body(...),
            _: None = Depends(verify_token)
    ):
        try:
            success = self.knowledge.update_metadata(
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
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found"
                )
            return {'message': 'update document metadata successfully'}
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    # update document content
    async def update_document_content(
            self,
            document_id: str,
            modified_by: str = Form(...),
            document: UploadFile = File(...),
            _: None = Depends(verify_token)
    ):
        try:
            content = await document.read()
            content_io = BytesIO(content)
            success = self.knowledge.update_content(
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
    async def delete_document(
            self,
            document_id: str,
            credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            current_user = self.get_user_from_token(credentials)
            success = self.knowledge.delete(
                deleted_by=current_user.userId,
                document_id=document_id
            )
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
    async def get_document_versions(
            self,
            user_id: str,
            document_id: str,
            _: None = Depends(verify_token)
    ):
        try:
            versions = self.knowledge.get_all_versions(
                user_id=user_id,
                document_id=document_id
            )
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
    async def get_specific_document_version(
            self,
            user_id: str,
            document_id: str,
            version_number: str,
            _: None = Depends(verify_token)
    ):
        try:
            document = self.knowledge.get_specific_version(
                user_id=user_id,
                document_id=document_id,
                version_number=version_number
            )
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

    # restore version
    async def restore_document_version(
            self,
            document_id: str,
            version_number: str = Form(...),
            restored_by: str = Form(...),
            _: None = Depends(verify_token)
    ):
        try:
            success = self.knowledge.restore_version(
                document_id=document_id,
                version_number=version_number,
                restored_by=restored_by
            )
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document version not found or restore failed"
                )
            return {'message': 'Document version restored successfully'}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    # share permission
    async def share_document_permission(
            self,
            shared_to: str = Form(...),
            document_id: str = Form(...),
            permissions: List[str] = Form(...),
            credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            current_user = self.get_user_from_token(credentials)
            success = self.knowledge.share_permissions(
                shared_by=current_user.userId,
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

    # remove version
    async def remove_document_permission(
            self,
            removed_by: str = Form(...),
            removed_to: str = Form(...),
            document_id: str = Form(...),
            permissions: List[str] = Form(...),
            _: None = Depends(verify_token)
    ):
        try:
            success = self.knowledge.remove_permissions(
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
