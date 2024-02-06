document.addEventListener('DOMContentLoaded', function () {
    const passBtn = document.querySelector('#passBtn');

    if (passBtn) {
        passBtn.addEventListener('click', () => {
            const passwordInput = document.querySelector('#password input');
            const passwordIcon = document.querySelector('#password i');

            togglePasswordVisibility(passwordInput, passwordIcon);
        });
    } else {
        console.error('passBtn not found in the document.');
    }

    const passBtn2 = document.querySelector('#passBtn2');

    if (passBtn2) {
        passBtn2.addEventListener('click', () => {
            const confirmPasswordInput = document.querySelector('#confirm_password input');
            const confirmPasswordIcon = document.querySelector('#confirm_password i');

            togglePasswordVisibility(confirmPasswordInput, confirmPasswordIcon);
        });
    } else {
        console.error('passBtn2 not found in the document.');
    }
});

function togglePasswordVisibility(passwordInput, passwordIcon) {
    if (passwordInput && passwordIcon) {
        passwordInput.getAttribute('type') === 'password' ? passwordInput.setAttribute('type', 'text') : passwordInput.setAttribute('type', 'password');

        if (passwordInput.getAttribute('type') === 'text') {
            passwordIcon.className = 'fa fa-eye-slash fa-fw';
        } else {
            passwordIcon.className = 'fa fa-eye fa-fw';
        }
    } else {
        console.error('One or both of the elements not found.');
    }
}
