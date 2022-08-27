import datetime
import logging
import ssl
from enum import Enum
from typing import List, Any, Dict

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# TODO implement JSON logging format


class ConnectorType(Enum):
    EXTERNAL_IMPORT = "EXTERNAL_IMPORT"  # From remote sources to OpenCTI stix2
    INTERNAL_IMPORT_FILE = (
        "INTERNAL_IMPORT_FILE"  # From OpenCTI file system to OpenCTI stix2
    )
    INTERNAL_ENRICHMENT = "INTERNAL_ENRICHMENT"  # From OpenCTI stix2 to OpenCTI stix2
    INTERNAL_EXPORT_FILE = (
        "INTERNAL_EXPORT_FILE"  # From OpenCTI stix2 to OpenCTI file system
    )
    STREAM = "STREAM"  # Read the stream and do something
    WORKER = "WORKER"


def get_logger(
    name: str, logging_level: str = "INFO", logging_format: str = LOG_FORMAT
) -> Any:
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    c_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(logging_format)
    c_handler.setFormatter(console_formatter)

    logger.addHandler(c_handler)

    return logger


def create_ssl_context() -> ssl.SSLContext:
    """Set strong SSL defaults: require TLSv1.2+

    `ssl` uses bitwise operations to specify context `<enum 'Options'>`
    """

    ssl_context_options: List[int] = [
        ssl.OP_NO_COMPRESSION,
        ssl.OP_NO_TICKET,  # pylint: disable=no-member
        ssl.OP_NO_RENEGOTIATION,  # pylint: disable=no-member
        ssl.OP_SINGLE_DH_USE,
        ssl.OP_SINGLE_ECDH_USE,
    ]
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    ssl_context.options &= ~ssl.OP_ENABLE_MIDDLEBOX_COMPAT  # pylint: disable=no-member
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

    for option in ssl_context_options:
        ssl_context.options |= option

    return ssl_context


def date_now() -> str:
    """get the current date (UTC)
    :return: current datetime for utc
    :rtype: str
    """
    return (
        datetime.datetime.utcnow()
        .replace(microsecond=0, tzinfo=datetime.timezone.utc)
        .isoformat()
    )


def check_max_tlp(tlp: str, max_tlp: str) -> bool:
    """check the allowed TLP levels for a TLP string

    :param tlp: string for TLP level to check
    :type tlp: str
    :param max_tlp: the highest allowed TLP level
    :type max_tlp: str
    :return: TLP level in allowed TLPs
    :rtype: bool
    """

    allowed_tlps: Dict[str, List[str]] = {
        "TLP:RED": ["TLP:WHITE", "TLP:GREEN", "TLP:AMBER", "TLP:RED"],
        "TLP:AMBER": ["TLP:WHITE", "TLP:GREEN", "TLP:AMBER"],
        "TLP:GREEN": ["TLP:WHITE", "TLP:GREEN"],
        "TLP:WHITE": ["TLP:WHITE"],
    }

    return tlp in allowed_tlps[max_tlp]
