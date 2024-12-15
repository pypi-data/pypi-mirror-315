from typing import List

from super_scad.type.Vector2 import Vector2

from super_scad_thread.enum.ThreadAnatomy import ThreadAnatomy
from super_scad_thread.lead_thread.external.ExternalThreadLeadCreator import ExternalThreadLeadCreator


class NoneExternalThreadLeadCreator(ExternalThreadLeadCreator):
    """
    Creates no lead on a 2D external thread profile.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, pitch: float, minor_diameter: float):
        """
        Object constructor.

        :param pitch: The pitch of the thread.
        :param minor_diameter: The minor diameter of the thread.
        """

        self.__pitch: float = pitch
        """
        The pitch of the thread.
        """

        self.__minor_diameter: float = minor_diameter
        """
        The minor diameter of the thread. 
        """

    # ------------------------------------------------------------------------------------------------------------------
    def create_lead(self,
                    thread_profile: List[Vector2],
                    thread_anatomy: List[ThreadAnatomy],
                    z: float,
                    angle: float) -> List[Vector2]:
        """
        Creates a lead on a 2D thread profile.

        :param thread_profile: The thread profile in 2D.
        :param thread_anatomy: The location of a points on the thread profile.
        :param z: The current translation in z-axis direction.
        :param angle: The angle of the current rotation.

        It is guaranteed that 0.0 <= z < pitch.
        It is guaranteed that 0.0 <= angle < 360.0.
        """
        for index, point in enumerate(thread_profile):
            if point.y < 0.0:
                thread_profile[index] = Vector2(self.__minor_diameter / 2.0, 0.0)
            else:
                break

        return thread_profile

# ----------------------------------------------------------------------------------------------------------------------
