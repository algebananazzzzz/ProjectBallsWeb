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


var player = videojs('video')

function myKeyPress(e) {
  var keynum;

  if (window.event) { // IE
    keynum = e.keyCode;
  } else if (e.which) { // Netscape/Firefox/Opera
    keynum = e.which;
  }
  alert(keynum)
}


var skipBehindButton = player.controlBar.addChild("button");
var skipBehindButtonDom = skipBehindButton.el();
skipBehindButtonDom.innerHTML = "30<<";
skipBehindButton.addClass("buttonClass");

skipBehindButtonDom.onclick = function() {
  skipS3MV(-30);
}

var skipAheadButton = player.controlBar.addChild("button");
var skipAheadButtonDom = skipAheadButton.el();
skipAheadButtonDom.innerHTML = ">>30";
skipAheadButton.addClass("buttonClass");

skipAheadButtonDom.onclick = function() {
  skipS3MV(30);
}

function skipS3MV(skipBy) {
  player.currentTime(player.currentTime() + skipBy);
}

// video.currentTime(video.currentTime() + 10);