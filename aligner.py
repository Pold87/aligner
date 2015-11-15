import pandas as pd
import numpy as np
import json
import datetime

# Read in GPS information from drone
with open("loggi.txt") as f_loggi:

    lines = f_loggi.readlines()    

# Parse information
timestamps = []
gps_x = []
gps_y = []
gps_z = []

for line in lines[:-1]:
    
    time_and_info = line.split(' ', 1)
    drone_info = json.loads(time_and_info[1])['droneInformation']

    # Extract timestampe and coordindates
    timestamps.append(datetime.datetime.strptime(time_and_info[0], "%M:%S.%f"))
    gps_x.append(drone_info['gpsx'])
    gps_y.append(drone_info['gpsy'])
    gps_z.append(drone_info['gpsz'])


# Save information in DataFrame
df_all_info = pd.DataFrame()
df_all_info['gps_x'] = gps_x
df_all_info['gps_y'] = gps_y
df_all_info['gps_z'] = gps_z
df_all_info['timestamp'] = timestamps

# Read in information about picture creation

df_imagelogger = pd.read_csv("imagelogger.txt", sep=" ", index_col=0)
np_imagelogger = df_imagelogger.iloc[:, 0].values

log_times = df_all_info.timestamp

image_gps_x = []
image_gps_y = []
image_gps_z = []
times_images = []
times_gps = []
time_diffs = []

for image_time in np_imagelogger:

    parsed = datetime.datetime.strptime(image_time, "%M:%S.%f")

    diffs = log_times - parsed
    diffs = np.divide(diffs, np.timedelta64(1, 's'))
    diffs = np.fabs(diffs)

    pos = np.argmin(diffs)
    diff = np.min(diffs)

    image_gps_x.append(df_all_info.ix[pos, "gps_x"])
    image_gps_y.append(df_all_info.ix[pos, "gps_y"])
    image_gps_z.append(df_all_info.ix[pos, "gps_z"])
    times_images.append(parsed)
    times_gps.append(df_all_info.ix[pos, "timestamp"])
    time_diffs.append(diff)


df_imageinfo = pd.DataFrame()
df_imageinfo['gpsx'] = image_gps_x
df_imageinfo['gpsy'] = image_gps_y
df_imageinfo['gpsz'] = image_gps_z
df_imageinfo['time_image'] = times_images
df_imageinfo['time_gps'] = times_gps
df_imageinfo['diff'] = time_diffs

df_imageinfo.to_csv("imagelocations.csv")



        
        
    
    
    


    

