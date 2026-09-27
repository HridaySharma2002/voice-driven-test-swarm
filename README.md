# Voice-Driven Multi-Agent Test & Debugging Swarm 🎙️🤖

An autonomous QA swarm that executes hybrid test suites and uses IBM Bob 2.0 to locate and audibly explain code regressions, eliminating context-switching for developers.

## 🏗️ Architecture & Phases

**Phase 1: Target App (Java 21 / Spring Boot / Maven)**
* Contains a vulnerable REST API (`CheckoutController.java`) with a deliberate logic bug (flat subtraction instead of percentage-based math).
* Contains a vulnerable UI (`index.html`) with a disabled submit button.
* `CheckoutApiTest.java` and `CheckoutUITest.java` are configured to fail intentionally and generate Surefire XML logs.

**Phase 2: Voice Orchestrator (Python)**
* Bypasses `pyaudio` and `whisper` (due to local Python 3.14 MSVC constraints).
* Hardcodes the recognized command (`"run api regression tests"`) to programmatically trigger the CI/CD pipeline.

**Phase 3: The Connector (Execution & Parsing)**
* Executes `mvn clean test` using absolute paths.
* Parses `target/surefire-reports/*.xml` to extract the `<failure>` elements, stack traces, and expected vs. actual results.

**Phase 4: IBM Bob Handoff & Audio (ElevenLabs v2)**
* Passes the failure trace to the IBM Bob CLI (`bob run`).
* Incorporates a robust fallback diagnostic summary if the local Bob CLI path is obstructed.
* Uses the ElevenLabs v2 SDK (Sarah voice) to generate `bob_summary.mp3` and automatically plays the root-cause analysis out loud to the developer.

## 🚀 How to Run

1. Navigate to the orchestrator directory:
   ```bash
   cd orchestrator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your ElevenLabs API Key:
   ```powershell
   $env:ELEVEN_API_KEY = "your_key_here"
   ```

4. Run the pipeline:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
voice-driven-test-swarm/
├── target_app/                        # Java Spring Boot app + tests
│   ├── pom.xml
│   └── src/
│       ├── main/java/.../controller/CheckoutController.java   # Deliberate bug
│       ├── main/resources/static/index.html                   # Disabled button bug
│       └── test/java/.../tests/
│           ├── CheckoutApiTest.java   # API regression test (fails intentionally)
│           └── CheckoutUITest.java    # UI Selenium test (fails intentionally)
├── orchestrator/
│   ├── main.py                        # Entry point
│   ├── requirements.txt
│   └── agents/
│       ├── voice_agent.py             # Phase 2: Simulated voice trigger
│       ├── test_runner.py             # Phase 3: Maven executor + XML parser
│       └── bob_handoff.py            # Phase 4: Bob CLI + ElevenLabs TTS
├── .bobignore
└── README.md
```

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `ELEVEN_API_KEY` | Your ElevenLabs API key for TTS audio generation |

## ⚠️ Known Constraints

- `pyaudio` has no pre-built wheel for Python 3.14 — mic input is simulated.
- `bob run` CLI requires IBM Bob to be on the system PATH — a fallback summary is used when unavailable.
- Rachel voice requires a paid ElevenLabs plan — Sarah (free-tier) is used instead.
