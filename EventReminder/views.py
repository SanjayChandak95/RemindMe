from django.shortcuts import render
from .models import User, EventReminder
from django.core.mail import send_mail
from django.http import HttpResponse
import datetime
from .forms import CreateEvent
from RemindMe.settings import EMAIL_HOST_USER
from heapq import heappush,heappop

TODAY = datetime.date.today()

# Create your views here.
def createEventReminder(request):
    userId = User.objects.get(userName = 'Sanjay')
    context = {'msg' : ""}
    items = EventReminder.objects.filter(userId = userId, EventProgress = 'F').all()
    context['items'] = items
    if request.method == 'POST':
        createEvent = request.POST
        messageDetail = createEvent['messageDetail']
        tt = setTime(createEvent['triggerDateTime'])
        processFlag = 'U'
        if tt.date() == TODAY:
            processFlag = 'P'

        eventReminder = EventReminder.objects.create(userId = userId ,\
            recipientMail = createEvent['recipientMail'],\
                createdDate = datetime.datetime.now(), \
                    messageDetail = messageDetail , triggerDateTime = tt, EventProgress = processFlag)
    return render(request, "createEventReminder.html",context)

def setTime(timeStr):
    # 2020-10-03T13:02
    timeStr = timeStr.replace("T"," ")
    return datetime.datetime.strptime(timeStr,'%Y-%m-%d %H:%M')

def sendReminder():
    TODAYS_TASK = EventReminder.objects.filter(EventProgress = 'P').all()
    currentTime = datetime.datetime.now().time()
    f = open('cronLog.txt','a')
    f.write("\nReminder Job Start at : "+str(currentTime)+"\n")
    f.write("today task \n" )
    f.write(str(TODAYS_TASK))
    for task in TODAYS_TASK:
        if task.triggerDateTime.time() <= currentTime:
            subject = "Reminder for your next event"
            send_mail(subject , task.messageDetail,task.userId.email, [task.recipientMail],fail_silently = False )
            task.EventProgress = 'F'
            task.save()
    f.write("\nReminder Job end :"+str(currentTime))
    f.close() 


def updateTodays_Task():
    backup = []
    tomorrowDate = TODAY + datetime.timedelta(days=1)
    twoDayFuture = TODAY + datetime.timedelta(days=2)
    task = EventReminder.objects.filter(EventProgress = 'U',\
        triggerDateTime__year = tomorrowDate.year,\
            triggerDateTime__month = tomorrowDate.month,\
                triggerDateTime__day = tomorrowDate.day).all()
    for eventReminder in task:
        heappush(backup,(eventReminder.triggerDateTime.time(), eventReminder))
        eventReminder.EventProgress = 'P'
        eventReminder.save()
    #end
    TODAY = tomorrowDate
    TODAYS_TASK = backup[:]