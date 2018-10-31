function formatDate(date) {
    return date.getDate() + "." + (date.getMonth() + 1) + "." + date.getFullYear();
}


function addZeros(i) {
    if (i < 10) {
        return "0" + i;
    } else {
        return "" + i;
    }
}

function formatDateForDjango(date) {
    return "" + date.getFullYear() + "/" + addZeros(date.getMonth() + 1) + "/" + addZeros(date.getDate()) + "/";

}

function getNow() {
    return new Date();
}

function getNowFormatted() {
    return formatDate(getNow());
}


$(document).ready(function () {
    // Initialize sidenav [MAT]
    $(".sidenav").sidenav();

    // Initialize datepicker [MAT]
    $('.datepicker').datepicker({
        format: 'dd.mm.yyyy',
        // Translate to German
        i18n: {
            months: ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
            monthsShort: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
            weekdays: ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'],
            weekdaysShort: ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'],
            weekdaysAbbrev: ['S', 'M', 'D', 'M', 'D', 'F', 'S'],

            // Buttons
            today: 'Heute',
            clear: 'Löschen',
            done: 'OK',
        },

        // Set monday as first day of week
        firstDay: 1,
        autoClose: true
    });

    // Initialize timepicker [MAT]
    $('.timepicker').timepicker({
        twelveHour: false,
        autoClose: true,
        cancelText: 'Abbrechen',
        clearText: 'Löschen',
        doneText: 'OK'
    });

    //Initialize tooltip [MAT]
    $('.tooltipped').tooltip();
});