$(document).ready(function() {
    const formLogin = $('.login-content .form-login .page-card-body .social-logins');
    if (formLogin.length) {

        // Create the button container with the face recognition button
        const buttonContainer = `
        	<p class="text-muted login-divider">{{ _("or") }}</p>
            <div class="login-button-wrapper" style="margin-top: 15px; margin-bottom: 15px;">
                <button id="face-recognition-login" class="btn btn-block btn-default btn-sm btn-login-option">Login with Face Recognition</button>
            </div>
        `;

        // Append the text divider and container div to the form-login div
        formLogin.append(buttonContainer);

        // Create a new section for face recognition login
        const faceRecognitionSection = `
            <section id="face-recognition-login-section" class="for-face-recognition-login" style="display: none;">
            	{{ logo_section(_('Login with Face Recognition')) }}
                <div class="login-content page-card">
                    <form class="form-signin form-face-recognition" role="form">
                        <div class="page-card-body">
                            <div class="face-recognition-field">
                                <button id="start-face-recognition" class="btn btn-sm btn-primary btn-block">Start Face Recognition</button>
                            </div>
                        </div>
                        <div class="page-card-actions">
                            <p class="text-center">
                                <a href="#login" class="back-to-login">Back to Login</a>
                            </p>
                        </div>
                    </form>
                </div>
            </section>
        `;



        // Append the new section to the existing content
        $('.page_content .for-login-with-email-link').after(faceRecognitionSection);

        // Handle button click to show the face recognition section
        $('#face-recognition-login').on('click', function() {
            $('.for-login').hide();
            $('.for-face-recognition-login').show();

            $('html, body').animate({
                scrollTop: $('#face-recognition-login-section').offset().top
            }, 1000);

            window.location.hash = 'face-recognition-login-section';
        });

        // Handle back to login link click
        $(document).on('click', '.back-to-login', function() {
            $('.for-face-recognition-login').hide();
            $('.for-login').show();

            $('html, body').animate({
                scrollTop: $('.for-login').offset().top
            }, 1000);

            window.location.hash = 'login';
        });

        $('#start-face-recognition').on('click', function(event) {
            event.preventDefault();
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
                    console.log('Face Verification Error:', result.message);
                }
            })
            .catch(error => {
                console.error('Face Recognition Login Error:', error);
            });
        });
    }
});
