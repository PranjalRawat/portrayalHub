// Countdown timer function
function countdown() {
    let seconds = 5; // Number of seconds to countdown
    let countdownElement = document.getElementById("countdown");

    // Update countdown text every second
    let countdownInterval = setInterval(function() {
        seconds--;
        countdownElement.textContent = seconds;

        // Redirect to home page when countdown reaches 0
        if (seconds <= 0) {
            clearInterval(countdownInterval); // Stop the countdown
            window.location.href = "/"; // Redirect to the home page
        }
    }, 1000); // Update countdown every 1 second (1000 milliseconds)
}

// Start the countdown timer when the page loads
window.onload = function() {
    countdown();
};
