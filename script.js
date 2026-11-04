const canvas  = document.getElementById('gauge');
const ctx = canvas.getContext('2d');
const radius = 100;
const maxSpeed = 200;

function drawGauge() {
 ctx.clearRect(0, 0, canvas.width, canvas.height);
 ctx.beginPath();
 ctx.arc(canvas.width / 2, canvas.height / 2, radius, 0.75 * Math.PI, 2.25 * Math.PI);
 ctx.strokeStyle = '#333';
 ctx.lineWidth = 10;
 ctx.stroke();
}

drawGauge();
 
