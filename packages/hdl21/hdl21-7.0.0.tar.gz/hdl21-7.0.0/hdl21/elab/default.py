""" 
# Elaboration Passes
"""

from enum import Enum
from typing import List

# Import all the defined passes
from .passes import (
    InstBundleElabPass,
    Orphanage,
    ConnTypes,
    BundleFlattener,
    ResolvePortRefs,
    ArrayFlattener,
    SliceResolver,
    MarkModules,
)


class ElabPass(Enum):
    """
    # Enumerated ElabPass Passes

    Each has a `value` attribute which is an `ElabPass` class,
    and a `name` attribute which is a (Python-enum-style) capitalized name.

    Typical usage involves arranging several `ElabPass` in a list
    to be performed in-order.
    The `default` class-method produces the default such list.
    """

    ORPHANAGE = Orphanage
    INSTANCE_BUNDLES = InstBundleElabPass
    RESOLVE_PORT_REFS = ResolvePortRefs
    CONN_TYPES = ConnTypes
    FLATTEN_BUNDLES = BundleFlattener
    FLATTEN_ARRAYS = ArrayFlattener
    RESOLVE_SLICES = SliceResolver
    MARK_MODULES = MarkModules

    @classmethod
    def default(cls) -> List["ElabPass"]:
        """Return the default ordered ElabPass Passes."""
        # Returns each in definition order, then a final few tests.
        return list(ElabPass)[:-1] + [
            ElabPass.CONN_TYPES,
            ElabPass.ORPHANAGE,
            ElabPass.MARK_MODULES,
        ]

    @property
    def elaborate(self):
        return self.value.elaborate
