const uploadForm = document.getElementById('form');
var bar;
var percentd;

const csrf = document.getElementsByName('csrfmiddlewaretoken')
$(document).ready(function() {

  $("#form").submit(function(event) {
    event.preventDefault();
    document.querySelectorAll('style,link[rel="stylesheet"]').forEach(item => item.remove())
    document.getElementsByTagName("head")[0].innerHTML = '<link rel="stylesheet" type="text/css" href="../static/css/loading.css">'
    document.body.innerHTML = '<div id="container">\
    <div class="divider" aria-hidden="true"></div>\
    <p class="loading-text" aria-label="Loading">\
      <span class="letter" aria-hidden="true">L</span>\
      <span class="letter" aria-hidden="true">o</span>\
      <span class="letter" aria-hidden="true">a</span>\
      <span class="letter" aria-hidden="true">d</span>\
      <span class="letter" aria-hidden="true">i</span>\
      <span class="letter" aria-hidden="true">n</span>\
      <span class="letter" aria-hidden="true">g</span>\
    </p>\
    <p>Downloading your video to the server... <b id="progress"></b>\
    </p>\
    <div class="progress">\
      <div class="determinate" id="bar" style="width: 0%"></div>\
    </div>\
  </div>';

    bar = document.getElementById('bar');
    percentd = document.getElementById('progress');

    var data = new FormData(this)
    var action = $(this).attr('action')
    var type = $(this).attr('method')

    $.ajax({
      type: 'POST',
      url: uploadForm.action,
      enctype: 'multipart/form-data',
      data: data,
      beforeSend: function() {

      },
      xhr: function() {
        const xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener('progress', e => {
          if (e.lengthComputable) {
            var percent = e.loaded / e.total * 100
            percent = percent.toFixed(1).toString() + '%'
            bar.style.width = percent
            console.log(percentd)
            percentd.innerHTML = percent
          }

        })
        return xhr
      },
      error: function(error){
        console.log(error)
      },
      success: function() {
        location.replace(document.referrer);
      },
      cache: false,
      contentType: false,
      processData: false,
    })
  })
  $('.require-count').characterCounter();

  $('.modal').modal();
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
