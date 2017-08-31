from datetime import datetime
from Register.models import *

#定时任务：每分钟查,15分钟未付款的订单被自动删除
def crontab_task1():
    print("crontab 1")

    #15分钟未付款
    res = ReservationOrder.objects.all()
    for re in res:
        #a = datetime.strptime(re.createdTime, "%Y-%m-%d %H:%M:%S.%f")
        a = re.createdTime
        b = datetime.now()

        cha = (b-a).seconds

        if cha > 900: #时间差大于15分钟
            print(">900")
            try:
                to = re.toBeRegistered_id
            except:
                re.delete()
            else:
                to.capacity = to.capacity + 1
                to.save()
                re.delete()
        else:
            break #按顺序理应更晚生成的在后面，读到第一个没到15分钟的，后面的也肯定没到15分钟

##  每天查,过时的ToBeRegistered表项目被删除、过时不就诊的预约单无效
def crontab_task2():
    print("crontab 2")

    tos = ToBeRegistered.objects.all()
    for to in tos:
        a = to.date
        b = datetime.now()

        cha = (a-b).days

        if cha < 1 | cha == 1:
            print("<1")
            to.delete()

    res = Reservation.objects.filter(ifJiuZhen=False,ifValid=True)
    print(res)
    for re in res:

        c = re.date
        d = datetime.now()

        cha2 = (c-d).days
        #cha2 = (c - d).seconds
        if cha2 < 1 | cha2 == 1 :
            print("cha2<1")
            re.ifValid=False
            if re.user_id.creditMark > 0:
                re.user_id.creditMark = re.user_id.creditMark - 1
                re.user_id.save()
            re.save()




