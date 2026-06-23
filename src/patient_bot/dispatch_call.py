from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from uuid import uuid4

from dotenv import load_dotenv

from .scenarios import get_scenario

load_dotenv(".env.local")


def main() -> None:
    scenario_id = sys.argv[1] if len(sys.argv) > 1 else "s01"
    scenario = get_scenario(scenario_id)

    agent_name = os.getenv("AGENT_NAME", "pgai-patient-bot")
    room_name = f"pgai-{scenario_id}-{uuid4().hex[:8]}"

    metadata = {
        "scenario_id": scenario_id,
        "scenario_name": scenario["name"],
        "started_at_unix": int(time.time()),
    }

    cmd = [
        "lk",
        "dispatch",
        "create",
        "--new-room",
        "--room",
        room_name,
        "--agent-name",
        agent_name,
        "--metadata",
        json.dumps(metadata),
    ]

    print("Dispatching call:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
