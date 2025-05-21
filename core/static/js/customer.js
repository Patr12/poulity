let customers = []; // Array to hold customer data
let currentEditIndex = -1; // To track which customer is being edited

document.getElementById('customerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    const name = document.getElementById('customerName').value;
    const email = document.getElementById('customerEmail').value;
    const phone = document.getElementById('customerPhone').value;

    if (currentEditIndex === -1) {
        // Add new customer
        const customer = { name, email, phone };
        customers.push(customer);
    } else {
        // Update existing customer
        customers[currentEditIndex] = { name, email, phone };
        currentEditIndex = -1; // Reset edit index
    }

    // Clear the form fields
    document.getElementById('customerForm').reset();

    // Refresh the customer list
    renderCustomerList();
});

function renderCustomerList() {
    const tableBody = document.getElementById('customerTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear existing rows

    customers.forEach((customer, index) => {
        const newRow = tableBody.insertRow();

        // Insert new cells for name, email, phone, and actions
        const nameCell = newRow.insertCell(0);
        const emailCell = newRow.insertCell(1);
        const phoneCell = newRow.insertCell(2);
        const actionsCell = newRow.insertCell(3);

        nameCell.textContent = customer.name;
        emailCell.textContent = customer.email;
        phoneCell.textContent = customer.phone;

        // Add edit button
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.onclick = () => editCustomer(index);
        actionsCell.appendChild(editButton);

        // Add delete button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deleteCustomer(index);
        actionsCell.appendChild(deleteButton);
    });
}

function editCustomer(index) {
    currentEditIndex = index;
    const customer = customers[index];

    document.getElementById('customerName').value = customer.name;
    document.getElementById('customerEmail').value = customer.email;
    document.getElementById('customerPhone').value = customer.phone;
}

function deleteCustomer(index) {
    customers.splice(index, 1); // Remove customer from the list
    renderCustomerList(); // Refresh the customer list
}