#!/usr/bin/env python3
"""
Agent Beta Startup Script
Autonomous student platform developer
"""

import sys
sys.path.insert(0, '.')

from shared.agent_utils import startup_protocol

# Execute startup protocol
context = startup_protocol('beta')

print("\n" + "="*60)
print("AGENT BETA - STARTUP COMPLETE")
print("="*60)
print(f"\nSession ID: {context['session_id']}")
print(f"Capability Level: {context['capability_level']}")
print(f"Supervision Level: {context['supervision_level']}")
print(f"Messages for me: {len(context['my_messages'])}")
print(f"My pending tasks: {len(context['my_tasks'])}")
print(f"Help requests: {len(context['help_requests'])}")
print(f"Active claims by others: {len(context['active_claims'])}")

if context['my_tasks']:
    print("\n📋 NEXT TASK:")
    print(f"   {context['my_tasks'][0]}")

if context['help_requests']:
    print("\n⚠️ HELP REQUESTS:")
    for req in context['help_requests']:
        print(f"   - {req['message']}")

print("\n✅ Ready to begin work!")
