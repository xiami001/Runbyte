# coding=utf-8
#python2.7 32位
import ctypes
import win32gui
import win32process
import win32api
import win32event
from win32con import PAGE_READWRITE, MEM_COMMIT, MEM_RESERVE, MEM_RELEASE,PROCESS_ALL_ACCESS

DWORD=ctypes.c_ulong
HANDLE=ctypes.c_ulong
LPVOID=ctypes.c_long

process_all = 0x1F0FFF
memcommit = (0x1000 | 0x2000)

#获取窗口句柄,unicode编码,python2.7需要加u转换,或者用unicode()函数转换
whandle=win32gui.FindWindow(None,u'游戏找CALL练习实例one')
print whandle

#获取进程PID
pid=win32process.GetWindowThreadProcessId(whandle)[1]
if pid==None:
    print "未找到进程"
    exit(-1)
else:
    print pid

#进程句柄
phandle=win32api.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
#获取程序基址
base=win32process.EnumProcessModules(phandle)
#print "游戏基址是: "+str(hex(base[0]))
print phandle

#加载kernal32.dll
kernel32=ctypes.windll.LoadLibrary(r"C:\Windows\System32\kernel32.dll")

#执行加血函数call
"""
pushad
mov edx,0x00453028
mov eax,0x00456d68
mov eax,[eax]
mov ebx,0x00452E98
call ebx
popad
ret
"""
shellcode="\x60\xC7\xC2\x28\x30\x45\x00\xC7\xC0\x68\x6D\x45\x00\x8B\x00\xC7\xC3\x98\x2E\x45\x00\xFF\xD3\x61\xc2\x04"

#MSF生成，弹计算器shellcode去掉00版本
shellcode2=("\xbe\x91\xf1\x32\x68\xdd\xc7\xd9\x74\x24\xf4\x5f\x31"
"\xc9\xb1\x31\x31\x77\x13\x83\xef\xfc\x03\x77\x9e\x13"
"\xc7\x94\x48\x51\x28\x65\x88\x36\xa0\x80\xb9\x76\xd6"
"\xc1\xe9\x46\x9c\x84\x05\x2c\xf0\x3c\x9e\x40\xdd\x33"
"\x17\xee\x3b\x7d\xa8\x43\x7f\x1c\x2a\x9e\xac\xfe\x13"
"\x51\xa1\xff\x54\x8c\x48\xad\x0d\xda\xff\x42\x3a\x96"
"\xc3\xe9\x70\x36\x44\x0d\xc0\x39\x65\x80\x5b\x60\xa5"
"\x22\x88\x18\xec\x3c\xcd\x25\xa6\xb7\x25\xd1\x39\x1e"
"\x74\x1a\x95\x5f\xb9\xe9\xe7\x98\x7d\x12\x92\xd0\x7e"
"\xaf\xa5\x26\xfd\x6b\x23\xbd\xa5\xf8\x93\x19\x54\x2c"
"\x45\xe9\x5a\x99\x01\xb5\x7e\x1c\xc5\xcd\x7a\x95\xe8"
"\x01\x0b\xed\xce\x85\x50\xb5\x6f\x9f\x3c\x18\x8f\xff"
"\x9f\xc5\x35\x8b\x0d\x11\x44\xd6\x5b\xe4\xda\x6c\x29"
"\xe6\xe4\x6e\x1d\x8f\xd5\xe5\xf2\xc8\xe9\x2f\xb7\x37"
"\x08\xfa\xcd\xdf\x95\x6f\x6c\x82\x25\x5a\xb2\xbb\xa5"
"\x6f\x4a\x38\xb5\x05\x4f\x04\x71\xf5\x3d\x15\x14\xf9"
"\x92\x16\x3d\x9a\x75\x85\xdd\x73\x10\x2d\x47\x8c")

#动态申请内存
lpbuffer =kernel32.VirtualAllocEx(int(phandle),None,len(shellcode2),MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE)
print lpbuffer

#句柄必须转换成int类型才可以
written = ctypes.c_int(0)
#写内存
kernel32.WriteProcessMemory(int(phandle), lpbuffer, shellcode2, len(shellcode2), ctypes.byref(written))

ret=0
## 创建远程线程，指定入口为我们的shellcode头部
retid=win32process.CreateRemoteThread(phandle,None,0,lpbuffer ,0,ret)
print retid

#等待线程结束
win32event.WaitForSingleObject(phandle,1000)

#释放内存
kernel32.VirtualFreeEx(int(phandle), None, 0, MEM_RELEASE)
print('远程线程执行函数CALL结束')




