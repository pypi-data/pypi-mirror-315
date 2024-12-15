import math
from typing import Any, Dict, List, Tuple

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.type import Vector3

from super_scad_thread.enum.ThreadDirection import ThreadDirection
from super_scad_thread.lead_thread.external.ExternalThreadLeadCreator import ExternalThreadLeadCreator
from super_scad_thread.Thread import Thread
from super_scad_thread.ThreadProfileCreator import ThreadProfileCreator


class ExternalThread(Thread):
    """
    SuperSCAD widget for creating external threads.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 length: float,
                 thread_profile_creator: ThreadProfileCreator,
                 top_thread_lead_creator: ExternalThreadLeadCreator,
                 bottom_thread_lead_creator: ExternalThreadLeadCreator,
                 direction: ThreadDirection,
                 inner_radius: float | None = None,
                 inner_diameter: float | None = None,
                 center: bool = False,
                 convexity: int = 2):
        """
        Object contructor.

        :param length: The length of the thread.
        :param thread_profile_creator: The thread profile creator.
        :param top_thread_lead_creator: The object for creating a lead on the top of the thread.
        :param bottom_thread_lead_creator: The object for creating a lead on the top of the thread.
        :param direction: The direction of the thread.
        :param inner_radius: For a hollow external thread, the outer radius of the thread.
        :param inner_diameter: For a hollow external thread, the outer diameter of the thread.
        :param center: Whether to center the thread along the z-axis.
        :param convexity: The convexity of the thread. Normally 2 is enough, however, in some cases, a higher value is
                          required.
        """
        Thread.__init__(self,
                        length=length,
                        thread_profile_creator=thread_profile_creator,
                        top_thread_lead_creator=top_thread_lead_creator,
                        bottom_thread_lead_creator=bottom_thread_lead_creator,
                        direction=direction,
                        center=center,
                        convexity=convexity)

        self._inner_radius: float | None = inner_radius
        """
        For a hollow external thread, the outer radius of the thread.
        """

        self._inner_diameter: float | None = inner_diameter
        """
        For a hollow external thread, the outer diameter of the thread.
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
        validator.validate_exclusive({'inner_radius'}, {'inner_diameter'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float | None:
        """
        Returns the internal radius of the external thread. 
        """
        if self._inner_radius is not None:
            return self._inner_radius

        if self._inner_diameter is not None:
            return 0.5 * self._inner_diameter

        return None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_diameter(self) -> float | None:
        """
        Returns the internal diameter of the external thread. 
        """
        if self._inner_diameter is not None:
            return self._inner_diameter

        if self._inner_radius is not None:
            return 2.0 * self._inner_radius

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def __create_faces_end_solid(self,
                                 faces: List[List[Vector3] | Tuple[Vector3, ...]],
                                 thread_3d: List[List[Vector3]]) -> None:
        """
        Creates faces for the top and bottom ends of the thread for a solid external thread.

        :param faces: The list of faces.
        :param thread_3d: The thread profile in 3D.
        """
        edges = len(thread_3d)
        number_of_points_per_pitch = self.thread_profile_creator.number_of_points_per_pitch

        # Add bottom face.
        bottom_face = []
        for edge in range(0, edges):
            bottom_face.append(thread_3d[edge][0])
        bottom_face.append(thread_3d[0][number_of_points_per_pitch])
        faces.append(bottom_face)

        # Add top face.
        top_face = []
        for index in range(edges - 1, 0, -1):
            top_face.append(thread_3d[index][len(thread_3d[index]) - 1])
        top_face.append(thread_3d[0][len(thread_3d[0]) - 1])
        faces.append(top_face)

    # ------------------------------------------------------------------------------------------------------------------
    def __create_faces_ends_hollow(self,
                                   faces: List[List[Vector3] | Tuple[Vector3, ...]],
                                   thread_3d: List[List[Vector3]]) -> None:
        """
        Creates faces for the top and bottom ends of the thread for a hollow external thread.

        :param faces: The list of faces.
        :param thread_3d: The thread profile in 3D.
        """
        edges = len(thread_3d)
        inner_radius = self.inner_radius

        bottom_points = []
        top_points = []
        for edge in range(0, edges):
            angle = edge * 360.0 / edges
            x = inner_radius * math.cos(math.radians(angle))
            y = inner_radius * math.sin(math.radians(angle))
            bottom_points.append(Vector3(x, y, 0.0))
            top_points.append(Vector3(x, y, self.length))

        # Add bottom face.
        for edge in range(1, edges):
            faces.append((thread_3d[edge - 1][0],
                          thread_3d[edge][0],
                          bottom_points[edge],
                          bottom_points[edge - 1]))
        faces.append((thread_3d[edges - 1][0],
                      thread_3d[0][0],
                      bottom_points[0],
                      bottom_points[edges - 1]))

        # Add top face.
        for edge in range(1, edges):
            faces.append((top_points[edge - 1],
                          top_points[edge],
                          thread_3d[edge][len(thread_3d[edge]) - 1],
                          thread_3d[edge - 1][len(thread_3d[edge - 1]) - 1]))
        faces.append((top_points[edges - 1],
                      top_points[0],
                      thread_3d[0][len(thread_3d[0]) - 1],
                      thread_3d[edges - 1][len(thread_3d[edges - 1]) - 1]))

        # Add inner faces.
        for edge in range(1, edges):
            faces.append((bottom_points[edge - 1],
                          bottom_points[edge],
                          top_points[edge],
                          top_points[edge - 1]))
        faces.append((bottom_points[edges - 1],
                      bottom_points[0],
                      top_points[0],
                      top_points[edges - 1]))

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

        # Faces between the consecutive edges.
        for edge in range(1, edges):
            for key in range(1, len(thread_3d[0])):
                faces.append((thread_3d[edge - 1][key - 1],
                              thread_3d[edge - 1][key],
                              thread_3d[edge][key],
                              thread_3d[edge][key - 1]))

        # Faces between the last and first edges.
        for key in range(1, len(thread_3d[0]) - number_of_points_per_pitch - 1):
            faces.append((thread_3d[edges - 1][key - 1],
                          thread_3d[edges - 1][key],
                          thread_3d[0][key + number_of_points_per_pitch],
                          thread_3d[0][key + number_of_points_per_pitch - 1]))

    # ------------------------------------------------------------------------------------------------------------------
    def _create_faces(self, thread_3d: List[List[Vector3]]) -> List[List[Vector3] | Tuple[Vector3, ...]]:
        """
        Creates faces given a thread profile in 3D.

        :param thread_3d: The thread profile in 3D.
        """
        faces: List[List[Vector3] | Tuple[Vector3, ...]] = []

        self.__create_faces_thread(faces, thread_3d)
        if self.inner_radius is None:
            self.__create_faces_end_solid(faces, thread_3d)
        else:
            self.__create_faces_ends_hollow(faces, thread_3d)

        return faces

# ----------------------------------------------------------------------------------------------------------------------
