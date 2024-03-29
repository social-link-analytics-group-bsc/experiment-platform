
/*
(function($){
    $(document).ready(function(){
        $('#changelist-filter').children('h3').each(function(){
            var $title = $(this);
            $title.click(function(){
                $title.next().slideToggle();
            });
        });
    });
})(django.jQuery);
*/

(function($){ $(document).ready(function(){
    $('#changelist-filter > h3').each(function(){
        var $title = $(this);
        $title.next().toggle();
        $title.css("cursor","pointer");
        $title.click(function(){
            $title.next().slideToggle();
        });
    });
    var toggle_flag = false;
    $('#changelist-filter > h2').css("cursor","pointer");
    $('#changelist-filter > h2').click(function () {
        toggle_flag = ! toggle_flag;
        $('#changelist-filter > ul').each(function(){
            $(this).slideToggle(toggle_flag);
        });
    });
  });
})(django.jQuery);