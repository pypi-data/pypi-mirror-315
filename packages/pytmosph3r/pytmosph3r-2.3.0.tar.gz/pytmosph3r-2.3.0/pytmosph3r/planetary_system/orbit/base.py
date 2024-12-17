from abc import ABC, abstractmethod

import numpy as np

from pytmosph3r.log import Logger


class Orbit(ABC, Logger):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    @abstractmethod
    def r(self, true_anomaly: float = 0) -> float:
        """
        Returns the distance between the star and the planet in `m`.

        Args:
            true_anomaly (): True anomaly in radian.

        """
        raise NotImplementedError

    @abstractmethod
    def star_coordinates_projected(self, phase):
        """Returns the coordinates in the reference frame of the transmittance (as seen from the observer).
        Only used in transmission, lightcurve.

        Should return (rayon, angle) (polar coordinates)
        """
        raise NotImplementedError

    @abstractmethod
    def obs_long_to_phase(self, longitude):
        raise NotImplementedError

    @abstractmethod
    def phase_to_obs_long(self, phase):
        raise NotImplementedError

    @abstractmethod
    def phase_from_observer(self, obs_loc=(0, np.pi)):
        raise NotImplementedError

    @abstractmethod
    def observer_from_phase(self, phase=0):
        raise NotImplementedError

    @property
    def is_tidal_locked(self) -> bool:
        return False
