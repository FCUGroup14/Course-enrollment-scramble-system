document.getElementById('clearButton').addEventListener('click', function() {

    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => input.value = '');

    const form = this.closest('form');
    form.submit();
});