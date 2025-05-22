
const ctx = document.getElementById('protocolChart').getContext('2d');
let chart;

function updateProtocolChart() {
    fetch('/protocols')
        .then(res => res.json())
        .then(data => {
            const labels = Object.keys(data);
            const values = Object.values(data);
            if (!chart) {
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Protokolle',
                            data: values,
                            backgroundColor: 'rgba(54, 162, 235, 0.7)'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { labels: { color: 'white' } }
                        },
                        scales: {
                            x: { ticks: { color: 'white' } },
                            y: { ticks: { color: 'white' } }
                        }
                    }
                });
            } else {
                chart.data.labels = labels;
                chart.data.datasets[0].data = values;
                chart.update();
            }
        });
}

function updateTopTalkers() {
    fetch('/toptalkers')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('toptalkers');
            list.innerHTML = '';
            data.forEach(([ip, count]) => {
                const li = document.createElement('li');
                li.className = "list-group-item";
                li.textContent = `${ip || 'Unbekannt'} (${count} Pakete)`;
                list.appendChild(li);
            });
        });
}

function updateConnections() {
    fetch('/connections')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('connections');
            list.innerHTML = '';
            data.forEach(([src, dst, count]) => {
                const li = document.createElement('li');
                li.className = "list-group-item";
                li.textContent = `${src || '??'} → ${dst || '??'} (${count}x)`;
                list.appendChild(li);
            });
        });
}

function updatePorts() {
    fetch('/ports')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('ports');
            list.innerHTML = '';
            data.forEach(([port, count]) => {
                const li = document.createElement('li');
                li.className = "list-group-item";
                li.textContent = `Port ${port || '??'} (${count}x)`;
                list.appendChild(li);
            });
        });
}

function refreshAll() {
    updateProtocolChart();
    updateTopTalkers();
    updateConnections();
    updatePorts();
}

setInterval(refreshAll, 3000);
refreshAll();
