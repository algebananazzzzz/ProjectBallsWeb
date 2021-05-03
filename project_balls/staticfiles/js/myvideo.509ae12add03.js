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

function remove_new() {
  document.getElementById("new_form").remove();
}


function remove(element) {
  element.parentNode.remove()
}

function remove_time(element) {
  var index = element.parentNode.parentNode.rowIndex
  var start_times = JSON.parse(decodeURIComponent(document.getElementById("hidden_start_time").value))
  var end_times = JSON.parse(decodeURIComponent(document.getElementById("hidden_end_time").value))
  var speeds = JSON.parse(decodeURIComponent(document.getElementById("hidden_speed").value))

  start_times = start_times.filter(function(item) {
    return item !== start_times[start_times.length - index]
  })
  end_times = end_times.filter(function(item) {
    return item !== end_times[end_times.length - index]
  })
  speeds = speeds.filter(function(item) {
    return item !== speeds[speeds.length - index]
  })

  document.getElementById("hidden_end_time").value = encodeURIComponent(JSON.stringify(end_times))
  document.getElementById("hidden_start_time").value = encodeURIComponent(JSON.stringify(start_times))
  document.getElementById("hidden_speed").value = encodeURIComponent(JSON.stringify(speeds))

  element.parentNode.parentNode.remove()
}

function validateForm(name, start_time, end_time, speed) {
  if (name == "") {
    return true;
  }
  if (start_time == "") {
    return true;
  }
  if (end_time == "") {
    return true;
  }
  if (speed == "") {
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
  var form_start_time = document.getElementById("hidden_start_time").value
  var form_end_time = document.getElementById("hidden_end_time").value
  var form_speed = document.getElementById("hidden_speed").value

  if (validateForm(form_name, form_start_time, form_end_time, form_speed)) {
    return
  }


  var data = {
    "name": form_name,
    "tags": '[' + form_new_tags + ']',
    "start_time": form_start_time,
    "end_time": form_end_time,
    "speed": form_speed
  }
  console.log(data)
  var hidden_input = document.getElementById("hidden_input")


  input_data = JSON.parse(decodeURIComponent(hidden_input.value))
  input_data.push(data)

  hidden_input.value = encodeURIComponent(JSON.stringify(input_data))

  var inner_html = '<div class="collapsible-header"><i class="material-icons" onclick="remove(this)">remove</i>' + form_name + '</div><div class="collapsible-body"><p>Name: ' + form_name + '</p><p>Tags: ' + form_new_tags + '</p><p>Snippet count: ' + JSON.parse(decodeURIComponent(form_end_time)).length + '</p></div>'




  li = document.createElement('li');
  li.innerHTML = inner_html.trim()
  li.setAttribute("class", "active")
  li.setAttribute("id", "new_form")
  list.appendChild(li);

  document.getElementById("name").value = ""
  document.getElementById("new_tags").value = ""
  document.getElementById("hidden_start_time").value = "%5B%5D"
  document.getElementById("hidden_end_time").value = "%5B%5D"
  document.getElementById("hidden_speed").value = "%5B%5D"

  $("#table tbody tr:not(:last)").remove()
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
      var start_times = JSON.parse(decodeURIComponent(document.getElementById("hidden_start_time").value))
      var end_times = JSON.parse(decodeURIComponent(document.getElementById("hidden_end_time").value))
      var speeds = JSON.parse(decodeURIComponent(document.getElementById("hidden_speed").value))
      var speed = parseFloat(document.getElementById("speed").value)

      start_times.push(parseFloat(start_time))
      var end_time = player.currentTime().toFixed(2)
      end_times.push(parseFloat(end_time))
      speeds.push(speed)

      $("#table tbody").prepend("<tr><td>" + start_time + "</td><td>" + end_time + "</td><td>" + speed + '</td><td><i class="material-icons" onclick="remove_time(this)">remove</i></td></tr>');

      document.getElementById("hidden_end_time").value = encodeURIComponent(JSON.stringify(end_times))
      document.getElementById("hidden_start_time").value = encodeURIComponent(JSON.stringify(start_times))
      document.getElementById("hidden_speed").value = encodeURIComponent(JSON.stringify(speeds))

      start_input.value = ""
      end_input.value = ""
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
