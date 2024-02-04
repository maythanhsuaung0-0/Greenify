document.addEventListener('DOMContentLoaded', function () {
    const passBtn = document.querySelector('#passBtn');

    if (passBtn) {
        passBtn.addEventListener('click', () => {
            const passwordInput = document.querySelector('#password-input');
            const passwordIcon = document.querySelector('#passBtn i');

            togglePasswordVisibility(passwordInput, passwordIcon);
        });
    } else {
        console.error('passBtn not found in the document.');
    }

    const passBtn2 = document.querySelector('#passBtn2');

    if (passBtn2) {
        passBtn2.addEventListener('click', () => {
            const confirmPasswordInput = document.querySelector('#confirm_password-input');
            const confirmPasswordIcon = document.querySelector('#passBtn2 i');

            togglePasswordVisibility(confirmPasswordInput, confirmPasswordIcon);
        });
    } else {
        console.error('passBtn2 not found in the document.');
    }

    function togglePasswordVisibility(passwordInput, passwordIcon) {
        if (passwordInput && passwordIcon) {
            passwordInput.type = (passwordInput.type === 'password') ? 'text' : 'password';

            if (passwordInput.type === 'text') {
                passwordIcon.classList.remove('fa-eye');
                passwordIcon.classList.add('fa-eye-slash');
            } else {
                passwordIcon.classList.remove('fa-eye-slash');
                passwordIcon.classList.add('fa-eye');
            }
        } else {
            console.error('One or both of the elements not found.');
        }
    }
});
