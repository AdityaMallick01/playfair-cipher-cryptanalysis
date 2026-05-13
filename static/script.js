let chartInstance = null;

async function sendRequest(action) {

    const text =
        document.getElementById("text").value;

    const key =
        document.getElementById("key").value;

    const response = await fetch("/process", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            text,
            key,
            action
        })
    });

    const data = await response.json();

    if (action === "encrypt" ||
        action === "decrypt") {

        document.getElementById("rowwise").innerText =
            data.rowwise;

        document.getElementById("columnwise").innerText =
            data.columnwise;

        generateFrequencyGraph(data.rowwise);
    }

    if (data.row_matrix) {

        const rowTable =
            document.getElementById("rowMatrix");

        rowTable.innerHTML = "";

        data.row_matrix.forEach(row => {

            const tr =
                document.createElement("tr");

            row.forEach(cell => {

                const td =
                    document.createElement("td");

                td.innerText = cell;

                tr.appendChild(td);
            });

            rowTable.appendChild(tr);
        });
    }

    if (data.column_matrix) {

        const columnTable =
            document.getElementById("columnMatrix");

        columnTable.innerHTML = "";

        data.column_matrix.forEach(row => {

            const tr =
                document.createElement("tr");

            row.forEach(cell => {

                const td =
                    document.createElement("td");

                td.innerText = cell;

                tr.appendChild(td);
            });

            columnTable.appendChild(tr);
        });
    }

    if (action === "attack") {

        document.getElementById("attackResult")
            .innerHTML = `

            <strong>Recovered Key:</strong>
            ${data.key}

            <br><br>

            <strong>Recovered Text:</strong>
            ${data.text}

            <br><br>

            <strong>Confidence Score:</strong>
            ${data.score}
        `;
    }
}

function encryptText() {

    sendRequest("encrypt");
}

function decryptText() {

    sendRequest("decrypt");
}

function attackCipher() {

    sendRequest("attack");
}

function generateFrequencyGraph(text) {

    const freq = {};

    text = text.replace(/[^A-Z]/gi, "");

    for (let char of text) {

        freq[char] = (freq[char] || 0) + 1;
    }

    const labels = Object.keys(freq);

    const values = Object.values(freq);

    const ctx =
        document.getElementById("freqChart");

    if (chartInstance) {

        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {

        type: 'bar',

        data: {

            labels: labels,

            datasets: [{

                label: 'Character Frequency',

                data: values,

                borderWidth: 1
            }]
        },

        options: {

            responsive: true,

            scales: {

                y: {
                    beginAtZero: true
                }
            }
        }
    });
}