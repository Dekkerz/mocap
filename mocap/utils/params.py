import os

LOCAL_DATA_PATH = os.path.expanduser(os.environ.get("LOCAL_DATA_PATH"))
LOCAL_REGISTRY_PATH = os.path.expanduser(os.environ.get("LOCAL_REGISTRY_PATH"))
CHUNK_SIZE=int(os.environ.get("CHUNK_SIZE"))
UNPROCESSED_DATA='raw'
PROCESSED_DATA='processed'
EXTERNAL_DATA='external'
DATA_SOURCE=os.environ.get("DATA_SOURCE")
FREQUENCY=50

#Mapping for Label Encoding of Class (Smoke Stand etc)
CLASS_ENCODING = {'SmokeST':0
                ,'SmokeSD':1 
                ,'DrinkST':2
                ,'DrinkSD':3 
                ,'Eat':4
                ,'Sit':5
                ,'Stand':6
                }

# Use this to optimize loading of raw_data without headers: pd.read_csv(..., dtypes=..., headers=False)
DTYPES_RAW_OPTIMIZED_HEADLESS = {0:'object'
                    ,1:'float32'
                    ,2:'float32'
                    ,3:'float32'
                    ,4:'float32'
                    ,5:'float32'
                    ,6:'float32'
                    ,7:'float32'
                    ,8:'float32'
                    ,9:'float32'
                    ,10:'float32'
                    ,11:'float32'
                    ,12:'float32'
                    ,13:'float32'
                    ,14:'float32'
                    ,15:'object'
                    ,16:'object'
                    ,17:'float32'
                    ,18:'float32'
                    ,19:'float32'
                    ,20:'float32'
                    ,21:'float32'
                    ,22:'float32'
                    ,23:'float32'
                    ,24:'float32'
                    ,25:'float32'
                    ,26:'float32'
                    ,27:'float32'
                    ,28:'float32'
                    ,29:'float32'
                    ,30:'float32'
                    ,31:'object'
                    }

COLUMN_NAMES_RAW = ['timestamp_WD'
                    ,'Accelerometer_x_WD'
                    ,'Accelerometer_y_WD'
                    ,'Accelerometer_z_WD'
                    ,'Linear_acceleration_sensor_x_WD'
                    ,'Linear_acceleration_sensor_y_WD'
                    ,'Linear_acceleration_sensor_z_WD'
                    ,'Gyroscope_x_WD'
                    ,'Gyroscope_y_WD'
                    ,'Gyroscope_z_WD'
                    ,'Magnetometer_x_WD'
                    ,'Magnetometer_y_WD'
                    ,'Magnetometer_z_WD'
                    ,'Pressure_sensor_WD'
                    ,'Heart_rate_sensor_WD'
                    ,'GAP'
                    ,'timestamp_PD'
                    ,'Accelerometer_x_PD'
                    ,'Accelerometer_y_PD'
                    ,'Accelerometer_z_PD'
                    ,'Linear_acceleration_sensor_x_PD'
                    ,'Linear_acceleration_sensor_y_PD'
                    ,'Linear_acceleration_sensor_z_PD'
                    ,'Gyroscope_x_PD'
                    ,'Gyroscope_y_PD'
                    ,'Gyroscope_z_PD'
                    ,'Magnetometer_x_PD'
                    ,'Magnetometer_y_PD'
                    ,'Magnetometer_z_PD'
                    ,'GPS_lat_PD'
                    ,'GPS_long_PD'
                    ,'Class_label']

COLUMN_NAMES_PROCESSED = {0:'Accelerometer_x_WD'
                          ,1:'Accelerometer_y_WD'
                          ,2:'Accelerometer_z_WD'
                          ,3:'Linear_acceleration_sensor_x_WD'
                          ,4:'Linear_acceleration_sensor_y_WD'
                          ,5:'Linear_acceleration_sensor_z_WD'
                          ,6:'Participant_Num'
                          ,7:'Engineered_Timestamp'
                          ,8:'Class_Encoded'
                          ,9:'Accelerometer_x_WD_MMS'
                          ,10:'Accelerometer_y_WD_MMS'
                          ,11:'Accelerometer_z_WD_MMS'
                          ,12:'Linear_acceleration_sensor_x_WD_MMS'
                          ,13:'Linear_acceleration_sensor_y_WD_MMS'
                          ,14:'Linear_acceleration_sensor_z_WD_MMS'
                          ,15:'Class_label'
                          }

#PROJECT = os.environ.get("PROJECT")
#DATASET = os.environ.get("DATASET")

env_valid_options = dict(
     DATA_SOURCE=['local','big query']
    ,MODEL_TARGET=['local','gcs','mlflow']
    ,PREFECT_BACKEND=['development','production']
)

def validate_env_value(env, valid_options):
    env_value = os.environ[env]
    if env_value not in valid_options:
        raise NameError(f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}")

for env, valid_options in env_valid_options.items():
    validate_env_value(env, valid_options)
