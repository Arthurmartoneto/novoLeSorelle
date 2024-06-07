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

// notifications --------------------

// Script JavaScript para atualizar dinamicamente a lista de notificações e limpar as notificações
$(document).ready(function() {

    // Elemento de áudio
    var notificationSound = document.getElementById("notificationSound");

    // Definir evento para o áudio quando ele estiver pronto para ser reproduzido
    notificationSound.oncanplaythrough = function() {
        // Obter notificações quando o áudio estiver pronto para ser reproduzido
        getNotifications();
    };

    function getNotifications() {
        $.ajax({
            url: "/get-notifications/",
            type: "GET",
            success: function(response) {
                $("#notificationItems").empty();
                // Contador de notificações
                var notificationCount = response.notifications.length;
                $("#notificationCount").text(notificationCount); // Atualiza o contador
                $.each(response.notifications, function(index, notification) {
                    // Cria um novo item de lista para a notificação
                    var listItem = $("<li>").addClass("bg-dark list-group-item border-0");
                    // Cria os elementos HTML para exibir os detalhes da notificação
                    var notificationDetails = $("<div>").addClass("d-flex align-items-center");
                    var notificationIcon = $("<div>").addClass("mr-3").append('<i class="mdi mdi-bell-ring mdi-24px text-danger"></i>');
                    var notificationContent = $("<div>");
                    var subjectParagraph = $("<p>").addClass("mb-2 text-muted").text("Assunto: ");
                    var subjectStrong = $("<strong>").addClass("text-light mb-3").text(notification.subject);
                    var messageParagraph = $("<p>").addClass("mb-0").text("Produto: " + notification.message);
                    var createdAtParagraph = $("<p>").addClass("mb-0 text-muted small").text(notification.created_at); // Adicionando o horário
                    // Adiciona os elementos HTML ao conteúdo da notificação
                    subjectParagraph.append(subjectStrong);
                    notificationContent.append(subjectParagraph, messageParagraph);
                    // Adiciona o conteúdo da notificação ao item de lista
                    notificationDetails.append(notificationIcon, notificationContent, createdAtParagraph);
                    listItem.append(notificationDetails);
                    // Adiciona o item de lista à lista de notificações
                    $("#notificationItems").append(listItem);
                    // Reproduzir som de notificação
                    notificationSound.play();
                });
            },
            error: function(xhr, status, error) {
                console.error("Erro ao obter notificações:", error);
            }
        });
    }

    // Função para limpar as notificações
    function clearNotifications() {
        // Altera o texto do botão para "Limpando..."
        $("#clearNotificationsBtn").text("Limpando...");
        // Realiza a requisição AJAX para limpar as notificações
        $.ajax({
            url: "/clear-notifications/",
            type: "POST",
            beforeSend: function(xhr, settings) {
                // Obtenha o token CSRF do cookie
                var csrftoken = getCookie('csrftoken');
                // Defina o cabeçalho CSRFToken na solicitação
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function(response) {
                // Limpar a lista de notificações
                $("#notificationItems").empty();
                // Definir o contador de notificações como zero
                $("#notificationCount").text("0");
                // Retorna o texto original do botão após a conclusão da limpeza
                $("#clearNotificationsBtn").text("Limpar Notificações");
                // Atualiza a página
                location.reload();
            },
            error: function(xhr, status, error) {
                console.error("Erro ao limpar notificações:", error);
                // Retorna o texto original do botão em caso de erro
                $("#clearNotificationsBtn").text("Limpar Notificações");
            }
        });
    }

    // Função auxiliar para obter o valor do cookie CSRF
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

    // Chamar a função para obter notificações quando a página é carregada
    getNotifications();

    // Atualizar a lista de notificações a cada 30 segundos
    setInterval(getNotifications, 30000);

    // Adicionar evento de clique para o botão "Limpar Notificações"
    $("#clearNotificationsBtn").click(function() {
        clearNotifications();
    });
});


// Impedir que o dropdown desapareça ao clicar nele
$(document).on('click', '#notificationList', function (e) {
    e.stopPropagation();
});


// Blog ----------------------------------------------------------------------
$(document).ready(function() {
    // Evento de clique em uma linha da tabela
    $('.blog-link').click(function() {
        // Obter os dados do blog da linha clicada
        var id = $(this).data('id');
        var descricao = $(this).data('descricao');
        var link = $(this).data('link');
        var usuario = $(this).data('usuario');
        var imagem = $(this).data('imagem');

        // Preencher o modal de detalhes com os dados do blog
        $('#modalId').text(id); // Atualizar o valor do modalId
        $('#modalDescricao').text(descricao);
        $('#modalLink').attr('href', link);
        $('#modalUsuario').text(usuario);
        $('#modalImagemBlog').attr('src', imagem);

        // Abrir o modal de detalhes do blog
        $('#modalBlogDetalhes').modal('show');
    });

    // Evento de clique no botão de editar no modal de detalhes do blog
    $('#editarBlog').click(function() {
        // Obter os dados do blog do modal de detalhes
        var id = $('#modalId').text(); // Agora vai pegar o ID do blog corretamente
        var descricao = $('#modalDescricao').text();
        var link = $('#modalLink').attr('href');
        var usuario = $('#modalUsuario').text();
        var imagem = $('#modalImagemBlog').attr('src'); // Obter a URL da imagem do modal de detalhes
        
        // Preencher o modal de edição com os dados do blog
        $('#editDescricao').val(descricao);
        $('#editLink').val(link);
        $('#editUsuario').val(usuario);
        $('#previewImagem').attr('src', imagem); // Exibir a mesma imagem no modal de edição
        $('#modalBlogDetalhes').modal('hide');
        $('#modalBlogEdicao').modal('show');
    });

    $('#salvarEdicaoBlog').click(function() {
        // Obter os dados do formulário de edição
        var id = $('#modalId').text();
        var descricao = $('#editDescricao').val();
        var link = $('#editLink').val();
        var usuario = $('#editUsuario').val();
        var imagem = $('#editImagem')[0].files[0]; // Para enviar arquivos, pegamos o primeiro elemento do array de arquivos
        
        console.log("Dados do formulário de edição:");
        console.log("ID:", id);
        console.log("Descrição:", descricao);
        console.log("Link:", link);
        console.log("Usuário:", usuario);
        console.log("Imagem:", imagem);
    
        // Criar um objeto FormData para enviar os dados do formulário via AJAX
        var formData = new FormData();
        formData.append('id', id);
        formData.append('descricao', descricao);
        formData.append('link', link);
        formData.append('usuario', usuario);
        formData.append('imagem', imagem);
    
        var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
        
        // Enviar os dados do formulário via AJAX
        $.ajax({
            headers: {
                'X-CSRFToken': csrftoken // inclui o token CSRF como cabeçalho na requisição
            },
            url: '/editar_blog/' + id + '/', // URL da sua view Django
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(response);
                if (response.status === 'success') {
                    // Sucesso: recarregar a página
                    location.reload();
                } else {
                    // Erro: exibir mensagem de erro
                    alert('Erro ao salvar: ' + response.errors);
                }
            },
            error: function(xhr, status, error) {
                // Erro na requisição AJAX
                console.error(xhr.responseText);
                alert('Erro na requisição AJAX: ' + error);
            }
        });
    });
});
