from __future__ import annotations

import os
import subprocess
import time

from dotenv import load_dotenv

from .scenarios import load_scenarios

load_dotenv(".env.local")

CALL_SPACING_SECONDS = int(os.getenv("CALL_SPACING_SECONDS", "220"))


def main() -> None:
    scenarios = load_scenarios()

    for i, scenario in enumerate(scenarios, start=1):
        scenario_id = scenario["id"]
        print(f"\n=== Running {i}/{len(scenarios)}: {scenario_id} - {scenario['name']} ===")

        subprocess.run(
            ["uv", "run", "python", "-m", "patient_bot.dispatch_call", scenario_id],
            check=True,
        )

        if i < len(scenarios):
            print(f"Waiting {CALL_SPACING_SECONDS}s before next call...")
            time.sleep(CALL_SPACING_SECONDS)

    print("\nBatch dispatched. Check calls/transcripts and download recordings.")


if __name__ == "__main__":
    main()
