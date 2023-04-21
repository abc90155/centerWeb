    // Set the date and time the countdown ends
    const countdownDate = new Date('2023-03-31T03:50:00').getTime();

    // Update the countdown every second
    const timerInterval = setInterval(() => {
    // Get the current date and time
    const now = new Date().getTime();
    
    // Calculate the remaining time
    const remainingTime = countdownDate - now;
    
    // Calculate the days, hours, minutes, and seconds remaining
    const days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
    const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
    
    // Update the timer display
    document.getElementById('days').innerHTML = `${days}`;
    document.getElementById('hours').innerHTML = `${hours}`;
    document.getElementById('mins').innerHTML = `${minutes}`;
    document.getElementById('secs').innerHTML = `${seconds}`;
    
    // Stop the timer if the countdown has ended
    if (remainingTime < 0) {
    clearInterval(timerInterval);
    document.getElementById('timer-display').innerHTML = 'Countdown ended!';
    }
    }, 1000);