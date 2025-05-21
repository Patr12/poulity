document.addEventListener("DOMContentLoaded", () => {
    // Handle delete button for feeding record
    const deleteButtons = document.querySelectorAll(".delete-feeding-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const row = button.closest("tr");
            const feedingId = row.getAttribute("data-feeding-id");

            // Confirmation before deleting
            if (confirm("Are you sure you want to delete this record?")) {
                // Perform AJAX request to delete feeding from the server
                fetch(`/feeding/delete/${feedingId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                    }
                }).then(response => {
                    if (response.ok) {
                        // Remove the row from the table if deletion is successful
                        row.remove();
                    } else {
                        alert("Error deleting the record.");
                    }
                }).catch(error => {
                    console.error("Error deleting the record:", error);
                });
            }
        });
    });

    // Optional: Show alert after adding a new feeding
    const feedingForm = document.querySelector("form");

    feedingForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const chicken = document.querySelector('input[name="chicken"]').value;
        const feedType = document.querySelector('input[name="feed_type"]').value;
        const quantity = document.querySelector('input[name="quantity"]').value;

        if (chicken && feedType && quantity) {
            alert("Feeding record added successfully!");
        }
    });
});
