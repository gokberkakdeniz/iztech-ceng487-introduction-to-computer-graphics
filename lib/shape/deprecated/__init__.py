# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from .shape import DeprecatedShape
from .object3d import Object3d
from .box import DeprecatedBox
from .cylinder import DeprecatedCylinder
from .sphere import DeprecatedSphere
from .torus import DeprecatedTorus

__all__ = [DeprecatedShape, Object3d, DeprecatedBox,
           DeprecatedTorus, DeprecatedCylinder, DeprecatedSphere]
