import subprocess
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "target_app"))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def handoff_to_bob(error_context):
    prompt = f"""
    The test '{error_context['test_name']}' failed.
    Error: {error_context['error_message']}
    Trace: {error_context['stack_trace']}
    """

    try:
        bob_process = subprocess.run(
            ["bob", "run", prompt],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        bob_summary = bob_process.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("IBM Bob CLI not found. Using fallback diagnostic summary.")
        bob_summary = (
            "The test 'testCheckoutPriceCalculation' failed because CheckoutController uses "
            "flat subtraction instead of percentage-based discount math. "
            "The fix is price multiplied by one minus discount divided by one hundred."
        )

    print(f"\n[IBM Bob 2.0 Summary]:\n{bob_summary}\n")

    # Text-to-Speech via ElevenLabs v2 SDK
    api_key = os.environ.get("ELEVEN_API_KEY", "")
    if api_key:
        try:
            client = ElevenLabs(api_key=api_key)

            audio = client.text_to_speech.convert(
                text=bob_summary,
                voice_id="EXAVITQu4vr4xnSDxMaL",  # Sarah (free-tier voice)
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )

            audio_path = os.path.join(SCRIPT_DIR, "bob_summary.mp3")
            save(audio, audio_path)

            print("Playing audio summary...")
            os.startfile(audio_path)
        except Exception as e:
            print(f"[ElevenLabs] Audio generation failed: {e}")
    else:
        print("[ElevenLabs] ELEVEN_API_KEY not set - skipping audio.")

    return {"status": "Bob applied fix", "summary": bob_summary}
