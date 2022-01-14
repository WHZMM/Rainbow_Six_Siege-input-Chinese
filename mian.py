import keyboard
import ctypes
from time import sleep
from time import localtime
from time import strftime
import sys
import tkinter


SendInput = ctypes.windll.user32.SendInput


PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


def press_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
#


# scan code of keys on num keyboard
key_code = {'0': 0x52,
            '1': 0x4F, '2': 0x50, '3': 0x51,
            '4': 0x4B, '5': 0x4C, '6': 0x4D,
            '7': 0x47, '8': 0x48, '9': 0x49}

key_code_2_keys = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g",
                   "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n",
                   "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t",
                   "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z",
                   "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+",
                   "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
                   "{", "}", r"|", ":", '"', "<", ">", "?",
                   "[", "]", "\\", ";", "'", ",", ".", "/",
                   " "]

hot_keys = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]  # 可以设定的hot_keys

ban_words = ["操你妈", "你妈逼", ]

cfg = {"hotkey": "f8", "bg": r"D:\bg.jpg", "-alpha": 1.0}  # 默认配置

cfg_bd = 1  # 边框大小，默认为2
cfg_bd_zero = 0  # 边框大小，应该是0，debug时候设为非0
cfg_bg = "#edeadb"  # 背景 ed ea db = 237 234 219
cfg_fg = "#7d7a6b"  # 字体颜色
cfg_sbg = "#66CCFF"  # 选中部分的背景
cfg_color_rim = "#dddacb"  # 边框颜色 "#dddacb"
cfg_clean = False  # 如果是True，不显示我用于宣传的话

str_in = ""
last_valid_str = ""
char_in = []
last_valid_char = []


def input_a_char(input1):   # 输入是字符的GB2312编码，以int的形式
    char_str = str(input1)
    press_key(0x38)  # L-alt: 0x38, R-alt: 0xb8
    for key in char_str:
        press_key(key_code[key])
        release_key(key_code[key])
        sleep(0.001)
    release_key(0x38)  # L-alt: 0x38, R-alt: 0xb8


def input_words():
    keyboard.remove_hotkey(cfg["hotkey"])  # without this, type too many times
    check_words()
    global last_valid_char
    for char_in_func in last_valid_char:  # char, "GB2312 code in the form of int" or "key in the form of str"
        if isinstance(char_in_func, str):  # 如果是字符串，就不用GB2312了
            keyboard.write(char_in_func)
            sleep(0.01)
            continue
        input_a_char(char_in_func)  # 用GB2312输入
    win_text_3.insert(tkinter.END, "\n" + time_str() + " 游戏内输入完成")
    win_text_3.see("end")
    sleep(0.5)  # time between two times of type, need to adjust, maybe 1s ?
    keyboard.add_hotkey(cfg["hotkey"], input_words, args=(), suppress=False)


def check_words():  # read input and store to char_in  # input 的时候不应该再次输出check结果
    read_from_text_1 = win_text_1.get(1.0, 'end')
    read_from_text_1 = read_from_text_1.split('\n')
    if read_from_text_1[-2] != "":  # 如果最后没有回车，那就加个回车
        win_text_1.insert(tkinter.END, '\n')
    # temp1 = win_text_1.get(1.0, 'end').split('\n')

    for _ in range(read_from_text_1.count('')):    # 删掉空白行，可以优化？
        read_from_text_1.remove('')
    if len(read_from_text_1) == 0:
        # print('空白输入')
        win_text_3.insert(tkinter.END, "\n" + time_str() + " 空白输入")
        win_text_3.see("end")
        return 0
    global str_in
    global last_valid_str
    global char_in
    global last_valid_char
    char_in = []
    str_in = read_from_text_1[-1]  # 只管最后一行
    except_or_not = 0

    for ban_word in ban_words:  # 如果检测到屏蔽的关键词，视为异常
        if ban_word in str_in:
            except_or_not = 1
            win_text_3.insert(tkinter.END, "\n" + time_str() + " 要谨言慎行！不要说不该说的话！")
            win_text_3.see("end")
            break

    for char in str_in:     # char, character in the form of str
        if char in key_code_2_keys:  # 如果不需要用GB2312code，直接把字符串放入char_in
            char_in.append(char)
            continue
        try:
            char_bytes = char.encode("GB2312")
        except UnicodeEncodeError:
            except_or_not = 1
            char_in.append(0)
            win_text_3.insert(tkinter.END, "\n" + time_str() + " 你输入的{}不能用GB2312表示".format(char))
            win_text_3.see("end")
        else:
            char_in.append(int.from_bytes(char_bytes, byteorder='big', signed=False))

    if except_or_not:  # 检查不通过
        win_text_3.insert(tkinter.END, "\n" + time_str() + " 检查不通过，请重新输入".format((cfg["hotkey"]).upper(), last_valid_str))
        win_text_3.see("end")
        return -1
    else:
        last_valid_str = str_in
        last_valid_char = char_in.copy()
        win_text_2.delete("1.0", "end")
        win_text_2.insert("end", last_valid_str)
        win_text_3.insert(tkinter.END, "\n" + time_str() + " 检查通过")
        win_text_3.see("end")
        return 0


def clean():  # 清空框框和记录
    win_text_1.delete("1.0", "end")
    win_text_2.delete("1.0", "end")
    win_text_3.delete("1.0", "end")
    global str_in
    global last_valid_str
    global char_in
    global last_valid_char
    str_in = ""
    last_valid_str = ""
    char_in = []
    last_valid_char = []


def time_str():  # 获取时间字符串
    return strftime("%H:%M:%S", localtime())


error_words = list()  # 暂存需要在UI界面运行状态处打印的报错内容

sys_argv = sys.argv
# 参数： 设置热键 背景图片路径 窗口大小位置
# 例如： 热键=F8 不透明度=

path = sys_argv[0]
path = path.replace("/", "\\")
path = (path.rsplit("\\", 1))[0] + "\\tk\\images\\12.1\\"
path_icon = path + "icon.ico"  # 窗口图标路径
path_img_0 = path + "img-0.gif"  # 背景图片路径
path_img_1 = path + "img-1.gif"  #
path_img_2 = path + "img-2.gif"  #
path_img_3 = path + "img-3.gif"  #
# path_img_4 = path + "img-4.gif"  #
# path_img_5 = path + "img-5.gif"  #
# path_img_6 = path + "img-6.gif"  #
# path_img_7 = path + "img-7.gif"  #
# path_img_8 = path + "img-8.gif"  #
# path_img_9 = path + "img-9.gif"  #

for argv in sys_argv[1:]:  # 第一个是进程本身，直接跳过了
    if argv.startswith("热键="):
        argv = argv[3:]
        if argv.lower() in hot_keys:
            cfg["hotkey"] = argv.lower()
            # print("热键已设置为{}".format(argv.upper()))
            error_words.append("热键已设置为{}".format(argv.upper()))  # 0为普通颜色
        else:
            # print("不支持你设定的热键{}，目前仅支持F1至F12，已经设定为默认值F8".format(argv))
            error_words.append( "不支持你设定的热键{}，目前仅支持F1至F12，已经设定为默认值F8".format(argv))  # 1为报错颜色
    elif argv.startswith("不透明度="):
        argv = argv[5:]
        try:
            argv = float(argv)
        except ValueError:
            # print("不支持你设定的不透明度，不透明度应该大于0、小于等于1")
            error_words.append( "不支持你设定的不透明度，不透明度应该大于0、小于等于1")
        else:
            cfg["-alpha"] = argv
    elif argv == "文字颜色=1":
        cfg_fg = "#6d6a5b"  # 字体颜色
    elif argv == "文字颜色=2":
        cfg_fg = "#5d5a4b"  # 字体颜色
    elif argv == "文字颜色=3":
        cfg_fg = "#4d4a3b"  # 字体颜色
    elif argv == "清空":
        cfg_clean = True  #
    else:
        # print("无效的参数设定：{}".format(argv))
        error_words.append((1, "无效的参数设定：{}".format(argv)))


keyboard.add_hotkey(cfg["hotkey"], input_words, args=(), suppress=False)

main_win = tkinter.Tk()
main_win.title("彩虹六号围攻 中文输入法        by: WHZ_MM (B站 ID)    by: Admimistrator (R6 ID)    若在游戏内遇到我，打个招呼可好？")
main_win.geometry('960x540+0+0')  # 初始窗口大小，位置
main_win.iconbitmap(path_icon)  # 窗口左上角icon
main_win.resizable(False, False)  # 窗口大小锁定
main_win["bg"] = "#FFFFFF"  # 窗口背景色
main_win.attributes("-alpha", cfg["-alpha"])  # 透明度

img_0 = tkinter.PhotoImage(file=path_img_0)  # 背景
background_label = tkinter.Label(main_win, image=img_0)
background_label.place(x=0, y=0)

# 输入框-标题
win_label_1 = tkinter.Label(main_win, text="在此处输入：", font=('宋体', 18, 'bold'), bg=cfg_bg, fg=cfg_fg, bd=cfg_bd_zero, anchor="nw")
win_label_1.place(x=10, y=10, width=250, height=30)

# 输入框
win_text_1 = tkinter.Text(main_win, bg=cfg_bg, font=('宋体', 18, 'bold'), fg=cfg_fg, selectbackground=cfg_sbg, bd=cfg_bd_zero, relief="ridge")
win_text_1.place(x=10, y=37, width=583, height=241)

# 当前打字内容-标题
win_label_2 = tkinter.Label(main_win, text="当前按{}打字内容：".format(cfg["hotkey"].upper()), font=('宋体', 18, 'bold'), bg=cfg_bg, fg=cfg_fg, bd=cfg_bd_zero, anchor="nw")
win_label_2.place(x=10, y=288, width=250, height=30)

# 当前打字内容显示框
win_text_2 = tkinter.Text(main_win, height=2, bg=cfg_bg, font=('宋体', 12, 'bold'), fg=cfg_fg, selectbackground=cfg_sbg, bd=cfg_bd_zero, relief="ridge")
win_text_2.place(x=10, y=315, width=515, height=55)

# 运行状态-标题
win_label_3 = tkinter.Label(main_win, text="运行状态：", font=('宋体', 18, 'bold'), bg=cfg_bg, fg=cfg_fg, bd=cfg_bd_zero, anchor="nw")
win_label_3.place(x=10, y=380, width=250, height=30)

# 运行状态-内容
win_text_3 = tkinter.Text(main_win, height=100, bg=cfg_bg, font=('宋体', 18, 'bold'), fg=cfg_fg, selectbackground=cfg_sbg, bd=cfg_bd_zero, relief="ridge")
win_text_3.place(x=10, y=407, width=515, height=123)

# 2B按钮 用来清除
img_1 = tkinter.PhotoImage(file=path_img_1)  #
win_button_clean_1 = tkinter.Button(main_win, command=clean, bd=cfg_bd_zero, relief="flat", image=img_1)
win_button_clean_1.place(x=689+2, y=35+2, width=64, height=64)  # +2是因为tk的坐标和画图的坐标有偏移

# A2按钮 用来检查
img_2 = tkinter.PhotoImage(file=path_img_2)  #
win_button_check_1 = tkinter.Button(main_win, command=check_words, bd=cfg_bd_zero, relief="flat", image=img_2)
win_button_check_1.place(x=815+2, y=172+2, width=56, height=56)  # +2是因为tk的坐标和画图的坐标有偏移

# 按键提示
win_label_4 = tkinter.Label(main_win, text="点击2B头部进行清空\n点击A2头部进行检查", font=('宋体', 8, 'bold'), bg="#000000", fg="#383838", bd=cfg_bd_zero, anchor="nw")
win_label_4.place(x=847, y=516, width=113, height=24)

win_rim_1 = tkinter.Label(main_win, bg=cfg_color_rim, bd=0, anchor="nw")
win_rim_1.place(x=10, y=37, width=583, height=1)
win_rim_2 = tkinter.Label(main_win, bg=cfg_color_rim, bd=0, anchor="nw")
win_rim_2.place(x=10, y=277, width=583, height=1)
win_rim_3 = tkinter.Label(main_win, bg=cfg_color_rim, bd=0, anchor="nw")
win_rim_3.place(x=10, y=315, width=515, height=1)
win_rim_4 = tkinter.Label(main_win, bg=cfg_color_rim, bd=0, anchor="nw")
win_rim_4.place(x=10, y=369, width=515, height=1)
win_rim_5 = tkinter.Label(main_win, bg=cfg_color_rim, bd=0, anchor="nw")
win_rim_5.place(x=10, y=407, width=515, height=1)
win_rim_6 = tkinter.Label(main_win, bg=cfg_color_rim, bd=0, anchor="nw")
win_rim_6.place(x=10, y=529, width=515, height=1)

if not cfg_clean:
    win_text_1.insert("end", '在此输入你想在游戏内发送的内容，点击A2头部进行检查，检查通过后，在彩虹六号围攻的打字界面按{}即可。'.format(cfg["hotkey"].upper()))
    win_text_1.insert("end", '\n\n如果你确信你输入的内容可以用GB2312编码表示，则可跳过检查的步骤，直接在彩虹六号围攻的打字界面按{}即可。'.format(cfg["hotkey"].upper()))
    win_text_1.insert("end", '\n\n点击2B的头部进行清空，点击A2的头部进行检查。\n')

welcome_words = ["最新的输入法和黑名单在这里：\n",
                 "链接：https://pan.baidu.com/s/1TYThOskPb-dwFgnyuGeJyg (提取码：WuHZ)\n",
                 "名单里主要是辱华玩家，请帮我完善此名单！"]
if len(error_words) == 0 and not cfg_clean:
    for temp_print in welcome_words:
        win_text_3.insert(tkinter.END, temp_print)
else:
    for temp_print in error_words:
        win_text_3.insert(tkinter.END, "\n" + temp_print)
win_text_3.see("end")

main_win.mainloop()
