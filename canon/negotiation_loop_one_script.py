"""
NEGOTIATION LOOP (ONE SCRIPT VERSION)

This script shows how to:
- limit the number of negotiation rounds (MAX_ROUNDS)
- control reporting behavior:
    - REPORT_EACH_ROUND  (short status each cycle)
    - REPORT_AT_END      (final summary at the end)

You only really need to edit the CONFIG section.
"""

import json

# ==========================
# CONFIG (YOU CAN CHANGE THIS)
# ==========================

# How many full cycles of A?B?C you want at most
MAX_ROUNDS = 5          # e.g. 5, 10, 20...

# Do you want a summary after each round?
REPORT_EACH_ROUND = False   # True or False

# Do you want a final summary at the end?
REPORT_AT_END = True        # True or False

# Which agents are participating?
AGENTS = ["Alpha", "Beta", "Gamma"]   # or ["Alpha", "Beta"]


# ==========================
# END OF CONFIG
# (Below here, you don't need to edit anything unless you want to.)
# ==========================


def call_agent(agent_name, team_chat, negotiation_state_text):
    """
    PSEUDOCODE PLACEHOLDER:
    This is where you'd call the LLM.

    Expected behavior:
      - You send:
          - agent_name (role)
          - current TEAM_CHAT
          - current NEGOTIATION_STATE (as text)
          - plus your PLAN_NEGOTIATION_LOOP instructions
      - The model returns:
          - agent_message (what it "says" into the chat)
          - proposed_state_update (dict), can be empty {}
          - loop_status: "CONTINUE" or "DONE"

    For now this is just a stub so the structure is clear.
    """
    raise NotImplementedError("Connect this to your LLM backend.")


def merge_state(current_state, proposed_update, agent_name):
    """
    Apply an agent's proposed updates into the negotiation_state.

    You don't need to change this unless you want to add more fields.
    """
    state = json.loads(current_state)
    agent_state = state["agents"][agent_name]

    # Allow agents to update their own flags
    for key in ["plan_submitted", "final_position"]:
        if key in proposed_update:
            agent_state[key] = proposed_update[key]

    # Add reviewed plans
    if "plans_reviewed_add" in proposed_update:
        for other in proposed_update["plans_reviewed_add"]:
            if other not in agent_state["plans_reviewed"]:
                agent_state["plans_reviewed"].append(other)

    # Increment disagreements
    if "disagreements_increment" in proposed_update:
        agent_state["disagreements"] += proposed_update["disagreements_increment"]

    # Allow some global updates
    for key in ["phase", "final_plan", "status"]:
        if key in proposed_update:
            state[key] = proposed_update[key]

    state["agents"][agent_name] = agent_state
    return json.dumps(state, indent=2)


def generate_round_summary(round_number, team_chat, negotiation_state_text):
    """
    Optional helper: create a short status summary for humans.

    You can keep this simple: just tag the current round and maybe
    dump the phase. For a real system, you'd ask an LLM to summarize.
    """
    state = json.loads(negotiation_state_text)
    phase = state.get("phase")
    return f"--- ROUND {round_number} SUMMARY ---\nPhase: {phase}\n"


def negotiation_loop():
    """
    Main negotiation loop.

    It will:
    - run up to MAX_ROUNDS
    - call each agent in AGENTS each round
    - respect 'status' and 'LoopStatus' signals
    - optionally report each round and/or at the end
    """

    # Start with empty chat and baseline state
    team_chat = ""
    negotiation_state = json.dumps({
        "phase": "COLLECT_PLANS",   # starting phase
        "round": 0,                 # we'll increment this as we go
        "agents": {
            agent_name: {
                "plan_submitted": False,
                "plans_reviewed": [],
                "final_position": None,
                "disagreements": 0
            }
            for agent_name in AGENTS
        },
        "final_plan": None,
        "status": "IN_PROGRESS",
        "metrics": {
            "max_rounds_allowed": MAX_ROUNDS,
            "rounds_completed": 0,
            "reached_agreement": False,
            "reason_for_stop": None
        }
    }, indent=2)

    loop_done = False
    current_round = 0

    # Run up to MAX_ROUNDS
    while not loop_done and current_round < MAX_ROUNDS:
        current_round += 1
        state_obj = json.loads(negotiation_state)
        state_obj["round"] = current_round
        negotiation_state = json.dumps(state_obj, indent=2)

        # One "round" = each agent gets a turn once
        for agent in AGENTS:
            agent_message, proposed_update, loop_status = call_agent(
                agent_name=agent,
                team_chat=team_chat,
                negotiation_state_text=negotiation_state
            )

            team_chat += f"\n[{agent}] {agent_message}\n"

            if proposed_update:
                negotiation_state = merge_state(negotiation_state, proposed_update, agent)

            state_obj = json.loads(negotiation_state)

            # If any agent says DONE or state is DONE, stop immediately
            if state_obj.get("status") == "DONE" or loop_status == "DONE":
                loop_done = True
                break

        # Update metrics after the round
        state_obj = json.loads(negotiation_state)
        state_obj["metrics"]["rounds_completed"] = current_round

        # Simple "agreement" check:
        positions = [a["final_position"] for a in state_obj["agents"].values()]
        all_agree = positions and all(p == "agree" for p in positions if p is not None)
        state_obj["metrics"]["reached_agreement"] = bool(all_agree)

        # Reason for stop (will be final if we end now)
        if loop_done:
            state_obj["metrics"]["reason_for_stop"] = "agent_marked_done"
        elif current_round >= MAX_ROUNDS:
            state_obj["metrics"]["reason_for_stop"] = "max_rounds_reached"

        negotiation_state = json.dumps(state_obj, indent=2)

        # Optional per-round report
        if REPORT_EACH_ROUND:
            round_summary = generate_round_summary(current_round, team_chat, negotiation_state)
            print(round_summary)

        # If we hit MAX_ROUNDS, end even if agents didn't say DONE
        if current_round >= MAX_ROUNDS:
            loop_done = True

    # Final metrics adjustment if needed
    state_obj = json.loads(negotiation_state)
    if state_obj["metrics"]["reason_for_stop"] is None:
        # If we ended without a clear reason (unlikely), set default
        state_obj["metrics"]["reason_for_stop"] = "loop_ended"

    negotiation_state = json.dumps(state_obj, indent=2)

    # Optional final report
    if REPORT_AT_END:
        print("\n=== FINAL NEGOTIATION SUMMARY ===")
        print(f"Rounds allowed: {MAX_ROUNDS}")
        print(f"Rounds completed: {state_obj['metrics']['rounds_completed']}")
        print(f"Reached agreement?: {state_obj['metrics']['reached_agreement']}")
        print(f"Reason for stop: {state_obj['metrics']['reason_for_stop']}")
        # You could also print or summarize final_plan here.

    return team_chat, negotiation_state


if __name__ == "__main__":
    # Example invocation
    # In practice, you'd call negotiation_loop() from your controller,
    # but this shows how it can be run.
    team_chat_log, final_state = negotiation_loop()
