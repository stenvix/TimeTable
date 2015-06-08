/**
 * Created by stepanov on 07.06.15.
 */
jQuery(document).ready(function () {
    jQuery(".chosen").chosen({
        no_results_text: "Оопс, нічого не знайдено!",
        placeholder_text_multiple: "Виберіть декілька позицій",
        placeholder_text_single: "Виберіть дані"
    });
});
jQuery(document).ready(function () {
    //jQuery("select[name$='lecturer'] option").attr('disabled', 'disabled').trigger("chosen:updated");
    refresh();
});
function refresh() {
    jQuery(document).ready(function () {
        jQuery("select.lesson").each(function () {
            jQuery("select[name$='_lecturer'] option").each(function (i, item) {
                if (jQuery(this).val() == jQuery(this).parent().val()) {
                    //jQuery(this).attr('disabled', false).trigger("chosen:updated");
                }
                else {
                    jQuery(this).attr('disabled', true).trigger("chosen:updated");
                }
            });
        })
    });
}
jQuery(document).ready(function () {
    jQuery("select.lesson").change(function () {
        var week = jQuery(this).attr('data-week');
        var tit = jQuery(this).attr('name') + '_lecturer';
        jQuery.get("/admin/rest/" + this.value)
            .success(function (data) {
                jQuery("select[name=" + tit + "][data-week=" + week + "] option").each(function (i, item) {
                    //console.log(item);
                    if (data.result.length != 0) {
                        jQuery.each(data.result, function (i, it) {
                            if (jQuery(item).val() == it.lecturer && jQuery(item).parent().attr('data-week') == week) {
                                jQuery(item).attr('disabled', false).trigger("chosen:updated");
                                return false
                            } else if (jQuery(item).parent().attr('data-week') == week) {
                                jQuery(item).attr('disabled', true).trigger("chosen:updated");
                            }
                        });
                    }
                    else {
                        jQuery(item).attr('disabled', true).prop('selected', false).trigger("chosen:updated");
                    }
                    jQuery(item).parent().val(0).trigger("chosen:updated");
                })

            })
            .error(function () {
                alert("Помилка з’єднання з сервером");
            })
            .complete(function () {

            })
    })
});

