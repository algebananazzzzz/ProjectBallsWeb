$(document).ready(function() {
  $('.materialize-textarea').characterCounter();
});
$('.canvas-basic').each(function() {
  new Granim({
    element: this,
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
});

function myKeyPress(e) {
  var keynum;

  if(window.event) { // IE
    keynum = e.keyCode;
  } else if(e.which) { // Netscape/Firefox/Opera
    keynum = e.which;
  }
  var key = String.fromCharCode(keynum)
  e.target.value = keynum
}
var tag_chips = $('#tag-chips')

$('.chips').chips();
tag_chips.chips({
  placeholder: 'Enter a tag',
  secondaryPlaceholder: '+Tag',
  data: [{
    tag: 'Apple',
  }, {
    tag: 'Microsoft',
  }, {
    tag: 'Google',
  }],
  onChipAdd: (event, chip) => {
    console.log(event[0].M_Chips.chipsData)
  },
  onChipDelete: (event, chip) => {
    console.log(event[0].M_Chips.chipsData)
  }
});

var tag_chips_0 = $('#tag-chips')[0]

$('#form').submit(function() { //listen for submit event
  $('<input />').attr('type', 'hidden')
    .attr('tags', tag_chips_0.M_Chips.chipsData)
    .attr('fwefe', 'fwefew')
    .appendTo('#form');
  return true;
});
