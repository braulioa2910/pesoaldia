/* Cálculo de finiquito y liquidación 2026 (México, Ley Federal del Trabajo)
   - Vacaciones (art. 76, Vacaciones Dignas): 12,14,16,18,20; luego +2 cada 5 años.
   - Prima vacacional (art. 80): mínimo 25 %.
   - Aguinaldo (art. 87): mínimo 15 días, proporcional al año de la baja.
   - Prima de antigüedad (art. 162, 485, 486): 12 días por año; salario base entre
     1 y 2 salarios mínimos. En renuncia solo con 15 años o más; en despido siempre.
   - Despido injustificado (art. 48, 50): 90 días de salario diario integrado (SDI)
     y, cuando aplica, 20 días de SDI por año de servicio. */
const FQ = {
  salarioMinimo: {general: 315.04, frontera: 440.87},
  diasVacaciones(anioServicio) {
    const n = Math.max(1, Math.floor(anioServicio));
    if (n <= 5) return 10 + 2 * n;
    return 22 + 2 * Math.floor((n - 6) / 5);
  },
  dias(a, b) { return Math.round((b - a) / 864e5); },
  fecha(s) { const t = new Date(s + 'T00:00:00Z').getTime(); return isNaN(t) ? null : t; },
  calcular(o) {
    const sd = Math.max(0, +o.salarioDiario || 0);
    const ini = FQ.fecha(o.ingreso), fin = FQ.fecha(o.salida);
    if (!ini || !fin || fin < ini || sd <= 0) return null;
    const zona = o.zona === 'frontera' ? 'frontera' : 'general';
    const sm = FQ.salarioMinimo[zona];
    const dAg = Math.max(15, +o.diasAguinaldo || 15);
    const pPrima = Math.max(25, +o.primaVacacional || 25) / 100;

    // Antigüedad: días totales (contando el día de salida) y años completos
    const diasTotales = FQ.dias(ini, fin) + 1;
    const anios = diasTotales / 365;
    const d0 = new Date(ini), df = new Date(fin);
    let completos = df.getUTCFullYear() - d0.getUTCFullYear();
    const aniv = Date.UTC(df.getUTCFullYear(), d0.getUTCMonth(), d0.getUTCDate());
    if (aniv > fin) completos--;
    const ultimoAniv = Date.UTC(d0.getUTCFullYear() + completos, d0.getUTCMonth(), d0.getUTCDate());
    const diasDesdeAniv = FQ.dias(ultimoAniv, fin) + 1;

    // Vacaciones del año de servicio en curso (proporcionales) + pendientes
    const vacAnio = FQ.diasVacaciones(completos + 1);
    const vacProp = vacAnio * Math.min(diasDesdeAniv, 365) / 365;
    const vacPend = Math.max(0, +o.vacacionesPendientes || 0);
    const vacDias = vacProp + vacPend;

    // Aguinaldo proporcional del año calendario de la baja
    const ene1 = Date.UTC(df.getUTCFullYear(), 0, 1);
    const diasAnioAg = FQ.dias(Math.max(ene1, ini), fin) + 1;
    const diasAnio = FQ.dias(ene1, Date.UTC(df.getUTCFullYear() + 1, 0, 1));

    const c = {};
    c.salarioPendiente = sd * Math.max(0, +o.diasPendientes || 0);
    c.aguinaldo = sd * dAg * diasAnioAg / diasAnio;
    c.vacaciones = sd * vacDias;
    c.primaVacacional = c.vacaciones * pPrima;

    const despido = o.motivo === 'despido';
    const baseAnt = Math.min(Math.max(sd, sm), 2 * sm);
    const tienePrimaAnt = despido || anios >= 15;
    c.primaAntiguedad = tienePrimaAnt ? baseAnt * 12 * anios : 0;

    const sdi = sd * (1 + dAg / 365 + vacAnio * pPrima / 365);
    c.indemnizacion90 = despido ? sdi * 90 : 0;
    c.indemnizacion20 = despido && o.veinteDias ? sdi * 20 * anios : 0;

    const finiquito = c.salarioPendiente + c.aguinaldo + c.vacaciones + c.primaVacacional;
    const total = finiquito + c.primaAntiguedad + c.indemnizacion90 + c.indemnizacion20;
    return {c, finiquito, total, sdi, anios, completos, diasTotales, vacAnio, vacProp, vacDias,
      diasAnioAg, diasAnio, baseAnt, tienePrimaAnt, despido, sm};
  }
};
if (typeof module !== 'undefined') module.exports = FQ;
