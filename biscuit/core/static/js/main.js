$(document).ready( function () {
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
