function animateTitle() {
	anime({
		targets: '.about-title svg path',
		strokeDashoffset: [anime.setDashoffset, 0],
		easing: 'easeInOutSine',
		duration: 2000,
		delay: function (el, i) {
			return i * 200;
		},
		direction: 'alternate',
		loop: false,
	});
}

function animateText() {
	new TypeIt('.about-text', {
		speed: 50,
		startDelay: 3000,
	}).go();
}

document.addEventListener('DOMContentLoaded', _ => {
	animateText();
	animateTitle();
});
