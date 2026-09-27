"""
main.py - Entry point for the Voice-Driven Test Swarm orchestrator.
Run this file from the orchestrator/ directory:
    python main.py
"""
import sys
import os

# Ensure agents/ is on the import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))

from voice_agent import listen_and_execute

if __name__ == "__main__":
    listen_and_execute()
