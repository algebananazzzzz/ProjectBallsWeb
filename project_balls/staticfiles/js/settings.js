$('.myKeyPress').keyup(function(event) {
  var keyCode = (event.keyCode ? event.keyCode : event.which);

  event.target.value = keyCode
})

$('#tagInput').tagEditor({
  onChange: (field, editor, tags) => {
    console.log(tags)
    $('#tagHiddenInput').val(encodeURIComponent(JSON.stringify(tags)))
  }
});