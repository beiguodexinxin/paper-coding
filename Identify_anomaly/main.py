import Common_functions as cf


def run(c):
    import numpy as np
    import tensorflow as tf

    path='E:/研究生学习/SHG/IPC-SHM-P2/chuli/base_on_class/%s'%c   #Sensor data storage directory
    path_2='E:/研究生学习/SHG/IPC-SHM-P2/chuli/分类标签/%s.mat'%c   #Label storage directory
    list_data = cf.read_file(path)
    list_data=np.sort(list_data)
    data=np.array([]).reshape(72000,-1)
    for i in list_data:
        temp_data=cf.read_data(path+'/'+i)
        data=np.concatenate((data,temp_data,),axis=1)
    print('the shape of '+c+' is '+str(data.shape))
    print(c+" data read successfully")
    wash_data=cf.wash_data(data)
    print(c+' data wash successfully，shape：',wash_data.shape)
    stat_data = cf.get_statisitic(wash_data.T, 2400, 1200)
    print(c+" statistics and the shape is",stat_data.shape)
    norm_data=cf.data_3D(stat_data).reshape(-1,60,12,1)
    print('successful standardization')
    mode_l=tf.keras.models.load_model('2_class_model_12.h5')
    mode_2=tf.keras.models.load_model('6_model.h5')
    pre_2 = mode_l.predict(norm_data)
    pre_label_2 = np.argmax(pre_2, axis=1)
    pre_6=mode_2.predict(norm_data)
    pre_label_6= np.argmax(pre_6, axis=1)
    tem=pre_label_2
    tem[pre_label_2==1]=(pre_label_6[pre_label_2==1]+1)
    real_label=cf.read_data(path_2).reshape(-1)-1
    acc=(tem==real_label).sum()/real_label.size      #Calculation accuracy
    alnormal=['normal','missing','minor','outlier','square','trend','drift']
    d=acc*100
    save_info=['The accuracy of the prediction on %s is %2.2f%%'%(c,d)]
    for i in range(tem.size):
        if tem[i]!=0:
            save_info.append(c+' '+list_data[i].split('V')[0][:-1]+' '+alnormal[tem[i]])
    with open('./inf/%s.txt'%c,'w') as f:
        for i in save_info:
            f.write(i+'\n')
    print('save %s successfully'%c)
    return save_info


if __name__ == '__main__':
    c=[]
    sensor_num_range=range(1,3)
    for i in sensor_num_range:
        c.append('sensor_'+str(i).zfill(2))
    length=len(c)
    for i in range(length):
        run(c[i])
