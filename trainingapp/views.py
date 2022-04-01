from django. contrib import messages
from unicodedata import name
from django.shortcuts import render
from django.shortcuts import render, redirect
from trainingapp.models import *
from datetime import datetime,date
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from io import BytesIO
from django.core.files import File
from django.conf import settings
import qrcode
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def login(request):
    des = designation.objects.get(designation_name='manager')
    des1 = designation.objects.get(designation_name='trainer')
    des2 = designation.objects.get(designation_name='trainee')
    des3 = designation.objects.get(designation_name='accounts')

    if request.method == 'POST':
        
        email  = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
                request.session['SAdm_id'] = user.id
                return redirect( 'Admin_Dashboard')
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['m_designation_id'] = member.designation_id
                request.session['m_fullname'] = member.fullname
                request.session['m_id'] = member.id
                return render(request, 'dashsec.html', {'member': member})
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des1.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['tr_designation_id'] = member.designation_id
                request.session['tr_fullname'] = member.fullname
                request.session['tr_team_id'] = member.team_id
                request.session['tr_id'] = member.id
                return render(request, 'tr_sec.html', {'member': member})
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des2.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['te_designation_id'] = member.designation_id
                request.session['te_fullname'] = member.fullname
                request.session['te_id'] = member.id
                request.session['te_team_id'] = member.team_id
                return render(request, 'traineesec.html', {'member': member})
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des3.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['acc_designation_id'] = member.designation_id
                request.session['acc_fullname'] = member.fullname
                request.session['acc_id'] = member.id
                return render(request, 'accountsec.html', {'member': member})
        else:
                context = {'msg': 'Invalid username or password'}
                return render(request, 'login.html', context)
    return render(request,'login.html')       



    
        # if request.method == 'POST':
        #     username = request.POST.get('email', None)
        #     password = request.POST.get('password', None)
        #     user = authenticate(email=username, password=password)
        #     if user:
        #         login(request, user)
        #         return redirect('Admin_Dashboard')
        #     else:
        #           context = {'msg': 'Invalid username or password'}
        #           return render(request, 'login.html',context)
        # if request.method == 'POST':
        #     email  = request.POST['email']
        #     password = request.POST['password']
        #     user = authenticate(email=email, password=password)
        #     if user is not None:
        #             request.session['SAdm_id'] = user.id
        #             return redirect('Admin_Dashboard')

        #     else:
        #         context = {'msg': 'Invalid username or password'}
        #         return render(request, 'login.html', context)
    

def manager_logout(request):
    if 'm_id' in request.session:  
        request.session.flush()
        return redirect('login')
    else:
        return redirect('login') 

def index(request):
    return render(request,'software_training/training/index.html')
    
def Trainings(request):
    return render(request,'software_training/training/training.html')

#******************Manager*****************************

def Manager_Dashboard(request):
    if 'm_id' in request.session:
        
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
       
        mem = user_registration.objects.filter(id=m_id)
        
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=m_id)
        for i in queryset:
            labels=[i.workperformance,i.attitude,i.creativity]
            data=[i.workperformance,i.attitude,i.creativity]
        return render(request, 'software_training/training/manager/manager_Dashboard.html', {'mem': mem ,'labels': labels,'data': data,})
    else:
        return redirect('/')

def Manager_trainer(request):
    return render(request,'software_training/training/manager/manager_trainer.html')

def manager_team(request):
    return render(request,'software_training/training/manager/manager_team.html')

def manager_current_team(request):
    return render(request,'software_training/training/manager/manager_current_team.html')

def Manager_current_task(request):
    return render(request,'software_training/training/manager/manager_current_task.html')

def manager_current_assigned(request):
    return render(request,'software_training/training/manager/manager_current_assigned.html')

def manager_current_trainees(request):
    return render(request,'software_training/training/manager/manager_current_trainees.html')

def manager_current_empdetails(request):
    return render(request,'software_training/training/manager/manager_current_empdetails.html')

def manager_current_attendance(request):
    return render(request,'software_training/training/manager/manager_current_attendance.html')

def manager_current_attendance_list(request):
    return render(request,'software_training/training/manager/manager_current_attendance_list.html')

def manager_current_task_list(request):
    return render(request,'software_training/training/manager/manager_current_task_list.html')

def manager_current_task_details(request):
    return render(request,'software_training/training/manager/manager_current_task_details.html')
    
def manager_previous_team(request):
    return render(request,'software_training/training/manager/manager_previous_team.html')

def Manager_previous_task(request):
    return render(request,'software_training/training/manager/Manager_previous_task.html')

def manager_previous_assigned(request):
    return render(request,'software_training/training/manager/manager_previous_assigned.html')

def manager_previous_trainees(request):
    return render(request,'software_training/training/manager/manager_previous_trainees.html')

def manager_previous_empdetails(request):
    return render(request,'software_training/training/manager/manager_previous_empdetails.html')

def manager_previous_attendance(request):
    return render(request,'software_training/training/manager/manager_previous_attendance.html')

def manager_previous_attendance_list(request):
    return render(request,'software_training/training/manager/manager_previous_attendance_list.html')

def manager_previous_task_list(request):
    return render(request,'software_training/training/manager/manager_previous_task_list.html')

def manager_previous_task_details(request):
    return render(request,'software_training/training/manager/manager_previous_task_details.html')

def manager_trainee(request):
    return render(request,'software_training/training/manager/manager_trainee.html')

def Manager_trainees_details(request):
    return render(request,'software_training/training/manager/Manager_trainees_details.html')

def Manager_trainees_attendance(request):
    return render(request,'software_training/training/manager/Manager_trainees_attendance.html')

def Manager_reported_issues(request):
    return render(request,'software_training/training/manager/manager_reported_issues.html')

def manager_trainerreportissue(request):
    return render(request,'software_training/training/manager/manager_trainerreportissue.html')

def manager_trainer_unsolvedissue(request):
    return render(request,'software_training/training/manager/manager_trainer_unsolvedissue.html')

def manager_trainer_solvedissue(request):
    return render(request,'software_training/training/manager/manager_trainer_solvedissue.html')

def manager_traineereportissue(request):
    return render(request,'software_training/training/manager/manager_traineereportissue.html')

def manager_trainee_unsolvedissue(request):
    return render(request,'software_training/training/manager/manager_trainee_unsolvedissue.html')

def manager_trainee_solvedissue(request):
    return render(request,'software_training/training/manager/manager_trainee_solvedissue.html')

def manager_report_issue(request):
    return render(request,'software_training/training/manager/manager_report_issue.html')

def manager_reported_issue(request):
    return render(request,'software_training/training/manager/manager_reported_issue.html')

def manager_trainee_solvedissue(request):
    return render(request,'software_training/training/manager/manager_trainee_solvedissue.html')

def Manager_attendance(request):
    return render(request,'software_training/training/manager/manager_attendance.html') 

def manager_trainee_attendance(request):
    return render(request,'software_training/training/manager/manager_trainee_attendance.html') 

def manager_trainer_attendance(request):
    return render(request,'software_training/training/manager/manager_trainer_attendance.html') 

def manager_trainer_attendance_table(request):
    return render(request,'software_training/training/manager/manager_trainer_attendance_table.html') 

def manager_trainee_attendance_table(request):
    return render(request,'software_training/training/manager/manager_trainee_attendance_table.html') 

def manager_applyleave(request):
    return render(request,'software_training/training/manager/manager_applyleave.html') 

def manager_applyleavsub(request):
    return render(request,'software_training/training/manager/manager_applyleavsub.html')

def manager_requestedleave(request):
    return render(request,'software_training/training/manager/manager_requestedleave.html')

def manager_trainer_leave(request):
    return render(request,'software_training/training/manager/manager_trainer_leave.html')

def manager_trainers_leavelist(request):
    return render(request,'software_training/training/manager/manager_trainers_leavelist.html')

def manager_trainer_leavestatus(request):
    return render(request,'software_training/training/manager/manager_trainer_leavestatus.html')

def manager_trainee_leave(request):
    return render(request,'software_training/training/manager/manager_trainee_leave.html')

def manager_trainee_leavelist(request):
    return render(request,'software_training/training/manager/manager_trainee_leavelist.html')

def manager_trainee_leavestatus(request):
    return render(request,'software_training/training/manager/manager_trainee_leavestatus.html')

def manager_new_team(request):
    return render(request,'software_training/training/manager/manager_new_team.html')

def manager_new_teamcreate(request):
    return render(request,'software_training/training/manager/manager_new_teamcreate.html')

def manager_newtrainees(request):
    return render(request,'software_training/training/manager/manager_newtrainees.html')

    
#******************Trainer*****************************

def trainer_dashboard(request):
    return render(request,'software_training/training/trainer/trainer_dashboard.html')

def trainer_applyleave(request):
    return render(request, 'software_training/training/trainer/trainer_applyleave.html')

def trainer_applyleave_form(request):
    return render(request, 'software_training/training/trainer/trainer_applyleave_form.html')

def trainer_traineesleave_table(request):
    return render(request, 'software_training/training/trainer/trainer_traineesleave_table.html')

def trainer_reportissue(request):
    return render(request, 'software_training/training/trainer/trainer_reportissue.html')

def trainer_reportissue_form(request):
    return render(request, 'software_training/training/trainer/trainer_reportissue_form.html')

def trainer_reportedissue_table(request):
    return render(request, 'software_training/training/trainer/trainer_reportedissue_table.html')

def trainer_topic(request):
    return render(request,'software_training/training/trainer/trainer_topic.html')

def trainer_addtopic(request):
    return render(request,'software_training/training/trainer/trainer_addtopic.html')

def trainer_viewtopic(request):
    return render(request,'software_training/training/trainer/trainer_viewtopic.html')

def trainer_attendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance.html')

def trainer_attendance_trainees(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees.html')

def trainer_attendance_trainer(request):
    return render(request, 'software_training/training/trainer/trainer_attendance_trainer.html')

def trainer_attendance_trainer_viewattendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainer_viewattendance.html')

def trainer_attendance_trainer_viewattendancelist(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainer_viewattendancelist.html')

def trainer_team(request):
    return render(request,'software_training/training/trainer/trainer_team.html')

def trainer_currentteam(request):
    return render(request,'software_training/training/trainer/trainer_current_team_list.html')

def trainer_currenttrainees(request):
    return render(request, 'software_training/training/trainer/trainer_current_trainees_list.html')

def trainer_currenttraineesdetails(request):
    return render(request,'software_training/training/trainer/trainer_current_tainees_details.html')

def trainer_currentattentable(request):
    return render(request,'software_training/training/trainer/trainer_current_atten_table.html')

def trainer_currentperform(request):
    return render(request,'software_training/training/trainer/trainer_current_perform.html')

def trainer_currentattenadd(request):
    return render(request,'software_training/training/trainer/trainer_current_atten_add.html')

def trainer_previousteam(request):
    return render(request,'software_training/training/trainer/trainer_previous_team_list.html')

def trainer_previoustrainees(request):
    return render(request,'software_training/training/trainer/trainer_previous_trainess_list.html')

def trainer_previoustraineesdetails(request):
    return render(request, 'software_training/training/trainer/trainer_previous_trainees_details.html')

def trainer_previousattentable(request):
    return render(request,'software_training/training/trainer/trainer_previous_atten_table.html')

def trainer_previousperfomtable(request):
    return render(request,'software_training/training/trainer/trainer_previous_performtable.html')

def trainer_current_attendance(request):
    return render(request,'software_training/training/trainer/trainer_current_attendance.html')

def trainer_Task(request) :
    return render(request,'software_training/training/trainer/trainer_task.html')
    
def trainer_teamlistpage(request) :
    return render(request,'software_training/training/trainer/trainer_teamlist.html')
    
def trainer_taskpage(request) :
    return render(request, 'software_training/training/trainer/trainer_taskfor.html')
    
def trainer_givetask(request) :
    return render(request, 'software_training/training/trainer/trainer_givetask.html')
    
def trainer_taskgivenpage(request) :
    return render(request,'software_training/training/trainer/trainer_taskgiven.html')
    
def trainer_taska(request):
    return render(request, 'software_training/training/trainer/trainer_taska.html')

def trainer_task_completed_teamlist(request):
    return render(request, 'software_training/training/trainer/trainer_task_completed_teamlist.html')

def trainer_task_completed_team_tasklist(request):
    return render(request, 'software_training/training/trainer/trainer_task_completed_team_tasklist.html')

def trainer_task_previous_teamlist(request):
    return render(request, 'software_training/training/trainer/trainer_task_previous_teamlist.html')

def trainer_task_previous_team_tasklist(request):
    return render(request, 'software_training/training/trainer/trainer_task_previous_team_tasklist.html')

def trainer_trainees(request):
    return render(request, 'software_training/training/trainer/trainer_trainees.html')

def trainer_previous_trainees(request):
    return render(request,'software_training/training/trainer/trainer_previous_trainees.html')

def trainer_current_trainees(request):
    return render(request,'software_training/training/trainer/trainer_current_trainees.html')

def trainer_myreportissue_table(request):
    return render(request, 'software_training/training/trainer/trainer_myreportissue_table.html')

def trainer_current_attendance_view(request):
    return render(request,'software_training/training/trainer/trainer_current_attendance_view.html')

def trainer_attendance_trainees_viewattendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees_viewattendance.html')

def trainer_attendance_trainees_viewattendancelist(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees_viewattendancelist.html')

def trainer_attendance_trainees_addattendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees_addattendance.html')
    
#******************  Trainee  *****************************

def trainee_dashboard_trainee(request):
    return render(request,'software_training/training/trainee/trainee_dashboard_trainee.html')
    
def trainee_task(request):
   return render(request,'software_training/training/trainee/trainee_task.html')   

def trainee_task_list(request):
    return render(request,'software_training/training/trainee/trainee_task_list.html')

def trainee_task_details(request):
    return render(request,'software_training/training/trainee/trainee_task_details.html')

def trainee_completed_taskList(request):
   return render(request,'software_training/training/trainee/trainee_completed_taskList.html')

def trainee_completedTask(request):
    return render(request,'software_training/training/trainee/trainee_completedTask.html')

def trainee_completed_details(request):
    return render(request,'software_training/training/trainee/trainee_completed_details.html')

def trainee_topic(request):
    return render(request, 'software_training/training/trainee/trainee_topic.html')

def trainee_currentTopic(request):
    return render(request, 'software_training/training/trainee/trainee_currentTopic.html')
    
def trainee_previousTopic(request):
    return render(request, 'software_training/training/trainee/trainee_previousTopic.html')

def trainee_reported_issue(request):
    return render(request, 'software_training/training/trainee/trainee_reported_issue.html')
   
def trainee_report_reported(request):
    return render(request, 'software_training/training/trainee/trainee_report_reported.html')
  
def trainee_report_issue(request):
    return render(request, 'software_training/training/trainee/trainee_report_issue.html')

def trainee_applyleave_form(request):
    return render(request, 'software_training/training/trainee/trainee_applyleave_form.html')  

def trainee_applyleave_card(request):
     return render(request, 'software_training/training/trainee/trainee_applyleave_cards.html')
    
def trainee_appliedleave(request):
     return render(request, 'software_training/training/trainee/trainee_appliedleave.html')
    
def Attendance(request):
   return render(request,'software_training/training/trainee/trainees_attendance.html')
    
def trainees_attendance_viewattendance(request):
    return render(request,'software_training/training/trainee/trainees_attendance_viewattendance.html')
 
def trainees_attendance_viewattendancelist(request):
   return render(request,'software_training/training/trainee/trainees_attendance_viewattendancelist.html')
   
def trainee_payment(request):
   return render(request,'software_training/training/trainee/trainee_payment.html')
   
def trainee_payment_addpayment(request):
   return render(request,'software_training/training/trainee/trainee_payment_addpayment.html')
  
def trainee_payment_viewpayment(request):
     return render(request,'software_training/training/trainee/trainee_payment_viewpayment.html')

#****************************  Admin- view  ********************************

def Admin_Dashboard(request):
    return render(request,'software_training/training/admin/admin_Dashboard.html')

def Admin_categories(request):
    return render(request,'software_training/training/admin/admin_categories.html') 

def Admin_emp_categories(request):
    return render(request,'software_training/training/admin/admin_emp_categories.html')  

def Admin_courses(request):
    return render(request,'software_training/training/admin/admin_courses.html')

def Admin_emp_course_list(request):
    return render(request,'software_training/training/admin/admin_emp_course_list.html')

def Admin_emp_course_details(request):
    return render(request,'software_training/training/admin/admin_emp_course_details.html')

def Admin_emp_profile(request):
    return render(request,'software_training/training/admin/admin_emp_profile.html')

def Admin_emp_attendance(request):
    return render(request,'software_training/training/admin/admin_emp_attendance.html')

def Admin_emp_attendance_show(request):
    return render(request,'software_training/training/admin/admin_emp_attendance_show.html')

def Admin_task(request):
    return render(request,'software_training/training/admin/admin_task.html')

def Admin_givetask(request):
    return render(request,'software_training/training/admin/admin_givetask.html')

def Admin_current_task(request):
    return render(request,'software_training/training/admin/admin_current_task.html')

def Admin_previous_task(request):
    return render(request,'software_training/training/admin/admin_previous_task.html')

def Admin_registration_details(request):
    return render(request,'software_training/training/admin/admin_registration_details.html')  

def Admin_attendance(request):
    return render(request,'software_training/training/admin/admin_attendance.html') 

def Admin_attendance_show(request):
    return render(request,'software_training/training/admin/admin_attendance_show.html')

def Admin_reported_issues(request):
    return render(request,'software_training/training/admin/admin_reported_issues.html') 

def Admin_emp_reported_detail(request):
    return render(request,'software_training/training/admin/admin_emp_reported_detail.html')

def Admin_emp_reported_issue_show(request):
    return render(request,'software_training/training/admin/admin_emp_reported_issue_show.html')

def Admin_manager_reported_detail(request):
    return render(request,'software_training/training/admin/admin_manager_reported_detail.html')

def Admin_manager_reported_issue_show(request):
    return render(request,'software_training/training/admin/admin_manager_reported_issue_show.html')

def Admin_add(request):
    return render(request,'software_training/training/admin/admin_add.html') 

def Admin_addcategories(request):
    return render(request,'software_training/training/admin/admin_addcategories.html') 

def Admin_categorieslist(request):
    return render(request,'software_training/training/admin/admin_categorieslist.html') 

def Admin_addcourse(request):
    return render(request,'software_training/training/admin/admin_addcourse.html') 

def Admin_addnewcourse(request):
    return render(request,'software_training/training/admin/admin_addnewcourse.html') 

def Admin_addnewcategories(request):
    return render(request,'software_training/training/admin/admin_addnewcategories.html') 

def Admin_courselist(request):
    return render(request,'software_training/training/admin/admin_courselist.html') 

def Admin_coursedetails(request):
    return render(request,'software_training/training/admin/admin_coursedetails.html') 

#******************accounts****************

def accounts_Dashboard(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
    
        return render(request, 'software_training/training/account/accounts_Dashboard.html',{'mem':mem})
    else:
        return redirect('/')

def logout5(request):
    if 'acc_id' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/') 

def account_accounts(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id= acc_id)
        return render(request, 'software_training/training/account/account_accounts.html', {'mem': mem})
    else:
        return redirect('/')

def imagechange_accounts(request): 
    if 'acc_id' in request.session:
        if request.method == 'POST':
            id = request.GET.get('id')
            abc = user_registration.objects.get(id=id)
            abc.photo = request.FILES['filenamees']
            abc.save()
            return redirect('account_accounts')
        return render(request, 'software_training/training/account/account_accounts.html')
    else:
        return redirect('/')

def changepassword_accounts(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_fullname'):
            acc_fullname = request.session['acc_fullname']
        if request.session.has_key('acc_designation_id'):
            acc_designation_id = request.session['acc_designation_id']
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        else:
            acc_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=acc_designation_id,id=acc_id).filter(fullname=acc_fullname)

        # mem = user_registration.objects.filter(id=acc_id)
    
        if request.method == 'POST':
            abc = user_registration.objects.get(id=acc_id)
    
            oldps = request.POST['currentPassword']
            newps = request.POST['newPassword']
            cmps = request.POST.get('confirmPassword')
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'software_training/training/account/changepassword_accounts.html', {'mem': mem,})
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')
    
            return render(request, 'software_training/training/account/changepassword_accounts.html', {'mem': mem,})
    
        return render(request, 'software_training/training/account/changepassword_accounts.html', {'mem': mem,})

    else:
        return redirect('/')   


def accounts_registration_details(request):

    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']

        mem = user_registration.objects.filter(id=acc_id)
        des = designation.objects.get(designation_name='trainee')
        deta = user_registration.objects.filter(designation_id = des.id)
        vars = paymentlist.objects.all()
        return render(request,'software_training/training/account/accounts_registration_details.html', { 'mem' : mem, 'deta':deta , 'vars':vars})
    else:
        return redirect('/')
    
def accounts_payment_detail_list(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        a = user_registration.objects.get(id=id)
        c = course.objects.get(id=a.course_id)  
        pay = paymentlist.objects.filter(paymentlist_user_id = a.id).order_by('-id') 
        return render(request,'software_training/training/account/accounts_payment_detail_list.html',{ 'mem' : mem, 'pay': pay , 'a':a , 'c':c})
    else:
        return redirect('/')

def verify(request,id):
    rem = paymentlist.objects.get(id=id)
    rem.paymentlist_amount_status = 1
    rem.save()
    return redirect('/softwareapp/accounts_registration_details')
    
def reminder(request,id):
    rem = user_registration.objects.get(id=id)
    rem.payment_status = 1
    rem.save()
    return redirect('/softwareapp/accounts_registration_details')
    
def accounts_payment_salary(request,id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        vars=user_registration.objects.get(id=id)
        if request.method == "POST":
            abc = acntspayslip()
            abc.acntspayslip_basic_salary = request.POST["salary"] 
            abc.acntspayslip_hra = request.POST["hra"] 
            abc.acntspayslip_conveyns = request.POST["ca"] 
            abc.acntspayslip_pf_tax = request.POST["pt"] 
            abc.acntspayslip_incentives = request.POST["ins"] 
            abc.acntspayslip_delay = request.POST["delay"] 
            abc.acntspayslip_leavesno= request.POST["leave"] 
            abc.acntspayslip_fromdate= request.POST["efdate"] 
            abc.acntspayslip_tax = 0
            abc.acntspayslip_pf = 0 
            abc.acntspayslip_incometax = 0 
            abc.acntspayslip_basictype = request.POST["basictype"] 
            abc.acntspayslip_hratype = request.POST["hratype"] 
            abc.acntspayslip_contype = request.POST["contype"] 
            abc.acntspayslip_protype = request.POST["protype"]
            abc.acntspayslip_instype = request.POST["instype"]
            abc.acntspayslip_deltype = request.POST["deltype"]
            abc.acntspayslip_leatype = request.POST["leatype"] 

            abc.acntspayslip_user_id = user_registration.objects.get(id=id)
            print(vars.designation.id)
            # abc.acntspayslip_designation = vars.designation.id 
            print(abc.acntspayslip_designation)
            abc.save()
        return render(request, 'software_training/training/account/accounts_payment_salary.html',{'vars':vars,'mem' : mem})
    else:
        return redirect('/')
    
def accounts_payment_view(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        reg =user_registration.objects.get(id=id)
        use =acntspayslip.objects.filter(acntspayslip_user_id=id)
        return render(request, 'software_training/training/account/accounts_payment_view.html',{'mem':mem, 'use':use, 'reg':reg})
    else:
        redirect('/')


def accounts_report(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        return render(request,'software_training/training/account/account_report.html',{'mem':mem})
    else:
        return redirect('/')

def accounts_report_issue(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']

        if request.session.has_key('acc_designation_id'):
            acc_designation_id = request.session['acc_designation_id']

        mem = user_registration.objects.filter(id=acc_id)
        des = designation.objects.get(designation_name = 'manager')
        #cut = user_registration.objects.get(designation_id=des.id)
        vars = reported_issue()
        if request.method == 'POST':
            vars.reported_issue_issue=request.POST['issue']
            vars.reported_issue_reporter = user_registration.objects.get(id=acc_id)
            vars.reported_issue_reported_date=datetime.now()
            vars.reported_issue_issuestatus=0
            vars. reported_issue_designation_id = designation.objects.get(id=acc_designation_id)
            vars.reported_issue_reported_to= user_registration.objects.get(designation_id=des.id)
            vars.save()
            return redirect('/softwareapp/accounts_report')
        return render(request, 'software_training/training/account/account_report_issue.html',{'mem':mem})
    else:
        redirect('/')   

def accounts_reported_issue(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        n = reported_issue.objects.filter(reported_issue_reporter=acc_id).order_by('-id')
        return render(request, 'software_training/training/account/account_reported_issue.html',{'mem':mem, 'n':n})
    else:
        redirect('/')


def accounts_employee(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id) 
        des = course.objects.all()
        return render(request, 'software_training/training/account/accounts_employee.html',{'des':des,'mem' : mem})
    else:
        return redirect('/')


def accounts_emp_dep(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
       # mem1 = course.objects.get(id=id)
        des=designation.objects.all().exclude(designation_name = 'trainee')
        context = {'des':des,'mem' : mem}
        return render(request, 'software_training/training/account/accounts_emp_dep.html', context)
    else:
        return redirect('/')
    
def accounts_emp_list(request, id): 
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'): 
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)   
        mem2 = designation.objects.get(id=id)
        
        use = user_registration.objects.filter(designation=mem2) 
        context = {'use':use,'mem' : mem} 
        return render(request, 'software_training/training/account/accounts_emp_list.html', context) 
    else: 
        return redirect('/') 
    
def accounts_emp_details(request, id): 
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'): 
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)   
        vars=user_registration.objects.get(id=id) 
        context = {'vars':vars,'mem' : mem} 
        return render(request, 'software_training/training/account/accounts_emp_details.html', context) 
    else:
        return redirect('/') 
    

def accounts_add_bank_acnt(request, id):
    if 'acc_id' in request.session:  
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id']  
        mem = user_registration.objects.filter(id=acc_id) 
        mem1 = user_registration.objects.filter(id=id) 
        if request.method == 'POST': 
            vars = user_registration.objects.get(id=id) 
            vars.account_no = request.POST['account_no'] 
            vars.ifsc = request.POST['ifsc'] 
            vars.bank_branch = request.POST['bank_branch'] 
            vars.bank_name= request.POST['bank_name'] 
            vars.save() 
        return render(request, 'software_training/training/account/accounts_add_bank_acnt.html',{'mem':mem, 'mem1':mem1})
    else:
        return redirect('/')

def accounts_bank_acnt_details(request):
    return render(request, 'software_training/training/account/accounts_bank_acnt_details.html')

def accounts_salary_details(request, id):
    if 'acc_id' in request.session:  
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id']  
        mem = user_registration.objects.filter(id=acc_id) 
        mem1=user_registration.objects.filter(id=id)
        usk=acntspayslip.objects.filter(acntspayslip_user_id =id)
        return render(request, 'software_training/training/account/accounts_salary_details.html',{ 'mem1':mem1,'usk':usk,'mem': mem})
    else:
        return redirect('/')

def accounts_expenses(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        vars=acntexpensest.objects.all()
        return render(request, 'software_training/training/account/accounts_expenses.html',{'mem':mem, 'vars':vars})
    else:
        return redirect('/')
 
def accounts_expenses_viewEdit(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        var=acntexpensest.objects.filter(id=id)
        return render(request, 'software_training/training/account/accounts_expenses_viewEdit.html',{'mem':mem, 'var':var})
    else:
        return redirect('/')
    

def accounts_expenses_viewEdit_Update(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        emps = acntexpensest.objects.get(id=id)
        if request.method == 'POST':            
            emps.acntexpensest_payee = request.POST['payee']
            emps.acntexpensest_payacnt = request.POST['payacnt']
            emps.acntexpensest_paymethod = request.POST['paymod']
            emps.acntexpensest_paydate = request.POST['paydt']
            emps.acntexpensest_category = request.POST['category']
            emps.acntexpensest_description = request.POST['description']
            emps.acntexpensest_refno = request.POST['ref']
            emps.acntexpensest_amount = request.POST['amount']
            emps.acntexpensest_tax = request.POST['tax']
            emps.acntexpensest_total = request.POST['total']                
            emps.save() 
            return redirect('/softwareapp/accounts_expenses')
        return render(request,'software_training/training/account/accounts_expenses_viewEdit.html',{'mem':mem})
    else:
        return redirect('/')
    

def accounts_expense_newTransaction(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        mem1=acntexpensest()
        if request.method == 'POST':
            mem1.acntexpensest_payee = request.POST['payee']
            mem1.acntexpensest_payacnt = request.POST['payacnt']
            mem1.acntexpensest_paymethod = request.POST['paymod']
            mem1.acntexpensest_paydate = request.POST['paydt']
            mem1.acntexpensest_category = request.POST['category']
            mem1.acntexpensest_description = request.POST['description']
            mem1.acntexpensest_refno = request.POST['ref']
            mem1.acntexpensest_amount = request.POST['amount']
            mem1.acntexpensest_tax = request.POST['tax']
            mem1.acntexpensest_total = request.POST['total']                
            mem1.save()
            return redirect('/softwareapp/accounts_expenses')
        else:
            return render(request, 'software_training/training/account/accounts_expense_newTransaction.html',{'mem':mem})
    else:
        return redirect('/')
  
def accounts_payment(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        des = course.objects.all()
        return render(request, 'software_training/training/account/accounts_payment.html', {'des' : des ,'mem' : mem})
    else:
        return redirect('/')
  
def accounts_payment_dep(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        des = designation.objects.all().exclude(designation_name = 'trainee')
        context = {'des':des,'mem' : mem}
        return render(request, 'software_training/training/account/accounts_payment_dep.html',context)
    else:
        return redirect('/')

def accounts_payment_list(request,id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        
        mem1 = designation.objects.get(id=id)
        use=user_registration.objects.filter(designation=mem1)
        context = {'use':use, 'mem':mem}
        return render(request,'software_training/training/account/accounts_payment_list.html',context)
    else:
        return redirect('/')

def account_payment_details(request, id):
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)
        vars = user_registration.objects.get(id=id) 
        context = {'vars':vars,'mem' : mem} 
        return render(request, 'software_training/training/account/account_payment_details.html', context) 
    else:
        return redirect('/')

def accounts_payment_details(request, id):
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)
        vars = user_registration.objects.get(id=id) 
        context = {'vars':vars,'mem' : mem} 
        return render(request, 'software_training/training/account/accounts_payment_details.html', context) 
    else:
        return redirect('/')
    
def accounts_payslip(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)   
        des = designation.objects.all()
        return render(request, 'software_training/training/account/accounts_payslip.html', {'des':des,'mem':mem})      
    else:
        return redirect('/')

@csrf_exempt
def accounts_acntpay(request):
    if 'acc_id' in request.session:
        fdate = request.POST['fdate']
        tdate = request.POST['tdate']
        desig_id = int(request.POST['desi'])  
        names = acntspayslip.objects.filter(acntspayslip_fromdate__range=(fdate,tdate),acntspayslip_designation= desig_id).values('acntspayslip_user_id__fullname','acntspayslip_eno', 'acntspayslip_user_id__account_no', 'acntspayslip_user_id__bank_name', 'acntspayslip_user_id__bank_branch','acntspayslip_user_id__id', 'acntspayslip_user_id__email')  
        print(fdate)
        print(tdate)
      
        print(desig_id)
        print(names)
        return render(request, 'software_training/training/account/accounts_acntpay.html')
    else:
        return redirect('/')
    
def accounts_paydetails(request,id):
     if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)  
        user = user_registration.objects.get(id=id)
        acc = acntspayslip.objects.get(user_id=id)
        names = acntspayslip.objects.all()
        return render(request, 'software_training/training/account/accounts_paydetails.html',{'acc':acc, 'user':user,'names':names, 'mem': mem})

def accounts_print(request,id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)  
        user = user_registration.objects.get(id=id)
        acc = acntspayslip.objects.get(user_id=id)
        return render(request, 'software_training/training/account/accounts_print.html',{'mem':mem, 'acc':acc, 'user':user,})
    else:
        return redirect('/')     