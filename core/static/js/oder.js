document.getElementById('orderForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    const orderDate = document.getElementById('orderDate').value;
    const customerName = document.getElementById('customerName').value;
    const orderType = document.getElementById('orderType').value;
    const orderDetails = document.getElementById('orderDetails').value;
    const quantity = document.getElementById('quantity').value;

    // Create a new row in the table
    const table = document.getElementById('orderTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();

    // Insert new cells for date, customer name, order type, order details, quantity, and actions
    const dateCell = newRow.insertCell(0);
    const customerCell = newRow.insertCell( 1);
    const typeCell = newRow.insertCell(2);
    const detailsCell = newRow.insertCell(3);
    const quantityCell = newRow.insertCell(4);
    const actionCell = newRow.insertCell(5);

    // Set the cell values
    dateCell.textContent = orderDate;
    customerCell.textContent = customerName;
    typeCell.textContent = orderType;
    detailsCell.textContent = orderDetails;
    quantityCell.textContent = quantity;

    // Create a delete button
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = function() {
        table.deleteRow(newRow.rowIndex - 1); // Adjust for header row
    };

    // Append the delete button to the action cell
    actionCell.appendChild(deleteButton);

    // Clear the form fields after submission
    document.getElementById('orderForm').reset();
});