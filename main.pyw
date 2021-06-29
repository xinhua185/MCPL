#codeing=gbk
import tkinter.ttk as tk
import tkinter.messagebox
from subprocess import *
from PIL import Image, ImageTk
import os,easygui,time,json,logging
from sys import argv
logging.basicConfig(level=logging.NOTSET) 
with open('version.txt') as temp:
    start=temp.read()
parent = os.path.dirname(os.path.realpath(__file__))
icon_path = parent + '/MCPL.ico'
window = tk.tkinter.Tk()
window.resizable(0, 0)
window.iconbitmap(icon_path)
window.title('MCPL')
aaaa='启动后关闭'
bg = ImageTk.PhotoImage(file='bg.png')
bgLabel = tk.Label(window,image=bg)
bgLabel.pack()
with open('minecraftpath.txt','r') as temp:
    minecraftpath=temp.read()
with open('java.txt') as temp:
    javapath=temp.read()
def javaSet():
    global javapath
    if javapath=='':
        if tk.messagebox.askyesno('警告','该计算机未安装Java，是否安装？'):
            os.system('explorer https://www.java.com/zh-CN/download/manual.jsp')
    javapath=easygui.diropenbox('选择Java安装路径',default='C:\Program Files')
    if javapath==None:
        with open('java.txt') as temp:
            javapath=temp.read()
    with open('java.txt','w') as temp:
        javapath=temp.write(javapath)
try:
    versionsList=os.listdir(minecraftpath+'/versions')
except:
    os.makedirs(minecraftpath+'/versions')
    os.mkdir(minecraftpath+'/mods')
v=tk.tkinter.IntVar()
def launcherSet():
    global minecraftpath,v
    gamedirs=['官方启动器目录(C:/Users/86181/AppData/Roaming/.minecraft)','当前目录(.minecraft)','自定义路径:('+minecraftpath+')']
    launcherSetwindow=tk.tkinter.Toplevel(window)
    launcherSetwindow.resizable(0,0)
    launcherSetwindow.title('设置')
    tk.Button(launcherSetwindow,text='当前Java路径为'+javapath,command=javaSet).pack()
    #windowSetBtn = tk.Button(launcherSetwindow, text='启动器可见性',command=windowSet)
    #windowSetBtn.place(x=0,y=0)
    tk.Label(launcherSetwindow,text='游戏目录').pack()
    index=0
    for i in gamedirs:
        tk.Radiobutton(launcherSetwindow, variable=v, text="{}".format(i), value=index,command=minecraftpathSet).pack()
        index+=1
def windowSet():
    global aaaa
    aaaa=easygui.buttonbox('启动器可见性','',['启动后关闭','启动后隐藏','保持可见'])
def minecraftpathSet():  
    global minecraftpath
    temp=v.get()
    logging.info(temp)
    if temp==0:
        minecraftpath="C:/Users/86181/AppData/Roaming/.minecraft"
    elif temp==2:
        minecraftpath=easygui.diropenbox()
    elif temp==1:
        minecraftpath='.minecraft'
    with open('minecraftpath.txt','w') as temp:
        temp.write(minecraftpath)
def set():
    file_path = minecraftpath+"/mods"  #文件路径
    path_list = os.listdir(file_path) #遍历整个文件夹下的文件name并返回一个列表
    get_modList = []#定义一个空列表
    a=[]
    b=[]
    for i in get_modList:
        if i.split('.jar')[1]=='disabled':           
            a.append(i)
        else:
            b.append(i)
    logging.info(a,b)
def run(): 
    global minecraftpath,start
    logging.info('正在启动'+str(start))
    os.popen(javapath,minecraftpath+'/versions'+start+' -Xmx'+mon+'m -Xmn128m -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow -Dos.name=Windows_7 -Dos.version=service_Pack_1')
    if aaaa=='启动后关闭':
        exit()
    elif aaaa=='启动后隐藏':
        pass
    else:
        return
def download():
    os.popen('python download.pyw')
bgLabel=tk.Label(window,text=start)
bgLabel.pack()
def versionsListWindow():
    global start,bgLabel
    if(len(versionsList)==0):
        tk.tkinter.messagebox.showerror('错误','未下载任何版本')
        return
    start=easygui.choicebox('选择一个版本','版本列表',versionsList)
    bgLabel.forget()
    bgLabel = tk.Label(window,text=start)
    bgLabel.pack()
launcherSetBtn = tk.Button(window, text='\n设置\n',command=launcherSet)
launcherSetBtn.place(x=0, y=0)
runBtn = tk.Button(window, text='\n启动\n',command=run)
runBtn.place(x=969, y=550)
downloadBtn = tk.Button(window, text='\n下载\n',command=download)
downloadBtn.place(x=0, y=170)
versionslistBtn= tk.Button(window, text='\n版本列表\n',command=versionsListWindow)
versionslistBtn.place(x=0, y=100)
setBtn = tk.Button(window, text='\n模组管理\n',command=set)
setBtn.place(x=969, y=0)
window.mainloop()