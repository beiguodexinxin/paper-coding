clear all;
clc;
path='E:\�о���ѧϰ\SHG\IPC-SHM-P2\label.mat';%label data directoty
saverdir='E:\�о���ѧϰ\SHG\IPC-SHM-P2\chuli\�����ǩ';%extracted label storage directory
load(path)  
% info.label.manual{1,1}
name='sensor_';
for i=1:38
    filename=[name,num2str(i,'%02d')];
%     disp(filename);
    instruction=[filename,'=','info.label.manual{1,',num2str(i),'};'];
    eval(instruction);
    tempdir=[saverdir,'\',filename,'.mat'];
%     disp(tempdir);
    eval(['save(tempdir,filename)']);
end