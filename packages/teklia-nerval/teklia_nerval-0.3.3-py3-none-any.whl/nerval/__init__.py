import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s/%(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

ALL_ENTITIES = "ALL"
