new Granim({
  element: '#canvas-background',
  direction: 'left-right',
  states: {
    "default-state": {
      gradients: [
        ['#F45C43', '#EB3349'],
        ['#FF8008', '#FFC837'],
        ['#3CD3AD', '#4CB8C4'],
        ['#24C6DC', '#514A9D'],
        ['#DD2476', '#FF512F'],
        ['#DA22FF', '#9733EE'],
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