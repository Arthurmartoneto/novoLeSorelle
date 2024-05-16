$(document).ready(function() {
    // Adicione um evento de clique às linhas da tabela com a classe 'reserva-link'
      $('.reserva-link').click(function() {
          // Recupere os detalhes da reserva
          var cliente = $(this).data('cliente');
          var email = $(this).data('email');
          var telefone = $(this).data('telefone');
          var comida = $(this).data('comida');
          var peso = $(this).data('peso');
          var precoTotal = $(this).data('preco-total');
          var data = $(this).data('data');
          var hora = $(this).data('hora');
          var fotoComida = $(this).data('foto-comida');

          // Preencha o modal com os detalhes da reserva
          $('#modalCliente').text(cliente);
          $('#modalEmail').text(email);
          $('#modalTelefone').text(telefone);
          $('#modalComida').text(comida);
          $('#modalPeso').text(peso);
          $('#modalPrecoTotal').text(precoTotal);
          $('#modalData').text(data);
          $('#modalHora').text(hora);
          $('#modalFotoComida').attr('src', fotoComida);

          // Exiba o modal
          $('#detalhesReserva').modal('show');
      });
  });

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