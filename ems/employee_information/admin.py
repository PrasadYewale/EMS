from django.contrib import admin
from employee_information.models import Department, Position, Employees, ActivityRule, Activity, Product, Score, EmpUsers, Point

# Register your models here.
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employees)
admin.site.register(Activity)
admin.site.register(ActivityRule)
admin.site.register(Point)
admin.site.register(Product)
admin.site.register(Score)
admin.site.register(EmpUsers)
