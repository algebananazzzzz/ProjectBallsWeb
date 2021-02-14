new Granim({
  element: '#canvas-background',
  direction: 'left-right',
  states: {
    "default-state": {
      gradients: [
        ['#b71c1c', '#880e4f'],
        ['#4a148c', '#311b92'],
        ['#1a237e', '#0d47a1'],
        ['#01579b', '#006064'],
        ['#004d40', '#1b5e20'],
        ['#33691e', '#827717'],
        ['#f57f17', '#ff6f00'],
        ['#e65100', '#bf360c'],
      ],
      transitionSpeed: 5000
    }
  }
});


var comfirm_password = document.getElementById("password2")
var password = document.getElementById("password1")

comfirm_password.addEventListener("keyup", match);


function match() {
  var val = comfirm_password.value;
  if (!val || !val.length) {
    return;
  }

  var match_val = password.value;

  if (match_val == val) {
    comfirm_password.classList.remove("invalid");
    comfirm_password.classList.add("valid");
  } else {
    comfirm_password.classList.remove("valid");
    comfirm_password.classList.add("invalid");
  }

}