document.addEventListener('DOMContentLoaded', function () {
    // Attach a submit event listener to the form
    document.getElementById('routeForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Fetch form data
        const formData = new FormData(event.target);

        // Send a POST request to the server
        fetch('/search_route', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                const toastEl = document.getElementById('routeToast');
                const toastBody = document.getElementById('result-container');
                
                toastBody.innerHTML = data.result;

                if (data.status === 'error') {
                    // Show error toast
                    toastEl.classList.remove('bg-success');
                    toastEl.classList.add('bg-danger');
                } else {
                    // Show success toast
                    toastEl.classList.remove('bg-danger');
                    toastEl.classList.add('bg-success');
                }

                // Show the toast notification
                const toast = new bootstrap.Toast(toastEl, { autohide: false });
                toast.show();
            })
            .catch(error => console.error('Error:', error));

        return false; // Prevent the form from redirecting
    });
});
