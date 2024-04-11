# littlescan
一个逻辑简单的web目录扫描脚本，后续会不断修正添加,也会考虑用golang写一个效率更高的scanner，或者用协程来实现scan  
  
笔者水平有限，各位大佬轻点🐎，提出的各种建议我都会积极考量，感谢各位  
  
## 项目介绍
本项目是基于python的多线程目录扫描脚本  
  
### 开发环境  
``` python --version python 3.9.13 ```  

### 参数
#### -h
显示帮助信息  

``` python scan.py DOMAIN -h ```  

#### -q
可设置是否永远不停止扫描  

``` python scan.py DOMAIN -q ```  

#### -d
更换字典，默认字典为php.txt,使用时取出放与scan.py同级目录即可  

``` python scan.py DOMAIN -d asp.txt ```  

#### -i
更换请求头，格式如给出的header.txt  

``` python scan.py DOMAIN -i header.txt ```  

#### -o
输出到指定文件  

``` python scan.py DOMAIN -o target.txt ```  

#### -s
指定除了200之外的其他状态码

``` python scan.py DOMAIN -s 403 ```  

### That's All  







