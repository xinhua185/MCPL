#codeing=gbk
import tkinter.ttk as tk
import tkinter.messagebox as msgbox
from subprocess import *
from PIL import ImageTk
import os,easygui,json
from sys import argv
import psutil
window = tk.tkinter.Tk()
load=tk.Label(window,text="加载中")
load.pack()
memory = psutil.virtual_memory()
maxmon=int(round(( float(memory.total) / 1024 / 1024), 2))
#读取启动信息
# #之后改成json
# try:
#     with open('version.txt') as temp:
#         config["start"]=temp.read()
# except:
#     config["start"]=""
# try:
#     with open('config["minecraftpath"].txt','r') as temp:
#         config["minecraftpath"]=temp.read()
# except:
#     config["minecraftpath"]=""
# try:
#     with open('java.txt') as temp:
#         config["javapath"]=temp.read()
# except:
#     config["javapath"]=""
# try: 
#     with open('config["lastpath"].txt') as temp:
#         config["lastpath"]=int(temp.read())
# except:
#     config["lastpath"]=""
# try:
#     with open('memset.txt') as temp:
#         config["maxmem"]=int(temp.read())
# except:
#     config["maxmem"]=maxmon
try:
    with open('mcpl.json','r') as temp:
      config=json.load(temp) 
except:
    #默认配置
    config={
        "sd_mode":"启动后关闭",
        "start":"",
        "javapath":"",
        "version":"",
        "minecraftpath":"",
        "lastpath":"",
        "maxmem":maxmon
    }
officalpath=os.path.join(os.environ.get("USERPROFILE"),"AppData","Roaming",".minecraft")
targetpath=os.path.join(os.getcwd(),".minecraft")
parent = os.path.dirname(os.path.realpath(__file__))
icon_path = parent + '/MCPL.ico'
window.resizable(0, 0)
window.iconbitmap(icon_path)
window.title('MCPL')
bg = ImageTk.PhotoImage(file='bg.png')
bgLabel = tk.Label(window,image=bg)
load.forget()
bgLabel.pack()
def javaSet():
    global jpathbtn
    if config["javapath"]=='':
        if msgbox.askyesno('警告','该计算机未安装Java,是否安装?'):
            os.system('www.java.com/zh-CN/download/manual.jsp')
    temp=easygui.diropenbox('选择Java安装路径')
    if temp!=None:
        config["javapath"]=temp
        jpathbtn.config(text='当前Java路径为:'+config["javapath"])
try:
    versionsList=os.listdir(config["minecraftpath"]+'/versions')
except:
    try:
        os.makedirs(config["minecraftpath"]+'/versions')
        os.mkdir(config["minecraftpath"]+'/mods')
    except:
        pass
gamedirvar=tk.tkinter.IntVar()
memvar=tk.tkinter.StringVar()
memsca=None
def monset(c):
    global memvar
    config["maxmem"]=int(float(c))
    memvar.set(config["maxmem"])
jpathbtn=None
sdbtn=None
def checkentry():
    global memvar
    print(memvar.get())
    if(memvar.get().isdigit()):
        temp=int(memvar.get())
        if(temp>=0):
            config["maxmem"]=temp
            memsca.set(config["maxmem"])
            return True
        else:
            memvar.set(str(config["maxmem"]))
            return False
    else:
        memvar.set(str(config["maxmem"]))
        return False
gamedirbtn=[]
def Settings():
    global gamedirvar,jpathbtn,sdbtn,launcherSetwindow,memvar,memsca,gamedirbtn
    gamedirvar.set(config["lastpath"])
    gamedirs=['官方启动器目录('+officalpath+')','当前目录('+targetpath+')','自定义路径:('+config["minecraftpath"]+')']
    launcherSetwindow=tk.tkinter.Toplevel(window)
    launcherSetwindow.resizable(0,0)
    launcherSetwindow.title('设置')
    launcherSetwindow.iconbitmap(icon_path)
    jpathbtn=tk.Button(launcherSetwindow,text='当前Java路径为:'+config["javapath"],command=javaSet)
    jpathbtn.pack()
    tk.Label(launcherSetwindow,text='游戏目录').pack()
    index=0
    for i in gamedirs:
        gamedirbtn.append(tk.Radiobutton(launcherSetwindow, variable=gamedirvar, text=i, value=index,command=minecraftpathSet))
        gamedirbtn[index].pack()
        index+=1
    tk.Label(launcherSetwindow,text='当前分配内存(MB):').pack()
    tk.Entry(launcherSetwindow,textvariable=memvar,validate='focusout',validatecommand=checkentry,invalidcommand=(lambda:msgbox.showerror("错误","请输入一个正整数"))).pack()
    memvar.set(str(config["maxmem"]))
    memsca=tk.Scale(launcherSetwindow, from_=0, to=maxmon, orient=tk.tkinter.HORIZONTAL,length=1000, command=monset)
    memsca.pack()
    memsca.set(config["maxmem"])
    sdbtn=tk.Button(launcherSetwindow,text='启动器可见性:'+config["sd_mode"],command=windowSet)
    sdbtn.pack()
def windowSet():
    global sdbtn,versionsList
    temp=easygui.buttonbox('启动器可见性','',['启动后关闭','启动后隐藏','保持可见'])
    if temp!=None:
        config["sd_mode"]=temp
        sdbtn.config(text='启动器可见性:'+config["sd_mode"])
def minecraftpathSet():  
    global versionsList,gamedirs,gamedirbtn
    config["lastpath"]=gamedirvar.get()
    if config["lastpath"]==0:
        config["minecraftpath"]=officalpath
    elif config["lastpath"]==2:
        config["minecraftpath"]=easygui.diropenbox()
    elif config["lastpath"]==1:
        config["minecraftpath"]=targetpath
    try:
        versionsList=os.listdir(config["minecraftpath"]+'/versions')
    except:
        try:
            os.makedirs(config["minecraftpath"]+'/versions')
            os.mkdir(config["minecraftpath"]+'/mods')
        except:
         pass
    gamedirs=['官方启动器目录('+officalpath+')','当前目录('+targetpath+')','自定义路径:('+config["minecraftpath"]+')']
    index=0
    for i in gamedirbtn:
        i.config(text=gamedirs[index])
        index+=1
def set():
    file_path = os.path.join(config["minecraftpath"],"mods")  #文件路径
    path_list = os.listdir(file_path) #遍历整个文件夹下的文件name并返回一个列表
    get_modList = []#定义一个空列表
    a=[]
    b=[]
    for i in get_modList:
        if i.split('.jar')[1]=='disabled':           
            a.append(i)
        else:
            b.append(i)
def run(): 
    #启动函数
    ###启动命令###
    
    ###
    if config["sd_mode"]=='启动后关闭':
        exit()
    elif config["sd_mode"]=='启动后隐藏':
        pass
    else:
        return
bgLabel=tk.Label(window,text=config["start"])
bgLabel.pack()
def versionsListWindow():
    global bgLabel
    if(len(versionsList)==0):
        msgbox.showerror('错误','未下载任何版本')
        return
    config["start"]=easygui.choicebox('选择一个版本','版本列表',versionsList)
    bgLabel.forget()
    bgLabel = tk.Label(window,text=config["start"])
    bgLabel.pack()
launcherSetBtn = tk.Button(window, text='\n设置\n',command=Settings)
launcherSetBtn.place(x=0, y=0)
runBtn = tk.Button(window, text='\n启动\n',command=run)
runBtn.place(x=969, y=550)
downloadBtn = tk.Button(window, text='\n下载\n',command=(lambda:os.popen('pythonw download.pyw')))
downloadBtn.place(x=0, y=170)
versionslistBtn= tk.Button(window, text='\n版本列表\n',command=versionsListWindow)
versionslistBtn.place(x=0, y=100)
setBtn = tk.Button(window, text='\n模组管理\n',command=set)
setBtn.place(x=969, y=0)
window.mainloop()
###保存设置
# with open('config["minecraftpath"].txt','w') as temp:
#     temp.write(config["minecraftpath"])
# with open('config["lastpath"].txt','w') as temp:
#     temp.write(str(config["lastpath"]))
# with open('java.txt','w') as temp:
#     temp.write(config["javapath"])
# with open('version.txt','w') as temp:
#     temp.write(config["start"])
# with open('memset.txt','w') as temp:
#     temp.write(str(config["maxmem"]))
with open('mcpl.json','w') as temp:
    json.dump(config,temp)
