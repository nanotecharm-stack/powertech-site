# Final English GRIDEC report (2026-11-22): the owner's revised English master
# (GRIDEC_EN_HY_checked_texts_for_Claude.zip → GRIDEC_EN_revised_text.md) in the same layout.
#
# EDITABLE SOURCE. All report text is in PAGES below, page by page. Layout code lives in gen_hy_final.py.
# Numbers, formulas and terms are the owner's; do not change them here without the owner.
# Markup in strings: **bold**, U_A / U_B → subscript, "ΔU…" is set in the mono font.
#
# Run:     python clean_figs_hy.py && sh make_pdf_final.sh
# Output:  out/GRIDEC_Demonstration_Report_EN_FINAL.pdf (and out/report-en-final.html)
import gen_hy_final as g
from gen_hy_final import DU, G1, C1, G2, C2

FOOT = 'GRIDEC / ENGINEERING EXAMPLE / MODELLED DATA'

LEG_U = [('line', G1, 'A / main switchboard'), ('line', C1, 'B / inverter'),
         ('dash', '#8A8A8A', 'U = 253 V (assumed threshold)')]

PAGES = [
    # ── 01 ────────────────────────────────────────────────────────────────────────────
    dict(head='TECHNICAL REPORT', cover=True, blocks=[
        ('kick', 'MODELLED DATA / DEMONSTRATION ONLY'),
        ('h1', 'Repeated PV inverter trips'),
        ('sub', 'Seven-day illustrative power-quality investigation / heavy-equipment repair workshop'),
        ('facts', [
            ('SITE', 'Heavy-equipment repair workshop (fictional)'),
            ('PERIOD', '8–14 June 2026 / UTC+04:00'),
            ('SOLAR PV PLANT', '100 kW AC / 125 kWp DC'),
            ('ELECTRICAL SYSTEM', '400/230 V / 50 Hz / TN-S (assumed in the model)')]),
        ('lbl', 'KEY FIGURES'),
        ('kpi', [
            ('INVERTER TRIPS', '8'),
            ('TOTAL TIME DISCONNECTED', '51 min 10 s'),
            ('HIGHEST 20 ms RMS VOLTAGE', '255.3 V'),
            ('VOLTAGE RISE, ' + DU, '10.8–12.3 V')]),
        ('find', 'Principal finding', [
            'The seven-day simulation produced eight inverter trips. Before each trip, the L2–N voltage at point B (the inverter AC terminals) exceeded the model\'s assumed 253 V threshold. The highest 20 ms RMS voltage at B was 255.3 V. Immediately before the trips, voltage at B was 10.8–12.3 V higher than at point A (the main distribution switchboard).',
            'In the model, most of this difference is attributable to the resistance of the 185 m cable between A and B. A further brief rise in voltage at A pushes the voltage at B above the assumed inverter protection threshold. The ten-minute voltage values at A remain within the indicative 207–253 V range. This does not constitute an assessment of network compliance.']),
        ('warn', '**IMPORTANT.** The demonstration uses a fictional trip rule: the inverter disconnects when L2–N voltage at B stays above 253 V for approximately 2.1 s. No actual inverter model, approved grid-connection settings or manufacturer-verified fault code are specified. These must be checked in any real installation.')]),

    # ── 02 ────────────────────────────────────────────────────────────────────────────
    dict(head='01 / INSTALLATION', blocks=[
        ('h1', 'Installation and measurement points'),
        ('factsb', [
            ('POINT A / MAIN DISTRIBUTION SWITCHBOARD', 'Point A is used to assess conditions within the workshop\'s electrical installation. It is not a documented point of supply or boundary of responsibility between the network operator and the customer. The workshop\'s electrical loads are connected to this switchboard. In the model\'s energy balance, grid imports and exports at A refer to the grid-side connection of the switchboard, not the PV feeder.'),
            ('POINT B / SOLAR PV INVERTER', 'Point B is at the inverter\'s AC terminals. The following active-power sign convention is used in the model: inverter output at B is positive, and power imported from the grid at A is positive. Power exported to the grid at A has the opposite sign.'),
            ('PV CABLE RUN', 'Aluminium cable, 4 × 70 mm² (L1/L2/L3/N), length 185 m. A separate copper protective earth (PE) conductor is included in the model. Its cross-sectional area and installation route are not specified; both must be checked for a real installation.'),
            ('ASSUMED CONDUCTOR RESISTANCE', 'R = 0.095 Ω per phase conductor at approximately 60 °C. This is an assumed value used in the calculation, not an on-site resistance measurement.')]),
        ('lbl', 'SIMPLIFIED SINGLE-LINE DIAGRAM / NOT AN INSTALLATION DRAWING'),
        ('diagram', dict(grid='GRID', a='A', b='B', sw='MAIN DISTRIBUTION SWITCHBOARD', inv='SOLAR PV INVERTER',
                         cable='Al 4 × 70 mm² / 185 m', loads='WORKSHOP LOADS',
                         pe1='SEPARATE PE CONDUCTOR /', pe2='VERIFY SIZE AND ROUTING')),
        ('p', 'Electrical power flows from the inverter (B) through the cable to the main switchboard (A). With unity power factor assumed, the current flowing through the cable resistance produces a higher voltage at B than at A.'),
        ('lbl', 'ASSUMED MEASUREMENT ARRANGEMENT'),
        ('p', 'The example assumes two three-phase power-quality analysers at A and B, with Class S measurement capability under IEC 61000-4-30. All modelled data use a common time base. The relative timing accuracy of two actual instruments has not been established to within 20 ms; nor is 20 ms trace recording implied solely by a Class S designation.')]),

    # ── 03 ────────────────────────────────────────────────────────────────────────────
    dict(head='02 / METHOD', blocks=[
        ('h1', 'Measurement representation and modelling method'),
        ('lbl', 'DATA STRUCTURE'),
        ('p', 'The model contains seven complete days of ten-minute time series, with 1,008 values in each series. The 20 ms RMS voltage values around inverter trips are aligned to the model\'s common time axis. No field measurements were carried out, and the accuracy or clock synchronisation of physical instruments was not assessed.'),
        ('table', ['SOURCE', 'MODELLED QUANTITIES', 'RECORD TYPES IN THE MODEL'], [
            ['A / main switchboard', 'L1–N, L2–N and L3–N RMS voltages; active power imported from and exported to the grid; THD(U); U2/U1; illustrative Pst and Plt; frequency', 'Ten-minute series and individual event records'],
            ['B / inverter', 'L1–N, L2–N and L3–N RMS voltages; inverter active power; PV feeder current', 'Ten-minute series and 20 ms RMS event records'],
            ['Inverter operating model', 'Trip times, illustrative AC_OV_1 code, operating state and reconnection', 'Trip log and series at 1 s intervals']],
         'lll', 'mt'),
        ('lbl', 'MAIN MODELLING ASSUMPTIONS'),
        ('p', 'The power-flow calculation uses a balanced three-phase approximation, with active power only and unity power factor. The small differences between the synthetic phase-voltage values shown later are not represented in this simplified power-flow calculation. The assumed resistance is 0.095 Ω per phase conductor for the PV feeder and 0.070 Ω for the equivalent upstream supply. The calculation is solved iteratively. Cable reactance, reactive power, harmonic currents, variations in conductor temperature and inverter-control dynamics are excluded from the power-flow calculation.'),
        ('p', 'The voltage and active-power time series were generated by the model. The Pst, Plt and THD(U) values are illustrative: they are not the results of measurements made using instruments implementing IEC 61000-4-15 and IEC 61000-4-7. The 253 V threshold and approximately 2.1 s delay are also modelling assumptions, not verified settings for an actual inverter.'),
        ('warn', '**FOR REAL FIELD MEASUREMENTS.** Verify the connection diagram and PE conductor, voltage-measurement circuits, current-sensor ratios and polarity, instrument measurement class, applicable calibration and/or statutory verification documentation, clock synchronisation, inverter make and model, and approved grid-connection settings.')]),

    # ── 04 ────────────────────────────────────────────────────────────────────────────
    dict(head='03 / SEVEN DAYS', blocks=[
        ('h1', 'Changes in voltage and power over seven days'),
        ('lbl', 'CHART 1. L2–N VOLTAGE AT A AND B / TEN-MINUTE MEAN VALUES'),
        ('fig', 'p4_1', dict(leg=LEG_U, lx=6.2, ly=8.3, y='L2–N voltage, V', yx=1.4, yy=46.5)),
        ('lbl', 'CHART 2. PV PLANT OUTPUT AND WORKSHOP LOAD / TEN-MINUTE MEAN VALUES'),
        ('fig', 'p4_2', dict(leg=[('line', C1, 'PV plant active-power output'), ('line', G1, 'Workshop active load')],
                             lx=6.2, ly=8.3, y='Active power, kW', yx=1.4, yy=46.5)),
        ('lbl', 'SEVEN-DAY ENERGY BALANCE'),
        ('cards', [
            ('Energy generated by the inverter at B', '4,883.8 kWh'),
            ('Energy losses in the PV cable', '175.2 kWh'),
            ('Energy consumed by the workshop', '2,748.1 kWh'),
            ('Energy imported from the grid at A', '812.9 kWh'),
            ('Energy exported to the grid at A', '2,773.4 kWh'),
            ('PV energy transferred from B to A', '4,708.6 kWh')]),
        ('note', 'Energy balance calculated from the model at 1 s intervals: **inverter generation (B) + grid imports = workshop consumption + feeder losses + grid exports**. Totals were calculated from unrounded data.')]),

    # ── 05 ────────────────────────────────────────────────────────────────────────────
    dict(head='04 / TRIPS', blocks=[
        ('h1', 'Summary of inverter trips'),
        ('table', ['EVENT', 'DATE AND LOCAL TIME', 'B: 20 ms RMS, V', 'A: RMS, V', DU + ', V', 'P, kW',
                   'TIME DISCONNECTED, min:s', 'ESTIMATED ENERGY NOT GENERATED, kWh'], [
            ['E-01', '08.06 12:41:16', '255.1', '242.8', '12.3', '99.1', '6:20', '10.5'],
            ['E-02', '10.06 11:57:42', '254.4', '242.7', '11.7', '93.8', '5:40', '9.0'],
            ['E-03', '10.06 13:22:18', '254.5', '243.1', '11.5', '92.1', '7:10', '11.3'],
            ['E-04', '11.06 12:08:09', '254.2', '243.4', '10.8', '87.1', '6:05', '9.1'],
            ['E-05', '13.06 11:36:27', '254.4', '243.1', '11.3', '90.5', '6:45', '10.5'],
            ['E-06', '13.06 12:54:31', '254.7', '243.1', '11.6', '93.2', '5:35', '8.6'],
            ['E-07', '14.06 11:21:54', '254.2', '243.1', '11.1', '89.3', '7:25', '11.4'],
            ['E-08', '14.06 13:11:38', '255.3', '243.5', '11.9', '95.6', '6:10', '10.1']],
         'vvnnnnnn', 'trips8'),
        ('note', 'The voltages at A and B refer to the same simulated instant immediately before each trip. The inverter power is taken from the model at that instant, not from a ten-minute mean. The table columns were rounded independently; subtracting the displayed voltages may differ from the listed ΔU by up to 0.1 V.'),
        ('lbl', 'OVERVIEW OF THE EIGHT TRIPS'),
        ('p', 'All eight trips were generated using the same fictional rule: the L2–N voltage at B remains above 253 V for 2.08–2.10 s. AC_OV_1 is an illustrative code for this example, not a manufacturer-verified fault code. Trips occur between 11:20 and 13:25 on five of the seven days, during periods of high simulated PV generation.'),
        ('p', 'Energy not generated was estimated by calculating the output the plant could have produced without the trips. This is not a calculation of financial loss, and the estimate has not been adjusted using measured weather data.'),
        ('total', 'Estimated energy not generated: 80.4 kWh. Total time disconnected: 51 min 10 s.'),
        ('note', 'The individually rounded event estimates sum to 80.5 kWh; the model total calculated from unrounded values is 80.4 kWh.')]),

    # ── 06 ────────────────────────────────────────────────────────────────────────────
    dict(head='05 / EVENT E-08', blocks=[
        ('h1', 'Event E-08: voltage leading up to the trip'),
        ('sub2', '14 June 2026, 13:11:38 / synthetic L2–N voltage trace with 20 ms RMS values'),
        ('fig', 'p6_3', dict(leg=LEG_U[:2], lx=6.2, ly=6.8, legb=LEG_U[2:], lbx=53.6, y='L2–N voltage, V', yx=1.4, yy=44.7,
                             x='Time relative to trip, s', xx=51.9, xy=95.8)),
        ('table', ['TIME RELATIVE TO TRIP', 'POINT A, V', 'POINT B, V', 'DESCRIPTION'], [
            ['−9.00 s', '237.6', '249.8', 'Before the brief voltage rise'],
            ['−2.00 s', '241.2', '253.1', 'Above the assumed threshold'],
            ['−0.02 s', '243.5', '255.3', 'Highest pre-trip RMS value'],
            ['+10.00 s', '228.6', '228.6', 'Inverter disconnected']],
         'vnnl', 'ev'),
        ('lbl', 'EVENT ANALYSIS'),
        ('p', 'Immediately before event E-08, the inverter\'s modelled active-power output is 95.6 kW. The voltage at B remains above the assumed 253 V threshold for 2.08 s and reaches 255.3 V. At the same simulated instant, voltage at A is 243.5 V. Once the inverter disconnects, the current flowing from the inverter towards point A falls to approximately zero, and the resistive voltage difference across the PV cable also nearly disappears.'),
        ('warn', '**LIMITATION.** The chart and table were generated from calculated data. Without separate verification of clock synchronisation, a real Class S power-quality analyser and the inverter event log cannot be assumed to agree in time to within 20 ms.')]),

    # ── 07 ────────────────────────────────────────────────────────────────────────────
    dict(head='06 / POWER QUALITY', tight=True, blocks=[
        ('h1', 'Diagnostic power-quality indicators'),
        ('lbl', 'MODELLED VALUES AT POINT A'),
        ('table', ['INDICATOR', 'MINIMUM', 'P95', 'MAXIMUM', 'INDICATIVE RANGE'], [
            ['U L1–N', '227.27 V', '236.37 V', '237.91 V', '207–253 V'],
            ['U L2–N', '227.87 V', '236.85 V', '238.44 V', '207–253 V'],
            ['U L3–N', '227.42 V', '236.53 V', '237.94 V', '207–253 V'],
            ['THD(U) *', '1.46%', '1.82%', '1.95%', '—'],
            ['U2/U1 *', '0.04%', '0.08%', '0.09%', '—'],
            ['Pst *', '0.32', '0.50', '0.57', '—'],
            ['Plt (2 h) *', '0.36', '0.47', '0.49', '—'],
            ['Frequency', '49.98 Hz', '50.02 Hz', '50.02 Hz', '—']],
         'lnnnn', 'pq'),
        ('note', 'P95 is the 95th percentile of the relevant modelled series; it does not, by itself, establish compliance with a standard. Indicators marked with an asterisk (*) are illustrative. Pst and Plt were not calculated with an IEC 61000-4-15-compliant flickermeter. THD(U) likewise does not come from field measurements.'),
        ('lbl', 'VOLTAGE AT INVERTER TERMINALS (POINT B) / TEN-MINUTE VALUES'),
        ('table', ['PHASE', 'MINIMUM', 'P95', 'MAXIMUM'], [
            ['L1–N', '227.3 V', '248.0 V', '250.3 V'],
            ['L2–N', '227.9 V', '248.5 V', '250.7 V'],
            ['L3–N', '227.4 V', '248.2 V', '250.2 V']],
         'lnnn', 'pb'),
        ('note', 'The highest ten-minute mean voltage at B is 250.7 V (L2–N). A brief overvoltage lasting approximately 2 s can produce 20 ms RMS values above 253 V without raising the corresponding ten-minute mean to that threshold.'),
        ('lbl', 'OTHER SHORT-DURATION EVENTS'),
        ('p', 'Two brief voltage dips were generated at A: on 9 June at 08:37:12, L1–N falls to 197.4 V for 320 ms; on 12 June at 16:09:45, L3–N falls to 201.3 V for 440 ms. The model attributes these events to simulated compressor starts. They do not coincide with the inverter trips.'),
        ('warn', '**NOTE.** The 230 V ±10% range is used here for reference only. These modelled values do not establish compliance with EN 50160 or GOST 32144-2013. A real assessment first requires confirmation of the applicable standard, the documented point of supply and the measurement method.')]),

    # ── 08 ────────────────────────────────────────────────────────────────────────────
    dict(head='07 / CALCULATION', blocks=[
        ('h1', 'Voltage-rise mechanism and calculation'),
        ('lbl', 'E-08 / RESISTIVE VOLTAGE RISE ALONG THE PV CABLE'),
        ('eq', [
            ('Maximum DC resistance of a 70 mm² aluminium conductor at 20 °C:', '0.443 Ω/km × 0.185 km = 0.08196 Ω per phase'),
            ('Assumed conductor resistance at approximately 60 °C:', 'R = 0.095 Ω per phase'),
            ('Approximate current:', 'I ≈ 95.6 kW ÷ (3 × 255.3 V) = 124.82 A'),
            ('Rise in voltage at B relative to A:', DU + ' ≈ 124.82 A × 0.095 Ω = 11.86 V')]),
        ('note', 'The IEC 60228 figure of 0.443 Ω/km is the maximum DC resistance at 20 °C for a 70 mm² aluminium conductor, not a value measured on site. The 60 °C conductor temperature is also assumed. This simplified calculation excludes cable reactance and resistance at the terminations. The current formula assumes balanced three-phase currents and unity power factor.'),
        ('lbl', 'CHART. VOLTAGE RISE VERSUS PV ACTIVE-POWER OUTPUT'),
        ('fig', 'p8_4', dict(leg=[('line', G2, 'Calculated curve, U_A = 243 V'), ('dot', C2, 'Trip events E-01–E-08')],
                             lx=6.6, ly=8.6, y='Voltage rise, ' + DU + ', V', yx=1.6, yy=43.3,
                             x='Inverter active-power output, kW', xx=52.2, xy=94.6)),
        ('lbl', 'THREE CONTRIBUTING FACTORS'),
        ('num', [
            '**PV cable from A to B.** The current flowing from the inverter to the main switchboard causes the voltage at B to be higher than at A. When the inverter current stops, this resistive voltage difference almost disappears.',
            '**Upstream supply network.** Exporting power to the grid may also raise the voltage at A. This model cannot determine the contribution of any particular distribution network or establish responsibility on the part of its operator.',
            '**Brief voltage rise at A.** The model includes an additional short-duration rise at A before the trip. The physical cause of this variation has not been established within the model.'])]),

    # ── 09 ────────────────────────────────────────────────────────────────────────────
    dict(head='08 / RECOMMENDATIONS', blocks=[
        ('h1', 'Recommended actions and verification'),
        ('steps', [
            ('01 / DO NOT RAISE THE PROTECTION THRESHOLDS WITHOUT AUTHORISATION', 'Increasing the illustrative 253 V threshold should not be treated as a substantiated solution. First, identify the installed inverter\'s manufacturer and model. Check the approved grid-connection settings, the overvoltage protection thresholds and operating delays. Confirm the meaning of the recorded fault code against the manufacturer\'s technical documentation.'),
            ('02 / REVIEW THE PV CABLE DESIGN', 'The design engineer should verify the cable conductor cross-sections, the separate PE conductor\'s size and installation method, cable current-carrying capacity, protective-device selection and coordination, termination condition and permissible voltage rise. Then compare feasible alternatives—a larger cable cross-section, a parallel cable run or a shorter route—taking account of installation costs and electrical losses.'),
            ('03 / REVIEW AVAILABLE INVERTER CONTROL FUNCTIONS', 'Consider active-power curtailment using P(U) and reactive-power control using Q(U), provided these functions are supported by the inverter and permitted by the grid-connection requirements. P(U) can reduce energy production. Q(U) changes current magnitude and phase relationship and may not resolve the overvoltage problem.'),
            ('04 / INVESTIGATE THE VOLTAGE RISE AT POINT A', 'At A, record phase-to-neutral (L–N) voltages, active and reactive power, PV feeder current and the operating states of nearby major loads. Where necessary, discuss the results with the distribution network operator. Responsibility cannot be assigned on the basis of this model alone.'),
            ('05 / REPEAT MEASUREMENTS AFTER ANY CHANGES', 'Repeat synchronised measurements at A and B under comparable conditions of high PV output and relatively low workshop demand. Retain weather data, inverter settings, the connection diagram, measurement-instrument details and the results of clock-synchronisation checks.')]),
        ('lbl', 'CRITERIA FOR ASSESSING THE RESULT'),
        ('num', [
            'No overvoltage-related inverter trips occur during a predefined verification period under comparable PV generation conditions.',
            'The maximum voltage at the inverter AC terminals and the voltage difference between A and B do not exceed the permissible values established by the design and approved settings, with measurement uncertainty taken into account.',
            'Before-and-after measurement records, inverter settings, calculations and the responsible engineer\'s conclusions are documented and retained.'])]),

    # ── 10 ────────────────────────────────────────────────────────────────────────────
    dict(head='09 / LIMITATIONS', tight=True, blocks=[
        ('h1', 'Data, limitations and references'),
        ('lbl', 'DATA ENVISAGED FOR THE DEMONSTRATION'),
        ('p', 'The example envisages ten-minute time series, an inverter trip log, eight 20 ms RMS event records, a post-trip reconnection series for E-08, records of two simulated voltage dips, a model summary and an automated validation log. The source data files are not attached to this PDF.'),
        ('lbl', 'LIMITATIONS OF THE EXAMPLE'),
        ('bul', [
            'No real workshop was investigated and no physical measuring instruments were installed. No measured cable temperature or verified PE-conductor design is available.',
            'No approved grid-connection settings or actual inverter overvoltage protection thresholds and delays are available. The 253 V / approximately 2.1 s rule and the AC_OV_1 code are illustrative.',
            'No exports from actual measuring instruments, tests of instrument synchronisation, calibration certificates or documented point of supply are provided.',
            'Full network impedance, reactive-power variations, measured solar irradiance, revenue-metering data and legal responsibility have not been assessed.']),
        ('lbl', 'DEFINITIONS AND NOTATION'),
        ('defs', [
            ('A', 'main distribution switchboard.'),
            ('B', 'inverter AC terminals.'),
            (DU, 'voltage rise at B relative to A.'),
            ('20 ms RMS', 'root-mean-square voltage calculated over one cycle at 50 Hz.'),
            ('P95', '95th percentile of the relevant data series.'),
            ('P(U)', 'voltage-dependent active-power control.'),
            ('Q(U)', 'voltage-dependent reactive-power control.')]),
        ('lbl', 'TECHNICAL REFERENCES'),
        ('refs', [
            'IEC 61000-4-30 — power-quality measurement methods.',
            'IEC 61000-4-7 — methods for measuring harmonics and interharmonics.',
            'IEC 61000-4-15 — flicker measurement methods.',
            'IEC 60228 — conductor construction and resistance.',
            'EN 50160 and GOST 32144-2013 — characteristics of supply voltage.']),
        ('p', 'The applicable standards, grid-connection requirements and measurement boundary must be confirmed for each actual site.'),
        ('warn', '**FINAL NOTE.** This is an educational example based on modelling. The figures are consistent with the stated simplified calculation but do not establish the cause of a real malfunction, the protection settings of any particular inverter, network compliance or legal responsibility. A real engineering conclusion requires original instrument data, verified settings and a checked connection diagram.')]),
]


def build():
    return g.build('en', PAGES, FOOT, 'GRIDEC — Technical report (demonstration example)')


if __name__ == '__main__':
    print(build())
