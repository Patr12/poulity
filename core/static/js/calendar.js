let vaccinationLabels = []; // Array to hold vaccination labels
let eggLayLabels = []; // Array to hold egg lay labels
let orderLabels = []; // Array to hold order labels

document.getElementById('label-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    const vaccinationDate = document.getElementById('vaccination-date').value;
    const eggLayDate = document.getElementById('egg-lay-date').value;
    const orderDate = document.getElementById('order-date').value;

    // Add new labels
    if (vaccinationDate) {
        vaccinationLabels.push(vaccinationDate);
    }
    if (eggLayDate) {
        eggLayLabels.push(eggLayDate);
    }
    if (orderDate) {
        orderLabels.push(orderDate);
    }

    // Clear the form fields
    document.getElementById('label-form').reset();

    // Refresh the labels
    renderLabels();
});

function renderLabels() {
    const vaccinationLabelsList = document.getElementById('vaccination-labels');
    vaccinationLabelsList.innerHTML = ''; // Clear existing labels
    vaccinationLabels.forEach(label => {
        const newLabel = document.createElement('li');
        newLabel.textContent = label;
        vaccinationLabelsList.appendChild(newLabel);
    });

    const eggLayLabelsList = document.getElementById('egg-lay-labels');
    eggLayLabelsList.innerHTML = ''; // Clear existing labels
    eggLayLabels.forEach(label => {
        const newLabel = document.createElement('li');
        newLabel.textContent = label;
        eggLayLabelsList.appendChild(newLabel);
    });

    const orderLabelsList = document.getElementById(' order-labels');
    orderLabelsList.innerHTML = ''; // Clear existing labels
    orderLabels.forEach(label => {
        const newLabel = document.createElement('li');
        newLabel.textContent = label;
        orderLabelsList.appendChild(newLabel);
    });
}

// Function to generate the calendar for the current month
function generateCalendar() {
    const calendarBody = document.getElementById('calendar-body');
    const date = new Date();
    const month = date.getMonth();
    const year = date.getFullYear();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    calendarBody.innerHTML = ''; // Clear existing calendar

    // Fill the calendar with empty cells for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement('td');
        calendarBody.appendChild(cell);
    }

    // Fill the calendar with the actual days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const cell = document.createElement('td');
        cell.textContent = day;
        calendarBody.appendChild(cell);
    }
}

// Call the function to generate the calendar when the page loads
window.onload = generateCalendar;