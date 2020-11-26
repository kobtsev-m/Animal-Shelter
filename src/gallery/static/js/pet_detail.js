function configLightbox() {
	$('.card-body-photo').lightGallery({
		thumbnail: true,
		animateThumb: false,
		toogleThumb: false,
		showThumbByDefault: false,
		fullScreen: false,
		share: false,
		flipHorizontal: false,
		flipVertical: false,
		rotateLeft: false,
		autoplayControls: false,
	});
}

document.addEventListener('DOMContentLoaded', _ => {
	configLightbox();
});
