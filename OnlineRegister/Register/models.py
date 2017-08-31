from django.db import models

# Create your models here.

#可登入系统的用户
##普通注册用户
class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    sex = models.IntegerField()
    phone_number = models.CharField(max_length=50, null=False)
    id_number = models.CharField(max_length=50, null=False)
    creditMark = models.IntegerField()

##医院挂号处,理论上每个医院一个
class Registry(models.Model):
    name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)

##分诊台,理论上医院一般每楼层一个分诊台
class Triage(models.Model):
    name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)

##系统管理员
class Admin(models.Model):
    name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)

class Hospital(models.Model):
    name = models.CharField(max_length=50, null=False)
    code = models.CharField(max_length=50, null=False)
    district = models.IntegerField() #所属行政区代码,例如北京市东城区为110101


#医院科室，按一级二级分类，如内科是一级，神经内科是二级,二级科室有一级科室的code为前缀
class Department(models.Model):
    name = models.CharField(max_length=50, null=False)
    code = models.CharField(max_length=50, null=False)
    level = models.IntegerField() #level值为0表示为一级科室，>0表示为二级，且数字代表其一级科室的code

class Department_Triage(models.Model):
    department_id = models.ForeignKey(Department)
    triage_id = models.ForeignKey(Triage)

class Doctor(models.Model):
    name = models.CharField(max_length=50, null=False)
    sex = models.IntegerField()
    position = models.CharField(max_length=50)
    phone_number = models.IntegerField()

class Registry_Hospital(models.Model):
    registry_id = models.ForeignKey(Registry)
    hospital_id = models.ForeignKey(Hospital)

class Triage_Hospital(models.Model):
    triage_id = models.ForeignKey(Triage)
    hospital_id = models.ForeignKey(Hospital)
    triage_number = models.IntegerField()

class Doctor_Hospital(models.Model):
    doctor_id = models.ForeignKey(Doctor)
    hospital_id = models.ForeignKey(Hospital)

#医生所属的二级科室
class Doctor_Department(models.Model):
    doctor_id = models.ForeignKey(Doctor)
    department_id = models.ForeignKey(Department)

#医生某天可预约的空位
class ToBeRegistered(models.Model):
    doctor_id = models.ForeignKey(Doctor)
    date = models.DateTimeField(auto_now_add=False, null=True)
    capacity = models.IntegerField()

class ReservationOrder(models.Model):
    toBeRegistered_id = models.ForeignKey(ToBeRegistered)
    user_id = models.ForeignKey(User)
    createdTime = models.DateTimeField(auto_now_add=True, null=False)

class Reservation(models.Model):
    toBeR_id = models.IntegerField(null=True)
    doctor_id = models.ForeignKey(Doctor)
    date = models.DateTimeField(auto_now_add=False, null=True)
    user_id = models.ForeignKey(User)
    createdTime = models.DateTimeField(auto_now_add=True, null=False)
    ifValid = models.BooleanField()
    ifJiuZhen = models.BooleanField(default=False)
