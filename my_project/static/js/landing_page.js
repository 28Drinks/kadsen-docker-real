


const ctx = document.getElementById('myChart');

const myChart = new Chart(ctx, {
    type: config["type"],
    data: config["data"],
    options: {
        responsive: true,
        maintainAspectRatio: false,
    }
});
