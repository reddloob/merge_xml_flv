#encoding=utf-8
import sys
import os
from natsort import natsorted
from ffmpy import FFmpeg

def mergexml(xmlfile_list):

    if len(xmlfile_list)==1:
        return
    
    f_output=open(xmlfile_list[0][:xmlfile_list[0].rindex('.')]+'-merge.xml','a+')
    f_input=open(xmlfile_list[0])
    lines=f_input.readlines()
    for i in range(0,24):
        f_output.write(lines[i])
    for i in range(24,len(lines)-1):
        if '<d p=' in lines[i]:
            f_output.write(lines[i])
    last_time = lines[len(lines) - 2][lines[len(lines) - 2].index('"')+1:lines[len(lines) - 2].index(',')]
    print(last_time)
    f_input.close()

    for i in range(1, len(xmlfile_list)):
        f_input = open(xmlfile_list[i])
        lines = f_input.readlines()
        for j in range(24,len(lines)-1):
            if '<d p=' in lines[j]:
                wrong_time=lines[j][lines[j].index('"')+1:lines[j].index(',')]
                true_time=format(float(wrong_time)+float(last_time),'.7f')
                correct_line=lines[j].replace(wrong_time, true_time, 1)
                f_output.write(correct_line)
                if j==len(lines)-2:
                    last_time=true_time
                    print(last_time)
        if i==len(xmlfile_list)-1:
            f_output.write('</i>')
        f_input.close()
    
    f_output.close()
    
    xmlfilename=xmlfile_list[0][:xmlfile_list[0].rindex('.')]+'-merge.xml'
    assfilename=xmlfilename[:xmlfilename.rindex('.')]+'.ass'
    os.system("DanmakuFactory -i %s -o %s" % (xmlfilename,assfilename))


def mergevideo(flvfile_list):

    tsfile_list=[]
    for flvfile in flvfile_list:
        tsfile=flvfile[:flvfile.rindex('.')]+'.ts'
        tsfile_list.append(tsfile)
        FFmpeg(inputs={flvfile: None},
               outputs={tsfile: '-c copy -bsf:v h264_mp4toannexb -f mpegts'}).run()

    mp4file = tsfile_list[0][:tsfile_list[0].rindex('.')]+'.mp4'

    if len(tsfile_list)==1:
        FFmpeg(inputs={tsfile_list[0]: None},
               outputs={mp4file: '-c copy -absf aac_adtstoasc'}).run()
    else:
        FFmpeg(inputs={'concat:' + '|'.join(tsfile_list): None},
               outputs={mp4file: '-c copy -absf aac_adtstoasc'}).run()





def main():

    input_path = sys.argv[1]  # 弹幕文件所在文件夹
    if input_path=='.':
        input_path=os.getcwd()
    path_list = []

    for root, dirs, filenames in os.walk(input_path):
        for filename in filenames:
            if root not in path_list:
                path_list.append(root)
    for path in path_list:
        xmlfile_list=[]
        flvfile_list=[]
        filenames = natsorted(os.listdir(path))
        for filename in filenames:
            if os.path.splitext(filename)[1]=='.xml':
                xmlfile_list.append(os.path.join(path,filename))
            if os.path.splitext(filename)[1]=='.flv':
                flvfile_list.append(os.path.join(path, filename))
        if xmlfile_list:
            print(xmlfile_list)
            mergexml(xmlfile_list)
        if flvfile_list:
            print(flvfile_list)
            mergevideo(flvfile_list)


if __name__ == "__main__":
    main()





