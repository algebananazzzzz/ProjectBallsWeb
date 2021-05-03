$("#sidebarToggle").on("click", function(e) {
  e.preventDefault();
  $("body").toggleClass("sb-sidenav-toggled");
});

var player = videojs('video');

var myTable = $('#dataTable').DataTable({
  paging: false,
  ordering: false,
  searching: false,
  info: false,
  "columnDefs": [{
    "targets": [1],
    "visible": false,
  }, ]
});

var autocomplete_data = ['dasdsad', 'adasdsdsd']
$('#tagInput').tagEditor({
  placeholder: "Add tags...",
  autocomplete: {
    delay: 0, // show suggestions immediately
    position: {
      collision: 'flip'
    }, // automatic menu position up/down
    source: ['dasdsad', 'adasdsdsd']
  },
  beforeTagSave: (field, editor, tags, tag, val) => {
    if (!autocomplete_data.includes(val)) {
      console.log('dasdasd')
      return false
    }
  },

});

$('#tag_search').tagEditor({
  placeholder: "Search for tag..."
});

function remove_row(element) {
  element.parentNode.parentNode.remove()
}


function get_table_data() {
  var tableData = myTable.data().toArray()
  var heads = ['Name', 'Tags', 'Start', 'End', 'Speed']
  var data = [];

  tableData.forEach((item, i) => {
    cur = {};

    item.forEach((v, x) => {
      if (x !== 5) {
        cur[heads[x]] = v
      }
    });
    data.push(cur);
  });
  return data
}


$('#video').keydown(function(event) {
  event.preventDefault();
  var keynum = (event.keyCode ? event.keyCode : event.which);
  var time = player.currentTime().toFixed(2)

  if (window.event) { // IE
    keynum = event.keyCode;
  } else if (event.which) { // Netscape/Firefox/Opera
    keynum = event.which;
  }

  if (keynum == 83) {
    $('#starttimeInput').val(time)
  } else if (keynum == 32) {
    start_time = $('#starttimeInput').val()
    if (start_time.length !== 0) {
      if (start_time < time) {
        name = $('#nameInput').val()
        if (name.length !== 0) {
          myTable.row.add([name, $('#tagInput').tagEditor('getTags')[0].tags, start_time, time, $('#speedInput').val(), '<i class="fas fa-minus" onclick="remove_row(this)"></i>']).draw();
          $('#starttimeInput').val('')
          $('#addsnippetWarning').remove();
          $('#finalsnippetData').val(encodeURIComponent(JSON.stringify(get_table_data())))
        } else {
          if ($('#addsnippetWarning').length) {
            $('#addsnippetWarning').html('Please input a name for the snippet!')
          } else {
            $('#addsnippetCard').prepend('<div id="addsnippetWarning" class="alert alert-danger" role="alert">Please input a name for the snippet!</div>')
          }
        }
      } else {
        if ($('#addsnippetWarning').length) {
          $('#addsnippetWarning').html('Snippet end time should be after its start time!')
        } else {
          $('#addsnippetCard').prepend('<div id="addsnippetWarning" class="alert alert-danger" role="alert">Snippet end time should be after its start time!</div>')
        }
      }
    }
  }
})