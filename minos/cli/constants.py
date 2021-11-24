from enum import (
    Enum,
)

TEMPLATES_REPOSITORY_URL = "git@github.com:Clariteia/minos-templates.git"


class TemplateCategory(str, Enum):
    """TODO"""

    MICROSERVICE = "microservice"
    PROJECT = "project"
