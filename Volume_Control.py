# volume_control.py - Handles Windows system volume control

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

class VolumeController:
    def __init__(self):
        # Get default speakers
        devices = AudioUtilities.GetSpeakers()

        # Activate volume interface
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )

        # Cast to usable volume object
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        self.prev_volume = 0.0  # for smoothing
        print("✓ Volume controller initialized!")

    def map_distance_to_volume(self, distance, min_dist=30, max_dist=200):
        """
        Convert finger distance to volume level (0.0 - 1.0)
        """
        vol = (distance - min_dist) / (max_dist - min_dist)
        return np.clip(vol, 0.0, 1.0)

    def set_volume(self, distance):
        """
        Smooth and apply volume to OS
        """
        vol_level = self.map_distance_to_volume(distance)

        # Smooth volume changes
        vol_level = 0.8 * self.prev_volume + 0.2 * vol_level
        self.prev_volume = vol_level

        # Apply to Windows OS
        self.volume.SetMasterVolumeLevelScalar(vol_level, None)

        return int(vol_level * 100)
