$(document).ready(function() {
    const formLogin = $('.login-content .form-login .page-card-body .social-logins');
    if (formLogin.length) {

        // Create the button container with the face recognition button
        const buttonContainer = `
            <p class="text-muted login-divider">{{ _("or") }}</p>
            <div class="login-button-wrapper" style="margin-top: 15px; margin-bottom: 15px;">
                <button id="start-face-recognition" class="btn btn-block btn-default btn-sm btn-login-option">Login with Face Recognition</button>
            </div>
        `;

        const verifymodal = `
            <div class="modal fade" id="faceRecognitionModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Face Recognition</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body">
                    <img src="/assets/face_recognition_login/img/face_recognition_verify.gif" alt="Loading..." class="img-fluid">
                    <p>Please stare at the camera.</p>
                  </div>
                </div>
              </div>
            </div>
        `

        // Append the text divider and container div to the form-login div
        $('body').append(verifymodal);

        formLogin.append(buttonContainer);


        $('#start-face-recognition').on('click', function(event) {
            event.preventDefault();
            $('#faceRecognitionModal').modal('show');

            fetch('/api/method/face_recognition_login.api.verify_face', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_email: 'omar' })
            })
            .then(response => response.json())
            .then(data => {
                const result = data.message.message;
                if (result.status === "success" && result.message === "Face verified") {
                    window.location.href = '/desk';
                    console.log('Successful Login Redirect');
                    console.log('Welcome: ', result.username);
                } else {
                    $('#faceRecognitionModal').modal('hide');
                    frappe.msgprint('Face Verification Error:', result.message)
                    console.log('Face Verification Error:', result.message);
                }
            })
            .catch(error => {
                $('#faceRecognitionModal').modal('hide');
                frappe.msgprint('Face Recognition Login Error:', error)
                console.error('Face Recognition Login Error:', error);
            });
        });
    }
});
