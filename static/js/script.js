document.addEventListener('DOMContentLoaded', function() {
    // Update the code and timer every second
    function updateCodeAndTimer() {
        fetch('/get_code/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('current-code').textContent = data.code;
                document.getElementById('time-left').textContent = `Оставшееся время: ${data.time_left} сек.`;
            });
    }

    // Update immediately and then every second
    updateCodeAndTimer();
    setInterval(updateCodeAndTimer, 1000);
});