import math
from typing import Any, Dict, List, Tuple

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.type.Vector3 import Vector3

from super_scad_thread.enum.ThreadDirection import ThreadDirection
from super_scad_thread.lead_thread.internal.InternalThreadLeadCreator import InternalThreadLeadCreator
from super_scad_thread.Thread import Thread
from super_scad_thread.ThreadProfileCreator import ThreadProfileCreator


class InternalThread(Thread):
    """
    SuperSCAD widget for creating internal threads.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 length: float,
                 thread_profile_creator: ThreadProfileCreator,
                 top_thread_lead_creator: InternalThreadLeadCreator,
                 bottom_thread_lead_creator: InternalThreadLeadCreator,
                 direction: ThreadDirection,
                 outer_radius: float | None = None,
                 outer_diameter: float | None = None,
                 center: bool = False,
                 convexity: int = 2):
        """
        Object contructor.

        :param length: The length of the thread.
        :param thread_profile_creator: The thread profile creator.
        :param top_thread_lead_creator: The object for creating a lead on the top of the thread.
        :param bottom_thread_lead_creator: The object for creating a lead on the top of the thread.
        :param direction: The direction of the thread.
        :param outer_radius: The outer radius of the thread.
        :param outer_diameter: The outer diameter of the thread.
        :param center: Whether to center the thread along the z-axis.
        :param convexity: The convexity of the thread, defaults to 2. Normally 2 is enough, however, in some cases a
                          higher value is required.
        """
        Thread.__init__(self,
                        length=length,
                        thread_profile_creator=thread_profile_creator,
                        top_thread_lead_creator=top_thread_lead_creator,
                        bottom_thread_lead_creator=bottom_thread_lead_creator,
                        direction=direction,
                        center=center,
                        convexity=convexity)

        self._outer_radius: float = outer_radius
        """
        The outer radius of the thread.
        """

        self._outer_diameter: float = outer_diameter
        """
        The outer diameter of the thread.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.

        :param args: The arguments supplied to the constructor.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'outer_radius'}, {'outer_diameter'})
        validator.validate_required({'outer_radius', 'outer_diameter'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the internal radius of the external thread.
        """
        if self._outer_radius is not None:
            radius = self._outer_radius
        elif self._outer_diameter is not None:
            radius = 0.5 * self._outer_diameter
        else:
            radius = 0.0

        if radius <= 0.0:
            radius = 0.5 * self.thread_profile_creator.major_diameter

        return radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_diameter(self) -> float:
        """
        Returns the internal diameter of the external thread.
        """
        if self._outer_diameter is not None:
            diameter = self._outer_diameter
        elif self._outer_radius is not None:
            diameter = 2.0 * self._outer_radius
        else:
            diameter = 0.0

        if diameter <= 0.0:
            diameter = self.thread_profile_creator.major_diameter

        return diameter

    # ------------------------------------------------------------------------------------------------------------------
    def __create_faces_thread(self,
                              faces: List[List[Vector3] | Tuple[Vector3, ...]],
                              thread_3d: List[List[Vector3]]) -> None:
        """
        Creates the faces for the thread profile.
        
        :param faces: The list of faces.
        :param thread_3d: The thread profile in 3D.
        """
        edges = len(thread_3d)
        number_of_points_per_pitch = self.thread_profile_creator.number_of_points_per_pitch

        face = []
        for index in range(number_of_points_per_pitch + 1):
            face.append(thread_3d[0][index])
        faces.append(face)

        # Faces between the consecutive edges.
        for edge in range(1, edges):
            for key in range(1, len(thread_3d[0])):
                faces.append((thread_3d[edge][key - 1],
                              thread_3d[edge][key],
                              thread_3d[edge - 1][key],
                              thread_3d[edge - 1][key - 1]))

        # Faces between the last and first edges.
        for key in range(1, len(thread_3d[0]) - number_of_points_per_pitch - 1):
            faces.append((thread_3d[0][key + number_of_points_per_pitch - 1],
                          thread_3d[0][key + number_of_points_per_pitch],
                          thread_3d[edges - 1][key],
                          thread_3d[edges - 1][key - 1]))

    # ------------------------------------------------------------------------------------------------------------------
    def __create_faces_outer(self,
                             faces: List[List[Vector3] | Tuple[Vector3, ...]],
                             thread_3d: List[List[Vector3]]) -> None:
        """
        Creates faces for the top, bottom, and outer faces.

        :param faces: The list of faces.
        :param thread_3d: The thread profile in 3D.
        """
        edges = len(thread_3d)
        outer_radius = self.outer_radius / math.cos(math.pi / edges)
        number_of_points_per_pitch = self.thread_profile_creator.number_of_points_per_pitch

        bottom_points = []
        top_points = []
        for edge in range(0, edges):
            angle = edge * 360.0 / edges
            x = outer_radius * math.cos(math.radians(angle))
            y = outer_radius * math.sin(math.radians(angle))
            bottom_points.append(Vector3(x, y, 0.0))
            top_points.append(Vector3(x, y, self.length))

        # Add bottom face.
        for edge in range(1, edges):
            faces.append((bottom_points[edge - 1],
                          bottom_points[edge],
                          thread_3d[edge][0],
                          thread_3d[edge - 1][0]))
        faces.append((bottom_points[edges - 1],
                      bottom_points[0],
                      thread_3d[0][0],
                      thread_3d[edges - 1][0]))

        # ???
        faces.append((bottom_points[0],
                      thread_3d[0][number_of_points_per_pitch],
                      thread_3d[edges - 1][0]))

        # Add top face.
        for edge in range(1, edges):
            faces.append((thread_3d[edge - 1][len(thread_3d[edge - 1]) - 1],
                          thread_3d[edge][len(thread_3d[edge]) - 1],
                          top_points[edge],
                          top_points[edge - 1]))
        faces.append((thread_3d[edges - 1][len(thread_3d[edges - 1]) - 1],
                      thread_3d[0][len(thread_3d[0]) - 1],
                      top_points[0],
                      top_points[edges - 1]))

        # Add outer faces.
        for edge in range(1, edges):
            faces.append((top_points[edge - 1],
                          top_points[edge],
                          bottom_points[edge],
                          bottom_points[edge - 1]))
        faces.append((top_points[edges - 1],
                      top_points[0],
                      bottom_points[0],
                      bottom_points[edges - 1]))

    # ------------------------------------------------------------------------------------------------------------------
    def _create_faces(self, thread_3d: List[List[Vector3]]) -> List[List[Vector3] | Tuple[Vector3, ...]]:
        """
        Creates faces given a thread profile in 3D.

        :param thread_3d: The thread profile in 3D.
        """
        faces: List[List[Vector3] | Tuple[Vector3, ...]] = []

        self.__create_faces_thread(faces, thread_3d)
        self.__create_faces_outer(faces, thread_3d)

        return faces

# ----------------------------------------------------------------------------------------------------------------------
