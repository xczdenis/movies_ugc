import uvicorn

from movies_ugc.app import create_app
from movies_ugc.app.event_handlers import register_event_handlers
from movies_ugc.app.exception_handler import register_exception_handlers
from movies_ugc.config.logger import setup_logging
from movies_ugc.config.settings import app_settings

app = create_app(app_settings.dict())

register_event_handlers(app)
register_exception_handlers(app)

if __name__ == "__main__":
    setup_logging()

    uvicorn.run("main:app", host=app_settings.APP_HOST, port=app_settings.APP_PORT)
