/**
 * Created by stepanov on 07.06.15.
 */
jQuery(document).ready(function () {
    ch_refresh()
});
function ch_refresh() {
    jQuery(".chosen").chosen({
        inherit_select_classes: true,
        no_results_text: "Оопс, нічого не знайдено!",
        placeholder_text_multiple: "Виберіть декілька позицій",
        placeholder_text_single: "Виберіть дані"
    });
}
jQuery(document).ready(function () {
    //jQuery("select[name$='lecturer'] option").attr('disabled', 'disabled').trigger("chosen:updated");
    refresh();
});
function refresh() {
    jQuery(document).ready(function () {
        jQuery("select.lesson").each(function () {
            jQuery("select[name$='_lecturer'] option").each(function (i, item) {
                if (jQuery(this).val() == jQuery(this).parent().val()) {
                    jQuery(this).attr('disabled', false).trigger("chosen:updated");
                }
                else {
                    jQuery(this).attr('disabled', true).trigger("chosen:updated");
                }
            });
        });
        jQuery('select#group option').each(function (i, item) {
            if (jQuery(item).parent().parent().val() == jQuery(item).val()) {
                jQuery(item).prop('selected', true).trigger("chosen:updated");
            }
        });
        jQuery('select#day option').each(function (i, item) {
            if (jQuery(item).parent().val() == jQuery(item).val()) {
                jQuery(item).prop('selected', true).trigger("chosen:updated");
            }
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
jQuery(document).ready(function () {

    jQuery("#form-timetable").submit(function () {
        var status = true;
        jQuery("select.lesson").each(function (i, item) {
            if (jQuery(item).val() != 0) {
                jQuery("select[name=" + jQuery(item).attr('name') + "_lecturer][data-week=" + jQuery(item).attr('data-week') + "]").each(function (j, jtem) {
                    if (jQuery(jtem).val() == 0 || jQuery(jtem).val() == null) {
                        console.log(jQuery('#' + jQuery(jtem).attr('name')));
                        jQuery('#' + jQuery(jtem).attr('name') + '_chosen').addClass('ch-error');
                        status = false;
                    } else {
                        jQuery('#' + jQuery(jtem).attr('name') + '_chosen').removeClass('ch-error');
                    }
                })
            }
        });
        if (status == false) {
            alert('Помилка, заповніть всі поля')
        }
        return status;
    })
});

jQuery(document).ready(function () {
    jQuery('#finishDate').datepicker({
        minDate: new Date(),
        dateFormat: "dd-mm-yy",
        onSelect: function () {
            jQuery.get("/admin/replacement/get", {group: jQuery('#group').val(), date: this.value})
                .success(function (data) {
                    if( data.result.length > 0){
                        jQuery('#finish_lesson').html('');
                        jQuery.each(data.result,function(i,item){
                            console.log(item);
                            if (item.id < 0){
                                jQuery('#finish_lesson').append(new Option(item.value,item.id*-1))
                            }
                        })
                    }
                }).error(function (data) {
                    alert('Помилка з’єднання з сервером')
                });
        },
        regional: "ru"
    });
    jQuery.datepicker.setDefaults($.datepicker.regional["uk"]);
    jQuery('#startDate').datepicker({
        onSelect: function () {
            jQuery.get("/admin/replacement/get", {group: jQuery('#group').val(), date: this.value})
                .success(function (data) {
                    if( data.result.length > 0){
                        jQuery('#start_subject').html('');
                        jQuery.each(data.result,function(i,item){
                            if ( item.id > 0)
                                var oOption =  new Option(item.value,item.id);
                                jQuery(oOption).attr('data-number',item.number);
                            jQuery('#start_subject').append(oOption).trigger("chosen:updated");
                        })
                    }
                }).error(function (data) {
                    alert('Помилка з’єднання з сервером')
                });
            jQuery("#finishDate").datepicker("option", "minDate", this.value);
        },
        minDate: new Date(),
        dateFormat: "dd-mm-yy",
        regional: "ru"
    });
    jQuery('#start_subject').change(function(){
        if (jQuery(this).val() > 0){
             jQuery('#start_lesson').val(jQuery(this).find('option:selected').data('number'));
        }
    });

    jQuery('#group').change(function(){
        jQuery.get('/admin/replacement/get_group',{group:jQuery(this).val()}).success(function(data){
            console.log(data);
            jQuery('#finish_subject').html('');
            if(data.result.length>0){
                jQuery.each(data.result,function(i,item){
                    jQuery('#finish_subject').append(new Option(item.value,item.id)).trigger("chosen:updated");
                })
                jQuery('#finish_subject').prop('selectedIndex',-1);
            }
        }).error(function(data){

        })
    });
    jQuery('#finish_lesson').prop('selectedIndex',-1);
    jQuery('#finish_subject').prop('selectedIndex',-1);
});