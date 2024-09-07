from .models import Employees, Department, Position, Point
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.http import HttpResponse
from employee_information.models import Activity, Department, Position, Employees, ActivityRule, Score, EmpUsers, Point
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend


employees = [

    {
        'code': 1,
        'name': "John D Smith",
        'contact': '09123456789',
        'address': 'Sample Address only'
    }, {
        'code': 2,
        'name': "Claire C Blake",
        'contact': '09456123789',
        'address': 'Sample Address2 only'
    }

]

# Front End


def main(request):
    return render(request, "front_end/home.html")

# Login


def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')

# Logout


def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.


@login_required
def home(request):
    context = {
        'page_title': 'Home',
        'employees': employees,
        'total_department': len(Department.objects.all()),
        'total_position': len(Position.objects.all()),
        'total_employee': len(Employees.objects.all()),
        'total_activity': len(Activity.objects.all()),
        'total_activity_rules': len(ActivityRule.objects.all()),
        'total_scores': len(Score.objects.all()),
    }
    return render(request, 'employee_information/home.html', context)


def about(request):
    context = {
        'page_title': 'About',
    }
    return render(request, 'employee_information/about.html', context)

# Departments


@login_required
def departments(request):
    department_list = Department.objects.all()
    context = {
        'page_title': 'Departments',
        'departments': department_list,
    }
    return render(request, 'employee_information/departments.html', context)


@login_required
def manage_departments(request):
    department = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            department = Department.objects.filter(id=id).first()

    context = {
        'department': department
    }
    return render(request, 'employee_information/manage_department.html', context)


@login_required
def save_department(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_department = Department.objects.filter(id=data['id']).update(
                name=data['name'], description=data['description'], status=data['status'])
        else:
            save_department = Department(
                name=data['name'], description=data['description'], status=data['status'])
            save_department.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_department(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Department.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Positions


def positions(request):
    position_list = Position.objects.all()
    context = {
        'page_title': 'Positions',
        'positions': position_list,
    }
    return render(request, 'employee_information/positions.html', context)


@login_required
def manage_positions(request):
    position = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            position = Position.objects.filter(id=id).first()

    context = {
        'position': position
    }
    return render(request, 'employee_information/manage_position.html', context)


@login_required
def save_position(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_position = Position.objects.filter(id=data['id']).update(
                name=data['name'], description=data['description'], status=data['status'])
        else:
            save_position = Position(
                name=data['name'], description=data['description'], status=data['status'])
            save_position.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_position(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Position.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Employees


def employees(request):
    employee_list = Employees.objects.all()
    context = {
        'page_title': 'Employees',
        'employees': employee_list,
    }
    return render(request, 'employee_information/employees.html', context)


@login_required
def manage_employees(request):
    employee = {}
    departments = Department.objects.filter(status=1).all()
    positions = Position.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'departments': departments,
        'positions': positions
    }
    return render(request, 'employee_information/manage_employee.html', context)


@login_required
def save_employee(request):
    data = request.POST
    resp = {'status': 'failed'}

    if data['id'].isnumeric() and int(data['id']) > 0:
        check = Employees.objects.exclude(
            id=data['id']).filter(code=data['code'])
    else:
        check = Employees.objects.filter(code=data['code'])

    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            dept = Department.objects.filter(id=data['department_id']).first()
            pos = Position.objects.filter(id=data['position_id']).first()

            if data['id'].isnumeric() and int(data['id']) > 0:
                employee = Employees.objects.get(id=data['id'])
                employee.code = data['code']
                employee.firstname = data['firstname']
                employee.middlename = data['middlename']
                employee.lastname = data['lastname']
                employee.dob = data['dob']
                employee.gender = data['gender']
                employee.contact = data['contact']
                employee.email = data['email']
                employee.address = data['address']
                employee.department_id = dept
                employee.position_id = pos
                employee.date_hired = data['date_hired']
                employee.salary = data['salary']
                employee.status = data['status']
                employee.save()
            else:
                employee = Employees.objects.create(
                    code=data['code'],
                    firstname=data['firstname'],
                    middlename=data['middlename'],
                    lastname=data['lastname'],
                    dob=data['dob'],
                    gender=data['gender'],
                    contact=data['contact'],
                    email=data['email'],
                    address=data['address'],
                    department_id=dept,
                    position_id=pos,
                    date_hired=data['date_hired'],
                    salary=data['salary'],
                    status=data['status']
                )

            # Create Point object for the newly saved employee with 0 points
            Point.objects.create(user_id=employee.code, points=0)

            resp['status'] = 'success'
        except Exception as e:
            resp['status'] = 'failed'
            print(e)
            print(json.dumps({
                "code": data['code'],
                "firstname": data['firstname'],
                "middlename": data['middlename'],
                "lastname": data['lastname'],
                "dob": data['dob'],
                "gender": data['gender'],
                "contact": data['contact'],
                "email": data['email'],
                "address": data['address'],
                "department_id": data['department_id'],
                "position_id": data['position_id'],
                "date_hired": data['date_hired'],
                "salary": data['salary'],
                "status": data['status']
            }))

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_employee(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Employees.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def view_employee(request):
    employee = {}
    departments = Department.objects.filter(status=1).all()
    positions = Position.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'departments': departments,
        'positions': positions
    }
    return render(request, 'employee_information/view_employee.html', context)
# activiity started


def activity(request):
    activity_list = Activity.objects.all()
    context = {
        'page_title': 'Activities',
        'activity': activity_list,
    }
    return render(request, 'employee_information/activity.html', context)


@login_required
def manage_activity(request):
    activity = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            activity = Activity.objects.filter(id=id).first()

    context = {
        'activity': activity
    }
    return render(request, 'employee_information/manage_activity.html', context)


@login_required
def save_activity(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_activity = Activity.objects.filter(id=data['id']).update(
                name=data['name'], description=data['description'], status=data['status'])
        else:
            save_activity = Activity(
                name=data['name'], description=data['description'], status=data['status'])
            save_activity.save()
        resp['status'] = 'success'
    except Exception:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_activity(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Activity.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Activity rules started

def activity_rules(request):
    activity_rules_list = ActivityRule.objects.all()
    context = {
        'page_title': 'Activities_rules',
        'activity_rules': activity_rules_list,
    }
    return render(request, 'employee_information/activity_rules.html', context)


@login_required
def manage_activity_rules(request):
    activity_rules = {}
    activity = Activity.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            activity_rules = ActivityRule.objects.filter(id=id).first()

    context = {
        'activity_rules': activity_rules,
        'activity': activity
    }
    return render(request, 'employee_information/manage_activity_rules.html', context)


@login_required
def save_activity_rules(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        act = Activity.objects.filter(id=data['activity_id']).first()
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_activity_rules = ActivityRule.objects.filter(id=data['id']).update(
                name=data['name'], points=data['points'], activity_id=act, min_score=data['min_score'], max_score=data['max_score'], operator=data['operator'], status=data['status'])
        else:
            save_activity_rules = ActivityRule(
                name=data['name'], points=data['points'], activity_id=act, min_score=data['min_score'], max_score=data['max_score'], operator=data['operator'], status=data['status'])
            save_activity_rules.save()
        resp['status'] = 'success'
    except Exception:
        resp['status'] = 'failed'
        print(Exception)
        print(json.dumps({"department_id": data['department_id']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_activity_rules(request):
    data = request.POST
    resp = {'status': ''}
    try:
        ActivityRule.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# activity rules end

# Scores started
def scores(request):
    scores_list = Score.objects.all()
    context = {
        'page_title': 'Scores',
        'scores': scores_list,
    }
    return render(request, 'employee_information/scores.html', context)


@login_required
def manage_scores(request):
    scores = {}
    activity = Activity.objects.filter(status=1).all()
    activity_rules = ActivityRule.objects.filter(status=1).all()
    employees = Employees.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            scores = Score.objects.filter(id=id).first()

    context = {
        'scores': scores,
        'activity': activity,
        'activity_rules': activity_rules,
        'employees': employees,

    }
    return render(request, 'employee_information/manage_scores.html', context)


def save_scores(request):
    data = request.POST
    resp = {'status': 'failed'}

    try:
        act = Activity.objects.filter(id=data['activity_id']).first()
        act_rules = ActivityRule.objects.filter(
            id=data['activity_rule_id']).first()
        emp1 = Employees.objects.filter(id=data['emp_id']).first()
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_scores = Score.objects.filter(id=data['id']).update(
                emp_id=emp1, activity_id=act, activity_rule_id=act_rules, score=data['score'], status=data['status'])
        else:
            save_scores = Score(
                emp_id=emp1, activity_id=act, activity_rule_id=act_rules, score=data['score'], status=data['status'])
            save_scores.save()
        points = act_rules.points
        scores = Score.objects.filter(emp_id=emp1).first()
        if act_rules.operator == "<=" and scores.score <= act_rules.max_score:
            emp_points = Point.objects.filter(user_id=emp1.code).first()
            if emp_points:
                emp_points.points += points
                emp_points.save()
        resp['status'] = 'success'
    except Exception:
        resp['status'] = 'failed'
        print(Exception)
        print(json.dumps({"activity_id": data['activity_id']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")

# def save_scores(request):
#     data = request.POST
#     resp = {'status': 'failed'}

#     try:
#         act = Activity.objects.filter(id=data['activity_id']).first()
#         act_rules = ActivityRule.objects.filter(
#             id=data['activity_rule_id']).first()
#         emp1 = Employees.objects.filter(id=data['emp_id']).first()
#         if (data['id']).isnumeric() and int(data['id']) > 0:
#             save_scores = Score.objects.filter(id=data['id']).update(
#                 emp_id=emp1, activity_id=act, activity_rule_id=act_rules, score=data['score'], status=data['status'])
#         else:
#             save_scores = Score(
#                 emp_id=emp1, activity_id=act, activity_rule_id=act_rules, score=data['score'], status=data['status'])
#             save_scores.save()

#             # Calculate and add points based on the activity rule
#             points = act_rules.points
#             if act_rules.operator == "<=" and save_scores.score <= act_rules.max_score:
#                 emp_points = Point.objects.filter(user_id=emp1.id).first()
#                 if emp_points:
#                     emp_points.points += points
#                     emp_points.save()
#                 else:
#                     Point.objects.create(user_id=emp1.id, points=points)
#             elif act_rules.operator == ">=" and save_scores.score >= act_rules.min_score:
#                 emp_points = Point.objects.filter(user_id=emp1.id).first()
#                 if emp_points:
#                     emp_points.points += points
#                     emp_points.save()
#                 else:
#                     Point.objects.create(user_id=emp1.id, points=points)

#         resp['status'] = 'success'
#     except Exception:
#         resp['status'] = 'failed'
#         print(Exception)
#         print(json.dumps({"activity_id": data['activity_id']}))
#     return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_scores(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Score.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Scores ended


# Usersdef

    # assuming email is entered in a form fieldfrom django.shortcuts import render, redirect

    # User


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Retrieve user with the specified email and password
        user = EmpUsers.objects.filter(email=email, password=password).first()

        if user is not None:
            # Email and password are correct, proceed with login
            # Set user session data for example: request.session['user_id'] = user.id
            # Redirect to user's profile page
            return redirect('pro', email=email)

        else:
            # Email and/or password are incorrect, show error message
            return render(request, 'user_end/uslogin.html', {'error': 'Invalid email or password'})

    return render(request, 'user_end/uslogin.html')
    # Profile
    # ==================================================================


def pro(request, email):
    Employee = Employees.objects.filter(email=email)
    context = {
        'page_title': 'Profile',
        'Employees': Employee,
    }
    return render(request, 'user_end/profile.html', context)
