document.addEventListener('DOMContentLoaded', function() {
    const timerElement = document.getElementById('timer');
    const redirectBtn = document.getElementById('redirect-btn');

    if (timerElement) {
        let timeLeft = parseInt(timerElement.textContent, 10);

        const countdown = setInterval(() => {
            timeLeft--;
            timerElement.textContent = timeLeft;

            if (timeLeft <= 0) {
                clearInterval(countdown);
                redirectBtn.disabled = false;
                redirectBtn.click(); // Auto-redirect when time is up
            }
        }, 1000);
    }
});