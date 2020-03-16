from django.shortcuts import render, redirect
from django.http import JsonResponse
from voteapp.models import Subject, Teacher
# Create your views here.
def show_subjects(request):
    subjects = Subject.objects.all()
    for item in subjects:
        print(item.name)
    return render(request, 'subject.html', {'subjects':subjects})

def show_teachers(request):
    try:
        sno = int(request.GET['sno'])
        subject = Subject.objects.get(no=sno)
        teachers = subject.teacher_set.all()
        return render(request, 'teachers.html', {'subject': subject, 'teachers': teachers})
    except (KeyError, ValueError, Subject.DoesNotExist):
        return redirect('/')

def prise_or_criticize(request):
    '''评价'''
    try:
        tno = int(request.GET['tno'])
        teacher = Teacher.objects.get(no=tno)
        if request.path.startswith('/praise'):
            teacher.good_count += 1
        else:
            teacher.bad_count += 1
        teacher.save()
        data = {'code': 200,'hint': '操作成功'}
    except (KeyError, ValueError, Teacher.DoesNotExist):
        data = {'code': 404, 'hint': '操作失败'}
    return JsonResponse(data)