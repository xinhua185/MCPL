#codeing=gbk
import os
import tkinter.ttk as tk
import tkinter.messagebox as msgbox
from easygui import fileopenbox,diropenbox
from PIL import Image, ImageTk
with open('minecraftpath.txt') as temp:
    minecraftpath=temp.read()
win=tk.tkinter.Tk()
parent = os.path.dirname(os.path.realpath(__file__))
icon_path = parent + '/MCPL.ico'
bg = ImageTk.PhotoImage(file='bg.png')
tk.Label(win,image=bg).pack()
win.resizable(0, 0)
win.iconbitmap(icon_path)
win.title('MCPL-下载')
def ope():
    os.chdir(diropenbox('整合包解压到'))
    os.popen('"'+os.path.abspath(parent)+r'\7z\7zG.exe" e '+fileopenbox(filetypes=['*.7z','*.zip','*.rar','*.001','*.cab','*.iso', '*.xz','*.txz','*.lzma','*.tar','*.cpio','*.bz2','*.bzip','*.tbz','*.tbz','*.gz','*.gzip','*.tgz','*.tpz','*.z','*.taz','*.lzh','*.lha','*.rpm','*.deb','*.arj','*.vhd','*.wim','*.swm','*.esd','*.fat','*.ntfs','*.dmg','*.hfs','*.xar','*.squashfs','*.exe']))
def ext():
    os.chdir(minecraftpath)
    os.popen('"'+os.path.abspath(parent)+r'\7z\7zG.exe" a -ad -slp -saa -- C:\Users\Public\Documents\我的世界Java版整合包')
menubar = tk.tkinter.Menu(win)
filemenu = tk.tkinter.Menu(menubar, tearoff=False)
webmenu = tk.tkinter.Menu(menubar, tearoff=False)
webmenu.add_command(label="网络设置",command=(lambda: os.popen("ncpa.cpl")))
webmenu.add_command(label="下载源设置",command=(lambda: os.popen("ncpa.cpl")))
filemenu.add_command(label="导入整合包",command=ope,accelerator='Ctrl+O')
filemenu.add_command(label="导出整合包", command=ext, accelerator='Ctrl+S')
menubar.add_cascade(label="文件", menu=filemenu)
menubar.add_cascade(label="网络", menu=webmenu)
win.config(menu=menubar)
win.bind_all("<Control-o>", lambda event: ope())
win.bind_all("<Control-s>", lambda event: ext())
msgbox.showerror('错误','该功能未完善,请访问 https://bmclapidoc.bangbang93.com/')
win.mainloop()