'use strict';

let supportsPassive = false;
try {
	window.addEventListener(
		'test',
		null,
		Object.defineProperty({}, 'passive', {
			get: _ => {
				supportsPassive = true;
			},
		})
	);
} catch (e) {}

let wheelOpt = supportsPassive ? { passive: false } : false;

function preventDefault(e) {
	e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
	const keys = { 37: 1, 38: 1, 39: 1, 40: 1 };
	if (keys[e.keyCode]) {
		preventDefault(e);
		return false;
	}
}

function disableScroll() {
	window.addEventListener('DOMMouseScroll', preventDefault, false);
	window.addEventListener('mousewheel', preventDefault, wheelOpt);
	window.addEventListener('touchmove', preventDefault, wheelOpt);
	window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

function enableScroll() {
	window.removeEventListener('DOMMouseScroll', preventDefault, false);
	window.removeEventListener('mousewheel', preventDefault, wheelOpt);
	window.removeEventListener('touchmove', preventDefault, wheelOpt);
	window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}

function addSideMenuEvents() {
	const navbarButToggler = document.querySelector('.navbar-toggler');
	const sideMenu = document.querySelector('.sidemenu');
	const sideMenuLinks = document.querySelectorAll('.sidemenu .nav__item');

	const sideMenuEasing = 'easeInOutSine';
	const sideMenuDuration = 500;

	const previewImgs = document.querySelectorAll(`.preview-box div`);
	const tabs = ['Home', 'Animals', 'About'];

	navbarButToggler.addEventListener('click', _ => {
		navbarButToggler.classList.toggle('toggled');
		if (navbarButToggler.classList.contains('toggled')) {
			anime({
				targets: sideMenu,
				translateX: '100vw',
				easing: sideMenuEasing,
				duration: sideMenuDuration,
			});
			disableScroll();
		} else {
			anime({
				targets: sideMenu,
				translateX: '0',
				easing: sideMenuEasing,
				duration: sideMenuDuration,
			});
			enableScroll();
		}
	});

	const showCurrPreviewImg = idx => {
		previewImgs.forEach(img => {
			img.style.display = 'none';
		});
		previewImgs[idx].style.display = 'block';
	};

	sideMenuLinks.forEach((item, idx) => {
		item.addEventListener('mouseenter', _ => {
			showCurrPreviewImg(idx);
			anime({
				targets: previewImgs[idx],
				translateY: [-500, 0],
				duration: 1000,
			});
		});
	});

	showCurrPreviewImg(
		tabs.indexOf(document.querySelector('title').textContent.trim())
	);
}

document.addEventListener('DOMContentLoaded', _ => {
	addSideMenuEvents();
});
