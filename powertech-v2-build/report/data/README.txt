GRIDEC · SAMPLE REPORT · SYNTHETIC DATA
Report: GRIDEC_Sample_Report_PV_Trips_EN.pdf / GRIDEC_Sample_Report_PV_Trips_HY.pdf

Everything here is invented: the site, the installation, the measurements and the events.
These files are not an export from an analyser or an inverter. They let you check every
figure in the sample report.

Site: heavy-equipment repair workshop, 100 kW AC PV plant.
Window: 2026-06-08 00:00:00 to 2026-06-15 00:00:00, Asia/Yerevan (UTC+04).
Point A: main switchboard. Point B: inverter AC terminals.

FILES
GRIDEC_example_10min_data.csv
  1008 rows. 10-minute means at A (u_pcc_*) and B (u_pv_*), PV output, workshop load,
  network power (import positive, export negative), THD(U), unbalance, Pst, frequency,
  inverter off-time in seconds.
GRIDEC_example_inverter_events.csv
  8 trips with code AC_OV_1. Highest 20 ms RMS voltage at B, voltage at A at the same
  moment, PV output before the trip, downtime, lost generation (output x downtime).
GRIDEC_example_E08_20ms_RMS.csv
  20 ms RMS record of L2-N voltage at A and B, 20 s before and after event E-08.
  The pv_kw_synthetic_interp column is illustrative, not a 20 ms power measurement.
GRIDEC_example_other_PQ_events.csv
  2 voltage dips at A.

NOTES
Timestamps are local time, UTC+04, without an offset.
Plt (2 h) in the report is calculated from 12 consecutive Pst values.
The U> setting of 253 V / 2.0 s belongs to this example only.

----------------------------------------------------------------------

GRIDEC · ՀԱՇՎԵՏՎՈՒԹՅԱՆ ՕՐԻՆԱԿ · ՄՈԴԵԼԱՎՈՐՎԱԾ ՏՎՅԱԼՆԵՐ

Այստեղ ամեն ինչ հորինված է՝ չափման վայրը, էլեկտրակայանքը, չափումները և դեպքերը։
Ֆայլերը չափիչ սարքից կամ ինվերտորից արտահանված չեն։ Դրանցով կարելի է ստուգել
հաշվետվության օրինակի յուրաքանչյուր թիվ։

A կետ՝ հիմնական բաշխիչ վահանակ։ B կետ՝ ինվերտորի AC սեղմակներ։
Ժամանակը տեղական է՝ UTC+04։

GRIDEC_example_10min_data.csv — 10 րոպեի միջիններ, 1008 տող։
GRIDEC_example_inverter_events.csv — ինվերտորի 8 անջատում։
GRIDEC_example_E08_20ms_RMS.csv — E-08 դեպքի 20 մվրկ RMS գրառումը։
GRIDEC_example_other_PQ_events.csv — լարման 2 անկում A կետում։
