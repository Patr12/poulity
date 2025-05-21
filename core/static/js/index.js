let vaccinationRecords = []; // Array to hold vaccination records

document.getElementById('vaccinationForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    const chickenName = document.getElementById('chickenName').value;
    const vaccinationDate = document.getElementById('vaccinationDate').value;
    const vaccineType = document.getElementById('vaccineType').value;

    // Add new vaccination record
    const record = { chickenName, vaccinationDate, vaccineType };
    vaccinationRecords.push(record);

    // Clear the form fields
    document.getElementById('vaccinationForm').reset();

    // Refresh the vaccination records list
    renderVaccinationList();
});

function renderVaccinationList() {
    const tableBody = document.getElementById('vaccinationTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear existing rows

    vaccinationRecords.forEach((record, index) => {
        const newRow = tableBody.insertRow();

        // Insert new cells for chicken name, vaccination date, vaccine type, and actions
        const nameCell = newRow.insertCell(0);
        const dateCell = newRow.insertCell(1);
        const typeCell = newRow.insertCell(2);
        const actionsCell = newRow.insertCell(3);

        nameCell.textContent = record.chickenName;
        dateCell.textContent = record.vaccinationDate;
        typeCell.textContent = record.vaccineType;

        // Add delete button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deleteVaccinationRecord(index);
        actionsCell.appendChild(deleteButton);
    });
}

function deleteVaccinationRecord(index) {
    vaccinationRecords.splice(index, 1); // Remove record from the list
    renderVaccinationList(); // Refresh the vaccination records list
}

function generateReport() {
    const reportOutput = document.getElementById('reportOutput');
    reportOutput.innerHTML = ''; // Clear previous report

    if (vaccinationRecords.length === 0) {
        reportOutput.textContent = 'No vaccination records available to generate a report.';
        return;
    }

    let reportContent = '<h2>Vaccination Report</h2><ul>';
    vaccinationRecords.forEach(record => {
        reportContent += `<li>${record.chickenName} - ${record.vaccinationDate} - ${record.vaccineType}</li>`;
    });
    reportContent += '</ul>';
    reportOutput.innerHTML = reportContent;
}