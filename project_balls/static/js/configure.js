$(document).ready(function() {
  $('.require-count').characterCounter();
});

$(document).ready(function() {
  $('.modal').modal();
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

$('.myKeyPress').keyup(function(event) {
  var keyCode = (event.keyCode ? event.keyCode : event.which);

  event.target.value = keyCode
})

var tag_chips = $('#tag-chips')
var tag_input = $('#id_primaryTags')[0]

function tag_data_to_str(data) {
  var str = []
  data.forEach((item, index) => {
    str.push(item['tag'])
  });
  return str

}

if (initial_tag_data) {


  function tag_str_to_data(str) {
    var data = []

    str = str.split(',')

    str.forEach((item, index) => {
      data.push({
        'tag': item
      })
    });
    return data
  }
  tag_chips.chips({
    placeholder: 'Enter a tag',
    secondaryPlaceholder: '+Tag',
    data: tag_str_to_data(initial_tag_data),
    onChipAdd: (event, chip) => {
      var $this = event[0].M_Chips;
      $this.chipsData.forEach(function(event, index) {
        if ((event.tag.length > 30))
          $this.deleteChip(index);
      });

      tag_input.value = tag_data_to_str($this.chipsData)
    },
    onChipDelete: (event, chip) => {
      tag_input.value = tag_data_to_str($this.chipsData)
      // console.log(event[0].M_Chips.chipsData)
    }
  });
} else {
  tag_chips.chips({
    placeholder: 'Enter a tag',
    secondaryPlaceholder: '+Tag',
    onChipAdd: (event, chip) => {
      tag_input.value = tag_data_to_str(event[0].M_Chips.chipsData)
    },
    onChipDelete: (event, chip) => {
      tag_input.value = tag_data_to_str(event[0].M_Chips.chipsData)
      // console.log(event[0].M_Chips.chipsData)
    }
  });
}