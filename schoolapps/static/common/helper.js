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


function setTime(lesson_field) {
    // fill timefield based on lesson value
    if (lesson_field.id === 'id_from_lesson') {
        $('[id=id_from_time]').val(lesson_field.value);
    } else {
        // calculate lessons end time
        // string methods easier than date function muddle
        var h = lesson_field.value.split(':')[0];
        var m = lesson_field.value.split(':')[1];
        if (m < 15) {
            m = parseInt(m) + 45;
        } else {
            m = parseInt(m) - 15;
            h = parseInt(h) + 1;
        }
        m = m.toString()
        h = h.toString()
        if (m.length === 1) {
            m = '0' + m
        }
        var newTime = h + ':' + m;
        $('[id=id_to_time]').val(newTime);
    }
}

function selectActiveLink() {
    var currlocation = $('meta[name="active-loaction"]');
    var url_name = currlocation.attr("content");
    //console.log(url_name);

    $("#" + url_name).addClass("active");
    $("#" + url_name).parent().parent().parent().addClass("active");
}

$(document).ready(function () {
    selectActiveLink();

    $("dmc-datetime input").addClass("datepicker");
    $("[data-form-control='date']").addClass("datepicker");
    $("[data-form-control='time']").addClass("timepicker");

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

    // Initialize tooltip [MAT]
    $('.tooltipped').tooltip();

    // Initialize select [MAT]
    $('select').formSelect();

    // Initalize print button
    $("#print").click(function () {
        window.print();
    });

    // Initialize Collapsible [MAT]
    $('.collapsible').collapsible();

    // Initialize FABs [MAT]
    $('.fixed-action-btn').floatingActionButton();

    // Initialize delete button
    $(".delete-button").click(function (e) {
        if (!confirm("Wirklich löschen?")) {
            e.preventDefault();
        }
    })
});