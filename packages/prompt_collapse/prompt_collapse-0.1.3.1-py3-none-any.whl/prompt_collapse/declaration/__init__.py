from .declaration import Declaration
from .decrement import DecrementDeclaration
from .emit import EmitDeclaration
from .emit_if_none import EmitIfNoneDeclaration
from .increment import IncrementDeclaration
from .overwrite import OverwriteDeclaration
from .registry import DECLARATION_REGISTRY

DECLARATION_REGISTRY.register("emit", EmitDeclaration)
DECLARATION_REGISTRY.register("emit_if_none", EmitIfNoneDeclaration)
DECLARATION_REGISTRY.register("decrement", DecrementDeclaration)
DECLARATION_REGISTRY.register("increment", IncrementDeclaration)
DECLARATION_REGISTRY.register("overwrite", OverwriteDeclaration)

DECLARATION_REGISTRY.register("set", EmitDeclaration)
DECLARATION_REGISTRY.register("try_set", EmitIfNoneDeclaration)
DECLARATION_REGISTRY.register("set_if_none", EmitIfNoneDeclaration)
DECLARATION_REGISTRY.register("dec", DecrementDeclaration)
DECLARATION_REGISTRY.register("inc", IncrementDeclaration)
DECLARATION_REGISTRY.register("update", OverwriteDeclaration)

__all__ = [
    "Declaration",
    "EmitDeclaration",
    "EmitIfNoneDeclaration",
    "DecrementDeclaration",
    "IncrementDeclaration",
    "OverwriteDeclaration",
    "DECLARATION_REGISTRY",
]
