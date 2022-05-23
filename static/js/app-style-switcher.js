$(function () {
    "use strict";

    function handlelogobg() {
        $('.theme-color .theme-item .theme-link').on("click", function () {
            var logobgskin = $(this).attr("data-logobg");
            $('.topbar .top-navbar .navbar-header').attr("data-logobg", logobgskin);
        });
    };
    handlelogobg();

    //****************************
    /* Top navbar Theme Change function Start */
    //****************************
    function handlenavbarbg() {
        if ($('#main-wrapper').attr('data-navbarbg') == 'skin6') {
            // do this
            $(".topbar .navbar").addClass('navbar-light');
            $(".topbar .navbar").removeClass('navbar-dark');
        } else {
            // do that

        }
        $('.theme-color .theme-item .theme-link').on("click", function () {
            var navbarbgskin = $(this).attr("data-navbarbg");
            $('#main-wrapper').attr("data-navbarbg", navbarbgskin);
            $('.topbar .navbar-collapse').attr("data-navbarbg", navbarbgskin);
            if ($('#main-wrapper').attr('data-navbarbg') == 'skin6') {
                // do this
                $(".topbar .navbar").addClass('navbar-light');
                $(".topbar .navbar").removeClass('navbar-dark');
            } else {
                // do that
                $(".topbar .navbar").removeClass('navbar-light');
                $(".topbar .navbar").addClass('navbar-dark');
            }
        });

    };
    handlenavbarbg();

    //****************************
    /* Manage sidebar bg color */
    //****************************
    function handlesidebarbg() {
        $('.theme-color .theme-item .theme-link').on("click", function () {
            var sidebarbgskin = $(this).attr("data-sidebarbg");
            $('.left-sidebar').attr("data-sidebarbg", sidebarbgskin);
            $('.scroll-sidebar').attr("data-sidebarbg", sidebarbgskin);
        });
    };
    handlesidebarbg();

    //****************************
    /* sidebar position */
    //****************************
    function handlesidebarposition() {
        $('#sidebar-position').change(function () {
            if ($(this).is(":checked")) {
                $('#main-wrapper').attr("data-sidebar-position", 'fixed');
                $('.topbar .top-navbar .navbar-header').attr("data-navheader", 'fixed');
            } else {
                $('#main-wrapper').attr("data-sidebar-position", 'absolute');
                $('.topbar .top-navbar .navbar-header').attr("data-navheader", 'relative');
            }
        });
    };
    handlesidebarposition();

    //****************************
    /* Header position */
    //****************************
    function handleheaderposition() {
        $('#header-position').change(function () {
            if ($(this).is(":checked")) {
                $('#main-wrapper').attr("data-header-position", 'fixed');
            } else {
                $('#main-wrapper').attr("data-header-position", 'relative');
            }
        });
    };
    handleheaderposition();

    //****************************
    /* sidebar position */
    //****************************
    function handleboxedlayout() {
        $('#boxed-layout').change(function () {
            if ($(this).is(":checked")) {
                $('#main-wrapper').attr("data-boxed-layout", 'boxed');
            } else {
                $('#main-wrapper').attr("data-boxed-layout", 'full');
            }
        });

    };
    handleboxedlayout();

    //****************************
    /* Header position */
    //****************************
    function handlethemeview() {
        $('#theme-view').change(function () {
            if ($(this).is(":checked")) {
                $('body').attr("data-theme", 'dark');
            } else {
                $('body').attr("data-theme", 'light');
            }
        });
    };
    handlethemeview();

    var setsidebartype = function () {
        var width = (window.innerWidth > 0) ? window.innerWidth : this.screen.width;
        if (width < 1170) {
            $("#main-wrapper").attr("data-sidebartype", "mini-sidebar");
            $("#main-wrapper").addClass("mini-sidebar");
        } else {
            $("#main-wrapper").attr("data-sidebartype", "full");
            $("#main-wrapper").removeClass("mini-sidebar");
        }
    };
    $(window).ready(setsidebartype);
    $(window).on("resize", setsidebartype);

    var prevScrollpos = window.pageYOffset;
    window.onscroll = function () {
        var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos && (width < 767 || document.getElementById("topnavbar").style.top == "-80px")) {
            $("#topnavbar").css("top", "0");
        } else if (width < 767 && prevScrollpos < currentScrollPos && !$("#main-wrapper").hasClass("show-sidebar")) {
            $("#topnavbar").css("top", "-80px");
        } else if (width >= 767 || !($(document).height() > $(window).height())) {
            $("#topnavbar").css("top", "0");
        }
        prevScrollpos = currentScrollPos;
    }

    $("#topnavbarnav div a.nav-toggler.waves-effect.waves-light.d-block.d-md-none").on('click', function () {

    });

    $(document).mouseup(function (e) {

        if ($("#main-wrapper").hasClass("show-sidebar")) {
            var container = $("#main-wrapper aside.left-sidebar div.scroll-sidebar.ps-container.ps-theme-default");

            if (!container.is(e.target) && container.has(e.target).length === 0 && !$('#modalChangeProfile').hasClass('show')) {

                if (e.target.className == "ti-close" || e.target.className == "nav-toggler waves-effect waves-light d-block d-md-none") {
                    $("#topnavbarnav div a.nav-toggler.waves-effect.waves-light.d-block.d-md-none").trigger("click");
                }
                $("#topnavbarnav div a.nav-toggler.waves-effect.waves-light.d-block.d-md-none").trigger("click");

            }
        }

    });

    $("a.nav-toggler.waves-effect.waves-light.d-block.d-md-none").click(function (e) {
        if ($("#main-wrapper").hasClass("show-sidebar")) {
            $("div.page-wrapper").css('filter', '');
            $("div.page-wrapper").css('pointer-events', 'auto');
        } else {
            $("div.page-wrapper").css('filter', 'blur(3px)');
            $("div.page-wrapper").css('pointer-events', 'none');
        }

    });

    $('.page-wrapper').append('<div id="toTop" class="btn btn-info">Back to Top</div>');
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#toTop').fadeIn();
        } else {
            $('#toTop').fadeOut();
        }
    });
    $('#toTop').click(function () {
        $('html, body').animate({ 'scrollTop': 0 }, 1000, 'easeInOutCirc');
        return false;
    });


});