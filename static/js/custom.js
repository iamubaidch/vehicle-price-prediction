	$(window).on('load', function() {
	
		"use strict";
		
		var preloader = $('#loading'),
			loader = preloader.find('#loading-center');
			loader.fadeOut();
			preloader.delay(400).fadeOut('slow');		
	});

$(window).on('scroll', function() {
		
		"use strict";
	
		
		var b = $(window).scrollTop();
		
		if( b > 80 ){		
			$(".wsmainfull").addClass("scroll");
		} else {
			$(".wsmainfull").removeClass("scroll");
		}				

	});



	$(document).ready(function() {
			
		"use strict";


		new WOW().init();
		$(".accordion > .accordion-item.is-active").children(".accordion-panel").slideDown();
				
		$(".accordion > .accordion-item").on('click', function() {
			$(this).siblings(".accordion-item").removeClass("is-active").children(".accordion-panel").slideUp();
			$(this).toggleClass("is-active").children(".accordion-panel").slideToggle("ease-out");
		});

		$('ul.tabs-1 li').on('click', function(){
			var tab_id = $(this).attr('data-tab');

			$('ul.tabs-1 li').removeClass('current');
			$('.tab-content').removeClass('current');

			$(this).addClass('current');
			$("#"+tab_id).addClass('current');
		});

	});
