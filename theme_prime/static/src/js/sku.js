$( document ).ready(function() {
    if ($('input:radio.always[checked="checked"]').length>0) {$('#sku').html($('input:radio.always[checked="checked"]').attr('code'))}
    if ($('select.always').length>0) {setTimeout(() => {$('#sku').html($('select.always > option[selected="selected"]').attr('code'))}, 300);}
    
    
});

$('input:radio.always').change(
    function(){
        if ($(this).is(':checked') )
            $('#sku').html($(this).attr('code'))
            console.log("lol")
        }
    );



    
    $('select.always').change(
        function(){
          
                  setTimeout(() => {$('#sku').html($('select.always > option[selected="selected"]').attr('code'))}, 100);
            }
        );
    
    