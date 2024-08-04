#codeing=gbk
import os,json,easygui,urllib3,platform
import tkinter.ttk as tk
import tkinter.messagebox as msgbox
# from PIL import Image, ImageTk
with open('mcpl.json','r') as temp:
    config=json.load(temp)
try:
    with open('version_manifest.json','r') as temp:
        version_manifest=json.load(temp)
except:
    version_manifest_rp = urllib3.request("GET",'https://bmclapi2.bangbang93.com/mc/game/version_manifest.json')
    version_manifest=json.loads(version_manifest_rp.data.decode('utf-8'))
    with open('version_manifest.json','w') as temp:
        temp.write(version_manifest_rp.data.decode("utf-8"))
    print("succesfully write")
win=tk.tkinter.Tk()
parent = os.path.dirname(os.path.realpath(__file__))
icon_path = parent + '/MCPL.ico'
systype=platform.platform()
# bg = ImageTk.PhotoImage(file='bg.png')
# tk.Label(win,image=bg).pack()
win.resizable(0, 0)
win.iconbitmap(icon_path)
win.title('MCPL-下载')
def import_package():
    os.chdir(easygui.diropenbox('整合包解压到'))
    os.popen(os.path.join(parent,'7z','7zG.exe')+' e '+easygui.fileopenbox(filetypes=['*.7z','*.zip','*.rar','*.001','*.cab','*.iso', '*.xz','*.txz','*.lzma','*.tar','*.cpio','*.bz2','*.bzip','*.tbz','*.tbz','*.gz','*.gzip','*.tgz','*.tpz','*.z','*.taz','*.lzh','*.lha','*.rpm','*.deb','*.arj','*.vhd','*.wim','*.swm','*.esd','*.fat','*.ntfs','*.dmg','*.hfs','*.xar','*.squashfs','*.exe']))
def extract_package():
    os.chdir(config['minecraftpath'])
    os.popen(os.path.join(parent,'7z','7zG.exe')+' a -ad -slp -saa --')
def network_set():
    msgbox.showerror('错误','尚未实现')
def download_version():
    version_list=[]
    for i in version_manifest["versions"]:
        version_list.append(i["id"])
    choice_version=easygui.choicebox("选择一个版本","下载",version_list)
    for i in version_manifest["versions"]:
        if(i["id"]==choice_version):
            version_type=easygui.choicebox("选择版本类型",'下载',["原版","forge","fabric"])
            version_info_rp = urllib3.request("GET",i["url"])
            src=json.loads(version_info_rp.data.decode('utf-8'))
            if(os.path.exists(os.path.join(config["minecraftpath"],"versions",i["id"]))==False):
                os.mkdir(os.path.join(config["minecraftpath"],"versions",i["id"]))
            with open(os.path.join(config["minecraftpath"],"versions",i["id"],i["id"]+'.json'),'w') as temp:
                temp.write(version_info_rp.data.decode("utf-8"))
            version_info=json.loads(version_info_rp.data.decode("utf-8"))
            if("logging" in version_info):
                if(os.path.exists(os.path.join(config["minecraftpath"],"versions",i["id"],"log4j2.xml"))==False):
                    log4j2_xml_rp=urllib3.request("GET",version_info["logging"]["client"]["file"]["url"])
                    with open(os.path.join(config["minecraftpath"],"versions",i["id"],"log4j2.xml"),'w') as temp:
                        temp.write(log4j2_xml_rp.data.decode("utf-8"))
            if(os.path.exists(os.path.join(config["minecraftpath"],"assets","indexes",version_info["assetIndex"]["id"])+'.json')==False):
                assetIndex_rp=urllib3.request("GET",version_info["assetIndex"]["url"])
                assetIndex=json.loads(assetIndex_rp.data.decode("utf-8"))
                with open(os.path.join(config["minecraftpath"],"assets","indexes",version_info["assetIndex"]["id"])+'.json','w') as temp:
                    temp.write(assetIndex_rp.data.decode("utf-8"))
                print("write assetIndex")
            else:
                with open(os.path.join(config["minecraftpath"],"assets","indexes",version_info["assetIndex"]["id"])+'.json','r') as temp:
                    assetIndex=json.load(temp)
                print("read assetIndex")
            print("starting download libraries")
            for libfile in version_info["libraries"]:
                f=True
                if("rules" in libfile):
                    f=False
                    for rule in libfile["rules"]:
                        if(rule["action"]=="allow"):
                            f=True
                            if("os" in rule):
                                if(rule["os"]==systype):
                                    f=True
                                else:
                                    f=False
                        else:
                            if("os" in rule):
                                if(rule["os"]==systype):
                                    f=False
                                else:
                                    f=True
                if(f):
                    libpath=os.path.join(config["minecraftpath"],"libraries",libfile["downloads"]["artifact"]["path"])
                    if(os.path.exists(libpath)==False):
                        libdir=os.path.dirname(libpath)
                        if(os.path.exists(libdir)==False):
                            os.mkdir(libdir)
                        pool=urllib3.PoolManager()
                        with open(libpath, 'wb') as f:
                            with pool.request('GET',libfile["downloads"]["artifact"]["url"], preload_content=False) as resp:
                                for chunk in resp.stream():
                                    f.write(chunk)
            msgbox.showinfo("下载","下载成功完成")
            break
        
menubar = tk.tkinter.Menu(win)
filemenu = tk.tkinter.Menu(menubar, tearoff=False)
webmenu = tk.tkinter.Menu(menubar, tearoff=False)
webmenu.add_command(label="网络设置",command=(lambda: os.popen("ncpa.cpl")))
webmenu.add_command(label="下载源设置",command=network_set)
filemenu.add_command(label="导入整合包",command=import_package,accelerator='Ctrl+O')
filemenu.add_command(label="导出整合包", command=extract_package, accelerator='Ctrl+S')
filemenu.add_command(label="下载新版本",command=download_version)
menubar.add_cascade(label="文件", menu=filemenu)
menubar.add_cascade(label="网络", menu=webmenu)
win.config(menu=menubar)
win.bind_all("<Control-o>", lambda event: import_package())
win.bind_all("<Control-s>", lambda event: extract_package())
msgbox.showerror('错误','该功能未完善,请访问 https://bmclapidoc.bangbang93.com/')
    
win.mainloop()