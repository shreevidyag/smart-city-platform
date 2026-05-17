"""
Smart City Platform — Business Case PDF Generator
Generates a professional 5-page PDF business case document.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# ─── Color palette ────────────────────────────────────────────────────────────
TEAL   = colors.HexColor("#0F6E56")
TEAL_L = colors.HexColor("#E1F5EE")
PURPLE = colors.HexColor("#534AB7")
AMBER  = colors.HexColor("#BA7517")
GRAY   = colors.HexColor("#5F5E5A")
LGRAY  = colors.HexColor("#F1EFE8")
WHITE  = colors.white
BLACK  = colors.HexColor("#1a1a1a")


def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title", fontSize=28, fontName="Helvetica-Bold",
        textColor=WHITE, leading=34, spaceAfter=8, alignment=TA_LEFT)

    styles["cover_sub"] = ParagraphStyle(
        "cover_sub", fontSize=13, fontName="Helvetica",
        textColor=colors.HexColor("#9FE1CB"), leading=18, spaceAfter=4)

    styles["cover_meta"] = ParagraphStyle(
        "cover_meta", fontSize=10, fontName="Helvetica",
        textColor=colors.HexColor("#5DCAA5"), leading=14)

    styles["h1"] = ParagraphStyle(
        "h1", fontSize=18, fontName="Helvetica-Bold",
        textColor=TEAL, spaceBefore=18, spaceAfter=6, leading=22)

    styles["h2"] = ParagraphStyle(
        "h2", fontSize=13, fontName="Helvetica-Bold",
        textColor=PURPLE, spaceBefore=12, spaceAfter=4, leading=16)

    styles["body"] = ParagraphStyle(
        "body", fontSize=10, fontName="Helvetica",
        textColor=BLACK, leading=15, spaceAfter=6, alignment=TA_JUSTIFY)

    styles["bullet"] = ParagraphStyle(
        "bullet", fontSize=10, fontName="Helvetica",
        textColor=BLACK, leading=15, spaceAfter=3,
        leftIndent=16, bulletIndent=4)

    styles["caption"] = ParagraphStyle(
        "caption", fontSize=8.5, fontName="Helvetica-Oblique",
        textColor=GRAY, leading=12, spaceAfter=4, alignment=TA_CENTER)

    styles["kpi_label"] = ParagraphStyle(
        "kpi_label", fontSize=8, fontName="Helvetica",
        textColor=GRAY, leading=10, alignment=TA_CENTER)

    styles["kpi_value"] = ParagraphStyle(
        "kpi_value", fontSize=20, fontName="Helvetica-Bold",
        textColor=TEAL, leading=24, alignment=TA_CENTER)

    styles["kpi_sub"] = ParagraphStyle(
        "kpi_sub", fontSize=8, fontName="Helvetica",
        textColor=PURPLE, leading=11, alignment=TA_CENTER)

    styles["footer"] = ParagraphStyle(
        "footer", fontSize=7.5, fontName="Helvetica",
        textColor=GRAY, leading=10, alignment=TA_CENTER)

    styles["table_header"] = ParagraphStyle(
        "table_header", fontSize=9, fontName="Helvetica-Bold",
        textColor=WHITE, leading=12, alignment=TA_CENTER)

    styles["table_cell"] = ParagraphStyle(
        "table_cell", fontSize=9, fontName="Helvetica",
        textColor=BLACK, leading=13)

    styles["quote"] = ParagraphStyle(
        "quote", fontSize=10.5, fontName="Helvetica-Oblique",
        textColor=PURPLE, leading=15, leftIndent=20, rightIndent=20,
        spaceAfter=8, spaceBefore=8)

    return styles


def cover_page(s):
    story = []
    # Dark header bar (simulated with a table)
    cover_data = [[
        Paragraph("Smart City Mini-Platform", s["cover_title"]),
    ]]
    cover_table = Table(cover_data, colWidths=[16*cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL),
        ("TOPPADDING",    (0, 0), (-1, -1), 32),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 32),
        ("LEFTPADDING",   (0, 0), (-1, -1), 24),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 24),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 0.5*cm))

    meta = [
        [Paragraph("Business Case &amp; Technical Overview", s["h2"])],
        [Paragraph("Integrating IoT Simulation, LSTM Forecasting, and Digital Strategy", s["body"])],
        [Spacer(1, 0.3*cm)],
        [HRFlowable(width="100%", thickness=1, color=TEAL_L)],
        [Spacer(1, 0.3*cm)],
        [Paragraph("<b>Author:</b> Shree Vidya Gurudath", s["body"])],
        [Paragraph("<b>Programme:</b> Master of Business Informatics — Metropolia UAS, Helsinki", s["body"])],
        [Paragraph("<b>Date:</b> May 2025", s["body"])],
        [Paragraph("<b>Stack:</b> Python · TensorFlow · MongoDB · Streamlit · Helsinki Open Data", s["body"])],
    ]
    t = Table(meta, colWidths=[16*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(t)
    story.append(Spacer(1, 1*cm))

    # KPI cards row
    kpi_data = [[
        Paragraph("RMSE", s["kpi_label"]),
        Paragraph("MAE", s["kpi_label"]),
        Paragraph("R²", s["kpi_label"]),
        Paragraph("Sensors", s["kpi_label"]),
        Paragraph("Forecast", s["kpi_label"]),
    ], [
        Paragraph("6.97", s["kpi_value"]),
        Paragraph("5.30", s["kpi_value"]),
        Paragraph("0.788", s["kpi_value"]),
        Paragraph("3", s["kpi_value"]),
        Paragraph("12h", s["kpi_value"]),
    ], [
        Paragraph("AQI units", s["kpi_sub"]),
        Paragraph("AQI units", s["kpi_sub"]),
        Paragraph("score", s["kpi_sub"]),
        Paragraph("IoT nodes", s["kpi_sub"]),
        Paragraph("LSTM horizon", s["kpi_sub"]),
    ]]
    kpi_t = Table(kpi_data, colWidths=[3.2*cm]*5)
    kpi_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.5, TEAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(kpi_t)
    story.append(Spacer(1, 0.8*cm))

    story.append(Paragraph(
        "Executive Summary",
        s["h1"]
    ))
    story.append(Paragraph(
        "Urban air quality monitoring is a persistent challenge for Nordic cities. Helsinki's "
        "existing manual station network (9 fixed HSY stations) covers less than 15% of the "
        "metropolitan area, leaving high-density residential and commercial zones unmonitored "
        "between measurement points. This project proposes and demonstrates a low-cost, "
        "cloud-native Smart City monitoring platform that combines IoT sensor simulation, "
        "real-time data ingestion into MongoDB, and a 2-layer LSTM neural network for "
        "12-hour ahead AQI forecasting — all exposed through a live Streamlit dashboard.",
        s["body"]
    ))
    story.append(Paragraph(
        "The platform is designed for rapid deployment at less than 10% of the cost of "
        "traditional sensor infrastructure, enabling data-driven urban planning decisions, "
        "proactive public health alerts, and compliance reporting aligned with the EU "
        "Ambient Air Quality Directive (2008/50/EC). The business case targets Helsinki City "
        "Environment Services (HSY) and Nordic smart city SaaS providers as primary customers.",
        s["body"]
    ))
    return story


def problem_page(s):
    story = [PageBreak()]
    story.append(Paragraph("1. Problem Statement", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL_L))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("1.1 The Helsinki Air Quality Gap", s["h2"]))
    story.append(Paragraph(
        "Helsinki ranks among Europe's cleanest cities, yet localised pollution events — "
        "vehicle exhaust during peak hours, industrial activity in Pasila, wood-burning "
        "in Kallio residential areas — go unmeasured between HSY's 9 fixed monitoring "
        "stations. The nearest station to a given street corner may be 3–8 km away, "
        "making its reading statistically unreliable for hyper-local decisions.",
        s["body"]
    ))

    problem_rows = [
        [Paragraph("Issue", s["table_header"]),
         Paragraph("Current state", s["table_header"]),
         Paragraph("Impact", s["table_header"])],
        [Paragraph("Spatial coverage", s["table_cell"]),
         Paragraph("9 HSY stations city-wide", s["table_cell"]),
         Paragraph("~85% of streets unmonitored", s["table_cell"])],
        [Paragraph("Update frequency", s["table_cell"]),
         Paragraph("Hourly readings", s["table_cell"]),
         Paragraph("Misses 30-min pollution spikes", s["table_cell"])],
        [Paragraph("Forecast capability", s["table_cell"]),
         Paragraph("No predictive layer", s["table_cell"]),
         Paragraph("No proactive alerts possible", s["table_cell"])],
        [Paragraph("Cost per sensor", s["table_cell"]),
         Paragraph("€15,000–€40,000 (reference)", s["table_cell"]),
         Paragraph("Limits network expansion", s["table_cell"])],
        [Paragraph("Integration", s["table_cell"]),
         Paragraph("Siloed CSV exports", s["table_cell"]),
         Paragraph("No real-time API", s["table_cell"])],
    ]
    pt = Table(problem_rows, colWidths=[4.5*cm, 6*cm, 5.5*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("BACKGROUND", (0, 1), (-1, 1), LGRAY),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE),
        ("BACKGROUND", (0, 3), (-1, 3), LGRAY),
        ("BACKGROUND", (0, 4), (-1, 4), WHITE),
        ("BACKGROUND", (0, 5), (-1, 5), LGRAY),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("1.2 Regulatory and Policy Context", s["h2"]))
    for point in [
        "<b>EU Ambient Air Quality Directive (2008/50/EC):</b> Requires member states to "
        "monitor PM<sub rise=2 size=7>2.5</sub>, NO<sub rise=2 size=7>2</sub>, and O<sub rise=2 size=7>3</sub> at defined intervals. "
        "Fines for non-compliance can reach €150,000 per year.",
        "<b>Helsinki Smart City Strategy 2021–2025:</b> Explicitly calls for data-driven "
        "urban services, open data APIs, and citizen-facing environmental dashboards.",
        "<b>Horizon Europe Green Deal calls:</b> Dedicated funding streams for urban "
        "air quality platforms with AI/ML components (up to €3M per project, 2024–2026).",
        "<b>Nordic Clean Air Partnership:</b> Collaborative initiative requiring "
        "cross-border data exchange in standardised formats — a gap this platform addresses.",
    ]:
        story.append(Paragraph(f"• {point}", s["bullet"]))
        story.append(Spacer(1, 0.15*cm))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("1.3 Opportunity Size", s["h2"]))
    story.append(Paragraph(
        "The global smart city air quality market was valued at USD 3.2 billion in 2023 "
        "and is projected to reach USD 9.8 billion by 2030 (CAGR 17.4%). In the Nordic "
        "region alone, 14 major municipalities have active smart city procurement frameworks "
        "for environmental monitoring. The total addressable market for a cloud-based "
        "monitoring-as-a-service product in Scandinavia is estimated at €180M annually.",
        s["body"]
    ))
    return story


def solution_page(s):
    story = [PageBreak()]
    story.append(Paragraph("2. Solution Architecture", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL_L))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The Smart City Mini-Platform is a three-tier system: an IoT data layer, a machine "
        "learning inference layer, and a presentation layer. Each tier is independently "
        "deployable and swappable.",
        s["body"]
    ))

    # Architecture table
    arch_rows = [
        [Paragraph("Layer", s["table_header"]),
         Paragraph("Component", s["table_header"]),
         Paragraph("Technology", s["table_header"]),
         Paragraph("Output", s["table_header"])],
        [Paragraph("IoT Data", s["table_cell"]),
         Paragraph("Sensor simulator / real sensors", s["table_cell"]),
         Paragraph("Python · MQTT · paho", s["table_cell"]),
         Paragraph("30-min readings: AQI, traffic, energy, noise", s["table_cell"])],
        [Paragraph("Storage", s["table_cell"]),
         Paragraph("Time-series database", s["table_cell"]),
         Paragraph("MongoDB Atlas (free tier)", s["table_cell"]),
         Paragraph("Indexed by sensor + timestamp", s["table_cell"])],
        [Paragraph("ML Inference", s["table_cell"]),
         Paragraph("LSTM forecast model", s["table_cell"]),
         Paragraph("TensorFlow 2.x · scikit-learn", s["table_cell"]),
         Paragraph("12-hour AQI forecast + CI bands", s["table_cell"])],
        [Paragraph("Presentation", s["table_cell"]),
         Paragraph("Live dashboard", s["table_cell"]),
         Paragraph("Streamlit · Plotly", s["table_cell"]),
         Paragraph("KPIs · charts · heatmap · alert log", s["table_cell"])],
        [Paragraph("Alerting", s["table_cell"]),
         Paragraph("Threshold monitor", s["table_cell"]),
         Paragraph("Python · email/SMS API", s["table_cell"]),
         Paragraph("Push alerts at AQI > 100", s["table_cell"])],
    ]
    at = Table(arch_rows, colWidths=[2.8*cm, 4*cm, 4*cm, 5.2*cm])
    at.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("BACKGROUND", (0, 1), (-1, 1), LGRAY),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE),
        ("BACKGROUND", (0, 3), (-1, 3), LGRAY),
        ("BACKGROUND", (0, 4), (-1, 4), WHITE),
        ("BACKGROUND", (0, 5), (-1, 5), LGRAY),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(at)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("2.1 LSTM Model Design", s["h2"]))
    story.append(Paragraph(
        "The forecasting engine uses a 2-layer LSTM architecture with batch normalisation "
        "and dropout regularisation. The model ingests a 48-step lookback window (24 hours) "
        "of three features — AQI, traffic density, and energy consumption — and outputs "
        "24 AQI forecasts (12 hours at 30-minute resolution). This multi-variate, "
        "multi-step design extends the spatial-temporal modelling approach developed in "
        "the author's published IoT/air quality research (2017–2022).",
        s["body"]
    ))

    model_rows = [
        [Paragraph("Parameter", s["table_header"]), Paragraph("Value", s["table_header"]),
         Paragraph("Rationale", s["table_header"])],
        [Paragraph("Lookback window", s["table_cell"]), Paragraph("48 steps (24h)", s["table_cell"]),
         Paragraph("Captures daily cycle + rush hour patterns", s["table_cell"])],
        [Paragraph("Forecast horizon", s["table_cell"]), Paragraph("24 steps (12h)", s["table_cell"]),
         Paragraph("Actionable for city planners and public health", s["table_cell"])],
        [Paragraph("LSTM units", s["table_cell"]), Paragraph("64 → 32", s["table_cell"]),
         Paragraph("Hierarchical feature extraction", s["table_cell"])],
        [Paragraph("Dropout", s["table_cell"]), Paragraph("0.20", s["table_cell"]),
         Paragraph("Prevents overfitting on 60-day dataset", s["table_cell"])],
        [Paragraph("Training data", s["table_cell"]), Paragraph("60 days synthetic + HSY open data", s["table_cell"]),
         Paragraph("Includes seasonal variation", s["table_cell"])],
        [Paragraph("Test RMSE", s["table_cell"]), Paragraph("6.97 AQI units", s["table_cell"]),
         Paragraph("Below WHO 10-unit significance threshold", s["table_cell"])],
        [Paragraph("R² score", s["table_cell"]), Paragraph("0.788", s["table_cell"]),
         Paragraph("Strong predictive power for city-scale decisions", s["table_cell"])],
    ]
    mt = Table(model_rows, colWidths=[4*cm, 4*cm, 8*cm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LGRAY, WHITE]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(mt)
    return story


def business_model_page(s):
    story = [PageBreak()]
    story.append(Paragraph("3. Business Model & Value Proposition", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL_L))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("3.1 Business Model Canvas (Key Elements)", s["h2"]))

    bmc_rows = [
        [Paragraph("CUSTOMER SEGMENTS", s["table_header"]),
         Paragraph("VALUE PROPOSITIONS", s["table_header"]),
         Paragraph("REVENUE STREAMS", s["table_header"])],
        [
            Paragraph(
                "• Municipal authorities (Helsinki, Espoo, Tampere)\n"
                "• Regional health agencies (THL)\n"
                "• Urban planners & developers\n"
                "• Real-estate companies (ESG reporting)\n"
                "• Citizens via public dashboard", s["table_cell"]),
            Paragraph(
                "• Hyper-local AQI monitoring (500m resolution)\n"
                "• 12-hour predictive forecasts\n"
                "• Real-time public health alerts\n"
                "• Regulatory compliance reporting\n"
                "• Open API for 3rd-party integration\n"
                "• Cost: 90% below traditional networks", s["table_cell"]),
            Paragraph(
                "• SaaS subscription (€2,500/month per city)\n"
                "• Horizon Europe grant funding\n"
                "• Public sector procurement contracts\n"
                "• White-label licensing to Nordic cities\n"
                "• Consulting: custom sensor deployment", s["table_cell"]),
        ],
    ]
    bmc_t = Table(bmc_rows, colWidths=[5.3*cm, 5.3*cm, 5.4*cm])
    bmc_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), TEAL),
        ("BACKGROUND", (1, 0), (1, 0), PURPLE),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#854F0B")),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(bmc_t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("3.2 ROI Analysis — Helsinki Pilot", s["h2"]))
    story.append(Paragraph(
        "A 12-month pilot covering 3 districts (Kallio, Kamppi, Pasila) with 9 sensor "
        "nodes can be deployed at a fraction of the cost of expanding the physical "
        "HSY station network:",
        s["body"]
    ))

    roi_rows = [
        [Paragraph("Cost item", s["table_header"]),
         Paragraph("Traditional approach", s["table_header"]),
         Paragraph("This platform", s["table_header"]),
         Paragraph("Saving", s["table_header"])],
        [Paragraph("Sensor hardware (9 nodes)", s["table_cell"]),
         Paragraph("€270,000", s["table_cell"]),
         Paragraph("€18,000", s["table_cell"]),
         Paragraph("€252,000", s["table_cell"])],
        [Paragraph("Annual maintenance", s["table_cell"]),
         Paragraph("€45,000", s["table_cell"]),
         Paragraph("€3,600", s["table_cell"]),
         Paragraph("€41,400", s["table_cell"])],
        [Paragraph("Software / dashboard", s["table_cell"]),
         Paragraph("€80,000 (custom dev)", s["table_cell"]),
         Paragraph("€0 (open source)", s["table_cell"]),
         Paragraph("€80,000", s["table_cell"])],
        [Paragraph("Data storage (annual)", s["table_cell"]),
         Paragraph("€12,000 (on-prem)", s["table_cell"]),
         Paragraph("€0 (MongoDB Atlas free)", s["table_cell"]),
         Paragraph("€12,000", s["table_cell"])],
        [Paragraph("<b>TOTAL (Year 1)</b>", s["table_cell"]),
         Paragraph("<b>€407,000</b>", s["table_cell"]),
         Paragraph("<b>€21,600</b>", s["table_cell"]),
         Paragraph("<b>€385,400 (95%)</b>", s["table_cell"])],
    ]
    roi_t = Table(roi_rows, colWidths=[5.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    roi_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AMBER),
        ("BACKGROUND", (0, 1), (-1, 4), None),
        ("BACKGROUND", (0, 5), (-1, 5), colors.HexColor("#FAEEDA")),
        ("ROWBACKGROUNDS", (0, 1), (-1, 4), [WHITE, LGRAY]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(roi_t)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("3.3 SWOT Analysis", s["h2"]))
    swot_rows = [
        [Paragraph("STRENGTHS", s["table_header"]), Paragraph("WEAKNESSES", s["table_header"])],
        [
            Paragraph(
                "• Built on proven research (LSTM + IoT, RIT Bangalore 2017–22)\n"
                "• Open-source stack: zero licensing cost\n"
                "• Scalable: add sensors without re-architecting\n"
                "• Aligns with Helsinki Smart City Strategy", s["table_cell"]),
            Paragraph(
                "• Synthetic training data: model not yet validated on live HSY data\n"
                "• No hardware prototypes yet (simulation only)\n"
                "• Single-person team: scaling requires partnerships", s["table_cell"]),
        ],
        [Paragraph("OPPORTUNITIES", s["table_header"]), Paragraph("THREATS", s["table_header"])],
        [
            Paragraph(
                "• Horizon Europe Green Deal funding (2024–2026)\n"
                "• 14 Nordic municipalities with active smart city procurement\n"
                "• EU Air Quality Directive revision driving compliance demand\n"
                "• HSY open data API — free ground truth for model validation", s["table_cell"]),
            Paragraph(
                "• Established competitors (Airly, BreezOMETER)\n"
                "• Municipal procurement cycles: 12–24 month timelines\n"
                "• GDPR constraints on location-tagged sensor data\n"
                "• IoT sensor calibration drift over time", s["table_cell"]),
        ],
    ]
    swot_t = Table(swot_rows, colWidths=[8*cm, 8*cm])
    swot_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), TEAL),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#3C3489")),
        ("BACKGROUND", (0, 2), (0, 2), colors.HexColor("#0F6E56")),
        ("BACKGROUND", (1, 2), (1, 2), colors.HexColor("#A32D2D")),
        ("BACKGROUND", (0, 1), (-1, 1), LGRAY),
        ("BACKGROUND", (0, 3), (-1, 3), LGRAY),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(swot_t)
    return story


def roadmap_page(s):
    story = [PageBreak()]
    story.append(Paragraph("4. Implementation Roadmap & Next Steps", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL_L))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The platform has been built in 8 weeks as a portfolio project demonstrating "
        "end-to-end capability. Below is the path from portfolio prototype to production "
        "pilot with Helsinki City Environment Services.",
        s["body"]
    ))

    road_rows = [
        [Paragraph("Phase", s["table_header"]),
         Paragraph("Timeline", s["table_header"]),
         Paragraph("Deliverable", s["table_header"]),
         Paragraph("Status", s["table_header"])],
        [Paragraph("1 — IoT Simulation", s["table_cell"]),
         Paragraph("Wk 1–2", s["table_cell"]),
         Paragraph("Sensor simulator + MongoDB schema", s["table_cell"]),
         Paragraph("✅ Complete", s["table_cell"])],
        [Paragraph("2 — LSTM Engine", s["table_cell"]),
         Paragraph("Wk 3–4", s["table_cell"]),
         Paragraph("Trained model, RMSE 6.97, R² 0.788", s["table_cell"]),
         Paragraph("✅ Complete", s["table_cell"])],
        [Paragraph("3 — Dashboard", s["table_cell"]),
         Paragraph("Wk 5–6", s["table_cell"]),
         Paragraph("Live Streamlit app (Streamlit Cloud)", s["table_cell"]),
         Paragraph("✅ Complete", s["table_cell"])],
        [Paragraph("4 — Business Case", s["table_cell"]),
         Paragraph("Wk 7", s["table_cell"]),
         Paragraph("This document", s["table_cell"]),
         Paragraph("✅ Complete", s["table_cell"])],
        [Paragraph("5 — Portfolio Publish", s["table_cell"]),
         Paragraph("Wk 8", s["table_cell"]),
         Paragraph("GitHub + LinkedIn write-up + demo video", s["table_cell"]),
         Paragraph("🔄 In progress", s["table_cell"])],
        [Paragraph("6 — HSY Data Integration", s["table_cell"]),
         Paragraph("Q3 2025", s["table_cell"]),
         Paragraph("Replace synthetic data with live HSY API", s["table_cell"]),
         Paragraph("⬜ Planned", s["table_cell"])],
        [Paragraph("7 — Hardware Pilot", s["table_cell"]),
         Paragraph("Q4 2025", s["table_cell"]),
         Paragraph("3 × Raspberry Pi + BME688 sensors in Kallio", s["table_cell"]),
         Paragraph("⬜ Planned", s["table_cell"])],
        [Paragraph("8 — Municipality Pitch", s["table_cell"]),
         Paragraph("Q1 2026", s["table_cell"]),
         Paragraph("Formal proposal to HSY + Horizon Europe application", s["table_cell"]),
         Paragraph("⬜ Planned", s["table_cell"])],
    ]
    rt = Table(road_rows, colWidths=[4*cm, 2.5*cm, 6.5*cm, 3*cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LGRAY, WHITE]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("4.1 Why This Portfolio Project Matters", s["h2"]))
    story.append(Paragraph(
        "This project is not a standard academic exercise. It is a complete, "
        "deployable system that demonstrates the intersection of three professional "
        "skill domains rarely combined in a single profile:",
        s["body"]
    ))
    for point in [
        "<b>Research continuity:</b> The LSTM methodology directly extends published "
        "work on IoT air quality monitoring (RIT Bangalore, 2017–2022) into a modern "
        "cloud-native deployment context.",
        "<b>Business Informatics application:</b> The Business Model Canvas, SWOT, and "
        "ROI analysis demonstrate the Digital Strategy and Business Modeling coursework "
        "from the Metropolia MBI programme applied to a real product.",
        "<b>Technical breadth:</b> The stack spans IoT simulation, NoSQL databases, "
        "deep learning, cloud deployment, and data visualisation — reflecting both the "
        "M.Tech (Computer Network Engineering) background and current AI/ML certifications.",
        "<b>Helsinki relevance:</b> Using HSY open data and referencing the Helsinki "
        "Smart City Strategy 2021–2025 signals local market awareness, directly relevant "
        "for roles at Finnish tech companies, city agencies, or Nordic consultancies.",
    ]:
        story.append(Paragraph(f"• {point}", s["bullet"]))
        story.append(Spacer(1, 0.15*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("4.2 Contact & Links", s["h2"]))

    contact_rows = [
        [Paragraph("Resource", s["table_header"]), Paragraph("Link / Contact", s["table_header"])],
        [Paragraph("GitHub repository", s["table_cell"]),
         Paragraph("github.com/shreevidyag/smart-city-platform", s["table_cell"])],
        [Paragraph("Live dashboard demo", s["table_cell"]),
         Paragraph("smart-city-helsinki.streamlit.app", s["table_cell"])],
        [Paragraph("LinkedIn", s["table_cell"]),
         Paragraph("linkedin.com/in/shreevidya-gurudath-6437b9200", s["table_cell"])],
        [Paragraph("Email", s["table_cell"]),
         Paragraph("shreevidyag@gmail.com", s["table_cell"])],
        [Paragraph("Helsinki open data (HSY)", s["table_cell"]),
         Paragraph("hsy.fi/en/air-quality | api.hel.fi", s["table_cell"])],
    ]
    ct = Table(contact_rows, colWidths=[5*cm, 11*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LGRAY, WHITE]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(ct)

    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL_L))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Smart City Mini-Platform · Business Case · Shree Vidya Gurudath · MBI, Metropolia UAS · May 2025  |  "
        "Built with Python · TensorFlow · MongoDB · Streamlit",
        s["footer"]
    ))
    return story


def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2.2*cm, bottomMargin=2*cm,
        title="Smart City Platform — Business Case",
        author="Shree Vidya Gurudath",
        subject="Business case for Helsinki Smart City monitoring platform",
    )
    s = build_styles()
    story = []
    story += cover_page(s)
    story += problem_page(s)
    story += solution_page(s)
    story += business_model_page(s)
    story += roadmap_page(s)
    doc.build(story)
    print(f"  ✓ PDF written → {output_path}")


if __name__ == "__main__":
    build_pdf("smart_city_business_case.pdf")
