import requests
import getpass
import base64
#欢迎
def showWel():
    print('-----------------------------------')
    print('|             七天灵堂             |')
    print('|        开发者 豆芽酱 lsr         |')
    print('|  豆芽酱     https://dyas.top     |')
    print('|  lsr     https://www.lishangru.cn|')
    print('-----------------------------------')

#登录获取TOKEN
def getToken():
    userName=input('请输入账号：')
    try:
        passWord=getpass.getpass('请输入密码(请直接输入，不会在屏幕显示)：')
    except Warning:
        print('环境不安全 禁止使用\n')
        return '0'
    passEn=str(base64.b64encode(passWord.encode('utf-8')),'utf-8')+'e01UZ3lNalUyTURVME1qRjdjM3B2Ym1WOX0='    
    #print(passEn)
    req={'usercode':userName,
         'password':passEn}
    #print(req)
    try:
        resp = requests.post('https://szone-my.7net.cc/login?usercode='+userName+'&password='+passEn,data=req)
        #print(resp.text)
        answ=resp.json()
    except Exception:
        print('网络异常\n')
        return '0'
    if answ['status']!=200:
        #print(answ)
        print('账号或密码错误\n')
        return '0'
    token=answ['data']['token']
    return token

#获取个人信息
def getInfo(Header):
    try:
        resp=requests.get('https://szone-my.7net.cc/userInfo/GetUserInfo', headers=Header)
    except Exception:
        print('网络异常\n')
        return '0'
    answ=resp.json()
    if answ['status']!=200:
        #print(answ)
        print('系统错误\n')
        return '0'
    return (answ)

#展示信息
def showUinfo(Info):
    print(':)'+Info['data']['studentName']+',恭喜！登录成功！')

#终止
def stopHere():
    while 1:
        1

#获取考试列表
def getExamlist(headers,Info):
    try:
        resp=requests.get('https://szone-score.7net.cc/exam/getClaimExams?startIndex=0&rows=5&studentName='+Info['data']['studentName']+'&schoolGuid='+Info['data']['schoolGuid']+'&grade='+Info['data']['grade'],headers=headers)
        answ=resp.json()
        #print (answ)
    except Exception:
        print('网络异常\n')
        return '0'
    if answ['status']!=200:
        #print(answ)
        print('系统错误\n')
        return '0'
    return answ['data']['list']

#展示考试列表
def showElist(lists):
    i=1
    print('考试列表')
    for Each in lists:
        print('\n第'+str(i)+'次考试')
        i+=1
        print(Each['type']+':'+Each['examName']+Each['time']+'总分'+str(Each['score']))
    inId=int(input('请输入您要查看的考试序号'))
    return lists[inId-1]
    
#展示考试详情
def showDetails(Headers,userInfo,examInfo):
    date={'grade':userInfo['data']['grade'],
          'examGuid':examInfo['examGuid'],
          'schoolGuid':userInfo['data']['schoolGuid'],
          'ruCode':examInfo['ruCode'],
          'studentCode':examInfo['studentCode']}
    try:
        resp=requests.post('https://szone-score.7net.cc/Question/Subjects',headers=Headers,data=date)
    except Exception:
        print('网络异常\n')
        return '0'
    answ=resp.json()
    answ=answ['data']
    answ=answ['subjects']
    #print(answ)
    for i in answ:
        print(str(i['km'])+str(i['myScore'])+'/'+str(i['fullScore']))
        print('班级排名'+str(i['cs']))
        print('级部排名'+str(i['ss']))
        print('联考排名'+str(i['us']))

#主流程
showWel()
token=getToken()
if token=='0':
    stopHere()
        
Header={'Token':token,'Version':'3.1.1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
userInfo=getInfo(Header)
if userInfo=='0':
    stopHere()
showUinfo(userInfo)

examList=getExamlist(Header,userInfo)
if examList=='0':
    stopHere()
examInfo=showElist(examList)
#print(examInfo)

showDetails(Header,userInfo,examInfo)

while 1:
    1
