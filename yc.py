#yc.py 双色球预测
import urllib.request,re,os,json
from lxml import etree
def yc():
    url='http://tubiao.zhcw.com/tubiao/ssqNew/ssqInc/ssqZongHeFengBuTuAscselect=50.html'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/53736'}
    req = urllib.request.Request(url,None,headers)
    html= urllib.request.urlopen(req).read().decode() #
    tree=etree.HTML(html)

    prered=tree.xpath('//td[contains(@class,"redqiu ")]/text()') #红球集合，300个,元素为字符串
    red=[int(i) for i in prered] #转字符串到整数
    preblue=tree.xpath('//td[contains(@class,"blueqiu3 td")]/text()') #篮球集合 50个，元素为字符串
    blue=[int(i) for i in preblue]
    preqh=tree.xpath('//a[contains(@title,"开奖日期")]/text()')#期号 元素为字符串
    qh=[int(i) for i in preqh]
    prerq=tree.xpath('//a[contains(@title,"开奖日期")]/@title')#开奖日期,格式为：“开奖日期：2016-07-26”
    rq=[re.findall(r'\d{4}-\d{2}-\d{2}',i)[0] for i in prerq] #重新获取日期

    #红球空字典
    hqdic={'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': [], 'h7': [], 'h8': [], 'h9': [], 'h10': [], 'h11': [], 'h12': [], 'h13': [], 'h14': [], 'h15': [], 'h16': [], 'h17': [], 'h18': [], 'h19': [], 'h20': [], 'h21': [], 'h22': [], 'h23': [], 'h24': [], 'h25': [], 'h26': [], 'h27': [], 'h28': [], 'h29': [], 'h30': [], 'h31': [], 'h32': [], 'h33': []}
    #篮球空字典
    lqdic={'l1': [], 'l2': [], 'l3': [], 'l4': [], 'l5': [], 'l6': [], 'l7': [], 'l8': [], 'l9': [], 'l10': [], 'l11': [], 'l12': [], 'l13': [], 'l14': [], 'l15': [], 'l16': []}

    for i in range(102,300): #33期*6
        y=red[i]
        hqdic['h{}'.format(y)].append(qh[int(i/6)])

    for i in range(2,50): #16*3期
        y=blue[i]
        lqdic['l{}'.format(y)].append(qh[i])
    hqqw={'h1': 33, 'h2': 33, 'h3': 33, 'h4': 33, 'h5': 33, 'h6': 33, 'h7': 33, 'h8': 33, 'h9': 33, 'h10': 33, 'h11': 33, 'h12': 33, 'h13': 33, 'h14': 33, 'h15': 33, 'h16': 33, 'h17': 33, 'h18': 33, 'h19': 33, 'h20': 33, 'h21': 33, 'h22': 33, 'h23': 33, 'h24': 33, 'h25': 33, 'h26': 33, 'h27': 33, 'h28': 33, 'h29': 33, 'h30': 33, 'h31': 33, 'h32': 33, 'h33': 33}
    #计算红球期望,没有出现的红球默认期望为33期
    for i in range(1,34):
        if len(hqdic['h{}'.format(i)]) ==0: #如果红球没有出现，就跳过
            pass
        else:
            hqqw['h{}'.format(i)]=round(33/len(hqdic['h{}'.format(i)]),2)#33期除于出现次数

    lqqw={'l1': 48, 'l2': 48, 'l3': 48, 'l4': 48, 'l5': 48, 'l6': 48, 'l7': 48, 'l8': 48, 'l9': 48, 'l10': 48, 'l11': 48, 'l12': 48, 'l13': 48, 'l14': 48, 'l15': 48, 'l16': 48}
    #计算篮球期望，没有出现的篮球默认期望为48期
    for i in range(1,17):
        if len(lqdic['l{}'.format(i)]) ==0: #如果红球没有出现，就跳过
            pass
        else:
            lqqw['l{}'.format(i)]=round(48/len(lqdic['l{}'.format(i)]),2) #48期除于出现次数

    xqqh=qh[-1]+1#下期期号，处理遗漏时用
    #红球遗漏
    hqyl={'h1': 33, 'h2': 33, 'h3': 33, 'h4': 33, 'h5': 33, 'h6': 33, 'h7': 33, 'h8': 33, 'h9': 33, 'h10': 33, 'h11': 33, 'h12': 33, 'h13': 33, 'h14': 33, 'h15': 33, 'h16': 33, 'h17': 33, 'h18': 33, 'h19': 33, 'h20': 33, 'h21': 33, 'h22': 33, 'h23': 33, 'h24': 33, 'h25': 33,'h26': 33, 'h27': 33, 'h28': 33, 'h29': 33, 'h30': 33, 'h31': 33, 'h32': 33, 'h33': 33}
    #篮球遗漏
    lqyl={'l1': 48, 'l2': 48, 'l3': 48, 'l4': 48, 'l5': 48, 'l6': 48, 'l7': 48, 'l8': 48, 'l9': 48, 'l10': 48, 'l11': 48, 'l12': 48, 'l13': 48, 'l14': 48, 'l15': 48, 'l16': 48}

    #遗漏处理，考虑到 可能长时间没有出现的情况，以及跨年计算情况 2017001-2016153=848

    for i in range(1,34): #红球遗漏
        if len(hqdic['h{}'.format(i)]) == 0:
            pass
        else:
            hqyl['h{}'.format(i)]=xqqh-hqdic['h{}'.format(i)][-1]

    for i in range(1,17): #篮球遗漏
        if len(lqdic['l{}'.format(i)]) == 0: #如果篮球没有出现，即没有期号，则跳过
            pass
        else:
            lqyl['l{}'.format(i)]=xqqh-lqdic['l{}'.format(i)][-1]

    hqyc={} #红球预测  
    for key,value in hqdic.items():
        hqyc[key]=round((hqyl[key]%hqqw[key])/hqqw[key],2)

    hyc=sorted(hqyc.items(), key=lambda item:item[1],reverse=True)


    lqyc={} #篮球预测
    for key,value in lqdic.items():
        lqyc[key]=round((lqyl[key]%lqqw[key])/lqqw[key],2)

    lyc=sorted(lqyc.items(), key=lambda item:item[1],reverse=True)

    return hyc[0:8],lyc[0:3],rq[49],qh[49]
if __name__ == '__main__':
    newhq,newlq,rq,qh=yc()[0],yc()[1],yc()[2],yc()[3]
    h,l=[],[]
    hst,lst='',''
    for i in newhq:
        h.append(str(re.split('h',i[0])[1]))
    for i in h:
        hst=hst+i+' '

    for i in newlq:
        l.append(str(re.split('l',i[0])[1]))

    for i in l:
        lst=lst+i+' '
    data={'rq':rq,'qh':str(qh),'hq':hst,'lq':lst}
    st=json.dumps(data)
    f=open('tz','a+')
    f.write('{}\n'.format(st))
    f.close()
                                                                                                                                
