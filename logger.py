
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configurar_logger():
    diretorio = Path(__file__).resolve().parent / "logs"
    diretorio.mkdir(exist_ok=True)

    logger = logging.getLogger("agente_linux")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        arquivo = RotatingFileHandler(
            diretorio / "agente.log",
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )

        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        arquivo.setFormatter(formato)
        logger.addHandler(arquivo)

    return logger


logger = configurar_logger()
