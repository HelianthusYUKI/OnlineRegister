
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
    url(r'^alter_hospital_select1/$',alter_hospital_select1),
    url(r'^alter_hospital_select2/$',alter_hospital_select2),
    url(r'^alter_hospital/$',alter_hospital),
    url(r'^del_hospital/$',del_hospital),

]