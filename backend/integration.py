# import numpy as np
# import pickle
# from trial import *

# from school import *
# from audio import *
# from inference import *

# # path = sys.argv[1]

# grid_locs_sound_data = pickle.load(open("sound_data_locs.dat", "rb"))
# coords_gen = np.array(list(grid_locs_sound_data.keys()))

# locis = sample_random_path()
# random_walk = [(locis[0][i], locis[1][i]) for i in range(100,150)]

# count = 0
# def predict():
#     gunshot_loc = random_walk[count]
#     dists_x_y = coords_gen - gunshot_loc
#     closest_loc = np.argmin(np.square(dists_x_y[:,0]) + np.square(dists_x_y[:,1]) ** 0.5)
#     response = LocIdentification(stoneman_douglas.coords, 
#                                  stoneman_douglas.cluster_labels, 
#                                  grid_locs_sound_data[(coords_gen[closest_loc][0], coords_gen[closest_loc][1])])
#     prediction = response.predicted_loc
#     count += 1
#     return (prediction[0], prediction[1])

