from fastapi import FastAPI, File, UploadFile, Response
# import tensorflow as tf
from integration import *

shooter_location_data = None
    
# model = tf.keras.saving.load_model("MODEL_NAME.keras")


def send(files: list[UploadFile], latitude: list[float], longitude: list[float]):
    #shooter_location_data = model.predict(files, latitude, longitude) 
    return True

shooter_points = [(26.30447185224176, -80.26779246279399),
 (26.30447185224176, -80.26779246279399),
 (26.304287879493405, -80.26779772702061),
 (26.304287879493405, -80.26779772702061),
 (26.304287879493405, -80.26779772702061),
 (26.304287879493405, -80.26779772702061),
 (26.304287879493405, -80.26779772702061),
 (26.304287879493405, -80.26779772702061),
 (26.304287879493405, -80.26779772702061),
 (26.304054169541878, -80.26810204619655),
 (26.304054169541878, -80.26810204619655),
 (26.304054169541878, -80.26810204619655),
 (26.304054169541878, -80.26810204619655),
 (26.304054169541878, -80.26810204619655),
 (26.304054169541878, -80.26810204619655),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.30366463982804, -80.26810724850266),
 (26.30366463982804, -80.26810724850266),
 (26.30366463982804, -80.26810724850266),
 (26.30366463982804, -80.26810724850266),
 (26.30366463982804, -80.26810724850266),
 (26.30366463982804, -80.26810724850266),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.303830436345226, -80.26812785696576),
 (26.304064332239868, -80.26846070382433),
 (26.304064332239868, -80.26846070382433),
 (26.304064332239868, -80.26846070382433),
 (26.304064332239868, -80.26846070382433),
 (26.304064332239868, -80.26846070382433),
 (26.304064332239868, -80.26846070382433),
 (26.304064332239868, -80.26846070382433),
 (26.304210114599453, -80.26848447124421),
 (26.304210114599453, -80.26848447124421),
 (26.304210114599453, -80.26848447124421),
 (26.304210114599453, -80.26848447124421),
 (26.304269295403568, -80.26878364254007),
 (26.304269295403568, -80.26878364254007),
 (26.304269295403568, -80.26878364254007),
 (26.304470255256295, -80.26876357043315)]

import numpy as np
import pickle
from trial import *

from school import *
from inference import *
from msd_driver import * 

grid_locs_sound_data = pickle.load(open("sound_data_locs.dat", "rb"))
coords_gen = np.array(list(grid_locs_sound_data.keys()))

locis = sample_random_path()
random_walk = [(locis[0][i], locis[1][i]) for i in range(100,150)]

stoneman_douglas = School(school_boundary, blocked_out_areas, 2500)

count = 0

def shooter_location():
    global count
    gunshot_loc = random_walk[count]
    dists_x_y = coords_gen - gunshot_loc
    closest_loc = np.argmin(np.square(dists_x_y[:,0]) + np.square(dists_x_y[:,1]) ** 0.5)
    response = LocIdentification(stoneman_douglas.coords, 
                                 stoneman_douglas.cluster_labels, 
                                 grid_locs_sound_data[(coords_gen[closest_loc][0], coords_gen[closest_loc][1])])
    prediction = response.predicted_loc
    count += 1
    return prediction[0], prediction[1]