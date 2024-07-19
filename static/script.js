function sendData() {
    const textInput = document.getElementById('textInput').value;
    const numberInput = document.getElementById('numberInput').value;
    const data = { text: textInput, number: numberInput };

    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Data sent successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to send data.');
    });
}

function loadData() {
    fetch('/load-data')
    .then(response => response.json())
    .then(data => {
        console.log('Data fetched:', data);
        const contentDisplay = document.getElementById('contentDisplay');
        contentDisplay.innerHTML = '';

        if (data.in_progres_start && data.in_progres_start.length > 0) {
            contentDisplay.innerHTML += '<h3>In Progress Start Files:</h3><ul>';
            data.in_progres_start.forEach(file => {
                contentDisplay.innerHTML += `<li>${file}</li>`;
            });
            contentDisplay.innerHTML += '</ul>';
        }

        if (data.in_progres && data.in_progres.length > 0) {
            contentDisplay.innerHTML += '<h3>In Progress Files:</h3><ul>';
            data.in_progres.forEach(file => {
                contentDisplay.innerHTML += `<li>${file}</li>`;
            });
            contentDisplay.innerHTML += '</ul>';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to load data.');
    });
}

function loadResults() {
    fetch('/load-results')
    .then(response => response.json())
    .then(data => {
        console.log('Results fetched:', data);
        const resultsDisplay = document.getElementById('resultsDisplay');
        resultsDisplay.innerHTML = '';

        for (const dir in data) {
            resultsDisplay.innerHTML += `<h3>${dir}:</h3><ul>`;
            data[dir].forEach(file => {
                resultsDisplay.innerHTML += `<li onclick="viewCSV('${dir}/${file}')">${file}</li>`;
            });
            resultsDisplay.innerHTML += '</ul>';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to load results.');
    });
}

function viewCSV(filePath) {
    window.location.href = `/csv-viewer/${filePath}`;
}

// Call loadData and loadResults once immediately and then at intervals
loadData();
loadResults();
setInterval(loadData, 5000); // Refresh in-progress content every 5 seconds
setInterval(loadResults, 5000); // Refresh results content every 5 seconds
