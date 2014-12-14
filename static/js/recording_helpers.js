var audio_context;
var recorder;

function __log(a){console.log(a)}

function setup_mp3_recording(){
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);
      window.URL = window.URL || window.webkitURL;
      
      audio_context = new AudioContext;
      __log('Audio context set up.');
      __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
      alert('No web audio support in this browser!');
    }
    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
      __log('No live audio input: ' + e);
    });
    init_mp3_buttons()
}

function init_mp3_buttons(){
    $('.recorder-start').unbind('click').bind('click', function(e){startRecording($(e.target))})
    $('.recorder-stop').unbind('click').bind('click', function(e){stopRecording($(e.target))})
}

function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    __log('Media stream created.' );
	__log("input sample rate " +input.context.sampleRate);
    
    input.connect(audio_context.destination);
    __log('Input connected to audio context destination.');
    
    recorder = new Recorder(input);
    __log('Recorder initialised.');
  }

function startRecording(button) {
  recorder && recorder.record();
  $('div').removeClass('redborder')
  button.addClass('redborder')
  //button.disabled = true;
  //button.nextElementSibling.disabled = false;
  __log('Recording...');
}

function stopRecording(button) {
  recorder && recorder.stop();
  $('div').removeClass('redborder')
  //button.disabled = true;
  //button.previousElementSibling.disabled = false;
  __log('Stopped recording.');
  // create WAV download link using audio data blob
  //just communicate through this global for now.
  note_id=button.attr('note_id')
  createDownloadLink(button);
  
  recorder.clear();
}

function createDownloadLink(div) {
  recorder && recorder.exportWAV(function(blob) {
    var url = URL.createObjectURL(blob);
    var li = document.createElement('li');
    var au = document.createElement('audio');
    var hf = document.createElement('a');
    
    au.controls = true;
    au.src = url;
    hf.href = url;
    hf.download = new Date().toISOString() + '.wav';
    hf.innerHTML = hf.download;
    li.appendChild(au);
    li.appendChild(hf);
    div.append(li);
  });
}