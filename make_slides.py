from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER

W, H = A4
doc = SimpleDocTemplate(
    'voice_driven_swarm_slides.pdf',
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

ACCENT = colors.HexColor('#3b82f6')
WHITE  = colors.HexColor('#f8fafc')
MUTED  = colors.HexColor('#94a3b8')
GREEN  = colors.HexColor('#22c55e')
RED    = colors.HexColor('#ef4444')
DARK   = colors.HexColor('#0f172a')
DARK2  = colors.HexColor('#1e293b')
DARK3  = colors.HexColor('#334155')

def H1(txt):
    return Paragraph(txt, ParagraphStyle('h1', fontSize=22, textColor=ACCENT,
        fontName='Helvetica-Bold', spaceAfter=6, alignment=TA_CENTER))

def H2(txt):
    return Paragraph(txt, ParagraphStyle('h2', fontSize=14, textColor=ACCENT,
        fontName='Helvetica-Bold', spaceAfter=6))

def Body(txt):
    return Paragraph(txt, ParagraphStyle('body', fontSize=10, textColor=WHITE,
        fontName='Helvetica', spaceAfter=4, leading=14))

def Sub(txt):
    return Paragraph(txt, ParagraphStyle('sub', fontSize=9, textColor=MUTED,
        fontName='Helvetica', spaceAfter=3, leading=12, alignment=TA_CENTER))

def Code(txt, color=WHITE):
    return Paragraph(txt, ParagraphStyle('code', fontSize=9, textColor=color,
        fontName='Courier', spaceAfter=3, leading=12, backColor=DARK2))

def HR():
    return HRFlowable(width='100%', thickness=1, color=ACCENT, spaceAfter=10, spaceBefore=6)

def SP(h=0.3):
    return Spacer(1, h*cm)

story = []

# SLIDE 1: TITLE
story += [
    SP(1.2),
    H1('Voice-Driven Multi-Agent'),
    H1('Test & Debugging Swarm'),
    SP(0.5),
    Sub('IBM Bob 2.0 Hackathon  |  September 2026'),
    SP(0.2),
    Sub('HridaySharma2002  |  github.com/HridaySharma2002/voice-driven-test-swarm'),
    SP(0.8),
    HR(),
]

# SLIDE 2: THE PROBLEM
story += [
    H2('The Problem: Context-Switching Tax'),
    Body('When a CI/CD build fails, developers must manually:'),
    Body('  1.  Parse RestAssured / Selenium execution logs'),
    Body('  2.  Trace the failure back through Spring Boot logic'),
    Body('  3.  Cross-reference schemas, configs, and test reports'),
    Body('  4.  Write and apply a fix, then re-run tests'),
    SP(0.2),
    Body('This multi-step debugging loop inflates <b>Mean Time to Resolution (MTTR)</b> and drains developer focus from building features.'),
    SP(0.2), HR(),
]

# SLIDE 3: THE SOLUTION
story += [
    H2('The Solution: One Voice Command, Full Resolution'),
    Body('The Voice-Driven Swarm collapses the entire debugging loop into a single spoken trigger:'),
    SP(0.2),
    Code('"Run API regression tests."', GREEN),
    SP(0.2),
    Body('The system then autonomously:'),
    Body('  - Executes the hybrid Java test suite (RestAssured + Selenium)'),
    Body('  - Parses Maven Surefire XML failure reports'),
    Body('  - Hands the stack trace to IBM Bob 2.0 for root-cause analysis'),
    Body('  - Plays the fix summary out loud via ElevenLabs TTS'),
    Body('Result: a multi-hour debugging cycle reduced to under 60 seconds.'),
    SP(0.2), HR(),
]

# SLIDE 4: ARCHITECTURE TABLE
story += [H2('Architecture — 4 Phases')]
phases = [
    ['Phase', 'Component', 'Technology', 'Role'],
    ['1', 'Target App', 'Java 21, Spring Boot 3.2, Maven', 'Buggy REST API + disabled UI button causes intentional failures + Surefire XML'],
    ['2', 'Voice Orchestrator', 'Python', 'Recognises spoken command, triggers pipeline (mic simulated on Python 3.14)'],
    ['3', 'Connector', 'Python + xml.etree', 'Runs mvn clean test, parses failure elements from surefire XML reports'],
    ['4', 'Bob Handoff + TTS', 'IBM Bob 2.0 + ElevenLabs v2', 'Bob analyses repo, explains root cause; Sarah voice plays summary aloud'],
]
t = Table(phases, colWidths=[1.2*cm, 3*cm, 4.5*cm, 7.8*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0),  ACCENT),
    ('TEXTCOLOR',    (0,0), (-1,0),  WHITE),
    ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 8),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [DARK2, DARK]),
    ('TEXTCOLOR',    (0,1), (-1,-1), WHITE),
    ('GRID',         (0,0), (-1,-1), 0.4, DARK3),
    ('VALIGN',       (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING',   (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0), (-1,-1), 5),
]))
story += [t, SP(0.3), HR()]

# SLIDE 5: THE BUG
story += [
    H2('The Deliberate Bug — CheckoutController.java'),
    Body('The controller uses <b>flat subtraction</b> instead of percentage-based discount math:'),
    SP(0.2),
    Code('// DELIBERATE BUG', RED),
    Code('double finalPrice = order.getPrice() - order.getDiscount();', RED),
    Code('if (finalPrice != 90.0) return ResponseEntity.badRequest();', RED),
    SP(0.2),
    Body('Test sends price=200, discount=10:'),
    Body('  BUG:  200 - 10 = 190  which is not 90.0  so returns HTTP 400  Test FAILS'),
    Body('  FIX:  200 x (1 - 10/100) = 180  returns HTTP 200  Test PASSES'),
    SP(0.2), HR(),
]

# SLIDE 6: IBM BOB USAGE
story += [
    H2('IBM Bob 2.0 Usage — Evaluator + Optimizer Pattern'),
    Body('<b>In Bob IDE (23.93 Bobcoins, 12 tasks completed):</b>'),
    Body('  - Fixed ElevenLabs v1 to v2 SDK migration'),
    Body('  - Resolved pyaudio build failure on Python 3.14 (no MSVC wheel available)'),
    Body('  - Fixed relative cwd path errors using os.path.abspath(__file__)'),
    Body('  - Renamed CheckoutAPiTest.java to CheckoutApiTest.java (Java filename rule)'),
    Body('  - Fixed pom.xml missing spring-boot-starter-test dependency'),
    Body('  - Hardcoded Maven absolute path (not on system PATH)'),
    SP(0.2),
    Body('<b>In the pipeline (bob_handoff.py):</b>'),
    Body('  - bob run called with the full Surefire XML failure trace as a natural language prompt'),
    Body('  - Bob reasons over the Spring Boot repository and returns a 2-sentence fix summary'),
    Body('  - Fallback feeds directly into ElevenLabs TTS when CLI path is restricted'),
    SP(0.2), HR(),
]

# SLIDE 7: LIVE OUTPUT
story += [
    H2('Live Terminal Output'),
    Code('[MIC BYPASSED] Simulating voice command capture...',          WHITE),
    Code("Recognized: 'run api regression tests'",                     GREEN),
    Code('Intent recognized: Triggering CI/CD Pipeline...',            WHITE),
    Code('Executing Java hybrid test suite...',                        WHITE),
    Code('Detected 2 test failures. Handing off to IBM Bob 2.0...',   RED),
    Code('[IBM Bob 2.0 Summary]: The test failed because',             ACCENT),
    Code('CheckoutController uses flat subtraction instead of',        ACCENT),
    Code('percentage-based discount math. Fix: price*(1-discount/100)',ACCENT),
    Code('Playing audio summary...',                                   GREEN),
    SP(0.3), HR(),
]

# SLIDE 8: IMPACT
story += [
    H2('Impact & Submission Details'),
    Body('<b>Before:</b>  30-60 min manual debug cycle'),
    Body('<b>After:</b>   Under 60 seconds, fully autonomous, voice-activated'),
    SP(0.3),
    Body('<b>GitHub:</b>  github.com/HridaySharma2002/voice-driven-test-swarm'),
    Body('<b>Bob Evidence:</b>  bob_sessions/ — 2 task screenshots, 23.93 Bobcoins total'),
    SP(0.3),
    Body('<b>Stack:</b>  Java 21 | Spring Boot 3.2 | Maven | RestAssured | Selenium 4'),
    Body('         Python 3.14 | IBM Bob 2.0 | ElevenLabs v2 SDK (Sarah voice)'),
    SP(0.5),
    Sub('Built with IBM Bob 2.0  |  IBM Bob 2.0 Hackathon  |  September 2026'),
]

doc.build(story)
print('PDF created successfully: voice_driven_swarm_slides.pdf')
