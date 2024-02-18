# from school import *
# from audio import *
# from inference import *

# blocked_out_areas = [[(26.30519670082991, -80.2696934486984), (26.30552456843113, -80.26946004753805)],
#                      [(26.30505198614237, -80.2696934486984), (26.305172487141704, -80.26750267960053)],
#                      [(26.30424262326676, -80.2696934486984), (26.304385226697374, -80.26897105198778)],
#                      [(26.304160444938894, -80.26930268328718), (26.304232955231214, -80.26891443200984)],
#                      [(26.304375558673733, -80.26759599538046), (26.305028148460227, -80.26750432493998)],
#                      [(26.303653, -80.26761014375148), (26.304248003454635, -80.26750432493998)],
#                      [(26.304221729826835, -80.26856872033741), (26.304692348071782, -80.26804374157416)],
#                      [(26.303624226860236, -80.26930672012321), (26.303892050342267, -80.26889396286808)],
#                      [(26.304810957510572, -80.26883965065957), (26.304946120422322, -80.26864852620692)],
#                      [(26.303975472509677, -80.2688456230644), (26.304131751948994, -80.26862691756197)],
#                      [(26.30494156021424, -80.26883928377447), (26.305137618206654, -80.26798664927954)],
#                      [(26.303687408626995, -80.26755336516939), (26.305135501619723, -80.26731600801872)]
#                     ]

# school_boundary = [(26.303653, -80.2696934486984), (26.305085, -80.267475)] # bottom left to top right (lat, long) or (y, x)

# stoneman_douglas = School(school_boundary, blocked_out_areas, 2500)

# interval = 12
# all_lats = np.linspace(school_boundary[0][0], school_boundary[1][0], num=interval)
# all_longs = np.linspace(school_boundary[0][1], school_boundary[1][1], num=interval)
# all_lats = np.tile(all_lats, interval)
# all_longs = np.array([np.repeat(i, interval) for i in all_longs]).flatten()
# grid_locs = np.vstack((all_lats, all_longs)).T

# grid_locs_sound_data = {}

# for loc in grid_locs:
#   data = StudentRecordings(stoneman_douglas.coords, (loc[0], loc[1]), "glock_17_9mm_caliber")
#   grid_locs_sound_data[(loc[0], loc[1])] = data.all_data
  