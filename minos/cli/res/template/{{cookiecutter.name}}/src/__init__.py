__author__ = "{{ cookiecutter.author }}"
__email__ = "{{ cookiecutter.email }}"
__version__ = "{{ cookiecutter.version }}"

from .aggregates import (
    {{ cookiecutter.aggregate }},
)
from .cli import (
    main,
)
from .commands import (
    {{ cookiecutter.aggregate }}CommandService,
)
from .queries import (
    {{ cookiecutter.aggregate }}QueryService,
)
