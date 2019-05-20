$(document).on('click', "a[dados='true']", function(event) {
  event.preventDefault();    // Now the link doesn't do anything
  var href = this.href;      // The link's URL is in this variable
});
$(document).ready(function(){
    $.ajax({
        url: '{% url 'block:edit_proxy' proxy.id %}',
        data: {},
        success: function (data) {
            var div = document.getElementById("proxy-div");
            div.innerHTML = data;
        }
    });
    $(".nav-tabs a").click(function(){
        var url = $(this).attr("form-url");  // get the url of the `load_cities` view
        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
            data: {
                    // add the country id to the GET parameters
            },
            success: function (data) {// `data` is the return of the `load_cities` view functio
              //$("#id_broker").html(data);  // replace the contents of the city input with the data that came from the serve$
                if($(this).id = "proxy-tab") {
                    var div = document.getElementById("proxy-div");
                    div.innerHTML = data;
                }
                if($(this).id = "broker-tab") {
                    var div = document.getElementById("broker-div");
                    div.innerHTML = data;
                }
                if($(this).id = "mqtt-tab") {
                    var div = document.getElementById("mqtt-div");
                    div.innerHTML = data;
                    alterdata(url);
                }

                if($(this).id = "sensor-tab") {
                    var div = document.getElementById("sensor-div");
                    div.innerHTML = data;
                }
            },
            error: function () {
                var div = document.getElementById("broker-div");
                div.innerHTML = '<p>TESTE</p>';
            }
        });
        $(this).tab('show');
    });
});

function alterdata(url){
    var id = 'mqtt-div';
    var ul = document.getElementsByClassName("pagination");
    if(ul != null) {
        for (var i = 0; ul.length > i; i++) {
            var li = ul[i];
            li = li.getElementsByTagName('li');
            if (li != null) {
                for (var j = 0; li.length > j; j++) {
                    var valor = li[j];
                    var a = valor.getElementsByTagName('a')[0];
                    if (!a.href.includes('ajax')) {
                        if (a.getAttribute('dados') == null) {
                            var texto = a.href.split('?');
                            if (url.includes('?page=')) {
                                url = url.split('?page=')[0];
                                texto = url + '?' + texto[1];
                            } else {
                                texto[0] = texto[0].slice(0, -1) + url;
                                texto = texto[0] + '?' + texto[1];
                            }
                            var dados = "'" + texto + "','" + id + "','" + graphUrl + "'";
                            a.setAttribute("onClick", 'alterDATA(' + dados + ')');
                            a.setAttribute("class", 'btn btn-dark');
                            a.setAttribute('dados', 'true');
                        }
                    }
                }
            }
        }
    }
};