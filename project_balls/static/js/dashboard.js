$('.canvas-basic').each(function() {
  new Granim({
    element: this,
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
});

function tag_str_to_data(str) {
  var data = {}

  str.forEach((item, index) => {
    data[item] = null
  });
  return data
}

function tag_data_to_str(data) {
  var str = []
  data.forEach((item, index) => {
    str.push(item['tag'])
  });
  return str
}

var query = $('#query')[0]

var autocomplete_data = tag_str_to_data(tag_autocomplete_data)

$('.chips').chips();
$('#query-chips').chips({
  placeholder: 'Enter query tags',
  secondaryPlaceholder: '+Query',
  autocompleteOptions: {
    data: autocomplete_data,
    limit: Infinity,
    minLength: 1
  },
  onChipAdd: (event, chip) => {
    var $this = event[0].M_Chips;
    $this.chipsData.forEach(function(event, index) {
      if (!(event.tag in autocomplete_data))
        $this.deleteChip(index);
    });
    query.value = tag_data_to_str($this.chipsData)

  },

  onChipDelete: (event, chip) => {
    var $this = event[0].M_Chips;
    query.value = tag_data_to_str($this.chipsData)
    // console.log(event[0].M_Chips.chipsData)
  }
});