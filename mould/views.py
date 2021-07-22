from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required 
from .models import Mould, MouldStatus, MouldComment 
import matplotlib.pyplot as plt  
import matplotlib.dates as mdates 
import os
import datetime 

# ------------------------------------------------- 
class MouldData: 

    def __init__(self): 
        self.threshold = None 
        self.presentCount = None 
    
    def isThresholdCross(self): 
        diffrence = self.threshold - self.presentCount 
        alert_flag = True 
        if diffrence <= 500: 
            alert_flag = True 
        else: 
            alert_flag = False 
 
        return alert_flag     
    

@login_required 
def mould_registration(request): 
    context = {}
    context['mouldRegistered'] = False 
    if request.method == "POST": 
        mould_id = request.POST.get('mouldNumber')
        mould_name = request.POST.get('mouldName')
        cavity_number = request.POST.get('cavityNumber')
        threshold_number = request.POST.get('thresholdValue')
        mould = Mould()
        mould.mould_id = mould_id 
        mould.mould_name = mould_name 
        mould.cavity_number = cavity_number 
        mould.registered_by = request.user 
        mould.threshold_value = threshold_number 
        mould.present_count = 0 
        mould.save() # mould registered. 
        context['mouldRegistered'] = True 
        context['mouldName'] = mould_name
        print(mould_id, mould_name, cavity_number)
        return render(request, 'mould_registration.html', context)
    else: 
        context['mouldRegistered'] = False 
        return render(request, 'mould_registration.html', context)



@login_required 
def mould_view(request, mould_id): 
    context = {}
    if request.method == "POST": 
        comment_on_mould_id = request.POST.get('id')
        comment_text = request.POST.get('comment')
        comment_by = request.user 
        comment = MouldComment()
        comment.comment_text = comment_text 
        comment.commented_by = comment_by
        comment.mould_id = Mould.objects.get(mould_id = comment_on_mould_id)
        comment.save()
        return redirect(f'/mould/{comment_on_mould_id}')

    comments = MouldComment.objects.filter(mould_id = mould_id).order_by('commented_date_time')
    comments = list(comments)[::-1]
    print(comments)
    context['comments'] = comments 
    mould_data =  Mould.objects.get(mould_id = mould_id)
    context['data'] = mould_data 
    
    drawGraphMould_vs_shots(mould_data)
    return render(request, 'mould_id.html', context)


@login_required 
def mould_update(request): 
    context = {}
    context['MouldUpdate'] = False 
    if request.method == "POST": 
        context['MouldUpdate'] = True 
        mould_data = Mould.objects.all() 
        context['Mould_Data'] = mould_data 
        mould_id = request.POST.get('mouldID')
        increment = request.POST.get('increment')

        target_mould = Mould.objects.get(mould_id = mould_id)
        target_mould.present_count = target_mould.present_count + int(increment) 
        target_mould.save()


        mould_entry = MouldStatus()
        mould_entry.mould_id = target_mould 
        mould_entry.count_increment = increment 
        mould_entry.save()
        print(mould_id, increment)
        mould_entry_data = MouldStatus.objects.filter(mould_id = target_mould)
        context['target_mould_data'] = mould_entry_data 

        return render(request, 'mould_update.html', context)
    else: 
        mould_data = Mould.objects.all() 
        context['Mould_Data'] = mould_data 
        return render(request, 'mould_update.html', context)


@login_required
def mould_search(request): 
    context = {}
    mould_id = Mould.objects.all()
    mould_list_id = []
    for mould in mould_id: 
        mould_list_id.append(mould.mould_id)
    context['mould_id'] = mould_list_id
    if request.method == "POST": 
        mould_id = request.POST.get('mould_id')
        return redirect(f'/mould/{mould_id}')
    else: 
        return render(request, 'mould_search.html', context)


@login_required 
def mould_data_update(request, mould_id): 
    context = {}
    mould_data = Mould.objects.get(mould_id = mould_id)
    context['MouldData'] = mould_data 
    if request.method == "POST": 
        return render(request, 'mould_data_update.html', context)
    else: 
        return render(request, 'mould_data_update.html', context)



# -----------------------------------------------
# Graph Drawer. 

def drawGraphMould_vs_shots(mould_id): 
    mould_status_data = MouldStatus.objects.filter(mould_id = mould_id).order_by('status_update')
    
    increment_date = []
    increment_count = []

    for mould in mould_status_data: 
        increment_date.append(mould.status_update.date())
        increment_count.append(mould.count_increment)
    print(increment_count)
    print(increment_date)
    plt.title(f'Shot vs Date for Mould ID {mould_id}')
    plt.xlabel('Date')
    plt.ylabel('Shot Count')
    # plt.show()
    plt.plot(increment_date, increment_count,marker='>', color='blue')
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%D:%M:%Y')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.savefig('mould/static/images/mould_daily_count.png')
    plt.close()