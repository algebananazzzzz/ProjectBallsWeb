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
