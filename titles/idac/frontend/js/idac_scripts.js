$(document).ready(function () {
    $('#exportBtn').click(function () {
        window.location = "/game/idac/export";

        // appendAlert('Successfully exported the profile', 'success');

        // Close the modal on success
        $('#export').modal('hide');
    });
});