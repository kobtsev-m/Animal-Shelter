function configCarousel() {
	$(".carousel").carousel({
		interval: false,
		keyboard: false,
	});
}

document.addEventListener("DOMContentLoaded", _ => {
	configCarousel();
});
