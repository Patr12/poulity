function showPage(pageId) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

function deleteRow(button) {
    const row = button.closest("tr");
    row.remove();
}

document.addEventListener("DOMContentLoaded", () => {
    showPage("home");

    const diseaseForm = document.getElementById("diseaseForm");
    const diseaseTableBody = document.querySelector("#diseaseTable tbody");

    diseaseForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const name = document.getElementById("diseaseName").value.trim();
        const description = document.getElementById("diseaseDescription").value.trim();

        if (name && description) {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${name}</td>
                <td>${description}</td>
                <td><button onclick="deleteRow(this)">Delete</button></td>
            `;
            diseaseTableBody.appendChild(row);
            diseaseForm.reset();
        }
    });

    const vaccinationForm = document.getElementById("vaccinationForm");
    const vaccinationTableBody = document.querySelector("#vaccinationTable tbody");

    vaccinationForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const vaccineType = document.getElementById("vaccineType").value.trim();
        const date = document.getElementById("vaccinationDate").value;
        const medication = document.getElementById("medication").value.trim();

        if (vaccineType && date && medication) {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${vaccineType}</td>
                <td>${date}</td>
                <td>${medication}</td>
                <td><button onclick="deleteRow(this)">Delete</button></td>
            `;
            vaccinationTableBody.appendChild(row);
            vaccinationForm.reset();
        }
    });
});
