// settings.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const toast = document.getElementById('toast');

    if (form && toast) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerText = "Saving...";

            // Show toast message
            toast.classList.add('show');

            setTimeout(() => {
                toast.classList.remove('show');
                submitButton.disabled = false;
                submitButton.innerText = "Save Settings";
                form.submit(); // Submit form after notification
            }, 1500);
        });
    }
});
