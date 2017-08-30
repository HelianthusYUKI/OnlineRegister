from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, render_to_response


# Create your views here.
from Register.models import *
# import time

# DOCS = 0

def index(request):
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
                #return render_to_response("")
                return HttpResponse("登录成功！")
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
    return render_to_response('reservation.html')