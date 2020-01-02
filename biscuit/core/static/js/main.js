$(document).ready( function () {
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

    $('table.datatable').each(function (index) {
        $(this).DataTable({
            "paging": false
        });
    });

    $('*:not(a, span)[data-poload]').each(function() {
        $(this).find('a, span').attr('data-poload', $(this).attr('data-poload'));
        $(this).removeAttr('data-poload');
    });

    $('*[data-poload]').popover({
        html: true,
	animation: true,
	placement: 'auto',
	contianer: 'body',
	trigger: 'hover'
    }).on("inserted.bs.popover", function() {
        var trigger_el = $(this);
	var popover_id = trigger_el.attr("aria-describedby");
	var popover_el = $('#' + popover_id);

	$.get(trigger_el.data('poload'), function(d) {
            popover_el.html(d);
	});
    });
});
