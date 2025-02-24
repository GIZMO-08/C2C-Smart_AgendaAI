document.getElementById('vocal').addEventListener('click', function() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US'; 
    recognition.interimResults = false; 
    recognition.maxAlternatives = 1; 

    recognition.start(); 

    recognition.onresult = function(event) {
        var transcript = event.results[0][0].transcript;
        console.log('Recognized speech:', transcript);
        
         Command(transcript);
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };
});


function Command(command) {
    
    console.log('Processing command:', command);
   
    if (command.includes("add a task")) {
      
    }
}

