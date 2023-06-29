jQuery(document).ready(function ($) {
	let mobilewidth = 1024, //mobile delimeter
		headerScrollMenuHeight = parseInt($('.wrapper').css('--scroll-menu-height'));

	//fixed-menu
	$(window).on("scroll", function () {
		menuOnScroll();
	});
	menuOnScroll();

	function menuOnScroll() {
		if ($(this).scrollTop() > 0) {
			$(".wrapper").addClass("scroll");
		} else {
			$(".wrapper").removeClass("scroll");
		}
	}

	function mobileMenu(selector) {

		let menu = $(selector);
		let button = menu.find('#hamburger');
		let overlay = menu.find('#menu-overlay');

		button.on('click', () => toggleMenu());
		overlay.on('click', () => toggleMenu());

		function toggleMenu() {
			if ($(window).width() <= mobilewidth) {
				menu.toggleClass('menu-active');

				if (menu.hasClass('menu-active')) {
					$('body').css('overflow', 'hidden');
				} else {
					$('body').css('overflow', 'visible');
				}
			}
		}
	}

	//init menu
	mobileMenu('#header-menu');

	//smooth scroll
	$(".js-scroll-to").on("click", function (event) {
		let url = $(this).attr('href');
		let anchor = getHashFromUrl(url);
		let top = $('#' + anchor).offset().top - parseInt($('#' + anchor).css('marginTop'));
		$('body,html').animate({
			scrollTop: top - headerScrollMenuHeight
		}, 750);
	});
	function getHashFromUrl(url) {
		return $("<a />").attr("href", url)[0].hash.replace(/^#/, "");
	}

	// slider
	function initBlogSlider() {
		$('.js-blog-slider').slick({
			slidesToShow: 3,
			slidesToScroll: 1,
			arrows: true,
			prevArrow: '<div class="sliderPrev"></div>',
			nextArrow: '<div class="sliderNext"></div>',
			appendArrows: $('.js-blog-slider-nav'),
			variableWidth: true,
			// responsive: [
			// 	{
			// 		breakpoint: 1025,
			// 		settings: {
			// 			slidesToShow: 3
			// 		}
			// 	},
			// 	{
			// 		breakpoint: 600,
			// 		settings: {
			// 			slidesToShow: 2
			// 		}
			// 	}
			// ]
		});
	}
	initBlogSlider();

	// showcase slider
	function initShowcaseSlider() {
		$('.js-showcase').slick({
			slidesToShow: 1,
			slidesToScroll: 1,
			arrows: false,
			infinite: true,
			variableWidth: true,
			centerMode: true,
			cssEase: 'linear'
		});
	}
	//initShowcaseSlider();

	//animations on page scroll	
	const sliderShowcase = document.querySelector('.js-showcase');
	const sliderProjects1 = document.querySelector('.js-project-row-1');
	const sliderProjects2 = document.querySelector('.js-project-row-2');	

	// create slider items clones and set position
	function createSliderItems(slider, slider_item) {		
		const items = slider.querySelectorAll(slider_item);
		for (let i = 0; i < 3; i++) {
			items.forEach(item => {
				let clone = item.cloneNode(true);
				clone.classList.add('clone');
				slider.appendChild(clone);			
			});
		}
		transform_start = 'matrix3d(1,0,0.00,0,0.00,1,0.00,0,0,0,1,0,-1500,0,0,1)';	
        slider.style.webkitTransform = transform_start;      
        slider.style.msTransform = transform_start;       
        slider.style.transform = transform_start;        
	}
	if (sliderProjects1 || sliderProjects2 || sliderShowcase) {
		createSliderItems(sliderShowcase, '.showcase__slider-item');
		createSliderItems(sliderProjects1, '.projects__list-item');
		createSliderItems(sliderProjects2, '.projects__list-item');	
		
		let lastScrollPosition = window.pageYOffset;	
		$(document).on('wheel scroll load', (function (e) {
			let currentScrollPosition = window.pageYOffset;
			let direction;

			if (currentScrollPosition > lastScrollPosition) {
			  direction = 'down';
			  scrollDelta = lastScrollPosition - currentScrollPosition;
			} else {
			  direction = 'up';
			  scrollDelta = currentScrollPosition - lastScrollPosition; 
			}
			lastScrollPosition = currentScrollPosition;			

			if (direction === 'down') {	
				if (elementInViewport(sliderShowcase)) {			
					transform(sliderShowcase, scrollDelta*1.5, 'right')	//multiply scrollDelta for more nice effect
				}		
				if (elementInViewport(sliderProjects1)) {			
					transform(sliderProjects1, scrollDelta, 'left')	
				}		
				if (elementInViewport(sliderProjects2)) {			
					transform(sliderProjects2, scrollDelta, 'right')	
				}
			} else {
				if (elementInViewport(sliderShowcase)) {			
					transform(sliderShowcase, scrollDelta*1.5, 'left')	//multiply scrollDelta for more nice effect
				}	
				if (elementInViewport(sliderProjects1)) {			
					transform(sliderProjects1, scrollDelta, 'right')	
				}		
				if (elementInViewport(sliderProjects2)) {			
					transform(sliderProjects2, scrollDelta, 'left')	
				}	
			}		
			
		}));
	}
	
	function elementInViewport(el, offset) {
		var elinfo = {
			"top":el.offsetTop,
			"height":el.offsetHeight,
		};	
		if (elinfo.top + elinfo.height < window.pageYOffset || elinfo.top > window.pageYOffset + window.innerHeight) {
			return false;
		} else {
			return true;
		}	
	}

	// element animation
	function getTranslate(el) {
		var translate = {};
		if (!window.getComputedStyle) return;
		var style = getComputedStyle(el);
		var transform = style.transform || style.webkitTransform || style.mozTransform;
		var mat = transform.match(/^matrix3d\((.+)\)$/);
	
		if (mat) {
		  translate.x = mat ? parseFloat(mat[1].split(', ')[12]) : 0;
		  translate.y = mat ? parseFloat(mat[1].split(', ')[13]) : 0;
		} else {
		  mat = transform.match(/^matrix\((.+)\)$/);
		  translate.x = mat ? parseFloat(mat[1].split(', ')[4]) : 0;
		  translate.y = mat ? parseFloat(mat[1].split(', ')[5]) : 0;
		}
	
		return translate;
	}
	function transform(element, x, direction) {		
        let transform,lerpX;
		let start = getTranslate(element);		
		if (direction === 'left') {
			lerpX = start.x - x;  		 
		} else {
			lerpX = start.x + x;
		}
		transform = `matrix3d(1,0,0.00,0,0.00,1,0.00,0,0,0,1,0,${lerpX},0,0,1)`;	

        element.style.webkitTransform = transform;
        element.style.msTransform = transform;
        element.style.transform = transform;
    }

	// accordion
	function initAcc(elem, row, head, option) {
		const acc = document.querySelectorAll(elem);
		if (acc) {
			acc.forEach(item => {
				item.addEventListener('click', function (e) {
					const accRow = e.target.closest(row);

					if (!accRow) {
						return;
					} else {
						if (!accRow.classList.contains('open')) {
							if (option == true) {
								item.querySelectorAll(row).forEach(row => {
									row.classList.remove('open');
								});
							}
							accRow.classList.add('open');
						} else {
							accRow.classList.remove('open');
						}
					}
				});
			});
		}
	}

	initAcc('.js-acc', '.js-acc__row', '.js-acc__head', true);

	// js-article-body
	const articleOL = document.querySelectorAll('.js-article-body ol');
	if (articleOL) {

		articleOL.forEach(ol => {
			const li = ol.querySelectorAll('li');
			li.forEach(li => {
				if (li.value) {
					li.classList.add('with-value');
				}
			});
		});

		articleOL.forEach(ol => {
			if (ol.getAttribute('start')) {
				ol.style.counterReset = `li ${ol.getAttribute('start') - 1}`;
			}
		});

	}

	//aos animations init
	AOS.init({
		disable: (
			/bot|crawler|spider|crawling/i.test(navigator.userAgent)
			|| window.matchMedia("(prefers-reduced-motion: reduce)").matches
		),
	})


});
