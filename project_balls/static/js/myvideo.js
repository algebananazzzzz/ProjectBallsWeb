document.getElementById('video').addEventListener('keydown', function(e) {
  if (e.keyCode == 32) {
    e.preventDefault();
  }
});

$(document).ready(function() {
  $('.require-count').characterCounter();
});

$(document).ready(function() {
  $('.collapsible').collapsible();
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

function remove_new() {
  document.getElementById("new_form").remove();
}


function remove(element) {
  element.parentNode.remove()
}

function validateForm(name, start_time, end_time) {
  if (name == "") {
    return true;
  }
  if (start_time == "") {
    return true;
  }
  if (end_time == "") {
    return true;
  }
  return false
}


function comfirm_snippet(element) {
  var list = document.getElementById("list");

  var parent_li = element.parentNode.parentNode

  var index = Array.from(list.children).indexOf(parent_li);

  var form_name = document.getElementById("name").value
  var form_new_tags = document.getElementById("new_tags").value
  var form_start_time = document.getElementById("start_time").value
  var form_end_time = document.getElementById("end_time").value


  if (validateForm(form_name, form_start_time, form_end_time)) {
    return
  }


  var data = {
    "name": form_name,
    "tags": '[' + form_new_tags + ']',
    "start_time": form_start_time,
    "end_time": form_end_time
  }

  var hidden_input = document.getElementById("hidden_input")


  input_data = JSON.parse(decodeURIComponent(hidden_input.value))
  input_data.push(data)

  hidden_input.value = encodeURIComponent(JSON.stringify(input_data))

  var inner_html = '<div class="collapsible-header"><i class="material-icons" onclick="remove(this)">remove</i>' + form_name + '</div><div class="collapsible-body"><p>Name: ' + form_name + '</p><p>Tags: ' + form_new_tags + '</p><p>Start time: ' + form_start_time + '</p><p>End time: ' + form_end_time + '</p></div>'




  li = document.createElement('li');
  li.innerHTML = inner_html.trim()
  li.setAttribute("class", "active")
  li.setAttribute("id", "new_form")
  list.appendChild(li);

  document.getElementById("name").value = ""
  document.getElementById("new_tags").value = ""
  document.getElementById("start_time").value = ""
  document.getElementById("end_time").value = ""
}


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

var tag_input = $('#new_tags')[0]

var autocomplete_data = tag_str_to_data(tag_autocomplete_data)

$('#new_tag_chips').chips({
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
    tag_input.value = tag_data_to_str($this.chipsData)

  },

  onChipDelete: (event, chip) => {
    var $this = event[0].M_Chips;
    tag_input.value = tag_data_to_str($this.chipsData)
    // console.log(event[0].M_Chips.chipsData)
  }
});


var start_time;

var start_input = $('#start_time')[0]
var end_input = $('#end_time')[0]

$('#video').keyup(function(event) {
  var keynum = (event.keyCode ? event.keyCode : event.which);

  if (window.event) { // IE
    keynum = event.keyCode;
  } else if (event.which) { // Netscape/Firefox/Opera
    keynum = event.which;
  }

  if (keynum == start_recording_key) {
    start_time = player.currentTime().toFixed(2)
    start_input.value = start_time
    end_input.value = ""

  } else if (keynum == end_recording_key) {

    if (start_time) {
      end_input.value = player.currentTime().toFixed(2)
    } else {
      start_input.value = ""
      end_input.value = ""
    }
  } else if (keynum == cancel_recording_key) {
    start_input.value = ""
    end_input.value = ""
    start_time = false

  }
});