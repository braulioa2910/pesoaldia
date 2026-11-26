/* Funciones compartidas del sitio */
const MXN = new Intl.NumberFormat('es-MX', {style: 'currency', currency: 'MXN'});
const NUM4 = new Intl.NumberFormat('es-MX', {minimumFractionDigits: 4, maximumFractionDigits: 4});
const FECHA = new Intl.DateTimeFormat('es-MX', {weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC'});
const FCORTA = new Intl.DateTimeFormat('es-MX', {day: 'numeric', month: 'short', timeZone: 'UTC'});

function aFecha(iso) { return new Date(iso + 'T00:00:00Z'); }

async function cargarTipoCambio() {
  const r = await fetch('data/tipo-cambio.json', {cache: 'no-cache'});
  if (!r.ok) throw new Error('No se pudo cargar el tipo de cambio');
  const j = await r.json();
  const datos = (j.datos || []).filter(d => typeof d.valor === 'number' && isFinite(d.valor));
  if (!datos.length) throw new Error('Sin datos');
  datos.sort((a, b) => a.fecha.localeCompare(b.fecha));
  return {datos, actualizado: j.actualizado, fuente: j.fuente};
}

function cambio(datos) {
  const hoy = datos[datos.length - 1], ant = datos[datos.length - 2];
  if (!ant) return {hoy, ant: null, dif: 0, pct: 0};
  const dif = hoy.valor - ant.valor;
  return {hoy, ant, dif, pct: dif / ant.valor * 100};
}

function chipCambio(el, c) {
  if (!c.ant) { el.textContent = 'Primer dato'; return; }
  const sube = c.dif > 0, igual = Math.abs(c.dif) < 0.00005;
  el.className = 'chip ' + (igual ? '' : sube ? 'up' : 'down');
  const signo = igual ? '' : sube ? '▲ +' : '▼ ';
  el.textContent = `${signo}${NUM4.format(c.dif)} (${c.pct.toFixed(2)}%) vs. ${FCORTA.format(aFecha(c.ant.fecha))}`;
}

/* Gráfica de línea a tamaño real; se redibuja al cambiar el ancho */
function graficaLinea(svg, datos) {
  const draw = () => {
    const W = svg.clientWidth, H = svg.clientHeight;
    if (!W || !H) return;
    const pad = {l: W < 520 ? 8 : 52, r: 12, t: 14, b: 26};
    const vals = datos.map(d => d.valor);
    let min = Math.min(...vals), max = Math.max(...vals);
    const m = (max - min) * 0.15 || 0.1; min -= m; max += m;
    const x = i => pad.l + (datos.length === 1 ? 0.5 : i / (datos.length - 1)) * (W - pad.l - pad.r);
    const y = v => pad.t + (1 - (v - min) / (max - min)) * (H - pad.t - pad.b);
    const pts = datos.map((d, i) => `${x(i).toFixed(1)},${y(d.valor).toFixed(1)}`);
    let g = '';
    if (W >= 520) {
      for (let k = 0; k <= 3; k++) {
        const v = min + (max - min) * k / 3, yy = y(v).toFixed(1);
        g += `<line x1="${pad.l}" x2="${W - pad.r}" y1="${yy}" y2="${yy}" stroke="currentColor" stroke-opacity=".12"/>`;
        g += `<text x="${pad.l - 8}" y="${+yy + 4}" text-anchor="end">${v.toFixed(2)}</text>`;
      }
    }
    const first = datos[0], last = datos[datos.length - 1];
    g += `<text x="${pad.l}" y="${H - 6}">${FCORTA.format(aFecha(first.fecha))}</text>`;
    g += `<text x="${W - pad.r}" y="${H - 6}" text-anchor="end">${FCORTA.format(aFecha(last.fecha))}</text>`;
    const area = `M${pts[0]} L${pts.join(' L')} L${x(datos.length - 1).toFixed(1)},${H - pad.b} L${x(0).toFixed(1)},${H - pad.b} Z`;
    g += `<path d="${area}" fill="#4fb3e8" fill-opacity=".18"/>`;
    g += `<polyline points="${pts.join(' ')}" fill="none" stroke="#2b8fc7" stroke-width="2.5" stroke-linejoin="round"/>`;
    g += `<circle cx="${x(datos.length - 1)}" cy="${y(last.valor)}" r="5" fill="#ff7a1a"/>`;
    svg.innerHTML = g;
  };
  const ro = new ResizeObserver(draw);
  ro.observe(svg);
  draw();
}

/* Marca en el menú la página actual */
{
  const aqui = location.pathname.split('/').pop().replace('.html', '') || 'index';
  for (const a of document.querySelectorAll('.nav ul a')) {
    const destino = a.getAttribute('href').replace('.html', '').replace('./', '') || 'index';
    if (destino === aqui) a.setAttribute('aria-current', 'page');
  }
  const y = document.getElementById('anio');
  if (y) y.textContent = new Date().getFullYear();
}
