# -*- coding: utf-8 -*-
"""Редакторские правки, этап 1 (бриф владельца 2026-09-14): EN+HY тексты в build.py,
форма и подписи в shell.html. Каждая замена с assert — повторный запуск падает."""
import re, io, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
B = 'build.py'; S = 'shell.html'
b = io.open(B, encoding='utf-8').read(); s = io.open(S, encoding='utf-8').read()

def rep(txt, old, new, n=1):
    c = txt.count(old); assert c == n, (c, old[:70]); return txt.replace(old, new)

def rrep(txt, pat, new, n=1):
    c = len(re.findall(pat, txt)); assert c == n, (c, pat[:70]); return re.sub(pat, lambda m: new, txt)

# 2.1 генератор/UPS
b = rep(b, "'We measure the operating load and starting currents of the equipment that needs backup power. These measurements help your supplier select the right capacity.'",
        "'We measure the operating load and starting currents of the equipment that needs backup power under agreed operating conditions. These measurements help your supplier select the required capacity.'", 2)
b = rep(b, "'Չափում ենք սարքավորումների փաստացի բեռնվածությունն ու մեկնարկային հոսանքները՝ աշխատանքային ամբողջ ցիկլի ընթացքում։ Այս տվյալներն օգնում են մատակարարին որոշել անհրաժեշտ հզորությունը։'",
        "'Չափում ենք պահուստային սնուցման ենթակա սարքավորումների բեռնվածությունն ու մեկնարկային հոսանքները՝ համաձայնեցված աշխատանքային ռեժիմներում։ Այս տվյալներն օգնում են մատակարարին ընտրել անհրաժեշտ հզորությունը։'", 2)
# 2.2 приёмка (HY)
b = rrep(b, r"'Չափում ենք էլեկտրասնուցման պարամետրերն ու բեռնվածությունը՝ սարքավորումների միաժամանակյա[^']*'",
         "'Չափում ենք էլեկտրասնուցման պարամետրերն ու բեռնվածությունը՝ համաձայնեցված աշխատանքային ռեժիմներում։ Հաշվետվությունն օգնում է մինչև սարքավորման ընդունումը մատակարարի հետ քննարկել չափումների արդյունքները։ Գրանցված տվյալները հետագայում ծառայում են որպես համեմատության հիմք՝ փոփոխությունների կամ խափանումների պատճառները պարզելիս։'", 2)
# 2.3 гармоники, карточка производства
b = rep(b, "'Հարմոնիկայի չափում։ Դրա առկայության հնարավոր ազդեցությունները։'",
        "'Ռեակտիվ հզորության և հարմոնիկ աղավաղման գնահատում՝ պարզելու համար, թե արդյոք լրացուցիչ ինժեներական ուսումնասիրություն է անհրաժեշտ։'")
b = rep(b, "'Whether reactive power or harmonic distortion requires further engineering review.'",
        "'Assessment of reactive power and harmonic distortion to determine whether further engineering investigation is needed.'")
# 2.4 «7» с единицей
b = rep(b, "('7', 'մոնիթորինգի տևողություն')", "('7', 'օր մոնիթորինգ')")
# 2.5 Dips & Swells по-армянски; «постоянный мониторинг как услуга» = մշտական
b = rep(b, "'Լարման անկումներ', 'Լարման անհամաչափություն'", "'Լարման կարճատև անկումներ և բարձրացումներ', 'Լարման անհամաչափություն'")
b = rep(b, "'Ժամանակավոր կամ շարունակական մոնիթորինգը", "'Ժամանակավոր կամ մշտական մոնիթորինգը")
# 2.6 подписи графика: кривая нарисована руками, оси времени нет → иллюстративный пример
b = rep(b, "'CT_CAP': 'RMS VOLTAGE · TYPICAL TRACE'", "'CT_CAP': 'RMS voltage · illustrative example'")
b = rep(b, "'CT_CAP': 'RMS լարում · 10-րոպեանոց միտում', 'CT_NOM': 'Անվանական'", "'CT_CAP': 'RMS լարում · պատկերային օրինակ', 'CT_NOM': 'Անվանական լարում'")
# 3 процесс (HY) + этапы EN
b = rep(b, "'SVC_P2': 'Մոնիթորինգի տևողությունն ընտրվում է աշխատանքային պայմանների բնորոշ պատկերը ստանալու համար։ Եթե խնդիրը պարբերաբար չի դրսևորվում կամ սարքավորման աշխատանքային ցիկլն ավելի երկար է, կարող է առաջարկվել ավելի երկար ժամանակահատված։'",
        "'SVC_P2': 'Մոնիթորինգի տևողությունն ընտրում ենք այնպես, որ գրանցենք համակարգի բնորոշ աշխատանքային ռեժիմները։ Եթե խնդիրը հազվադեպ կամ անկանոն է դրսևորվում, կամ աշխատանքային ցիկլն ավելի երկար է, առաջարկում ենք երկարացնել չափումների ժամանակահատվածը։'")
b = rep(b, "('01', 'Հստակեցնում ենք՝ ինչ պետք է ստուգվի, որ սարքավորումն է ներգրավված և ինչ որոշման պետք է աջակցեն արդյունքները։')",
        "('01', 'Նախ հստակեցնում ենք՝ ինչ ենք ստուգելու, որ սարքավորումների վրա և ինչ որոշում եք կայացնելու արդյունքների հիման վրա։')")
b = rep(b, "('02', 'Չափումները կատարվում են էլեկտրական համակարգի աշխատանքի ընթացքում՝ բնորոշ աշխատանքային պայմաններում։')",
        "('02', 'Չափումները կատարում ենք համակարգի աշխատանքի ընթացքում՝ ընդգրկելով համաձայնեցված աշխատանքային ռեժիմները։')")
b = rep(b, "('03', 'Արդյունքները գնահատվում են խնդրի համատեքստում և ներկայացվում տեխնիկական հաշվետվությամբ՝ գրանցված տվյալներով հիմնավորված եզրահանգումներով։')",
        "('03', 'Վերլուծում ենք գրանցված տվյալները և հաշվետվության մեջ ներկայացնում եզրակացություններն ու առաջարկվող քայլերը։')")
b = rep(b, "('01', 'Before anything is connected, we agree what needs verifying, on which equipment, and what the answer is for.')",
        "('01', 'Before monitoring starts, we agree on the equipment to assess, the measurements required and the decision the results will support.')")
b = rep(b, "('02', 'Measurements are carried out while the electrical system operates under representative operating conditions.')",
        "('02', 'We take measurements during the agreed operating conditions.')")
b = rep(b, "('03', 'We read the record against the question we started with, and write up the conclusions.')",
        "('03', 'We analyse the recorded data and present our conclusions and recommended next steps in the report.')")
# 4 первый экран, раздел 01, отрасли, пояснение к величинам
b = rep(b, "The report gives you the findings and our recommendation.'", "The report presents our findings and recommended next steps.'")
b = rep(b, "'WHY_H2': 'The event may be over before anyone can inspect it'", "'WHY_H2': 'A brief voltage dip can be missed during an inspection'")
b = rep(b, "'WHY_H2': 'Իրադարձությունը կարող է ավարտվել դեռևս ստուգումը սկսելուց առաջ'", "'WHY_H2': 'Լարման կարճատև անկումը կարող է չերևալ ստուգման պահին'")
b = rep(b, "'WHY_P': 'A voltage event can last a few cycles. An hour later a spot check reads normal and there is nothing left on site to find. A continuous recording captures it, with a time stamp and the load conditions before and after.'",
        "'WHY_P': 'A voltage dip can last only a few cycles. A later spot check may show normal readings. Continuous monitoring records the event and when it occurred, allowing us to analyse the measured conditions.'")
b = rep(b, "'WHY_P': 'Էլեկտրական համակարգում որոշ իրադարձություններ տևում են ընդամենը միլիվայրկյաններ կամ մի քանի ցիկլ։ Մեկանգամյա կարճատև ստուգման պահին չափվող արժեքները կարող են արդեն վերադարձած լինել բնականոն մակարդակի։ Մոնիթորինգը պահպանում է իրադարձության ժամանակային նշումը և դրա պահին գրանցված պայմանները։'",
        "'WHY_P': 'Լարման անկումը կարող է տևել ընդամենը մի քանի պարբերություն։ Հետագա ստուգման պահին լարումն արդեն կարող է բնականոն լինել։ Անընդհատ մոնիթորինգը գրանցում է իրադարձությունը, դրա ժամանակը և չափված պարամետրերը՝ հետագա վերլուծության համար։'")
b = rep(b, "'APP_P': 'The sector matters less than the question. Monitoring is worth doing when supply conditions are affecting equipment or output, or when a decision has to rest on measurements.'",
        "'APP_P': 'Monitoring helps when power quality affects equipment or operations, or when you need measurements to make a technical decision.'")
b = rep(b, "'APP_P': 'Էլեկտրաէներգիայի որակի խնդիրները չեն սահմանափակվում մեկ ոլորտով։ Մոնիթորինգը կիրառելի է, երբ էլեկտրաէներգիայի որակն ազդում է սարքավորումների կամ աշխատանքային գործընթացների վրա, կամ երբ ինժեներական որոշման համար անհրաժեշտ են չափված և գրանցված տվյալներ։'",
        "'APP_P': 'Մոնիթորինգն օգնում է, երբ էլեկտրաէներգիայի որակն ազդում է սարքավորումների կամ աշխատանքային գործընթացների վրա, կամ երբ տեխնիկական որոշում կայացնելու համար անհրաժեշտ են չափումների տվյալներ։'")
b = rep(b, "lnote_html('The last cell is not a measurement: risk is what we read from the other seven.')",
        "lnote_html('We assess potential equipment risks using the recorded data and operating conditions.')")
b = rep(b, " 'MEA_NOTE': lnote_html(''),", " 'MEA_NOTE': lnote_html('Գրանցված տվյալների և աշխատանքային պայմանների հիման վրա գնահատում ենք սարքավորումների հնարավոր ռիսկերը։'),")
# 5 о компании
b = rep(b, """    ('Ինչպես ենք մտածում',
     'Ինժեներական աշխատանքը սկսվում է ճիշտ հարցերից՝ հասկանալով, թե ինչպես է իրականում աշխատում համակարգը, և եզրակացությունները հիմնավորելով չափումների տվյալներով։ Նպատակը ամեն գնով խնդիր գտնելը չէ։ Երբեմն ամենաօգտակար արդյունքը հաստատելն է, որ համակարգն աշխատում է այնպես, ինչպես պետք է։'),
    ('Ինչ ենք կառուցում',
     'Gridec-ը ստեղծում ենք երկարաժամկետ նպատակով։ Ուզում ենք, որ մեր աշխատանքը ճանաչվի ճշգրտությամբ, հստակ հաղորդակցությամբ և տվյալներով հիմնավորված տեխնիկական եզրակացություններով։')]),""",
        """    ('Ինչպես ենք աշխատում',
     'Նախ հստակեցնում ենք՝ ինչ պետք է պարզել։ Այնուհետև չափում ենք էլեկտրական պարամետրերը և վերլուծում տվյալները՝ հաշվի առնելով համակարգի աշխատանքային ռեժիմները։ Եզրակացություններում նշում ենք նաև չափումների սահմանափակումները։'),
    ('Ինչով ենք հիմնավորում եզրակացությունները',
     'Հաշվետվություններում ներկայացնում ենք գրանցված տվյալները, չափումների պայմաններն ու վերլուծությունը, որոնց վրա հիմնված են եզրակացությունները։ Այս տեղեկություններով կարող եք արդյունքները քննարկել ձեր ինժեների կամ սարքավորումների մատակարարի հետ։')]),""")
b = rep(b, """    ('HOW WE WORK',
     'A useful investigation starts with the question that needs answering. We measure the system under real operating conditions and base the conclusion on what the data shows, whether that points to a problem or confirms normal operation.'),
    ('WHAT WE ARE BUILDING',
     'We are building Gridec in Armenia as a small engineering firm whose conclusions hold up when someone checks them. We would rather grow slowly than lose that.')]),""",
        """    ('HOW WE WORK',
     'We first agree on what needs to be established. We then measure the electrical parameters and analyse the data alongside the system’s operating conditions. Our conclusions also explain the limitations of the measurements.'),
    ('HOW WE SUPPORT OUR CONCLUSIONS',
     'Our reports present the recorded data, measurement conditions and analysis behind our conclusions, so you can review the findings with your engineer or equipment supplier.')]),""")
# 6 отчёт (EN пункт 2)
b = rep(b, "'Monitoring period and operating context'", "'Monitoring period and operating conditions'")
# 7 форма
b = rep(b, "'F_CONTACT': 'Կոնտակտային տվյալներ'", "'F_CONTACT': 'Կապի տվյալներ'")
b = rep(b, "'F_SEND': 'Ուղարկել տվյալները'", "'F_SEND': 'Ուղարկել'")
b = rep(b, "'F_MSG_PH': 'Կարճ նկարագրեք՝ ինչ է տեղի ունեցել, երբ եք դա նկատել և ինչ սարքավորման վրա։'", "'F_MSG_PH': 'Նշեք՝ ինչ է տեղի ունեցել, երբ եք դա նկատել և որ սարքավորման աշխատանքում։'")
# вводная строка HY повторяла подсказку поля слово в слово (на EN снята по той же причине)
b = rep(b, "'F_INTRO': intro_html('Նշեք՝ ինչ է տեղի ունեցել, երբ է դա նկատվել և ինչ սարքավորման վրա։')", "'F_INTRO': intro_html('')")
b = rep(b, "'F_OK_P': 'Մենք կուսումնասիրենք տրամադրված տեղեկատվությունը և կկապվենք ձեզ հետ՝ չափումների շրջանակը հստակեցնելու համար։'", "'F_OK_P': 'Կուսումնասիրենք ձեր հարցումը և կկապվենք ձեզ հետ՝ մանրամասները ճշտելու համար։'")
b = rep(b, "'F_OK_P': 'We will review the information and contact you to clarify the measurement scope.'", "'F_OK_P': 'We will review your enquiry and contact you to clarify the details.'")
b = rep(b, "'Ձևն առաքվում է FormSubmit երրորդ կողմի ծառայության միջոցով։ '", "'Ձեր հաղորդագրությունն ուղարկվում է FormSubmit ծառայության միջոցով։ '")
b = rep(b, "'F_ONE_CONTACT': 'Email or phone — at least one, so that we can reply.'", "'F_ONE_CONTACT': 'Email or phone: at least one, so that we can reply.'")
b = rep(b, "'CT_H2': 'Start with what happened'", "'CT_H2': 'Tell us what you need to assess'")
b = rep(b, "'CT_H2': 'Ներկայացրեք խնդիրը նախնական գնահատման համար'", "'CT_H2': 'Նկարագրեք ձեր խնդիրը'")
# 8 политика
b = rep(b, "'does — nothing beyond that.'", "'does.'")
b = rep(b, "'նկարագրում է կայքի իրական աշխատանքը՝ ոչ ավելին։'", "'նկարագրում է կայքի իրական աշխատանքը։'")
b = rep(b, "   'We do not claim protection beyond that. Ordinary email should not be treated as a '\n", "   'Ordinary email should not be treated as a '\n")
b = rep(b, "   'Դրանից ավելին չենք հավաստիացնում։ Սովորական էլեկտրոնային փոստը չպետք է դիտարկել '\n", "   'Սովորական էլեկտրոնային փոստը չպետք է դիտարկել '\n")
b = rep(b, "'date below. A material change will be described here rather than made quietly.'", "'date below. We will describe any material changes on this page.'")
b = rep(b, "'Էական փոփոխությունն այստեղ կնկարագրվի, այլ ոչ թե կկատարվի լուռ։'", "'Էական փոփոխությունները կներկայացնենք այս էջում։'")
b = rep(b, "'Եթե հարցումը վերածվում է պայմանագրի, առնչվող փաստաթղթերը պահում ենք այնքան, '", "'Եթե հարցման արդյունքում պայմանագիր է կնքվում, առնչվող փաստաթղթերը պահում ենք այնքան, '")
b = rep(b, """   'The form service is a third-party service, so the contents of the form may cross a '
   'border when you send it. If you would rather they did not, email us directly '
   'at <a href="mailto:sales@gridec.am">sales@gridec.am</a> instead of using the '
   'form.']),""",
        """   'The form service is a third-party service, so the data may be transferred outside '
   'Armenia when you send the form. You can also contact us directly '
   'at <a href="mailto:sales@gridec.am">sales@gridec.am</a>.']),""")
b = rep(b, """   'Ձևի ծառայությունը երրորդ կողմի ծառայություն է, ուստի ձևն ուղարկելիս դրա '
   'պարունակությունը կարող է հատել սահմանը։ Եթե նախընտրում եք դրանից '
   'խուսափել, ձևի փոխարեն գրեք ուղիղ '
   '<a href="mailto:sales@gridec.am">sales@gridec.am</a> հասցեին։']),""",
        """   'Ձևի ծառայությունը երրորդ կողմի ծառայություն է, ուստի ձևն ուղարկելիս տվյալները '
   'կարող են փոխանցվել Հայաստանից դուրս։ Մեզ կարող եք դիմել նաև ուղիղ՝ '
   '<a href="mailto:sales@gridec.am">sales@gridec.am</a> հասցեով։']),""")
b = rep(b, "'PP_UPD': 'Last updated 17 August 2026'", "'PP_UPD': 'Last updated 14 September 2026'")
b = rep(b, "'PP_UPD': 'Թարմացվել է՝ 2026 թ. օգոստոսի 17'", "'PP_UPD': 'Թարմացվել է՝ 2026 թ. սեպտեմբերի 14'")
# форма: звёздочка не на каждом из двух полей, а на группе «почта ИЛИ телефон»
s = rep(s, '<div class="ghd">%%F_CONTACT%%</div>', '<div class="ghd">%%F_CONTACT%% <em>*</em></div>')
s = rep(s, '<label for="ptfEmail">%%F_EMAIL%% <em>*</em></label>', '<label for="ptfEmail">%%F_EMAIL%%</label>')
s = rep(s, '<label for="ptfPhone">%%F_PHONE%% <em>*</em></label>', '<label for="ptfPhone">%%F_PHONE%%</label>')
io.open(B, 'w', encoding='utf-8', newline='\n').write(b); io.open(S, 'w', encoding='utf-8', newline='\n').write(s)
print('patched OK')
