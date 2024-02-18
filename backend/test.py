import numpy as np
import matplotlib.pyplot as plt
import os
import scipy
from scipy.io import wavfile
from scipy.signal import find_peaks
from sklearn.cluster import KMeans

blocked_out_areas = [[(26.30519670082991, -80.2696934486984), (26.30552456843113, -80.26946004753805)],
                     [(26.30505198614237, -80.2696934486984), (26.305172487141704, -80.26750267960053)],
                     [(26.30424262326676, -80.2696934486984), (26.304385226697374, -80.26897105198778)],
                     [(26.304160444938894, -80.26930268328718), (26.304232955231214, -80.26891443200984)],
                     [(26.304375558673733, -80.26759599538046), (26.305028148460227, -80.26750432493998)],
                     [(26.303653, -80.26761014375148), (26.304248003454635, -80.26750432493998)],
                     [(26.304221729826835, -80.26856872033741), (26.304692348071782, -80.26804374157416)],
                     [(26.303624226860236, -80.26930672012321), (26.303892050342267, -80.26889396286808)],
                     [(26.304810957510572, -80.26883965065957), (26.304946120422322, -80.26864852620692)],
                     [(26.303975472509677, -80.2688456230644), (26.304131751948994, -80.26862691756197)],
                     [(26.30494156021424, -80.26883928377447), (26.305137618206654, -80.26798664927954)],
                     [(26.303687408626995, -80.26755336516939), (26.305135501619723, -80.26731600801872)]
                    ]

school_boundary = [(26.303653, -80.2696934486984), (26.305085, -80.267475)]

class School():
    def __init__(self, school_boundary, blocked_out_areas, num_students):
        self.boundary = school_boundary
        self.blocked_out = blocked_out_areas
        self.coords = self.sample_lat_long(num_students)
        self.cluster_labels = self.cluster_students()

  def in_bounds(self, coord, lat1, long1, lat2, long2):
    if np.random.binomial(1, 0.02):
      return False
    return coord[0] >= lat1 and coord[0] <= lat2 and coord[1] >= long1 and coord[1] <= long2

  def plot_coords(self, coords):
    coords = np.array(coords)
    plt.scatter(coords[:,1], coords[:,0], s=1)
    plt.show()

  def sample_lat_long(self, num_students):
    lat_rand = np.random.uniform(school_boundary[0][0], school_boundary[1][0], size=int(num_students / 0.7))
    long_rand = np.random.uniform(school_boundary[0][1], school_boundary[1][1], size=int(num_students / 0.7))
    coords_rand = np.vstack((lat_rand, long_rand)).T
    coords_rand = coords_rand.tolist()
    for block in self.blocked_out:
      lat1 = block[0][0]
      lat2 = block[1][0]
      long1 = block[0][1]
      long2 = block[1][1]
      coords_rand = [coord for coord in coords_rand if not self.in_bounds(coord, lat1, long1, lat2, long2)]
    return np.array(coords_rand)

  def cluster_students(self, num_clusters=10):
    kmeans = KMeans(n_clusters=num_clusters, n_init="auto")
    kmeans.fit(self.coords)
    # plt.scatter(coords_rand[:,1], coords_rand[:,0], s=1, c=kmeans.labels_)
    # plt.scatter(kmeans.cluster_centers_[:,1], kmeans.cluster_centers_[:,0], c="r")
    # plt.show()
    return kmeans.labels_

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

grid_locs_sound_data = pickle.load(open("asdfj;adsfjkl;", "rb"))
coords_gen = np.array(list(grid_locs_sound_data.keys()))

def sample_random_walk():
  mult_lat = 0.2
  mult_long = 0.2
  #Get random gun_loc
  lat_dist = abs(school_boundary[0][0] - school_boundary[1][0])
  zone = lat_dist * (1/11)
  n = np.random.randint(4)
  min_la = school_boundary[0][0]
  max_la = school_boundary[0][0] + zone
  min_lo = school_boundary[0][1]
  max_lo = school_boundary[0][1] + zone
  if n == 1 or n == 3:
    min_lo = school_boundary[1][1] - zone
    max_lo = school_boundary[1][1]
    mult_long = mult_long * -1

  if n == 2 or n == 3:
    min_la = school_boundary[1][0] - zone
    max_la = school_boundary[1][0]
    mult_lat = mult_lat * -1

  gunshot_loc = (np.random.uniform(min_la,max_la), np.random.uniform(min_lo,max_lo))
  print(gunshot_loc)


  #Begin random plotting
  g2 = (gunshot_loc[0], gunshot_loc[1])
  # just for graphing the path
  min = 0.0001
  max = 0.0002

  # Camera prep
  fig = plt.figure()
  plt.xlim(school_boundary[0][0],school_boundary[1][0])
  plt.ylim(school_boundary[0][1],school_boundary[1][1])
  camera = Camera(fig)

  #loop thru mvmt, making a list of all gunshot locations
  locis = [[gunshot_loc[0]],[gunshot_loc[1]]]
  rand = np.random.randint(34,39)
  for i in range(300):
    if i % 40 == rand: #random movements
      a = np.random.randint(2)
      if a == 1:
        mult_lat = mult_lat * -1
      else:
        mult_long = mult_lat * -1
    lat_mod = mult_lat * np.random.uniform(min, max)
    long_mod = mult_long * np.random.uniform(min, max)
    g2 = (g2[0] + lat_mod , g2[1] + long_mod)
    if g2[0] < school_boundary[0][0] or g2[0] > school_boundary[1][0] or g2[1] < school_boundary[0][1] or g2[1] > school_boundary[1][1]:
      mult_lat = mult_lat * -1
      mult_long = mult_long * -1
      g2 = (g2[0] - lat_mod, g2[1] - long_mod)
    locis[0].append(g2[0])
    locis[1].append(g2[1])
  return locis

random_walk = [(locis[0][i], locis[1][i]) for i in range(100,150)]

for gunshot_loc in random_walk:
  dists_x_y = coords_gen - gunshot_loc
  closest_loc = np.argmin(np.square(dists_x_y[:,0]) + np.square(dists_x_y[:,1]) ** 0.5)
  response = LocIdentification(stoneman_douglas.coords, 
                               stoneman_douglas.cluster_labels, 
                               grid_locs_sound_data[(coords_gen[closest_loc][0], coords_gen[closest_loc][1])])
  prediction = response.predicted_loc
  return prediction[0], prediction[1]