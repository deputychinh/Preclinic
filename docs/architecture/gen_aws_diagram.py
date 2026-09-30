"""Generate the AWS deployment architecture diagram (draw.io) for the real estate portal.

Run:  python3 docs/architecture/gen_aws_diagram.py
Out:  docs/architecture/aws_architecture.drawio  (export PNG: see plan.md §15.2)

Same conventions as the thesis figure H4.1 (docs/diagrams/gen_drawio.py):
- layers are columns, left → right: Client · Edge & Security · Load Balancing · Application · Data;
- official AWS icons (draw.io `mxgraph.aws4.*`), coloured per AWS service category;
- AWS groups nested AWS Cloud → Region → VPC → subnets; global services sit in AWS Cloud, outside the Region;
- circled numbers on arrows = flow table in plan.md §15.3; dashed arrows = supporting flows;
- every shape carries `layer` and `aws_resource` data (Edit Data in draw.io) to trace it to infra/terraform.
Edit this script and rerun; do not hand-edit the generated file.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

OUT_FILE = Path(__file__).resolve().parent / "aws_architecture.drawio"

FONT = "fontFamily=Helvetica;"
TEXT = "#232F3E"
F = 28        # main label and arrow numbers
T = 23        # technical name under the main label
TITLE = 30    # layer (column) title

AWS_COLOURS = {
    "compute": "#ED7100",
    "containers": "#ED7100",
    "database": "#C925D1",
    "networking": "#8C4FFF",
    "storage": "#7AA116",
    "management": "#E7157B",
    "security": "#DD344C",
}

LABEL_RIGHT = "labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=middle;spacingLeft=6;"
LABEL_LEFT = "labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;spacingRight=6;"

EDGE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
    "endArrow=block;endFill=1;strokeColor=#545B64;strokeWidth=1.5;"
    f"fontSize={F};fontColor={TEXT};labelBackgroundColor=#FFFFFF;" + FONT
)
AUX = EDGE + "dashed=1;"

COLUMN = (
    "swimlane;horizontal=1;startSize=96;html=1;whiteSpace=wrap;collapsible=0;"
    "fillColor={fill};swimlaneFillColor={fill};strokeColor=#D5D8DC;"
    f"fontSize={TITLE};fontStyle=1;fontColor={TEXT};" + FONT
)
DASHED_BOX = (
    "rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#879196;dashed=1;"
    f"verticalAlign=top;align=left;spacingLeft=16;spacingTop=4;fontSize={F};fontStyle=1;"
    f"fontColor={TEXT};arcSize=3;" + FONT
)
CLUSTER_BOX = DASHED_BOX.replace("align=left;spacingLeft=16;", "align=center;")
EXTERNAL_BOX = (
    "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;dashed=1;"
    f"fontColor={TEXT};fontSize={F};arcSize=8;spacing=6;" + FONT
)


def resource_icon(res: str, category: str, label_at: str = "bottom") -> str:
    style = (
        "sketch=0;outlineConnect=0;fontColor=#232F3E;"
        f"fillColor={AWS_COLOURS[category]};strokeColor=#ffffff;dashed=0;"
        f"verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize={F};"
        f"fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res};{FONT}"
    )
    return style + {"bottom": "", "left": LABEL_LEFT, "right": LABEL_RIGHT}[label_at]


def shape_icon(shape: str, fill: str = "#232F3D", label_at: str = "bottom") -> str:
    """Plain AWS shapes: users, clients, NAT / internet gateway."""
    style = (
        f"sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};"
        "strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
        f"html=1;fontSize={F};fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.{shape};" + FONT
    )
    return style + {"bottom": "", "left": LABEL_LEFT, "right": LABEL_RIGHT}[label_at]


def aws_group(gr_icon: str, stroke: str, fill: str = "none", dashed: int = 0) -> str:
    return (
        "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],"
        "[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;"
        f"whiteSpace=wrap;fontSize={F};fontStyle=1;container=1;pointerEvents=0;collapsible=0;"
        f"recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{gr_icon};"
        f"strokeColor={stroke};fillColor={fill};verticalAlign=top;align=left;spacingLeft=40;"
        f"fontColor={stroke};dashed={dashed};{FONT}"
    )


def lab(title: str, tech: str = "") -> str:
    """Function name large and bold, technical name small underneath (same rule as H4.1)."""
    head = "<br>".join(f"<b>{escape(t)}</b>" for t in title.split("\n"))
    if not tech:
        return head
    small = "<br>".join(escape(t) for t in tech.split("\n"))
    return f'{head}<br><font style="font-size:{T}px;color:#545B64">{small}</font>'


class Diagram:
    def __init__(self, name: str, width: int, height: int):
        self.name, self.width, self.height = name, width, height
        self.cells: list[str] = []

    @staticmethod
    def _data(data: dict[str, str] | None) -> str:
        return "".join(f" {k}={quoteattr(v)}" for k, v in (data or {}).items())

    def vertex(self, cid: str, value: str, style: str, x: float, y: float, w: float, h: float,
               data: dict[str, str] | None = None) -> None:
        geo = f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        cell = f'<mxCell style={quoteattr(style)} vertex="1" parent="1">{geo}</mxCell>'
        self.cells.append(f'<object id="{cid}" label={quoteattr(value)}{self._data(data)}>{cell}</object>')

    def edge(self, cid: str, source: str, target: str, value: str,
             ports: tuple[float, float, float, float], points: list[tuple[float, float]] | None = None,
             style: str = EDGE, at: float = 0.0) -> None:
        ex, ey, nx, ny = ports
        style += f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;entryX={nx};entryY={ny};entryDx=0;entryDy=0;"
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + "</Array>"
        pos = f' x="{at}"' if at else ""
        geo = f'<mxGeometry{pos} relative="1" as="geometry">{pts}</mxGeometry>'
        cell = f'<mxCell style={quoteattr(style)} edge="1" parent="1" source="{source}" target="{target}">{geo}</mxCell>'
        self.cells.append(f'<object id="{cid}" label={quoteattr(value)}>{cell}</object>')

    def page(self) -> str:
        """One draw.io page (<diagram>); several pages can share one file."""
        return (
            f'<diagram id={quoteattr(self.name)} name={quoteattr(self.name)}>'
            '<mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
            f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.width}" pageHeight="{self.height}" '
            'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + "".join(self.cells)
            + "</root></mxGraphModel></diagram>"
        )

    def xml(self) -> str:
        return mxfile([self], host="gen_aws_diagram.py")


def mxfile(pages: list[Diagram], host: str) -> str:
    return f'<mxfile host="{host}" type="device">' + "".join(p.page() for p in pages) + "</mxfile>\n"


def architecture() -> Diagram:
    """CarePath deployment: CloudFront+WAF -> S3 (SPA) / ALB -> Django API on Fargate, with
    Celery worker + Celery beat as their own Fargate services (bulk import and AI drafting must
    never block the request cycle). RDS Postgres and ElastiCache Redis are Multi-AZ-capable and
    sit behind a customer-managed KMS key (plan Sec 15.4) - unlike the sibling real-estate
    project's AWS-managed-key trade-off, PHI storage does not get that trade-off here."""
    d = Diagram("CarePath deployment architecture", 2260, 1330)

    # -- Layers (columns) --
    for cid, text, x, w, fill in [
        ("band-client", "Client Layer", 10, 280, "#F2F4F4"),
        ("band-edge", "Edge &amp; Security<br>Layer", 300, 420, "#F5F0FF"),
        ("band-lb", "Load Balancing<br>Layer", 730, 340, "#EEF7F7"),
        ("band-app", "Application Layer", 1080, 640, "#FFF4EC"),
        ("band-data", "Data Layer", 1730, 520, "#FBF0FC"),
    ]:
        d.vertex(cid, text, COLUMN.format(fill=fill), x, 10, w, 1080, data={"layer": cid.removeprefix("band-")})

    # -- AWS groups --
    d.vertex("aws-cloud", "AWS Cloud", aws_group("group_aws_cloud_alt", "#232F3E"), 310, 110, 1940, 1210)
    d.vertex("region", "Region ap-southeast-1", aws_group("group_region", "#00A4A6", dashed=1), 740, 150, 1500, 1166)
    d.vertex("vpc", "VPC 10.0.0.0/16", aws_group("group_vpc2", "#8C4FFF"), 750, 240, 1486, 700)
    d.vertex("subnet-public", "Public subnets<br>AZ a . b",
             aws_group("group_security_group", "#7AA116", fill="#F2F6E8"), 766, 320, 304, 600)
    d.vertex("subnet-app", "Private app subnets<br>AZ a . b",
             aws_group("group_security_group", "#00A4A6", fill="#E6F6F7"), 1098, 320, 620, 600)
    d.vertex("subnet-data", "Private data subnets<br>AZ a . b",
             aws_group("group_security_group", "#00A4A6", fill="#E6F6F7"), 1746, 320, 490, 600)
    d.vertex("grp-external", "External Systems", DASHED_BOX, 20, 1135, 270, 175)
    d.vertex("cross-box", "Cross-cutting Concerns", DASHED_BOX, 300, 1135, 1930, 175)

    # -- Client --
    d.vertex("users", lab("Clinicians,\ncoordinators,\ncompliance"), shape_icon("users"),
             108, 130, 64, 64, data={"layer": "client"})
    d.vertex("browser", lab("Web browser", "Vue 3 SPA"), shape_icon("client"), 110, 320, 60, 58,
             data={"layer": "client", "source": "frontend/"})
    d.vertex("github", lab("CI/CD", "GitHub Actions\nOIDC role"), EXTERNAL_BOX, 14, 820, 270, 115,
             data={"layer": "external", "source": ".github/workflows/deploy.yml"})
    d.vertex("terraform", lab("Infra as code", "Terraform\nstate in S3"), EXTERNAL_BOX, 14, 1182, 270, 115,
             data={"layer": "external", "source": "infra/terraform"})

    # -- Edge & security --
    d.vertex("route53", lab("DNS", "Amazon Route 53"), resource_icon("route_53", "networking", "left"),
             580, 220, 64, 64, data={"layer": "edge", "aws_resource": "aws_route53_record.app"})
    d.vertex("cloudfront", lab("CDN", "Amazon CloudFront"), resource_icon("cloudfront", "networking", "left"),
             580, 520, 64, 64, data={"layer": "edge", "aws_resource": "aws_cloudfront_distribution.app"})
    d.vertex("waf", lab("Web firewall", "AWS WAF"), resource_icon("waf", "security", "left"),
             580, 800, 64, 64, data={"layer": "edge", "aws_resource": "aws_wafv2_web_acl.edge"})

    # -- Load balancing (public subnets) --
    d.vertex("igw", lab("Internet gateway"), shape_icon("internet_gateway", "#8C4FFF", "right"),
             1036, 262, 48, 48, data={"layer": "network", "aws_resource": "aws_internet_gateway.main"})
    d.vertex("alb", lab("ALB", "Application LB"), resource_icon("elastic_load_balancing", "networking"),
             920, 520, 64, 64, data={"layer": "load-balancing", "aws_resource": "aws_lb.app"})
    d.vertex("nat", lab("NAT gateway"), shape_icon("nat_gateway", "#8C4FFF"),
             870, 790, 48, 48, data={"layer": "network", "aws_resource": "aws_nat_gateway.main"})

    # -- Application (private app subnets): API + Celery worker + Celery beat --
    d.vertex("grp-ecs-cluster", "ECS cluster . Fargate", CLUSTER_BOX, 1128, 380, 570, 510,
             data={"layer": "application", "aws_resource": "aws_ecs_cluster.main"})
    d.vertex("api", lab("REST API", "Django + gunicorn\n2 tasks"), resource_icon("fargate", "containers", "left"),
             1440, 500, 64, 64,
             data={"layer": "application", "aws_resource": "aws_ecs_service.api", "source": "backend/"})
    d.vertex("worker", lab("Celery worker", "bulk import,\nAI drafting"), resource_icon("fargate", "containers", "left"),
             1440, 640, 64, 64,
             data={"layer": "application", "aws_resource": "aws_ecs_service.worker", "source": "backend/apps"})
    d.vertex("beat", lab("Celery beat", "singleton,\n1 task"), resource_icon("fargate", "containers", "left"),
             1440, 780, 64, 64,
             data={"layer": "application", "aws_resource": "aws_ecs_service.beat"})
    d.vertex("ecr", lab("Image registry", "Amazon ECR"), resource_icon("ecr", "containers", "left"),
             1450, 940, 64, 64, data={"layer": "application", "aws_resource": "aws_ecr_repository.api|worker"})

    # -- Data (private data subnets + regional S3), all behind one customer-managed KMS key --
    d.vertex("kms", lab("Encryption key", "KMS CMK"), resource_icon("key_management_service", "security", "left"),
             2150, 460, 64, 64, data={"layer": "data", "aws_resource": "aws_kms_key.phi"})
    d.vertex("redis", lab("Cache / broker", "ElastiCache Redis 7"),
             resource_icon("elasticache", "database", "right"), 1790, 580, 64, 64,
             data={"layer": "data", "aws_resource": "aws_elasticache_replication_group.redis"})
    d.vertex("pg", lab("Database", "RDS PostgreSQL 16\nMulti-AZ, CMK"), resource_icon("rds", "database", "right"),
             1790, 800, 64, 64, data={"layer": "data", "aws_resource": "aws_db_instance.postgres"})
    d.vertex("s3-spa", lab("SPA assets", "Amazon S3"), resource_icon("s3", "storage", "right"),
             1790, 1000, 64, 64, data={"layer": "data", "aws_resource": "aws_s3_bucket.spa"})

    d.vertex("claude", lab("Claude API", "tool-calling,\nread-only"), EXTERNAL_BOX, 14, 970, 260, 115,
             data={"layer": "external", "external": "true", "source": "backend/apps/ai_assistant"})

    # -- Cross-cutting --
    for cid, title, tech, res, cat, cx in [
        ("acm", "TLS certificates", "AWS Certificate Manager", "certificate_manager_3", "security", 540),
        ("iam", "Access control", "IAM . GitHub OIDC", "identity_and_access_management", "security", 900),
        ("secrets", "Secrets", "Secrets Manager", "secrets_manager", "security", 1250),
        ("cloudwatch", "Logs & alarms", "CloudWatch, CMK", "cloudwatch_2", "management", 1650),
        ("ssm", "Deploy config", "SSM Parameter Store", "systems_manager", "management", 2020),
    ]:
        d.vertex(cid, lab(title, tech), resource_icon(res, cat),
                 cx - 28, 1182, 56, 56, data={"layer": "cross-cutting", "aws_resource": tech})

    # -- Numbered flows (plan.md Sec 15.2) --
    e = d.edge
    e("f1", "browser", "route53", "1", (1, .38, .3, 1), [(599.2, 342)], at=-0.3)
    e("f2", "browser", "cloudfront", "2", (1, .88, .5, 0), [(612, 371)], at=-0.3)
    e("f3", "cloudfront", "s3-spa", "3 static", (1, .2, .5, 1), [(700, 532.8), (700, 1090), (1822, 1090)], at=0.1)
    e("f4", "cloudfront", "alb", "4 /api/*", (1, .4, 0, .4))
    e("f5", "alb", "api", "5", (1, .3, .0175, 0), [(984, 564.8), (984, 532), (1436, 532)], at=-0.35)
    e("f6", "api", "pg", "6", (1, .3, 0, .35), [(1740, 532), (1740, 828)], at=-0.35)
    e("f7", "api", "redis", "7 enqueue", (1, .5, 0, .5))
    e("f8", "redis", "worker", "7", (1, .7, 0, .5), [(1700, 624.8), (1700, 672)], style=AUX, at=0.2)
    e("f9", "worker", "claude", "9", (1, .15, 1, .5), [(1600, 649.6), (1600, 1128), (274, 1128)], at=-0.4)
    e("f10", "worker", "s3-spa", "8", (1, .8, 0, .85), [(1780, 785), (1780, 1053)], at=0.15)
    e("f11", "grp-ecs-cluster", "cloudwatch", "10", (.9298, 1, .5, 0), style=AUX, at=0.3)
    e("f12", "github", "ecr", "11", (.4, 1, .5, 1), [(122, 942), (295, 942), (295, 1118), (1482, 1118)], at=0.1)
    e("f13", "github", "grp-ecs-cluster", "12", (.7, 1, .0526, 1), [(203, 962), (305, 962), (305, 1100), (1158, 1100)], at=0.35)

    # -- Supporting flows (unnumbered, dashed) --
    e("s-waf", "waf", "cloudfront", "", (.5, 0, .5, 1), style=AUX)
    e("s-ecr", "ecr", "grp-ecs-cluster", "", (.5, 0, .6842, 1), style=AUX)
    e("s-nat", "grp-ecs-cluster", "nat", "", (0, .8235, 1, .5), style=AUX)
    e("s-kms-rds", "kms", "pg", "", (.5, 1, 1, .2), [(2182, 812.8)], style=AUX)
    e("s-kms-s3", "kms", "s3-spa", "", (.5, 1, 1, .5), [(2200, 1032)], style=AUX)
    e("s-beat", "beat", "worker", "", (0, .5, 0, .3), [(1420, 812), (1420, 660)], style=AUX)
    return d


if __name__ == "__main__":
    import sys
    import subprocess

    OUT_FILE.write_text(architecture().xml(), encoding="utf-8")
    print("wrote", OUT_FILE)
    if "--png" in sys.argv:   # needs draw.io desktop (brew install --cask drawio)
        png = OUT_FILE.with_suffix(".png")
        subprocess.run(["drawio", "--export", "--format", "png", "--scale", "2", "--border", "16",
                        "-o", str(png), str(OUT_FILE)], check=True, capture_output=True)
        print("exported", png.name)
