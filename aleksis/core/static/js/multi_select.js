$(document).ready(function () {
    $("#select_all_container").show();
    $("#header_box").change(function () {
        if ($(this).is(":checked")) {
            $(document).find('input[name="selected_objects"]').prop({
                indeterminate: false,
                checked: true,
            });
        } else {
            $(document).find('input[name="selected_objects"]').prop({
                indeterminate: false,
                checked: false,
            });
        }
    });

    $('input[name="selected_objects"]').change(function () {
        let checked = $(this).is(":checked");
        let indeterminate = false;
        $(document).find('input[name="selected_objects"]').each(function () {
            if ($(this).is(":checked") !== checked) {
                $("#header_box").prop({
                    indeterminate: true,
                })
                indeterminate = true;
                return false;
            }
        });
        if (!(indeterminate)) {
            $("#header_box").prop({
                indeterminate: false,
                checked: checked,
            });
        }
    });
});
