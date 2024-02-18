import numpy as np
import pickle
import matplotlib.pyplot as plt
from celluloid import Camera
# import sys
from re import A

from school import *
from audio import *
from inference import *

# grid_locs_sound_data = pickle.load(open(path, "rb"))
# coords_gen = np.array(list(grid_locs_sound_data.keys()))

def sample_random_path():
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

# locis = sample_random_path()
# random_walk = [(locis[0][i], locis[1][i]) for i in range(100,150)]

# errors = []

# fig = plt.figure()
# camera = Camera(fig)

# predictions = []

# for gunshot_loc in random_walk:
#   dists_x_y = coords_gen - gunshot_loc
#   closest_loc = np.argmin(np.square(dists_x_y[:,0]) + np.square(dists_x_y[:,1]) ** 0.5)
#   response = LocIdentification(stoneman_douglas.coords, 
#                                stoneman_douglas.cluster_labels, 
#                                grid_locs_sound_data[(coords_gen[closest_loc][0], coords_gen[closest_loc][1])])
#   prediction = response.predicted_loc
#   error = ((gunshot_loc[0] - prediction[0]) ** 2 + (gunshot_loc[1] - prediction[1]) ** 2) ** 0.5 * 111139 # meters
#   errors.append(error)
#   predictions.append((prediction[0], prediction[1]))

#   shift_x = np.min(stoneman_douglas.coords[:,1])
#   scale_x = msd_img.shape[1] / (np.max(stoneman_douglas.coords[:,1]) - shift_x)
#   shift_y = np.min(stoneman_douglas.coords[:,0])
#   scale_y = msd_img.shape[0] / (np.max(stoneman_douglas.coords[:,0]) - shift_y)

#   plt.scatter(scale_x * (stoneman_douglas.coords[:,1] - shift_x), 
#               msd_img.shape[0] - scale_y * (stoneman_douglas.coords[:,0] - shift_y),
#               s=1, c=stoneman_douglas.cluster_labels)

#   temp1 = np.array(response.locations).reshape(50,2)
#   temp2 = np.array(response.absolute_peaks)
#   plt.imshow(msd_img, alpha=0.35)
#   plt.scatter(scale_x * (temp1[:,1] - shift_x), 
#               msd_img.shape[0] - scale_y * (temp1[:,0] - shift_y), 
#               c=temp2, cmap="inferno")
#   plt.scatter(scale_x * (gunshot_loc[1] - shift_x), 
#               msd_img.shape[0] - scale_y * (gunshot_loc[0] - shift_y), 
#               s=200, c="r", marker="D", alpha=0.5)
#   plt.scatter(scale_x * (prediction[1] - shift_x), 
#               msd_img.shape[0] - scale_y * (prediction[0] - shift_y), 
#               s=200, c="k", marker="X", alpha=0.5)
#   plt.axis("off")
#   camera.snap()

# anim = camera.animate()
# plt.close()
# anim = camera.animate(interval = 200, repeat = True, repeat_delay = 1000)
