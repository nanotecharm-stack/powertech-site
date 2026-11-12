# For Partners (EN) — review and rewrite

Source reviewed: `site/partners/index.html` at commit `cae452b` (the published version). Date: 2026-11-12.

---

## Part A — Critical review

**Overall.** The page is short, restrained and free of the usual marketing vocabulary. Its weaknesses are different: three sections built on one template, several claims that go further than measurement can support, and a few terms an engineer would correct.

### Structure

All three sections follow the same pattern: imperative heading, a paragraph on the problem, then "Gridec measures / checks … We also …". Two sentences are near-duplicates:

- 01: "Gridec measures power quality, identifies the source of problems and recommends practical technical solutions."
- 03: "Gridec measures power quality, identifies recurring disturbances and recommends technical solutions to reduce electrical risks."

A reader who scans all three sees one argument repeated, not three cases.

### Language

| Phrase | Problem | Direction |
|---|---|---|
| "Make sure electrical systems work as intended." | Could head any electrical contractor's page. It also tells engineers to do what they already do. | Say what Gridec supplies to them: measurements. |
| "recommends practical technical solutions" | Vague. "Practical" and "technical" add nothing to "solutions". | Name the actual output, or remove. |
| "Check electrical conditions before installing expensive equipment." | "Expensive" is conversational. The lessor does not install the equipment. | Address the lessor's position: the supply the asset will be connected to. |
| "cause shutdowns, damage equipment and disrupt production" | A list of three where the first and third say the same thing. | One concrete consequence is enough. |
| "issues that were not apparent during initial testing" | "Initial testing" is undefined. | "No-load tests" or "pre-commissioning tests". |

None of the text reads as machine-written. The fault is sameness, not style.

### Technical accuracy

| Phrase | Problem |
|---|---|
| "Motor starts, generator changeovers and harmonics can reveal issues" | Category error. Motor starts and changeovers are events. Harmonics are a disturbance, not an event that reveals one. |
| "identifies the source of problems" | Too firm. Measurement often shows whether a disturbance originates upstream or downstream, and often points to the equipment. It does not always. |
| "Voltage fluctuations, phase imbalance" | "Voltage fluctuations" has a narrow meaning (the cause of flicker). The intended sense is probably dips and swells. The established term is "voltage unbalance". |
| "Identify electrical risks before equipment fails." | Implies prediction. Power quality measurement covers supply disturbances. It does not cover insulation condition, earthing, protection settings or fire risk. |
| "provide and integrate monitoring systems" (03) vs "help select and integrate" (01) | Inconsistent. "Provide" implies Gridec sells hardware. |

### Commercial positioning

- **Engineering firms.** "Recommends practical technical solutions" places Gridec in the firm's own territory. Nothing on the page says Gridec will work as a subcontractor or that design and installation stay with the partner.
- **Leasing companies.** "Helping investigate failures and resolve disputes" overstates. A record informs a dispute; it does not resolve one. The text also never states the lessor's interest: the lessor owns an asset on a site it does not control.
- **Insurance companies.** The section does not mention claims, adjusters or loss. "Reduce electrical risks" is broader than the service. An insurer reading it could take Gridec for an electrical safety auditor.

---

## Part B — Final website copy

### For Partners

**01 — Engineering Firms & System Integrators**

**Power quality measurements for your projects.**

Some problems appear only under working load: voltage dips on motor starts, voltage and frequency deviations at generator changeover, harmonic distortion from drives and rectifiers. No-load tests do not show them.

Gridec works as your subcontractor or alongside your team. We record baseline conditions before new equipment goes in, investigate disturbances on operating sites and repeat the measurements after corrective work to show what changed. Design and installation remain yours. We also prepare measurement reports for commissioning and handover, and supply and integrate permanent monitoring where a project needs it.

**02 — Leasing Companies**

**Know the supply before the equipment is connected.**

CNC machines, production lines and medical equipment are specified for a supply within stated limits. Whether the lessee's site stays within them is a separate question, and it is easier to answer before delivery than after a failure.

Gridec measures the supply at the point of connection before commissioning and compares it with the manufacturer's stated requirements. That report is the baseline. For higher-value assets, a permanent monitor keeps a time-stamped record for the lease term. Gridec holds the data, and every party to the lease has access to it. If the equipment faults, or a dispute follows, the record shows what the supply was doing at the time.

**03 — Insurance Companies**

**Measured electrical conditions, before and after a loss.**

Voltage dips, unbalance, harmonic distortion and transients do not show up in a routine inspection. They can trip drives, overheat motors and transformers and damage electronics, and they leave no record unless an instrument is logging.

Gridec assesses power quality at insured facilities and reports which disturbances occur, how often and how severe. Where a monitor is installed, its event records can be compared with the time of a failure. This is evidence for your adjusters and experts to weigh, not a finding on cause. The scope is power quality; it is not an electrical safety inspection.

**Discuss a Partnership ↗**

**Meta description**

Power quality measurement and monitoring for engineering firms, system integrators, leasing companies and insurers: baseline surveys, disturbance investigation and verification after corrective work.

---

## Part C — Explanation of changes

1. **Three arguments instead of one.** Engineers get a division of labour. Leasing managers get a before-and-after record for an asset on someone else's site. Insurers get evidence with stated limits. Headings are no longer three imperatives.
2. **"Recommends technical solutions" removed from all sections.** For engineering firms it read as competition; "Design and installation remain yours" now says the opposite in plain words. For insurers it was too broad.
3. **"Identifies the source of problems" removed.** Replaced with what is always true: Gridec records, investigates and reports.
4. **"Resolve disputes" softened.** The record "shows what the supply was doing at the time". Responsibility is left to the parties.
5. **"Identify electrical risks before equipment fails" removed.** No prediction is implied. The insurance section states its own scope limit and says the evidence is for the insurer's people to weigh.
6. **Terminology corrected.** "Voltage unbalance", "voltage dips", "transients", "point of connection". Harmonics are tied to their usual sources (drives, rectifiers).
7. **"Provide monitoring systems" removed.** The copy now says "help select and integrate" (01) and "a monitor is installed" (02, 03). It makes no statement on who supplies hardware.
8. **Length.** Section 01 is close to the original. Sections 02 and 03 are about 25 words longer each. The extra words carry the baseline idea and the scope limits, which the brief asked for.
9. **Not added.** No standards, instrument classes, accreditations, client names or project counts.

---

## Part D — Questions before publication

Owner's answers, 2026-11-12: (1) Gridec sells monitoring equipment. (2) Yes. (3) Gridec holds the records; all parties have access. (5) The Armenian page will change on the owner's instructions. Question 4 is open. Part B above includes answers 1 and 3.

1. **Hardware.** Does Gridec sell monitoring equipment, or only select, install and commission it? The new copy avoids the point.
2. **Subcontracting.** Will Gridec work under an engineering firm's contract, with reports issued to the firm and not to the end client? Section 01 says yes.
3. **Monitoring data.** During a lease, who holds the records: Gridec, the lessor or the lessee? Section 02 says only that a record is kept.
4. **Recommendations.** Gridec no longer offers "technical solutions" on this page. Is that correct for partners, or should corrective recommendations stay as an option at the partner's request?
5. **Armenian page.** `/hy/partners/` still carries the old argument. Should it follow this version?
