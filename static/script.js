function getRandomValue(min, max) {
    // Generate a random decimal between 0 and 1
    var randomDecimal = Math.random();
  
    // Scale and shift the random decimal to fit within the desired range
    var randomValue = min + randomDecimal * (max - min);
  
    // Round the result to an integer if needed
    // randomValue = Math.round(randomValue);
  
    return randomValue;
  }

function aiButtonClick() {
    aiButton = document.getElementById('ai_button');
    aiLoader = document.getElementById('ailoader');
    var prediction = document.createElement('h2');
    prediction.textContent = "Some prediction";
    nextbutton = document.getElementById('nextbutton');

    if (aiButton) {
        aiButton.style.display = "none";
        ailoader.style.display = "block";
        setTimeout(function(){
            ailoader.style.display = "none";
            document.getElementById('prediction').appendChild(prediction);
            nextbutton.classList.remove('d-none');
        }, getRandomValue(3500, 4500))
    }
}

document.getElementById("showInfo").addEventListener("click", function() {
    document.getElementById("overlay").style.display = "flex";
});

document.getElementById("closeButton").addEventListener("click", function() {
    document.getElementById("overlay").style.display = "none";
});