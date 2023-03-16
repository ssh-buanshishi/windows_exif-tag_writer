# win_exif_tag_writer
本程序用以向jpg、tiff图片文件写入windows系统专属的exif标签。

本程序（.py和.exe）需要在Windows系统下运行，建议Win7及以上（最好是Win10）。

运行".py"脚本需要额外安装的python库：
piexif、pyexiv2

编译指令：
pyinstaller -D "win_exif_tag_writer.py"

使用"-D"打包成文件夹是为了较快的运行速度，如果使用"-F"，第一次运行速度会很慢，需要大概10秒。

★☆ 注意！！！如果需要编译，还需要调整pyexiv2库，不然编译出来会找不到运行库！！！ ★☆

调整方法如下：
1.进入python（python.exe）所在的目录；
2.顺着路径"Lib\site-packages\pyexiv2"，来到“pyexiv2库文件夹”，把这个位置记为“pyexiv2库文件夹”；
3.进入这里的"lib"文件夹，将文件"exiv2.dll"、"exiv2api.cpp"和"README.md"移动到上一级文件夹，也就是第一步里的“pyexiv2库文件夹”；
4.移动文件完成后，回到第三步的"lib"文件夹，继续深入，进入"py3.8-win"文件夹，将文件"exiv2api.pyd"移动到第一步里的“pyexiv2库文件夹”；
5.回到第一步里的“pyexiv2的库文件夹”，删除"lib"文件夹（此时这个文件夹里只有不重要的缓存文件了）；
6.至此，完成了重要文件的移动。整个移动过程可以理解为把重要的东西全部转移到“根目录”下，方便编译时访问。
7.用趁手的.py代码工具打开“pyexiv2库文件夹”下的"core.py"，
  将第四行的：
  from .lib import exiv2api
  去掉“lib”字样，改为：
  from . import exiv2api
8.保存更改过后的"core.py"，退出编辑工具。至此，所有调整工作全部完成。


文件列表：
1.源码文件：win_exif_tag_writer.py
2.命令行帮助文件：win_exif_tag_writer.py

本人的代码编辑和运行环境：
Python版本：Python_3.8.6_x64
Windows版本：Windows 10 [版本 10.0.19044.1706]

【2023年3月16日】
