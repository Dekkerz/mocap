import pandas as pd


def rename_features(df):
    d = {0:'timestamp_WD',
     1:'Accelerometer_x_WD', 2:'Accelerometer_y_WD', 3:'Accelerometer_z_WD',
     4:'Linear_acceleration_sensor_x_WD', 5:'Linear_acceleration_sensor_y_WD', 6:'Linear_acceleration_sensor_z_WD',
     7:'Gyroscope_x_WD', 8:'Gyroscope_y_WD', 9:'Gyroscope_z_WD',
    10:'Magnetometer_x_WD', 11:'Magnetometer_y_WD', 12:'Magnetometer_z_WD',
     13:'Pressure_sensor_WD', 14:'Heart_rate_sensor_WD',
    15:'GAP',
     16:'timestamp_PD',
     17:'Accelerometer_x_PD', 18:'Accelerometer_y_PD', 19:'Accelerometer_z_PD',
    20:'Linear_acceleration_sensor_x_PD', 21:'Linear_acceleration_sensor_y_PD', 22:'Linear_acceleration_sensor_z_PD',
     23:'Gyroscope_x_PD', 24:'Gyroscope_y_PD',25:'Gyroscope_z_PD',
     26:'Magnetometer_x_PD', 27:'Magnetometer_y_PD', 28:'Magnetometer_z_PD',
     29:'GPS_lat_PD',30:'GPS_long_PD',
     31:'Class_label'}

    df = df.rename(d, axis=1)

    return df
