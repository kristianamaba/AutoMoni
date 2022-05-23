function sAlert(message, loca) {
	showToast(message, 'success');
	setTimeout(function () {
		if (loca == "reload-page")
			history.go(0);
		else if (!isBlank(loca))
			window.location.href = loca;
	}, 2000);
	// swal({
	//     icon: "success",
	//     title: "Success!",
	//     text: message,
	//     showConfirmButton: false,
	//     timer: 3000
	//     }).then(function() {

	// 	if(loca == "reload-page")
	// 		history.go(0);
	//     else if(!isBlank(loca))
	//         window.location.href=loca;
	// });
}

function fAlert(message) {
	// swal({
	// 	icon: 'error',
	// 	title: 'Oops...',
	// 	text: message,
	// 	showConfirmButton: false,
	// 	timer: 3000
	// });
	showToast(message, 'error');
}

function isBlank(str) {
	return (!str || /^\s*$/.test(str));
}

function checkFormC(formID) {
	var returnTemp = true;
	$("form#" + formID + " :input").each(function () {
		var input = $(this); // This is the jquery object of the input, do what you will
		if (!input.prop('required')) {
			input.css('border-color', '');

			if (!isEmptyC(input.val())) {
				if (!validateTextC(input.val(), input.prop('type'))) {
					input.css('border-color', 'red');
					showInputMessageC(input, "Invalid Input", "Invalid " + input.prop('type') + " input : " + input.val());
					fAlert("Invalid " + input.prop('type') + " input : " + input.val());
					returnTemp = false;
				}
				else
					clearInputMessageC(input);
			}
			else
				clearInputMessageC(input);

		} else {
			if (isEmptyC(input.val())) {
				input.css('border-color', 'red');
				fAlert("Empty " + input.prop('type'));
				showInputMessageC(input, "Required Input Field", "Empty " + input.prop('type'));
				returnTemp = false;
			}
			else {
				if (validateTextC(input.val(), input.prop('type'))) {
					input.css('border-color', '');
					clearInputMessageC(input);
				}
				else {
					input.css('border-color', 'red');
					fAlert("Invalid " + input.prop('type') + " input : " + input.val());
					showInputMessageC(input, "Invalid Input", "Invalid " + input.prop('type') + " input : " + input.val());
					returnTemp = false;
				}
			}
		}
	});
	return returnTemp;
}

function clearInputMessageC(element) {
	element.popover('disable');
}

function showInputMessageC(element, title, message) {

	element.attr("title", title);
	element.attr("data-original-title", title);
	element.attr("data-toggle", "popover");
	element.attr("data-placement", "left");
	element.attr("data-trigger", "hover");
	element.attr("data-content", message);
	$('[data-toggle="popover"]').popover();
	element.popover('enable');
}

function checkAttributeC(element, attribute) {
	if (element.hasAttr(attribute)) {
		return true;
	} else {
		return false;
	}
}

function validateTextC(txt, type) {
	if (type == "text")
		return isValidTextC(txt);
	if (type == "email")
		return isEmailC(txt);
	else if (type == "number")
		return isNumberC(txt);
	else
		return true;
}

function isValidTextC(string) {
	var checker = true;
	var arrayInvalid = ["\\0", "\\'", "\\b", "\\n", "\\r", "\\t", "\\z", "\\", "\%", "\\_", ";"];
	for (var i = 0; i < string.length; i++) {
		if (arrayInvalid.includes(string[i])) {
			checker = false;
		}
	}
	return checker;
}

function isNumberC(number) {
	return number.match(/^\d+$/);
}

function isEmailC(email) {
	var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return regex.test(email);
}

function isEmptyC(txt) {
	try {
		if (!txt.trim())
			return true;
		else
			return false;
	}
	catch (e) {
		return true;
	}

}





