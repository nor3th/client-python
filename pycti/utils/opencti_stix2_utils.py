import uuid
from stix2 import (
    ObjectPath,
    EqualityComparisonExpression,
    ObservationExpression,
    CustomObservable,
    properties,
)

PATTERN_MAPPING = {
    "Autonomous-System": ["number"],
    "Directory": ["path"],
    "Domain-Name": ["value"],
    "Email-Addr": ["value"],
    "File_md5": ["hashes", "MD5"],
    "File_sha1": ["hashes", "SHA-1"],
    "File_sha256": ["hashes", "SHA-256"],
    "File_sha512": ["hashes", "SHA-512"],
    "Email-Message_Body": ["body"],
    "Email-Message_Subject": ["subject"],
    "Email-Mime-Part-Type": ["body"],
    "IPv4-Addr": ["value"],
    "IPv6-Addr": ["value"],
    "Mac-Addr": ["value"],
    "Mutex": ["name"],
    "Network-Traffic": ["dst_port"],
    "Process": ["pid"],
    "Software": ["name"],
    "Url": ["value"],
    "User-Account": ["acount_login"],
    "Windows-Registry-Key": ["key"],
    "Windows-Registry-Value-Type": ["name"],
}


class OpenCTIStix2Utils:
    @staticmethod
    def create_stix_pattern(observable_type, observable_value):
        if observable_type in PATTERN_MAPPING:
            lhs = ObjectPath(
                observable_type.lower()
                if "_" not in observable_type
                else observable_type.split("_")[0].lower(),
                PATTERN_MAPPING[observable_type],
            )
            ece = ObservationExpression(
                EqualityComparisonExpression(lhs, observable_value)
            )
            return str(ece)
        else:
            return None

    """Generate random stix id
    This id will be ignored by opencti
    :param stix_type: the stix type
    """

    @staticmethod
    def generate_random_stix_id(stix_type):
        new_uuid = str(uuid.uuid4())
        return stix_type + "--" + new_uuid.replace(new_uuid[:8], "00000000")


@CustomObservable(
    "x-opencti-simple-observable",
    [
        ("key", properties.StringProperty(required=True)),
        ("value", properties.StringProperty(required=True)),
        ("description", properties.StringProperty()),
    ],
)
class SimpleObservable:
    pass
