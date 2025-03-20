let nameField = $('#name');
let contactField = $('#contact');
let emailField = $('#email');
let passwordField = $('#password');
let imageField = $('#image');
let addressField = $('#address');
let user_type = $('#user_type');

$(document).ready(function () {
    //login
    $('#login_form').submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        UserLogin(formData);

    });

    // Registration
    $('#registrationForm').submit(function (event) {
        event.preventDefault();
        if (validateRegister()) {
            var formData = new FormData(this);
            UserRegistration(formData);
        }
    });

});

const UserLogin = (formData) => {
    let formObj = Object.fromEntries(formData);
    PostRequest(loginApiUrl, formObj,
        (response) => {
            if (response.status) {
                showSuccess(response.message);
                setTimeout(() => {
                    window.location.href = homeUrl;
                }, 2000);
            } else {
                showError(response.message);
            }
        },
    );
}

const UserRegistration = (formData) => {
    // let formObj = Object.fromEntries(formData);
    PostRequest(registerApiUrl, formData,
        (response) => {
            console.log(response);
            if (response.status) {
                showSuccess(response.message);
                setTimeout(() => {
                    window.location.href = `/login`;
                }, 2000);
            } else {
                showError(response.message);
            }
        }, true
    );
}



const validateRegister = () => {
    const namePattern = /^[a-zA-Z]+(?:\s[a-zA-Z]+)*$/;
    const contactPattern = /^\d{10}$/;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (nameField.val() === '') {
        showError('Name Field is required');
        return false;
    }
    if (!namePattern.test(nameField.val())) {
        showError('Please enter valid name');
        return false;
    }
    if (contactField.val() === '') {
        showError('Phone Number is required');
        return false;
    }
    if (!contactPattern.test(contactField.val())) {
        showError('Please enter a valid 10-digit contact number.');
        return false;
    }
    if (emailField.val() === '') {
        showError('Email ID is required');
        return false;
    }
    if (!emailPattern.test(emailField.val())) {
        showError('Please enter a valid email address.');
        return false;
    }
    if (addressField.val() === '') {
        showError('Address is required');
        return false;
    }
    if (passwordField.val() === '') {
        showError('password is required');
        return false;
    }
    return true;
}


