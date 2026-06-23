from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCENARIOS_PATH = ROOT / "scenarios.yaml"


def load_scenarios() -> list[dict[str, Any]]:
    with SCENARIOS_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        raise ValueError("scenarios.yaml must contain a list")
    return data


def get_scenario(scenario_id: str) -> dict[str, Any]:
    for scenario in load_scenarios():
        if scenario.get("id") == scenario_id:
            return scenario
    known = ", ".join(s["id"] for s in load_scenarios())
    raise ValueError(f"Unknown scenario_id={scenario_id!r}. Known: {known}")


def build_patient_prompt(scenario: dict[str, Any]) -> str:
    must_test = "\n".join(f"- {x}" for x in scenario.get("must_test", []))
    return f'''
You are a realistic patient calling a medical office AI agent.

You are NOT the office assistant. You are the caller/patient.

Scenario:
- ID: {scenario["id"]}
- Name: {scenario["name"]}
- Persona: {scenario["persona"]}
- Goal: {scenario["goal"]}
- Steering: {scenario["steering"]}

Bug/quality probes:
{must_test}

Conversation rules:
- Sound like a real human on the phone, not like a benchmark.
- Keep each response short: usually 1 sentence, max 2.
- Do not dump all information at once. Let the office agent ask.
- Stay coherent and steer toward the scenario goal.
- Give realistic fake personal details when asked.
- Do not reveal that you are an AI, a bot, or testing system unless the office agent directly accuses you.
- If the office agent asks whether this is an emergency, answer according to the scenario.
- If the scenario goal is complete, politely end the call.
- If the office agent gets stuck, rephrase once.
- If the agent gives a wrong or unsafe response, continue naturally so the transcript captures the bug.
'''.strip()
