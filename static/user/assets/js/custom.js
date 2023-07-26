(function ($) {
    "use strict";

    // To Days-Slider
    $('.todays_slider').owlCarousel({
        loop: true,
        dots: false,
        autoplayHoverPause: true,
        autoplay: true,
        smartSpeed: 1000,
        margin: 30,
        navText: [
            "<i class='fas fa-chevron-left'></i>",
            "<i class='fas fa-chevron-right'></i>"
        ],
        nav: true,
        responsive: {
            0: {
                items: 1,
            },
            480: {
                items:2,
            },
            576: {
                items:2,
            },
            768: {
                items:3,
            },
            1200: {
                items:4,
            }
        }
    });

    // Instgram-Slider
    $('.instagram_post_slider').owlCarousel({
        loop: true,
        dots: false,
        autoplayHoverPause: true,
        autoplay: true,
        smartSpeed: 1000,
        margin: 0,
        nav: false,
        responsive: {
            0: {
                items: 2,
            },
            768: {
                items:3,
            },
            992: {
                items:4,
            },
            1200: {
                items:5,
            }
        }
    });
    // Product Modal-Slider
    $('.products_modal_sliders').owlCarousel({
        loop: true,
        dots: true,
        autoplayHoverPause: true,
        autoplay: true,
        smartSpeed: 1000,
        margin: 0,
        nav: false,
        responsive: {
            0: {
                items: 1,
            },
            768: {
                items:1,
            },
            992: {
                items:1,
            },
            1200: {
                items:1,
            }
        }
    });
    // product_single_two_img Slider
    $('.product_single_two_img').owlCarousel({
        loop: true,
        dots: true,
        autoplayHoverPause: true,
        autoplay: true,
        smartSpeed: 1000,
        margin: 0,
        nav: true,
        navText: [
            "<i class='fas fa-chevron-left'></i>",
            "<i class='fas fa-chevron-right'></i>"
        ],
        responsive: {
            0: {
                items: 1,
            },
            768: {
                items:1,
            },
            992: {
                items:1,
            },
            1200: {
                items:1,
            }
        }
    });
    // Team Slider Slider
    $('.team_slider').owlCarousel({
        loop: true,
        dots: false,
        autoplayHoverPause: true,
        autoplay: true,
        smartSpeed: 1000,
        margin: 30,
        nav: false,
        navText: [
            "<i class='fas fa-chevron-left'></i>",
            "<i class='fas fa-chevron-right'></i>"
        ],
        responsive: {
            0: {
                items: 1,
            },
            768: {
                items:2,
            },
            992: {
                items:3,
            },
            1200: {
                items:4,
            }
        }
    });


/*===========================================
			PORTFOLIO
=============================================*/
$(window).on('load', function () {
	// init Isotope
	$('#isotope-container').isotope({});


	// filter items on button click
	$('#isotope-filters').on('click', 'button', function () {

		// get filter value
		var filterValue = $(this).attr('data-filter');


		$('#isotope-container').isotope({
			filter: filterValue,
            // itemSelector: '.item',
            // filter: "*"
		});

		//  active button
		$("#isotope-filters").find('.active').removeClass('active');
		$(this).addClass('active');

	});

});


$(window).on("load", function() {
    $("#status").fadeOut();
    $("#preloader")
      .delay(350)
      .fadeOut("slow");
  });
}(jQuery));
