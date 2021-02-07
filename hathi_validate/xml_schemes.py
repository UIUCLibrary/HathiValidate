import pkgutil
from typing import Optional


def get_scheme(scheme_name: str) -> Optional[bytes]:
    try:
        data = pkgutil.get_data(
            "hathi_validate", "xsd/{}.xsd".format(scheme_name)
        )

        return data
    except FileNotFoundError:
        raise ValueError("Unknown scheme {}".format(scheme_name))
