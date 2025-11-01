document.getElementById('new-button').addEventListener('click', function() {
    var form = document.getElementById('form');
    var cancelButton = document.getElementById('cancel');
    form.style.visibility = 'visible';
    cancelButton.style.visibility = 'visible';
    this.style.visibility = 'hidden';
    getElementById('repeat-vars').disabled = false;
    getElementById('end-repeat').disabled = false;
});

document.getElementById('end-time').addEventListener('change', function() {
    var repeatVarsSelect = document.getElementById('repeat-vars');
    var repeatEndSelect = document.getElementById('end-repeat');

    var startTimeInput = document.getElementById('start-time');
    var start = new Date(startTimeInput.value);
    var end = new Date(this.value);

    if (!(isNaN(start) || isNaN(end))) {
        var hours = (end - start) / (1000 * 60 * 60);
        if (start.getFullYear() == end.getFullYear() && start.getMonth() == end.getMonth() && start.getDay() == end.getDay()) {
            repeatVarsSelect.disabled = false;
            repeatEndSelect.disabled = false;
        } else {
            repeatVarsSelect.value = "none";
            repeatVarsSelect.disabled = true;
            repeatEndSelect.value = "never";
            repeatEndSelect.disabled = true;
        }

        if (hours <= 0) {
            this.value = "";
            alert('Дата начала не может быть позже (или равна) даты конца!');
        }
    }
});

document.getElementById('end-repeat').addEventListener('change', function() {
    var endRepeatDateField = document.getElementById('endLabel');

    if (this.value === 'date') {
        endRepeatDateField.style.visibility = 'visible';
    } else {
        endRepeatDateField.style.visibility = 'hidden';
    }
});

function resetForm() {
    var form = document.getElementById('form');
    form.reset();
    form.style.visibility = 'hidden';

    document.getElementById('new-button').style.visibility = 'visible';
    document.getElementById('endLabel').style.visibility = 'hidden';
    document.getElementById('cancel').style.visibility = 'hidden';
    document.getElementById('delete').style.visibility = 'hidden';
    document.getElementById('id').value = '';
    var mainAction = document.getElementById('main-action');
    mainAction.value = 'Сохранить';
}

function deleteEvent(event) {
    var id = document.getElementById('id').value;
    location.replace('/delete/event/' + id);
}

document.getElementById('cancel').addEventListener('click', resetForm);
document.getElementById('delete').addEventListener('click', deleteEvent);


