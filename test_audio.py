from pycaw.pycaw import AudioUtilities

device = AudioUtilities.GetSpeakers()

print(type(device))
print(dir(device))
