const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
ctx.strokeStyle = '#000';
ctx.lineWidth = 1;
ctx.lineJoin = 'round';

let isDrawing = false;
let previousX, previousY;

function drawLine(x1, y1, x2, y2) {
    // Реализация алгоритма Ву для сглаживания линий
    const dx = Math.abs(x2 - x1);
    const dy = Math.abs(y2 - y1);

    if (dx > dy) {
        if (x1 > x2) {
            [x1, x2] = [x2, x1];
            [y1, y2] = [y2, y1];
        }

        const gradient = dy / dx;
        let y = y1;

        for (let x = x1; x <= x2; x++) {
            ctx.fillRect(x, Math.floor(y), 1, 1);
            ctx.fillRect(x, Math.ceil(y), 1, 1);
            y += gradient;
        }
    } else {
        if (y1 > y2) {
            [x1, x2] = [x2, x1];
            [y1, y2] = [y2, y1];
        }

        const gradient = dx / dy;
        let x = x1;

        for (let y = y1; y <= y2; y++) {
            ctx.fillRect(Math.floor(x), y, 1, 1);
            ctx.fillRect(Math.ceil(x), y, 1, 1);
            x += gradient;
        }
    }
}

canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    [previousX, previousY] = [e.clientX - canvas.getBoundingClientRect().left, e.clientY - canvas.getBoundingClientRect().top];
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDrawing) return;
    const [x, y] = [e.clientX - canvas.getBoundingClientRect().left, e.clientY - canvas.getBoundingClientRect().top];
    drawLine(previousX, previousY, x, y);
    [previousX, previousY] = [x, y];
});

canvas.addEventListener('mouseup', () => {
    isDrawing = false;
});

canvas.addEventListener('mouseout', () => {
    isDrawing = false;
});
