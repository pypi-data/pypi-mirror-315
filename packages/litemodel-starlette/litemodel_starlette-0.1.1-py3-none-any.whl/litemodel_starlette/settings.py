from pathlib import Path
from databases import DatabaseURL
from starlette.config import Config

config = Config(".env")

# Directories
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
ADMIN_TEMPLATES_DIR = TEMPLATES_DIR / "admin"
MODEL_TEMPLATES_DIR = TEMPLATES_DIR / "model"
STATIC_DIR = BASE_DIR / "static"
IMAGE_DIR = STATIC_DIR / "img"


# Database
DATABASE_PATH = config("DATABASE_PATH", default=BASE_DIR / "sqlite.db")
DATABASE_URL = config(
    "DATABASE_URL", cast=DatabaseURL, default=f"sqlite:///{DATABASE_PATH}"
)

# Debug
DEBUG = config("DEBUG", cast=bool, default=False)

# Views
CREATE_VIEW_URL_ENDING = "new"
EDIT_VIEW_URL_ENDING = "edit"
DETAIL_VIEW_URL_ENDING = ""
DELETE_VIEW_URL_ENDING = "delete"
LIST_VIEW_URL_ENDING = ""
MODEL_VIEW_ITEMS_PER_PAGE = 20