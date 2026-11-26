/* Sueldo neto mensual 2026 (México)
   - ISR: tarifa mensual art. 96 LISR (Anexo 8 RMF 2026), usa la misma tabla que AG.
   - Subsidio para el empleo 2026 (DOF 31/12/2025): 15.02 % de la UMA mensual = $535.65
     para ingresos de hasta $11,492.66 al mes; no puede ser mayor que el ISR del mes.
   - Sin retención de ISR para quien gana el salario mínimo (art. 96 LISR).
   - IMSS (cuota del trabajador, estimada): 0.25 % prestaciones en dinero, 0.375 % gastos
     médicos de pensionados, 0.625 % invalidez y vida, 1.125 % cesantía y vejez sobre el
     salario base de cotización (SBC), más 0.40 % sobre lo que pase de 3 UMA.
     Si gana el salario mínimo, esa cuota la paga el patrón (art. 36 LSS). */
const SN = {
  umaDiaria: 117.31,
  subsidio: 535.65,
  limiteSubsidio: 11492.66,
  factorIntegracion: 1 + 15 / 365 + 12 * 0.25 / 365,
  calcular({mensual, zona = 'general', imss = true}) {
    const bruto = Math.max(0, +mensual || 0);
    const sd = bruto / 30.4;
    const sm = AG.salarioMinimo[zona];
    const minimo = sd <= sm + 0.005;
    const isrCausado = AG.isrMensual(bruto);
    const subsidio = bruto <= SN.limiteSubsidio ? Math.min(SN.subsidio, isrCausado) : 0;
    const isr = minimo ? 0 : Math.max(0, isrCausado - subsidio);
    let cuotaImss = 0;
    if (imss && !minimo && bruto > 0) {
      const sbc = Math.min(sd * SN.factorIntegracion, 25 * SN.umaDiaria);
      const excedente = Math.max(0, sbc - 3 * SN.umaDiaria);
      cuotaImss = (sbc * 0.02375 + excedente * 0.004) * 30.4;
    }
    const neto = bruto - isr - cuotaImss;
    return {bruto, isrCausado, subsidio: minimo ? 0 : subsidio, isr, imss: cuotaImss, neto, minimo,
      tasa: bruto ? (isr + cuotaImss) / bruto * 100 : 0};
  }
};
if (typeof module !== 'undefined') module.exports = SN;
