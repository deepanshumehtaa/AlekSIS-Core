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


function selectActiveLink() {
    var currlocation = $('meta[name="active-loaction"]');
    var url_name = currlocation.attr("content");
    //console.log(url_name);

    var selector = ".url-" + url_name;
    console.log(selector);
    $(selector).addClass("active");
    $(selector).parent().parent().parent().addClass("active");
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
            cancel: 'Abbrechen',
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
        i18n: {
            cancel: 'Abbrechen',
            clear: 'Löschen',
            done: 'OK'
        },
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

    // Initialize Modals [MAT]
    $('.modal').modal();

    // Initialize delete button
    $(".delete-button").click(function (e) {
        if (!confirm("Wirklich löschen?")) {
            e.preventDefault();
        }
    });

    if (typeof onFinish !== 'undefined') {
        onFinish();
    }
});
