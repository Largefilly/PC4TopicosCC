// static/blobs.js
async function fetchState() {
  const response = await fetch("/state");
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  return response.json();
}

function drawBlob(ctx, blob, minSpeed, maxSpeed) {
  // Evitamos división por cero
  const range = Math.max(maxSpeed - minSpeed, 0.0001);

  // t va de 0 (lento) a 1 (rápido) según la población actual
  const t = (blob.speed - minSpeed) / range;

  // Color: de azul (lentos) a rojo (rápidos) pasando por morado
  // hue: 240° = azul, 0° = rojo
  const hue = (1 - t) * 240;
  ctx.fillStyle = `hsl(${hue}, 80%, 50%)`;
  ctx.strokeStyle = "#000";

  ctx.beginPath();
  ctx.arc(blob.x, blob.y, 5, 0, 2 * Math.PI);
  ctx.fill();
  ctx.stroke();
}

function drawFood(ctx, f) {
  ctx.fillStyle = "green";
  ctx.beginPath();
  ctx.arc(f.x, f.y, 3, 0, 2 * Math.PI);
  ctx.fill();
}

(() => {
  const canvas = document.getElementById("elCanvas");
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    console.error("2D context not supported/available.");
    return;
  }
  canvas.width = 1500;
  canvas.height = 900;

  const slider = document.getElementById("speedSlider");
  const label = document.getElementById("speedLabel");
  const statsDiv = document.getElementById("stats");

  let delay = parseInt(slider.value, 10);
  label.textContent = `${delay} ms`;

  slider.addEventListener("input", () => {
    delay = parseInt(slider.value, 10);
    label.textContent = `${delay} ms`;
  });

  async function loop() {
    try {
      const state = await fetchState();
      const blobs = state.blobs;
      const food = state.food;

      // --- estadísticas básicas ---
      const day = state.day;
      const phase = state.phase;

      let alive = 0;
      let total = blobs.length;
      let sumSpeed = 0;
      let sumEnergy = 0;
      let minSpeed = Infinity;
      let maxSpeed = -Infinity;

      for (const b of blobs) {
        if (!b.alive) continue;
        alive++;
        sumSpeed += b.speed;
        sumEnergy += b.energy;
        if (b.speed < minSpeed) minSpeed = b.speed;
        if (b.speed > maxSpeed) maxSpeed = b.speed;
      }

      const dead = total - alive;
      const foodRemaining = food.length;
      const avgSpeed = alive > 0 ? sumSpeed / alive : 0;
      const avgEnergy = alive > 0 ? sumEnergy / alive : 0;

      // Mostrar stats en el panel
      if (statsDiv) {
        statsDiv.innerHTML = `
          <b>Dia:</b> ${day} &nbsp;
          <b>Fase:</b> ${phase} <br/>
          <b>Vivos:</b> ${alive} &nbsp;
          <b>Muertos:</b> ${dead} &nbsp;
          <b>Total:</b> ${total} &nbsp;
          <b>Comida restante:</b> ${foodRemaining} <br/>
          <b>Velocidad promedio.:</b> ${avgSpeed.toFixed(2)} &nbsp;
          <b>Energia promedio:</b> ${avgEnergy.toFixed(1)}
        `;
      }

      // --- limpiar canvas ---
      canvas.width = canvas.width;

      // --- dibujar comida ---
      for (const f of food) {
        drawFood(ctx, f);
      }

      // --- asegurar min/max velocidad para colorear ---
      if (!isFinite(minSpeed)) {
        minSpeed = 0;
        maxSpeed = 1;
      }

      // --- dibujar blobs ---
      for (const b of blobs) {
        if (b.alive) {
          drawBlob(ctx, b, minSpeed, maxSpeed);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setTimeout(loop, delay);
    }
  }

  loop();
})();
