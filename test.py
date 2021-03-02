#此程序用于把一个文件夹内（不包含子目录中）的多个flv文件转码为mp4文件
import sys
import os
from natsort import natsorted
from ffmpy import FFmpeg

path = sys.argv[1]
if path == '.':
    path = os.getcwd()

filenames = natsorted(os.listdir(path))

for filename in filenames:
    file = os.path.join(path,filename)
    if os.path.splitext(file)[1] == '.flv':
        tsfile = file[:file.rindex('.')] + '.ts'
        mp4file = tsfile[:tsfile.rindex('.')] + '.mp4'
        FFmpeg(inputs={file: None},
               outputs={tsfile: '-y -c copy -bsf:v h264_mp4toannexb -f mpegts'}).run()
        os.remove(file)
        FFmpeg(inputs={tsfile: None},
               outputs={mp4file: '-y -c copy -absf aac_adtstoasc'}).run()
        os.remove(tsfile)
