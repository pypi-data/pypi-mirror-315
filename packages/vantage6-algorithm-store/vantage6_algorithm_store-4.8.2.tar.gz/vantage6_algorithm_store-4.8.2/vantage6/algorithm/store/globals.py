from pathlib import Path

from vantage6.common.globals import APPNAME

#
#   INSTALLATION SETTINGS
#
PACKAGE_FOLDER = Path(__file__).parent.parent.parent.parent

SERVER_MODULE_NAME = APPNAME + "-algorithm-store"

# TODO: this should be done differently
# Which resources should be initialized. These names correspond to the
# file-names in the resource directory
RESOURCES = [
    "version",
    "algorithm",
    "vantage6_server",
    "role",
    "rule",
    "user",
    "policy",
    "review",
]

# Where the resources modules have to be loaded from
RESOURCES_PATH = "vantage6.algorithm.store.resource"
