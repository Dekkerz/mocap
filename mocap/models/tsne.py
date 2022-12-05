import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE



def TSNE_analysis(df):

    shuffled_1 = df.sample(n=100000)


    tsne_data = shuffled_1[['Accelerometer_x_WD', 'Accelerometer_y_WD',
        'Accelerometer_z_WD', 'Linear_acceleration_sensor_x_WD',
        'Linear_acceleration_sensor_y_WD', 'Linear_acceleration_sensor_z_WD',
        'Gyroscope_x_WD', 'Gyroscope_y_WD', 'Gyroscope_z_WD',
        'Magnetometer_x_WD', 'Magnetometer_y_WD', 'Magnetometer_z_WD']].copy()



    scl = StandardScaler()
    tsne_data = scl.fit_transform(tsne_data)

    tsne = TSNE(random_state=42, n_components=2)
    tsne_transformed = tsne.fit_transform(tsne_data)

    return tsne_transformed

def plot_TSNE(tsne_transformed, df):

    # Plot data
    dftsne = pd.DataFrame(tsne_transformed)
    dftsne['Class_label'] = df['Class_label'].reset_index(drop=True)
    dftsne.columns = ['x1','x2','Class_label']

    fig, ax = plt.subplots(figsize=(18, 7))
    sns.scatterplot(data=dftsne,x='x1',y='x2',hue='Class_label',legend="full",alpha=0.5,ax=ax)
    ax.set_title('TSNE Reduction Colored by Activity')
