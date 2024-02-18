import numpy as np
import scipy
import matplotlib.pyplot as plt
import pickle
from celluloid import Camera

class LocIdentification():
  def __init__(self, coords, cluster_labels, all_data):
    self.scaling_factor = 1e4
    self.locations = []
    self.absolute_peaks = []
    self.predicted_loc = self.calculate(coords, cluster_labels, all_data)

  def filter_from_cluster(self, coords, cluster_data):
    top_n = 5
    idxs = np.argsort(np.max(cluster_data, axis=1))[-1 * top_n:]
    locations = coords[idxs]
    absolute_peaks = np.max(cluster_data, axis=1)[idxs]
    self.locations.append(locations)
    self.absolute_peaks.append(absolute_peaks)
    return locations, absolute_peaks
  
  def location_inference(self, coords_subset, peak_data):
    loc_delegates = []
    peak_delegates = []
    for i in range(peak_data.shape[0]):
      subweights = scipy.special.softmax(self.scaling_factor * (peak_data[i] - np.min(peak_data[i])))
      loc_delegate = np.sum(np.multiply(coords_subset[i], subweights.reshape(-1,1)), axis=0)
      peak_delegate = np.sum(np.multiply(peak_data[i], subweights))
      loc_delegates.append(loc_delegate)
      peak_delegates.append(peak_delegate)
      
    weights = scipy.special.softmax(self.scaling_factor * (peak_delegates - np.min(peak_delegates)))
    computed_loc = np.sum(np.multiply(loc_delegates, weights.reshape(-1,1)), axis=0)
    return computed_loc
  
  def calculate(self, coords, cluster_labels, all_data):
    candidate_coords = []
    absolute_peaks = []
    for cluster in range(np.max(cluster_labels) + 1):
      locs, peaks = self.filter_from_cluster(coords[cluster_labels == cluster], all_data[cluster_labels == cluster])
      candidate_coords.append(locs)
      absolute_peaks.append(peaks)
    candidate_coords = np.array(candidate_coords)
    absolute_peaks = np.array(absolute_peaks)
    return self.location_inference(candidate_coords, absolute_peaks)
