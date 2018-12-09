$(document).ready(function(){
    for (var i=0; document.getElementsByClassName('list-group').length;i++){
        doc = document.getElementsByClassName('list-group')[i];
        if(doc.getElementsByClassName("teste").length>0){
            a = doc.getElementsByClassName("teste")[0];
            a.click();
        }

    }
});

function alterDATA(url, id, graphUrl) {
    var graph_id = 'graph-'+id;
    id = 'tabela-'+id;
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
            },
        success: function (data) {
            var div = document.getElementById(id);
            div.innerHTML = data;
        },
        error: function () {
            var div = document.getElementById(id);
            div.innerHTML = '<p>TESTE</p>';
        }
    });

    grafico(graphUrl, graph_id);
}
function grafico(url, graph_id) {
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
            },
        success: function (data) {
            var teste = "["+data+"]";
            var teste = JSON.parse(teste);
            var teste = teste[0];
            var ctx = document.getElementById(graph_id);
            console.log(graph_id);
            var prices = teste['dado'];
            var names = teste['id'];
            var productsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: names,
                    datasets: [{
                        label: 'Dados',
                        data: prices,
                        backgroundColor: [
                            'rgba(51,51,51, 0.2)',
                            'rgba(51,51,51, 0.2)',
                            'rgba(251,51,51, 0.2)',
                            'rgba(51,51,51, 0.2)',
                            'rgba(51,51,51, 0.2)',
                            'rgba(51,51,51, 0.2)'
                        ],
                        borderColor: [
                            'rgba(51,51,51,1)',
                            'rgba(51,51,51, 1)',
                            'rgba(51,51,51, 1)',
                            'rgba(51,51,51, 1)',
                            'rgba(51,51,515, 1)',
                            'rgba(51,51,51, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
        },
        error: function () {
        }
    });
}