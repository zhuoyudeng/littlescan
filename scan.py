import sys
import getopt
import random
import chardet
import requests
import threading

from fake_useragent import UserAgent


EXIT = False  # 控制是否退出扫描的标志
DICT = []  # 存储字典内容
DOMAIN = ''  # 目标域名
OUTPUT = []  # 存储扫描结果
STATUS = []  # 期望的 HTTP 状态码
THREAD = 100  # 线程数量
OUTPUT_FILE = ''  # 输出文件路径
NEVER_STOP = False  # 是否永远不停止扫描
TIMEOUT_QUANTITY = 0  # 超时次数
UA = UserAgent()
HEADER = {'User-Agent': UA.random}  # 随机ua
HELP_INFO = '''usage: python scan.py domain [OPTIONS]

    -h: show this help information
    -d: dictionary file, default: data/default.list
    -t: number of threads, default threads: 100
    -i: request headers file
    -o: save the result to output file
    -s: set other HTTP status code to print, default: 200 status code only
    -q: quiet mode, does not interact when timeout error
    
output: [url]   [http status code]'''

def help():
    """显示帮助信息"""
    print(HELP_INFO)
    exit()


def getEncoding(file):
    """获取文件编码"""
    fp = open(file, 'rb')
    d = fp.read()
    fp.close()
    return chardet.detect(d)["encoding"]


def loadDict(file):
    """加载字典文件"""
    print("\033[1;34m[*]\033[0m Loading the dictionary file into memory, please wait...")
    try:
        n = 0
        encoding = getEncoding(file)
        for i in open(file, encoding=encoding):
            i = i.strip("\r\n")  # 删除换行符
            if i:
                DICT.append(i)
                n += 1
        print("\033[1;32m[+]\033[0m loading completed. %d dictionary" % (n))
        return n
    except:
        print("\n\033[1;31m[!]\033[0m Cant open the dictionary file: %s" % (file))
        exit()


def setRequestHeader(file):
    """设置请求头"""
    try:
        for i in open(file):
            tmp = i.split(":")
            v = ""
            if len(tmp) >= 2:
                v = tmp[1].strip("\n")
            k = tmp[0].strip("\n")
            HEADER[k] = v
    except:
        print("\n\033[1;31m[!]\033[0m Cant open the request header file: %s" % (file))
        exit()

def saveResult():
    """保存扫描结果"""
    file = open(OUTPUT_FILE, "w")
    for i in OUTPUT:
        file.write("%s\n" % (i))
    file.close()
    print("\033[1;32m[+]\033[0m Result has been saved to file: %s" % (OUTPUT_FILE))


class aThread(threading.Thread): # 扫描线程类
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global EXIT
        global NEVER_STOP
        global TIMEOUT_QUANTITY
        while DICT:
            if lock.acquire():
                if DICT:
                    string = DICT.pop()
                    lock.release()
                    url = "%s%s" % (DOMAIN, string)
                    try:
                        h = requests.get(url=url, headers=HEADER, timeout=2)
                        if h.status_code in STATUS:  # 只输出指定的状态码
                            if lock.acquire():
                                print("%s   \033[1;32m%s\033[0m" % (url, h.status_code))
                                if OUTPUT_FILE:
                                    OUTPUT.append(url)
                                lock.release()
                                continue
                        elif not STATUS and h.status_code == 200:  # 默认输出200状态码
                            if lock.acquire():
                                print("%s   \033[1;32m200\033[0m" % (url))
                                if OUTPUT_FILE:
                                    OUTPUT.append(url)
                                lock.release()
                    except:
                        TIMEOUT_QUANTITY += 1
                        if lock.acquire():
                            if TIMEOUT_QUANTITY > 50 and NEVER_STOP == False:
                                if DICT:
                                    d = input(
                                        "\033[1;31m[!]\033[0m It has timeout 50 times here, Maybe your IP is locked, Keep scanning?[y/n]?>_ ")
                                    if d == 'y':
                                        NEVER_STOP = True
                                        lock.release()
                                        continue
                                    else:
                                        EXIT = True
                                        print("\033[1;31m[!]\033[0m Scan stop, Too many timeout error.")
                                        del DICT[:]
                            lock.release()
                else:
                    lock.release()

arg = getopt.getopt(sys.argv[2:], '-h-d:-t:-i:-o:-s:-q', [])
dir_file = 'php.txt'
for opt_n, opt_v in arg[0]:
    if opt_n == "-h":
        help()
        continue
    if opt_n == "-q":
        NEVER_STOP = True
        continue
    if opt_n == "-d":
        dir_file = opt_v
        continue
    if opt_n == "-t":
        THREAD = int(opt_v)
        continue
    if opt_n == "-i":
        setRequestHeader(opt_v)
        continue
    if opt_n == "-o":
        OUTPUT_FILE = opt_v
        continue
    if opt_n == "-s":
        for i in opt_v.split(","):
            STATUS.append(int(i))
        if 200 in STATUS:
            STATUS.remove(200)

if len(sys.argv) < 2 or sys.argv[1] == "-h":
    help()
DOMAIN = sys.argv[1]
try:
    h = requests.get(url=DOMAIN, headers=HEADER, timeout=3)
except:
    print("\033[1;31m[!]\033[0m Cant open the website: %s, check your network" % (DOMAIN))
    exit()

impossibleUrl = ''
for i in range(255):
    impossibleUrl += chr(random.randint(97, 123))
h = requests.get(url="%s/%s" % (DOMAIN, impossibleUrl), headers=HEADER)
if h.status_code == 200:
    if input("\033[1;31m[!]\033[0m Maybe all url will return a 200 status code, Keep the scan?[y/n]: ") != 'y':
        exit()

dict_size = loadDict(dir_file)
if dict_size < (THREAD * 2):
    THREAD = dict_size / 2
if THREAD < 1:
    THREAD = 1
print("\033[1;34m[*]\033[0m This project will rewrite")
tmp = "\033[1;31m Quiet mode\033[0m" if NEVER_STOP else ""
print("\033[1;34m[*]\033[0m Starting. Threads: %s.%s\n" % (THREAD, tmp))

threadList = []
lock = threading.Lock()
for i in range(THREAD):
    t = aThread()
    threadList.append(t)
for t in threadList:
    t.start()
for t in threadList:
    t.join()

if EXIT == False:
    print("\n\033[1;32m[+]\033[0m Scan completed")
if OUTPUT_FILE:
    saveResult()
