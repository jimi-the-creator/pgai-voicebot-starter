AI Voice QA Bot for Medical Scheduling Agents

This project is an automated voice QA harness for testing medical-office AI phone agents.

It uses a synthetic patient voice agent to call a medical scheduling AI, run realistic patient scenarios, record the calls, save transcripts, and identify quality issues in the agent’s behavior.

What This Project Tests

The system evaluates whether a medical-office voice agent can handle common patient workflows such as:

New patient appointment scheduling
Weekend appointment requests
Rescheduling appointments
Appointment cancellation
Medication refill requests
Insurance questions
Office logistics such as address, hours, parking, and Saturday availability
Ambiguous symptom calls
Emergency escalation
Patient corrections and interruptions
Tech Stack
Python
LiveKit Agents
LiveKit SIP / dispatch
Telnyx outbound SIP trunk
OpenAI Realtime voice model
LiveKit Agent Observability for recordings and transcripts
High-Level Architecture
Synthetic Patient Scenario
        ↓
Python LiveKit Agent
        ↓
OpenAI Realtime Voice Model
        ↓
LiveKit SIP Dispatch
        ↓
Telnyx Outbound SIP Trunk
        ↓
Pretty Good AI Test Line
        ↓
Audio Recording + Transcript + QA Findings
How It Works
A scenario is selected, such as s03 for rescheduling an appointment.
The Python agent joins a LiveKit room.
LiveKit places an outbound SIP call to the assessment phone number.
The OpenAI Realtime model speaks as a realistic patient.
The medical-office AI responds over the phone.
The session is recorded and transcribed.
The transcript and recording are reviewed for bugs or quality issues.
Final Evidence

The final submission includes:

calls/final_recordings/
  s01-new-patient-appointment.oga
  s02-weekend-appointment-request.oga
  s03-reschedule-appointment.oga
  s04-cancel-appointment.oga
  s05-medication-refill.oga
  s06-insurance-question.oga
  s07-office-logistics.oga
  s08-ambiguous-symptoms.oga
  s09-emergency-escalation.oga
  s10-correction-interruption.oga

calls/final_transcripts/
  s01-new-patient-appointment.txt
  s02-weekend-appointment-request.txt
  s03-reschedule-appointment.txt
  s04-cancel-appointment.txt
  s05-medication-refill.txt
  s06-insurance-question.txt
  s07-office-logistics.txt
  s08-ambiguous-symptoms.txt
  s09-emergency-escalation.txt
  s10-correction-interruption.txt

reports/
  BUG_REPORT.md
Key Findings Summary

The test calls found several recurring issues:

The agent often escalated to clinic support instead of completing common workflows.
Identity verification sometimes repeated unnecessarily.
Corrected patient information was not always handled cleanly.
Some patient-provided details, such as phone numbers and dates of birth, were misheard or inconsistently repeated back.
The agent struggled with basic office logistics.
The agent missed the main intent in the ambiguous symptom scenario.
Emergency escalation worked well when the caller reported chest pressure and shortness of breath.

More detail is available in:

reports/BUG_REPORT.md
Safety Note

This project uses synthetic patient scenarios for QA testing. It does not provide medical advice, diagnose patients, or interact with real patient records.

Caller Number Used
+18052698799
Assessment Number Called
+18054398008
Environment Variables

Secrets are stored locally in .env.local and are not committed to the repository.

Required variables include:

LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
OPENAI_API_KEY=
SIP_TRUNK_ID=
CALLER_NUMBER=
TEST_PHONE_NUMBER=
AGENT_NAME=
OPENAI_REALTIME_MODEL=
OPENAI_REALTIME_VOICE=
Running a Scenario

Start the worker:

uv run python -m patient_bot.agent dev

Dispatch one scenario:

uv run python -m patient_bot.dispatch_call s01

Valid scenario IDs:

s01, s02, s03, s04, s05, s06, s07, s08, s09, s10
Project Goal

The goal is to demonstrate an end-to-end voice AI evaluation workflow: realistic patient simulation, outbound phone calling, audio/transcript collection, and actionable QA reporting.