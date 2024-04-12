/******************************************
    File Name: custom.js
    Template Name: Landigoo
    Created By: MelodyThemes
    Envato Profile: http://themeforest.net/user/melodythemes
    Website: https://melodythemes.com
    Version: 1.0
/****************************************** */

(function($) {
    "use strict";

    // Função para ativar o smooth scroll
    function activateSmoothScroll() {
        $('a[href*=#]:not([href=#])').click(function() {
            if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') || location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
        });
    }

    // Função para ativar o scrollspy
    function activateScrollSpy() {
        $('body').scrollspy({
            target: '#mainNav',
            offset: 54
        });
    }

    // Função para tornar o menu fixo no topo
    function activateFixedMenu() {
        $(window).on('scroll', function () {
            if ($(window).scrollTop() > 50) {
                $('.header-block-top').addClass('fixed-menu');
            } else {
                $('.header-block-top').removeClass('fixed-menu');
            }
        });
    }

    // Função para adicionar a classe 'active' ao clicar nos itens do menu
    function activateMenuActiveClass() {
        $('.navbar-nav li a').on("click", function(e) {
            $('.navbar-nav li').removeClass('active');
            var $parent = $(this).parent();
            if (!$parent.hasClass('active')) {
                $parent.addClass('active');
            }
        });
    }

    // Função para inicializar o carousel
    function initializeCarousel() {
        $("#owl-demo").owlCarousel({
            autoPlay: 3000, //Set AutoPlay to 3 seconds
            items : 3,
            itemsDesktop : [1199,3],
            itemsDesktopSmall : [979,2]
        });
    }

    // Função para inicializar o slider com navegação
    function initializeSlider() {
        $('.slider-single').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: false,
            adaptiveHeight: true,
            infinite: false,
            useTransform: true,
            speed: 400,
            cssEase: 'cubic-bezier(0.77, 0, 0.18, 1)',
        });

        $('.slider-nav').slick({
            slidesToShow: 4,
            slidesToScroll: 7,
            dots: false,
            focusOnSelect: false,
            infinite: false,
            responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 4,
                }
            }, {
                breakpoint: 769,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 4,
                }
            }, {
                breakpoint: 420,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                }
            }]
        });

        $('.slider-single').on('afterChange', function(event, slick, currentSlide) {
            $('.slider-nav').slick('slickGoTo', currentSlide);
            var currrentNavSlideElem = '.slider-nav .slick-slide[data-slick-index="' + currentSlide + '"]';
            $('.slider-nav .slick-slide.is-active').removeClass('is-active');
            $(currrentNavSlideElem).addClass('is-active');
        });

        $('.slider-nav').on('click', '.slick-slide', function(event) {
            event.preventDefault();
            var goToSingleSlide = $(this).data('slick-index');

            $('.slider-single').slick('slickGoTo', goToSingleSlide);
        });
    }

    // Função para inicializar o WOW Animation
    function initializeWowAnimation() {
        new WOW().init();
    }

    // Função para inicializar o date/time picker
    function initializeDateTimePicker() {
        var date = new Date();
        var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
        $('#date-picker').datetimepicker({
            format: 'DD.MM.YYYY',
            minDate: today
        });
        $('#time-picker').datetimepicker({
            format: 'LT'
        });
    }

    // Função para inicializar o selectpicker
    function initializeSelectPicker() {
        $('.selectpicker').selectpicker();
    }

    // Função para inicializar o preloader
    function initializePreloader() {
        $(window).load(function() { 
            $("#status").fadeOut("slow"); 
            $("#loader").delay(200).fadeOut(); 
        });
    }

    // Função para mostrar o botão de scroll up
    function showScrollUpButton() {
        $(window).scroll(function(){
            if ($(this).scrollTop() > 100) {
                $('.scrollup').fadeIn();
            } else {
                $('.scrollup').fadeOut();
            }
        }); 

        $('.scrollup').click(function(){
            $("html, body").animate({ scrollTop: 0 }, 600);
            return false;
        });
    }

    // Função para abrir/fechar o painel de cores
    function toggleColorPanel() {
        $( "#color-panel .panel-button" ).click(function(){
            $( "#color-panel" ).toggleClass( "close-color-panel", "open-color-panel", 1000 );
            $( "#color-panel" ).toggleClass( "open-color-panel", "close-color-panel", 1000 );
            return false;
        });

        // Color Skins
        $('.switcher').click(function(){
            var title = jQuery(this).attr('title');     
            jQuery('#changeable-colors').attr('href', 'css/colors/' + title + '.css');                
            return false;
        }); 

        jQuery(".orange-bg").on('click',function(){
            jQuery(".logo-header img").attr("src", "images/logo.png");
            jQuery(".footer-logo .text-center img").attr("src", "images/logo.png");
            return false;
        });

        jQuery(".strong-blue-bg").on('click',function(){
            jQuery(".logo-header img").attr("src", "images/logo2.png");
            jQuery(".footer-logo .text-center img").attr("src", "images/logo2.png");
            return false;
        });

        jQuery(".moderate-green-bg").on('click',function(){
            jQuery(".logo-header img").attr("src", "images/logo3.png");
            jQuery(".footer-logo .text-center img").attr("src", "images/logo3.png");
            return false;
        });

        jQuery(".vivid-yellow-bg").on('click',function(){
            jQuery(".logo-header img").attr("src", "images/logo4.png");
            jQuery(".footer-logo .text-center img").attr("src", "images/logo4.png");
            return false;
        });
    }

    // Função para inicializar o paralaxe
    $.fn.parallax = function(options) {
        var windowHeight = $(window).height();
        var settings = $.extend({
            speed        : 0.15
        }, options);
        return this.each( function() {
            var $this = $(this);
            $(document).scroll(function(){
                var scrollTop = $(window).scrollTop();
                var offset = $this.offset().top;
                var height = $this.outerHeight();
                if (offset + height <= scrollTop || offset >= scrollTop + windowHeight) {
                    return;
                }
                var yBgPosition = Math.round((offset - scrollTop) * settings.speed);
                $this.css('background-position', 'center ' + yBgPosition + 'px');
            });
        });
    }

    // Função para inicializar o formulário de contato
    function initializeContactForm() {
        $('#contact-form').submit(function() {
            var action = $(this).attr('action');
            $("#message").slideUp(750, function() {
                $('#message').hide();
                $('#submit')
                    .after('<img src="images/ajax-loader.gif" class="loader" />')
                    .attr('disabled', 'disabled');
                $.post(action, {
                        first_name: $('#first_name').val(),
                        email: $('#email').val(),
                        phone: $('#phone').val(),
                        no_of_persons: $('#no_of_persons').val(),
                        preferred_food: $('#preferred_food').val(),
                        occasion: $('#occasion').val(),
                        verify: $('#verify').val()
                    },
                    function(data) {
                        document.getElementById('message').innerHTML = data;
                        $('#message').slideDown('slow');
                        $('#contact-form img.loader').fadeOut('slow', function() {
                            $(this).remove()
                        });
                        $('#submit').removeAttr('disabled');
                        if (data.match('success') != null) $('#contact-form').slideUp('slow');
                    }
                );
            });
            return false;
        });
    }

    // Chamar as funções necessárias ao carregar o documento
    $(document).ready(function() {
        activateSmoothScroll();
        activateScrollSpy();
        activateFixedMenu();
        activateMenuActiveClass();
        initializeCarousel();
        initializeSlider();
        initializeWowAnimation();
        initializeDateTimePicker();
        initializeSelectPicker();
        initializePreloader();
        showScrollUpButton();
        toggleColorPanel();
        $('.parallax').parallax({
            speed : 0.15
        });
        initializeContactForm();
        // Adicione outras funções de inicialização aqui, se necessário
    });

})(jQuery);
