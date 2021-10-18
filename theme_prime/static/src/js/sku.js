$( document ).ready(function() {
    $('#sku').html($('input:radio.always[checked="checked"]').attr('code'))
});

$('input:radio.always').change(
    function(){
        if ($(this).is(':checked') )
            $('#sku').html($(this).attr('code'))
            console.log("lol")
        }
    );


