'use strict';

const clickEvent = new Event('click');

function addPhotoFormsetEvents() {
	const formset = document.querySelector('.formset-photos');
	const addBtn = document.querySelector('.formset-photos .row-add');
	const controlPrev = document.querySelector('.formset-prev');
	const controlNext = document.querySelector('.formset-next');

	const formsTotal = document.getElementById('id_petphoto_set-TOTAL_FORMS');
	const formsLimit = document.getElementById('id_petphoto_set-MAX_NUM_FORMS');
	const formsPhoto = document.querySelectorAll('.formset-photos form');

	const maxSize = 3.0;
	const possibleExtensions = ['png', 'jpg', 'jpeg', 'svg', 'tiff'];

	let inputs, deleteBtns, lastInput, lastDeleteBtn;

	const isLimit = _ => {
		return +formsTotal.value >= +formsLimit.value - 1;
	};

	const showError = (target, message) => {
		if (target.nodeName == 'INPUT') {
			target = target.parentNode.parentNode.parentNode;
		}
		target.childNodes[7].style.display = 'block';
		target.childNodes[7].textContent = message;
		disableAddBtn();
	};

	const hideError = target => {
		target = target.parentNode.parentNode.parentNode;
		target.childNodes[7].style.display = 'none';
	};

	const updateLastElements = event => {
		deleteBtns = document.querySelectorAll('.formset-photos .row-delete');
		inputs = document.querySelectorAll('.formset-photos input[type=file]');

		lastDeleteBtn = deleteBtns[deleteBtns.length - 1];
		lastInput = inputs[inputs.length - 1];

		if (lastDeleteBtn && event == 'add') {
			lastDeleteBtn.addEventListener('click', deleteBtnListener);
		}
		if (lastInput && event == 'add') {
			lastInput.addEventListener('change', inputListener);
			$(lastInput.parentNode.parentNode.parentNode).fileinput({
				maxSize: maxSize,
			});
			$(lastInput.parentNode.parentNode.parentNode).on(
				'max_size.bs.fileinput',
				e => {
					showError(e.target, `Max size of photo is ${maxSize}MB`);
				}
			);
		}
	};

	const checkForFileErrors = file => {
		const ext = file.value.substring(file.value.lastIndexOf('.') + 1);
		if (!possibleExtensions.includes(ext.toLowerCase())) {
			$(file.parentNode.parentNode.parentNode).fileinput('clear');
			showError(file, 'Please, upload an image');
			return true;
		}

		const countSameValues = Array.from(inputs).reduce(
			(acc, input) => (input.value == file.value ? acc + 1 : acc),
			0
		);
		if (countSameValues == 2) {
			$(file.parentNode.parentNode.parentNode).fileinput('clear');
			showError(file, 'Please, choose different photos');
			return true;
		}

		return false;
	};

	const inputListener = e => {
		if (e.target.value) {
			if (!checkForFileErrors(e.target)) {
				hideError(e.target);
				if (!isLimit()) {
					enableAddBtn();
				}
			}
		} else {
			if (e.target == lastInput) {
				disableAddBtn();
			} else {
				const inputDeleteBtn = e.path[4].childNodes[3];
				inputDeleteBtn.dispatchEvent(clickEvent);
			}
		}
	};

	const deleteBtnListener = e => {
		const target = e.target.nodeName == 'A' ? e.target : e.path[1];
		if (target == lastDeleteBtn) {
			enableAddBtn();
		} else if (+formsTotal.value == +formsLimit.value - 2) {
			if (lastInput.value) {
				enableAddBtn();
			} else {
				disableAddBtn();
			}
		}
		updateLastElements('delete');
	};

	const disableAddBtn = _ => {
		addBtn.classList.add('disabled');
		addBtn.innerHTML = isLimit()
			? "<span>Can't add more photos " +
			  '<i class="far fa-frown"></i></span>'
			: 'Choose previous photo to add new';
		addBtn.blur();
	};

	const enableAddBtn = _ => {
		addBtn.classList.remove('disabled');
		addBtn.innerHTML = '<i class="fas fa-plus"></i>';
	};

	addBtn.addEventListener('click', _ => {
		disableAddBtn();
		updateLastElements('add');
	});

	controlPrev.addEventListener('click', _ => {
		anime({
			targets: formset,
			scrollLeft: '-=100',
			easing: 'easeInOutQuad',
			duration: 200,
		});
	});

	controlNext.addEventListener('click', _ => {
		anime({
			targets: formset,
			scrollLeft: '+=100',
			easing: 'easeInOutQuad',
			duration: 200,
		});
	});

	// Инициализация формсета
	disableAddBtn();
	updateLastElements('add');

	// Очистка в случае неудачной валидации
	if (formsPhoto.length) {
		formset.appendChild(addBtn);
		formsPhoto.forEach(form => {
			form.remove();
			formsTotal.value = String(+formsTotal.value - 1);
		});
		if (lastDeleteBtn) {
			lastDeleteBtn.style.display = 'none';
		}
	}
}

function addAnimalFormEvents() {
	const descriptionInput = document.querySelector('#id_description');
	const descriptionHint = document.querySelector('#hint_id_description');

	const descriptionTotal = parseInt(descriptionHint.textContent);

	descriptionInput.addEventListener('keyup', _ => {
		const leftSymbols = descriptionTotal - descriptionInput.value.length;
		descriptionHint.textContent = String(leftSymbols) + ' symbols';
	});
}

document.addEventListener('DOMContentLoaded', _ => {
	addAnimalFormEvents();
	addPhotoFormsetEvents();
});
