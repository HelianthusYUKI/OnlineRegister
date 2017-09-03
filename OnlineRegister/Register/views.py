from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response


# Create your views here.
from Register.models import *
# import time

# DOCS = 0

def index(request):
    request.session['type'] = 'un_user'
    return render_to_response("index.html")

def register(request):
    print("regis")
    if 'name' in request.POST and request.POST['name'] \
        and 'password' in request.POST and request.POST['password'] \
        and 'cfm_password' in request.POST and request.POST['cfm_password'] \
        and 'sex' in request.POST and request.POST['sex'] \
        and 'id_number' in request.POST and request.POST['id_number'] \
        and 'phone' in request.POST and request.POST['phone']:

        name = request.POST['name']
        psw = request.POST['password']
        cfm_psw = request.POST['cfm_password']
        sex = request.POST['sex']
        id = request.POST['id_number']
        phone = request.POST['phone']

        print(id)
        print(phone)

        errors = []

        try:
            User.objects.get(id_number=id)
        except:
            if not psw == cfm_psw:
                errors.append("两次密码输入不一致！")
                return HttpResponse(errors[0])
            else:
                User.objects.create(name=name,
                                    password=psw,
                                    sex=sex,
                                    id_number=id,
                                    phone_number=phone,
                                    creditMark=3).save()
            return render_to_response("index.html")

        else:
            errors.append("身份证号已注册！")
            return HttpResponse(errors[0])

    else:
        raise HttpResponse("ooops!")

def login(request):
    print("user login")
    if 'id' in request.POST and request.POST['id'] \
        and 'password' in request.POST and request.POST['password']:

        id = request.POST['id']
        psw = request.POST['password']

        try:
            user = User.objects.get(id_number=id)
            user_psw = user.password
        except:
            return HttpResponse("没有此用户！请先注册！")
        else:
            if psw == user_psw:
                print("successUser")
                request.session['id'] = user.id
                request.session['type'] = "user"

                return HttpResponseRedirect("/OnlineRegister/show_user_info/")
            else:
                return HttpResponse("密码错误！")


    return

def adminLogin(request):
    if 'name' in request.POST and request.POST['name'] \
        and 'password' in request.POST and request.POST['password'] \
        and 'type' in request.POST and request.POST['type']:
        userName = request.POST['name']
        userPsw = request.POST['password']
        userType = request.POST['type']

        print(userName)
        print(userPsw)
        print(userType)

        if userType == 'admin':
            admin = Admin.objects.get(name = userName, password = userPsw)
            if admin:
                print("successAdmin")
                request.session['id'] = admin.id
                request.session['type'] = "admin"
                return render_to_response("backstage_index.html")
            return render_to_response("index.html")
        elif userType == 'registry':
            raise Http404
        elif userType == 'triage':
            raise Http404
        else:
            raise Http404
    else:
        print("???")
        raise Http404



def header(request):
    print("load header")
    return render_to_response('header.html')

def admin_left(request):
    print("load left")
    return render_to_response('admin_left.html')



########################################################
########################################################
##这是后台操作

def admin_hos_wh(request):
    return render_to_response('admin_hos_wh.html')

def hospital_search(request):
    print("hospital search")

    if request.method == "POST":
        district_code = request.POST.get('district')
        print(district_code)
        hospitals = Hospital.objects.filter(district=district_code)

        return render(request, 'hospital_search_results.html', {'hospitals': hospitals})
    else:
        raise Http404


def add_hospital(request):
    print("add hospital")

    if request.method == "POST":
        district_code = request.POST.get('district')
        hospital_name = request.POST.get('name')
        hospital_code = request.POST.get('code')
        print(district_code)
        print(hospital_name)
        print(hospital_code)

        new_hos = Hospital.objects.create(name = hospital_name, code = hospital_code, district = district_code)
        new_hos.save()

        #bug-无法返回
        return HttpResponse()
    else:
        raise Http404

def alter_hospital_select1_1(request):
    print("alter hospital 1..1")
    if request.method == "POST":
        district_code = request.POST.get('district')
        print(district_code)
        hospitals = Hospital.objects.filter(district=district_code)

        return render(request, 'hospital_options.html', {'hospitals': hospitals})
    else:
        raise Http404

def alter_hospital_select1_2(request):
    print("alter hospital 1..2")
    if request.method == "POST":
        district_code = request.POST.get('district')
        print(district_code)
        hospitals = Hospital.objects.filter(district=district_code)

        return render(request, 'hospital_options2.html', {'hospitals': hospitals})
    else:
        raise Http404


def alter_hospital_select2(request):
    print("alter hospital 2")
    print(request.POST.get('hos_id'))

    if request.method == "POST":
        hos_id = request.POST.get('hos_id')

        hospital = Hospital.objects.get(id = hos_id)

        return render(request, 'hos_info.html', {'hos': hospital})

    else:
        raise Http404


def alter_hospital(request):
    print("alter hospital 3")

    if request.method == "POST":
        hos_id = request.POST.get('id')
        hos_name = request.POST.get('name')
        hos_code = request.POST.get('code')

        hospital = Hospital.objects.get(id = hos_id)
        hospital.name = hos_name
        hospital.code = hos_code
        hospital.save()

        return render(request, 'hos_info.html', {'hos': hospital})

    else:
        raise Http404


def del_hospital(request):
    print("del hospital")

    if request.method == "POST":
        hos_id = request.POST.get('hos_id')

        Hospital.objects.get(id = hos_id).delete()

        return render(request, 'hos_info.html', )

    else:
        raise Http404


def show_department(request):
    print("show dep")
    dep1 = Department.objects.filter(level=0)

    return render(request, 'admin_dep_wh.html', {'departments_1':dep1})


def show_dep2(request):
    print("show dep2")

    if request.method == "POST":
        dep1_code = request.POST.get('dep1')

        dep2 = Department.objects.filter(level=dep1_code)

        return render(request, 'dep2_items.html',{'departments_2':dep2} )

    else:
        raise Http404

def show_dep2_2(request):
    print("show dep2 2")
    if request.method == "POST":
        dep1_code = request.POST.get('dep1_code')
        print(dep1_code)

        if dep1_code == "0":
            return render(request, 'dep2_options.html',{} )
        else:
            dep2 = Department.objects.filter(level=dep1_code)
            print(dep2)

            return render(request, 'dep2_options.html',{'dep2s':dep2} )
    else:
        raise Http404


def add_dep(request):
    print("add dep")
    if request.method == "POST":
        dep_name = request.POST.get('name')
        dep_code = request.POST.get('code')
        dep_level =request.POST.get('level')
        print(dep_name)
        print(dep_code)
        print(dep_level)

        new_dep = Department.objects.create(name = dep_name, code = dep_code, level = dep_level)
        new_dep.save()
        print("add dep worked!")


        dep1 = Department.objects.filter(level=0)

        return render(request, 'admin_dep_wh.html', {'departments_1': dep1})


    else:
        raise Http404



def alter_dep(request):
    print("alter dep")
    if request.method == "POST":
        olddep_code = request.POST.get('old_code')
        dep_name = request.POST.get('name')
        dep_code = request.POST.get('code')
        dep_level = request.POST.get('level')
        print(dep_name)
        print(dep_code)
        print(dep_level)

        dep = Department.objects.get(code=olddep_code)
        dep.name = dep_name
        dep.code = dep_code
        dep.level = dep_level
        dep.save()
        print("alter dep worked!")

        dep1 = Department.objects.filter(level=0)

        return render(request, 'admin_dep_wh.html', {'departments_1': dep1})


    else:
        raise Http404

def del_dep(request):
    print("del dep")

    if request.method == "POST":
        deldep_code = request.POST.get('code')

        Department.objects.get(code = deldep_code).delete()

        print("del dep worked!")

        dep1 = Department.objects.filter(level=0)

        return render(request, 'admin_dep_wh.html', {'departments_1': dep1})


    else:
        raise Http404



def show_doctor(request):
    print("show doc")

    dep1 = Department.objects.filter(level=0)

    return render(request,'admin_doc_wh.html',{'dep1s':dep1})

def search_doctor(request):
    print("search doctor")
    #dep1 = Department.objects.filter(level=0)
    if request.method == "POST":

        hos_id = request.POST.get('hospital')
        dep1_code = request.POST.get('dep1')
        dep2_code = request.POST.get('dep2')
        print(hos_id)
        print(dep1_code)
        print(dep2_code)

        if hos_id == "0":
            print("1")
            docs = Doctor.objects.filter(id=0)
            return render(request, 'doctor_search_results.html', {'docs': docs})
        else:
            print("2")
            doc_hos = Doctor_Hospital.objects.filter(hospital_id_id=hos_id).values("doctor_id_id")
            print(doc_hos)
            docs = Doctor.objects.filter(id__in=doc_hos)
            print(docs)
            if dep1_code == "0":
                #只选择了医院,传回这个医院所有的医生
                print("3")
                return render(request, 'doctor_search_results.html', {'docs': docs})
            else:
                print("4")

                if dep2_code == "0":
                    print("5")
                    #只选择了医院和科室，传回此科室的所有医生
                    dep2s = Department.objects.filter(level=dep1_code).values("id")
                    print(dep2s)
                    doc_dep = Doctor_Department.objects.filter(department_id_id__in=dep2s).values("doctor_id_id")
                    print(doc_dep)
                    docs = docs.filter(id__in=doc_dep)
                    print(docs)
                    return render(request, 'doctor_search_results.html', {'docs': docs})
                else:
                    print("6")
                    dep2s_2 = Department.objects.filter(code=dep2_code).values("id")
                    print(dep2s_2)
                    doc_dep_2 = Doctor_Department.objects.filter(department_id_id__in=dep2s_2).values("doctor_id_id")
                    print(doc_dep_2)
                    docs = docs.filter(id__in=doc_dep_2)
                    print(docs)
                    # global DOCS
                    # DOCS = docs

                    return render(request, 'doctor_search_results.html', {'docs': docs})
    else:
        raise Http404


def add_doc(request):
    print("add doc")
    if request.method == "POST":
        doc_name = request.POST.get('name')
        doc_sex = request.POST.get('sex')
        doc_position = request.POST.get('position')
        doc_phone = request.POST.get('phone')

        new_doc = Doctor.objects.create(name = doc_name,sex = doc_sex,position = doc_position,phone_number = doc_phone)
        doc_id = new_doc.id #数据库建立有误，应为医生设置特有的工号
        print(doc_id)
        new_doc.save()

        doc_dep = request.POST.get('dep_code')
        doc_hos = request.POST.get('hospital')

        print(doc_hos)

        doc = Doctor.objects.get(id=doc_id)
        dep = Department.objects.get(code=doc_dep)###!!!
        hos = Hospital.objects.get(id=doc_hos)



        new_doc_dep = Doctor_Department.objects.create(doctor_id = doc, department_id = dep)
        new_doc_dep.save()

        new_doc_hos = Doctor_Hospital.objects.create(doctor_id = doc, hospital_id = hos)
        new_doc_hos.save()

        print("add doc worked!")

        return render_to_response('admin_doc_wh.html')
    else:
        raise Http404


def alter_doc(request):
    print("alter doc")

    return

def del_doc(request):
    print("del doc")
    if request.method == "POST":

        doc = request.POST.getlist("doc")
        if doc:
            print(doc)

            for i in doc:
                print(i)
                Doctor.objects.get(id=i).delete() #用外键会连同doctor_dep和doc_hos一起删除

            return render_to_response('admin_doc_wh.html')
        else:
            print("fail")
            raise Http404
    else:
        raise Http404


def toBeRegistered(request):
    print("to be regis")
    dep1 = Department.objects.filter(level=0)

    return render(request, 'to_be_registered.html', {'dep1s': dep1})


def search_doctor2(request):
    print("search doctor 2")
    #dep1 = Department.objects.filter(level=0)
    if request.method == "POST":

        hos_id = request.POST.get('hospital')
        dep1_code = request.POST.get('dep1')
        dep2_code = request.POST.get('dep2')
        print(hos_id)
        print(dep1_code)
        print(dep2_code)

        if hos_id == "0":
            print("1")
            docs = Doctor.objects.filter(id=0)
            return render(request, 'doctor_search_results2.html', {'docs': docs})
        else:
            print("2")
            doc_hos = Doctor_Hospital.objects.filter(hospital_id_id=hos_id).values("doctor_id_id")
            print(doc_hos)
            docs = Doctor.objects.filter(id__in=doc_hos)
            print(docs)
            if dep1_code == "0":
                #只选择了医院,传回这个医院所有的医生
                print("3")
                return render(request, 'doctor_search_results2.html', {'docs': docs})
            else:
                print("4")

                if dep2_code == "0":
                    print("5")
                    #只选择了医院和科室，传回此科室的所有医生
                    dep2s = Department.objects.filter(level=dep1_code).values("id")
                    print(dep2s)
                    doc_dep = Doctor_Department.objects.filter(department_id_id__in=dep2s).values("doctor_id_id")
                    print(doc_dep)
                    docs = docs.filter(id__in=doc_dep)
                    print(docs)
                    return render(request, 'doctor_search_results2.html', {'docs': docs})
                else:
                    print("6")
                    dep2s_2 = Department.objects.filter(code=dep2_code).values("id")
                    print(dep2s_2)
                    doc_dep_2 = Doctor_Department.objects.filter(department_id_id__in=dep2s_2).values("doctor_id_id")
                    print(doc_dep_2)
                    docs = docs.filter(id__in=doc_dep_2)
                    print(docs)
                    # global DOCS
                    # DOCS = docs

                    return render(request, 'doctor_search_results2.html', {'docs': docs})
    else:
        raise Http404

def setToBeRe(request):
    print("set to_be_registered")
    if request.method == "POST":
        dates = request.POST.get("dateTime").split(',')  #It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format
        capacity = request.POST.get("capacity")
        doc_id = request.POST.get("doc")

        print(dates)
        print(doc_id)
        for date in dates:
            t = date.strip()
            t = t.split("/")
            date_format = t[2]+"-"+t[0]+"-"+t[1]+" 23:59:59"
            print(date_format)
            ToBeRegistered.objects.create(date=date_format, capacity=capacity, doctor_id_id=doc_id ).save()
        return HttpResponse('ok')
    else:
        raise Http404


def show_to_be_registered_for_doc(request):
    print("show to be regis")

    if request.method == "POST":
        doc_id = request.POST.get('doc_id')
        print(doc_id)
        toBeRs = ToBeRegistered.objects.filter(doctor_id_id = doc_id)

        return render(request, 'to_be_regis_for_doc.html', {'toBeRs': toBeRs})
    else:
        raise  Http404


def alter_to_be_registered(request):
    print("alter to be regis")

    if request.method == "POST":
        toBeR = request.POST.get('toBeR')
        capacity = request.POST.get('capacity')
        dateTime = request.POST.get('dateTime')
        t = dateTime.split("/")
        date = t[2]+"-"+t[0]+"-"+t[1]+" 23:59:59"
        print(toBeR)

        if capacity == '0':
            ToBeRegistered.objects.get(id = toBeR).delete()
        else:
            tmp = ToBeRegistered.objects.get(id=toBeR)
            tmp.capacity = capacity
            tmp.date = date
            tmp.save()

        return HttpResponse("ok~")
    else:
        raise  Http404


def reservation(request):
    print("reservation")

    dep1 = Department.objects.filter(level=0)

    #从request中得到hos_id,dep2_id,doc_id,date
    #显示已预约信息：选择区县、医院、科室、医生、日期，显示已预约信息

    return render_to_response('reservation.html',{'dep1s':dep1})

def show_reservation(request):

    if request.method == "POST":
        doc_id = request.POST.get('doc')
        date = request.POST.get('date')
        print(doc_id)
        print(date)

        t = date.strip()
        t = t.split("/")
        date_format = t[2] + "-" + t[0] + "-" + t[1] + " 23:59:59"
        print(date_format)

        res = Reservation.objects.filter(doctor_id_id=doc_id,date=date_format,ifJiuZhen=False)
        print(res)

        return render_to_response('reservation_list.html',{'res': res})
    else:
        raise Http404

def del_reservation_for_admin(request,re_id):
    print("del reservation for admin")

    re = Reservation.objects.get(id=re_id)

    try:
        to = ToBeRegistered.objects.get(id=re.toBeR_id)
    except:
        re.delete()
    else:
        to.capacity = to.capacity + 1
        to.save()
        re.delete()

    print("del reservation successfully!")

    return HttpResponse("取消成功！")


def jiuZhen(request,re_id):
    print("jiuzhen")

    re = Reservation.objects.get(id=re_id)
    re.ifJiuZhen = True
    re.save()

    return HttpResponse("就诊成功！")




########################################################
########################################################



########################################################
########################################################
##这是后台和前台的分割线,以下是User部分


#用户挂号功能，点击某天的某个医生（传入toBeRegistered_id），进行挂号操作（生成挂号订单，跳转支付页面，支付成功后生成挂号单）
def show_reservation_order(request):
    print("show reservation order")
    if not request.method == "POST":
        raise Http404
    elif request.session['type']=="user":
        toBeRegistered_id = request.POST.get('tobeR_id')
        user_id = request.session['id']
        #user_id = 1
        #toBeRegistered_id = 1

        user = User.objects.get(id=user_id)
        toBeRegistered = ToBeRegistered.objects.get(id=toBeRegistered_id)

        if toBeRegistered.capacity == 0:
            return HttpResponse("此医生已约满！")

        else:

            #reservation_order = ReservationOrder.objects.create(toBeRegistered_id_id=toBeRegistered_id,user_id_id=user_id)
            #reservation_order.save()

            #cap = toBeRegistered.capacity
            #toBeRegistered.capacity = cap - 1

            #toBeRegistered.save()

            doc = toBeRegistered.doctor_id
            dep2 = Doctor_Department.objects.get(doctor_id=doc).department_id
            dep1 = Department.objects.get(id=dep2.level)
            hos = Doctor_Hospital.objects.get(doctor_id=doc).hospital_id




            #挂号订单显示：User（用户姓名，身份证，手机号），（医院名字，科室，医生信息），（应就诊时间，订单生成时间）
            return render_to_response('reservation_order.html',{'user': user,
                                                            'doc': doc, 'dep1':dep1, 'dep2':dep2, 'hos':hos,
                                                            'toBeRegistered': toBeRegistered,
                                                            })
    else:
        return HttpResponse("还未登录!")


def creat_reservation_order(request):
    print("creat reservation order")

    if request.method == "POST":

        doc_id = request.POST.get('doc_id')
        date = request.POST.get('date')
        print(date)
        user_id = request.POST.get('user_id')
        toBeRegistered_id = request.POST.get('toBeRegistered_id')

        reservation_order = ReservationOrder.objects.create(toBeRegistered_id_id=toBeRegistered_id,user_id_id=user_id)
        reservation_order.save()

        toBeRegistered = ToBeRegistered.objects.get(id=toBeRegistered_id)
        cap = toBeRegistered.capacity
        toBeRegistered.capacity = cap - 1
        toBeRegistered.save()


        return render_to_response('pay.html',{
                                              'doc_id': doc_id,
                                              'user_id': user_id,
                                              'date': date,
                                              'reservation_order': reservation_order})

    else:
        raise Http404


def creat_reservation(request):
    print("creat reservation")

    if request.method == "POST":
        toBeR_id = request.POST.get('toBeR_id')
        print(toBeR_id)
        doc_id = request.POST.get('doc_id')
        date = request.POST.get('date')
        print(date)
        user_id = request.POST.get('user_id')

        print(doc_id)
        print(user_id)

        Reservation.objects.create(doctor_id_id=doc_id,
                                   user_id_id=user_id,
                                   ifValid=True,
                                   date=date,
                                   toBeR_id=toBeR_id
                                   ).save()

        #挂号单生成成功以后删除临时订单
        ReservationOrder.objects.get(id=request.POST['reservation_order_id']).delete()

        return HttpResponse("挂号成功！")
    else:
        raise Http404


def del_reservation(request):
    print("del reservation")
    if request.method == "POST":

        reservation_id = request.POST.get('reservation_id')

        re = Reservation.objects.get(id=reservation_id)

        try:
            to = ToBeRegistered.objects.get(id=re.toBeR_id)
        except:
            re.delete()
        else:
            to.capacity = to.capacity + 1
            to.save()
            re.delete()

        print("del reservation successfully!")

        return HttpResponseRedirect("/OnlineRegister/show_user_info/")

    else:
        raise Http404





#用户个人信息查看页面：个人信息、预约订单查看、挂号单查看和操作
def show_user_info(request):
    print("show user info")
    if request.session['type'] == "user":
        user_id = request.session['id']
        user = User.objects.get(id=user_id)
        reservation_orders = user.reservationorder_set.all()
        reservations = user.reservation_set.all()

        print(reservation_orders)
        print(reservations)



        return render_to_response('user_info.html',{'user': user,
                                                    'reservation_orders': reservation_orders,
                                                    'reservations': reservations
                                                    })
    else:
        raise Http404

def alter_user_info(request):
    print("alter user info")

    if request.method == "POST":


        if request.session['type'] == "user":
            user = User.objects.get(id=request.session['id'])
            user.name = request.POST.get('name')
            user.sex = request.POST.get('sex')
            user.phone_number = request.POST.get('phone')
            user.save()
            return HttpResponseRedirect("/OnlineRegister/show_user_info/")
        else:
            return Http404
    else:
        raise Http404



#非注册用户和注册用户都能浏览的页面，主要是医院、科室、医生和可预约容量查询
def show_hos_list(requset):
    return render_to_response('hos_list.html')

def show_dep_list(request,hos_id):

    hos = Hospital.objects.get(id=hos_id)
    dep1 = Department.objects.filter(level=0)

    return render_to_response('dep_to_be_regis.html', {'hos':hos ,'departments_1':dep1} )


def show_capacity_for_dep(request):
    if request.method == "POST":
        hos_id = request.POST.get('hos_id')
        dep2_id = request.POST.get('dep2_id')
        print(hos_id)
        print(dep2_id)

        doc = Doctor_Hospital.objects.filter(hospital_id_id = hos_id).values('doctor_id')
        doc_dep = Doctor_Department.objects.filter(doctor_id__in=doc,department_id_id=dep2_id).values('doctor_id')
        tobeR = ToBeRegistered.objects.filter(doctor_id__in=doc_dep).order_by('date')
        dates = tobeR.values('date')
        print(tobeR)
        print(dates)

        date_c = []
        cap_c = []

        for da in dates :
            count = 0
            print("..1")
            print(da.get('date'))

            for to in tobeR :
                print("..2")
                print(to.date)
                if to.date == da.get('date') :
                    print("..3")
                    count = count + to.capacity
                    #print(count)
                    #dic = (to.date, count)
                    #print(dic)
                    #cap.add(dic)
            if not da.get('date') in date_c:
                date_c.append(da.get('date'))
                cap_c.append(count)

        print(date_c)
        print(cap_c)

        #计算出每天，医院这个科室所有医生的容量总和

        return render(request,'capacity_for_dep2.html',{'dates': date_c,
                                                        'caps': cap_c,
                                                        'dep2_id': dep2_id,
                                                        'hos_id': hos_id})
    else:
        raise Http404

def show_doc_list(request):
    if request.method == "POST":
        #toBeRs = request.POST.get('toBeR')
        hos_id = request.POST.get('hos_id')
        dep2_id = request.POST.get('dep2_id')
        date = request.POST.get('date')
        #print(toBeRs)说明前端传回后端的只能是str
        print(date)

        if not request.session['type'] == "user":
            user_id = 0
        else:
            user_id = request.session['id']
        print(user_id)

        #筛选出这个医院这个科室的医生所选日期的toBeR对象传入
        doc = Doctor_Hospital.objects.filter(hospital_id_id=hos_id).values('doctor_id')
        doc_dep = Doctor_Department.objects.filter(doctor_id__in=doc, department_id_id=dep2_id).values('doctor_id')
        tobeR = ToBeRegistered.objects.filter(doctor_id__in=doc_dep,date=date)

        print(tobeR)


        return render_to_response('capacity_for_doc.html',{'user_id': user_id,
                                                           'tobeRs': tobeR})
    else:
        raise Http404













