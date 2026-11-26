"""Genera las páginas nuevas del sitio con la misma cabecera, menú y pie.
Uso: python scripts/paginas_nuevas.py  (desde la carpeta del sitio)"""
import glob
import re

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' "
           "height='32' rx='8' fill='%2310223a'/%3E%3Cpath d='M7 22l6-7 5 4 7-9' stroke='%23ff7a1a' stroke-width='3' "
           "fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")

NAV = '''<nav class="nav" aria-label="Principal">
      <a class="logo" href="./"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#10223a"/><path d="M7 22l6-7 5 4 7-9" stroke="#ff7a1a" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>Peso al Día</a>
      <ul>
        <li><a href="dolar-hoy.html">Dólar hoy</a></li>
        <li><a href="calculadora-aguinaldo.html">Aguinaldo</a></li>
        <li><a href="calculadora-finiquito.html">Finiquito</a></li>
        <li><a href="calculadora-sueldo-neto.html">Sueldo neto</a></li>
        <li><a href="./#guias">Guías</a></li>
      </ul>
    </nav>'''

FOOTER = '''<footer>
  <div class="wrap">
    <div>© <span id="anio">2026</span> Peso al Día · Datos oficiales de Banxico, INEGI, SAT y CONASAMI.</div>
    <ul>
      <li><a href="acerca.html">Acerca y contacto</a></li>
      <li><a href="privacidad.html">Aviso de privacidad</a></li>
      <li><a href="terminos.html">Términos de uso</a></li>
    </ul>
  </div>
</footer>'''


def head(title, desc, extra=''):
    return f'''<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#4fb3e8">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<!-- Código de AdSense aquí cuando te aprueben -->
{extra}</head>'''


def pagina(archivo, title, desc, h1, lead, main, scripts='', extra_head='', hero_extra=''):
    html = head(title, desc, extra_head) + f'''
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="top">
  <div class="wrap">
    {NAV}
    <div class="hero" style="padding-bottom:28px">
      <h1 class="in">{h1}</h1>
      <p class="lead in" style="margin:0">{lead}</p>{hero_extra}
    </div>
  </div>
</header>

<main id="contenido">
  <div class="wrap">
{main}
  </div>
</main>

{FOOTER}
<script src="assets/site.js"></script>
{scripts}
</body>
</html>
'''
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(html)


def faq_ld(pares):
    import json
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n'


def faq_html(pares):
    return '\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in pares)


AD = '    <div class="ad"><!-- Bloque de anuncio AdSense --></div>'

# ---------------------------------------------------------------- Sueldo neto
faq = [
    ("¿Qué es el subsidio para el empleo?", "Es un apoyo fiscal que reduce el ISR de quienes ganan hasta $11,492.66 al mes en 2026. Equivale a $535.65 mensuales y nunca puede ser mayor que el ISR que te toca pagar."),
    ("¿Por qué ganar un poco más puede dejarme con menos neto?", "Si tu sueldo pasa de $11,492.66 al mes pierdes el subsidio completo. Por eso alguien que gana $11,500 puede recibir menos neto que alguien que gana $11,490."),
    ("¿Si gano el salario mínimo me descuentan algo?", "No. A quien gana el salario mínimo no se le retiene ISR, y su cuota del IMSS la paga el patrón."),
]
pagina('calculadora-sueldo-neto.html',
       'Calculadora de sueldo neto 2026: ISR e IMSS',
       'Calcula cuánto te llega de sueldo después de ISR, subsidio para el empleo e IMSS con las tablas 2026. Gratis y sin registro.',
       'Calculadora de sueldo neto 2026',
       'Escribe tu sueldo bruto y ve cuánto te descuentan de ISR e IMSS y cuánto te llega.',
       f'''    <section class="band calc">
      <form id="f" novalidate>
        <div class="field">
          <fieldset>
            <legend>Periodo de tu sueldo</legend>
            <div class="seg">
              <label><input type="radio" name="tipo" value="mensual" checked><span>Mensual</span></label>
              <label><input type="radio" name="tipo" value="quincenal"><span>Quincenal</span></label>
              <label><input type="radio" name="tipo" value="semanal"><span>Semanal</span></label>
            </div>
          </fieldset>
        </div>
        <div class="field">
          <label for="sueldo">Sueldo bruto (antes de descuentos)</label>
          <input id="sueldo" type="number" inputmode="decimal" min="0" step="any" value="15000">
        </div>
        <div class="field">
          <label for="zona">Zona de salario mínimo</label>
          <select id="zona">
            <option value="general">General (casi todo el país)</option>
            <option value="frontera">Zona Libre de la Frontera Norte</option>
          </select>
        </div>
        <div class="field">
          <label style="display:flex;gap:10px;align-items:center;font-weight:500"><input type="checkbox" id="imss" checked style="width:22px;height:22px;flex:none">Descontar cuota del IMSS</label>
          <span class="hint">Desmárcalo si trabajas por honorarios o sin seguro social.</span>
        </div>
      </form>
      <aside class="result" aria-live="polite">
        <div style="font-weight:600" id="rt">Te llega al mes</div>
        <div class="big" id="neto">$0</div>
        <div id="rsub"></div>
        <ul class="lines">
          <li><span>Sueldo bruto</span><b id="bruto">$0</b></li>
          <li><span>ISR según tabla</span><b id="isrc">$0</b></li>
          <li><span>Subsidio para el empleo (se resta)</span><b id="sub">$0</b></li>
          <li><span>ISR que te retienen</span><b id="isr">$0</b></li>
          <li><span>IMSS (estimado)</span><b id="imssv">$0</b></li>
          <li class="total"><span>Sueldo neto</span><b id="neto2">$0</b></li>
        </ul>
        <p class="note" id="aviso"></p>
      </aside>
    </section>
{AD}
    <section class="band prose">
      <h2>Cómo se calcula tu sueldo neto</h2>
      <p>Tu patrón te retiene ISR con la tarifa mensual del artículo 96 de la Ley del ISR. Ubica tu sueldo en la tabla, le resta el límite inferior, multiplica lo que sobra por el porcentaje de ese renglón y le suma la cuota fija. Si ganas hasta $11,492.66 al mes, a ese ISR se le resta el subsidio para el empleo de $535.65.</p>
      <p>Además se descuenta tu parte de las cuotas del IMSS, que en total ronda el 2.4 % de tu salario base de cotización. Esta calculadora la estima con las prestaciones mínimas de ley; tu recibo puede variar un poco si tienes más prestaciones, vales o fondo de ahorro.</p>
      <div class="box">
        <h3>Ejemplo con $15,000 al mes</h3>
        <p style="margin:0">El ISR según la tabla es de unos $1,403. Como pasas del límite, no hay subsidio. El IMSS ronda los $394. Te llegan cerca de <strong>$13,203</strong> al mes.</p>
      </div>
      <h2>Preguntas frecuentes</h2>
{faq_html(faq)}
      <p class="meta">Tarifa ISR mensual 2026 (Anexo 8 RMF, DOF 28/12/2025); subsidio para el empleo (DOF 31/12/2025); UMA 2026 $117.31. Resultado estimado e informativo.</p>
    </section>
{AD}''',
       scripts='''<script src="assets/aguinaldo.js"></script>
<script src="assets/sueldo.js"></script>
<script>
{
  const $ = id => document.getElementById(id);
  const f = $('f'), CLAVE = 'pad-sueldo';
  const aMes = {mensual: 1, quincenal: 30.4 / 15.2, semanal: 30.4 / 7};
  function pintar() {
    const tipo = f.tipo.value, s = +$('sueldo').value || 0;
    const r = SN.calcular({mensual: s * aMes[tipo], zona: $('zona').value, imss: $('imss').checked});
    const div = 1 / aMes[tipo];
    $('rt').textContent = tipo === 'mensual' ? 'Te llega al mes' : tipo === 'quincenal' ? 'Te llega por quincena' : 'Te llega por semana';
    $('neto').textContent = MXN.format(r.neto * div);
    $('rsub').textContent = `Equivale a ${MXN.format(r.neto)} al mes`;
    for (const [id, v] of [['bruto', r.bruto], ['isrc', r.isrCausado], ['sub', r.subsidio], ['isr', r.isr], ['imssv', r.imss], ['neto2', r.neto]]) $(id).textContent = MXN.format(v * div);
    const av = [];
    if (r.minimo) av.push('Con salario mínimo no te retienen ISR y tu cuota del IMSS la paga el patrón.');
    else av.push(`Te descuentan el ${r.tasa.toFixed(1)} % de tu sueldo.`);
    if (!r.minimo && r.bruto > 11492.66 && r.bruto < 12500) av.push('Pasaste por poco el límite del subsidio para el empleo ($11,492.66 al mes).');
    $('aviso').textContent = av.join(' ');
    try { localStorage.setItem(CLAVE, JSON.stringify({tipo, s: $('sueldo').value, z: $('zona').value, i: $('imss').checked})); } catch (e) {}
  }
  try { const g = JSON.parse(localStorage.getItem(CLAVE) || 'null'); if (g) { f.tipo.value = g.tipo; $('sueldo').value = g.s; $('zona').value = g.z; $('imss').checked = g.i; } } catch (e) {}
  f.addEventListener('input', pintar); f.addEventListener('change', pintar); f.addEventListener('submit', e => e.preventDefault());
  pintar();
}
</script>''',
       extra_head=faq_ld(faq))

# ---------------------------------------------------------------- Vacaciones
filas = ''.join(f'<tr><td>{a}</td><td class="n">{d} días</td></tr>' for a, d in
                [('1 año', 12), ('2 años', 14), ('3 años', 16), ('4 años', 18), ('5 años', 20), ('6 a 10 años', 22),
                 ('11 a 15 años', 24), ('16 a 20 años', 26), ('21 a 25 años', 28), ('26 a 30 años', 30), ('31 a 35 años', 32)])
faq = [
    ("¿Cuándo tengo que tomar mis vacaciones?", "Dentro de los seis meses siguientes a que cumples cada año de trabajo. Al menos 12 días deben ser seguidos, si tú lo pides."),
    ("¿Me pueden pagar las vacaciones en lugar de tomarlas?", "No mientras sigas trabajando: la ley prohíbe cambiarlas por dinero. Solo se pagan si terminas tu relación laboral antes de tomarlas."),
    ("¿Cuánto es la prima vacacional?", "Mínimo el 25 % del salario de tus días de vacaciones. Tu contrato puede darte más."),
]
pagina('calculadora-vacaciones.html',
       'Calculadora de vacaciones y prima vacacional 2026',
       'Cuántos días de vacaciones te tocan por ley según tu antigüedad y cuánto te deben pagar de prima vacacional. Tabla de Vacaciones Dignas 2026.',
       'Calculadora de vacaciones y prima vacacional',
       'Pon tu fecha de ingreso y tu sueldo: te decimos cuántos días te tocan y cuánto es tu prima vacacional.',
       f'''    <section class="band calc">
      <form id="f" novalidate>
        <div class="field">
          <label for="ingreso">Fecha en que entraste a trabajar</label>
          <input id="ingreso" type="date" value="2022-08-15">
        </div>
        <div class="field">
          <label for="sueldo">Sueldo mensual bruto</label>
          <input id="sueldo" type="number" inputmode="decimal" min="0" step="any" value="12000">
        </div>
        <div class="field">
          <label for="prima">Prima vacacional (%)</label>
          <input id="prima" type="number" inputmode="numeric" min="25" step="1" value="25">
          <span class="hint">La ley marca mínimo 25 %.</span>
        </div>
      </form>
      <aside class="result" aria-live="polite">
        <div style="font-weight:600">Vacaciones que te tocan</div>
        <div class="big" id="dias">0 días</div>
        <div id="rsub"></div>
        <ul class="lines">
          <li><span>Años cumplidos</span><b id="anios">0</b></li>
          <li><span>Pago de tus días de vacaciones</span><b id="pago">$0</b></li>
          <li><span>Prima vacacional</span><b id="primav">$0</b></li>
          <li><span>Próximo aniversario</span><b id="aniv">—</b></li>
          <li class="total"><span>Días en tu siguiente año</span><b id="sig">0</b></li>
        </ul>
        <p class="note" id="aviso"></p>
      </aside>
    </section>
{AD}
    <section class="band prose">
      <h2>Tabla de vacaciones 2026 por antigüedad</h2>
      <p>Desde la reforma conocida como Vacaciones Dignas (artículo 76 de la Ley Federal del Trabajo), el primer año te tocan 12 días, y suben dos por año hasta llegar a 20 en el quinto. A partir del sexto año aumentan dos días cada cinco años.</p>
      <div class="scroll"><table><thead><tr><th>Años cumplidos</th><th class="n">Días de vacaciones</th></tr></thead><tbody>{filas}</tbody></table></div>
      <h2>Cómo se calcula la prima vacacional</h2>
      <p>Multiplica tu salario diario por los días de vacaciones y luego por 25 %. Con un sueldo de $12,000 al mes (salario diario de $400) y 16 días de vacaciones: $400 × 16 = $6,400 de vacaciones pagadas, y la prima es $6,400 × 25 % = <strong>$1,600</strong>.</p>
      <h2>Preguntas frecuentes</h2>
{faq_html(faq)}
      <p class="meta">Artículos 76, 78, 79 y 80 de la Ley Federal del Trabajo. Resultado informativo.</p>
    </section>
{AD}''',
       scripts='''<script src="assets/finiquito.js"></script>
<script>
{
  const $ = id => document.getElementById(id);
  const f = $('f'), CLAVE = 'pad-vacaciones';
  const FC = new Intl.DateTimeFormat('es-MX', {day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC'});
  function pintar() {
    const ini = FQ.fecha($('ingreso').value), sd = (+$('sueldo').value || 0) / 30, pr = Math.max(25, +$('prima').value || 25) / 100;
    const hoy = new Date(); const t = Date.UTC(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());
    if (!ini || ini > t) { $('dias').textContent = '—'; $('aviso').textContent = 'Revisa tu fecha de ingreso.'; return; }
    const d0 = new Date(ini);
    let comp = new Date(t).getUTCFullYear() - d0.getUTCFullYear();
    if (Date.UTC(new Date(t).getUTCFullYear(), d0.getUTCMonth(), d0.getUTCDate()) > t) comp--;
    const prox = Date.UTC(d0.getUTCFullYear() + comp + 1, d0.getUTCMonth(), d0.getUTCDate());
    const dias = comp >= 1 ? FQ.diasVacaciones(comp) : 0;
    $('dias').textContent = dias + ' días';
    $('rsub').textContent = comp >= 1 ? `por tu año ${comp} de trabajo` : 'Aún no cumples tu primer año';
    $('anios').textContent = comp;
    $('pago').textContent = MXN.format(sd * dias);
    $('primav').textContent = MXN.format(sd * dias * pr);
    $('aniv').textContent = FC.format(new Date(prox));
    $('sig').textContent = FQ.diasVacaciones(comp + 1) + ' días';
    $('aviso').textContent = comp >= 1 ? 'Debes poder tomarlas dentro de los 6 meses siguientes a tu aniversario.' : 'Al cumplir tu primer año te tocarán 12 días. Si te vas antes, se pagan proporcionales en tu finiquito.';
    try { localStorage.setItem(CLAVE, JSON.stringify({i: $('ingreso').value, s: $('sueldo').value, p: $('prima').value})); } catch (e) {}
  }
  try { const g = JSON.parse(localStorage.getItem(CLAVE) || 'null'); if (g) { $('ingreso').value = g.i; $('sueldo').value = g.s; $('prima').value = g.p; } } catch (e) {}
  f.addEventListener('input', pintar); f.addEventListener('submit', e => e.preventDefault());
  pintar();
}
</script>''',
       extra_head=faq_ld(faq))

# ---------------------------------------------------------------- Euro hoy
pagina('euro-hoy.html',
       'Precio del euro hoy en pesos mexicanos (Banxico)',
       'Tipo de cambio del euro hoy en pesos mexicanos según el Banco de México, con historial y convertidor de euros a pesos.',
       'Precio del euro hoy en México',
       'Tipo de cambio del euro en pesos que publica el Banco de México cada día hábil.',
       '''    <section class="band hero-grid" aria-live="polite">
      <div>
        <div class="big" id="fx" style="color:var(--ink)">—<small>pesos</small></div>
        <span class="chip" id="chg" style="background:var(--panel)">Cargando…</span>
        <p class="meta" id="fxdate"></p>
      </div>
      <div class="box">
        <div style="font-weight:600" id="rango">Últimos días hábiles</div>
        <div class="fig"><svg id="chart" role="img" aria-label="Gráfica del tipo de cambio peso-euro"></svg></div>
      </div>
    </section>
    <section class="band">
      <h2>Convertir euros a pesos</h2>
      <div class="box conv">
        <div class="field" style="margin:0"><label for="eur">Euros (EUR)</label><input id="eur" type="number" inputmode="decimal" min="0" step="any" value="100"></div>
        <div class="eq" aria-hidden="true">=</div>
        <div class="field" style="margin:0"><label for="mxn">Pesos (MXN)</label><input id="mxn" type="number" inputmode="decimal" min="0" step="any"></div>
      </div>
    </section>
''' + AD + '''
    <section class="band prose">
      <h2>De dónde sale el tipo de cambio del euro</h2>
      <p>El Banco de México publica cada día hábil el valor del euro en pesos. Lo calcula con el tipo de cambio FIX del dólar y la equivalencia del euro frente al dólar que da a conocer el Fondo Monetario Internacional. Es una referencia oficial: en bancos y casas de cambio el precio de venta será más alto.</p>
      <p>¿Buscas el dólar? Consulta el <a href="dolar-hoy.html">precio del dólar hoy</a>.</p>
      <p class="meta">Fuente: Banco de México, tipos de cambio respecto a otras divisas.</p>
    </section>''',
       scripts='''<script>
{
  const $ = id => document.getElementById(id);
  let tc = 0; const r2 = v => Math.round(v * 100) / 100;
  $('eur').addEventListener('input', () => { if (tc) $('mxn').value = $('eur').value === '' ? '' : r2($('eur').value * tc); });
  $('mxn').addEventListener('input', () => { if (tc) $('eur').value = $('mxn').value === '' ? '' : r2($('mxn').value / tc); });
  fetch('data/euro.json', {cache: 'no-cache'}).then(r => { if (!r.ok) throw 0; return r.json(); }).then(j => {
    const datos = (j.datos || []).filter(d => typeof d.valor === 'number').sort((a, b) => a.fecha.localeCompare(b.fecha));
    if (!datos.length) throw 0;
    const c = cambio(datos); tc = c.hoy.valor;
    $('fx').firstChild.textContent = NUM4.format(tc);
    chipCambio($('chg'), c);
    $('fxdate').textContent = 'Pesos por euro · ' + FECHA.format(aFecha(c.hoy.fecha));
    const ult = datos.slice(-60); $('rango').textContent = `Últimos ${ult.length} días hábiles`;
    graficaLinea($('chart'), ult);
    $('mxn').value = r2($('eur').value * tc);
  }).catch(() => { $('chg').textContent = 'Estamos actualizando este dato. Vuelve más tarde.'; });
}
</script>''')

# ---------------------------------------------------------------- Salario mínimo 2026
faq = [
    ("¿Cuánto es el salario mínimo 2026 al mes?", "En la zona general, $315.04 diarios equivalen a unos $9,577 al mes (multiplicando por 30.4 días). En la Zona Libre de la Frontera Norte, $440.87 diarios son unos $13,402 al mes."),
    ("¿Al salario mínimo le quitan impuestos?", "No. A quien gana solo el salario mínimo no se le retiene ISR, y su cuota del IMSS la paga el patrón."),
]
pagina('salario-minimo-2026.html',
       'Salario mínimo 2026 en México: diario, mensual y por zona',
       'Cuánto es el salario mínimo 2026 en México: $315.04 diarios en la zona general y $440.87 en la frontera norte, con equivalencias por semana, quincena y mes.',
       'Salario mínimo 2026 en México',
       'Montos oficiales de la CONASAMI vigentes desde el 1 de enero de 2026, con su equivalente por semana, quincena y mes.',
       f'''    <section class="band">
      <div class="tools">
        <div class="tool"><b>Zona general</b><span>Casi todo el país</span><em>$315.04 al día</em></div>
        <div class="tool"><b>Zona Libre de la Frontera Norte</b><span>Municipios de la franja fronteriza</span><em>$440.87 al día</em></div>
      </div>
    </section>
    <section class="band prose">
      <h2>Equivalencias del salario mínimo 2026</h2>
      <div class="scroll"><table>
        <thead><tr><th>Periodo</th><th class="n">Zona general</th><th class="n">Frontera norte</th></tr></thead>
        <tbody>
          <tr><td>Diario</td><td class="n">$315.04</td><td class="n">$440.87</td></tr>
          <tr><td>Semanal (7 días)</td><td class="n">$2,205.28</td><td class="n">$3,086.09</td></tr>
          <tr><td>Quincenal (15.2 días)</td><td class="n">$4,788.61</td><td class="n">$6,701.22</td></tr>
          <tr><td>Mensual (30.4 días)</td><td class="n">$9,577.22</td><td class="n">$13,402.45</td></tr>
        </tbody>
      </table></div>
      <p>El salario mensual se calcula multiplicando el diario por 30.4, que es el promedio de días de un mes. Así lo hacen el SAT y la mayoría de los patrones.</p>
{AD}
      <h2>Qué cambió en 2026</h2>
      <p>El salario mínimo general subió 13 %, de $278.80 a $315.04 diarios. En la frontera norte subió 5 %, de $419.88 a $440.87. Los nuevos montos rigen desde el 1 de enero de 2026.</p>
      <h2>Qué se calcula con el salario mínimo</h2>
      <p>Con el salario mínimo se define quién no paga ISR, el tope de la prima de antigüedad (dos salarios mínimos al día) y el monto mínimo de prestaciones como el aguinaldo. Para multas, créditos y exenciones de impuestos se usa la <a href="uma-2026.html">UMA</a>, que es otra cifra.</p>
      <p>Calcula con estos montos tu <a href="calculadora-aguinaldo.html">aguinaldo</a>, tu <a href="calculadora-finiquito.html">finiquito</a> o tu <a href="calculadora-sueldo-neto.html">sueldo neto</a>.</p>
      <h2>Preguntas frecuentes</h2>
{faq_html(faq)}
      <p class="meta">Fuente: Comisión Nacional de los Salarios Mínimos (CONASAMI), resolución publicada en el DOF para 2026.</p>
    </section>''',
       extra_head=faq_ld(faq))

# ---------------------------------------------------------------- UMA 2026
faq = [
    ("¿Cuánto vale la UMA en 2026?", "$117.31 diarios, $3,566.22 mensuales y $42,794.64 anuales, vigentes del 1 de febrero de 2026 al 31 de enero de 2027."),
    ("¿Cuál es la diferencia entre UMA y salario mínimo?", "El salario mínimo es lo menos que se puede pagar por un día de trabajo. La UMA es una unidad de referencia para calcular multas, créditos, exenciones de impuestos y otras obligaciones."),
]
pagina('uma-2026.html',
       'UMA 2026: valor diario, mensual y anual y convertidor a pesos',
       'Valor de la UMA 2026: $117.31 diarios, $3,566.22 mensuales y $42,794.64 anuales. Convierte UMAs a pesos y conoce para qué se usa.',
       'UMA 2026: valor y convertidor a pesos',
       'Valores oficiales del INEGI vigentes desde el 1 de febrero de 2026, y un convertidor de UMAs a pesos.',
       f'''    <section class="band calc">
      <form id="f" novalidate>
        <div class="field">
          <label for="n">Cantidad de UMAs</label>
          <input id="n" type="number" inputmode="decimal" min="0" step="any" value="30">
          <span class="hint">Por ejemplo, una multa de 20 UMA o la exención de 30 UMA del aguinaldo.</span>
        </div>
      </form>
      <aside class="result" aria-live="polite">
        <div style="font-weight:600">Equivale a</div>
        <div class="big" id="pesos">$0</div>
        <div>con la UMA diaria de $117.31</div>
      </aside>
    </section>
{AD}
    <section class="band prose">
      <h2>Valor de la UMA 2026</h2>
      <div class="scroll"><table>
        <thead><tr><th>Periodo</th><th class="n">2025</th><th class="n">2026</th></tr></thead>
        <tbody>
          <tr><td>Diario</td><td class="n">$113.14</td><td class="n">$117.31</td></tr>
          <tr><td>Mensual</td><td class="n">$3,439.46</td><td class="n">$3,566.22</td></tr>
          <tr><td>Anual</td><td class="n">$41,273.52</td><td class="n">$42,794.64</td></tr>
        </tbody>
      </table></div>
      <p>La UMA subió 3.69 %, igual que la inflación anual de diciembre de 2025. Los valores de 2026 rigen del 1 de febrero de 2026 al 31 de enero de 2027; en enero se usa todavía la del año anterior.</p>
      <h2>Para qué se usa la UMA</h2>
      <p>Desde 2016 la UMA sustituyó al salario mínimo como referencia para calcular multas de tránsito, trámites, créditos de Infonavit y los montos exentos de impuestos. Algunos ejemplos de 2026:</p>
      <div class="scroll"><table>
        <thead><tr><th>Concepto</th><th>Regla</th><th class="n">Monto 2026</th></tr></thead>
        <tbody>
          <tr><td>Aguinaldo exento de ISR</td><td>30 UMA</td><td class="n">$3,519.30</td></tr>
          <tr><td>Prima vacacional exenta</td><td>15 UMA</td><td class="n">$1,759.65</td></tr>
          <tr><td>Indemnización exenta por año trabajado</td><td>90 UMA</td><td class="n">$10,557.90</td></tr>
          <tr><td>Subsidio para el empleo mensual</td><td>15.02 % de la UMA mensual</td><td class="n">$535.65</td></tr>
        </tbody>
      </table></div>
      <h2>Preguntas frecuentes</h2>
{faq_html(faq)}
      <p class="meta">Fuente: INEGI, valores de la UMA publicados en el DOF el 9 de enero de 2026.</p>
    </section>''',
       scripts='''<script>
{
  const n = document.getElementById('n'), out = document.getElementById('pesos');
  const pintar = () => { out.textContent = MXN.format((+n.value || 0) * 117.31); };
  n.addEventListener('input', pintar); document.getElementById('f').addEventListener('submit', e => e.preventDefault()); pintar();
}
</script>''',
       extra_head=faq_ld(faq))

# ---------------------------------------------------------------- Días festivos 2027
festivos = [
    ('Viernes 1 de enero de 2027', 'Año Nuevo', 'I'),
    ('Lunes 1 de febrero de 2027', 'Conmemoración del 5 de febrero (Constitución)', 'II'),
    ('Lunes 15 de marzo de 2027', 'Conmemoración del 21 de marzo (Benito Juárez)', 'III'),
    ('Sábado 1 de mayo de 2027', 'Día del Trabajo', 'IV'),
    ('Jueves 16 de septiembre de 2027', 'Independencia de México', 'V'),
    ('Lunes 15 de noviembre de 2027', 'Conmemoración del 20 de noviembre (Revolución)', 'VI'),
    ('Sábado 25 de diciembre de 2027', 'Navidad', 'VIII'),
]
filas = ''.join(f'<tr><td>{d}</td><td>{m}</td><td class="n">{fr}</td></tr>' for d, m, fr in festivos)
faq = [
    ("¿Cuánto me pagan si trabajo un día festivo?", "Tu salario normal más un salario doble adicional por el día trabajado; es decir, tres veces tu salario diario (artículo 75 de la LFT)."),
    ("¿El 2 de noviembre o el 12 de diciembre son días de descanso obligatorio?", "No. Son fechas importantes, pero no están en el artículo 74 de la Ley Federal del Trabajo. Descansar depende de tu patrón o tu contrato."),
    ("¿Si el festivo cae en sábado se recorre?", "No. La ley solo recorre al lunes las conmemoraciones del 5 de febrero, 21 de marzo y 20 de noviembre."),
]
pagina('dias-festivos-2027.html',
       'Días festivos 2027 en México: descansos obligatorios y puentes',
       'Calendario de días de descanso obligatorio 2027 en México según el artículo 74 de la LFT, puentes y cuánto te deben pagar si trabajas un festivo.',
       'Días festivos 2027 en México',
       'Los días de descanso obligatorio que marca la Ley Federal del Trabajo para 2027, los puentes y cuánto te pagan si trabajas.',
       f'''    <section class="band prose">
      <h2>Días de descanso obligatorio 2027</h2>
      <div class="scroll"><table class="stack">
        <thead><tr><th>Fecha</th><th>Motivo</th><th class="n">Fracción art. 74</th></tr></thead>
        <tbody>{filas}</tbody>
      </table></div>
      <p>Además, cuando hay elecciones ordinarias también es descanso obligatorio el día de la jornada electoral que fijen las leyes electorales (fracción IX). El 1 de octubre solo aplica cuando hay cambio de presidente; el siguiente es en 2030.</p>
      <h2>Puentes de 2027</h2>
      <p>Hay tres fines de semana largos: del 30 de enero al 1 de febrero, del 13 al 15 de marzo y del 13 al 15 de noviembre. El 16 de septiembre cae en jueves, así que algunos patrones dan el viernes, aunque la ley no lo obliga. El 1 de mayo y el 25 de diciembre caen en sábado.</p>
{AD}
      <h2>Lo que queda de 2026</h2>
      <p>Del calendario de 2026 solo falta el <strong>viernes 25 de diciembre</strong> (Navidad).</p>
      <h2>Cuánto te pagan si trabajas un día festivo</h2>
      <p>Si te toca trabajar un día de descanso obligatorio, tu patrón debe pagarte tu salario de ese día más un salario doble adicional: en total, el triple. Con un salario diario de $400, trabajar el 1 de enero te deja $1,200 por ese día.</p>
      <h2>Preguntas frecuentes</h2>
{faq_html(faq)}
      <p class="meta">Fuente: artículos 74 y 75 de la Ley Federal del Trabajo.</p>
    </section>''',
       extra_head=faq_ld(faq))

# ---------------------------------------------------------------- Términos de uso
pagina('terminos.html',
       'Términos de uso | Peso al Día',
       'Condiciones de uso del sitio Peso al Día, alcance de las calculadoras y responsabilidad sobre la información.',
       'Términos de uso',
       'Última actualización: 26 de noviembre de 2026.',
       '''    <section class="band prose">
      <h2>Uso del sitio</h2>
      <p>Al usar Peso al Día aceptas estos términos. El sitio es gratuito y ofrece datos públicos y calculadoras con fines informativos y educativos.</p>
      <h2>La información no es asesoría</h2>
      <p>Los resultados de las calculadoras son estimaciones hechas con la ley y los valores oficiales vigentes, pero no consideran todos los casos posibles (contratos especiales, prestaciones adicionales, sentencias o cambios de ley). No sustituyen la asesoría de un contador, abogado laboral o asesor financiero. Antes de tomar una decisión importante, verifica la información con un profesional o con la autoridad correspondiente.</p>
      <h2>Exactitud de los datos</h2>
      <p>El tipo de cambio se obtiene automáticamente del Banco de México y puede tardar en actualizarse o fallar temporalmente. Hacemos lo posible por mantener todo correcto y al día, pero no garantizamos que la información esté libre de errores. Si encuentras uno, escríbenos desde la página de <a href="acerca.html">contacto</a>.</p>
      <h2>Publicidad y enlaces</h2>
      <p>El sitio se financia con anuncios de terceros, como Google AdSense. No respaldamos los productos anunciados. Los enlaces a otros sitios se ofrecen por comodidad y no somos responsables de su contenido.</p>
      <h2>Propiedad del contenido</h2>
      <p>Los textos, diseño y código de las calculadoras son propiedad de Peso al Día. Puedes compartir enlaces libremente; para reproducir el contenido pide autorización.</p>
      <h2>Cambios</h2>
      <p>Podemos actualizar estos términos. La versión vigente siempre estará en esta página.</p>
    </section>''')

# ---------------------------------------------------------------- 404
pagina('404.html',
       'Página no encontrada | Peso al Día',
       'La página que buscas no existe.',
       'No encontramos esa página',
       'Puede que el enlace esté mal escrito o que la página haya cambiado de lugar.',
       '''    <section class="band">
      <div class="row">
        <a class="btn main" href="./">Ir al inicio</a>
        <a class="btn alt" href="dolar-hoy.html">Ver el dólar hoy</a>
      </div>
    </section>''')

# ---------------------------------------------------------------- Menú y pie en las páginas existentes
for p in glob.glob('*.html'):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<nav class="nav" aria-label="Principal">.*?</nav>', NAV, s, flags=re.S)
    s = re.sub(r'<footer>.*?</footer>', FOOTER, s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)
print('ok')
