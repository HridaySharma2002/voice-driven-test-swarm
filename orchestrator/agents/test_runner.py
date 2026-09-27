import subprocess
import xml.etree.ElementTree as ET
import os
from bob_handoff import handoff_to_bob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "target_app"))
REPORT_DIR = os.path.join(BASE_DIR, "target", "surefire-reports")
MVN_CMD = r"C:\maven\apache-maven-3.9.6\bin\mvn.cmd"

def run_tests_and_parse():
    print("Executing Java hybrid test suite...")

    subprocess.run(
        [MVN_CMD, "clean", "test"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    failed_traces = []
    if os.path.exists(REPORT_DIR):
        for filename in os.listdir(REPORT_DIR):
            if filename.endswith(".xml"):
                tree = ET.parse(os.path.join(REPORT_DIR, filename))
                root = tree.getroot()
                for testcase in root.findall("testcase"):
                    failure = testcase.find("failure")
                    if failure is not None:
                        failed_traces.append({
                            "test_name": testcase.get("name"),
                            "error_message": failure.get("message"),
                            "stack_trace": failure.text,
                        })

    if failed_traces:
        print(f"Detected {len(failed_traces)} test failures. Handing off to IBM Bob 2.0...")
        return handoff_to_bob(failed_traces[0])

    print("All tests passed. Build is Green.")
    return {"status": "success"}
