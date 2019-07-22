$(document).ready( function () {
    $('table.datatable').each(function (index) {
        $(this).DataTable({
            "paging": false
        });
    });

    $('*[data-poload]').popover({
        html: true,
	animation: true,
	placement: 'auto',
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
