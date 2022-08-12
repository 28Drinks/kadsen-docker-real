$(document).ready(function(){

    $('.btn').click(function(){
        $.ajax({
            url: 'get_stats.py',
            type: 'POST',
            data: {
                lotto_amount: get_stats()
            },
            success: function(response){
                $('.lotto_stats').append('<p>' + response.data + '</p>')
            }
        })
    })
})
