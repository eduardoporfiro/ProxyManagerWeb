$(document).ready(function(){
    for (var i=0; document.getElementsByClassName('list-group').length> i;i++){
        doc = document.getElementsByClassName('list-group')[i];
        if(doc.getElementsByClassName("teste").length>0){
            a = doc.getElementsByClassName("teste")[0];
            a.click();
        }

    }
});
$(document).on('click', "a[dados='true']", function(event) {
  event.preventDefault();    // Now the link doesn't do anything
  var href = this.href;      // The link's URL is in this variable
});

function alterDATA(url, id, graphUrl) {
    var graph_id = 'graph-'+id;
    if(! id.includes('tabela'))
        id = 'tabela-'+id;
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
            },
        success: function (data) {
            var div = document.getElementById(id);
            div.innerHTML = data;
            var ul = document.getElementsByClassName("pagination");
            if(ul != null){
                for (var i=0;ul.length > i;i++){
                    var li = ul[i];
                    li = li.getElementsByTagName('li');
                    if(li != null) {
                        for (var j = 0; li.length > j; j++) {
                            var valor = li[j];
                            var a = valor.getElementsByTagName('a')[0];
                            if (! a.href.includes('ajax')) {
                                if(a.getAttribute('dados') == null ){
                                    var texto = a.href.split('?');
                                    if(url.includes('?page=') || url.includes('ajax')){
                                        url = url.split('?page=')[0];
                                        texto = url + '?' + texto[1];
                                    }else{
                                        texto[0] = texto[0].slice(0, -1) + url;
                                        texto = texto[0] + '?' + texto[1];
                                    }
                                    var dados = "'"+texto + "','" + id + "','" + graphUrl+"'";
                                    a.setAttribute("onClick", 'alterDATA('+dados+')');
                                    a.setAttribute("class",'btn btn-dark');
                                    a.setAttribute('dados','true');
                                }
                            }
                        }
                    }
                }
            }
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