import logging, structlog
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from core.settings import Settings

class Logger:
    @staticmethod
    def get_logger(name: str = __name__):
        return structlog.get_logger(name)
    
    @staticmethod
    def setup_logger() -> None:
        file_handler = Logger._file_handler()
        console_handler = Logger._conlose_handler()

        logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            wrapper_class=structlog.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    
    @staticmethod
    def _file_handler() -> RotatingFileHandler:
        file_handler = RotatingFileHandler(
            Settings.PATH_LOGS / "main.log",
            maxBytes=1024*1024,
            backupCount=5,
        )

        file_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=structlog.processors.JSONRenderer(),
            )
        )
        file_handler.setLevel(logging.INFO)
        return file_handler
    
    @staticmethod
    def _conlose_handler() -> StreamHandler:
        console_handler = StreamHandler()
        console_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=structlog.dev.ConsoleRenderer(),
            )
        )
        console_handler.setLevel(logging.INFO)
        return console_handler
    
Logger.setup_logger()