"""Generate one UML sequence diagram per business flow (draw.io, one page per flow).

Run:  python3 docs/architecture/gen_business_flows.py
Out:  docs/architecture/business_flows.drawio   (pages B1–B6; export PNGs: see plan.md §7A)

Same style as the thesis sequences S1–S7 (docs/diagrams/gen_drawio.py, sequence()):
- one lifeline per participant (user, Nuxt, FastAPI, Redis, MySQL …), left → right in call order;
- steps numbered 1 → n top to bottom; solid arrow = call, dashed open arrow = reply, loop = internal step;
- `opt [condition]` frames mark the branch that only happens under that condition (errors, cache miss …).
Each page names the FR/NFR it implements (plan.md §2A). Edit the FLOWS data and rerun.
"""
from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_aws_diagram import FONT, TEXT, Diagram, mxfile  # noqa: E402

OUT_FILE = Path(__file__).resolve().parent / "business_flows.drawio"

PX = 23          # message text, participant title, frame label (same as thesis S1–S7)
TECH_PX = 20     # technical name under the participant title
COL = 200        # distance between two lifelines
BOX = 180        # participant box width
HEAD = 110       # participant box height
GAP = 72         # vertical distance between two steps
FRAME_PAD = 30   # extra space around an opt frame

LIFELINE = (
    "shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;dropTarget=0;"
    f"collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;size={HEAD};"
    f"fillColor=#FFFFFF;strokeColor=#545B64;fontColor={TEXT};fontSize={PX};spacing=4;" + FONT
)
CALL = (f"html=1;verticalAlign=bottom;endArrow=block;endFill=1;strokeColor=#232F3E;strokeWidth=1.5;"
        f"fontSize={PX};fontColor={TEXT};labelBackgroundColor=#FFFFFF;" + FONT)
REPLY = CALL.replace("endArrow=block;endFill=1;", "endArrow=open;endFill=0;") + "dashed=1;"
SELF = CALL + "edgeStyle=orthogonalEdgeStyle;align=left;labelPosition=right;spacingLeft=48;entryX=0;"
FRAME = (f"shape=umlFrame;whiteSpace=wrap;html=1;width={{w}};height=32;fontSize={PX - 2};fontStyle=1;"
         f"strokeColor=#879196;fontColor={TEXT};" + FONT)


def title(name: str, tech: str) -> str:
    return f'<b>{escape(name)}</b><br><font style="font-size:{TECH_PX}px;color:#545B64">{escape(tech)}</font>'


class Sequence(Diagram):
    def message(self, cid: str, x1: float, x2: float, y: float, text: str, style: str,
                loop: bool = False) -> None:
        target_y = y + 18 if loop else y
        points = (f'<Array as="points"><mxPoint x="{x1 + 40}" y="{y}"/><mxPoint x="{x1 + 40}" y="{target_y}"/></Array>'
                  if loop else "")
        geo = ('<mxGeometry relative="1" as="geometry">'
               f'<mxPoint x="{x1}" y="{y}" as="sourcePoint"/><mxPoint x="{x2}" y="{target_y}" as="targetPoint"/>'
               f"{points}</mxGeometry>")
        cell = f'<mxCell style={quoteattr(style)} edge="1" parent="1">{geo}</mxCell>'
        self.cells.append(f'<object id="{cid}" label={quoteattr(text)}>{cell}</object>')


def sequence(page: str, participants: list[tuple[str, str, str]], steps: list[tuple[str, str, str, str]],
             frames: tuple[tuple[str, int, int, str, str], ...] = ()) -> Sequence:
    """participants: (id, title, tech). steps: (kind, from, to, text), kind = call | reply | self.
    frames: (label, first step, last step, leftmost participant, rightmost participant)."""
    left, top = 20, 20
    starts = {f[1] for f in frames}
    after = {f[2] + 1 for f in frames}
    ys, y = [], top + HEAD + 58
    for n in range(1, len(steps) + 1):
        if n > 1:
            y += GAP + (FRAME_PAD if n in starts or n in after else 0)
        ys.append(y)
    height = ys[-1] + 40
    width = left * 2 + COL * (len(participants) - 1) + BOX + 120   # room for the last loop label
    d = Sequence(page, width, height + 20)

    xs: dict[str, float] = {}
    for i, (pid, name, tech) in enumerate(participants):
        x = left + i * COL
        xs[pid] = x + BOX / 2
        d.vertex(f"ll-{pid}", title(name, tech), LIFELINE, x, top, BOX, height - top)

    for n, (kind, src, dst, text) in enumerate(steps, 1):
        label = f"{n}. {escape(text)}"
        if kind == "self":
            d.message(f"m{n}", xs[src], xs[src] + 1, ys[n - 1], label, SELF, loop=True)
        else:
            d.message(f"m{n}", xs[src], xs[dst], ys[n - 1], label, REPLY if kind == "reply" else CALL)

    for i, (name, first, last, lp, rp) in enumerate(frames):
        fy = ys[first - 1] - 70
        fh = ys[last - 1] - ys[first - 1] + 90
        fx = max(4, min(xs[lp], xs[rp]) - BOX / 2 - 6)
        fr = min(width - 4, max(xs[lp], xs[rp]) + BOX / 2 + 6)
        d.vertex(f"frame{i}", escape(name), FRAME.format(w=min(int(fr - fx) - 20, 13 * len(name) + 36)),
                 fx, fy, fr - fx, fh)
    return d


# -- Participants --
CLINICIAN = ("user", "Clinician", "browser")
COORDINATOR = ("user", "Care Coordinator", "browser")
COMPLIANCE = ("user", "Compliance Officer", "browser")
WEB = ("web", "Web frontend", "Vue 3 SPA")
API = ("api", "REST API", "Django + DRF")
WORKER = ("worker", "Celery worker", "background task")
CLAUDE = ("claude", "Claude API", "tool-calling")
DB = ("db", "Database", "PostgreSQL")
S3 = ("s3", "Object storage", "Amazon S3")


def flows() -> list[Sequence]:
    b1 = sequence(
        "B1 Patient search (FR-02, NFR-02, NFR-05)",
        [CLINICIAN, WEB, API, ("redis", "Cache", "Redis"), DB],
        [
            ("call", "user", "web", "search patients"),
            ("call", "web", "api", "GET /patients?q=..."),
            ("self", "api", "api", "for_user(): scope to care team"),
            ("call", "api", "redis", "GET cache key"),
            ("reply", "redis", "api", "page | nil"),
            ("call", "api", "db", "SELECT ... keyset paginated"),
            ("reply", "db", "api", "rows"),
            ("call", "api", "redis", "SET key, 30 s"),
            ("call", "api", "db", "INSERT AuditEvent(READ)"),
            ("reply", "api", "web", "200 Page[Patient]"),
            ("reply", "web", "user", "roster shown"),
        ],
        frames=(("opt [cache miss]", 6, 8, "api", "db"),),
    )
    b2 = sequence(
        "B2 Encounter + AI draft + sign (FR-04, FR-05, NFR-04)",
        [CLINICIAN, WEB, API, WORKER, CLAUDE, DB],
        [
            ("call", "user", "web", "click Draft with AI"),
            ("call", "web", "api", "POST /encounters/{id}/ai-draft"),
            ("call", "api", "worker", "enqueue (Redis broker)"),
            ("reply", "api", "web", "202 {job_id}"),
            ("call", "worker", "claude", "draft SOAP note (tools: history, meds, allergies)"),
            ("reply", "claude", "worker", "tool call get_medications"),
            ("call", "worker", "db", "SELECT medications (read-only)"),
            ("call", "worker", "claude", "tool result"),
            ("reply", "claude", "worker", "draft text + ICD-10 codes"),
            ("call", "worker", "db", "INSERT AIDraft(PENDING_REVIEW)"),
            ("call", "web", "api", "GET .../ai-draft/{job_id}"),
            ("reply", "api", "web", "draft text + codes"),
            ("call", "user", "web", "edit draft text"),
            ("call", "web", "api", "POST /ai-drafts/{id}/approve"),
            ("call", "api", "db", "INSERT EncounterNoteVersion + AuditEvent(CREATE)"),
            ("reply", "api", "web", "200 signed"),
        ],
        frames=(("opt [clinician edits before signing]", 13, 14, "user", "api"),),
    )
    b3 = sequence(
        "B3 Referral with consent gate (FR-07)",
        [COORDINATOR, WEB, API, DB],
        [
            ("call", "user", "web", "create referral"),
            ("call", "web", "api", "POST /referrals"),
            ("call", "api", "db", "SELECT active Consent(DATA_SHARING)"),
            ("reply", "db", "api", "none"),
            ("reply", "api", "web", "409 CONSENT_REQUIRED"),
            ("call", "api", "db", "INSERT Referral(REQUESTED) + AuditEvent"),
            ("reply", "api", "web", "201 Referral"),
            ("reply", "web", "user", "referral sent"),
        ],
        frames=(("opt [no active consent]", 4, 5, "api", "db"),),
    )
    b4 = sequence(
        "B4 Bulk lab import (FR-08, NFR-05)",
        [COORDINATOR, WEB, API, S3, WORKER, DB],
        [
            ("call", "user", "web", "upload CSV"),
            ("call", "web", "api", "POST /lab-imports (multipart)"),
            ("call", "api", "s3", "PUT object"),
            ("call", "api", "db", "INSERT LabImportJob(idempotency_key)"),
            ("reply", "api", "web", "200 existing job (no-op)"),
            ("call", "api", "worker", "enqueue process_import(job_id)"),
            ("reply", "api", "web", "202 {job_id}"),
            ("call", "worker", "s3", "stream CSV rows"),
            ("self", "worker", "worker", "validate each row"),
            ("call", "worker", "db", "bulk_create LabResult (chunks of 500)"),
            ("call", "worker", "db", "UPDATE LabImportJob(SUCCEEDED, error_report)"),
            ("call", "web", "api", "GET /lab-imports/{id}"),
            ("reply", "api", "web", "progress + error report"),
            ("reply", "web", "user", "42,318 rows imported, 12 errors"),
        ],
        frames=(("opt [same file already imported]", 4, 5, "api", "web"),),
    )
    b5 = sequence(
        "B5 Break-glass access (FR-11, NFR-02, NFR-03)",
        [CLINICIAN, WEB, API, DB],
        [
            ("call", "user", "web", "open patient outside care team"),
            ("call", "web", "api", "GET /patients/{mrn}"),
            ("call", "api", "db", "for_user() scope check"),
            ("reply", "db", "api", "not in care team"),
            ("reply", "api", "web", "404 Not Found"),
            ("reply", "web", "user", "patient not found"),
            ("call", "user", "web", "Emergency access + reason"),
            ("call", "web", "api", "POST /patients/{id}/break-glass"),
            ("call", "api", "db", "INSERT AuditEvent(BREAK_GLASS, reason_code)"),
            ("reply", "api", "web", "200 scoped token"),
            ("call", "web", "api", "GET /patients/{mrn} + scoped token"),
            ("reply", "api", "web", "200 patient chart"),
            ("reply", "web", "user", "chart shown, emergency banner"),
        ],
        frames=(("opt [no break-glass reason given]", 4, 6, "api", "web"),),
    )
    b6 = sequence(
        "B6 Compliance audit review (FR-09)",
        [COMPLIANCE, WEB, API, DB],
        [
            ("call", "user", "web", "open audit log, set filters"),
            ("call", "web", "api", "GET /audit-events?..."),
            ("self", "api", "api", "require role = COMPLIANCE_OFFICER"),
            ("reply", "api", "web", "403 Forbidden"),
            ("call", "api", "db", "SELECT AuditEvent ... keyset"),
            ("reply", "db", "api", "rows"),
            ("reply", "api", "web", "200 Page[AuditEvent]"),
            ("reply", "web", "user", "table of events"),
            ("call", "user", "web", "export CSV"),
            ("call", "web", "api", "GET /audit-events/export?..."),
            ("call", "api", "db", "SELECT (same filter, streamed)"),
            ("reply", "api", "web", "200 text/csv"),
            ("reply", "web", "user", "file downloaded"),
        ],
        frames=(("opt [not a compliance officer]", 3, 4, "api", "web"),),
    )
    return [b1, b2, b3, b4, b5, b6]


# PNG file name per page, in page order (descriptive, like aws_architecture.png).
PNG_NAMES = [
    "flow_b1_patient_search.png",
    "flow_b2_encounter_ai_draft.png",
    "flow_b3_referral_consent.png",
    "flow_b4_bulk_lab_import.png",
    "flow_b5_break_glass.png",
    "flow_b6_audit_review.png",
]


def export_png() -> None:
    """Export every page with draw.io desktop (brew install --cask drawio)."""
    import subprocess

    for index, name in enumerate(PNG_NAMES, 1):
        subprocess.run(["drawio", "--export", "--format", "png", "--scale", "2", "--border", "16",
                        "--page-index", str(index), "-o", str(OUT_FILE.parent / name), str(OUT_FILE)],
                       check=True, capture_output=True)
        print("exported", name)


if __name__ == "__main__":
    pages = flows()
    assert len(pages) == len(PNG_NAMES), "add a PNG name for every flow"
    OUT_FILE.write_text(mxfile(pages, host="gen_business_flows.py"), encoding="utf-8")
    print("wrote", OUT_FILE, f"({len(pages)} pages)")
    if "--png" in sys.argv:
        export_png()
