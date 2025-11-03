from django.shortcuts import render, redirect
from django.utils import timezone
import pytz
from .models import Event
import json

# функция собирает в виде я json все события пользователя
def collect_events(user):
    user_events = Event.objects.filter(author=user)
    formatted_events = []
    for event in user_events:
        el = {
            "id": event.id, # id
            "title": event.title, #
            "start": event.start_date.isoformat(), #
            "end": event.end_date.isoformat(), #
            "extendedProps": {
                "alert": event.alert, #
                "duration": { #
                    "hours": (event.end_date - event.start_date).total_seconds() // (60 * 60),
                    "minutes": (event.end_date - event.start_date).total_seconds() % (60 * 60) // 60,
                }
            },
            "color": '#9ea7d9', #
            "textColor": '#000', #
            "display": 'block', #
        }
        if event.repeat_status != 'none':
            rrule = {
                "freq": event.repeat_status, #
                "dtstart": event.start_date.isoformat(), #
                "interval": 1, #
            }
            if event.end_repeat == 'date':
                rrule["until"] = event.end_repeat_date.isoformat() #
            el["rrule"] = rrule
        formatted_events.append(el)
    return formatted_events


def base_view(request):
    mobile = 'mobile/' if "Mobile" in request.headers["User-Agent"] else ''
    if request.user.is_authenticated:
        user = request.user
        if user.is_verified:
            if request.method == 'POST':
                title = request.POST.get('title')
                start_time = request.POST.get('start-time')
                end_time = request.POST.get('end-time')
                repeat_choice = request.POST.get('repeat-vars')
                if repeat_choice is None:
                    repeat_choice = 'none'
                end_repeat = request.POST.get('end-repeat')
                if end_repeat is None:
                    end_repeat = 'never'
                end_repeat_date = request.POST.get('end-repeat-date')
                if end_repeat_date == "":
                    end_repeat_date = timezone.now()
                alert_choice = request.POST.get('alert-vars')
                event_id = request.POST.get('id')
                time_server = timezone.now()
                user_timezone = pytz.timezone(user.timezone)
                local_time = time_server.astimezone(user_timezone)
                if event_id != '':
                    event = Event.objects.get(id=event_id)
                    event.title = title
                    event.start_date = start_time
                    event.end_date = end_time
                    event.repeat_status = repeat_choice
                    event.end_repeat = end_repeat
                    event.end_repeat_date = end_repeat_date
                    event.alert = alert_choice
                    event.start_alerts(local_time.replace(tzinfo=None))
                    event.save()
                else:
                    event = Event.objects.create(
                        title=title,
                        start_date=start_time,
                        end_date=end_time,
                        repeat_status=repeat_choice,
                        end_repeat=end_repeat,
                        end_repeat_date=end_repeat_date,
                        alert=alert_choice,
                        author=user
                    )
                    event.start_alerts(local_time.replace(tzinfo=None))
                    event.save()
                return redirect('/')
            events = collect_events(request.user)
            context = {'email': str(user.email),
                       'events': json.dumps(events)}
            return render(request, f"{mobile}control-panel.html", context)
        return redirect(f'verify/{str(user.uuid)}')
    return render(request, f'{mobile}auth-buttons.html')

def delete_event(request, id):
    try:
        event = Event.objects.get(id=id)
        if request.user.is_verified and event.author.uuid == request.user.uuid:
            event.delete()
    except Event.DoesNotExist:
        pass
    return redirect('/')
