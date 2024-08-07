(function ($) {
    'use strict';

    $(function () {
        $('#tabs').tabs();
    });

    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        var box = $('.header-text').height();
        var header = $('header').height();

        if (scroll >= box - header) {
            $('header').addClass('background-header');
        } else {
            $('header').removeClass('background-header');
        }
    });

    $('.schedule-filter li').on('click', function () {
        var tsfilter = $(this).data('tsfilter');
        $('.schedule-filter li').removeClass('active');
        $(this).addClass('active');
        var imagePath = '../static/assets/images/schedule/' + tsfilter + '.png';
        $('.schedule-image').attr('src', imagePath);
    });

    // Window Resize Mobile Menu Fix
    mobileNav();

    // Scroll animation init
    window.sr = new scrollReveal();

    // Menu Dropdown Toggle
    if ($('.menu-trigger').length) {
        $('.menu-trigger').on('click', function () {
            $(this).toggleClass('active');
            $('.header-area .nav').slideToggle(200);
        });
    }

    $(document).ready(function () {
        $(document).on('scroll', onScroll);

        //smoothscroll
        $('.scroll-to-section a[href^="#"], a.logo[href^="#"]').on(
            'click',
            function (e) {
                e.preventDefault();
                $(document).off('scroll');

                $('a').each(function () {
                    $(this).removeClass('active');
                });
                $(this).addClass('active');

                var target = this.hash,
                    menu = target;
                var target = $(this.hash);
                $('html, body')
                    .stop()
                    .animate(
                        {
                            scrollTop: target.offset().top + 1,
                        },
                        500,
                        'swing',
                        function () {
                            window.location.hash = '';
                            $(document).on('scroll', onScroll);
                        }
                    );
            }
        );
    });

    function onScroll(event) {
        var scrollPos = $(document).scrollTop();
        $('.nav a').each(function () {
            var currLink = $(this);
            var refElement = $(currLink.attr('href'));
            if (
                refElement.position().top <= scrollPos &&
                refElement.position().top + refElement.height() > scrollPos
            ) {
                $('.nav ul li a').removeClass('active');
                currLink.addClass('active');
            } else {
                currLink.removeClass('active');
            }
        });
    }

    // Page loading animation
    $(window).on('load', function () {
        $('#js-preloader').addClass('loaded');
    });

    // Window Resize Mobile Menu Fix
    $(window).on('resize', function () {
        mobileNav();
    });

    // Window Resize Mobile Menu Fix
    function mobileNav() {
        var width = $(window).width();
        $('.submenu').on('click', function () {
            if (width < 767) {
                $('.submenu ul').removeClass('active');
                $(this).find('ul').toggleClass('active');
            }
        });
    }
})(window.jQuery);

document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("contact");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        // Perform form validation if needed
        var name = document.getElementById("name").value.trim();
        var number = document.getElementById("number").value.trim();
        var email = document.getElementById("email").value.trim();
        var subject = document
            .getElementById("subject")
            .value.trim();
        var message = document
            .getElementById("message")
            .value.trim();
        var csrfToken = document.querySelector('input[name="csrf_token"]').value;

        if (
            name === "" ||
            number === "" ||
            email === "" ||
            subject === "" ||
            message === ""
        ) {
            alert("Please fill out all fields.");
            return;
        }

        // Submit form data via AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/");
        xhr.setRequestHeader(
            "Content-Type",
            "application/json;charset=UTF-8"
        ); // Set content type to JSON
        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                alert(response.message); // Show success message from server
                form.reset();
            } else {
                alert(
                    "Failed to send message. Please try again later."
                );
            }
        };
        xhr.onerror = function () {
            alert(
                "Failed to send message. Please try again later."
            );
        };
        var formData = {
            name: name,
            number: number,
            email: email,
            subject: subject,
            message: message,
            csrf_token: csrfToken, // Include CSRF token in the request
        };
        xhr.send(JSON.stringify(formData));
    });
});