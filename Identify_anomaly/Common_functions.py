def read_data(file):
    """
    Read mat file
    :param file: data directory
    :return: return data,the shape of data is 72000*38, 38 corresponds to 38 sensors
    """
    import scipy.io as scio
    data=scio.loadmat(file)
    temp=list(data.keys())
    d=data[temp[-1]]
    return d

def read_file(file):
    """
    read the data directory under the file
    """
    import os
    import numpy as np
    return np.array(os.listdir(file))

def wash_data(data):
    """
    clean the data,replace the nan in that column with the average of this column,
    if this column of data is all nan, 0 replace its nan
    :param data:
    :return:
    """
    from sklearn.impute import SimpleImputer
    import numpy as np
    nan_data=np.isnan(data)
    nan_arg=nan_data.sum(axis=0)
    list_all_nan=np.argwhere(nan_arg==data.shape[0]).reshape(-1)
    for i in list_all_nan:
        data[:,i]=np.zeros(data.shape[0])
    imputer=SimpleImputer(missing_values=np.nan,strategy='mean')
    imputer=imputer.fit(data)
    data_1=(imputer.transform(data))
    return data_1

def static_1D(data):
    '''
    read one-dimensional data,then returned statistic include maximum,
    minimum,standard deviation,range,value,kurtosis,skewness.
    '''
    import numpy as np
    import pandas as pd
    data_max=np.nanmax(data)
    data_min=np.nanmin(data)
    data_std=np.nanstd(data)
    data_range=data_max-data_min
    value = np.sqrt(sum(np.power(data, 2)) / len(data))
    data_kurt=pd.Series(data).kurt()
    return np.array([data_max,data_min,data_std,data_range,np.float(value),data_kurt])


def derivation(y):
    import numpy as np
    t=np.array(range(y.shape[0]))/20
    temp_data=np.diff(y)/np.diff(t)
    return temp_data

def get_split_data_stat(data,length,overlap):
    import numpy as np
    return_data=static_1D(data).reshape(-1,6)
    split_start=0
    while True:
        split_end=split_start+length
        temp_data=static_1D(data[split_start:split_end]).reshape(-1,6)
        return_data=np.concatenate((return_data,temp_data),axis=0)
        if split_end>=data.shape[0]:
            break
        split_start =split_end-overlap
    return return_data

def get_statisitic(data,length,overlap):
    """

    :param data: the shape of data is n*72000,n take any values.
    :param length:the length of split data
    :param overlap: overlap of split data
    :return: the shape of returned data is n*60*12,based on length=2400,overlap=1200
    """
    import numpy as np
    save_data=np.array([]).reshape(-1,60,12)
    for i in range(data.shape[0]):
        temp_data=data[i,:]
        diff_data=derivation(temp_data)
        diff_data=np.append(diff_data,0)
        stat_1 = get_split_data_stat(temp_data,length,overlap)
        stat_2=get_split_data_stat(diff_data,length,overlap)
        stat_data=np.concatenate((stat_1,stat_2),axis=1)
        stat_data=stat_data.reshape(-1,60,12)
        save_data=np.concatenate((save_data,stat_data),axis=0)
    return save_data

def feature_normalize(dt):
    from sklearn import preprocessing
    min_max_scaler=preprocessing.MaxAbsScaler()
    x_traun_maxsbs=min_max_scaler.fit_transform(dt)
    return x_traun_maxsbs


def data_3D(data):
    import numpy as np
    temp_data=np.array([]).reshape(-1,60,12)
    for i in range(data.shape[0]):
        temp_data=np.concatenate((temp_data,feature_normalize(data[i,:,:]).reshape(-1,60,12)),axis=0)
    return temp_data