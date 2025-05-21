let chickens = []; // Array to hold chicken data
let currentEditIndex = -1; // To track which chicken is being edited

document.getElementById('chickenForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    const name = document.getElementById('chickenName').value;
    const breed = document.getElementById('breed').value;
    const age = document.getElementById('age').value;

    if (currentEditIndex === -1) {
        // Add new chicken
        const chicken = { name, breed, age: parseInt(age) };
        chickens.push(chicken);
    } else {
        // Update existing chicken
        chickens[currentEditIndex] = { name, breed, age: parseInt(age) };
        currentEditIndex = -1; // Reset edit index
    }

    // Clear the form fields
    document .getElementById('chickenForm').reset();

    // Refresh the chicken list
    renderChickenList();
});

function renderChickenList() {
    const tableBody = document.getElementById('chickenTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear existing rows

    chickens.forEach((chicken, index) => {
        const newRow = tableBody.insertRow();

        // Insert new cells for name, breed, age, and actions
        const nameCell = newRow.insertCell(0);
        const breedCell = newRow.insertCell(1);
        const ageCell = newRow.insertCell(2);
        const actionsCell = newRow.insertCell(3);

        nameCell.textContent = chicken.name;
        breedCell.textContent = chicken.breed;
        ageCell.textContent = chicken.age;

        // Add edit button
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.onclick = () => editChicken(index);
        actionsCell.appendChild(editButton);

        // Add sell button
        const sellButton = document.createElement('button');
        sellButton.textContent = 'Sell';
        sellButton.onclick = () => sellChicken(chicken.name);
        actionsCell.appendChild(sellButton);
    });
}

function editChicken(index) {
    currentEditIndex = index;
    const chicken = chickens[index];

    document.getElementById('chickenName').value = chicken.name;
    document.getElementById('breed').value = chicken.breed;
    document.getElementById('age').value = chicken.age;
}

document.getElementById('sellForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const sellName = document.getElementById('sellName').value;
    const sellPrice = document.getElementById('sellPrice').value;

    const chickenIndex = chickens.findIndex(chicken => chicken.name === sellName);
    if (chickenIndex !== -1) {
        chickens.splice(chickenIndex, 1); // Remove chicken from the list
        document.getElementById('sellMessage').textContent = `Sold ${sellName} for $${sellPrice}.`;
        renderChickenList(); // Refresh the chicken list
    } else {
        document.getElementById('sellMessage').textContent = `Chicken ${sellName} not found.`;
    }

    // Clear the sell form fields
    document.getElementById('sellForm').reset();
});