$(document).ready(function () {

    $('#detectlandslide').submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        showConfirmation("Are you sure you want to detect the land slide?",
            () => {
                DetectLandSlide(formData);
            });
    });

    $('#image').change(function () {
        $('#disease_name').text('');
        $('#details-block').empty();
        $('.info-block').hide()
        displayImage(this);
    });


});


const displayImage = (input) => {
    var previewImage = $('#previewImage')[0];

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}


const DetectLandSlide = (formData) => {
    showProcessingAlert("Please wait....", false);
    PostRequest(detectSLideApiUrl, formData,
        (response) => {
            closeProcessingAlert();
            if (response.status) {
                console.log(response.message);
                showInfo(response.message)
            } else {
                showError(response.message);
            }
        }, true
    );
}
