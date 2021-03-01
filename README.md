# merge_xml_flv

一个用于拼接弹幕姬（https://github.com/Bililive/BililiveRecorder） 录制的视频、弹幕的工具

用法：

python merge.py PATH

程序会递归扫描 PATH 下的所有文件，把同一文件夹内的flv和xml文件合并，输出到该文件夹内。可以指定为PATH为 . ,此时PATH为python程序所在的文件夹。
