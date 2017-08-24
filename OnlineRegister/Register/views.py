from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, render_to_response


# Create your views here.
from Register.models import *


def index(request):
    return render_to_response("index.html")

def register(request):
    return

def login(request):
    return

def adminLogin(request):
    if 'name' in request.POST and request.POST['name']\
        and 'password' in request.POST and request.POST['password']\
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

def alter_hospital_select1(request):
    print("alter hospital 1")
    if request.method == "POST":
        district_code = request.POST.get('district')
        print(district_code)
        hospitals = Hospital.objects.filter(district=district_code)

        return render(request, 'hospital_options.html', {'hospitals': hospitals})
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

