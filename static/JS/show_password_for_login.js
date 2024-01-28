document.addEventListener('DOMContentLoaded', function () {
    const passBtn = document.querySelector('#passBtn');

    if (passBtn) {
        passBtn.addEventListener('click', () => {
            const passwordInput = document.querySelector('#password input');
            const passwordIcon = document.querySelector('#password i');

            passwordInput.getAttribute('type') === 'password' ? passwordInput.setAttribute('type', 'text') : passwordInput.setAttribute('type', 'password');

            if (passwordInput.getAttribute('type') === 'text') {
                passwordIcon.className = 'fa fa-eye-slash fa-fw';
            } else {
                passwordIcon.className = 'fa fa-eye fa-fw';
            }
        });
    } else {
        console.error('passBtn not found in the document.');
    }
});