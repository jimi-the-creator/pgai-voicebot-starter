Pretty Good AI Voice Agent QA Report
Overview

This report summarizes 10 recorded patient-simulation calls made to the Pretty Good AI assessment line. The test harness used a synthetic patient voice agent to call the medical-office AI, run realistic scheduling/support scenarios, save transcripts, and collect audio recordings.

Caller number used: +18052698799
Assessment number called: +18054398008
Total completed scenarios: 10
Artifacts included: 10 audio recordings and 10 matching transcripts

Scenario Coverage
Scenario	Purpose	Result Summary
s01 — New patient appointment	Test basic appointment scheduling	Partially handled, but booking failed and escalated
s02 — Weekend appointment request	Test weekend availability handling	Escalated instead of clearly answering availability
s03 — Reschedule appointment	Test rescheduling flow	Repeated DOB prompt and escalated without completing reschedule
s04 — Cancel appointment	Test cancellation flow	Repeated identity collection and escalated without completing cancellation
s05 — Medication refill	Test refill request workflow	Included as a refill workflow test with transcript/audio evidence
s06 — Insurance question	Test insurance/benefits handling	Misheard phone number and did not answer insurance question
s07 — Office logistics	Test address, parking, hours, Saturday availability	Failed to provide basic office logistics and escalated
s08 — Ambiguous symptoms	Test mild symptom triage / uncertainty handling	Missed the symptom intent and escalated due to record access
s09 — Emergency escalation	Test urgent chest-pressure symptoms	Passed; gave appropriate 911/ER guidance
s10 — Interruption and correction	Test corrected DOB/name and messy patient flow	Partially handled correction but repeated verification and escalated
Key Findings
Finding 1 — Over-escalation instead of completing common workflows

Observed in: s01, s02, s03, s04, s07, s08, s10

Across multiple routine scenarios, the agent moved to clinic support escalation instead of completing or meaningfully advancing the workflow.

Examples:

In s03, the caller asked to reschedule a Friday 3 PM appointment to Monday morning. The agent collected identity information but then transferred instead of completing or attempting the reschedule.
In s04, the caller clearly wanted to cancel an appointment and not reschedule. The agent repeated identity prompts and then escalated.
In s07, the caller asked for office address, parking details, hours, and Saturday availability. The agent said it could not pull up the address and escalated.
In s08, the caller reported mild stomach discomfort and asked whether they should come in. The agent did not ask symptom follow-up questions and escalated due to record access.

Impact:
The agent may not reliably complete common front-desk tasks such as scheduling, rescheduling, cancellation, office logistics, or basic triage intake. This creates a poor patient experience and reduces the value of automation.

Finding 2 — Repeated or fragile identity verification

Observed in: s03, s04, s06, s10

The agent often repeated identity-verification questions even after the caller had already answered or corrected the information.

Examples:

In s03, the agent repeated: “Please tell me your date of birth” twice.
In s04, the agent asked for name/DOB multiple times even after Robert Kim confirmed his information.
In s10, Noah corrected his DOB from March 4 to March 14, but the agent still asked whether March 4 was correct immediately afterward.
In s06, the caller gave phone number 415-555-1287, but the agent repeated it back as 415-555-1285.

Impact:
Repeated or incorrect identity confirmation can frustrate patients, increase call time, and create trust issues. For healthcare workflows, accurate patient identification is especially important.

Finding 3 — Incorrect or incomplete capture of patient-provided details

Observed in: s06, s10

The agent sometimes failed to reliably incorporate corrected or spoken information.

Examples:

In s06, the phone number was repeated back incorrectly.
In s10, the patient corrected the DOB, but the agent’s next response still referenced the incorrect date.

Impact:
Incorrect capture of patient details can break downstream workflows, prevent record lookup, and cause unnecessary escalation.

Finding 4 — Failure to answer basic office logistics

Observed in: s07

The caller asked for office address, parking details, hours, and Saturday appointment availability. The agent was unable to provide the address and escalated to patient support.

Impact:
Address, hours, parking, and weekend availability are common front-desk questions. The agent should ideally answer these directly or clearly state what it can and cannot verify.

Finding 5 — Missed symptom-triage opportunity for non-emergency symptoms

Observed in: s08

The caller described mild stomach discomfort for two days and asked whether they should come in. The agent did not ask clarifying questions such as severity, duration, fever, worsening symptoms, or red flags. Instead, it treated the call primarily as a record-access issue and escalated.

Impact:
For ambiguous symptoms, the agent should avoid diagnosis but still follow a safe triage workflow: ask clarifying questions, check urgent warning signs, and recommend appropriate next steps or escalation.

Finding 6 — Emergency escalation worked well

Observed in: s09

The caller reported chest pressure and shortness of breath. The agent correctly recognized that these symptoms could be serious and advised the caller to call 911 or go to the nearest emergency room.

Impact:
This was the strongest safety behavior observed. The agent avoided treating the call as a normal scheduling request and gave appropriate emergency guidance.

Overall Assessment

The agent performed well on explicit emergency escalation, but struggled with several routine front-desk workflows. The most common pattern was collecting identity information, failing to complete the requested task, and escalating to clinic support.

The most important improvement areas are:

Reduce repeated identity-verification loops.
Improve handling of corrected patient information.
Complete common workflows before escalating.
Provide basic office logistics directly when available.
Add safer structured triage behavior for ambiguous non-emergency symptoms.
Improve reliability of phone-number and DOB capture.
Included Evidence

The final submission includes:

calls/final_recordings/ — 10 audio recordings
calls/final_transcripts/ — 10 matching transcripts

Each recording/transcript pair is named by scenario for easier review.