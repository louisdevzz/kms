from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from backend.knowledge.knowledge_manager import KnowledgeManager
from backend.api.api_router import KMS_APIRouter
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(kms_app: FastAPI):
    # Startup code
    try:
        knowledge_manager = KnowledgeManager()
        kms_app.state.api_router = KMS_APIRouter(knowledge_manager)
        kms_app.include_router(kms_app.state.api_router.router)
        logger.info("Resources initialized successfully.")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise

    yield  # now running

    logger.info("Cleaning up resources...")
    knowledge_manager.dao.close_connection()  # close connection to db


app = FastAPI(
    title="Knowledge Management System API",
    lifespan=lifespan
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
