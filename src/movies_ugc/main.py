import uvicorn
from app import create_app
from app.event_handlers import register_event_handlers
from app.exception_handler import register_exception_handlers
from config.logger import setup_logging
from config.settings import app_settings

app = create_app(app_settings.dict())

register_event_handlers(app)
register_exception_handlers(app)

if __name__ == "__main__":
    setup_logging()

    uvicorn.run("main:app", host=app_settings.APP_HOST, port=app_settings.APP_PORT)
