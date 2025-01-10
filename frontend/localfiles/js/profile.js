document.addEventListener('DOMContentLoaded', function() {
    var totalHours = parseFloat('{{ total_hours|floatformat:2 }}');
    var hoursCount = parseFloat('{{ hours_count|floatformat:2 }}');

    var percentage = (totalHours / hoursCount) * 100;

    var progressBar = document.getElementById('progress-bar');
    var progressText = document.getElementById('progress-text');

    progressBar.style.width = percentage + '%';
    progressText.textContent = totalHours.toFixed(2) + ' hours';
});