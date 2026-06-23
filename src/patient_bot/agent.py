from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from dotenv import load_dotenv
from livekit import agents, api
from livekit.agents import Agent, AgentServer, AgentSession
from livekit.plugins import openai

from .reporting import save_session_report
from .scenarios import build_patient_prompt, get_scenario

load_dotenv(".env.local")

AGENT_NAME = os.getenv("AGENT_NAME", "pgai-patient-bot")
TEST_PHONE_NUMBER = os.getenv("TEST_PHONE_NUMBER", "+18054398008")
SIP_TRUNK_ID = os.getenv("SIP_TRUNK_ID")
MAX_CALL_SECONDS = int(os.getenv("MAX_CALL_SECONDS", "180"))

OPENAI_REALTIME_MODEL = os.getenv("OPENAI_REALTIME_MODEL", "gpt-realtime-2")
OPENAI_REALTIME_VOICE = os.getenv("OPENAI_REALTIME_VOICE", "marin")


class PatientAgent(Agent):
    def __init__(self, instructions: str) -> None:
        super().__init__(instructions=instructions)


server = AgentServer()


async def on_session_end(ctx: agents.JobContext) -> None:
    metadata: dict[str, Any] = {}
    if ctx.job.metadata:
        try:
            metadata = json.loads(ctx.job.metadata)
        except json.JSONDecodeError:
            metadata = {}

    scenario_id = metadata.get("scenario_id", "unknown")

    try:
        report = ctx.make_session_report()
    except RuntimeError as e:
        print(f"No session report saved for {scenario_id}: {e}")
        return

    save_session_report(ctx.room.name, scenario_id, report.to_dict())


async def shutdown_after(ctx: agents.JobContext, seconds: int) -> None:
    await asyncio.sleep(seconds)
    print(f"Max call time reached ({seconds}s). Shutting down room.")
    ctx.shutdown(reason="max_call_time_reached")


@server.rtc_session(agent_name=AGENT_NAME, on_session_end=on_session_end)
async def entrypoint(ctx: agents.JobContext):
    if not SIP_TRUNK_ID:
        raise RuntimeError("Missing SIP_TRUNK_ID in .env.local")

    metadata: dict[str, Any] = {}
    if ctx.job.metadata:
        try:
            metadata = json.loads(ctx.job.metadata)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid dispatch metadata JSON: {ctx.job.metadata}") from exc

    scenario_id = metadata.get("scenario_id", "s01")
    scenario = get_scenario(scenario_id)
    patient_prompt = build_patient_prompt(scenario)

    print(f"Starting scenario {scenario_id}: {scenario['name']}")
    print(f"Calling assessment number: {TEST_PHONE_NUMBER}")

    asyncio.create_task(shutdown_after(ctx, MAX_CALL_SECONDS))

    sip_identity = "pgai-test-line"

    try:
        await ctx.api.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id=SIP_TRUNK_ID,
                sip_call_to=TEST_PHONE_NUMBER,
                participant_identity=sip_identity,
                participant_name="Pretty Good AI Test Line",
                krisp_enabled=True,
                wait_until_answered=True,
            )
        )
    except api.TwirpError as e:
        print("Failed to create SIP participant.")
        print("Message:", e.message)
        print("SIP status code:", e.metadata.get("sip_status_code"))
        print("SIP status:", e.metadata.get("sip_status"))
        ctx.shutdown(reason="sip_participant_create_failed")
        return

    await ctx.wait_for_participant(identity=sip_identity)

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            model=OPENAI_REALTIME_MODEL,
            voice=OPENAI_REALTIME_VOICE,
        )
    )

    await session.start(
        room=ctx.room,
        agent=PatientAgent(patient_prompt),
        record=True,
    )

    await session.generate_reply(
        instructions=(
            "The call has connected. Begin naturally as the patient. "
            f"Your opening line is: {scenario['opening']}"
        )
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
