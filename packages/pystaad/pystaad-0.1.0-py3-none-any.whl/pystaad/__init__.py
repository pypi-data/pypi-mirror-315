from typing import Any
from .tools import deg2node
from win32com.client import GetActiveObject
try:
    Root=GetActiveObject("StaadPro.OpenSTAAD")
except Exception:
    print("You need to run STAAD.Pro to initialize PyStaad.")
    exit("STAAD.Pro must be open to use PyStaad")
class GeometryInterface:
    def GetAllNodes(self) -> Any:
        """Returns all nodes."""
        pass

    def GetNodeCoordinates(self, node_id: int) -> Any:
        """Returns node coordinates."""
        pass
Geometry:GeometryInterface=Root.Geometry
Property=Root.Property
Support=Root.Support
Load=Root.Load
Table=Root.Table
Views=Root.View
Output=Root.Output
Design=Root.Design
Commands=Root.Command




