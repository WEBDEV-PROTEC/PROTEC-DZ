odoo.define('user.required', function (require) {
    "use strict";
    console.log('ac#############')

    var rpc = require('web.rpc');
    var cities = document.querySelector('#ville');
//    console.log('city', cities)
    $(document).ready(function(){
        $('#scan').val('');
        $('.file_alert').hide();

//        $('#State').on('click', function(){
//            console.log(cities.length)
//            if (cities.length==1){
//                console.log('hi')
//            }
//            else if(cities.length>1){
//                console.log('hello')
//                $('#ville').hide();
//            }
//        });

        $('#State').on('change', function(){
            var id = $('#State').val()
            var cit = $('#city').val();
            $('#ville').find('option').remove()
//            for (let j=0; j< cities.length; j++){
//                console.log('#####', typeof(cities[j]))
//            }
//            if (cities.length==1){
//                console.log('hi')
//            }
            var model = 'res.city';
            var domain = ('state_id.id', '=', id);
            var field = ['name'];
            rpc.query({
                    route: "/get/city",
                    params: {
                        'domain': id,
                    },
                }).then(function(data){
//                console.log('data_value', data)
//                console.log('data', data.length)
                for(let i = 0; i < data.length; i++){
//                    console.log(data[i].name)

                    var option = new Option(data[i][0], data[i][1]);
                    cities.add(option);
                }

            });
//            console.log(this.data);

        });



        if ( $('.check_2').is(':checked') || $('.check_1').is(':checked')) {
            $('.req_mark').show();
            $('#agrem').attr('required', '');
            $('#exp_agrem').attr('required', '');
        }
        else{
            $('.req_mark').hide();
            $('#agrem').removeAttr('required');
            $('#exp_agrem').removeAttr('required');
        }
        $("#scan").on('change', function(){
            console.log('hi')
            var a = $('#scan')[0].files;
            if (a.length > 4){
                $('.file_alert').show();
                $('.doc').prop('disabled', true);
                console.log('hello')
            }
            else{
                $('.file_alert').hide();
                $('.doc').prop('disabled', false);
            }
            console.log(a.length)
        });
    });
    $(document).on("click", function(event){
        if ( $('.check_2').is(':checked') || $('.check_1').is(':checked')) {
            $('.req_mark').show();
            $('#agrem').attr('required', '');
            $('#exp_agrem').attr('required', '');
        }
        else{
            $('.req_mark').hide();
            $('#agrem').removeAttr('required');
            $('#exp_agrem').removeAttr('required');
        }
    });

    });