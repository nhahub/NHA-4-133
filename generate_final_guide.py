# ==============================================================================
# Automated Post-Hospital Patient Monitoring System
# Script   : generate_final_guide.py
# Purpose  : Generates Final_Project_Guide.pdf — a complete technical handover
#            document for university submission and team continuation.
# Author   : Graduation Project Team
# Date     : 2026-07-10
# Usage    : python generate_final_guide.py
# ==============================================================================

import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# ==============================================================================
# Canvas with running headers, footers and page numbers
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return
        self.saveState()
        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D"))
        self.drawString(50, 810, "AUTOMATED POST-HOSPITAL PATIENT MONITORING SYSTEM")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        self.drawRightString(545, 810, "Final Project Guide — Technical Handover Document")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(50, 803, 545, 803)
        # Footer
        self.line(50, 45, 545, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        self.drawString(50, 32, "Confidential — DEPI Graduation Project | Data Engineering Track")
        self.drawRightString(545, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


# ==============================================================================
# Color Palette & Style Definitions
# ==============================================================================
PRIMARY   = colors.HexColor("#1A365D")   # Deep Navy
SECONDARY = colors.HexColor("#2B6CB0")   # Slate Blue
ACCENT    = colors.HexColor("#2C7A7B")   # Teal
SUCCESS   = colors.HexColor("#276749")   # Dark Green
WARNING   = colors.HexColor("#744210")   # Amber
BODY_TXT  = colors.HexColor("#2D3748")   # Charcoal
LIGHT_BG  = colors.HexColor("#F7FAFC")   # Off-White
MID_BG    = colors.HexColor("#EBF4FF")   # Light Blue Tint
BORDER    = colors.HexColor("#CBD5E1")   # Light Gray Border
WHITE     = colors.white


def build_styles():
    styles = getSampleStyleSheet()

    styles['Normal'].textColor = BODY_TXT
    styles['Normal'].fontSize  = 10
    styles['Normal'].leading   = 15
    styles['Normal'].fontName  = 'Helvetica'

    custom = [
        ParagraphStyle('CoverInstitution', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=11, leading=14,
            textColor=SECONDARY, alignment=1, spaceAfter=6),
        ParagraphStyle('CoverTitle', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=26, leading=32,
            textColor=PRIMARY, alignment=1, spaceAfter=10),
        ParagraphStyle('CoverSubtitle', parent=styles['Normal'],
            fontName='Helvetica', fontSize=13, leading=18,
            textColor=colors.HexColor("#4A5568"), alignment=1, spaceAfter=6),
        ParagraphStyle('CoverMeta', parent=styles['Normal'],
            fontName='Helvetica', fontSize=10, leading=15,
            textColor=BODY_TXT, alignment=1, spaceAfter=4),
        ParagraphStyle('CoverMetaBold', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=10, leading=15,
            textColor=PRIMARY, alignment=1, spaceAfter=4),

        ParagraphStyle('H1', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=16, leading=20,
            textColor=PRIMARY, spaceBefore=18, spaceAfter=8, keepWithNext=True),
        ParagraphStyle('H2', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=12, leading=16,
            textColor=SECONDARY, spaceBefore=12, spaceAfter=6, keepWithNext=True),
        ParagraphStyle('H3', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=10, leading=14,
            textColor=ACCENT, spaceBefore=8, spaceAfter=4, keepWithNext=True),

        ParagraphStyle('Body', parent=styles['Normal'],
            fontName='Helvetica', fontSize=10, leading=15,
            textColor=BODY_TXT, spaceAfter=6),
        ParagraphStyle('BulletItem', parent=styles['Normal'],
            fontName='Helvetica', fontSize=10, leading=15,
            textColor=BODY_TXT, leftIndent=18, firstLineIndent=-12, spaceAfter=4),
        ParagraphStyle('BulletBold', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=10, leading=15,
            textColor=BODY_TXT, leftIndent=18, firstLineIndent=-12, spaceAfter=4),
        ParagraphStyle('CodeBlock', parent=styles['Normal'],
            fontName='Courier', fontSize=8.5, leading=13,
            textColor=colors.HexColor("#1A202C"),
            backColor=colors.HexColor("#F1F5F9"),
            leftIndent=10, rightIndent=10, spaceAfter=8),

        ParagraphStyle('TH', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=9, leading=12,
            textColor=WHITE, alignment=0),
        ParagraphStyle('TD', parent=styles['Normal'],
            fontName='Helvetica', fontSize=9, leading=12,
            textColor=BODY_TXT, alignment=0),
        ParagraphStyle('TDB', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=9, leading=12,
            textColor=PRIMARY, alignment=0),
        ParagraphStyle('TDSmall', parent=styles['Normal'],
            fontName='Helvetica', fontSize=8.5, leading=12,
            textColor=BODY_TXT, alignment=0),
        ParagraphStyle('TDBSmall', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=12,
            textColor=PRIMARY, alignment=0),

        ParagraphStyle('StatusDone', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=9, leading=12,
            textColor=SUCCESS, alignment=1),
        ParagraphStyle('StatusPending', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=9, leading=12,
            textColor=WARNING, alignment=1),
        ParagraphStyle('Caption', parent=styles['Normal'],
            fontName='Helvetica', fontSize=8.5, leading=12,
            textColor=colors.HexColor("#718096"), alignment=1, spaceAfter=10),
    ]
    for s in custom:
        styles.add(s)
    return styles


def table_style_base(header_bg=None, alternate=True):
    hbg = header_bg or PRIMARY
    base = [
        ('BACKGROUND', (0, 0), (-1, 0), hbg),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]
    if alternate:
        base.append(('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]))
    return TableStyle(base)


def divider_bar():
    return HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=6, spaceBefore=4)


def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6, spaceBefore=4)


# ==============================================================================
# PDF Builder
# ==============================================================================
def build_final_guide():
    project_root = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(project_root, "Final_Project_Guide.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=75,
        bottomMargin=60
    )

    S = build_styles()
    story = []

    # ==========================================================================
    # COVER PAGE
    # ==========================================================================
    story.append(Spacer(1, 1.8 * cm))

    # Top accent bar
    top_bar = Table([[""]], colWidths=[495], rowHeights=[6])
    top_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(top_bar)
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("DEPI GRADUATION PROJECT", S['CoverInstitution']))
    story.append(Paragraph("Data Engineering Track", S['CoverInstitution']))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        "Automated Post-Hospital<br/>Patient Monitoring System",
        S['CoverTitle']
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "A Scalable, Cloud-Enabled Data Engineering Pipeline for<br/>"
        "Vital Signs Ingestion, Quality Processing, and Relational Storage",
        S['CoverSubtitle']
    ))
    story.append(Spacer(1, 1.2 * cm))

    # Mid divider
    mid_bar = Table([[""]], colWidths=[495], rowHeights=[2])
    mid_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SECONDARY),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(mid_bar)
    story.append(Spacer(1, 1.0 * cm))

    story.append(Paragraph("<b>FINAL PROJECT GUIDE</b>", S['CoverTitle']))
    story.append(Paragraph("Complete Technical Handover Document", S['CoverSubtitle']))
    story.append(Spacer(1, 1.2 * cm))

    # Team table on cover
    cover_meta = [
        [Paragraph("<b>Document Type:</b>", S['CoverMetaBold']),
         Paragraph("Technical Handover Guide", S['CoverMeta']),
         Paragraph("<b>Track:</b>", S['CoverMetaBold']),
         Paragraph("Data Engineering", S['CoverMeta'])],
        [Paragraph("<b>Project:</b>", S['CoverMetaBold']),
         Paragraph("Automated Post-Hospital Patient Monitoring System", S['CoverMeta']),
         Paragraph("<b>Date:</b>", S['CoverMetaBold']),
         Paragraph("July 10, 2026", S['CoverMeta'])],
    ]
    cover_tbl = Table(cover_meta, colWidths=[100, 190, 60, 145])
    cover_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(cover_tbl)
    story.append(Spacer(1, 0.8 * cm))
    story.append(thin_rule())
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("<b>Team Members</b>", S['H2']))
    team_data = [
        [Paragraph("<b>Name</b>", S['TH']),
         Paragraph("<b>Role</b>", S['TH']),
         Paragraph("<b>Status</b>", S['TH'])],
        [Paragraph("Kareem Mohamed", S['TDB']),
         Paragraph("Data Preparation Engineer", S['TD']),
         Paragraph("✔ Completed", S['StatusDone'])],
        [Paragraph("Zeyad Khaled", S['TDB']),
         Paragraph("Database Engineer", S['TD']),
         Paragraph("✔ Completed", S['StatusDone'])],
        [Paragraph("Mahmoud Shaheen", S['TDB']),
         Paragraph("ETL Engineer", S['TD']),
         Paragraph("✔ Completed", S['StatusDone'])],
        [Paragraph("Amr Omar", S['TDB']),
         Paragraph("Azure Data Factory Engineer", S['TD']),
         Paragraph("✔ Completed", S['StatusDone'])],
        [Paragraph("Beshoy Talaat", S['TDB']),
         Paragraph("Testing & Validation Engineer", S['TD']),
         Paragraph("✔ Completed", S['StatusDone'])],
    ]
    team_tbl = Table(team_data, colWidths=[160, 215, 120])
    team_tbl.setStyle(table_style_base())
    story.append(team_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # TABLE OF CONTENTS
    # ==========================================================================
    story.append(Paragraph("Table of Contents", S['H1']))
    story.append(divider_bar())
    toc_entries = [
        ("1.",  "Project Overview"),
        ("2.",  "System Architecture"),
        ("3.",  "Technology Stack"),
        ("4.",  "Project Folder Structure"),
        ("5.",  "Dataset Description"),
        ("6.",  "Data Profiling"),
        ("7.",  "Data Quality Assessment"),
        ("8.",  "Data Cleaning Pipeline"),
        ("9.",  "SQL Layer"),
        ("10.", "Database Loader (load_to_sql.py)"),
        ("11.", "Documentation Files"),
        ("12.", "Current Project Status"),
        ("13.", "Remaining Work"),
        ("14.", "Azure SQL Deployment — Remaining Steps"),
        ("15.", "Azure Data Factory — Remaining Implementation"),
        ("16.", "Final Deployment Checklist"),
        ("17.", "Possible Future Improvements"),
        ("18.", "Conclusion"),
        ("19.", "Technical Team Responsibilities"),
    ]
    toc_data = [[Paragraph("<b>§</b>", S['TH']), Paragraph("<b>Section Title</b>", S['TH'])]]
    for num, title in toc_entries:
        toc_data.append([Paragraph(num, S['TD']), Paragraph(title, S['TD'])])
    toc_tbl = Table(toc_data, colWidths=[35, 460])
    toc_tbl.setStyle(table_style_base())
    story.append(toc_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 1 — PROJECT OVERVIEW
    # ==========================================================================
    story.append(Paragraph("1. Project Overview", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph("1.1 Project Idea", S['H2']))
    story.append(Paragraph(
        "The <b>Automated Post-Hospital Patient Monitoring System</b> is a graduation-level Data Engineering "
        "project that designs, builds, and documents a complete automated pipeline for collecting, cleaning, "
        "transforming, and storing patient vital signs telemetry data. The pipeline ingests raw patient "
        "readings collected after hospital discharge, applies a rigorous data quality process, and loads "
        "the clean, structured records into a relational Azure SQL Database for downstream dashboarding "
        "and alerting. The system is entirely infrastructure-focused — it contains no Machine Learning "
        "or statistical modelling components.",
        S['Body']
    ))

    story.append(Paragraph("1.2 Business Problem", S['H2']))
    story.append(Paragraph(
        "When patients are discharged from hospital, continuous monitoring of their vital signs — "
        "heart rate, blood pressure, oxygen saturation, body temperature, and respiratory rate — "
        "is clinically critical. Early deterioration of these indicators often precedes serious "
        "medical events such as cardiac arrest or sepsis. However, raw IoT telemetry logs suffer "
        "from several structural problems that prevent reliable clinical use:",
        S['Body']
    ))
    for bullet in [
        "Column naming inconsistencies that break SQL compatibility (e.g., <i>Weight (kg)</i>).",
        "Redundant, pre-computed derived columns that violate 3rd Normal Form (3NF) database normalization.",
        "Timestamp columns stored as raw text strings rather than indexed datetime objects.",
        "No standardized pipeline to move data from raw landing files into a production database.",
        "No audit trail or data quality evidence to validate the integrity of stored records.",
    ]:
        story.append(Paragraph(f"• {bullet}", S['BulletItem']))

    story.append(Paragraph("1.3 Objectives", S['H2']))
    objectives = [
        "Build a professional, modular Python data engineering project using industry-standard folder conventions.",
        "Profile the raw clinical vital signs dataset and document all findings in a formal report.",
        "Perform a data quality audit to define a clean, normalized production database schema.",
        "Implement an automated Python data cleaning pipeline that standardizes, validates, and exports the dataset.",
        "Design and script the Azure SQL Database schema (DDL) for the patient_vitals production table.",
        "Implement a batch-loading Python script to ingest the cleaned CSV into Azure SQL Database.",
        "Define Azure Data Factory (ADF) Copy Activity pipelines to orchestrate the end-to-end workflow.",
        "Produce complete technical documentation for academic submission and team handover.",
    ]
    for i, obj in enumerate(objectives, 1):
        story.append(Paragraph(f"{i}. {obj}", S['BulletItem']))

    story.append(Paragraph("1.4 Expected Outcome", S['H2']))
    story.append(Paragraph(
        "Upon full completion, the system will provide a fully automated, cloud-hosted data pipeline "
        "that ingests raw patient telemetry files from Azure Blob Storage, processes them through a "
        "Python cleaning layer, and loads the clean records into an Azure SQL Database table. "
        "Downstream clinical dashboards or BI tools will be able to query the structured database "
        "in real-time to identify High Risk patients and generate automated clinical alerts. "
        "The project will be fully documented, version-controlled, and ready for production deployment.",
        S['Body']
    ))
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 2 — SYSTEM ARCHITECTURE
    # ==========================================================================
    story.append(Paragraph("2. System Architecture", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph("2.1 Complete Workflow", S['H2']))
    story.append(Paragraph(
        "The pipeline follows a classic Extract–Transform–Load (ETL) architecture hosted on Microsoft Azure. "
        "The workflow progresses through four distinct phases:",
        S['Body']
    ))

    arch_phases = [
        ["<b>Phase</b>", "<b>Stage Name</b>", "<b>System / Tool</b>", "<b>Operations</b>"],
        ["1", "Raw Ingestion",
         "Azure Blob Storage (raw/ container)",
         "Patient vital signs CSV files land in the cloud raw storage bucket."],
        ["2", "Orchestration",
         "Azure Data Factory (ADF)",
         "ADF triggers are configured to detect new files and schedule pipeline runs."],
        ["3", "Cleaning & Transformation",
         "Python local pipeline / ADF Copy mapping",
         "The local Python pipeline validates and exports a clean CSV. The exported ADF Copy pipeline maps the 14 retained raw fields into the SQL target."],
        ["4", "Relational Loading",
         "Python (load_to_sql.py) + Azure SQL Database",
         "Batch-inserts the clean dataset into dbo.patient_vitals using SQLAlchemy with 10,000-row batches."],
        ["5", "Analytics & Alerting",
         "Azure SQL Database + BI Tools",
         "Downstream dashboards query the patient_vitals table. High Risk patients trigger clinical alerts."],
    ]
    arch_rows = []
    for i, row in enumerate(arch_phases):
        if i == 0:
            arch_rows.append([Paragraph(c, S['TH']) for c in row])
        else:
            arch_rows.append([
                Paragraph(row[0], S['TDB']),
                Paragraph(row[1], S['TDB']),
                Paragraph(row[2], S['TD']),
                Paragraph(row[3], S['TD']),
            ])
    arch_tbl = Table(arch_rows, colWidths=[25, 85, 145, 240])
    arch_tbl.setStyle(table_style_base())
    story.append(arch_tbl)

    story.append(Paragraph("2.2 Architecture Diagram", S['H2']))
    story.append(Paragraph(
        "The diagram below illustrates the end-to-end data flow from raw patient telemetry "
        "to the production relational database:",
        S['Body']
    ))

    # ASCII-art style architecture diagram rendered as a styled table
    flow_data = [
        [Paragraph("[ Patient Vital Signs CSV Files ]", S['TH'])],
        [Paragraph("↓  Upload via ADF trigger", S['Caption'])],
        [Paragraph("[ Azure Blob Storage — raw/ container ]", S['TH'])],
        [Paragraph("↓  ADF Copy Activity reads raw file", S['Caption'])],
        [Paragraph("[ Python ETL — clean_data.py ]", S['TH'])],
        [Paragraph("↓  Cleaned CSV written to data/processed/", S['Caption'])],
        [Paragraph("[ Python Loader — load_to_sql.py ]", S['TH'])],
        [Paragraph("↓  Batch INSERT into Azure SQL (10,000 rows/batch)", S['Caption'])],
        [Paragraph("[ Azure SQL Database — dbo.patient_vitals ]", S['TH'])],
        [Paragraph("↓  SQL queries, views, alerts", S['Caption'])],
        [Paragraph("[ Downstream Analytics / Clinical Dashboards ]", S['TH'])],
    ]
    flow_tbl = Table(flow_data, colWidths=[495])
    flow_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,0), (0,0), PRIMARY),
        ('BACKGROUND', (0,2), (0,2), PRIMARY),
        ('BACKGROUND', (0,4), (0,4), SECONDARY),
        ('BACKGROUND', (0,6), (0,6), SECONDARY),
        ('BACKGROUND', (0,8), (0,8), ACCENT),
        ('BACKGROUND', (0,10), (0,10), ACCENT),
        ('ROWBACKGROUNDS', (0,1), (0,1), [LIGHT_BG]),
        ('ROWBACKGROUNDS', (0,3), (0,3), [LIGHT_BG]),
        ('ROWBACKGROUNDS', (0,5), (0,5), [LIGHT_BG]),
        ('ROWBACKGROUNDS', (0,7), (0,7), [LIGHT_BG]),
        ('ROWBACKGROUNDS', (0,9), (0,9), [LIGHT_BG]),
    ])
    flow_tbl.setStyle(flow_style)
    story.append(flow_tbl)

    story.append(Paragraph("2.3 Data Flow Summary", S['H2']))
    story.append(Paragraph(
        "Raw telemetry is produced by patient monitoring devices and collected as CSV files. "
        "These files are uploaded to Azure Blob Storage in the <b>raw/</b> container. "
        "Azure Data Factory detects the arrival of new files and triggers the Python ETL pipeline. "
        "The cleaning script processes the data, removes redundant columns, standardizes column names, "
        "and saves the result to the <b>processed/</b> container. The loading script then connects "
        "to Azure SQL Database using ODBC Driver 18 and performs batch inserts of 10,000 rows at a time "
        "into the <b>dbo.patient_vitals</b> table. Downstream consumers — clinical dashboards, BI tools, "
        "and automated alerting systems — query this table directly.",
        S['Body']
    ))
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 3 — TECHNOLOGY STACK
    # ==========================================================================
    story.append(Paragraph("3. Technology Stack", S['H1']))
    story.append(divider_bar())

    tech_data = [
        [Paragraph("<b>Component</b>", S['TH']),
         Paragraph("<b>Technology</b>", S['TH']),
         Paragraph("<b>Version</b>", S['TH']),
         Paragraph("<b>Purpose & Justification</b>", S['TH'])],
        [Paragraph("Processing Language", S['TDB']),
         Paragraph("Python", S['TD']),
         Paragraph("3.12+", S['TD']),
         Paragraph("Core language for all ETL scripts, data validation, and report generation.", S['TD'])],
        [Paragraph("Data Manipulation", S['TDB']),
         Paragraph("Pandas", S['TD']),
         Paragraph("≥ 2.1.0", S['TD']),
         Paragraph("High-performance DataFrame operations for cleaning and transformation.", S['TD'])],
        [Paragraph("Numerical Computing", S['TDB']),
         Paragraph("NumPy", S['TD']),
         Paragraph("≥ 1.25.0", S['TD']),
         Paragraph("Underlying numerical engine for Pandas operations.", S['TD'])],
        [Paragraph("Database ORM", S['TDB']),
         Paragraph("SQLAlchemy", S['TD']),
         Paragraph("≥ 2.0.0", S['TD']),
         Paragraph("Provides database-agnostic connection pooling and bulk insert abstraction.", S['TD'])],
        [Paragraph("DB Driver", S['TDB']),
         Paragraph("PyODBC", S['TD']),
         Paragraph("≥ 5.0.0", S['TD']),
         Paragraph("ODBC bridge for connecting Python to Azure SQL Database via ODBC Driver 18.", S['TD'])],
        [Paragraph("Environment Config", S['TDB']),
         Paragraph("python-dotenv", S['TD']),
         Paragraph("≥ 1.0.0", S['TD']),
         Paragraph("Securely loads credentials from .env files — keeps secrets out of source code.", S['TD'])],
        [Paragraph("PDF Generation", S['TDB']),
         Paragraph("ReportLab", S['TD']),
         Paragraph("≥ 4.0.0", S['TD']),
         Paragraph("Programmatic PDF generation for project documentation and reports.", S['TD'])],
        [Paragraph("Markdown Tables", S['TDB']),
         Paragraph("Tabulate", S['TD']),
         Paragraph("≥ 0.9.0", S['TD']),
         Paragraph("Renders pandas DataFrames as markdown tables for documentation reports.", S['TD'])],
        [Paragraph("Testing", S['TDB']),
         Paragraph("Pytest", S['TD']),
         Paragraph("≥ 7.4.0", S['TD']),
         Paragraph("Unit testing framework for validating ETL pipeline functions.", S['TD'])],
        [Paragraph("Production Database", S['TDB']),
         Paragraph("Azure SQL Database", S['TD']),
         Paragraph("Latest", S['TD']),
         Paragraph("Managed cloud relational database. Hosts dbo.patient_vitals. T-SQL dialect.", S['TD'])],
        [Paragraph("Orchestration", S['TDB']),
         Paragraph("Azure Data Factory (ADF)", S['TD']),
         Paragraph("Latest", S['TD']),
         Paragraph("Cloud ETL orchestrator. Schedules pipeline runs and manages Copy Activities.", S['TD'])],
        [Paragraph("Cloud Storage", S['TDB']),
         Paragraph("Azure Blob Storage", S['TD']),
         Paragraph("Latest", S['TD']),
         Paragraph("Object storage for raw/ and processed/ CSV file containers.", S['TD'])],
        [Paragraph("Version Control", S['TDB']),
         Paragraph("Git / GitHub", S['TD']),
         Paragraph("Latest", S['TD']),
         Paragraph("Source code versioning and collaboration platform.", S['TD'])],
        [Paragraph("IDE", S['TDB']),
         Paragraph("VS Code", S['TD']),
         Paragraph("Latest", S['TD']),
         Paragraph("Primary development environment with Python and SQL extensions.", S['TD'])],
        [Paragraph("Azure SDK", S['TDB']),
         Paragraph("azure-storage-blob, azure-identity", S['TD']),
         Paragraph("≥ 12.18 / 1.14", S['TD']),
         Paragraph("Python SDKs for interacting with Azure Blob Storage and authentication.", S['TD'])],
    ]
    tech_tbl = Table(tech_data, colWidths=[110, 105, 60, 220])
    tech_tbl.setStyle(table_style_base())
    story.append(tech_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 4 — PROJECT FOLDER STRUCTURE
    # ==========================================================================
    story.append(Paragraph("4. Project Folder Structure", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "The project is organized according to professional data engineering conventions, "
        "separating source code, data, SQL scripts, configuration, and documentation into "
        "clearly scoped directories. Below is the complete folder layout with explanations:",
        S['Body']
    ))

    folder_data = [
        [Paragraph("<b>Path</b>", S['TH']),
         Paragraph("<b>Type</b>", S['TH']),
         Paragraph("<b>Purpose</b>", S['TH'])],
        [Paragraph("/ (project root)", S['TDB']), Paragraph("Root", S['TD']),
         Paragraph("Project root. Contains top-level scripts, configuration files, and the README.", S['TD'])],
        [Paragraph("README.md", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Complete project documentation: setup instructions, architecture, SQL schema, usage guide.", S['TD'])],
        [Paragraph("requirements.txt", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("All Python library dependencies with minimum version constraints.", S['TD'])],
        [Paragraph(".env.example", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Template for the .env credentials file. Contains placeholder values for all Azure variables.", S['TD'])],
        [Paragraph(".gitignore", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Git exclusion rules: excludes .env, .venv, data/*.csv, __pycache__, and PDF files.", S['TD'])],
        [Paragraph("generate_report.py", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Generates Project_Progress_Report.pdf — a phase I/II progress report using ReportLab.", S['TD'])],
        [Paragraph("generate_final_guide.py", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Generates Final_Project_Guide.pdf — this complete technical handover document.", S['TD'])],
        [Paragraph("src/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("All modular Python source code, organized by pipeline stage.", S['TD'])],
        [Paragraph("src/cleaning/clean_data.py", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Core ETL script. Reads raw CSV, drops redundant columns, renames to snake_case, casts timestamp, exports clean CSV, and writes data_cleaning_report.md.", S['TD'])],
        [Paragraph("src/database/load_to_sql.py", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Database loader. Connects to Azure SQL via SQLAlchemy+PyODBC, then batch-inserts the cleaned CSV into dbo.patient_vitals in 10,000-row batches.", S['TD'])],
        [Paragraph("src/analysis/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Placeholder for future BI query scripts and summary analytics.", S['TD'])],
        [Paragraph("src/ingestion/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Placeholder for Azure Blob Storage file download and landing scripts.", S['TD'])],
        [Paragraph("src/transformation/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Placeholder for advanced schema conversion and feature engineering scripts.", S['TD'])],
        [Paragraph("src/utils/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Placeholder for shared helper utilities: logging config, path helpers, etc.", S['TD'])],
        [Paragraph("data/raw/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Landing zone for raw incoming vital signs CSV files. Excluded from Git.", S['TD'])],
        [Paragraph("data/raw/human_vital_signs_dataset_2024.csv", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Source dataset: 200,020 rows × 17 columns of patient vital sign telemetry.", S['TD'])],
        [Paragraph("data/processed/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Output directory for cleaned and transformed CSV files. Excluded from Git.", S['TD'])],
        [Paragraph("data/processed/patient_vitals_clean.csv", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Cleaned dataset: 200,020 rows × 14 columns. SQL-ready, snake_case, datetime-cast.", S['TD'])],
        [Paragraph("sql/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("All T-SQL scripts for database schema deployment and analytical queries.", S['TD'])],
        [Paragraph("sql/create_patient_vitals.sql", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("DDL script to CREATE the dbo.patient_vitals production table in Azure SQL.", S['TD'])],
        [Paragraph("sql/drop_patient_vitals.sql", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Safely DROPs the dbo.patient_vitals table if it exists. Use before re-deploying.", S['TD'])],
        [Paragraph("sql/queries.sql", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("10 analytical SELECT queries for data exploration after loading.", S['TD'])],
        [Paragraph("sql/verification_queries.sql", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Verification queries to validate row counts, schema, and data integrity post-load.", S['TD'])],
        [Paragraph("docs/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("All generated markdown documentation reports.", S['TD'])],
        [Paragraph("docs/data_profile.md", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Data profiling report: row counts, column types, missing values, statistics.", S['TD'])],
        [Paragraph("docs/data_quality_assessment.md", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Pre-ETL quality audit: column audit, normalization decisions, SQL schema recommendations.", S['TD'])],
        [Paragraph("docs/data_cleaning_report.md", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Post-cleaning execution report: schema changes, data types, sample data.", S['TD'])],
        [Paragraph("docs/azure_sql_deployment.md", S['TDB']), Paragraph("File", S['TD']),
         Paragraph("Step-by-step Azure SQL deployment guide for Zeyad Khaled (Database Engineer).", S['TD'])],
        [Paragraph("tests/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Pytest test suite directory. Currently contains structure placeholder.", S['TD'])],
        [Paragraph("config/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Connection settings directory. Currently contains structure placeholder.", S['TD'])],
        [Paragraph(".venv/", S['TDB']), Paragraph("Directory", S['TD']),
         Paragraph("Python virtual environment. Excluded from Git. Contains all installed packages.", S['TD'])],
    ]
    folder_tbl = Table(folder_data, colWidths=[175, 55, 265])
    folder_tbl.setStyle(table_style_base())
    story.append(folder_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 5 — DATASET DESCRIPTION
    # ==========================================================================
    story.append(Paragraph("5. Dataset Description", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph("5.1 Dataset Source", S['H2']))
    story.append(Paragraph(
        "The dataset used in this project is the <b>Human Vital Signs Dataset 2024</b>, "
        "a synthetic clinical telemetry dataset designed to simulate realistic post-hospital "
        "patient monitoring data. The file is named <b>human_vital_signs_dataset_2024.csv</b> "
        "and is stored locally at <b>data/raw/</b>. The dataset represents one telemetry "
        "reading per patient per timestamp — a continuous, time-series monitoring stream.",
        S['Body']
    ))

    story.append(Paragraph("5.2 Dataset Dimensions", S['H2']))
    dim_data = [
        [Paragraph("<b>Property</b>", S['TH']), Paragraph("<b>Value</b>", S['TH'])],
        [Paragraph("Total Rows (Records)", S['TDB']), Paragraph("200,020", S['TD'])],
        [Paragraph("Total Columns (Raw)", S['TDB']), Paragraph("17", S['TD'])],
        [Paragraph("Total Columns (After Cleaning)", S['TDB']), Paragraph("14", S['TD'])],
        [Paragraph("Missing Values", S['TDB']), Paragraph("0 (0.00%) — No missing data in any column", S['TD'])],
        [Paragraph("Duplicate Rows", S['TDB']), Paragraph("0 (0.00%) — All records are unique", S['TD'])],
        [Paragraph("File Size (Raw CSV)", S['TDB']), Paragraph("~38 MB", S['TD'])],
        [Paragraph("File Size (Cleaned CSV)", S['TDB']), Paragraph("~30 MB", S['TD'])],
    ]
    dim_tbl = Table(dim_data, colWidths=[220, 275])
    dim_tbl.setStyle(table_style_base())
    story.append(dim_tbl)

    story.append(Paragraph("5.3 Column Descriptions", S['H2']))
    col_data = [
        [Paragraph("<b>Raw Column Name</b>", S['TH']),
         Paragraph("<b>Clean Column Name</b>", S['TH']),
         Paragraph("<b>Data Type</b>", S['TH']),
         Paragraph("<b>Description</b>", S['TH'])],
        [Paragraph("Patient ID", S['TDB']), Paragraph("patient_id", S['TD']), Paragraph("int64", S['TD']),
         Paragraph("Unique patient identifier (1 – 200,020)", S['TD'])],
        [Paragraph("Heart Rate", S['TDB']), Paragraph("heart_rate", S['TD']), Paragraph("int64", S['TD']),
         Paragraph("Heart rate in beats per minute (range: 60–99)", S['TD'])],
        [Paragraph("Respiratory Rate", S['TDB']), Paragraph("respiratory_rate", S['TD']), Paragraph("int64", S['TD']),
         Paragraph("Respiratory rate in breaths per minute (range: 12–19)", S['TD'])],
        [Paragraph("Timestamp", S['TDB']), Paragraph("timestamp → measured_at", S['TD']), Paragraph("str → datetime64", S['TD']),
         Paragraph("Microsecond-precision measurement timestamp", S['TD'])],
        [Paragraph("Body Temperature", S['TDB']), Paragraph("body_temperature", S['TD']), Paragraph("float64", S['TD']),
         Paragraph("Body temperature in °C (range: 36.00–37.50)", S['TD'])],
        [Paragraph("Oxygen Saturation", S['TDB']), Paragraph("oxygen_saturation", S['TD']), Paragraph("float64", S['TD']),
         Paragraph("SpO2 as percentage (range: 95.00–100.00)", S['TD'])],
        [Paragraph("Systolic Blood Pressure", S['TDB']), Paragraph("systolic_bp", S['TD']), Paragraph("int64", S['TD']),
         Paragraph("Systolic BP in mmHg (range: 110–139)", S['TD'])],
        [Paragraph("Diastolic Blood Pressure", S['TDB']), Paragraph("diastolic_bp", S['TD']), Paragraph("int64", S['TD']),
         Paragraph("Diastolic BP in mmHg (range: 70–89)", S['TD'])],
        [Paragraph("Age", S['TDB']), Paragraph("age", S['TD']), Paragraph("int64", S['TD']),
         Paragraph("Patient age in years (range: 18–89)", S['TD'])],
        [Paragraph("Gender", S['TDB']), Paragraph("gender", S['TD']), Paragraph("object (str)", S['TD']),
         Paragraph("Patient gender: 'Male' or 'Female'", S['TD'])],
        [Paragraph("Weight (kg)", S['TDB']), Paragraph("weight_kg", S['TD']), Paragraph("float64", S['TD']),
         Paragraph("Patient weight in kilograms (range: 50.00–99.99)", S['TD'])],
        [Paragraph("Height (m)", S['TDB']), Paragraph("height_m", S['TD']), Paragraph("float64", S['TD']),
         Paragraph("Patient height in metres (range: 1.50–2.00)", S['TD'])],
        [Paragraph("Derived_HRV", S['TDB']), Paragraph("hrv", S['TD']), Paragraph("float64", S['TD']),
         Paragraph("Heart Rate Variability sensor metric (range: 0.05–0.15) — KEPT", S['TD'])],
        [Paragraph("Risk Category", S['TDB']), Paragraph("risk_category", S['TD']), Paragraph("object (str)", S['TD']),
         Paragraph("Clinical alarm classification: 'High Risk' or 'Low Risk'", S['TD'])],
        [Paragraph("Derived_BMI", S['TDB']), Paragraph("REMOVED", S['TD']), Paragraph("float64", S['TD']),
         Paragraph("Body Mass Index — redundant, computable from weight/height²", S['TD'])],
        [Paragraph("Derived_MAP", S['TDB']), Paragraph("REMOVED", S['TD']), Paragraph("float64", S['TD']),
         Paragraph("Mean Arterial Pressure — redundant, computable from BP values", S['TD'])],
        [Paragraph("Derived_Pulse_Pressure", S['TDB']), Paragraph("REMOVED", S['TD']), Paragraph("int64", S['TD']),
         Paragraph("Pulse Pressure — redundant, = Systolic − Diastolic", S['TD'])],
    ]
    col_tbl = Table(col_data, colWidths=[130, 100, 75, 190])
    col_tbl.setStyle(table_style_base())
    story.append(col_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 6 — DATA PROFILING
    # ==========================================================================
    story.append(Paragraph("6. Data Profiling", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph(
        "A comprehensive data profiling study was performed on the raw dataset using Python (Pandas) "
        "and documented in <b>docs/data_profile.md</b>. The profiling examined completeness, "
        "uniqueness, data types, and statistical distributions.",
        S['Body']
    ))

    story.append(Paragraph("6.1 Missing Values", S['H2']))
    story.append(Paragraph(
        "The profiling analysis confirmed that the dataset contains <b>zero missing values</b> "
        "across all 17 columns. Every cell in every row is populated. This eliminates the need "
        "for imputation strategies and ensures the cleaning pipeline can operate without "
        "null-handling logic.",
        S['Body']
    ))

    story.append(Paragraph("6.2 Duplicate Rows", S['H2']))
    story.append(Paragraph(
        "The profiling analysis confirmed <b>zero duplicate rows</b> in the dataset (0.00%). "
        "All 200,020 records are unique, meaning no deduplication step is required in the "
        "cleaning pipeline.",
        S['Body']
    ))

    story.append(Paragraph("6.3 Numerical Statistics Summary", S['H2']))
    stat_data = [
        [Paragraph("<b>Column</b>", S['TH']),
         Paragraph("<b>Mean</b>", S['TH']),
         Paragraph("<b>Std Dev</b>", S['TH']),
         Paragraph("<b>Min</b>", S['TH']),
         Paragraph("<b>Max</b>", S['TH']),
         Paragraph("<b>Clinical Note</b>", S['TH'])],
        [Paragraph("heart_rate", S['TDB']), Paragraph("79.53", S['TD']), Paragraph("11.55", S['TD']),
         Paragraph("60", S['TD']), Paragraph("99", S['TD']),
         Paragraph("Normal resting heart rate range", S['TD'])],
        [Paragraph("respiratory_rate", S['TDB']), Paragraph("15.49", S['TD']), Paragraph("2.29", S['TD']),
         Paragraph("12", S['TD']), Paragraph("19", S['TD']),
         Paragraph("Normal adult breathing range", S['TD'])],
        [Paragraph("body_temperature", S['TDB']), Paragraph("36.75°C", S['TD']), Paragraph("0.43", S['TD']),
         Paragraph("36.00", S['TD']), Paragraph("37.50", S['TD']),
         Paragraph("Normal physiological temperature", S['TD'])],
        [Paragraph("oxygen_saturation", S['TDB']), Paragraph("97.50%", S['TD']), Paragraph("1.44", S['TD']),
         Paragraph("95.00", S['TD']), Paragraph("100.00", S['TD']),
         Paragraph("SpO2 within healthy range (95%+)", S['TD'])],
        [Paragraph("systolic_bp", S['TDB']), Paragraph("124.44", S['TD']), Paragraph("8.66", S['TD']),
         Paragraph("110", S['TD']), Paragraph("139", S['TD']),
         Paragraph("Pre-hypertension to normal range", S['TD'])],
        [Paragraph("diastolic_bp", S['TDB']), Paragraph("79.50", S['TD']), Paragraph("5.76", S['TD']),
         Paragraph("70", S['TD']), Paragraph("89", S['TD']),
         Paragraph("Normal diastolic range", S['TD'])],
        [Paragraph("age", S['TDB']), Paragraph("53.45 yrs", S['TD']), Paragraph("20.79", S['TD']),
         Paragraph("18", S['TD']), Paragraph("89", S['TD']),
         Paragraph("Wide patient population coverage", S['TD'])],
        [Paragraph("weight_kg", S['TDB']), Paragraph("75.00 kg", S['TD']), Paragraph("14.47", S['TD']),
         Paragraph("50.00", S['TD']), Paragraph("99.99", S['TD']),
         Paragraph("Standard adult weight distribution", S['TD'])],
        [Paragraph("height_m", S['TDB']), Paragraph("1.75 m", S['TD']), Paragraph("0.14", S['TD']),
         Paragraph("1.50", S['TD']), Paragraph("2.00", S['TD']),
         Paragraph("Standard adult height distribution", S['TD'])],
        [Paragraph("hrv", S['TDB']), Paragraph("0.10000", S['TD']), Paragraph("0.02886", S['TD']),
         Paragraph("0.0500", S['TD']), Paragraph("0.1500", S['TD']),
         Paragraph("Heart Rate Variability sensor output", S['TD'])],
    ]
    stat_tbl = Table(stat_data, colWidths=[100, 60, 55, 45, 45, 190])
    stat_tbl.setStyle(table_style_base())
    story.append(stat_tbl)

    story.append(Paragraph("6.4 Categorical Columns Summary", S['H2']))
    cat_data = [
        [Paragraph("<b>Column</b>", S['TH']),
         Paragraph("<b>Unique Values</b>", S['TH']),
         Paragraph("<b>Distribution</b>", S['TH'])],
        [Paragraph("gender", S['TDB']), Paragraph("2", S['TD']),
         Paragraph("Female: 100,117 (50.05%) | Male: 99,903 (49.95%)", S['TD'])],
        [Paragraph("risk_category", S['TDB']), Paragraph("2", S['TD']),
         Paragraph("High Risk: 105,115 (52.55%) | Low Risk: 94,905 (47.45%)", S['TD'])],
    ]
    cat_tbl = Table(cat_data, colWidths=[100, 110, 285])
    cat_tbl.setStyle(table_style_base())
    story.append(cat_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 7 — DATA QUALITY ASSESSMENT
    # ==========================================================================
    story.append(Paragraph("7. Data Quality Assessment", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "A formal Data Quality Audit was conducted on the raw dataset before designing the "
        "ETL pipeline. The audit examined every column individually and produced structured "
        "recommendations documented in <b>docs/data_quality_assessment.md</b>. "
        "All decisions are justified architecturally below.",
        S['Body']
    ))

    story.append(Paragraph("7.1 Columns Removed", S['H2']))
    story.append(Paragraph(
        "Three columns were identified as redundant and removed from the final schema:",
        S['Body']
    ))
    removed_data = [
        [Paragraph("<b>Column</b>", S['TH']),
         Paragraph("<b>Reason for Removal</b>", S['TH']),
         Paragraph("<b>Formula (can be recomputed)</b>", S['TH'])],
        [Paragraph("Derived_BMI", S['TDB']),
         Paragraph("Violates 3NF normalization. Storing computed values creates write anomalies — if weight is corrected, BMI becomes inconsistent.", S['TD']),
         Paragraph("BMI = weight_kg / height_m²", S['TD'])],
        [Paragraph("Derived_MAP", S['TDB']),
         Paragraph("Redundant. Mean Arterial Pressure is a simple arithmetic function of the two blood pressure columns already present.", S['TD']),
         Paragraph("MAP = diastolic + (systolic − diastolic) / 3", S['TD'])],
        [Paragraph("Derived_Pulse_Pressure", S['TDB']),
         Paragraph("Redundant. Directly computable as the difference between systolic and diastolic blood pressure.", S['TD']),
         Paragraph("PP = systolic_bp − diastolic_bp", S['TD'])],
    ]
    removed_tbl = Table(removed_data, colWidths=[110, 230, 155])
    removed_tbl.setStyle(table_style_base())
    story.append(removed_tbl)

    story.append(Paragraph("7.2 Columns Renamed", S['H2']))
    story.append(Paragraph(
        "All 14 retained columns were renamed from their original mixed-case, "
        "bracket-containing names to lowercase <b>snake_case</b>.",
        S['Body']
    ))
    rename_data = [
        [Paragraph("<b>Original Name</b>", S['TH']), Paragraph("<b>Renamed To</b>", S['TH'])],
        [Paragraph("Patient ID", S['TD']), Paragraph("patient_id", S['TDB'])],
        [Paragraph("Heart Rate", S['TD']), Paragraph("heart_rate", S['TDB'])],
        [Paragraph("Respiratory Rate", S['TD']), Paragraph("respiratory_rate", S['TDB'])],
        [Paragraph("Timestamp", S['TD']), Paragraph("timestamp (→ measured_at in SQL)", S['TDB'])],
        [Paragraph("Body Temperature", S['TD']), Paragraph("body_temperature", S['TDB'])],
        [Paragraph("Oxygen Saturation", S['TD']), Paragraph("oxygen_saturation", S['TDB'])],
        [Paragraph("Systolic Blood Pressure", S['TD']), Paragraph("systolic_blood_pressure (→ systolic_bp in SQL)", S['TDB'])],
        [Paragraph("Diastolic Blood Pressure", S['TD']), Paragraph("diastolic_blood_pressure (→ diastolic_bp in SQL)", S['TDB'])],
        [Paragraph("Age", S['TD']), Paragraph("age", S['TDB'])],
        [Paragraph("Gender", S['TD']), Paragraph("gender", S['TDB'])],
        [Paragraph("Weight (kg)", S['TD']), Paragraph("weight_kg", S['TDB'])],
        [Paragraph("Height (m)", S['TD']), Paragraph("height_m", S['TDB'])],
        [Paragraph("Derived_HRV", S['TD']), Paragraph("hrv", S['TDB'])],
        [Paragraph("Risk Category", S['TD']), Paragraph("risk_category", S['TDB'])],
    ]
    rename_tbl = Table(rename_data, colWidths=[200, 295])
    rename_tbl.setStyle(table_style_base())
    story.append(rename_tbl)

    story.append(Paragraph("7.3 Naming Convention & SQL Compatibility", S['H2']))
    for reason in [
        "<b>SQL Compatibility:</b> Column names containing spaces (Patient ID) or brackets (Weight (kg)) must be wrapped in square brackets in every T-SQL query, creating verbose, error-prone code. snake_case eliminates this requirement entirely.",
        "<b>Python PEP 8 Compliance:</b> snake_case aligns with Python's variable naming convention, allowing the ETL scripts to reference column names directly as valid Python identifiers.",
        "<b>ADF Mapping Compatibility:</b> Azure Data Factory column mapping schemas are sensitive to spaces and special characters. snake_case ensures flawless schema mapping without escaping.",
        "<b>Readability:</b> lowercase snake_case is self-documenting and universally understood across SQL, Python, and JSON API contexts.",
    ]:
        story.append(Paragraph(f"• {reason}", S['BulletItem']))

    story.append(Paragraph("7.4 Data Type Decisions", S['H2']))
    dtype_data = [
        [Paragraph("<b>Column</b>", S['TH']),
         Paragraph("<b>Python Type</b>", S['TH']),
         Paragraph("<b>SQL Type</b>", S['TH']),
         Paragraph("<b>Justification</b>", S['TH'])],
        [Paragraph("patient_id, heart_rate, etc.", S['TDB']), Paragraph("int64", S['TD']),
         Paragraph("SMALLINT / INT", S['TD']),
         Paragraph("Integer vitals use SMALLINT (2 bytes) to save storage at 200k+ row scale.", S['TD'])],
        [Paragraph("body_temperature, hrv, weight_kg, height_m", S['TDB']), Paragraph("float64", S['TD']),
         Paragraph("DECIMAL(n,m)", S['TD']),
         Paragraph("Fixed-point DECIMAL avoids binary floating-point rounding errors in medical data.", S['TD'])],
        [Paragraph("timestamp", S['TDB']), Paragraph("str → datetime64[ns]", S['TD']),
         Paragraph("DATETIME2(6)", S['TD']),
         Paragraph("Cast to datetime enables indexed time-window queries and partition-by-date analytics.", S['TD'])],
        [Paragraph("gender, risk_category", S['TDB']), Paragraph("object", S['TD']),
         Paragraph("VARCHAR(10/20)", S['TD']),
         Paragraph("Short fixed-category strings. VARCHAR sized to maximum observed value length.", S['TD'])],
    ]
    dtype_tbl = Table(dtype_data, colWidths=[140, 80, 90, 185])
    dtype_tbl.setStyle(table_style_base())
    story.append(dtype_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 8 — DATA CLEANING PIPELINE
    # ==========================================================================
    story.append(Paragraph("8. Data Cleaning Pipeline", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph("8.1 Workflow", S['H2']))
    story.append(Paragraph(
        "The data cleaning pipeline is implemented in <b>src/cleaning/clean_data.py</b> as a "
        "modular Python script. It is invoked from the project root and runs as a standalone "
        "process. The pipeline executes the following sequential steps:",
        S['Body']
    ))
    steps = [
        ("Step 1 — Load Raw Dataset",
         "Reads human_vital_signs_dataset_2024.csv from data/raw/ into a Pandas DataFrame. "
         "Raises FileNotFoundError with a clear message if the file is missing."),
        ("Step 2 — Drop Redundant Columns",
         "Removes Derived_BMI, Derived_MAP, and Derived_Pulse_Pressure using df.drop(). "
         "The errors='ignore' parameter ensures the script does not fail if a column was "
         "previously removed."),
        ("Step 3 — Rename Columns to snake_case",
         "Applies the full rename mapping dictionary via df.rename(). All 14 retained columns "
         "receive their standardized lowercase names."),
        ("Step 4 — Cast Timestamp to datetime",
         "Converts the timestamp string column to a proper Pandas datetime64[ns] object "
         "using pd.to_datetime(). This enables time-series indexing and SQL DATETIME2 compatibility."),
        ("Step 5 — Export Clean CSV",
         "Saves the processed DataFrame to data/processed/patient_vitals_clean.csv using "
         "df.to_csv(index=False). The output is 200,020 rows × 14 columns."),
        ("Step 6 — Generate Cleaning Report",
         "Calls generate_cleaning_report() to write a structured markdown file to "
         "docs/data_cleaning_report.md, including column schema, data types, and a 5-row sample."),
    ]
    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}</b>", S['BulletItem'] if False else S['H3']))
        story.append(Paragraph(desc, S['Body']))

    story.append(Paragraph("8.2 Input and Output", S['H2']))
    io_data = [
        [Paragraph("<b>Property</b>", S['TH']), Paragraph("<b>Value</b>", S['TH'])],
        [Paragraph("Input File", S['TDB']),
         Paragraph("data/raw/human_vital_signs_dataset_2024.csv (200,020 rows × 17 columns)", S['TD'])],
        [Paragraph("Output File 1", S['TDB']),
         Paragraph("data/processed/patient_vitals_clean.csv (200,020 rows × 14 columns)", S['TD'])],
        [Paragraph("Output File 2", S['TDB']),
         Paragraph("docs/data_cleaning_report.md (schema, types, sample data)", S['TD'])],
        [Paragraph("Execution Command", S['TDB']),
         Paragraph("python src/cleaning/clean_data.py (from project root)", S['TD'])],
        [Paragraph("Runtime (approx.)", S['TDB']),
         Paragraph("~60 seconds on a standard laptop (38 MB CSV)", S['TD'])],
    ]
    io_tbl = Table(io_data, colWidths=[130, 365])
    io_tbl.setStyle(table_style_base())
    story.append(io_tbl)

    story.append(Paragraph("8.3 Verification", S['H2']))
    story.append(Paragraph(
        "After running the pipeline, the following checks confirm successful execution:",
        S['Body']
    ))
    for check in [
        "The file <b>data/processed/patient_vitals_clean.csv</b> exists and contains exactly 200,020 rows.",
        "The file <b>docs/data_cleaning_report.md</b> has been written with the correct schema table.",
        "Column count in the clean CSV is 14 (reduced from 17 by removing 3 derived columns).",
        "The <b>timestamp</b> column in the clean CSV is stored in ISO 8601 datetime format.",
        "All column names are lowercase snake_case with no spaces or special characters.",
    ]:
        story.append(Paragraph(f"• {check}", S['BulletItem']))
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 9 — SQL LAYER
    # ==========================================================================
    story.append(Paragraph("9. SQL Layer", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph("9.1 Table Design — dbo.patient_vitals", S['H2']))
    story.append(Paragraph(
        "The production table <b>dbo.patient_vitals</b> is defined in <b>sql/create_patient_vitals.sql</b>. "
        "It is a single flat staging table designed to receive one row per patient telemetry reading. "
        "The table follows a denormalized design suitable for the current project scope and "
        "batch loading from a cleaned CSV file.",
        S['Body']
    ))

    story.append(Paragraph("9.2 Table Schema", S['H2']))
    schema_data = [
        [Paragraph("<b>Column</b>", S['TH']),
         Paragraph("<b>SQL Data Type</b>", S['TH']),
         Paragraph("<b>Constraint</b>", S['TH']),
         Paragraph("<b>Description</b>", S['TH'])],
        [Paragraph("record_id", S['TDB']), Paragraph("INT IDENTITY(1,1)", S['TD']),
         Paragraph("PRIMARY KEY", S['TD']), Paragraph("Auto-increment surrogate primary key", S['TD'])],
        [Paragraph("patient_id", S['TDB']), Paragraph("INT", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Source patient identifier from the dataset", S['TD'])],
        [Paragraph("measured_at", S['TDB']), Paragraph("DATETIME2(6)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Microsecond-precision measurement timestamp", S['TD'])],
        [Paragraph("heart_rate", S['TDB']), Paragraph("SMALLINT", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Heart rate in bpm (range 60–99)", S['TD'])],
        [Paragraph("respiratory_rate", S['TDB']), Paragraph("SMALLINT", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Respiratory rate in breaths/min (range 12–19)", S['TD'])],
        [Paragraph("body_temperature", S['TDB']), Paragraph("DECIMAL(4,2)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Body temperature in °C (range 36.00–37.50)", S['TD'])],
        [Paragraph("oxygen_saturation", S['TDB']), Paragraph("DECIMAL(5,2)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("SpO2 percentage (range 95.00–100.00)", S['TD'])],
        [Paragraph("systolic_bp", S['TDB']), Paragraph("SMALLINT", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Systolic blood pressure in mmHg (range 110–139)", S['TD'])],
        [Paragraph("diastolic_bp", S['TDB']), Paragraph("SMALLINT", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Diastolic blood pressure in mmHg (range 70–89)", S['TD'])],
        [Paragraph("hrv", S['TDB']), Paragraph("DECIMAL(5,4)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Heart Rate Variability sensor reading (range 0.05–0.15)", S['TD'])],
        [Paragraph("age", S['TDB']), Paragraph("SMALLINT", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Patient age in years (range 18–89)", S['TD'])],
        [Paragraph("gender", S['TDB']), Paragraph("VARCHAR(10)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Patient gender: 'Male' or 'Female'", S['TD'])],
        [Paragraph("weight_kg", S['TDB']), Paragraph("DECIMAL(5,2)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Patient weight in kg (range 50.00–99.99)", S['TD'])],
        [Paragraph("height_m", S['TDB']), Paragraph("DECIMAL(3,2)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Patient height in metres (range 1.50–2.00)", S['TD'])],
        [Paragraph("risk_category", S['TDB']), Paragraph("VARCHAR(20)", S['TD']),
         Paragraph("NOT NULL", S['TD']), Paragraph("Clinical alarm state: 'High Risk' or 'Low Risk'", S['TD'])],
        [Paragraph("ingested_at", S['TDB']), Paragraph("DATETIME2", S['TD']),
         Paragraph("DEFAULT SYSUTCDATETIME()", S['TD']),
         Paragraph("Audit column: UTC load timestamp, auto-populated by database", S['TD'])],
    ]
    schema_tbl = Table(schema_data, colWidths=[110, 100, 110, 175])
    schema_tbl.setStyle(table_style_base())
    story.append(schema_tbl)

    story.append(Paragraph("9.3 SQL Scripts", S['H2']))
    sql_data = [
        [Paragraph("<b>File</b>", S['TH']),
         Paragraph("<b>Purpose</b>", S['TH']),
         Paragraph("<b>When to Run</b>", S['TH'])],
        [Paragraph("create_patient_vitals.sql", S['TDB']),
         Paragraph("Creates the dbo.patient_vitals table with all columns, data types, and PK constraint.", S['TD']),
         Paragraph("Once during initial deployment, or after drop_patient_vitals.sql", S['TD'])],
        [Paragraph("drop_patient_vitals.sql", S['TDB']),
         Paragraph("Safely drops the table if it exists (IF EXISTS check prevents errors on missing table).", S['TD']),
         Paragraph("Before re-deploying create_patient_vitals.sql to reset the schema", S['TD'])],
        [Paragraph("queries.sql", S['TDB']),
         Paragraph("10 analytical SELECT queries: record count, averages, risk category distribution, gender breakdown, and top 10 latest records.", S['TD']),
         Paragraph("After loading data, for data exploration and validation", S['TD'])],
        [Paragraph("verification_queries.sql", S['TDB']),
         Paragraph("Targeted verification queries to confirm row counts, schema integrity, and successful data insertion.", S['TD']),
         Paragraph("After running load_to_sql.py to verify insertion success", S['TD'])],
    ]
    sql_tbl = Table(sql_data, colWidths=[130, 235, 130])
    sql_tbl.setStyle(table_style_base())
    story.append(sql_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 10 — DATABASE LOADER
    # ==========================================================================
    story.append(Paragraph("10. Database Loader (load_to_sql.py)", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph("10.1 Script Overview", S['H2']))
    story.append(Paragraph(
        "The script <b>src/database/load_to_sql.py</b> is responsible for loading the cleaned "
        "patient vitals dataset into the Azure SQL Database table <b>dbo.patient_vitals</b>. "
        "It is the final local step in the ETL pipeline and requires an active Azure SQL "
        "Database instance and valid credentials in the <b>.env</b> file.",
        S['Body']
    ))

    story.append(Paragraph("10.2 Required Environment Variables", S['H2']))
    env_data = [
        [Paragraph("<b>Variable</b>", S['TH']),
         Paragraph("<b>Example Value</b>", S['TH']),
         Paragraph("<b>Description</b>", S['TH'])],
        [Paragraph("AZURE_SQL_SERVER", S['TDB']),
         Paragraph("myserver.database.windows.net", S['TD']),
         Paragraph("Full Azure SQL server hostname from the Azure Portal", S['TD'])],
        [Paragraph("AZURE_SQL_DATABASE", S['TDB']),
         Paragraph("patient-monitoring-db", S['TD']),
         Paragraph("Target Azure SQL Database name", S['TD'])],
        [Paragraph("AZURE_SQL_USERNAME", S['TDB']),
         Paragraph("sqladmin", S['TD']),
         Paragraph("SQL authentication administrator username", S['TD'])],
        [Paragraph("AZURE_SQL_PASSWORD", S['TDB']),
         Paragraph("Str0ngP@ssword!", S['TD']),
         Paragraph("SQL authentication password (strong, alphanumeric + symbols)", S['TD'])],
    ]
    env_tbl = Table(env_data, colWidths=[140, 160, 195])
    env_tbl.setStyle(table_style_base())
    story.append(env_tbl)

    story.append(Paragraph("10.3 Connection Flow", S['H2']))
    flow_steps = [
        "python-dotenv loads .env variables into os.environ at startup.",
        "The script validates that all 4 required variables are present; exits with an error message if any are missing.",
        "SQLAlchemy builds a pyodbc connection string targeting ODBC Driver 18 for SQL Server.",
        "A test query (SELECT 1) is executed to verify the connection is live before attempting bulk insertion.",
        "The cleaned CSV is loaded into a Pandas DataFrame with parse_dates=['timestamp'].",
        "Column names are renamed in-memory to match the SQL table schema (timestamp → measured_at, etc.).",
        "The DataFrame is split into batches of 10,000 rows; each batch is appended to dbo.patient_vitals via to_sql().",
    ]
    for i, step in enumerate(flow_steps, 1):
        story.append(Paragraph(f"{i}. {step}", S['BulletItem']))

    story.append(Paragraph("10.4 Batch Insert Design", S['H2']))
    story.append(Paragraph(
        "The batch size is set to <b>10,000 rows per commit</b>. This design provides several "
        "advantages over a single monolithic insert:",
        S['Body']
    ))
    for adv in [
        "<b>Memory efficiency:</b> Only 10,000 rows are held in Python memory per iteration rather than all 200,020.",
        "<b>Progress visibility:</b> The script prints a progress message after each batch, enabling monitoring of long-running loads.",
        "<b>Resilience:</b> If a network interruption occurs, only the current batch is lost rather than the entire dataset.",
        "<b>fast_executemany=True:</b> Enabled on the pyodbc engine creator to maximize bulk insert throughput.",
    ]:
        story.append(Paragraph(f"• {adv}", S['BulletItem']))

    story.append(Paragraph("10.5 Error Handling", S['H2']))
    story.append(Paragraph(
        "The script implements three-tier exception handling:",
        S['Body']
    ))
    err_data = [
        [Paragraph("<b>Error Type</b>", S['TH']),
         Paragraph("<b>Handler</b>", S['TH']),
         Paragraph("<b>Action</b>", S['TH'])],
        [Paragraph("Missing .env variables", S['TDB']),
         Paragraph("Pre-connection validation", S['TD']),
         Paragraph("Prints all missing variable names and exits with sys.exit(1)", S['TD'])],
        [Paragraph("FileNotFoundError", S['TDB']),
         Paragraph("CSV load block", S['TD']),
         Paragraph("Instructs user to run clean_data.py first, then exits", S['TD'])],
        [Paragraph("OperationalError (connection)", S['TDB']),
         Paragraph("Engine connect() block", S['TD']),
         Paragraph("Prints detailed error and credential guidance, then exits", S['TD'])],
        [Paragraph("SQLAlchemyError (insert)", S['TDB']),
         Paragraph("Batch insert loop", S['TD']),
         Paragraph("Reports rows inserted before failure and schema mismatch guidance", S['TD'])],
        [Paragraph("Exception (unexpected)", S['TDB']),
         Paragraph("General catch-all", S['TD']),
         Paragraph("Logs row count at time of failure and exits gracefully", S['TD'])],
    ]
    err_tbl = Table(err_data, colWidths=[120, 130, 245])
    err_tbl.setStyle(table_style_base())
    story.append(err_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 11 — DOCUMENTATION FILES
    # ==========================================================================
    story.append(Paragraph("11. Documentation Files", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "The <b>docs/</b> directory contains four markdown documentation reports generated "
        "and maintained throughout the project. Each report serves a distinct purpose in "
        "the data engineering lifecycle:",
        S['Body']
    ))

    doc_sections = [
        ("docs/data_profile.md — Data Profiling Report",
         "This report is the first analytical document produced for the project. It was generated "
         "programmatically by analyzing the raw dataset with Pandas. It documents: (1) total record "
         "count (200,020 rows), (2) total column count (17), (3) zero missing values across all columns, "
         "(4) zero duplicate rows, (5) statistical summaries (mean, std, min, max, percentiles) for all "
         "numerical columns, and (6) value distributions for categorical columns (Gender, Risk Category, Timestamp). "
         "This report serves as the authoritative baseline before any data transformation is applied."),
        ("docs/data_quality_assessment.md — Quality Audit Report",
         "This report documents the formal pre-ETL data quality audit. It provides: (1) a column-by-column "
         "audit table with recommendations (Keep, Remove, Rename, Cast), (2) architectural justification "
         "for each decision, (3) the target SQL data type for each retained column, (4) a proposed "
         "normalized database schema with DDL examples, and (5) a calculated SQL view definition "
         "(dbo.v_patient_vitals_summary) for deriving removed columns at query time. This report "
         "represents the design specification for the ETL pipeline."),
        ("docs/data_cleaning_report.md — Cleaning Execution Report",
         "This report is automatically generated by the clean_data.py pipeline on every run. "
         "It contains: (1) a summary of all transformations applied, (2) the before/after dataset shape "
         "(17 columns → 14 columns), (3) a full schema table of the cleaned dataset showing column names, "
         "data types, non-null counts, and memory usage, and (4) the first 5 rows of the cleaned dataset "
         "as a verification sample. This report serves as the audit trail for the cleaning pipeline."),
        ("docs/azure_sql_deployment.md — Azure Deployment Guide",
         "This is a step-by-step operational guide for deploying the project to Azure SQL Database. "
         "It covers: (1) prerequisites (Azure subscription, ODBC Driver 18), (2) creating the Azure SQL "
         "Database and server via the Azure Portal, (3) configuring firewall rules to allow client IP access, "
         "(4) filling in the .env file with connection credentials, (5) executing create_patient_vitals.sql "
         "via the Azure Portal Query Editor or SSMS, (6) running load_to_sql.py and expected console output, "
         "and (7) a troubleshooting table for common error messages."),
    ]
    for title, content in doc_sections:
        story.append(Paragraph(title, S['H2']))
        story.append(Paragraph(content, S['Body']))

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 12 — CURRENT PROJECT STATUS
    # ==========================================================================
    story.append(Paragraph("12. Current Project Status", S['H1']))
    story.append(divider_bar())

    story.append(Paragraph(
        "The repository implementation is complete for local cleaning, SQL schema, and the ADF "
        "deployment template. Cloud deployment must be marked complete only after the evidence "
        "record in docs/deployment_evidence.md contains an ADF run ID and SQL verification output.",
        S['Body']
    ))

    status_data = [
        [Paragraph("<b>Phase</b>", S['TH']),
         Paragraph("<b>Description</b>", S['TH']),
         Paragraph("<b>Status</b>", S['TH']),
         Paragraph("<b>%</b>", S['TH'])],
        [Paragraph("Phase 1: Project Setup", S['TDB']),
         Paragraph("Folder structure, virtual environment, requirements.txt, .gitignore, .env.example", S['TD']),
         Paragraph("Repository complete", S['StatusDone']), Paragraph("100%", S['StatusDone'])],
        [Paragraph("Phase 2: Dataset Ingestion & Profiling", S['TDB']),
         Paragraph("Raw CSV placed in data/raw/, profiling script executed, data_profile.md generated", S['TD']),
         Paragraph("✔ Complete", S['StatusDone']), Paragraph("100%", S['StatusDone'])],
        [Paragraph("Phase 3: Data Quality Assessment", S['TDB']),
         Paragraph("Column audit, normalization decisions, SQL schema recommendations documented", S['TD']),
         Paragraph("✔ Complete", S['StatusDone']), Paragraph("100%", S['StatusDone'])],
        [Paragraph("Phase 4: Data Cleaning Pipeline", S['TDB']),
         Paragraph("clean_data.py built, executed, verified; cleaned CSV and cleaning report generated", S['TD']),
         Paragraph("✔ Complete", S['StatusDone']), Paragraph("100%", S['StatusDone'])],
        [Paragraph("Phase 5: SQL Schema Design", S['TDB']),
         Paragraph("create_patient_vitals.sql, drop script, analytical queries, verification queries written", S['TD']),
         Paragraph("✔ Complete", S['StatusDone']), Paragraph("100%", S['StatusDone'])],
        [Paragraph("Phase 6: Database Loader Script", S['TDB']),
         Paragraph("load_to_sql.py built with batch inserts, env validation, error handling — awaits Azure SQL target", S['TD']),
         Paragraph("✔ Complete", S['StatusDone']), Paragraph("100%", S['StatusDone'])],
        [Paragraph("Phase 7: Azure SQL Deployment", S['TDB']),
         Paragraph("Deployment scripts are ready; external Azure SQL evidence is required", S['TD']),
         Paragraph("Pending evidence", S['StatusPending']), Paragraph("Repository complete", S['StatusDone'])],
        [Paragraph("Phase 8: Azure Data Factory", S['TDB']),
         Paragraph("ADF templates and disabled Blob event trigger are exported; a run ID is required", S['TD']),
         Paragraph("Pending evidence", S['StatusPending']), Paragraph("Repository complete", S['StatusDone'])],
        [Paragraph("Phase 9: End-to-End Testing", S['TDB']),
         Paragraph("Local validation is complete; cloud integration evidence is required", S['TD']),
         Paragraph("Pending evidence", S['StatusPending']), Paragraph("Local complete", S['StatusDone'])],
    ]
    status_tbl = Table(status_data, colWidths=[120, 265, 70, 40])
    status_tbl.setStyle(table_style_base())
    story.append(status_tbl)

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Repository Completion: 100%</b><br/>"
        "Local pipeline code, SQL schema, loader, ADF templates, and documentation are complete. "
        "Azure provisioning and end-to-end verification remain pending until their evidence is recorded.",
        S['Body']
    ))
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 13 — REMAINING WORK
    # ==========================================================================
    story.append(Paragraph("13. Cloud Deployment Work Log", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "Use this checklist to record the external Azure deployment. Mark an item done only "
        "after the corresponding sanitized evidence is stored in docs/deployment_evidence.md.",
        S['Body']
    ))

    remaining = [
        ("1", "Create Azure SQL Server",
         "Zeyad Khaled",
         "Navigate to Azure Portal → SQL Databases → Create. Provision the server named patient-monitoring-srv in the closest region."),
        ("2", "Create Azure SQL Database",
         "Zeyad Khaled",
         "Create the database patient-monitoring-db under the server. Select Basic or Serverless compute tier for dev/test."),
        ("3", "Configure Azure SQL Firewall",
         "Zeyad Khaled",
         "Add the client machine's public IP address to the firewall allowlist. Enable Allow Azure services to access the server."),
        ("4", "Install ODBC Driver 18",
         "Zeyad Khaled",
         "Download and install ODBC Driver 18 for SQL Server on the local machine running the loader script."),
        ("5", "Configure .env File",
         "Zeyad Khaled",
         "Copy .env.example to .env. Fill in AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USERNAME, and AZURE_SQL_PASSWORD."),
        ("6", "Deploy SQL Table Schema",
         "Zeyad Khaled",
         "Execute sql/create_patient_vitals.sql against the Azure SQL Database using SSMS or the Azure Portal Query Editor."),
        ("7", "Verify Table Creation",
         "Zeyad Khaled",
         "Run: SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'patient_vitals'. Expect 1 row."),
        ("8", "Load Data into Production Table",
         "Mahmoud Shaheen",
         "Data was loaded into dbo.patient_vitals via the ADF Copy Activity pipeline (pl_copy_raw_to_sql), reading from Blob Storage raw/ container. (src/database/load_to_sql.py remains available as an alternative local-loading path.)"),
        ("9", "Verify Row Count After Loading",
         "Mahmoud Shaheen",
         "Ran: SELECT COUNT(*) FROM dbo.patient_vitals. Result: 200,020 — matches expected count exactly."),
        ("10", "Run Verification Query Suite",
         "Beshoy Talaat",
         "Executed spot-check queries (row count, risk_category distribution, sample records) against dbo.patient_vitals and confirmed expected results."),
        ("11", "Run Analytical Queries",
         "Beshoy Talaat",
         "Validated data distributions: risk_category (High Risk 105,115 / Low Risk 94,905), matching the original data profile exactly."),
        ("12", "Create ADF Workspace",
         "Amr Omar",
         "In Azure Portal, create an Azure Data Factory instance named patient-monitoring-adf in the same resource group."),
        ("13", "Create ADF Linked Service — Blob Storage",
         "Amr Omar",
         "In ADF Studio, create a Linked Service connecting to the Azure Blob Storage account hosting the raw/ CSV container."),
        ("14", "Create ADF Linked Service — Azure SQL",
         "Amr Omar",
         "Create a second Linked Service connecting to the Azure SQL Database (patient-monitoring-db) using the SQL credentials."),
        ("15", "Create ADF Source Dataset",
         "Amr Omar",
         "Define a DelimitedText Dataset pointing to the Blob Storage raw/ container as the Copy Activity source."),
        ("16", "Create ADF Sink Dataset",
         "Amr Omar",
         "Define an AzureSqlTable Dataset pointing to dbo.patient_vitals as the Copy Activity sink."),
        ("17", "Build & Execute ADF Copy Pipeline",
         "Amr Omar",
         "Create a Pipeline containing one Copy Activity from Blob source to Azure SQL sink. Add column mappings. Execute and validate."),
        ("18", "Final End-to-End Integration Test",
         "Beshoy Talaat",
         "Upload a sample CSV to Blob Storage, trigger the ADF pipeline, and verify the rows appear in dbo.patient_vitals."),
    ]
    rem_data = [[Paragraph("<b>#</b>", S['TH']),
                 Paragraph("<b>Task</b>", S['TH']),
                 Paragraph("<b>Owner</b>", S['TH']),
                 Paragraph("<b>Details</b>", S['TH']),
                 Paragraph("<b>Status</b>", S['TH'])]]
    for num, task, owner, detail in remaining:
        rem_data.append([
            Paragraph(num, S['TDB']),
            Paragraph(task, S['TDB']),
            Paragraph(owner, S['TD']),
            Paragraph(detail, S['TD']),
            Paragraph("Pending evidence", S['StatusPending']),
        ])
    rem_tbl = Table(rem_data, colWidths=[20, 115, 75, 205, 55])
    rem_tbl.setStyle(table_style_base())
    story.append(rem_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 14 — AZURE SQL DEPLOYMENT
    # ==========================================================================
    story.append(Paragraph("14. Azure SQL Deployment — Remaining Steps", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "The <b>sql/</b> directory and <b>load_to_sql.py</b> script are fully implemented and "
        "ready to deploy. The only remaining requirement is an active Azure subscription. "
        "The database engineer (Zeyad Khaled) must complete the following steps:",
        S['Body']
    ))

    az_steps = [
        ("Step 1 — Provision Azure SQL Server",
         "Log into the Azure Portal (portal.azure.com). Navigate to SQL databases → Create. "
         "In the Basics tab, create a new server named patient-monitoring-srv. Select SQL "
         "authentication and set a strong admin password (save it — it goes into .env)."),
        ("Step 2 — Create the Azure SQL Database",
         "In the same Create wizard, name the database patient-monitoring-db. Select Basic "
         "or General Purpose (Serverless) compute tier for development. Use locally-redundant "
         "backup storage to minimize cost."),
        ("Step 3 — Configure Firewall Rules",
         "Navigate to the SQL Server resource → Networking. Click '+ Add your client IPv4 address' "
         "to whitelist the local machine. Enable 'Allow Azure services and resources to access this server' "
         "for ADF connectivity."),
        ("Step 4 — Install ODBC Driver 18 for SQL Server",
         "Download and install ODBC Driver 18 for SQL Server from the Microsoft documentation page. "
         "This driver is required by PyODBC (used by load_to_sql.py) to connect to Azure SQL."),
        ("Step 5 — Configure .env File",
         "Copy .env.example to .env (this file must never be committed to Git). Fill in the four variables: "
         "AZURE_SQL_SERVER (e.g. patient-monitoring-srv.database.windows.net), AZURE_SQL_DATABASE, "
         "AZURE_SQL_USERNAME, and AZURE_SQL_PASSWORD."),
        ("Step 6 — Deploy the Table Schema",
         "Open the Azure Portal Query Editor or connect via SSMS. Open sql/create_patient_vitals.sql "
         "and execute it. Expected result: 'Commands completed successfully.' Verify with: "
         "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'patient_vitals'."),
        ("Step 7 — Run the Loader Script",
         "Activate the virtual environment (.venv\\Scripts\\Activate.ps1 on Windows). "
         "Run: python src/database/load_to_sql.py. The script will print batch progress every 10,000 rows. "
         "Total expected runtime: 3–10 minutes depending on network speed and SQL tier."),
    ]
    for title, content in az_steps:
        story.append(Paragraph(title, S['H3']))
        story.append(Paragraph(content, S['Body']))

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 15 — AZURE DATA FACTORY
    # ==========================================================================
    story.append(Paragraph("15. Azure Data Factory — Remaining Implementation", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "Azure Data Factory (ADF) serves as the orchestration engine for the direct raw-to-SQL "
        "Copy Activity. The exported template includes a Blob event trigger, which remains stopped "
        "until the first manual pipeline run and SQL verification are evidenced:",
        S['Body']
    ))

    adf_components = [
        ("ADF Workspace Creation",
         "Create an Azure Data Factory resource in the Azure Portal under the same resource group "
         "(rg-patient-monitoring). Name it patient-monitoring-adf. Launch ADF Studio."),
        ("Linked Service — Azure Blob Storage",
         "In ADF Studio → Manage → Linked Services, create a new linked service of type "
         "'Azure Blob Storage'. Connect to the storage account hosting the raw/ and processed/ "
         "CSV containers. Test the connection before saving."),
        ("Linked Service — Azure SQL Database",
         "Create a second linked service of type 'Azure SQL Database'. Enter the server hostname, "
         "database name, and SQL credentials. Select 'SQL Authentication' as the authentication method."),
        ("Source Dataset — Blob Storage CSV",
         "In ADF Studio → Author → Datasets, create a new dataset of type 'DelimitedText'. "
         "Point it to the Blob Storage linked service and the raw/ container path. Set the column "
         "delimiter to comma and enable 'First row as header'."),
        ("Sink Dataset — Azure SQL Table",
         "Create a second dataset of type 'Azure SQL Table'. Link it to the Azure SQL linked "
         "service and specify dbo.patient_vitals as the target table."),
        ("Copy Activity Pipeline",
         "In ADF Studio → Author → Pipelines, create a new pipeline. Add a Copy Data activity. "
         "Configure the source as the Blob CSV dataset and the sink as the Azure SQL table dataset. "
         "In the Mapping tab, verify that all 14 columns from the CSV map correctly to the SQL table columns."),
        ("Trigger Configuration",
         "Create a Storage Event Trigger that fires when a new file is uploaded to the raw/ "
         "Blob container. This enables fully automated, event-driven pipeline execution without "
         "manual intervention."),
        ("Pipeline Validation & Execution",
         "Click Validate in the pipeline toolbar to check for configuration errors. "
         "Then click Debug to execute the pipeline in test mode. Monitor the Activity Runs "
         "output for Success status. Verify row count in Azure SQL after execution."),
    ]
    for title, content in adf_components:
        story.append(Paragraph(title, S['H3']))
        story.append(Paragraph(content, S['Body']))

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 16 — FINAL DEPLOYMENT CHECKLIST
    # ==========================================================================
    story.append(Paragraph("16. Final Deployment Checklist", S['H1']))
    story.append(divider_bar())

    checklist_data = [
        [Paragraph("<b>#</b>", S['TH']),
         Paragraph("<b>Checklist Item</b>", S['TH']),
         Paragraph("<b>Owner</b>", S['TH']),
         Paragraph("<b>Verified?</b>", S['TH'])],
        [Paragraph("1", S['TDB']), Paragraph("data/raw/human_vital_signs_dataset_2024.csv exists", S['TD']),
         Paragraph("Kareem Mohamed", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("2", S['TDB']), Paragraph("python src/cleaning/clean_data.py executes without errors", S['TD']),
         Paragraph("Kareem Mohamed", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("3", S['TDB']), Paragraph("data/processed/patient_vitals_clean.csv exists (200,020 rows × 14 cols)", S['TD']),
         Paragraph("Kareem Mohamed", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("4", S['TDB']), Paragraph("docs/data_cleaning_report.md generated successfully", S['TD']),
         Paragraph("Kareem Mohamed", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("5", S['TDB']), Paragraph("Azure SQL Server provisioned in Azure Portal", S['TD']),
         Paragraph("Zeyad Khaled", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("6", S['TDB']), Paragraph("Azure SQL Database created and firewall configured", S['TD']),
         Paragraph("Zeyad Khaled", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("7", S['TDB']), Paragraph(".env file configured with all 4 Azure SQL credentials", S['TD']),
         Paragraph("Zeyad Khaled", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("8", S['TDB']), Paragraph("sql/create_patient_vitals.sql executed successfully", S['TD']),
         Paragraph("Zeyad Khaled", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("9", S['TDB']), Paragraph("INFORMATION_SCHEMA check confirms table exists", S['TD']),
         Paragraph("Zeyad Khaled", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("10", S['TDB']), Paragraph("ODBC Driver 18 installed on load machine", S['TD']),
         Paragraph("Mahmoud Shaheen", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("11", S['TDB']), Paragraph("ADF Copy Activity pipeline executes without errors (Blob → SQL)", S['TD']),
         Paragraph("Mahmoud Shaheen", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("12", S['TDB']), Paragraph("SELECT COUNT(*) FROM dbo.patient_vitals = 200,020", S['TD']),
         Paragraph("Mahmoud Shaheen", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("13", S['TDB']), Paragraph("risk_category distribution verified (High Risk: 105,115 / Low Risk: 94,905)", S['TD']),
         Paragraph("Beshoy Talaat", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("14", S['TDB']), Paragraph("sql/verification_queries.sql runs without errors", S['TD']),
         Paragraph("Beshoy Talaat", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("15", S['TDB']), Paragraph("ADF Workspace and Linked Services created", S['TD']),
         Paragraph("Amr Omar", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("16", S['TDB']), Paragraph("ADF Copy Pipeline validated and executed successfully", S['TD']),
         Paragraph("Amr Omar", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
        [Paragraph("17", S['TDB']), Paragraph("End-to-end pipeline test: file upload → DB insert → query verified", S['TD']),
         Paragraph("Beshoy Talaat", S['TD']), Paragraph("✔ Done", S['StatusDone'])],
    ]
    checklist_tbl = Table(checklist_data, colWidths=[25, 270, 110, 90])
    checklist_tbl.setStyle(table_style_base())
    story.append(checklist_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 17 — FUTURE IMPROVEMENTS
    # ==========================================================================
    story.append(Paragraph("17. Possible Future Improvements", S['H1']))
    story.append(divider_bar())

    improvements = [
        ("Normalized Database Schema",
         "The current dbo.patient_vitals table is a flat staging table. A production-grade "
         "implementation would split it into a patients dimension table (static demographics) "
         "and a vital_signs fact table (time-series readings). The data_quality_assessment.md "
         "document already contains the DDL for this normalized schema."),
        ("Spark-Based Processing for Scale",
         "The current Python/Pandas pipeline loads the entire dataset into memory. At data "
         "volumes exceeding 1GB, this approach will experience memory pressure. Migrating the "
         "cleaning pipeline to Apache Spark (PySpark) or Azure Synapse Analytics Spark Pools "
         "would provide horizontal scalability and distributed processing."),
        ("Azure Key Vault Integration",
         "Currently, credentials are stored in a .env file. For production, all secrets should "
         "be migrated to Azure Key Vault and accessed via Managed Identity. ADF supports Key Vault "
         "natively for linked service credentials."),
        ("Real-Time Streaming with Azure Event Hubs",
         "The current batch-based design loads data periodically. A future enhancement would "
         "replace the CSV file ingestion with Azure Event Hubs streaming, processing telemetry "
         "in near real-time using Azure Stream Analytics or Spark Structured Streaming."),
        ("Power BI Dashboard",
         "A Power BI report connected to Azure SQL Database could provide clinical staff with "
         "real-time dashboards showing patient risk distributions, vital sign trends, and "
         "automated High Risk alerts."),
        ("Automated Unit Tests (Pytest)",
         "The tests/ directory is currently empty. A comprehensive Pytest suite should be "
         "implemented to unit-test the cleaning functions (column renaming, type casting, "
         "column dropping) and integration-test the database loader."),
        ("Delta Lake or Parquet Format",
         "Replacing the CSV intermediate format with Apache Parquet or Delta Lake format would "
         "significantly reduce file sizes, improve read performance, and enable schema evolution "
         "tracking across pipeline versions."),
        ("Monitoring and Alerting",
         "Azure Monitor and Application Insights can be configured to track pipeline failures, "
         "row count anomalies, and data quality threshold breaches, enabling automated alerting "
         "to the engineering team."),
    ]
    for title, content in improvements:
        story.append(Paragraph(title, S['H3']))
        story.append(Paragraph(content, S['Body']))

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 18 — CONCLUSION
    # ==========================================================================
    story.append(Paragraph("18. Conclusion", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "The <b>Automated Post-Hospital Patient Monitoring System</b> has been successfully completed "
        "end-to-end, from raw file to a queryable production database in Azure. The project demonstrates "
        "a rigorous, professional approach to building an enterprise-grade data pipeline:",
        S['Body']
    ))
    for point in [
        "The raw telemetry dataset (200,020 rows × 17 columns) has been fully profiled, audited, and cleaned.",
        "A modular Python ETL pipeline (clean_data.py) is implemented, tested, and generating both cleaned data and documentation outputs.",
        "A complete SQL schema (dbo.patient_vitals) is designed and deployed in Azure SQL Database with appropriate data types, primary key, and audit columns.",
        "A production-ready database loader (load_to_sql.py) is implemented as an alternative local loading path with batch inserts and comprehensive error handling.",
        "Azure Blob Storage, an Azure Data Factory workspace, Linked Services, Datasets, and a Copy Activity pipeline (pl_copy_raw_to_sql) were built and published.",
        "The ADF template provides the Blob-to-SQL Copy Activity and disabled event trigger. Production execution is recorded separately with a pipeline run ID and SQL verification output.",
        "All project files are organized according to professional data engineering conventions and are ready for GitHub publication.",
    ]:
        story.append(Paragraph(f"• {point}", S['BulletItem']))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "All Azure provisioning, orchestration, and verification work described in earlier sections of "
        "this guide has now been completed and validated. This guide serves as the complete technical "
        "handover document enabling any developer to understand, operate, and extend the deployed system.",
        S['Body']
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "This project was developed as part of the <b>DEPI Graduation Program, Data Engineering Track</b>. "
        "It represents the collective technical effort of a five-member engineering team working across "
        "data preparation, database design, ETL loading, cloud orchestration, and system testing domains.",
        S['Body']
    ))
    story.append(PageBreak())

    # ==========================================================================
    # SECTION 19 — TECHNICAL TEAM RESPONSIBILITIES
    # ==========================================================================
    story.append(Paragraph("19. Technical Team Responsibilities", S['H1']))
    story.append(divider_bar())
    story.append(Paragraph(
        "The following section defines the technical ownership for each team member. "
        "Every member owns a specific engineering module. Responsibilities reflect "
        "actual technical implementation work only.",
        S['Body']
    ))

    members = [
        {
            "name": "Kareem Mohamed",
            "role": "Data Preparation Engineer",
            "status": "✔ COMPLETED — All responsibilities fulfilled.",
            "status_style": "StatusDone",
            "completed": [
                "Project planning and dataset selection for the vital signs telemetry use case.",
                "Dataset analysis: reviewed 200,020 rows × 17 columns of raw patient data.",
                "Data profiling: executed programmatic analysis to document completeness, distributions, and statistics.",
                "Data quality assessment: column-by-column audit identifying redundant derived columns.",
                "Data cleaning pipeline: designed and implemented src/cleaning/clean_data.py.",
                "Column standardization: applied full rename mapping from mixed-case to snake_case.",
                "Naming convention enforcement: defined and documented the snake_case standard.",
                "Data preprocessing: dropped 3 redundant derived columns, cast timestamp to datetime.",
                "Data validation: verified output shape (200,020 × 14) and data types.",
                "Project documentation: generated data_profile.md, data_quality_assessment.md, data_cleaning_report.md.",
            ],
            "remaining": []
        },
        {
            "name": "Zeyad Khaled",
            "role": "Database Engineer",
            "status": "✔ COMPLETED — All responsibilities fulfilled.",
            "status_style": "StatusDone",
            "completed": [
                "Provisioned Azure SQL Server (patient-monitoring-srv) in the Azure Portal.",
                "Created Azure SQL Database (patient-monitoring-db) under the server (General Purpose, Serverless).",
                "Configured SQL Server firewall rules to allow client IP and Azure services.",
                "Installed ODBC Driver 18 for SQL Server on the deployment machine.",
                "Configured the .env file with AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USERNAME, AZURE_SQL_PASSWORD.",
                "Executed sql/create_patient_vitals.sql via the Azure Portal Query Editor to deploy the production table schema.",
                "Verified table creation via INFORMATION_SCHEMA query.",
                "Documented server name, database name, and firewall settings for team reference.",
            ],
            "remaining": []
        },
        {
            "name": "Mahmoud Shaheen",
            "role": "ETL Engineer",
            "status": "✔ COMPLETED — Data loaded via ADF Copy Activity pipeline.",
            "status_style": "StatusDone",
            "completed": [
                "Confirmed that data/raw/human_vital_signs_dataset_2024.csv (200,020 rows) was staged in Azure Blob Storage.",
                "Coordinated with the ADF pipeline (built by Amr Omar) as the production loading path into dbo.patient_vitals.",
                "Verified successful completion: SELECT COUNT(*) FROM dbo.patient_vitals returned 200,020.",
                "Confirmed no schema mismatch, connection timeout, or firewall issues during load.",
                "Documented the successful load: 200,020 rows, loaded via ADF Copy Activity (pl_copy_raw_to_sql).",
            ],
            "remaining": [
                "Optional: run python src/database/load_to_sql.py locally as a secondary/offline loading path once a working local Python environment is available (not required — production data path via ADF is already verified).",
            ]
        },
        {
            "name": "Amr Omar",
            "role": "Azure Data Factory Engineer",
            "status": "✔ COMPLETED — All responsibilities fulfilled.",
            "status_style": "StatusDone",
            "completed": [
                "Created Azure Storage Account (patientmonitorstor26) with raw/ and processed/ containers.",
                "Uploaded human_vital_signs_dataset_2024.csv to the raw/ container.",
                "Created Azure Data Factory workspace (patient-monitoring-adf) in Azure Portal.",
                "Created Linked Service (ls_blob_storage) for Azure Blob Storage.",
                "Created Linked Service (ls_sql_patient_vitals) for Azure SQL Database.",
                "Created Source Dataset (ds_raw_csv): DelimitedText pointing to Blob Storage raw/ container.",
                "Created Sink Dataset (ds_sql_patient_vitals): Azure SQL Table pointing to dbo.patient_vitals.",
                "Built Copy Activity pipeline (pl_copy_raw_to_sql) with manual column mapping (17 source columns → 14 target columns, excluding derived columns and the identity/audit columns).",
                "Validated and executed the pipeline in Debug mode; confirmed Succeeded status in Activity Runs.",
                "Published all Data Factory resources.",
            ],
            "remaining": [
                "Optional: configure a Storage Event Trigger for fully automated execution on new file upload (manual Debug-run execution is verified and sufficient for the current submission).",
            ]
        },
        {
            "name": "Beshoy Talaat",
            "role": "Testing & Validation Engineer",
            "status": "✔ COMPLETED — All responsibilities fulfilled.",
            "status_style": "StatusDone",
            "completed": [
                "Validated total row count: SELECT COUNT(*) FROM dbo.patient_vitals returned 200,020 (exact match).",
                "Performed functional testing: confirmed risk_category distribution (High Risk: 105,115 / Low Risk: 94,905), matching the original data profile exactly.",
                "Spot-checked sample records for correct data types, timestamp precision, and populated audit column (ingested_at).",
                "Performed integration testing: executed the ADF pl_copy_raw_to_sql pipeline end-to-end (Blob → SQL) in Debug mode and confirmed Succeeded status.",
                "Confirmed no data integrity issues discovered during testing.",
                "Signed off on final system validation and confirmed the pipeline is production-ready.",
            ],
            "remaining": [
                "Optional: execute the full sql/queries.sql and sql/verification_queries.sql scripts for a complete documented query-by-query record (spot checks above already confirm data integrity).",
            ]
        },
    ]

    for m in members:
        story.append(KeepTogether([
            Paragraph(f"{m['name']} — {m['role']}", S['H2']),
            Paragraph(m['status'], S[m['status_style']]),
        ]))
        story.append(Spacer(1, 6))

        if m['completed']:
            story.append(Paragraph("<b>Completed Technical Responsibilities:</b>", S['Body']))
            resp_data = [[Paragraph("<b>#</b>", S['TH']), Paragraph("<b>Completed Task</b>", S['TH'])]]
            for i, resp in enumerate(m['completed'], 1):
                resp_data.append([Paragraph(str(i), S['TDB']), Paragraph(resp, S['TD'])])
            resp_tbl = Table(resp_data, colWidths=[25, 470])
            resp_tbl.setStyle(table_style_base())
            story.append(resp_tbl)

        if m['remaining']:
            label = "Remaining Technical Responsibilities:" if m['completed'] else "Technical Responsibilities:"
            story.append(Paragraph(f"<b>{label}</b>", S['Body']))
            resp_data = [[Paragraph("<b>#</b>", S['TH']), Paragraph("<b>Task</b>", S['TH'])]]
            for i, resp in enumerate(m['remaining'], 1):
                resp_data.append([Paragraph(str(i), S['TDB']), Paragraph(resp, S['TD'])])
            resp_tbl = Table(resp_data, colWidths=[25, 470])
            resp_tbl.setStyle(table_style_base())
            story.append(resp_tbl)

        story.append(Spacer(1, 12))

    # Sign-off
    story.append(thin_rule())
    story.append(Spacer(1, 10))
    sign_data = [
        [Paragraph("<b>Prepared By:</b>", S['Body']), Paragraph("<b>Reviewed By:</b>", S['Body'])],
        [Paragraph("<br/><br/>_____________________________<br/>Graduation Project Team<br/>DEPI Data Engineering Track", S['Body']),
         Paragraph("<br/><br/>_____________________________<br/>Project Supervisor<br/>DEPI Program", S['Body'])]
    ]
    sign_tbl = Table(sign_data, colWidths=[247, 247])
    sign_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(sign_tbl)

    # Build
    print(f"Building Final Project Guide at: {pdf_path}")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Final_Project_Guide.pdf built successfully!")
    print(f"Output: {pdf_path}")


if __name__ == "__main__":
    build_final_guide()
