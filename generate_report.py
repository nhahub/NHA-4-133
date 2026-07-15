import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    A canvas that enables running headers, footers, and page numbers.
    It performs a two-pass render to accurately determine the total page count.
    """
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
        # Page 1 is the cover page; do not draw headers/footers
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D")) # Deep Navy

        # Running Header
        self.drawString(54, 750, "AUTOMATED PATIENT MONITORING SYSTEM")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568")) # Slate Gray
        self.drawRightString(558, 750, "Graduation Project Progress Report - Phase I & II")
        
        # Header Rule
        self.setStrokeColor(colors.HexColor("#CBD5E1")) # Light Gray
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)

        # Footer Rule
        self.line(54, 55, 558, 55)

        # Running Footer
        self.drawString(54, 40, "Confidential - Academic Submission Only")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)

        self.restoreState()

def build_pdf_report():
    pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Project_Progress_Report.pdf"))
    
    # Page setup: Letter size is 612 x 792. 
    # Margins: Left/Right = 54 pt (0.75 in), Top/Bottom = 72 pt (1 in)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    # Styling setup
    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#1A365D")   # Deep Navy
    secondary_color = colors.HexColor("#2B6CB0") # Slate Blue
    text_color = colors.HexColor("#2D3748")      # Charcoal Body Text
    light_bg = colors.HexColor("#F7FAFC")        # Off-white

    styles.add(ParagraphStyle(
        name='CoverTop',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=secondary_color,
        alignment=1, # Center
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#4A5568"),
        alignment=1, # Center
        spaceAfter=30
    ))

    styles.add(ParagraphStyle(
        name='MetadataLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=primary_color
    ))

    styles.add(ParagraphStyle(
        name='MetadataVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color
    ))

    # Academic Document Styles
    styles['Normal'].textColor = text_color
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    styles['Normal'].fontName = 'Helvetica'

    styles.add(ParagraphStyle(
        name='AcademicH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='AcademicH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='BulletItem',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=0
    ))

    styles.add(ParagraphStyle(
        name='TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=text_color,
        alignment=0
    ))

    styles.add(ParagraphStyle(
        name='TableBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=primary_color,
        alignment=0
    ))

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("GRADUATION PROJECT PROGRESS REPORT", styles['CoverTop']))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Automated Post-Hospital Patient<br/>Monitoring System", styles['CoverTitle']))
    story.append(Paragraph("A Scalable, Cloud-Enabled Data Engineering Ingestion & Quality Pipeline", styles['CoverSubtitle']))
    story.append(Spacer(1, 100))

    # Divider bar
    divider = Table([[""]], colWidths=[504], rowHeights=[4])
    divider.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary_color),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(divider)
    story.append(Spacer(1, 60))

    # Metadata Grid
    meta_data = [
        [Paragraph("Course:", styles['MetadataLabel']), Paragraph("DEPI Graduation Project", styles['MetadataVal']),
         Paragraph("Prepared By:", styles['MetadataLabel']), Paragraph("Graduation Project Team", styles['MetadataVal'])],
        [Paragraph("Project Domain:", styles['MetadataLabel']), Paragraph("Data Engineering", styles['MetadataVal']),
         Paragraph("Submitted To:", styles['MetadataLabel']), Paragraph("University Project Supervisor", styles['MetadataVal'])],
        [Paragraph("Submission Date:", styles['MetadataLabel']), Paragraph("June 30, 2026", styles['MetadataVal']),
         Paragraph("Department:", styles['MetadataLabel']), Paragraph("Computer & Data Engineering", styles['MetadataVal'])],
    ]
    meta_table = Table(meta_data, colWidths=[90, 162, 90, 162])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & INTRODUCTION
    # =========================================================================
    story.append(Paragraph("Table of Contents", styles['AcademicH1']))
    story.append(Spacer(1, 5))

    toc_data = [
        [Paragraph("<b>Section</b>", styles['MetadataLabel']), Paragraph("<b>Page</b>", styles['MetadataLabel'])],
        [Paragraph("1. Project Overview & Context", styles['Normal']), Paragraph("2", styles['Normal'])],
        [Paragraph("2. Problem Statement & Project Objectives", styles['Normal']), Paragraph("2", styles['Normal'])],
        [Paragraph("3. Technology Stack & Architecture", styles['Normal']), Paragraph("3", styles['Normal'])],
        [Paragraph("4. Dataset Description & Profiling", styles['Normal']), Paragraph("3", styles['Normal'])],
        [Paragraph("5. Data Quality Assessment (Audit)", styles['Normal']), Paragraph("4", styles['Normal'])],
        [Paragraph("6. Data Cleaning & Transformation Pipeline", styles['Normal']), Paragraph("4", styles['Normal'])],
        [Paragraph("7. Implemented Code & Reports Registry", styles['Normal']), Paragraph("5", styles['Normal'])],
        [Paragraph("8. Project Status, Completion Percentage & Justification", styles['Normal']), Paragraph("5", styles['Normal'])],
        [Paragraph("9. Risks, Limitations & Next Development Phase", styles['Normal']), Paragraph("6", styles['Normal'])],
        [Paragraph("10. Conclusion", styles['Normal']), Paragraph("6", styles['Normal'])],
    ]
    toc_table = Table(toc_data, colWidths=[454, 50])
    toc_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("1. Project Overview & Context", styles['AcademicH1']))
    story.append(Paragraph(
        "The \"Automated Post-Hospital Patient Monitoring System\" is a dedicated Data Engineering graduation project "
        "designed to build a robust, scalable, and automated telemetry ingestion and processing platform. As patients are "
        "discharged from medical centers, their continuous vital signs are collected via clinical monitoring devices. "
        "This project establishes a data pipeline that ingests this high-frequency vital signs stream, subjects it to data quality "
        "assurance processes, and loads it into a high-performance database. The primary target is to enable real-time dashboarding, "
        "alert triggering, and historical analysis. Importantly, this project focusing strictly on infrastructure, "
        "orchestration, and database design, and is completely free of Machine Learning components.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Why this project was chosen:", styles['AcademicH2']))
    story.append(Paragraph(
        "Post-hospitalization patient monitoring represents an ideal intersection between vital healthcare telemetry and "
        "cloud data architecture. By designing and building this pipeline, we demonstrate capability in managing complex "
        "data ingestion lifecycles (ingestion, staging, validation, transformations, and load layers) while ensuring "
        "data privacy, security, and strict data quality gates. In a live setting, such pipelines provide immediate, "
        "actionable insight to doctors, drastically reducing patient readmission rates.",
        styles['Normal']
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: PROBLEM STATEMENT, OBJECTIVES & TECH STACK
    # =========================================================================
    story.append(Paragraph("2. Problem Statement & Project Objectives", styles['AcademicH1']))
    story.append(Paragraph(
        "<b>Problem Statement:</b> Once a patient leaves the medical facility, continuous care is interrupted. Early clinical deterioration "
        "is frequently missed due to sporadic or unstandardized telemetry collection. To construct a reliable monitoring "
        "dashboard, clinical analysts require a high-fidelity, clean database of vitals. However, raw IoT vital logs "
        "suffer from bad data shapes, unit mismatches, out-of-sync timestamps, and redundant mathematical indicators. "
        "Without an automated pipeline that applies rigorous data quality gates and standardized naming conventions, clinical "
        "alert systems cannot operate effectively.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Project Objectives:</b>", styles['Normal']))
    story.append(Paragraph("&bull; Build a professional, modular folder structure suitable for automated pipeline deployments.", styles['BulletItem']))
    story.append(Paragraph("&bull; Set up a standardized virtual environment to isolate library dependencies.", styles['BulletItem']))
    story.append(Paragraph("&bull; Perform a thorough, code-driven profiling study of the raw clinical vital signs dataset.", styles['BulletItem']))
    story.append(Paragraph("&bull; Perform a data quality assessment to define the target relational production schema.", styles['BulletItem']))
    story.append(Paragraph("&bull; Create a reusable, automated Python data cleaning pipeline to structure and parse inputs.", styles['BulletItem']))
    story.append(Paragraph("&bull; Deploy Azure resources (ADF, Blob Storage, SQL Database) to schedule and run the pipeline (Planned).", styles['BulletItem']))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Technology Stack & Rationale", styles['AcademicH1']))
    
    tech_data = [
        [Paragraph("<b>Component</b>", styles['TableHead']), Paragraph("<b>Technology</b>", styles['TableHead']), Paragraph("<b>Rationale & Selection Justification</b>", styles['TableHead'])],
        [Paragraph("<b>Processing Core</b>", styles['TableBodyBold']), Paragraph("Python 3.12 (Pandas)", styles['TableBody']), Paragraph("Industry-standard for data parsing and cleaning. Pandas provides high-performance column manipulations.", styles['TableBody'])],
        [Paragraph("<b>Storage / Database</b>", styles['TableBodyBold']), Paragraph("Azure SQL Database", styles['TableBody']), Paragraph("Enterprise-grade relational storage with native connection pooling, clustering index supports, and security integration.", styles['TableBody'])],
        [Paragraph("<b>Orchestration</b>", styles['TableBodyBold']), Paragraph("Azure Data Factory (ADF)", styles['TableBody']), Paragraph("Cloud scheduling and workflow coordination. Triggers python cleaning scripts and SQL loading tasks.", styles['TableBody'])],
        [Paragraph("<b>Staging Area</b>", styles['TableBodyBold']), Paragraph("Azure Blob Storage", styles['TableBody']), Paragraph("Cost-effective object storage to host the landing raw CSV logs and clean intermediate files.", styles['TableBody'])],
        [Paragraph("<b>Dev & Control</b>", styles['TableBodyBold']), Paragraph("VS Code / Git", styles['TableBody']), Paragraph("Standardized IDE environment and secure version control utilizing environment configurations.", styles['TableBody'])],
    ]
    tech_table = Table(tech_data, colWidths=[100, 130, 274])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tech_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ARCHITECTURE & DATASET DESCRIPTION
    # =========================================================================
    story.append(Paragraph("4. Current System Architecture", styles['AcademicH1']))
    story.append(Paragraph(
        "The system pipeline follows an ingestion, cleaning, staging, and relational loading architecture. Below is the workflow diagram:",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))

    # Text-based architecture layout
    arch_data = [
        [Paragraph("<b>Phase</b>", styles['TableHead']), Paragraph("<b>Source / System</b>", styles['TableHead']), Paragraph("<b>Operations / Tasks</b>", styles['TableHead'])],
        [Paragraph("1. Raw Ingestion", styles['TableBodyBold']), Paragraph("Azure Blob (Raw Container)", styles['TableBody']), Paragraph("Incoming telemetry CSV files land in the cloud storage bucket.", styles['TableBody'])],
        [Paragraph("2. Cleaning & Staging", styles['TableBodyBold']), Paragraph("Python script in ADF / VM", styles['TableBody']), Paragraph("Executes data cleaning, drops derived columns, renames to snake_case, and exports clean CSV.", styles['TableBody'])],
        [Paragraph("3. Relational Load", styles['TableBodyBold']), Paragraph("Azure SQL Database (patient_vitals)", styles['TableBody']), Paragraph("Loads processed records into database. Enabled dynamic query views for dashboarding (Planned).", styles['TableBody'])],
    ]
    arch_table = Table(arch_data, colWidths=[110, 160, 234])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("5. Dataset Description & Profiling", styles['AcademicH1']))
    story.append(Paragraph(
        "<b>Dataset Profile (Raw):</b> The dataset `human_vital_signs_dataset_2024.csv` was analyzed programmatically. It contains "
        "exactly <b>200,020 rows</b> and <b>17 columns</b>. Profiling verified that the raw dataset has <b>0% missing values</b> "
        "across all columns and contains <b>0 duplicate rows</b>.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Key statistics extracted from numerical features during profiling:", styles['Normal']))

    stat_data = [
        [Paragraph("<b>Feature Column</b>", styles['TableHead']), Paragraph("<b>Mean Value</b>", styles['TableHead']), Paragraph("<b>Min</b>", styles['TableHead']), Paragraph("<b>Max</b>", styles['TableHead']), Paragraph("<b>Clinical Interpretation</b>", styles['TableHead'])],
        [Paragraph("Heart Rate", styles['TableBodyBold']), Paragraph("79.53 bpm", styles['TableBody']), Paragraph("60", styles['TableBody']), Paragraph("99", styles['TableBody']), Paragraph("Ranges between standard resting limits.", styles['TableBody'])],
        [Paragraph("Oxygen Saturation", styles['TableBodyBold']), Paragraph("97.50%", styles['TableBody']), Paragraph("95.0%", styles['TableBody']), Paragraph("100.0%", styles['TableBody']), Paragraph("Normal physiological range (95%+).", styles['TableBody'])],
        [Paragraph("Systolic BP", styles['TableBodyBold']), Paragraph("124.44 mmHg", styles['TableBody']), Paragraph("110", styles['TableBody']), Paragraph("139", styles['TableBody']), Paragraph("Pre-hypertension to standard blood pressure.", styles['TableBody'])],
        [Paragraph("Diastolic BP", styles['TableBodyBold']), Paragraph("79.50 mmHg", styles['TableBody']), Paragraph("70", styles['TableBody']), Paragraph("89", styles['TableBody']), Paragraph("Normal diastolic range.", styles['TableBody'])],
        [Paragraph("Age", styles['TableBodyBold']), Paragraph("53.45 years", styles['TableBody']), Paragraph("18", styles['TableBody']), Paragraph("89", styles['TableBody']), Paragraph("Broad patient population coverage.", styles['TableBody'])],
        [Paragraph("Weight", styles['TableBodyBold']), Paragraph("75.00 kg", styles['TableBody']), Paragraph("50.0", styles['TableBody']), Paragraph("100.0", styles['TableBody']), Paragraph("Standard weight profile.", styles['TableBody'])],
        [Paragraph("Height", styles['TableBodyBold']), Paragraph("1.75 meters", styles['TableBody']), Paragraph("1.5", styles['TableBody']), Paragraph("2.0", styles['TableBody']), Paragraph("Standard height profile.", styles['TableBody'])],
    ]
    stat_table = Table(stat_data, colWidths=[100, 74, 40, 40, 250])
    stat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(stat_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: QUALITY ASSESSMENT & CLEANING
    # =========================================================================
    story.append(Paragraph("6. Data Quality Assessment (Audit Recommendations)", styles['AcademicH1']))
    story.append(Paragraph(
        "A formal data quality audit was conducted on the raw data columns. The audit highlighted major structural "
        "redundancies in the derived metrics. The recommendations approved by the supervisor are as follows:",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))

    audit_data = [
        [Paragraph("<b>Raw Column</b>", styles['TableHead']), Paragraph("<b>Status / Action</b>", styles['TableHead']), Paragraph("<b>Architectural Justification</b>", styles['TableHead'])],
        [Paragraph("Patient ID", styles['TableBodyBold']), Paragraph("Keep & Rename", styles['TableBody']), Paragraph("Remains as primary identifier. Set as Primary Key (PK).", styles['TableBody'])],
        [Paragraph("Timestamp", styles['TableBodyBold']), Paragraph("Keep, Parse & Cast", styles['TableBody']), Paragraph("Must be converted from string/text type to proper Datetime object for timeseries query partitions.", styles['TableBody'])],
        [Paragraph("Derived_BMI", styles['TableBodyBold']), Paragraph("Remove", styles['TableBody']), Paragraph("Redundant. Directly computed via $Weight / Height^2$. Storing calculated columns in relational tables violates 3NF normalization rules and leads to database anomalies.", styles['TableBody'])],
        [Paragraph("Derived_MAP", styles['TableBodyBold']), Paragraph("Remove", styles['TableBody']), Paragraph("Redundant. Calculated mathematically from Systolic and Diastolic Blood Pressures.", styles['TableBody'])],
        [Paragraph("Derived_Pulse_Pressure", styles['TableBodyBold']), Paragraph("Remove", styles['TableBody']), Paragraph("Redundant. Calculated dynamically as $Systolic - Diastolic$.", styles['TableBody'])],
        [Paragraph("Derived_HRV", styles['TableBodyBold']), Paragraph("Keep & Rename (hrv)", styles['TableBody']), Paragraph("Heart Rate Variability is a complex sensor measurement, not easily reverse-engineered. Renamed to simple snake_case.", styles['TableBody'])],
        [Paragraph("Risk Category", styles['TableBodyBold']), Paragraph("Keep & Rename (risk_category)", styles['TableBody']), Paragraph("Retained in order to compare model/alarm classifications later.", styles['TableBody'])],
    ]
    audit_table = Table(audit_data, colWidths=[120, 110, 274])
    audit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(audit_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("7. Data Cleaning & Transformation Pipeline", styles['AcademicH1']))
    story.append(Paragraph(
        "A modular, automated Python cleaning script was built under `src/cleaning/clean_data.py` to automate these changes. "
        "Upon loading the raw CSV data into memory, the script performs the following sequential actions:",
        styles['Normal']
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("1. <b>Drop derived features:</b> Dropped the columns `Derived_BMI`, `Derived_MAP`, and `Derived_Pulse_Pressure`.", styles['BulletItem']))
    story.append(Paragraph("2. <b>Apply Naming Conventions:</b> Re-mapped and renamed remaining mixed-case and bracketed columns into lowercase `snake_case` (e.g. `Patient ID` $\\rightarrow$ `patient_id`, `Weight (kg)` $\\rightarrow$ `weight_kg`).", styles['BulletItem']))
    story.append(Paragraph("3. <b>Convert Timestamps:</b> Converted the string `Timestamp` column to proper Python/Pandas `datetime64[ns]` type.", styles['BulletItem']))
    story.append(Paragraph("4. <b>Export Clean Output:</b> Saved the resulting database-ready data matrix (containing 200,020 rows and 14 columns) to `data/processed/patient_vitals_clean.csv`.", styles['BulletItem']))
    story.append(Paragraph("5. <b>Write Report:</b> Generated a data cleaning execution summary logged directly to `docs/data_cleaning_report.md`.", styles['BulletItem']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ARTIFACTS REGISTRY & PROJECT STATUS
    # =========================================================================
    story.append(Paragraph("8. Implemented Code & Reports Registry", styles['AcademicH1']))
    story.append(Paragraph(
        "The table below details every workspace file and report successfully created, along with its function and contribution:",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))

    reg_data = [
        [Paragraph("<b>Workspace File / Path</b>", styles['TableHead']), Paragraph("<b>Type</b>", styles['TableHead']), Paragraph("<b>Purpose & Contribution to Pipeline</b>", styles['TableHead'])],
        [Paragraph("`src/cleaning/clean_data.py`", styles['TableBodyBold']), Paragraph("Python Module", styles['TableBody']), Paragraph("Consists of `clean_dataset()` and `generate_cleaning_report()` which automates parsing, drops columns, renames to snake_case, and exports output.", styles['TableBody'])],
        [Paragraph("`docs/data_profile.md`", styles['TableBodyBold']), Paragraph("Markdown Doc", styles['TableBody']), Paragraph("Formulates the initial data profile. Provides records counts, missing value analysis, duplicates, and key statistics.", styles['TableBody'])],
        [Paragraph("`docs/data_quality_assessment.md`", styles['TableBodyBold']), Paragraph("Markdown Doc", styles['TableBody']), Paragraph("Pre-ETL quality audit outlining normalisation suggestions, calculated views, and Azure SQL schema recommendations.", styles['TableBody'])],
        [Paragraph("`docs/data_cleaning_report.md`", styles['TableBodyBold']), Paragraph("Markdown Doc", styles['TableBody']), Paragraph("Summary report verifying column counts, memory footprint, and data types before/after the cleaning runs.", styles['TableBody'])],
        [Paragraph("`data/processed/patient_vitals_clean.csv`", styles['TableBodyBold']), Paragraph("Dataset File", styles['TableBody']), Paragraph("Final cleaned data output, structured in snake_case and ready for database insertion.", styles['TableBody'])],
    ]
    reg_table = Table(reg_data, colWidths=[160, 80, 264])
    reg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(reg_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("9. Project Status, Completion Percentage & Justification", styles['AcademicH1']))
    story.append(Paragraph(
        "<b>Current Completion Percentage:</b> <b>35%</b>",
        styles['Normal']
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Justification:</b>", styles['Normal']))
    story.append(Paragraph("&bull; <b>Phase 1: Project Setup (100% completed):</b> Root folders, virtual environment, .gitignore, .env.example, and libraries are complete.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Phase 2: Ingestion & Data Profile (100% completed):</b> Raw files moved, profiling script executed, and stats verified.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Phase 3: Data Quality & Audit (100% completed):</b> Comprehensive schema assessment and data audit completed.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Phase 4: Data Cleaning Pipeline (100% completed):</b> Automated Python module implemented, run, and verified.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Phase 5: Azure Cloud Deployment & Storage (Planned - 0% completed):</b> Azure Blob Storage, ADF triggers, connection strings.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Phase 6: Relational Database & SQL (Planned - 0% completed):</b> SQL DDL schema deployment, index tuning, and calculated views.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Phase 7: End-to-End Orchestration & Testing (Planned - 0% completed):</b> Automating pipeline runs under ADF schedule.", styles['BulletItem']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: RISKS, FUTURE WORK & CONCLUSION
    # =========================================================================
    story.append(Paragraph("10. Risks, Limitations & Next Development Phase", styles['AcademicH1']))
    story.append(Paragraph(
        "<b>Risks and Limitations:</b>",
        styles['Normal']
    ))
    story.append(Paragraph("&bull; <b>Data Volume Scaling:</b> The cleaning pipeline currently runs locally using Pandas which loads the dataset entirely into memory. While sufficient for 200k rows (38MB), it will experience performance degradation if patient telemetry grows into gigabytes. Transitioning to PySpark or Azure Synapse Spark pools will be required for high-volume settings.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Connection and Security:</b> Moving variables to Azure will require Key Vault configurations. Hardcoding connection keys must be strictly prohibited, which we have mitigated using the `.env.example` configurations.", styles['BulletItem']))
    story.append(Paragraph("&bull; <b>Timestamp Precision:</b> Telemetry uses microsecond logging. If database indexes are not properly configured, time-window aggregations will experience severe latency.", styles['BulletItem']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Next Development Phase:</b>", styles['Normal']))
    story.append(Paragraph("Our next step is the database design and cloud configuration. We will define and write standard SQL deployment scripts "
                           "under `sql/` to compile the single production table `patient_vitals`. Following this, we will transition to Azure cloud setup, "
                           "deploying Azure Storage Blob, Azure SQL Database, and defining ADF Copy activities to link the ingestion pipelines.", styles['Normal']))

    story.append(Spacer(1, 15))
    story.append(Paragraph("11. Conclusion", styles['AcademicH1']))
    story.append(Paragraph(
        "The \"Automated Post-Hospital Patient Monitoring System\" has completed its foundational pre-ingestion phases. "
        "The raw telemetry has been profiled, structures audited, and a robust cleaning script executed. The clean dataset, "
        "saved in a database-compatible snake_case form, is staged at `data/processed/patient_vitals_clean.csv`. All actions "
        "have been formally documented in profiling, quality, and cleaning reports, establishing a production-ready starting point "
        "for the subsequent database DDL integration and Azure orchestration phases.",
        styles['Normal']
    ))
    
    story.append(Spacer(1, 40))
    
    # Sign-off box
    sign_data = [
        [Paragraph("<b>Submitted By:</b>", styles['MetadataLabel']), Paragraph("<b>Approved By:</b>", styles['MetadataLabel'])],
        [Paragraph("<br/><br/>_____________________________________<br/>Graduation Project Team", styles['MetadataVal']),
         Paragraph("<br/><br/>_____________________________________<br/>Project Supervisor", styles['MetadataVal'])]
    ]
    sign_table = Table(sign_data, colWidths=[250, 250])
    sign_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(sign_table)

    # Build document
    print(f"Building PDF at: {pdf_path}")
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete!")

if __name__ == "__main__":
    build_pdf_report()
