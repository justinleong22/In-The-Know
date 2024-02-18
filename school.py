import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

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
