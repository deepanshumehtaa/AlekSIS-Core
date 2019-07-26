$(document).ready( function () {
    $('table.datatable').each(function (index) {
        $(this).DataTable({
            "paging": false
        });
    });

    $('a[data-poload], *[data-poload] > a*').popover({
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
