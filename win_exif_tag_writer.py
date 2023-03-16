# -*- coding: UTF-8 -*-

# ------------- 所需要添加的库 ------------- #

# 指令参数解析库
import argparse
# 系统辅助库
import os,sys
# exif写入操作库piexif和pvexiv2
import piexif,pyexiv2

# ------------- 所需要添加的库 ------------- #





# https://exiv2.org/tags.html 的说明：

# 【Metadata reference tables】
# //Standard Exif Tags//
# These are the Exif tags as defined in the Exif 2.3 standard.
# IFD1 tags are not listed separately. 
# All IFD0 tags may also be present in IFD1, according to the standard. 
# The second part of the Exiv2 key of an IFD1 tag is Thumbnail (instead of Image), 
# the other two parts of the key are the same as for IFD0 tags.

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Tag (hex)		Tag (dec)	IFD			Key						Type	Tag description										个人备注     #
# …… …… 																																#
# 0x9c9b		40091		Image		Exif.Image.XPTitle		Byte	Title tag used by Windows, encoded in UCS2			ps:标题		#
# 0x9c9c		40092		Image		Exif.Image.XPComment	Byte	Comment tag used by Windows, encoded in UCS2		ps:备注		#
# 0x9c9d		40093		Image		Exif.Image.XPAuthor		Byte	Author tag used by Windows, encoded in UCS2			ps:作者		#
# 0x9c9e		40094		Image		Exif.Image.XPKeywords	Byte	Keywords tag used by Windows, encoded in UCS2		ps:标记		#
# 0x9c9f		40095		Image		Exif.Image.XPSubject	Byte	Subject tag used by Windows, encoded in UCS2		ps:主题		#
# …… ……																																	#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# USC2就是python里的：encoding='utf-16'。





## 添加函数
# 定义piexif写exif函数
def pv1_write(img_path_full,choice,contents_written_into):
    try:
        # 这个模块不需要重命名和cd操作
        # 修改前记录当前文件夹位置
        # currentPath = os.getcwd()

        # 处理路径中的“\”
        img_path_full = img_path_full.replace("\\\\","/")
        img_path_full = img_path_full.replace("\\","/")

        # 检查文件是否存在
        status = os.path.exists(img_path_full)
        if status != True:
            raise Exception(str("图片文件路径：" + img_path_full + " 不存在"))

        # 读取当前图片的exif信息到一个变量。否则如果直接piexif.insert()，图片原本的exif会被覆盖。
        exif_dict = piexif.load(img_path_full)

        # 根据写入选项，使用字典类型，预先分配好要修改的exif项
        # piexif模块需要用到utf-16编码。
        if choice == 1:
            exif_dict["0th"][40091] = bytes(str(contents_written_into), encoding='utf-16')
        elif choice == 2:
            exif_dict["0th"][40092] = bytes(str(contents_written_into), encoding='utf-16')
        elif choice == 3:
            exif_dict["0th"][40093] = bytes(str(contents_written_into), encoding='utf-16')
        elif choice == 4:
            exif_dict["0th"][40094] = bytes(str(contents_written_into), encoding='utf-16')
        elif choice == 5:
            exif_dict["0th"][40095] = bytes(str(contents_written_into), encoding='utf-16')
        # 防止意外
        else:
            exif_dict["0th"][40092] = bytes(str(contents_written_into), encoding='utf-16')

        # 转换为byte类型，适应下一步操作
        exif_bytes = piexif.dump(exif_dict)
        # 在原图片中写入指定的exif信息
        piexif.insert(exif_bytes,img_path_full)


        # 这个模块不需要重命名和cd操作
        # 修改后返回之前的目录，防止出错
        # os.chdir(currentPath)
    except Exception as e:
        print(e)
        return int(2)
    else:
        return int(0)


# 定义pyexiv2写exif函数
# pyexiv2库对路径中的中文和特殊字符支持很差，所以要手动cd到图片目录，重命名图片，改完exif以后还得恢复原样。
def pv2_write(img_path_full,choice,contents_written_into):
    try:
        # ★☆修改前记录当前文件夹的路径，顺带处理这个路径中的"\"★☆
        currentPath = os.getcwd().replace("\\\\","/")
        currentPath = currentPath.replace("\\","/")

        # 处理路径中的“\”
        img_path_full = img_path_full.replace("\\\\","/")
        img_path_full = img_path_full.replace("\\","/")

        # 检查文件是否存在
        status = os.path.exists(img_path_full)
        if status != True:
            raise Exception(str("图片文件路径：" + img_path_full + " 不存在"))

        # 获取路径
        img_path = os.path.dirname(img_path_full)
        # 获取文件名
        img_file_name = os.path.basename(img_path_full)

        # 相当于cmd命令里的"cd"命令
        if img_path == "":
            os.chdir(".")
        else:
            os.chdir(img_path)

        # 重命名操作，以适应pyexiv2模块的英文操作。
        os.rename(img_file_name,r'_target_.jpg')

        # 分配“句柄”
        i = pyexiv2.Image(r'_target_.jpg')


        # 根据写入选项，使用字典类型，预先分配好要修改的exif项
        # pyexiv2模块不需要用到utf-16编码，模块自身会打理好编码。
        if choice == 1:
            exif_dict = {'Exif.Image.XPTitle': str(contents_written_into)}
        elif choice == 2:
            exif_dict = {'Exif.Image.XPComment': str(contents_written_into)}
        elif choice == 3:
            exif_dict = {'Exif.Image.XPAuthor': str(contents_written_into)}
        elif choice == 4:
            exif_dict = {'Exif.Image.XPKeywords': str(contents_written_into)}
        elif choice == 5:
            exif_dict = {'Exif.Image.XPSubject': str(contents_written_into)}
        # 防止意外
        else:
            exif_dict = {'Exif.Image.XPComment': str(contents_written_into)}
        
        # 执行修改
        i.modify_exif(exif_dict)
        # 关闭“句柄”
        i.close

        # 重命名操作，把名字恢复成原来的
        os.rename(r'_target_.jpg',img_file_name)


        # ★☆修改后返回之前的目录，防止出错★☆
        os.chdir(currentPath)
    except Exception as e:
        print(e)
        return int(2)
    else:
        return int(0)




## 函数测试（自己测试需要改变下面的文件路径）
# pv1_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",1,"pv1_标题")
# pv1_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",2,"pv1_备注")
# pv1_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",3,"pv1_作者")
# pv1_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",4,"pv1_标记")
# pv1_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",5,"pv1_主题")
# os.system("pause")
# pv2_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",1,"pv2_标题")
# pv2_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",2,"pv2_备注")
# pv2_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",3,"pv2_作者")
# pv2_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",4,"pv2_标记")
# pv2_write("E:\【测试文件夹】㊙️❗️🌡️python修改图片exif中的标题和备注\测试.jpg",5,"pv2_主题")

# 默认的exe文件名
exe_filename = '\"win_exif_tag_writer.exe\"'

# 考虑到exe文件可能会被重命名，届时帮助里的exe文件名也可能需要跟着变化，所以增加exe_choice这个选项。
# 选项不通过命令行传递进来，需要在代码里手动更改。
# 固定exe文件名：0；可变exe文件名：1。
# 固定exe文件名可以加快速度，毕竟可变exe文件名需要搜索当前目录下的exe文件名。
exe_name_choice = 0

if exe_name_choice == 1:
    # 获取当前目录下所有项目到f_list
    f_list = os.listdir()
    for i in f_list:
        # 查找排在第一个的exe文件的文件名（就是本程序自身）
        if os.path.splitext(i)[1]  == '.exe':
            exe_filename = os.path.basename(i)
            break
    # 如果查找成功的话，在exe文件名两边加上英文双引号：""
    if exe_filename != '\"win_exif_tag_writer.exe\"':
        exe_filename = str('\"'+ exe_filename +'\"')


# print(exe_filename)


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    usage=str(
        "\n \n"+
        "========================================================================================================"+"\n"+
        "\n"+
        "介绍："+"\n"+
        "  本程序用以向jpg、tiff图片文件写入windows系统专属的exif标签。"+"\n \n"+
        "注意事项："+"\n"+
        "  1.本程序采用的是覆盖的方式对单个exif标签进行写入，被写入的exif标签之前的内容会被清除（如果exif能正确识别的话），"+"\n"+
        "    其他标签的值则会被保留，这点可以放心，不会一次性把所有其他标签全都擦除掉。"+"\n \n"+
        "  2.如果之前用windows自带的图片属性编辑工具，插入或修改过本程序帮助里提到的exif标签（尤其"+"\n"+
        "    是“标题”、“作者”、“标记”）,且标签里有文本内容的话，由于用windows自带工具写入的标签属性的exif格式"+"\n"+
        "    和本程序接受的格式有差异（表现在图片文件的二进制里，对比用本程序插入属性的图片，经过windows插入属性的图片"+"\n"+
        "    在图片文件头部会多出一大段空白和形似“<xxx>.....</xxx>”的类xml标签），所以用本程序有很大可能是直接覆盖不了"+"\n"+
        "    这些标签的内容的（表现在windows的图片文件属性里，此标签的值没有发生变化）。"+"\n"+
        "  【 我这边用一个jpg文件测试了一下，对原来有文本内容的标签，用此程序操作后，“标题”、“作者”标签的文本内容不变，"+"\n"+
        "     “标记”被追加了一个值，“备注”和“主题”则能够成功覆盖 】"+"\n \n"+
        "    ★☆ 所以建议对属性空白的图片使用该程序，比如刚刚生成或刚刚拍摄的图片；    ★☆"+"\n"+
        "    ★☆ 或者在写入标签前，用windows自带的工具或者其他工具（如“ExifCleaner”，★☆"+"\n"+
        "    ★☆    但是使用“ExifCleaner”会把所有的exif标签全删除掉），手动清除      ★☆"+"\n"+
        "    ★☆ 之前用windows自带工具插入的这些标签的值。                             ★☆"+"\n"+
        "  【 我这边用一个jpg文件测试了一下，用windows自带工具清除了windows工具自身之前写入的标签属性后，"+"\n"+
        "    是能够用此程序写入标签值的 】"+"\n \n"+
        "  3.是“2.”的补充说明：之前经过本程序操作的图片，只要不用windows自带的图片属性编辑工具进行编辑，"+"\n"+
        "    再次运行此程序后，是能够覆盖之前标签里的内容的。"+"\n \n"+
        "  4.程序支持从其他路径调用，以下面展示的cmd窗口示例为例："+"\n"+
        "\n"+
        "========================================================================================="+"\n"+
        " Microsoft Windows [版本 10.0.19044.1706]"+"\n"+
        " (c) Microsoft Corporation。保留所有权利。"+"\n \n"+
        " E:\\【存放图片的文件夹】> \"D:\\win_exif_tag_writer\\bin\\win_exif_tag_writer.exe\" -write \"123456_test\" -to \"1.jpg\" -tag \"标记\""+"\n \n"+
        "========================================================================================="+"\n"+
        "\n"+
        "  ★☆ 图片文件路径支持相对路径，如上面的例子所示。                                                        ★☆"+"\n"+
        "  ★☆ 所以完全可以将本程序的路径添加进系统环境变量“path”中。                                            ★☆"+"\n"+
        "  ★☆ 这样就能直接在cmd窗口中输入：\"win_exif_tag_writer.exe\" -write \"123456_test\" -to \"1.jpg\" -tag \"标记\" ★☆"+"\n \n \n \n \n"
    ),
    # epilog里，如果要表示换多个行，每两个换行符之间得加个空格才能识别，所以换行表示形式和其他部分不同。
    # description里也顺手写成“\n \n”了。
    description=str(
        "参数说明："+"\n"+
        "  本程序的命令行由4个主要参数组成，其中2个为必需参数，另外2个为可选参数。"+"\n"+
        "  还有一个获取帮助的参数\"-h\"（python库自带的）。"+"\n"+
        "  其中参数的说明如下方所示："+"\n"+
        "\n \n"
    ),
    epilog=str(
        "\n"+
        "命令行格式帮助："+"\n"+
        "  本程序的命令行格式十分灵活，同一个参数有很多可用的命令关键字，且所有参数的顺序可以互换。"+"\n"+
        "  下面仅展示个人推测在逻辑方面比较好理解，容易记住的几种格式方法。"+"\n \n"+
        "  “[ ]”里的是可选的参数，如果可选参数和必选参数一起组成的命令行是比较好记忆的，这个可选参数不会被“[ ]”括出；"+"\n"+
        "  “{ }”里的是从多个中选取一个，别漏看了大括号前面的“-”。"+"\n"+
        "\n \n"+
        "方法1："+"\n"+
        "      " + exe_filename + " " + "-write 【文本内容】 -{ to / to_file / to_img / to_jpg } 【图片文件路径】 [ -tag 【选中的exif标签名称、代号或编号】 -use 【用来进行写入操作的python库】 ]"+"\n"+
        "★☆ 注意！“-to”默认指定的是【图片文件路径】，不是【选中的exif标签名称、代号或编号】！  ★☆"+"\n"+
        "★☆ 如果需要指定标签，需要用“-to_tag”或“-tag”，总之要有\"tag\"字样。                   ★☆"+"\n"+
        "\n \n"+
        "方法2："+"\n"+
        "      " + exe_filename + " " + "-write 【文本内容】 -to_tag 【选中的exif标签名称、代号或编号】 -{ file / img / jpg } 【图片文件路径】 [ -use 【用来进行写入操作的python库】 ]"+"\n"+
        "\n \n"+
        "方法3："+"\n"+
        "      " + exe_filename + " " + "-{ i / file / img / jpg } 【图片文件路径】 -write 【文本内容】 -to_tag 【选中的exif标签名称、代号或编号】 [ -use 【用来进行写入操作的python库】 ]"+"\n"+
        "\n \n"+
        "方法4："+"\n"+
        "      " + exe_filename + " " + "-{ i / file / img / jpg } 【图片文件路径】 -{ tag / write_tag } 【选中的exif标签名称、代号或编号】 -{ content / text / string } 【文本内容】 [ -use 【用来进行写入操作的python库】 ]"+"\n"+
        "\n \n \n \n"+
        "示例："+"\n"+
        "(1)" +"\n"+
        "  " + exe_filename + " " + "-write \"abcdefg_test\" -to \"E:\\folder\\path\\file.jpg\""+"\n"+
        "说明：将文本内容\"abcdefg_test\"写入到文件\"E:\\folder\\path\\file.jpg\"的exif标签“备注”中，"+"\n"+
        "      没有\"-tag\"参数的情况下，程序默认选择的是“备注”。"+"\n"+
        "★☆ 注意！“-to”默认指定的是【图片文件路径】，不是【选中的exif标签名称、代号或编号】！  ★☆"+"\n"+
        "★☆ 如果需要指定标签，需要用“-to_tag”或“-tag”，总之要有\"tag\"字样。                   ★☆"+"\n"+
        "\n \n"+
        "(2)" +"\n"+
        "  " + exe_filename + " " + "-write \"abcdefg_\" -to_tag \"5\" -img \"relative_path\\file.jpg\""+"\n"+
        "说明：将文本内容\"abcdefg_\"写入到文件\"relative_path\\file.jpg\"的exif标签“主题”中，"+"\n"+
        "      查前面的参数说明，可知“5”对应的是“主题”。"+"\n"+
        "★☆ 可以使用相对路径 ★☆"+"\n"+
        "\n \n"+
        "(3)" +"\n"+
        "  " + exe_filename + " " + "-write \"2023-01-01 00:00:01\" -to \"E:\\folder\\path\\file.jpg\" -tag \"标记\""+"\n"+
        "说明：将文本内容\"2023-01-01 00:00:01\"写入到文件\"E:\\folder\\path\\file.jpg\"的exif标签“标记”中。"+"\n"+
        "\n \n"+
        "(4)" +"\n"+
        "  " + exe_filename + " " + "-img \"D:\\folder\\test.jpg\" -write \"123456\" -to_tag \"40093\""+"\n"+
        "说明：将文本内容\"123456\"写入到文件\"D:\\folder\\test.jpg\"的exif标签“作者”中，"+"\n"+
        "      查前面的参数说明，可知“40093”对应的是“作者”。"+"\n"+
        "\n \n"+
        "(5)" +"\n"+
        "  " + exe_filename + " " + "-i \"D:\\folder\\test.jpg\" -write_tag \"XPTitle\" -text \"123456\" [ -use \"pyexiv2\" ]"+"\n"+
        "说明：将文本内容\"123456\"写入到文件\"D:\\folder\\test.jpg\"的exif标签“标题”中，"+"\n"+
        "      查前面的参数说明，可知“XPTitle”对应的是“作者”。"+"\n"+
        "      \"-i\"也是ffmpeg的导入文件命令，用过ffmpeg的比较好适应，所以加了这个\"-i\"进来；"+"\n"+
        "      进行写入操作的是python的pyexiv2库。"+"\n \n"+
        "   【 注：默认情况下用的是另一个piexif库，"+"\n"+
        "      只有使用\"-use\"参数（前面提到的“参数四”），"+"\n"+
        "      且指定为pyexiv2，才会转为用pyexiv2库 】"+"\n"+
        "// 个人建议使用程序默认的python库piexif，也就是如果不需要调整这项设置，不需要加这个参数。//"+"\n \n \n"+
        "========================================================================================================"+"\n \n \n"
    ),
)

    # 接收被写入图片的路径
parser.add_argument(
	##——————————
	# # # # #
	"-i","-I","--i","--I",
	# # # # #
    "-to","-TO","-To",
    "--to","--TO","--To",
	# # #
    "-file","-FILE","-File",
    "--file","--FILE","--File",
	# # #
    "-to_file","-TO_FILE","-To_File",
    "--to_file","--TO_FILE","--To_File",
	"-to-file","-TO-FILE","-To-File",
    "--to-file","--TO-FILE","--To-File",
	# # #
    "-img","-IMG","-Img",
    "--img","--IMG","--Img",
	# # #
	"-to_img","-TO_IMG","-To_Img",
    "--to_img","--TO_IMG","--To_Img",
	"-to-img","-TO-IMG","-To-Img",
    "--to-img","--TO-IMG","--To-Img",
	# # #
    "-jpg","-JPG","-jpg",
    "--jpg","--JPG","--jpg",
	# # #
	"-to_jpg","-TO_JPG","-To_Jpg",
    "--to_jpg","--TO_JPG","--To_Jpg",
	"-to-jpg","-TO-JPG","-To-Jpg",
    "--to-jpg","--TO-JPG","--To-Jpg",
	# # #
	##——————————
    # metavar="【图片文件路径】",,加上的话看起来太乱。
    dest="file",type=str,default=None,
    help=str(
            "\n"+
			"参数一、指定图片文件路径（必要的命令关键字！）："+"\n"+
			"\n"+
            "格式：【参数命令关键字】+[空格]+【图片文件路径】"+"\n"+
            "上面列出的命令关键字均可使用，字母不区分大小写。"+"\n"+
            "\n"+
            "★☆【图片文件路径】支持相对路径。★☆"+"\n"+
            "\n"+
            "举例，指定内容所写入到的exif项目名称（标题）："+"\n"+
            "  1. -i \"D:\\123\\456.jpg\" "+"\n"+
            "  2. -to \"D:\\123\\456.jpg\" "+"\n"+
            "  3. -img \"folder\\test.jpg\" "+"\n"+
            "  4. -file \"D:\\123\\456.jpg\" "+"\n"+
			"\n"+
            "{建议给输入的路径前后加上英文双引号\"\"，命令关键字可不加\"\"。}"+"\n"
            +"\n\n\n\n\n"
            )
)

# 接收写入到这个exif标签里的文本内容
parser.add_argument(
	##——————————
	# # # # #
    "-write","-WRITE","-Write",
    "--write","--WRITE","--Write",
	# # #
    "-content","-CONTENT","-Content",
    "-text","-TEXT","-Text",
    "-string","-STRING","-String","-str","-STR","-Str",
	# # #
    "--content","--CONTENT","--Content",
    "--text","--TEXT","--Text",
    "--string","--STRING","--String","--str","--STR","--Str",
	# # #
	##——————————
    # metavar="【文本内容】",加上的话看起来太乱。
    dest="content",type=str,default=None,
    help=str(
            "\n"+
			"参数二、指定写入到exif标签里的文本内容（必要的命令参数！）："+"\n"+
			"\n"+
            "格式：【参数命令关键字】+[空格]+【文本内容】"+"\n"+
            "上面列出的命令关键字均可使用，字母不区分大小写。"+"\n"+
            "\n"+
            "所有输入的文本内容有且仅有一个字符串。"+"\n"+
            "\n"+
            "举例："+"\n"+
            "1. -content \"123456测试\" "+"\n"+
            "2. --text \"123456\" "+"\n"+
            "3. -write \"2023-01-01 00:00:01\" "+"\n"+
            "4. --string \"abcdefgh\" "+"\n"+
            "\n"+
            "{建议给输入的内容前后加上英文双引号\"\"，命令关键字可不加\"\"。}"+"\n"
            +"\n\n\n\n\n"
            )
)

# 接收exif的标签名
parser.add_argument(
	##——————————
	# # # # #
    "-tag","-TAG","-Tag",
    "--tag","--TAG","--Tag",
	# # #
    "-write_tag","-WRITE_TAG","-Write_Tag",
    "-write-tag","-WRITE-TAG","-Write-Tag",
	# # #
    "--write_tag","--WRITE_TAG","--Write_Tag",
    "--write-tag","--WRITE-TAG","--Write-Tag",
	# # #
    "-to_tag","-TO_TAG","-To_Tag",
    "-to-tag","-TO-TAG","-To-Tag",
	# # #
    "--to_tag","--TO_TAG","--To_Tag",
    "--to-tag","--TO-TAG","--To-Tag",
	# # #
	##——————————
    # metavar="【选中的exif标签名称、代号或编号】",,加上的话看起来太乱。
    dest="tag",type=str,default="2",
    help=str(
            "\n"+
			"参数三、指定文本内容所写入到的exif标签的名称（可选，非必要的命令参数）："+"\n"+
			"\n"+
            "格式：【参数命令关键字】+[空格]+【选中的exif标签名称、代号或编号】"+"\n"+
            "上面列出的命令关键字均可使用，字母不区分大小写。"+"\n"+
            "\n"+
            "下面列出的是每一类标签所对应的名称、代号或编号的可用值，输入值用“【】”括出。"+"\n"+
            "标题:【标题】、【1】、【40091】、【Title】、【XPTitle】；"+"\n"+
            "备注:【备注】、【2】、【40092】、【Comment】、【XPComment】；"+"\n"+
            "作者:【作者】、【3】、【40093】、【Author】、【XPAuthor】；"+"\n"+
            "标记:【标记】、【4】、【40094】、【Keywords】、【XPKeywords】；"+"\n"+
            "主题:【主题】、【5】、【40095】、【Subject】、【XPSubject】。"+"\n"+
            "\n"+
            "举例，指定文本内容所写入到的exif标签为【标题】："+"\n"+
            "  1. -write_tag \"标题\" "+"\n"+
            "  2. --write_tag \"Title\" "+"\n"+
            "  3. -tag \"标题\" "+"\n"+
            "  4. --tag \"1\" "+"\n"+
            "  5. -to_tag \"40091\" "+"\n"+
            "  6. --to_tag \"XPTitle\" "+"\n"+
			"\n"+
			"★☆ 注意！如果没有这个参数，默认情况下，程序会选择：【备注】 ★☆"+
			"\n"+
            "{建议给输入的内容前后加上英文双引号\"\"，命令关键字可不加\"\"。}"+"\n"
            +"\n\n\n\n\n"
            )
)


# 接收用来操作的python库的选项
parser.add_argument(
	##——————————
	# # # # #
    "-use","-USE","-Use",
    "--use","--USE","--Use",
	# # #
    "-lib","-LIB","-Lib",
    "--lib","--LIB","--Lib",
	# # #
    "-use_lib","-USE_LIB","-Use_Lib",
    "--use-lib","--USE-LIB","--Use-Lib",
	# # #
	##——————————
    # metavar="【1 / p1 / pie / pi / piexif / ……】",加上的话看起来太乱。
    dest="lib",type=str,default="1",
    help=str(
            "\n"+
			"参数四、指定用来进行写入操作的python库，相当于模式切换（可选，非必要的命令参数）："+"\n"+
			"\n"+
            "格式：【参数命令关键字】+[空格]+【用来进行写入操作的python库】"+"\n"+
            "上面列出的命令关键字均可使用，字母不区分大小写。"+"\n"+
            "\n"+
            "下面列出的是每一个python库所对应的可用输入值，输入值用“【】”括出。"+"\n"+
            "piexif: 【1】、【p1】、【pie】、【pi】、【piexif】；"+"\n"+
            "pyexiv2:【2】、【p2】、【pye】、【py】、【pyexiv2】、【py2】。"+"\n"+
            "\n"+
            "举例："+"\n"+
            "1. -use \"2\" "+"\n"+
            "2. --lib \"p2\" "+"\n"+
            "3. -use \"pyexiv2\" "+"\n"+
            "4. --use_lib \"pie\" "+"\n"+
            "\n"+
            "{建议给输入的内容前后加上英文双引号\"\"，命令关键字可不加\"\"。}"+"\n"+
            "\n"+
            "个人建议使用程序默认的python库piexif，也就是如果不需要调整这项设置，不需要加这个参数。"+"\n"
            +"\n\n\n\n\n"
            )
)
# 开始解析
args = parser.parse_args()

# 如果argparse模块接收到“-h”获取帮助指令，就会退出，代码不会运行到这里。
# 命令行接收参数测试
# print(args.file)
# print(args.content)
# print(args.tag)
# print(args.lib)

## 分析传过来的参数
# 检查是否缺少参数，并传递值
if (args.file == None) or (args.content == None):
    print("未指定【图片文件路径】或写入的【文本内容】")
    sys.exit(1)
else:
    input_file = args.file
    input_content = args.content

# 检查并传递tag
if   ((args.tag == "标题") or (args.tag == "1") or 
    (args.tag == "40091") or (args.tag.lower() == "title") or (args.tag.lower() == "xptitle")):
    input_tag = int(1)
elif ((args.tag == "备注") or (args.tag == "2") or 
    (args.tag == "40092") or (args.tag.lower() == "comment") or (args.tag.lower() == "xpcomment")):
    input_tag = int(2)
elif ((args.tag == "作者") or (args.tag == "3") or 
    (args.tag == "40093") or (args.tag.lower() == "author") or (args.tag.lower() == "xpauthor")):
    input_tag = int(3)
elif ((args.tag == "标记") or (args.tag == "4") or 
    (args.tag == "40094") or (args.tag.lower() == "keywords") or (args.tag.lower() == "xpkeywords")):
    input_tag = int(4)
elif ((args.tag == "主题") or (args.tag == "5") or 
    (args.tag == "40095") or (args.tag.lower() == "subject") or (args.tag.lower() == "xpsubject")):
    input_tag = int(5)
else:
    print("参数【选中的exif标签名称、代号或编号】指定错误")
    sys.exit(1)

# 检查并传递lib
if   ((args.lib == "1") or (args.lib.lower() == "p1") or 
    (args.lib.lower() == "pie") or (args.lib.lower() == "pi") or (args.lib.lower() == "piexif")):
    input_lib = int(1)
elif ((args.lib == "2") or (args.lib.lower() == "p2") or (args.lib.lower() == "py2")
    (args.lib.lower() == "pye") or (args.lib.lower() == "py") or (args.lib.lower() == "pyexiv2")):
    input_lib = int(2)
else:
    print("参数【用来进行写入操作的python库】指定错误")
    sys.exit(1)


# 传入函数参数，这里因为是需要cmd命令行传入，所以这么写。
# 如果移植到你的python源代码里，这里就是填写传递给函数参数的地方。
img_path_full = input_file
choice = input_tag
contents_written_into = input_content


# 根据选择的python库执行写入
if input_lib == 1:
    errorlevel = pv1_write(img_path_full,choice,contents_written_into)
else:
    errorlevel = pv2_write(img_path_full,choice,contents_written_into)

if errorlevel != 0:
    print(str(img_path_full + "  运行错误"))

sys.exit(int(errorlevel))