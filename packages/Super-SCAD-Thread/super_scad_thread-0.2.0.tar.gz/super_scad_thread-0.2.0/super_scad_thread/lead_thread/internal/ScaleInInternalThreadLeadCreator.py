from typing import List

from super_scad.type.Vector2 import Vector2

from super_scad_thread.enum.ThreadAnatomy import ThreadAnatomy
from super_scad_thread.lead_thread.internal.InternalThreadLeadCreator import InternalThreadLeadCreator


class ScaleInInternalThreadLeadCreator(InternalThreadLeadCreator):
    """
    Creates a lead on a 2D internal thread profile.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 pitch: float,
                 minor_diameter: float,
                 major_diameter: float,
                 start_angle: float = 180.0):
        """
        Object constructor.

        :param pitch: The pitch of the thread.
        :param minor_diameter: The minor diameter of the thread.
        :param major_diameter: The major diameter of the thread.
        :param start_angle: The angle at which the thread starts to appear.
        """

        self.__pitch: float = pitch
        """
        The pitch of the thread.
        """

        self.__minor_diameter: float = minor_diameter
        """
        The minor diameter of the thread. 
        """

        self.__major_diameter: float = major_diameter
        """
        The major diameter of the thread. 
        """

        self.__start_angle: float = start_angle
        """
        The angle at which the thread start to appear. 
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
        index_first_root = None
        index_second_root = None
        prev = None
        for index, point in enumerate(thread_profile):
            if thread_anatomy[index] == ThreadAnatomy.AT_MAJOR and prev != ThreadAnatomy.AT_MAJOR:
                index_first_root = index_second_root
                index_second_root = index
            prev = thread_anatomy[index]
            if point.y > z + self.__pitch:
                break

        for index, point in enumerate(thread_profile):
            if point.y < 0.0:
                thread_profile[index] = Vector2(self.__major_diameter / 2.0, 0.0)
            elif index < index_second_root:
                if angle >= self.__start_angle and index > index_first_root:
                    fraction = (angle - self.__start_angle) / (360.0 - self.__start_angle)
                    d_min = self.__major_diameter - (self.__major_diameter - self.__minor_diameter) * fraction
                    x = max(d_min / 2.0, point.x)
                    y = point.y
                    thread_profile[index] = Vector2(x, y)
                else:
                    x = self.__major_diameter / 2.0
                    y = point.y
                    thread_profile[index] = Vector2(x, y)
            else:
                break

        return thread_profile

# ----------------------------------------------------------------------------------------------------------------------
