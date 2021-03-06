var lastScrollTop = 0;

$(window).scroll(function() {
  var docViewTop = $(window).scrollTop();
  var docViewBottom = docViewTop + $(window).height();

  function isScrolledIntoView(elem, offset, animation) {

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height() - offset;

    return ((elemBottom <= docViewBottom) && (elemTop + offset >= docViewTop));
  }

  if (docViewTop >= lastScrollTop) {
    var scrollDown = true
  } else {
    var scrollDown = false
  }

  lastScrollTop = docViewTop;

  function opacityControl(element) {
    var elemTop = element.offset().top;
    var elementHeight = element.height();
    if (elemTop > docViewTop) {
      element.css({
        opacity: (elementHeight - elemTop + docViewTop) / elementHeight
      });
    } else {
      element.css({
        opacity: (elementHeight - docViewTop + elemTop) / elementHeight
      });
    }
  };

  function fadeInOutAnim(element, offset, animation) {
    elem = element[0]
    if (isScrolledIntoView(element, offset)) {
      elem.classList.add(animation);
      elem.classList.remove("fade-out")
      element.css({
        opacity: 1
      });
    } else {
      var elementHeight = element.offset().top;
      if (docViewTop < elementHeight) {
        if (scrollDown) {
          element.css({
            opacity: 0
          });
        } else {
          elem.classList.remove(animation);
          elem.classList.add("fade-out")
        }
      } else {
        element.css({
          opacity: function() {
            var elemTop = $(this).offset().top;
            var elementHeight = $(this).height();

            return (elementHeight - docViewTop + elemTop) / elementHeight;
          },
        });
      }
    }
  };

  $('#home-background').css({
    opacity: function() {
      var elementHeight = $(this).height();
      return (elementHeight - docViewTop) / elementHeight;
    },
  });
  var content1 = $('#home-content1');

  var content2 = $('#home-content2');

  var content3 = $('#home-content3');

  opacityControl(content2)


  fadeInOutAnim(content1, 0, "fade-in-anim");
  fadeInOutAnim(content3, 0, "bounce-in")

});


$(document).ready(function() {
  $('.materialboxed').materialbox();
});

$(document).ready(function() {
  $('#card-tab').tabs();
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