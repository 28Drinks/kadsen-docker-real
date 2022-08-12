// $(function() {
//     $('a#getbot').bind('click', function() {
//         $('#bots-container').append('<div class: "card-body"></div>')
//     }, function(data) {
//         var image = "<div class='image-container'> <img src='image' class='image'></div>";
//         var name = "<h1 class='name'> (name) <h1>"
//         $("card-body").append(image, name)
//         $("#result").text(data.result);
//     });
//     return false;
// })


// var obj = {
//     image:bot.image,
//     name:bot.name,
//     share:bot.display_share,
//     bet:bot.bet,
//     price:bot.price,
//   };
//   $.each( obj, function( key, value ) {
//     alert( key + ": " + value );
//   });


// var codeBlock = '<div class="card">' +
//                     '<div class="image-container">' +
//                         '<img src="" class="image">' +
//                     '</div>' +
//                     '<div class="card-body">' +
//                         '<h1 class="name"> variable for image </h1>' +
//                         '<div class="split">' +
//                             '<div class="value share">' +
//                             '<h5>Profit Share:</h5>' +
//                             '<h1 class="share"> variable for share </h1>' +
//                         '</div>' +
//                     '</div>' +
//                 '</div>';


// $(document).ready(function(){
//     $("button").click(function(){
//         $("#bot-container").prepend(codeBlock);
//     });
// });

$(document).ready(function(){
    $("#button-price-asce").click(function(){
        $("#bot-container-price-a").toggle();
    });
    $("#button-price-desc").click(function(){
        $("#bot-container-price-d").toggle();
    });
    $("#button-bet-asce").click(function(){
        $("#bot-container-bet-a").toggle();
    });
    $("#button-bet-desc").click(function(){
        $("#bot-container-bet-d").toggle();
    });
});

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

  var x = 29

  var data = google.visualization.arrayToDataTable([
    ['Date', 'Soccer', 'League of Legends', 'CounterStrike'],
    ['13.07',  9.7,      14.26,              26],
    ['14.07',  9.8,      13.81,              27],
    ['15.07',  11.3,       13.52,            28],
    ['16.07',  10.6,      14.29,             (x)]
  ]);

  var options = {
    title: 'Company Performance',
    curveType: 'function',
    legend: { position: 'bottom' }
  };

  var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

  chart.draw(data, options);
}

