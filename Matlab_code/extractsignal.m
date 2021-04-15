clear;
clc;
data_save_dir="E:\研究生学习\SHG\IPC-SHM-P2\chuli\base_on_class";  %signal extraction storage directory
file_dirname="E:\研究生学习\SHG\IPC-SHM-P2\data";    %directory of original signal
sensor_nums=38; %number of sensors
file_dir=dir(file_dirname);
file_dir(1:2) = [];
file_nums = length(file_dir); 
temp_dir={}; 

for z=1:sensor_nums
    sensor_dir_num=num2str(z,'%02d');
    create_dir=strcat('sensor_',sensor_dir_num);
    cunchu_dir=strcat(data_save_dir,'\',create_dir);
    mulu=cunchu_dir;
    temp_dir=[temp_dir;mulu];
    if ~exist(mulu,'dir')
	mkdir(mulu);
    end                 %generate catalog
end


for i=1:file_nums
    duqu_dir_1=strcat(file_dirname,'\',file_dir(i).name);
%     disp(duqu_dir_1); 
    file_dir_2=dir(duqu_dir_1);
    file_dir_2(1:2) = [];
    file_nums_2 = length(file_dir_2); 
    for j=1:file_nums_2
        duqu_dir_2=strcat(duqu_dir_1,'\',file_dir_2(j).name);
%         disp(duqu_dir_2); 
        load(duqu_dir_2);
        for t=1:sensor_nums
             S = regexp(file_dir_2(j).name, '\.', 'split'); 
            cunfangfile_dir=strcat(temp_dir{t},'\',S{1},'_','sensor_',num2str(t),'.mat');
%             disp(cunfangfile_dir);
            d=['sensor_',num2str(t)];
            eval([d,'=data(:,t);']);
            eval(['save(cunfangfile_dir,d)']);
        end
    end
    
    end