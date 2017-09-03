
from django.conf.urls import url, include
from django.contrib import admin
from Register.views import *

urlpatterns = [


    url(r'^$',index),
    url(r'^login/$',login),
    url(r'^admin_login/$',adminLogin),
    url(r'^register/$',register),

    url(r'^header.html$',header),
    url(r'^admin_left.html$',admin_left),

    url(r'^admin_hos_wh/$',admin_hos_wh),
    url(r'^hospital_search/$',hospital_search),
    url(r'^add_hospital/$',add_hospital),
    url(r'^alter_hospital_select1_1/$',alter_hospital_select1_1),
url(r'^alter_hospital_select1_2/$',alter_hospital_select1_2),
    url(r'^alter_hospital_select2/$',alter_hospital_select2),
    url(r'^alter_hospital/$',alter_hospital),
    url(r'^del_hospital/$',del_hospital),

    url(r'^show_dep2/$',show_dep2),
url(r'^show_dep2_2/$',show_dep2_2),

    url(r'^show_department/$',show_department),
    url(r'^add_department/$',add_dep),
    url(r'^alter_department/$',alter_dep),
    url(r'^del_department/$',del_dep),

    url(r'^show_doctor/$',show_doctor),
    url(r'^search_doctor/$',search_doctor),
    url(r'^add_doctor/$',add_doc),
    url(r'^alter_doctor/$',alter_doc),
    url(r'^del_doctor/$',del_doc),

    url(r'^to_be_registered/$',toBeRegistered),
url(r'^search_doctor2/$', search_doctor2),
    url('^set_to_be_re/$',setToBeRe),
    url('^show_to_be_registered_for_doc/$',show_to_be_registered_for_doc),
    url('^alter_to_be_registered/$',alter_to_be_registered),


    url(r'^reservation/$',reservation),
    url(r'^show_reservation/$',show_reservation),
    url(r'^del_reservation_for_admin/(\d+)/$',del_reservation_for_admin),
    url(r'^jiuZhen/(\d+)/$',jiuZhen),

    url(r'^show_reservation_order/$',show_reservation_order),
    url(r'^creat_reservation_order/$',creat_reservation_order),
    url(r'^creat_reservation/$',creat_reservation),
    url(r'^del_reservation/$',del_reservation),
    url(r'^show_user_info/$',show_user_info),
    url(r'^alter_user_info/$',alter_user_info),

    url(r'^show_hos_list/$',show_hos_list),
    url(r'^show_dep_list/(\d+)/$',show_dep_list),
    url(r'^show_capacity_for_dep/$',show_capacity_for_dep),
    url(r'^show_doc_list/$',show_doc_list),


]