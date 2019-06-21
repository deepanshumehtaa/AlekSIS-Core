$(document).ready( function () {
    $('table.datatable').each(function (index) {
        $(this).DataTable({
            "paging": false
        });
    });
});
