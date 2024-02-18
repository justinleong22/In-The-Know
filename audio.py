import numpy as np
import os
import scipy
from scipy.io import wavfile

class StudentRecordings():
  def __init__(self, coords, gunshot_loc, path=None):
    self.root = "/content/drive/MyDrive/Treehacks Empower Project/" + path
    self.decibel_gunshot = 150
    self.radius_of_max_decibel = 1 # meter
    self.all_data = self.collect_student_audio(coords, gunshot_loc)

  def distance(self, lat1, long1, lat2, long2):
    return ((lat1 - lat2) ** 2 + (long1 - long2) ** 2) ** 0.5 * 111139

  def acquire_data(self):
    idx = np.random.randint(len(os.listdir(self.root)))
    path = os.listdir(self.root)[idx]
    _, gunshot = wavfile.read(self.root + "/" + path)
    gunshot = gunshot[np.arange(0, gunshot.shape[0], 100)]
    return gunshot

  def sound_decay(self, sound_data, distance):
    decibel_decay = np.log2(distance / self.radius_of_max_decibel) * 6
    ratio = 1 - decibel_decay / self.decibel_gunshot
    return sound_data * ratio

  def distort_sound(self, sound_data):
    # distortion accounts for phones in pocket, phones in backpack, poor audio quality, etc.
    p_distortion = 0.6
    if np.random.binomial(1, p_distortion):
      sound_data = sound_data * np.clip(np.random.normal(loc=0.2, scale=0.2), a_min=0, a_max=None)
    for i in range(sound_data.shape[0]):
      sound_data[i] -= np.random.uniform(0, sound_data[i] * 0.2)
    return sound_data

  def collect_student_audio(self, coords, gunshot_loc):
    gunshot = self.acquire_data()
    all_sound_data = []
    for coord in coords:
      dist = self.distance(coord[0], coord[1], gunshot_loc[0], gunshot_loc[1])
      dist_adjusted_sound = self.sound_decay(gunshot, dist)
      distorted_sound = self.distort_sound(dist_adjusted_sound)
      all_sound_data.append(distorted_sound)
    return np.array(all_sound_data)
