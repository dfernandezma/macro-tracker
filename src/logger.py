import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "app.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="[%(asctime)s] | %(levelname)-8s | %(name)s | %(filename)s:%(funcName)s:%(lineno)d | PID:%(process)d | THREAD:%(threadName)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("macro_tracker")
