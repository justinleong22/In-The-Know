import numpy as np
import matplotlib.pyplot as plt
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
