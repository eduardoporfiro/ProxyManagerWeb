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
    waitingDialog.show('Carregando');
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
            //Pagination
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

            //sort
            var ths = document.getElementsByClassName("orderable");
            if(ths != null){
                for (var i=0;ths.length > i;i++){
                    var th = ths[i];
                    var a = th.getElementsByTagName('a')[0];
                    if (! a.href.includes('ajax')) {
                        if(a.getAttribute('dados') == null ){
                            var texto = a.href.split('?');
                            if(url.includes('?sort=') || url.includes('ajax')){
                                url = url.split('?sort=')[0];
                                texto = url + '?' + texto[1];
                            }else{
                                texto[0] = texto[0].slice(0, -1) + url;
                                texto = texto[0] + '?' + texto[1];
                            }
                            var dados = "'"+texto + "','" + id + "','" + graphUrl+"'";
                            a.setAttribute("onClick", 'alterDATA('+dados+')');
                            a.setAttribute('dados','true');
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
setTimeout(function () {waitingDialog.hide();}, 1000);
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
                            'rgba(51,51,51, 0.2)'
                        ],
                        borderColor: [
                            'rgba(51,51,51,1)'
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


var waitingDialog = waitingDialog || (function ($) {
    'use strict';

	// Creating modal dialog's DOM
	var $dialog = $(
		'<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%; overflow-y:visible;">' +
		'<div class="modal-dialog modal-m">' +
		'<div class="modal-content">' +
			'<div class="modal-header"><h3 style="margin:0;"></h3><i class="fa fa-cog fa-spin fa-3x fa-fw" style="display: block; width: 50%;"></div>' +
			'<div class="modal-body">' +'</div>' +
		'</div></div></div>');

	return {
		/**
		 * Opens our dialog
		 * @param message Custom message
		 * @param options Custom options:
		 * 				  options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
		 * 				  options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
		 */
		show: function (message, options) {
			// Assigning defaults
			if (typeof options === 'undefined') {
				options = {};
			}
			if (typeof message === 'undefined') {
				message = 'Loading';
			}
			var settings = $.extend({
				dialogSize: 'm',
				progressType: '',
				onHide: null // This callback runs after the dialog was hidden
			}, options);

			// Configuring dialog
			$dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
			$dialog.find('.progress-bar').attr('class', 'progress-bar');
			if (settings.progressType) {
				$dialog.find('.progress-bar').addClass('progress-bar-' + settings.progressType);
			}
			$dialog.find('h3').text(message);
			// Adding callbacks
			if (typeof settings.onHide === 'function') {
				$dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
					settings.onHide.call($dialog);
				});
			}
			// Opening dialog
			$dialog.modal();
		},
		/**
		 * Closes dialog
		 */
		hide: function () {
			$dialog.modal('hide');
		}
	};

})(jQuery);
