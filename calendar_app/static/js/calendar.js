function renderData(str) {
    var date = new Date(str);

    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0'); // месяцы с 0
    var day = String(date.getDate()).padStart(2, '0');
    var hours = String(date.getHours()).padStart(2, '0');
    var minutes = String(date.getMinutes()).padStart(2, '0');

    var value = `${year}-${month}-${day}T${hours}:${minutes}`;
    return value;
}

function resetForm() {
    var form = document.getElementById('form');
    form.reset();
    form.style.visibility = 'hidden';

    document.getElementById('new-button').style.visibility = 'visible';
    document.getElementById('endLabel').style.visibility = 'hidden';
    document.getElementById('cancel').style.visibility = 'hidden';
    document.getElementById('delete').style.visibility = 'hidden';
    var mainAction = document.getElementById('main-action');
    mainAction.value = 'Сохранить';
}

function handleEventClick(info) {
    resetForm();
    var event = info.event;

    var buttonNew = document.getElementById('new-button');
    buttonNew.style.visibility = 'hidden';

    var form = document.getElementById('form');
    form.style.visibility = 'visible';

    var cancel = document.getElementById('cancel');
    cancel.style.visibility = 'visible';

    var inputTitle = document.getElementById('inputTitle');
    inputTitle.value = event.title;

    var inputStarttime = document.getElementById('start-time');
    inputStarttime.value = renderData(event.start);

    var inputEndtime = document.getElementById('end-time');
    inputEndtime.value = renderData(event.end);

    if (event._def.recurringDef) {
        var hours = Number(event.extendedProps.duration.hours);
        var minutes = Number(event.extendedProps.duration.minutes);
        var start = new Date(renderData(event.start));

        var end = new Date(start.getTime() + (hours * 60 + minutes) * 60 * 1000);
        var year = end.getFullYear();
        var month = String(end.getMonth() + 1).padStart(2, '0'); // месяцы с 0
        var day = String(end.getDate()).padStart(2, '0');
        var hours = String(end.getHours()).padStart(2, '0');
        var minutes = String(end.getMinutes()).padStart(2, '0');

        var end = `${year}-${month}-${day}T${hours}:${minutes}`;
        inputEndtime.value = end;

        var options = event._def.recurringDef.typeData.rruleSet._rrule[0].options;
        if (options.until === undefined) {
            var endRepeatSelect = document.getElementById('end-repeat');
            endRepeatSelect.value = 'never';
        } else {
            var endRepeatSelect = document.getElementById('end-repeat');
            endRepeatSelect.value = 'date';

            var endRepeatDate = document.getElementById('end-repeat-date');
            endRepeatDate.value = renderData(options.until);
            document.getElementById('endLabel').style.visibility = 'visible';
        }
        if (options.freq === 0) {
            var val = 'yearly';
        } else if (options.freq === 1) {
            var val = 'monthly';
        } else if (options.freq === 2) {
            var val = 'weekly';
        } else if (options.freq === 3) {
            var val = 'daily';
        }
    } else {
        var val = 'none';
    }

    var repeatVars = document.getElementById('repeat-vars');
    repeatVars.value = val;

    const changeEvent = new Event('change', {
        bubbles: true,
        cancelable: true // Опционально, для возможности отмены
    });

    inputEndtime.dispatchEvent(changeEvent);

    var alertVars = document.getElementById('alert-vars');
    alertVars.value = event.extendedProps.alert;

    var mainAction = document.getElementById('main-action');
    mainAction.value = 'Изменить';

    console.log(event.id);
    var invisField = document.getElementById('id');
    invisField.value = event.id;

    var buttonDelete = document.getElementById('delete');
    buttonDelete.style.visibility = 'visible';
}

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    try {
        var eventik = JSON.parse(JSON.parse(document.getElementById('events-data').textContent.trim()));
        var right = 'dayGridMonth,timeGridWeek,timeGridDay';
    } catch (error) {
        var eventik = [];
        var right = '';
    }
    var calendar = new FullCalendar.Calendar(calendarEl, {
        themeSystem: 'standard',
        initialView: 'dayGridMonth',
        locale: 'ru',
        height: 'auto',
        firstDay: 1,
        eventDisplay: 'dot',
        displayEventTime: false,
        eventDisplay: 'list-item',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: right
        },
        allDaySlot: false,

        buttonText: {
            today: 'Сегодня',
            month: 'Месяц',
            week: 'Неделя',
            day: 'День'
        },
        events: eventik,
        eventClick: handleEventClick
    });
    calendar.render();
});