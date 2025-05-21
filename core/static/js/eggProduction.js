document.getElementById('eggProductionForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    const date = document.getElementById('date').value;
    const quantity = document.getElementById('quantity').value;

    // Create a new row in the table
    const table = document.getElementById('productionTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();

    // Insert new cells for date and quantity
    const dateCell = newRow.insertCell(0);
    const quantityCell = newRow.insertCell(1);

    // Set the cell values
    dateCell.textContent = date;
    quantityCell.textContent = quantity;

    // Clear the form fields
    document.getElementById('eggProductionForm').reset();
});