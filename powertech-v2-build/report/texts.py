# Тексты учебного отчёта: ключ → (английский, армянский). Числа в фигурных скобках
# подставляет gen.py из файлов данных. Разделитель «|» — пункты списка или ячейки строки.
#
# Правила (разбор владельца 2026-11-21): оговорка «это пример» стоит один раз на обложке,
# один раз на последней странице и строкой в подвале; сам текст написан как настоящий
# отчёт. Армянский: «հիմնական բաշխիչ վահանակ» везде одинаково, секунды «վրկ» (не «վ» —
# путается с вольтом «Վ»), «ստուգաչափում» вместо «կալիբրացում», «մոնիթորինգ» как на сайте.
T = {
 'doc_title': ('Gridec · Sample report · PV inverter trips', 'Gridec · Հաշվետվության օրինակ · Ինվերտորի անջատումներ'),
 'ft': ('Sample report · synthetic data', 'Հաշվետվության օրինակ · մոդելավորված տվյալներ'),
 'u_volt': ('V', 'Վ'), 'u_v': ('U, V', 'U, Վ'), 'u_kw': ('P, kW', 'P, կՎտ'), 'u_s': ('s', 'վրկ'),
 'u_kwh': ('kWh', 'կՎտ·ժ'), 'u_hz': ('Hz', 'Հց'),
 'ax_time': ('Time relative to trip, s', 'Ժամանակը անջատման պահի նկատմամբ, վրկ'),

 # ── обложка
 'kick': ('Technical report', 'Տեխնիկական հաշվետվություն'),
 'title': ('PV inverter trips at a repair workshop', 'Արևային կայանի ինվերտորի անջատումներ'),
 'sub': ('Seven days of power quality monitoring at the main switchboard and at the inverter.',
         'Էլեկտրաէներգիայի որակի յոթօրյա մոնիթորինգ հիմնական բաշխիչ վահանակում և ինվերտորի մոտ։'),
 'm_site': ('Site', 'Չափման վայր'),
 'm_site_v': ('Heavy-equipment repair workshop', 'Ծանր տեխնիկայի վերանորոգման արհեստանոց'),
 'm_period': ('Period', 'Ժամանակահատված'),
 'm_period_v': ('8–14 June 2026 · UTC+04', '2026 թ. հունիսի 8–14 · UTC+04'),
 'm_pv': ('PV plant', 'Արևային կայան'),
 'm_pv_v': ('100 kW AC / 125 kWp DC', '100 կՎտ AC / 125 կՎտ (պիկ) DC'),
 'm_supply': ('Supply', 'Սնուցում'),
 'm_supply_v': ('3 × 400/230 V · 50 Hz · TN-S', '3 × 400/230 Վ · 50 Հց · TN-S'),
 'k1': ('inverter trips', 'ինվերտորի անջատում'),
 'k2': ('total downtime, min:s', 'ընդհանուր պարապուրդ, ր:վրկ'),
 'k3': ('highest voltage at the inverter', 'առավելագույն լարումը ինվերտորի մոտ'),
 'k4': ('voltage rise along the feeder', 'լարման բարձրացումը մալուխային գծում'),
 'find_h': ('Finding', 'Եզրակացություն'),
 'find_1': ('All eight trips follow the same pattern. The L2–N voltage at the inverter terminals (point B) stays above '
            'the overvoltage setting of {uset} V for about two seconds, and the inverter logs AC_OV_1. At the main '
            'switchboard (point A) the voltage is {du_lo}–{du_hi} V lower at the same moment. The 185 m feeder between '
            'A and B produces this difference while the plant exports power.',
            'Բոլոր ութ անջատումներն ունեն նույն պատկերը։ Ինվերտորի սեղմակներում (B կետ) L2–N լարումը մոտ երկու '
            'վայրկյան մնում է գերլարման պաշտպանության {uset} Վ շեմից բարձր, և ինվերտորը գրանցում է AC_OV_1 կոդը։ '
            'Նույն պահին հիմնական բաշխիչ վահանակում (A կետ) լարումը {du_lo}–{du_hi} Վ-ով ցածր է։ Այս տարբերությունն '
            'առաջանում է A և B կետերը միացնող 185 մ մալուխային գծում, երբ կայանը հզորություն է տալիս ցանց։'),
 'find_2': ('The 10-minute values at A stay within the ±10 % band of GOST 32144-2013 for the whole week. The report '
            'does not assess the supply beyond that and does not assign responsibility.',
            'A կետում 10 րոպեի միջին լարումներն ամբողջ շաբաթվա ընթացքում մնում են ԳՕՍՏ 32144-2013-ով սահմանված ±10 % '
            'միջակայքում։ Հաշվետվությունը մատակարարվող լարման այլ գնահատական չի տալիս և պատասխանատվության հարց չի քննում։'),
 'smp_h': ('Sample report · synthetic data', 'Հաշվետվության օրինակ · մոդելավորված տվյալներ'),
 'smp_p': ('The site, the measurements and the events in this report are invented. The report shows the structure and '
           'level of detail of a Gridec report. The data files are published with it.',
           'Այս հաշվետվության մեջ չափման վայրը, չափումները և դեպքերը հորինված են։ Օրինակը ցույց է տալիս Gridec-ի '
           'հաշվետվության կառուցվածքն ու մանրամասնության աստիճանը։ Տվյալների ֆայլերը հրապարակված են հաշվետվության հետ։'),

 # ── 01 установка
 's1': ('Installation', 'Էլեկտրակայանք'),
 'h1_1': ('Installation and measurement points', 'Էլեկտրակայանք և չափման կետեր'),
 'f1': ('Supply connection', 'Սնուցման միացում'),
 'f1v': ('0.4 kV main switchboard · point A', '0,4 կՎ հիմնական բաշխիչ վահանակ · A կետ'),
 'f2': ('Inverter', 'Ինվերտոր'),
 'f2v': ('One three-phase unit, 100 kW AC · point B', 'Մեկ եռաֆազ ինվերտոր, 100 կՎտ AC · B կետ'),
 'f3': ('Workshop load during the week', 'Արհեստանոցի բեռը շաբաթվա ընթացքում'),
 'f3v': ('{load_rng} kW', '{load_rng} կՎտ'),
 'f4': ('Feeder A–B', 'A–B մալուխային գիծ'),
 'f4v': ('Aluminium, 4 × 70 mm², 185 m', 'Ալյումին, 4 × 70 մմ², 185 մ'),
 'f5': ('Main loads', 'Հիմնական սպառիչներ'),
 'f5v': ('Welders, air compressor, lifting equipment', 'Եռակցման սարքեր, կոմպրեսոր, վերամբարձ սարքավորումներ'),
 'f6': ('Feeder conductor resistance', 'Գծի հաղորդչի դիմադրություն'),
 'f6v': ('{r} Ω per phase at about 60 °C', '{r} Օմ մեկ ֆազի համար՝ մոտ 60 °C-ում'),
 'f7': ('Measuring instruments', 'Չափիչ սարքեր'),
 'f7v': ('Two three-phase power quality analysers, Class S', 'Էլեկտրաէներգիայի որակի երկու եռաֆազ չափիչ սարք, S դաս'),
 'f8': ('Inverter overvoltage setting U>', 'Ինվերտորի գերլարման պաշտպանություն U>'),
 'f8v': ('{uset} V phase to neutral, {tset} s', '{uset} Վ ֆազ–չեզոք, {tset} վրկ'),
 'dg_h': ('Measurement layout', 'Չափման սխեմա'),
 'dg_grid': ('NETWORK', 'ՑԱՆՑ'), 'dg_grid_s': ('0.4 kV supply', '0,4 կՎ սնուցում'),
 'dg_a': ('A · MAIN SWITCHBOARD', 'A · ՀԻՄՆԱԿԱՆ ԲԱՇԽԻՉ ՎԱՀԱՆԱԿ'), 'dg_a_s': ('point of supply', 'մատակարարման կետ'),
 'dg_b': ('B · INVERTER', 'B · ԻՆՎԵՐՏՈՐ'), 'dg_b_s': ('100 kW AC', '100 կՎտ AC'),
 'dg_load': ('WORKSHOP LOADS', 'ԱՐՀԵՍՏԱՆՈՑԻ ԲԵՌՆԵՐ'), 'dg_load_s': ('{load_rng} kW', '{load_rng} կՎտ'),
 'dg_cable': ('185 m · Al 4 × 70 mm²', '185 մ · Al 4 × 70 մմ²'),
 'dg_cable_s': ('feeder A–B', 'A–B մալուխային գիծ'),
 'dg_meter': ('analyser', 'չափիչ սարք'),
 'dg_note': ('Not a wiring diagram. Both analysers record voltage at the same time. Current and active power are '
             'measured on the incomer at A and on the PV feeder at B. Power drawn from the network is positive, '
             'exported power is negative.',
             'Մոնտաժային սխեմա չէ։ Երկու չափիչ սարքերը լարումը գրանցում են միաժամանակ։ Հոսանքն ու ակտիվ հզորությունը '
             'չափվում են A կետում՝ ներածման գծում, և B կետում՝ արևային կայանի գծում։ Ցանցից վերցվող հզորությունը '
             'դրական է, ցանց տրվողը՝ բացասական։'),
 'chk_h': ('Checked on site before recording', 'Չափումից առաջ տեղում ստուգվել է'),
 'chk_l': ('Cable type, length and cross-section against the as-built documents.|'
           'Inverter grid profile and protection settings, as exported from the inverter.|'
           'Neutral and protective-conductor arrangement of the four-core feeder.|'
           'Inverter serial number and firmware version.',
           'Մալուխի տեսակը, երկարությունը և հատույթը՝ ըստ կատարողական փաստաթղթերի։|'
           'Ինվերտորի ցանցային պրոֆիլը և պաշտպանության կարգաբերումները՝ ինվերտորից արտահանված տեսքով։|'
           'Քառաջիղ մալուխի չեզոք և պաշտպանիչ հաղորդիչների միացումը։|'
           'Ինվերտորի սերիական համարը և ծրագրային տարբերակը։'),

 # ── 02 программа
 's2': ('Method', 'Մեթոդ'),
 'h1_2': ('Measurement programme', 'Չափումների ծրագիր'),
 'mt_h': ('Channel|Location|Quantities|Resolution', 'Ալիք|Տեղը|Չափվող մեծություններ|Լուծաչափ'),
 'mt1': ('A · analyser|Main switchboard, incomer|Voltage, current, frequency, THD(U), unbalance, flicker, active power|'
         '10-minute means. Event records, 20 ms RMS',
         'A · չափիչ սարք|Հիմնական բաշխիչ վահանակ, ներածման գիծ|Լարում, հոսանք, հաճախություն, THD(U), անհամաչափություն, '
         'ֆլիկեր, ակտիվ հզորություն|10 րոպեի միջիններ։ Դեպքերի գրառումներ՝ 20 մվրկ RMS'),
 'mt2': ('B · analyser|Inverter AC terminals|Voltage, feeder current, active power|10-minute means. Event records, 20 ms RMS',
         'B · չափիչ սարք|Ինվերտորի AC սեղմակներ|Լարում, գծի հոսանք, ակտիվ հզորություն|10 րոպեի միջիններ։ Դեպքերի '
         'գրառումներ՝ 20 մվրկ RMS'),
 'mt3': ('INV · log|Inverter|Trip code, operating state|Event log, 1 s',
         'INV · մատյան|Ինվերտոր|Անջատման կոդ, աշխատանքային վիճակ|Դեպքերի մատյան, 1 վրկ'),
 'win_h': ('Recording window', 'Գրանցման ժամանակահատված'),
 'win_p': ('8 June 2026, 00:00 to 15 June 2026, 00:00 (UTC+04). Seven full days, {rows} ten-minute records per '
           'channel, no gaps.',
           '2026 թ. հունիսի 8-ի 00:00-ից հունիսի 15-ի 00:00-ն (UTC+04)։ Յոթ լրիվ օր, յուրաքանչյուր ալիքում՝ {rows} '
           'տասրոպեանոց գրառում, առանց բացթողումների։'),
 'meth_h': ('Measurement method', 'Չափման մեթոդ'),
 'meth_p': ('Voltage, frequency, harmonics, unbalance and flicker are measured with IEC 61000-4-30 Class S methods. '
            'Short events are recorded as RMS values over one 20 ms cycle. These are not waveform samples.',
            'Լարումը, հաճախությունը, հարմոնիկները, անհամաչափությունը և ֆլիկերը չափվում են ԳՕՍՏ ԻԷԿ 61000-4-30-2017-ի '
            'S դասի մեթոդներով։ Կարճատև դեպքերը գրանցվում են որպես մեկ պարբերության՝ 20 մվրկ-ի գործող (RMS) արժեքներ։ '
            'Դրանք ալիքաձևի ակնթարթային նմուշներ չեն։'),
 'pre_h': ('Checks before recording', 'Ստուգումներ գրանցումից առաջ'),
 'pre_l': ('Phase order L1/L2/L3 is the same at A and B.|Voltage is measured phase to neutral.|'
           'Current-transformer ratio and direction.|Sign of active power.|'
           'Clocks of both analysers and the inverter aligned to within ±0.5 s.',
           'L1/L2/L3 ֆազերի հերթականությունը A և B կետերում նույնն է։|Լարումը չափվում է ֆազի և չեզոքի միջև։|'
           'Հոսանքի տրանսֆորմատորների գործակիցն ու ուղղությունը։|Ակտիվ հզորության նշանը։|'
           'Երկու չափիչ սարքերի և ինվերտորի ժամացույցները համաժամեցված են ±0,5 վրկ ճշտությամբ։'),
 'why_h': ('Why two measurement points', 'Ինչու երկու չափման կետ'),
 'why_p': ('One analyser at the main switchboard cannot show the voltage that the inverter sees. The inverter log has '
           'a 1-second step and no voltage record. With two points recorded at the same time, the voltages at A and B '
           'can be compared at the moment of each trip.',
           'Հիմնական բաշխիչ վահանակում տեղադրված մեկ չափիչ սարքը ցույց չի տալիս, թե ինչ լարում է ինվերտորի սեղմակներում։ '
           'Ինվերտորի մատյանն ունի 1 վրկ քայլ և լարման գրառում չի պարունակում։ Երկու կետում միաժամանակ գրանցումը թույլ '
           'է տալիս համեմատել A և B կետերի լարումները յուրաքանչյուր անջատման պահին։'),

 # ── 03 неделя
 's3': ('Week', 'Շաբաթ'),
 'h1_3': ('Voltage and power over the week', 'Լարումը և հզորությունը շաբաթվա ընթացքում'),
 'c1_h': ('L2–N voltage at A and B · 10-minute means', 'L2–N լարումը A և B կետերում · 10 րոպեի միջիններ'),
 'c2_h': ('PV output and workshop load · 10-minute means',
          'Արևային կայանի հզորությունը և արհեստանոցի բեռը · 10 րոպեի միջիններ'),
 'lg_a': ('A · main switchboard', 'A · հիմնական բաշխիչ վահանակ'), 'lg_b': ('B · inverter', 'B · ինվերտոր'),
 'lg_pv': ('PV output', 'Արևային կայան'), 'lg_load': ('Workshop load', 'Արհեստանոցի բեռ'),
 'wk_note': ('The voltage at B follows PV output. On clear days it reaches {b10_lo}–{b10_hi} V as a 10-minute mean. '
             'The trips are not visible at this resolution: each one develops within a few seconds. Vertical lines in '
             'the upper chart mark the eight trips.',
             'B կետի լարումը հետևում է արևային կայանի հզորությանը։ Պարզ օրերին 10 րոպեի միջինը հասնում է '
             '{b10_lo}–{b10_hi} Վ-ի։ Անջատումներն այս լուծաչափով չեն երևում. յուրաքանչյուրը զարգանում է մի քանի '
             'վայրկյանում։ Վերին գրաֆիկի ուղղահայաց գծերը ցույց են տալիս ութ անջատումները։'),
 'en_h': ('Energy over the week', 'Էներգիան շաբաթվա ընթացքում'),
 'en1': ('PV output', 'արևային կայանի արտադրություն'), 'en2': ('workshop consumption', 'արհեստանոցի սպառում'),
 'en3': ('drawn from the network', 'ցանցից վերցված'), 'en4': ('exported to the network', 'ցանց տրված'),
 'en_note': ('Calculated from 10-minute mean power. These are not revenue-meter readings.',
             'Հաշվարկված է 10 րոպեի միջին հզորություններից։ Առևտրային հաշվիչի ցուցմունքներ չեն։'),

 # ── 04 журнал
 's4': ('Trip log', 'Անջատումներ'),
 'h1_4': ('Eight inverter trips', 'Ինվերտորի ութ անջատում'),
 'tl_h': ('Event|Date, time|B: highest L2–N, V|A: L2–N at that moment, V|Difference, V|PV output before trip, kW|Downtime, min:s',
          'Դեպք|Ամսաթիվ, ժամ|B՝ L2–N առավելագույնը, Վ|A՝ L2–N նույն պահին, Վ|Տարբերություն, Վ|Հզորությունն անջատումից առաջ, կՎտ|Պարապուրդ, ր:վրկ'),
 'tl_note': ('B: highest 20 ms RMS value in the event record. A: value at the same moment, not a 10-minute mean. '
             'PV output before trip: mean output in that 10-minute interval while the inverter was running.',
             'B՝ դեպքի գրառման 20 մվրկ RMS առավելագույն արժեքը։ A՝ նույն պահի արժեքը, ոչ թե 10 րոպեի միջինը։ '
             'Հզորությունն անջատումից առաջ՝ միջին հզորությունը տվյալ 10 րոպեում, քանի դեռ ինվերտորն աշխատում էր։'),
 'com_h': ('What the eight events have in common', 'Ինչն է ընդհանուր ութ դեպքերում'),
 'com_l': ('PV output is {p_rng} kW.|'
           'The voltage at B is {du_rng} V above the voltage at A, in proportion to the output.|'
           'For a few seconds the voltage at A is itself {sw_lo}–{sw_hi} V above its 10-minute mean.|'
           'B passes {uset} V, the inverter logs AC_OV_1 and disconnects. It reconnects after 5.5–7.5 minutes.|'
           'All trips fall between 11:20 and 13:25, on five of the seven days.',
           'Արևային կայանի հզորությունը {p_rng} կՎտ է։|'
           'B կետի լարումը A կետի լարումից բարձր է {du_rng} Վ-ով՝ հզորությանը համեմատական։|'
           'A կետի լարումն էլ մի քանի վայրկյան {sw_lo}–{sw_hi} Վ-ով բարձր է իր 10 րոպեի միջինից։|'
           'B կետում լարումն անցնում է {uset} Վ-ը, ինվերտորը գրանցում է AC_OV_1 և անջատվում։ 5,5–7,5 րոպե անց այն '
           'նորից միանում է։|'
           'Բոլոր անջատումները եղել են 11:20–13:25 միջակայքում, յոթ օրից հինգում։'),
 'lost_h': ('Lost generation', 'Չարտադրված էներգիա'),
 'lost_p': ('Output before each trip multiplied by its downtime. The estimate assumes that output would have stayed at '
            'the pre-trip level. Irradiance was not measured. This is about {lost_pct} % of the PV output for the week.',
            'Յուրաքանչյուր անջատումից առաջ եղած հզորությունը բազմապատկված է պարապուրդի տևողությամբ։ Գնահատումը '
            'ենթադրում է, որ հզորությունը կմնար նույն մակարդակին։ Արևի ճառագայթումը չի չափվել։ Սա շաբաթվա '
            'արտադրության մոտ {lost_pct} %-ն է։'),

 # ── 05 событие
 's5': ('Event E-08', 'E-08 դեպք'),
 'h1_5': ('Event E-08 · 14 June 2026, 13:11:38', 'E-08 դեպք · 2026 թ. հունիսի 14, 13:11:38'),
 'c3_h': ('L2–N voltage at A and B · 20 ms RMS values', 'L2–N լարումը A և B կետերում · 20 մվրկ RMS արժեքներ'),
 'c3_note': ('Time zero is the trip time in the inverter log. The shaded band is the time that B spends above the U> setting.',
             'Զրոն ինվերտորի մատյանում գրանցված անջատման պահն է։ Գունավոր շերտը ցույց է տալիս, թե որքան ժամանակ է B '
             'կետի լարումը մնում U> շեմից բարձր։'),
 'ev_h': ('Time|B · L2–N, V|A · L2–N, V|Difference, V|Inverter', 'Ժամ|B · L2–N, Վ|A · L2–N, Վ|Տարբերություն, Վ|Ինվերտոր'),
 'st1': ('{e8_p} kW · running', '{e8_p} կՎտ · աշխատում է'),
 'st2': ('B passes {uset} V', 'B կետի լարումն անցնում է {uset} Վ-ը'),
 'st3': ('AC_OV_1 · trip', 'AC_OV_1 · անջատում'),
 'st4': ('0 kW · off', '0 կՎտ · անջատված'),
 'st5': ('reconnected', 'նորից միացված'),
 'rec_h': ('What the record shows', 'Ինչ է ցույց տալիս գրառումը'),
 'rec_l': ('Before the event, at {e8_p} kW, the voltage at B is {e8_pre_du} V above the voltage at A.|'
           'About six seconds before the trip the voltage at A starts to rise and gains {e8_swell} V. PV output does '
           'not change. B follows A and stays above {uset} V for {e8_above} s. This matches the {tset} s delay of the '
           'U> setting.|'
           'When the inverter disconnects, the difference between A and B falls to {e8_post_du} V. The voltage at A '
           'falls by about {e8_drop} V.',
           'Դեպքից առաջ, {e8_p} կՎտ հզորության դեպքում, B կետի լարումը {e8_pre_du} Վ-ով բարձր է A կետի լարումից։|'
           'Անջատումից մոտ վեց վայրկյան առաջ A կետի լարումը սկսում է բարձրանալ և աճում է {e8_swell} Վ-ով։ Արևային '
           'կայանի հզորությունը չի փոխվում։ B կետի լարումը հետևում է A-ին և {e8_above} վրկ մնում է {uset} Վ-ից բարձր։ '
           'Սա համապատասխանում է U> պաշտպանության {tset} վրկ հապաղմանը։|'
           'Ինվերտորի անջատվելուց հետո A և B կետերի լարումների տարբերությունը նվազում է մինչև {e8_post_du} Վ։ A կետի '
           'լարումն իջնում է մոտ {e8_drop} Վ-ով։'),

 # ── 06 качество
 's6': ('Power quality', 'Էլեկտրաէներգիայի որակ'),
 'h1_6': ('Power quality at the main switchboard', 'Էլեկտրաէներգիայի որակը հիմնական բաշխիչ վահանակում'),
 'pq_h': ('Parameter at A|Lowest|95 % value|Highest|Limit for 95 % of the week|Limit for 100 %|Result',
          'Ցուցանիշը A կետում|Նվազագույն|95 % արժեք|Առավելագույն|Նորմ՝ շաբաթվա 95 %-ի համար|Նորմ՝ 100 %-ի համար|Արդյունք'),
 't10': ('10 min', '10 ր'), 't2h': ('2 h', '2 ժ'),
 'unb': ('Voltage unbalance', 'Լարման անհամաչափություն'), 'freq': ('Frequency', 'Հաճախություն'),
 'ok': ('within limits', 'նորմայում'), 'inf': ('for information¹', 'տեղեկատվական¹'),
 'pq_note': ('Limits: GOST 32144-2013, applied at the point of supply. EN 50160:2022 sets the same ±10 % band for 95 % '
             'of the 10-minute voltage values. ¹ The standard assesses frequency on 10-second values; the table shows '
             '10-minute means.',
             'Նորմերը՝ ըստ ԳՕՍՏ 32144-2013-ի, կիրառվում են էլեկտրաէներգիայի մատակարարման կետում։ EN 50160:2022-ը նույն '
             '±10 % միջակայքն է սահմանում լարման 10 րոպեի արժեքների 95 %-ի համար։ ¹ Ստանդարտը հաճախությունը գնահատում '
             'է 10 վայրկյանի արժեքներով. աղյուսակում 10 րոպեի միջիններն են։'),
 'pb_h': ('Voltage at the inverter (B) · 10-minute means', 'Լարումն ինվերտորի մոտ (B կետ) · 10 րոպեի միջիններ'),
 'pb_th': ('Phase|Lowest|95 % value|Highest', 'Ֆազ|Նվազագույն|95 % արժեք|Առավելագույն'),
 'pb_p': ('At B the highest 10-minute mean is {b10max} V on L2, {b10gap} V below the inverter setting. The limits of '
          'the standard do not apply at B, which is a point inside the customer installation. The table shows how '
          'little margin is left.',
          'B կետում 10 րոպեի ամենաբարձր միջինը {b10max} Վ է՝ L2 ֆազում, ինվերտորի շեմից {b10gap} Վ-ով ցածր։ Ստանդարտի '
          'նորմերը B կետում չեն կիրառվում, քանի որ այն սպառողի ներքին ցանցի կետ է։ Աղյուսակը ցույց է տալիս, թե որքան '
          'փոքր է մնացած պաշարը։'),
 'dip_h': ('Voltage dips at A', 'Լարման անկումներ A կետում'),
 'dip_p': ('Two dips were recorded: L1–N down to {dip1_u} V for {dip1_ms} ms (9 June, {dip1_t}) and L3–N down to '
           '{dip2_u} V for {dip2_ms} ms (12 June, {dip2_t}). Neither coincides with an inverter trip. The operations '
           'log links both to compressor starts.',
           'Գրանցվել է երկու անկում. L1–N՝ մինչև {dip1_u} Վ, {dip1_ms} մվրկ (հունիսի 9, {dip1_t}) և L3–N՝ մինչև '
           '{dip2_u} Վ, {dip2_ms} մվրկ (հունիսի 12, {dip2_t})։ Դրանցից ոչ մեկը չի համընկնում ինվերտորի անջատման հետ։ '
           'Ըստ շահագործման մատյանի՝ երկուսն էլ համընկնում են կոմպրեսորի գործարկման հետ։'),

 # ── 07 причина
 's7': ('Cause', 'Պատճառ'),
 'h1_7': ('Why the voltage rises at the inverter', 'Ինչու է լարումը բարձրանում ինվերտորի մոտ'),
 'bg1': ('inverter terminals, E-08', 'ինվերտորի սեղմակներ, E-08'),
 'bg2': ('main switchboard, same moment', 'հիմնական բաշխիչ վահանակ, նույն պահին'),
 'bg3': ('rise along the feeder', 'բարձրացումը մալուխային գծում'),
 'bg4': ('of the nominal 230 V', 'անվանական 230 Վ-ի նկատմամբ'),
 'calc_h': ('Feeder calculation', 'Մալուխային գծի հաշվարկ'),
 'eq1': ('I = P / (√3 × U × cos φ) = {p_w} / (√3 × 400 × {cosphi}) ≈ {i_calc} A',
         'I = P / (√3 × U × cos φ) = {p_w} / (√3 × 400 × {cosphi}) ≈ {i_calc} Ա'),
 'eq2': ('ΔU = I × R × cos φ = {i_calc1} × {r} × {cosphi} ≈ {du_calc} V',
         'ΔU = I × R × cos φ = {i_calc1} × {r} × {cosphi} ≈ {du_calc} Վ'),
 'calc_p': ('Measured at E-08: {e8_du} V. The calculated and the measured rise agree.',
            'E-08 դեպքում չափված արժեքը՝ {e8_du} Վ։ Հաշվարկային և չափված արժեքները համընկնում են։'),
 'calc_r': ('R: {rkm} Ω/km at 20 °C for 70 mm² aluminium (IEC 60228) × {lkm} km = {r20} Ω, about {r} Ω at 60 °C. '
            'The calculation uses the nominal voltage and neglects cable reactance.',
            'R. 70 մմ² ալյումինի համար {rkm} Օմ/կմ 20 °C-ում (IEC 60228) × {lkm} կմ = {r20} Օմ, 60 °C-ում՝ մոտ {r} Օմ։ '
            'Հաշվարկում վերցված է անվանական լարումը, մալուխի ռեակտիվ դիմադրությունը հաշվի չի առնված։'),
 'three_h': ('Three contributions to the voltage at B', 'B կետի լարման երեք բաղադրիչ'),
 'c1t': ('Feeder A–B', 'A–B մալուխային գիծ'),
 'c1p': ('At {p_lo}–{p_hi} kW. Measured at every trip, proportional to output, gone when the inverter is off.',
         '{p_lo}–{p_hi} կՎտ հզորության դեպքում։ Չափվել է յուրաքանչյուր անջատման ժամանակ, համեմատական է հզորությանը և '
         'անհետանում է, երբ ինվերտորն անջատված է։'),
 'c2t': ('Supply upstream of A', 'Սնուցող ցանցը մինչև A կետը'),
 'c2p': ('After the trip in E-08 the voltage at A falls by this amount. Exported power raises the voltage at the main '
         'switchboard as well.',
         'E-08 դեպքում անջատումից հետո A կետի լարումն իջնում է այսքանով։ Ցանց տրվող հզորությունը բարձրացնում է լարումը '
         'նաև հիմնական բաշխիչ վահանակում։'),
 'c3t': ('Short rises at A', 'Կարճատև բարձրացումներ A կետում'),
 'c3p': ('For a few seconds before each trip. The record does not show their source.',
         'Մի քանի վայրկյան՝ յուրաքանչյուր անջատումից առաջ։ Գրառումները դրանց աղբյուրը ցույց չեն տալիս։'),
 'concl_h': ('Conclusion', 'Եզրակացություն'),
 'concl_p': ('The feeder uses most of the margin between the normal voltage at A and the {uset} V setting. With a '
             'feeder rise of 3 V at full output, the voltage at B would have stayed below {b_hyp} V during this week, '
             'and the short rises at A would not have tripped the inverter.',
             'A կետի սովորական լարման և {uset} Վ շեմի միջև եղած պաշարի մեծ մասը ծախսվում է մալուխային գծում։ Եթե լրիվ '
             'հզորության դեպքում գծում լարման բարձրացումը լիներ 3 Վ, այս շաբաթվա ընթացքում B կետի լարումը կմնար '
             '{b_hyp} Վ-ից ցածր, և A կետի կարճատև բարձրացումները ինվերտորը չէին անջատի։'),
 'open_h': ('Not established by this record', 'Ինչ չի հաստատվում այս գրառումներով'),
 'open_l': ('Conductor temperature and joint resistance along the feeder.|'
            'Cable reactance and the reactive power of the inverter.|'
            'The source of the short rises at A.|'
            'Whether the {uset} V / {tset} s setting meets the network operator’s requirements for this connection.',
            'Հաղորդչի ջերմաստիճանը և միացումների դիմադրությունը գծի երկայնքով։|'
            'Մալուխի ռեակտիվ դիմադրությունը և ինվերտորի ռեակտիվ հզորությունը։|'
            'A կետում կարճատև բարձրացումների աղբյուրը։|'
            '{uset} Վ / {tset} վրկ կարգաբերման համապատասխանությունը ցանցի օպերատորի պահանջներին։'),
 'other_h': ('Other causes considered', 'Դիտարկված այլ պատճառներ'),
 'other_p': ('The inverter logged an AC overvoltage code at every trip. Its log for the week contains no temperature, '
             'frequency or insulation alarm.',
             'Յուրաքանչյուր անջատման ժամանակ ինվերտորը գրանցել է AC գերլարման կոդ։ Շաբաթվա ընթացքում նրա մատյանում '
             'ջերմաստիճանի, հաճախության կամ մեկուսացման ազդանշան չկա։'),

 # ── 08 шаги
 's8': ('Next steps', 'Քայլեր'),
 'h1_8': ('Recommended next steps', 'Առաջարկվող քայլեր'),
 'act_intro': ('The steps are for the owner, the electrical designer and the PV installer. Gridec supplies the '
               'measured data for each step.',
               'Քայլերը նախատեսված են սեփականատիրոջ, էլեկտրական մասի նախագծողի և արևային կայանի մոնտաժողի համար։ '
               'Յուրաքանչյուր քայլի համար Gridec-ը տրամադրում է չափված տվյալները։'),
 'a1t': ('Keep the protection settings as they are', 'Պաշտպանության կարգաբերումները թողնել անփոփոխ'),
 'a1p': ('Raising U> would hide the cause and may conflict with the connection requirements. Export the present '
         'settings and the event log and keep them with this report.',
         'U> շեմի բարձրացումը կթաքցնի պատճառը և կարող է հակասել միացման պահանջներին։ Արտահանեք ներկա կարգաբերումներն '
         'ու դեպքերի մատյանը և պահեք այս հաշվետվության հետ։'),
 'a2t': ('Have the designer review the A–B feeder', 'Նախագծողին հանձնարարել վերանայել A–B մալուխային գիծը'),
 'a2p': ('Inputs from this report: {e8_du} V rise at {e8_p} kW, {k} V per kW. Options to compare: a larger '
         'cross-section, a second cable in parallel, an inverter position closer to the main switchboard.',
         'Տվյալներ այս հաշվետվությունից՝ {e8_du} Վ բարձրացում {e8_p} կՎտ դեպքում, {k} Վ մեկ կՎտ-ի համար։ Համեմատվող '
         'տարբերակներ՝ ավելի մեծ հատույթ, երկրորդ զուգահեռ մալուխ, ինվերտորի տեղափոխում հիմնական բաշխիչ վահանակին '
         'ավելի մոտ։'),
 'a3t': ('Ask the installer about voltage control in the inverter', 'Մոնտաժողի հետ քննարկել ինվերտորի լարման կարգավորումը'),
 'a3p': ('Active-power reduction P(U) and reactive-power control Q(U) limit the voltage at high output. Both need the '
         'network operator’s consent. The first reduces yield, the second loads the cable with reactive current.',
         'Ակտիվ հզորության սահմանափակումը՝ P(U), և ռեակտիվ հզորության կարգավորումը՝ Q(U), սահմանափակում են լարումը '
         'մեծ հզորության դեպքում։ Երկուսի համար էլ պահանջվում է ցանցի օպերատորի համաձայնությունը։ Առաջինը նվազեցնում '
         'է արտադրությունը, երկրորդը մալուխը բեռնում է ռեակտիվ հոսանքով։'),
 'a4t': ('Raise the voltage rise at A with the network operator', 'Ցանցի օպերատորի հետ քննարկել լարման բարձրացումը A կետում'),
 'a4p': ('Inputs: a rise of about {e8_drop} V at A at full export, and short rises of {sw_lo}–{sw_hi} V at A before '
         'each trip.',
         'Տվյալներ՝ լրիվ հզորությունը ցանց տալիս A կետում մոտ {e8_drop} Վ բարձրացում, և յուրաքանչյուր անջատումից առաջ՝ '
         '{sw_lo}–{sw_hi} Վ կարճատև բարձրացումներ։'),
 'a5t': ('Measure again after the change', 'Փոփոխությունից հետո կրկնել չափումը'),
 'a5p': ('The same two points, for seven days with clear weather and low workshop load, weekend included.',
         'Նույն երկու կետերում, յոթ օր՝ պարզ եղանակին և արհեստանոցի փոքր բեռի պայմաններում, ներառյալ հանգստյան օրերը։'),
 'acc_h': ('How to judge the result', 'Ինչպես գնահատել արդյունքը'),
 'acc_l': ('No U> trips in the repeat week.|'
           'The feeder rise at full output is close to the designer’s calculated value.|'
           'The settings before and after the change are documented.',
           'Կրկնակի չափման շաբաթվա ընթացքում U> անջատումներ չկան։|'
           'Լրիվ հզորության դեպքում գծում լարման բարձրացումը մոտ է նախագծողի հաշվարկային արժեքին։|'
           'Կարգաբերումները՝ փոփոխությունից առաջ և հետո, փաստաթղթավորված են։'),

 # ── 09 рамки
 's9': ('Scope', 'Շրջանակ'),
 'h1_9': ('Scope, deliverables and terms', 'Շրջանակ, հանձնվող նյութեր և տերմիններ'),
 'del_h': ('Delivered with a report', 'Հաշվետվության հետ հանձնվում է'),
 'del_l': ('Signed report, PDF.|Raw data files and the analyser configuration.|Event records.|'
           'Inverter log as exported.|Measurement layout with points A and B.|'
           'Analyser serial numbers and calibration certificates.|Record of clock alignment.',
           'Ստորագրված հաշվետվություն՝ PDF։|Չափումների սկզբնական ֆայլերը և չափիչ սարքի կարգաբերումները։|'
           'Դեպքերի գրառումները։|Ինվերտորի մատյանը՝ արտահանված տեսքով։|Չափման սխեման՝ A և B կետերով։|'
           'Չափիչ սարքերի սերիական համարները և ստուգաչափման վկայականները։|Ժամացույցների համաժամեցման գրառումը։'),
 'out_h': ('Outside the scope', 'Շրջանակից դուրս է'),
 'out_l': ('Insulation, earthing and contact-resistance tests.|Functional tests of protection.|'
           'A statement of conformity for the supply.|Design of the remedy.',
           'Մեկուսացման, հողանցման և կոնտակտային դիմադրության փորձարկումները։|Պաշտպանության գործարկման փորձարկումները։|'
           'Մատակարարվող լարման համապատասխանության հավաստումը։|Լուծման նախագծումը։'),
 'terms_h': ('Terms', 'Տերմիններ'),
 'terms': ('A=Main switchboard. In this report, the point of supply.|B=Inverter AC terminals.|'
           'L2–N=RMS voltage between phase L2 and neutral.|20 ms RMS=RMS value over one cycle at 50 Hz.|'
           'U>=Overvoltage protection stage of the inverter.|'
           'P(U), Q(U)=Control of active and reactive power as a function of voltage.|'
           'Pst, Plt=Short-term (10 min) and long-term (2 h) flicker severity.|'
           'THD(U)=Total harmonic distortion of voltage.',
           'A=Հիմնական բաշխիչ վահանակ։ Այս հաշվետվության մեջ՝ մատակարարման կետ։|B=Ինվերտորի AC սեղմակներ։|'
           'L2–N=L2 ֆազի և չեզոքի միջև լարման գործող (RMS) արժեք։|20 մվրկ RMS=Գործող արժեք մեկ պարբերության համար՝ 50 Հց-ում։|'
           'U>=Ինվերտորի գերլարման պաշտպանության աստիճան։|'
           'P(U), Q(U)=Ակտիվ և ռեակտիվ հզորության կարգավորում՝ կախված լարումից։|'
           'Pst, Plt=Ֆլիկերի կարճատև (10 ր) և երկարատև (2 ժ) չափաբաժին։|'
           'THD(U)=Լարման հարմոնիկ աղավաղման գումարային գործակից։'),
 'stds_h': ('Standards', 'Ստանդարտներ'),
 'stds': ('GOST 32144-2013=Power quality limits in public supply systems.|'
          'EN 50160:2022=Voltage characteristics of public electricity networks.|'
          'IEC 61000-4-30=Power quality measurement methods.|IEC 61000-4-7=Harmonics and interharmonics measurement.|'
          'EN 50549-1=Generating plants connected in parallel with low-voltage networks.|'
          'IEC 60228=Conductors of insulated cables.',
          'ԳՕՍՏ 32144-2013=Էլեկտրաէներգիայի որակի նորմեր ընդհանուր նշանակության ցանցերում։|'
          'EN 50160:2022=Հանրային էլեկտրական ցանցերի լարման բնութագրեր։|'
          'ԳՕՍՏ ԻԷԿ 61000-4-30-2017=Էլեկտրաէներգիայի որակի չափման մեթոդներ։|'
          'ԻԷԿ 61000-4-7=Հարմոնիկների և միջհարմոնիկների չափում։|'
          'EN 50549-1=Ցածր լարման ցանցին զուգահեռ միացվող արտադրող կայանքներ։|'
          'IEC 60228=Մեկուսացված մալուխների հաղորդիչներ։'),
 'about_p': ('Everything in this report is invented: the site, the installation, the measurements and the events. '
             'Four data files are published with it so that every figure can be checked: the 10-minute data, the '
             'inverter event log, the 20 ms record of E-08 and the list of voltage dips. In a real report the same '
             'figures come from the analyser and inverter exports.',
             'Այս հաշվետվության մեջ ամեն ինչ հորինված է՝ չափման վայրը, էլեկտրակայանքը, չափումները և դեպքերը։ '
             'Հաշվետվության հետ հրապարակված է տվյալների չորս ֆայլ, որպեսզի յուրաքանչյուր թիվ հնարավոր լինի ստուգել. '
             '10 րոպեի տվյալները, ինվերտորի դեպքերի մատյանը, E-08 դեպքի 20 մվրկ գրառումը և լարման անկումների ցանկը։ '
             'Իրական հաշվետվության մեջ նույն թվերը վերցվում են չափիչ սարքի և ինվերտորի արտահանված ֆայլերից։'),
}
