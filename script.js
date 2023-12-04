const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const drawLineBtn = document.getElementById("drawLineBtn");

drawLineBtn.addEventListener("click", drawLine);

function drawLine() {
    const x1 = parseInt(prompt("Введите X1:"));
    const y1 = parseInt(prompt("Введите Y1:"));
    const x2 = parseInt(prompt("Введите X2:"));
    const y2 = parseInt(prompt("Введите Y2:"));

    const startTime = performance.now(); // Запоминаем время начала отрисовки

    bresenhamLine(x1, y1, x2, y2);

    const endTime = performance.now(); // Запоминаем время окончания отрисовки
    const elapsedTime = endTime - startTime; // Вычисляем время отрисовки

    alert("Время отрисовки: " + elapsedTime + " миллисекунд");
}

function bresenhamLine(x1, y1, x2, y2) {
    const dx = Math.abs(x2 - x1);
    const dy = Math.abs(y2 - y1);
    const sx = (x1 < x2) ? 1 : -1;
    const sy = (y1 < y2) ? 1 : -1;
    let err = dx - dy;

    while (true) {
        ctx.fillRect(x1, -y1, 1, 1);

        if (x1 === x2 && y1 === y2) {
            break;
        }

        const e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x1 += sx;
        }
        if (e2 < dx) {
            err += dx;
            y1 += sy;
        }
    }
}

// привет Билли Харингтон
const graph_width = canvas.width;
const graph_height = canvas.height;

// Добавляем масштаб, систему координат, оси, линии сетки и подписи
const scale = 20; // масштаб

// Система координат
ctx.beginPath();
ctx.moveTo(graph_width / 2, 0);
ctx.lineTo(graph_width / 2, graph_height);
ctx.moveTo(0, graph_height / 2);
ctx.lineTo(graph_width, graph_height / 2);
ctx.strokeStyle = "#888";
ctx.stroke();

// Линии сетки
for (let i = 0; i < graph_width; i += scale) {
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, graph_height);
    ctx.moveTo(0, i);
    ctx.lineTo(graph_width, i);
    ctx.strokeStyle = "#ddd";
    ctx.stroke();
}

// Подписи
for (let i = -graph_width / 2; i <= graph_width / 2; i += scale) {
    ctx.fillText(i, graph_width / 2 + i - 3, graph_height / 2 + 10);
    ctx.fillText(i, graph_width / 2 + 5, graph_height / 2 - i + 3);
}

ctx.translate(200, 200);