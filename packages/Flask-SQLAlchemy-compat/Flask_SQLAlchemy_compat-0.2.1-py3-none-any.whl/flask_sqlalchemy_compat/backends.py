# -*- coding: UTF-8 -*-
"""
Backends
========
@ Flask SQLAlchemy Compat

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The backends of the `flask_sqlalchemy_compat` package. These backends are modules
conditionally loaded. In other words, if the model is intalled, will load the module.
Otherwise, load a placeholder of the corresponding module.

The backends include:
1. `fsa`: `flask_sqlalchemy`
    (licensed by BSD 3-Clause License, Copyright 2010 Pallets)
2. `fsa_lite`: `flask_sqlalchemy_lite`
    (licensed by MIT License, Copyright 2024 Pallets)
"""

import sys
import importlib
import importlib.util
from types import ModuleType

from typing import TYPE_CHECKING, cast
from typing import Union, Optional, Generic, TypeVar

try:
    from typing import Sequence
except ImportError:
    from collections.abc import Sequence

from typing_extensions import Literal, TypeGuard


M1 = TypeVar("M1", bound=ModuleType)
M2 = TypeVar("M2", bound=ModuleType)

__all__ = (
    "fsa",
    "fsa_lite",
    "ModulePlaceholder",
    "conditional_import",
    "is_module_invalid",
    "BackendProxy",
    "proxy",
)


class ModulePlaceholder(ModuleType):
    """The placeholder module.

    This module is used as a placeholder of a module that cannot be found.
    It can still provide `__name__` property. However, it does not contain
    the `__spec__` property.
    """

    __file__: Optional[str] = None
    """The `file` attribute of this placeholder module is empty."""

    removed_kw = set(("__path__",))

    protected_kw = set(
        (
            "__repr__",
            "__str__",
            "__name__",
            "__qualname__",
            "__annotations__",
            "__spec__",
            "__origin__",
            "__weakref__",
            "__weakrefoffset__",
            "force_load",
            "__class__",
            "__dict__",
            "abstract",
        )
    )

    def __init__(self, name: str, doc: Optional[str] = None) -> None:
        """Initialization.
        Arguments:
            name: The module name. It will be passed to ModuleType.
        """
        name = str(name)
        if doc is None:
            doc = (
                "{0}\n"
                "This module is used as a placeholder, because the required "
                "module {0} is not found.".format(name)
            )
        else:
            doc = str(doc)
        super().__init__(name=name, doc=doc)

    def __repr__(self) -> str:
        """This repr is used for showing that this is a placeholder."""
        return "<ModulePlaceholder {name}>".format(
            name=object.__getattribute__(self, "__name__")
        )

    @property
    def __all__(self) -> Sequence[str]:
        """The attribute list of this placeholder module is empty."""
        return tuple()

    def force_load(self) -> None:
        """Nothing happens. Because this is a placeholder."""
        return

    def __getattribute__(self, attr: str):
        """Add more error information to the attribute error."""
        if attr in ModulePlaceholder.removed_kw:
            raise AttributeError(
                "{0} does not offer the attribute {1}".format("ModulePlaceholder", attr)
            )
        if attr in ModulePlaceholder.protected_kw:
            try:
                return object.__getattribute__(self, attr)
            except AttributeError:
                pass
        try:
            return super().__getattribute__(attr)
        except AttributeError as err:
            name = object.__getattribute__(self, "__name__")
            raise ImportError(
                'utils: Fail to fetch the attribute "{0}" from module "{1}" '
                "because this optional module is not successfully loaded. At least "
                "one dependency of this module is not installed.".format(attr, name)
            ) from err


def conditional_import(name: str) -> ModuleType:
    """Import the module if it exists. Otherwise, return a `ModulePlaceholder`."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.find_spec(name)
    if spec is None:
        return ModulePlaceholder(name)
    if spec.loader is None:
        return ModulePlaceholder(name)
    # module = importlib.import_module(name)
    # return module
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def is_module_invalid(module: ModuleType) -> TypeGuard[ModulePlaceholder]:
    """Check whether the given module is invalid or not.

    An invalid module does not provide any functionalities but only serves as a
    placeholder.
    """
    return isinstance(module, ModulePlaceholder)


# Import sub-modules
if TYPE_CHECKING:
    import flask_sqlalchemy as fsa
    import flask_sqlalchemy_lite as fsa_lite
else:
    # Create conditional-loaded modules.
    if sys.version_info < (3, 8):
        # Attempt to import the Python 3.7 version.
        fsa = conditional_import("flask_sqlalchemy_py37")
        if is_module_invalid(fsa):
            fsa = conditional_import("flask_sqlalchemy")
    else:
        fsa = conditional_import("flask_sqlalchemy")
    fsa_lite = conditional_import("flask_sqlalchemy_lite")


class BackendProxy(Generic[M1, M2]):
    """A proxy class that is used for maintaining the dynamically loaded modules.

    The properties of this module are editable, thus allowing the modules to be
    dynamically changed if necessary.
    """

    def __init__(self, fsa: M1, fsa_lite: M2) -> None:
        """Initialization."""
        self.__fsa: M1 = fsa
        self.__fsa_prototype: M1 = self.__fsa
        self.__fsa_lite: M2 = fsa_lite
        self.__fsa_lite_prototype: M2 = self.__fsa_lite

    @property
    def fsa(self) -> M1:
        """A reference to `flask_sqlalchemy`.

        This value can be set by `True`, `False`, or `None`.
        If using `True`, will attempt to retrieve the module.
        If using `False` or `None`, will make the module replaced by the placeholder.
        """
        return self.__fsa

    @fsa.setter
    def fsa(self, value: Union[M1, Literal[True, False], None]) -> None:
        """A reference to `flask_sqlalchemy`. (Setter)"""
        if value is False or value is None:
            if is_module_invalid(self.__fsa_lite):
                # This is the only installed module. Should not disable it.
                return
            self.__fsa = cast(M1, ModulePlaceholder(fsa.__name__))
        elif value is True:
            self.__fsa = self.__fsa_prototype
        else:
            if is_module_invalid(self.__fsa_lite):
                # This is the only installed module. Should not disable it.
                return
            self.__fsa = value

    @property
    def fsa_lite(self) -> M2:
        """A reference to `flask_sqlalchemy_lite`.

        This value can be set by `True`, `False`, or `None`.
        If using `True`, will attempt to retrieve the module.
        If using `False` or `None`, will make the module replaced by the placeholder.
        """
        return self.__fsa_lite

    @fsa_lite.setter
    def fsa_lite(self, value: Union[M2, Literal[True, False], None]) -> None:
        """A reference to `flask_sqlalchemy_lite`. (Setter)"""
        if value is False or value is None:
            if is_module_invalid(self.__fsa):
                # This is the only installed module. Should not disable it.
                return
            self.__fsa_lite = cast(M2, ModulePlaceholder(fsa_lite.__name__))
        elif value is True:
            self.__fsa_lite = self.__fsa_lite_prototype
        else:
            if is_module_invalid(self.__fsa):
                # This is the only installed module. Should not disable it.
                return
            self.__fsa_lite = value


proxy = BackendProxy(fsa, fsa_lite)
"""The proxy of internally used modules. For the testing purposes, its properties
can by dynamically changed by `None`, `True`, or `False` to turn on or turn off the
modules. Changing the properties of this instance will take a global effect to all
functionalities actually loading the extensions. For example,
`flask_sa_api.as_flask_sqlalchemy(...)` will not be able to use Flask SQLAlchemy if
the property `fsa` is deliberately configured by `False` or `None`."""
