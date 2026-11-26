/* Cálculo de aguinaldo 2026 (México)
   - LFT art. 87: mínimo 15 días de salario; proporcional si no se trabajó el año completo.
   - LISR art. 93 fr. XIV: exento hasta 30 UMA (UMA diaria 2026 = $117.31 → $3,519.30).
   - ISR estimado con la tarifa mensual del art. 96 (Anexo 8 RMF 2026):
     ISR(sueldo mensual + parte gravada) − ISR(sueldo mensual).
   - Art. 96: no hay retención a quien gana solo el salario mínimo. */
const AG = {
  anio: 2026,
  uma: 117.31,
  salarioMinimo: {general: 315.04, frontera: 440.87},
  tarifa: [ // límite inferior, cuota fija, % sobre excedente
    [0.01, 0, 1.92], [844.60, 16.22, 6.40], [7168.52, 420.95, 10.88],
    [12598.03, 1011.68, 16.00], [14644.65, 1339.14, 17.92], [17533.65, 1856.84, 21.36],
    [35362.84, 5665.16, 23.52], [55736.69, 10457.09, 30.00], [106410.51, 25659.23, 32.00],
    [141880.67, 37009.69, 34.00], [425642.00, 133488.54, 35.00]
  ],
  isrMensual(base) {
    if (base <= 0) return 0;
    let fila = AG.tarifa[0];
    for (const f of AG.tarifa) if (base >= f[0]) fila = f;
    return fila[1] + (base - fila[0]) * fila[2] / 100;
  },
  diasTrabajados(fechaIngreso, anio = AG.anio) {
    const inicio = Date.UTC(anio, 0, 1), fin = Date.UTC(anio, 11, 31);
    const diasAnio = Math.round((fin - inicio) / 864e5) + 1;
    if (!fechaIngreso) return {dias: diasAnio, diasAnio};
    const f = new Date(fechaIngreso + 'T00:00:00Z').getTime();
    if (isNaN(f) || f <= inicio) return {dias: diasAnio, diasAnio};
    if (f > fin) return {dias: 0, diasAnio};
    return {dias: Math.round((fin - f) / 864e5) + 1, diasAnio};
  },
  calcular({salarioDiario, diasAguinaldo = 15, fechaIngreso = '', zona = 'general'}) {
    const sd = Math.max(0, +salarioDiario || 0);
    const dAg = Math.max(15, +diasAguinaldo || 15);
    const {dias, diasAnio} = AG.diasTrabajados(fechaIngreso);
    const bruto = sd * dAg * dias / diasAnio;
    const topeExento = 30 * AG.uma;
    const exento = Math.min(bruto, topeExento);
    const gravado = Math.max(0, bruto - topeExento);
    const mensual = sd * 30.4;
    const minimo = sd <= AG.salarioMinimo[zona] + 0.005;
    const isr = (minimo || gravado === 0) ? 0 : AG.isrMensual(mensual + gravado) - AG.isrMensual(mensual);
    return {bruto, exento, gravado, isr, neto: bruto - isr, dias, diasAnio, dAg, minimo, topeExento};
  }
};
if (typeof module !== 'undefined') module.exports = AG;
