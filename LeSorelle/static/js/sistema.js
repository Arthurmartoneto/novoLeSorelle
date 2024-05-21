$(document).ready(function() {
    $('.prato-link').click(function() {
        var nome = $(this).data('nome');
        var descricao = $(this).data('descricao');
        var valor = $(this).data('valor');
        var id = $(this).data('id');
        var status = $(this).data('status');
        var imagem = $(this).data('imagem');

        $('#modalNome').text(nome);
        $('#modalDescricao').text(descricao);
        $('#modalValor').text(valor);
        $('#modalId').text(id);

        // Adiciona a classe CSS com base no status
        $('#modalStatus').removeClass('text-success text-danger');
        if (status === 'ativo') {
        $('#modalStatus').addClass('text-success').text('Ativo');
        $('#pratoButton').html('<button type="button" class="col-3 btn btn-warning mb-3 inativar-prato" data-id="' + id + '">Inativar</button>');
        } else {
        $('#modalStatus').addClass('text-danger').text('Inativo');
        $('#pratoButton').html('<button type="button" class="col-3 btn btn-success mb-3 ativar-prato" data-id="' + id + '">Ativar</button>');
        }

        $('#modalImagem').attr('src', imagem);
        $('#modalPratoDetalhes').modal('show');

        // Verifique o status do prato e ajuste os botões correspondentes
        if (status === 'ativo') {
            $('.inativar-prato').show();
            $('.ativar-prato').hide();
        } else {
            $('.inativar-prato').hide();
            $('.ativar-prato').show();
        }
    });
});

$(document).ready(function() {
    // Adicione um evento de clique aos elementos da tabela com a classe 'reserva-link'
    $('.reserva-link').click(function() {
        // Recupere os detalhes da reserva
        var imgSrc = $(this).data('img-src');
        var nomeProduto = $(this).data('nome-produto');
        var peso = $(this).data('peso');
        var precoTotal = $(this).data('preco-total');
        var data = $(this).data('data');
        var hora = $(this).data('hora');

        // Preencha o modal com os detalhes da reserva
        $('#modalImagem').attr('src', imgSrc);
        $('#modalNomeProduto').text(nomeProduto);
        $('#modalPeso').text(peso);
        $('#modalPrecoTotal').text(precoTotal);
        $('#modalData').text(data);
        $('#modalHora').text(hora);

        // Exiba o modal
        $('#myModal').modal('show');
    });
  });

  $(document).ready(function() {
      // Evento de clique para o botão de cancelar entrega
      $('#cancelarEntrega').click(function() {
          // Coloque aqui o código para cancelar a entrega
          // Por exemplo, você pode enviar uma requisição AJAX para o servidor para cancelar a entrega
          // Ou exibir uma mensagem de confirmação ao usuário e tomar a ação apropriada
          // Neste exemplo, apenas fecharemos o modal
          $('#myModal').modal('hide');
      });
  });


// Função para desativar o botão após o envio do formulário
function disableButton() {
document.getElementById("submitBtn").disabled = true;
document.getElementById("submitBtn").innerText = 'Enviando...';
}


$(document).ready(function() {
    $('#adicionarbtn').on('click', function() {
        var btn = $(this);
        btn.button('loading'); // Exibir "Aguarde..." no botão

        // Submeter o formulário
        $('#addPratoForm').submit();
    });
});


function adicionarPrato() {
    var pratoModel = document.querySelector(".prato");
    var pratoContainer = document.getElementById("pratoContainer");
    
    // Clone o modelo de prato sempre que precisarmos adicionar um novo
    var novoPrato = pratoModel.cloneNode(true);
    novoPrato.style.display = "block";
        
    // Adiciona botão "Remover" ao lado do novo campo de prato
    pratoContainer.appendChild(novoPrato);
}


function removerPrato(botaoRemover) {
    var prato = botaoRemover.closest('.prato');
    prato.parentNode.removeChild(prato);
}


// Função para obter o token CSRF do cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// Função para marcar uma reserva como cancelada
function marcarCancelado(reservaId) {
    if (confirm('Tem certeza que deseja cancelar esta reserva?')) {
        fetch(`/cancelar_reserva/${reservaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Reserva cancelada com sucesso.');
                location.reload();  // Recarrega a página para atualizar o status da reserva
            } else {
                alert('Falha ao cancelar a reserva. Tente novamente.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao cancelar a reserva. Tente novamente.');
        });
    }
}


// Função para obter o token CSRF do cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function marcarEmPreparo(reservaId) {
    if (confirm('Marcar esta reserva como Em Preparo?')) {
        fetch(`/marcar_em_preparo/${reservaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Reserva marcada como Em Preparo.');
                location.reload();  // Recarrega a página para atualizar o status da reserva
            } else {
                alert('Falha ao marcar a reserva como Em Preparo. Tente novamente.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao marcar a reserva como Em Preparo. Tente novamente.');
        });
    }
}


// Função para obter o token CSRF do cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function marcarPronto(reservaId) {
    if (confirm('Marcar esta reserva como Pronto?')) {
        fetch(`/marcar_pronto/${reservaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Reserva marcada como Pronto.');
                location.reload();  // Recarrega a página para atualizar o status da reserva
            } else {
                alert('Falha ao marcar a reserva como Pronto. Tente novamente.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao marcar a reserva como Pronto. Tente novamente.');
        });
    }
}


// Função para obter o token CSRF do cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function marcarFinalizado(reservaId) {
    if (confirm('Marcar esta reserva como Finalizada?')) {
        fetch(`/marcar_finalizado/${reservaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Reserva marcada como Finalizada.');
                location.reload();  // Recarrega a página para atualizar o status da reserva
            } else {
                alert('Falha ao marcar a reserva como Finalizada. Tente novamente.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao marcar a reserva como Finalizada. Tente novamente.');
        });
    }
}
