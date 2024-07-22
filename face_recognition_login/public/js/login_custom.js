frappe.ui.form.on('User', {
    refresh: function(frm) {
        if (!frm.is_new()) {

            const collectmodal = `
                <div class="modal fade" id="faceCollectModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Collecting Face Models, Please wait...</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </div>
                      <div class="modal-body">
                        <div class="progress">
                          <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;">
                            0%
                          </div>
                        </div>
                        <br>
                        <img src="/assets/face_recognition_login/img/collect_face_models.gif" alt="Loading..." class="img-fluid">
                        <br>
                        <br>
                        <h4><b>Move your head</b> at different angles for better accuracy</h4>
                      </div>
                    </div>
                  </div>
                </div>
            `

            // Append the collectmodal to body
            $('body').append(collectmodal);


            frm.add_custom_button(__('Collect Face Model'), function() {
                // Create a new dialog
                let dialog = new frappe.ui.Dialog({
                    title: __('Instructions'),
                    indicator: 'orange',
                    fields: [
                        {
                            fieldtype: 'HTML',
                            fieldname: 'instructions_html',
                            options: `
                                <div>
                                    <img src="/assets/face_recognition_login/img/instructions.png" alt="Instructions Image" style="width: 100%; height: auto;">
                                    <p>After clicking OK, please do the following:</p>
                                    <ol>
                                        <li><b>Move your head</b> at different angles for better accuracy.</li>
                                        <li><b>Stare at the camera</b> until we collect the required models for your face.</li>
                                        <li>A <b>success message</b> will pop up when finished.</li>
                                    </ol>
                                    <p style="color: red; font-weight: bold;">Important: Make sure you follow all the steps carefully to ensure the accuracy of the model.</p>
                                </div>
                            `
                        },
                        {
                            fieldtype: 'Check',
                            fieldname: 'accept_instructions',
                            label: __('I have read and understood the instructions'),
                            reqd: 1
                        }
                    ],
                    primary_action_label: __('OK'),
                    primary_action(values) {
                        if (values.accept_instructions) {

                            const email = frm.doc.email;
                            if (!email) {
                                alert("Please enter your email first.");
                                return;
                            }

                            $('#faceCollectModal').modal('show');

                            fetch('/api/method/face_recognition_login.api.collect_face_model', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-Frappe-CSRF-Token': frappe.csrf_token
                                },
                                body: JSON.stringify({ user_email: email })
                            }).then(response => {
                                return response.json();
                            }).then(data => {
                                $('#faceCollectModal').modal('hide');
                                if (data.status === "error") {
                                    frappe.throw(data.message)
                                } else {
                                    frappe.msgprint({
                                        title: __('Success'),
                                        indicator: 'green',
                                        message: String(data.message.message)
                                    });
                                }
                            }).catch(error => {
                                $('#faceCollectModal').modal('hide');
                                console.error('Collect Face Model Error:', error);
                                frappe.throw('An unexpected error occurred. Please try again later.')
                            });

                            // Start polling for progress
                            const progressBar = $('#faceCollectModal .progress-bar');
                            const interval = setInterval(() => {
                                fetch(`/api/method/face_recognition_login.face_recognition_login.collect_face_model.get_progress?user_email=${email}`)
                                    .then(response => response.json())
                                    .then(progress => {
                                        const progressValue = parseInt(progress.message);

                                        progressBar.css('width', `${progressValue}%`);
                                        progressBar.attr('aria-valuenow', progressValue);
                                        progressBar.text(`${progressValue}%`);
                                        if (progress >= 100) {
                                            clearInterval(interval);
                                        }
                                    });
                            }, 100); // Poll every second

                            dialog.hide();
                        } else {
                            frappe.msgprint(__('Please accept the instructions to proceed.'));
                        }
                    }
                });

                // Show the dialog
                dialog.show();
            }).addClass('btn-success');
        }
    }
});
