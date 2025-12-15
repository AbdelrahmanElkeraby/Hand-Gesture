# # volume_control.py - Handles Windows system volume control

# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# import numpy as np

# class VolumeController:
#     def __init__(self):
#         # Get default speakers
#         devices = AudioUtilities.GetSpeakers()

#         # Activate volume interface
#         interface = devices.Activate(
#             IAudioEndpointVolume._iid_, CLSCTX_ALL, None
#         )

#         # Cast to usable volume object
#         self.volume = cast(interface, POINTER(IAudioEndpointVolume))

#         self.prev_volume = 0.0  # for smoothing
#         print("✓ Volume controller initialized!")

#     def map_distance_to_volume(self, distance, min_dist=30, max_dist=200):
#         """
#         Convert finger distance to volume level (0.0 - 1.0)
#         """
#         vol = (distance - min_dist) / (max_dist - min_dist)
#         return np.clip(vol, 0.0, 1.0)

#     def set_volume(self, distance):
#         """
#         Smooth and apply volume to OS
#         """
#         vol_level = self.map_distance_to_volume(distance)

#         # Smooth volume changes
#         vol_level = 0.8 * self.prev_volume + 0.2 * vol_level
#         self.prev_volume = vol_level

#         # Apply to Windows OS
#         self.volume.SetMasterVolumeLevelScalar(vol_level, None)

#         return int(vol_level * 100)





# from pycaw.pycaw import AudioUtilities
# import numpy as np

# class VolumeController:
#     def __init__(self):
#         device = AudioUtilities.GetSpeakers()

#         # Correct way for your pycaw version
#         self.volume = device.EndpointVolume

#         self.min_vol, self.max_vol, _ = self.volume.GetVolumeRange()

#     def set_volume_by_percent(self, percent):
#         percent = np.clip(percent, 0, 100)
#         vol = np.interp(percent, [0, 100], [self.min_vol, self.max_vol])
#         self.volume.SetMasterVolumeLevel(vol, None)

#     def volume_up(self, step=5):
#         current = self.volume.GetMasterVolumeLevel()
#         self.volume.SetMasterVolumeLevel(
#             min(current + step, self.max_vol), None
#         )

#     def volume_down(self, step=5):
#         current = self.volume.GetMasterVolumeLevel()
#         self.volume.SetMasterVolumeLevel(
#             max(current - step, self.min_vol), None
#         )

# def set_volume(self, percent):
#     self.set_volume_by_percent(percent)









from pycaw.pycaw import AudioUtilities
import numpy as np

class VolumeController:
    def __init__(self):
        # Get default speakers
        device = AudioUtilities.GetSpeakers()

        # Access the volume interface in your pycaw version
        self.volume = device.EndpointVolume

        # Store previous volume for smoothing
        self.prev_volume = 0.0

        # Get min and max volume for mapping
        self.min_vol, self.max_vol, _ = self.volume.GetVolumeRange()

        print("✓ Volume controller initialized!")

    def map_distance_to_volume(self, distance, min_dist=30, max_dist=200):
        """
        Convert finger distance to volume level (0.0 - 1.0)
        """
        vol = (distance - min_dist) / (max_dist - min_dist)
        return np.clip(vol, 0.0, 1.0)

    def set_volume(self, distance):
        """
        Smooth and apply volume to Windows OS
        """
        # Map finger distance to 0.0-1.0
        vol_level = self.map_distance_to_volume(distance)

        # Smooth volume changes
        vol_level = 0.8 * self.prev_volume + 0.2 * vol_level
        self.prev_volume = vol_level

        # Convert 0.0-1.0 to actual Windows volume level
        win_vol = np.interp(vol_level, [0, 1], [self.min_vol, self.max_vol])
        self.volume.SetMasterVolumeLevel(win_vol, None)

        return int(vol_level * 100)


