from django.shortcuts import render
from django.http import HttpResponse
from .models import h1b_1
from subprocess import run,PIPE
import sys

def index(request):
    return render(request, "h1b_app/home.html")

def visa_page(request):
    return render(request, "h1b_app/visa_page.html")
def h1b_form1(request):
    return render (request, "h1b_app/index.html")

name = ""
gender = ""
dob = ""
res = ""
nationality = ""
name_org=""
is_uni=""
job_title=""
fulltime=""
salary=""
company_address=""
occupation=""
hours_per_week=""

def h1b_page2(request):
    global name, gender, dob, res, nationality
    first_name = request.POST["first_name"]
    middle_name = request.POST["middle_name"]
    last_name = request.POST["last_name"]
    
    name = first_name + " " + middle_name + " " + last_name
    
    gender = request.POST["gender"]
    dob = request.POST["dob"]
    res = request.POST["res"]
    nationality = request.POST["nationality"]

    return render (request, "h1b_app/h1b_page2.html")

    
def h1b_page3(request):
    global name_org, is_uni, company_address
    name_org = request.POST["name_org"]
    is_uni = request.POST["uni"]
    company_address=request.POST["company_address"]
    
    return render (request, "h1b_app/h1b_page3.html")

def save_form(request):
    global job_title, fulltime, salary, occupation
    job_title = request.POST["job_title"]
    fulltime = request.POST["fulltime"]
    salary = request.POST["salary"]
    occupation = request.POST["occupation"]
    hours_per_week = request.POST["hours_per_week"]
    
    h1b_info = h1b_1(ben_name=name, ben_dob=dob, ben_gender=gender, ben_addr=res, nationality=nationality, job_title=job_title, hours_per_week=hours_per_week, salary=salary, employer_name=name_org, occupation=occupation, full_time_position=fulltime, location=company_address, is_uni=is_uni )
    h1b_info.save()
    
    return render (request, "h1b_app/congrats.html")

def result(request):

    out=run([sys.executable,'C://Users//Lenovo//Desktop//assignments//sl1//H1B_prediction//h1b_app//h1b_pred.py' , fulltime,  company_address, name_org, occupation, salary], shell=False, stdout=PIPE)
    
    return render (request, "h1b_app/result.html", {'data1':out.stdout})
