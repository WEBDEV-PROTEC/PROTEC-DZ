$( document ).ready(function() {
    if ($('input:radio.always[checked="checked"]').length>0) {$('#al').html($('input:radio.always[checked="checked"]').attr('code'))}
    if ($('select.always"]').length>0) {setTimeout(() => {$('#al').html($('select.always > option[selected="selected"]').attr('code'))}, 300);}
    
    
});

$('input:radio.always').change(
    function(){
        if ($(this).is(':checked') )
            $('#al').html($(this).attr('code'))
            console.log("lol")
        }
    );



    
    $('select.always').change(
        function(){
          
                  setTimeout(() => {$('#al').html($('select.always > option[selected="selected"]').attr('code'))}, 100);
            }
        );
    
    