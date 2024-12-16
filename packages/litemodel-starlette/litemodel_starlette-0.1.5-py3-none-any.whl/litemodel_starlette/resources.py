from databases import Database
from starlette.templating import Jinja2Templates
from litemodel_starlette import settings

database = Database(settings.DATABASE_URL)
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
admin_templates = Jinja2Templates(directory=settings.ADMIN_TEMPLATES_DIR)
model_templates = Jinja2Templates(directory=settings.MODEL_TEMPLATES_DIR)
# static = StaticFiles(directory=settings.STATIC_DIR)
# images = StaticFiles(directory=settings.IMAGE_DIR)