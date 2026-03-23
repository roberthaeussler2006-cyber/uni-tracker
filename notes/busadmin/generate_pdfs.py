#!/usr/bin/env python3
"""Generate PDF notes for Business Administration B - Financial Management."""

import sys
sys.path.insert(0, '/Users/roberthaeussler/Library/Python/3.9/lib/python/site-packages')

from fpdf import FPDF
import re
import os
import tempfile
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Temp directory for formula images
_FORMULA_DIR = tempfile.mkdtemp(prefix="busadmin_formulas_")
_FORMULA_COUNTER = 0

# Slide extraction directory
_SLIDE_DIR = tempfile.mkdtemp(prefix="busadmin_slides_")
_SLIDE_COUNTER = 0

# Base path for lecture slides
_SLIDES_BASE = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/busadmin/Lecture slides (for notes generation)'


def extract_slide(pdf_filename, page_num, crop_sidebar=False):
    """Extract a slide page from a lecture PDF as a cropped PNG image."""
    global _SLIDE_COUNTER
    _SLIDE_COUNTER += 1
    pdf_path = os.path.join(_SLIDES_BASE, pdf_filename)
    output_prefix = os.path.join(_SLIDE_DIR, f"slide_{_SLIDE_COUNTER}")

    subprocess.run([
        'pdftoppm', '-png', '-r', '300',
        '-f', str(page_num), '-l', str(page_num),
        pdf_path, output_prefix
    ], check=True, capture_output=True)

    raw_path = None
    for suffix in [f'-{page_num}.png', f'-{page_num:02d}.png', f'-{page_num:03d}.png']:
        candidate = output_prefix + suffix
        if os.path.exists(candidate):
            raw_path = candidate
            break
    if raw_path is None:
        raise FileNotFoundError(f"Could not find extracted slide image for page {page_num}")

    if crop_sidebar:
        from PIL import Image
        img = Image.open(raw_path)
        w, h = img.size
        cropped = img.crop((0, 0, int(w * 0.87), int(h * 0.97)))
        cropped.save(raw_path)

    return raw_path


def render_latex(latex_str, fontsize=14):
    """Render a LaTeX string to a PNG image and return the path."""
    global _FORMULA_COUNTER
    _FORMULA_COUNTER += 1
    path = os.path.join(_FORMULA_DIR, f"formula_{_FORMULA_COUNTER}.png")

    fig, ax = plt.subplots(figsize=(7, 0.15 * latex_str.count(r'\\') + 0.6))
    ax.text(0.5, 0.5, f"${latex_str}$", fontsize=fontsize,
            ha='center', va='center', transform=ax.transAxes)
    ax.axis('off')
    fig.savefig(path, dpi=200, bbox_inches='tight', pad_inches=0.05,
                transparent=False, facecolor='#F0F0FF')
    plt.close(fig)
    return path


class NotesPDF(FPDF):
    """Custom PDF class for generating FM study notes."""

    # BusAdmin indigo color scheme
    PRIMARY = (50, 50, 130)       # Deep indigo for titles
    SECONDARY = (70, 80, 170)     # Lighter indigo for sections
    ACCENT = (99, 102, 241)       # #6366F1 indigo accent

    def __init__(self, title, subtitle):
        super().__init__()
        self.title_text = title
        self.subtitle_text = subtitle
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, self.title_text, align="L")
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")
        self.set_text_color(0, 0, 0)

    def cover_page(self):
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*self.PRIMARY)
        self.multi_cell(0, 12, self.title_text, align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, self.subtitle_text, align="C")
        self.ln(15)
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 7, "Schaefer - Principles of Financial Management", align="C")
        self.ln(5)
        self.multi_cell(0, 7, "Study Notes", align="C")
        self.set_text_color(0, 0, 0)

    def chapter_title(self, text):
        self.ln(6)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*self.PRIMARY)
        self.multi_cell(0, 9, text)
        self.set_draw_color(*self.PRIMARY)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def section_title(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.SECONDARY)
        self.multi_cell(0, 7, text)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def subsection_title(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, text)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def sub_subsection_title(self, text):
        self.ln(2)
        self.set_font("Helvetica", "BI", 11)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 6, text)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self._write_rich_text(text, indent=0)
        self.ln(2)

    def bullet(self, text, level=0):
        indent = 8 + level * 8
        self.set_x(self.l_margin + indent)
        bullet_char = "-" if level == 0 else "  >"
        self.set_font("Helvetica", "", 10)
        self.cell(5, 5, bullet_char)
        self.set_x(self.l_margin + indent + 5)
        self._write_rich_text(text, indent=indent + 5)
        self.ln(1.5)

    def formula_block(self, latex, fontsize=14):
        """Render a LaTeX formula as an image and embed it centered."""
        self.ln(2)
        img_path = render_latex(latex, fontsize=fontsize)
        from PIL import Image
        with Image.open(img_path) as img:
            w_px, h_px = img.size
        w_mm = w_px * 25.4 / 200
        h_mm = h_px * 25.4 / 200
        max_w = self.w - self.l_margin - self.r_margin - 20
        if w_mm > max_w:
            scale = max_w / w_mm
            w_mm *= scale
            h_mm *= scale
        if self.get_y() + h_mm + 4 > self.h - self.b_margin:
            self.add_page()
        x = self.l_margin + (self.w - self.l_margin - self.r_margin - w_mm) / 2
        self.image(img_path, x=x, y=self.get_y(), w=w_mm, h=h_mm)
        self.set_y(self.get_y() + h_mm + 2)
        self.set_font("Helvetica", "", 10)

    def slide_figure(self, pdf_filename, page_num, caption, width_pct=0.85):
        """Embed a lecture slide as a captioned figure."""
        img_path = extract_slide(pdf_filename, page_num)
        from PIL import Image
        with Image.open(img_path) as img:
            w_px, h_px = img.size

        avail_w = (self.w - self.l_margin - self.r_margin) * width_pct
        w_mm = avail_w
        h_mm = (h_px / w_px) * w_mm

        needed = h_mm + 14
        if self.get_y() + needed > self.h - self.b_margin:
            self.add_page()

        self.ln(4)
        x = self.l_margin + (self.w - self.l_margin - self.r_margin - w_mm) / 2
        self.image(img_path, x=x, y=self.get_y(), w=w_mm, h=h_mm)
        self.set_y(self.get_y() + h_mm + 2)

        safe_caption = caption.replace('\u2014', '-').replace('\u2013', '-').replace('\u2019', "'")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 4, safe_caption, align="C")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 10)
        self.ln(3)

    def key_concept_box(self, title, text):
        self.ln(3)
        self.set_fill_color(235, 235, 255)   # Light indigo fill
        self.set_draw_color(99, 102, 241)     # Indigo border
        x = self.l_margin + 5
        w = self.w - self.l_margin - self.r_margin - 10
        self.set_x(x)
        self.set_font("Helvetica", "B", 10)
        self.cell(w, 6, title, fill=True, border="LTR")
        self.ln()
        self.set_x(x)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(w, 5, text, fill=True, border="LBR")
        self.ln(3)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*self.PRIMARY)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6, col, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)

    def table_row(self, cols, widths, fill=False):
        self.set_font("Helvetica", "", 9)
        if fill:
            self.set_fill_color(235, 235, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 5.5, col, border=1, fill=fill, align="C" if i > 0 else "L")
        self.ln()

    def _write_rich_text(self, text, indent=0):
        """Write text with **bold** markers converted to actual bold."""
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.set_font("Helvetica", "B", 10)
                content = part[2:-2]
            else:
                self.set_font("Helvetica", "", 10)
                content = part
            if content:
                self.write(5, content)
        self.ln()


# ============================================================
# LECTURE 1: Introduction (Schaefer Ch 1 & 2 + Lecture Slides)
# ============================================================

def generate_lecture1():
    """Generate Lecture 1 PDF: Introduction to Financial Management (Ch 1 & 2)."""
    pdf = NotesPDF(
        "FM Lecture 1: Introduction to Financial Management",
        "Schaefer Chapters 1 & 2 + Lecture 1 Slides"
    )
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ===== LECTURE CONTEXT =====
    pdf.add_page()
    pdf.chapter_title("LECTURE CONTEXT: INTRODUCTION & LEARNING OBJECTIVES")

    pdf.section_title("Course Overview")
    pdf.body_text("Business Administration B covers two parts: Business Ethics (KW 8-10, Prof. Festl) and Financial Management (KW 11-21, Dr. Simon Pfister). This lecture introduces Financial Management.")
    pdf.bullet("**Course weight**: 5.5 ECTS")
    pdf.bullet("**Exam**: Written, digital, 180 min, closed book (180 pts: 45 Ethics + 135 FM)")
    pdf.bullet("**Supplementary aids**: Private laptop (compulsory), mains adapter, LockDown Browser")

    pdf.section_title("Learning Objectives")
    pdf.bullet("Understand what Financial Management entails and how it is embedded in the St.Gallen Management Model (SGMM)")
    pdf.bullet("Understand the different sub-processes of Financial Management and their hierarchy")
    pdf.bullet("Understand the function of financial reporting and its principles")
    pdf.bullet("Know how a company communicates financial information to stakeholders")

    # ===== CHAPTER 1 =====
    pdf.add_page()
    pdf.chapter_title("CHAPTER 1: INTRODUCTION")

    pdf.section_title("1.1 What is Financial Management?")
    pdf.body_text("Financial Management (FM) is the discipline of managing a company's financial resources, reporting, and decision-making. The textbook is structured into four parts:")

    pdf.bullet("**Part A - Introduction**: Embedding FM into the SGMM, understanding FM sub-processes")
    pdf.bullet("**Part B - External Financial Management**: Financial accounting, financial reporting (external stakeholders)")
    pdf.bullet("**Part C - Internal Financial Management**: Management accounting, performance measurement (internal decision-making)")
    pdf.bullet("**Part D - Strategic Financial Management**: Operating decisions, strategic decisions (capital structure, M&A, investments)")

    pdf.key_concept_box(
        "Four Parts of Financial Management",
        "A: Introduction (SGMM embedding) -> B: External FM (accounting, reporting) -> "
        "C: Internal FM (management accounting, performance) -> D: Strategic FM (operating & strategic decisions)"
    )

    pdf.section_title("1.2 Symbols and Notation")
    pdf.body_text("Throughout the textbook, two running examples illustrate FM concepts:")
    pdf.bullet("**Nestle**: Used in the textbook as the primary case study (global FMCG company)")
    pdf.bullet("**On AG**: Used in lectures as the practical case study (Swiss running shoe company)")
    pdf.bullet("Key notation: Assets (A), Liabilities (L), Equity (E), Revenue (R), Expenses (Ex), Profit (P)")

    # ===== CHAPTER 2 =====
    pdf.add_page()
    pdf.chapter_title("CHAPTER 2: EMBEDDING FM INTO THE SGMM")

    pdf.section_title("2.1 Introductory Example: Nestle")
    pdf.body_text("The textbook opens with Nestle's strategic decision to invest in health-oriented business lines. This illustrates how FM supports strategic decision-making:")
    pdf.bullet("Nestle's shift toward health science (acquisition of medical nutrition companies)")
    pdf.bullet("FM provides the analytical framework: Is the investment profitable? Can it be financed? What are the risks?")
    pdf.bullet("The **goal triangle** of FM guides all such decisions: profitability, risk, and liquidity")

    pdf.section_title("2.2 Managerial Finance and the SGMM")

    pdf.subsection_title("The Goal Triangle of Financial Management")
    pdf.body_text("Every financial decision involves balancing three competing objectives:")
    pdf.bullet("**Profitability**: Generating returns (profit, ROI, ROE)")
    pdf.bullet("**Risk**: Managing uncertainty and potential losses")
    pdf.bullet("**Liquidity**: Ensuring the company can meet its payment obligations at all times")

    pdf.key_concept_box(
        "The Goal Triangle",
        "Profitability <-> Risk <-> Liquidity. These three goals are in constant tension. "
        "Higher profitability often means higher risk. Maintaining high liquidity reduces profitability "
        "(idle cash earns little). FM seeks the optimal balance for each specific company."
    )

    pdf.subsection_title("The FM Processes Pyramid")
    pdf.body_text("Financial Management consists of six hierarchical sub-processes, arranged in a pyramid. From bottom (most transactions, least abstraction) to top (fewest transactions, most strategic):")

    pdf.bullet("**Layer 1 - Financial Accounting** (base): Recording individual transactions in accordance with local laws and accounting/reporting standards")
    pdf.bullet("**Layer 2 - Financial Reporting**: Communicating financial position to external stakeholders (annual reports, interim reports)")
    pdf.bullet("**Layer 3 - Management Accounting**: Internal cost analysis, budgeting, planning for management decision-making")
    pdf.bullet("**Layer 4 - Performance Measurement**: Financial ratios, ratio systems (e.g., ROE decomposition), balanced scorecards")
    pdf.bullet("**Layer 5 - Operating Decisions**: Pricing, make-or-buy, revenue/cost efficiency")
    pdf.bullet("**Layer 6 - Strategic Decisions** (top): Capital structure, M&A, investment decisions")

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 16,
        'Figure: The FM Processes Pyramid - Six sub-processes from financial accounting to strategic decisions (Lecture Slide)')

    pdf.key_concept_box(
        "External vs. Internal FM",
        "External FM (Layers 1-2): Financial accounting + reporting -> communicates to external stakeholders "
        "(investors, regulators, public). Internal FM (Layers 3-6): Management accounting, performance measurement, "
        "operating and strategic decisions -> supports internal management decision-making."
    )

    pdf.subsection_title("FM as Support Process and Management Process")
    pdf.body_text("Within the SGMM, Financial Management serves a dual role:")
    pdf.bullet("**Support process**: FM provides the infrastructure for recording, reporting, and measuring financial data")
    pdf.bullet("**Management process**: FM actively shapes strategic and operational decisions through analysis and performance measurement")

    pdf.section_title("2.3 FM as an Essential Management Task")
    pdf.body_text("FM is not just a back-office function. It is essential for every manager because:")
    pdf.bullet("All business decisions have financial implications")
    pdf.bullet("Managers must understand financial reports to evaluate performance")
    pdf.bullet("Investment and financing decisions require FM expertise")
    pdf.bullet("Regulatory compliance (accounting standards, tax law) is mandatory")

    pdf.section_title("2.4 The Task Perspective of the SGMM")

    pdf.subsection_title("Environmental Spheres")
    pdf.body_text("Companies operate within four environmental spheres that influence FM:")
    pdf.bullet("**Society**: Social norms, demographic trends, public expectations")
    pdf.bullet("**Nature**: Environmental regulations, sustainability requirements")
    pdf.bullet("**Technology**: Digital transformation, automation of accounting, FinTech")
    pdf.bullet("**Economy**: Interest rates, inflation, capital markets, exchange rates")

    pdf.subsection_title("Stakeholders and Their Information Needs")
    pdf.body_text("A central function of financial reporting is to serve diverse stakeholders. Each group has different decision-making needs:")

    # Stakeholder table
    w_group = 28
    w_sub = 30
    w_decision = 42
    w_info = 50
    widths = [w_group, w_sub, w_decision, w_info]
    if pdf.get_y() + 70 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["Group", "Subgroup", "Decision (why)", "Info Need (what)"], widths)
    pdf.table_row(["Internal", "Management", "Planning", "Financial position, future"], widths, fill=True)
    pdf.table_row(["Internal", "Employees", "Workplace", "Continuity"], widths)
    pdf.table_row(["External", "Shareholders", "Buy/sell", "Return, financial pos."], widths, fill=True)
    pdf.table_row(["External", "Creditors", "Creditworthiness", "Liquidity"], widths)
    pdf.table_row(["External", "Pot. investors", "Investment", "Return, products, future"], widths, fill=True)
    pdf.table_row(["External", "Customers", "Cust. relationship", "Financial pos., products"], widths)
    pdf.table_row(["External", "Government", "Tax/regulation", "Profit, equity, liquidity"], widths, fill=True)
    pdf.table_row(["External", "Media", "Reporting", "Background info"], widths)
    pdf.table_row(["External", "Suppliers", "Creditworthiness", "Liquidity, earnings"], widths, fill=True)
    pdf.table_row(["External", "Rating agencies", "Credit assessment", "Liquidity, financial pos."], widths)
    pdf.ln(2)

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 46,
        'Figure: Stakeholders - their decisions and information needs (Lecture Slide, exam-relevant)')

    pdf.subsection_title("Interaction Issues")
    pdf.body_text("Stakeholders interact with the company on various issues: resources, norms & values, and concerns & interests. FM provides the data foundation for these interactions.")

    pdf.subsection_title("Processes and Value Creation")
    pdf.body_text("The SGMM distinguishes three types of processes:")
    pdf.bullet("**Management processes**: Strategy, governance, resource allocation")
    pdf.bullet("**Business processes and business model**: Core value creation activities")
    pdf.bullet("**Support processes**: FM, HR, IT, legal - enabling the business processes")

    pdf.subsection_title("Governance: Principal-Agent Theory")
    pdf.body_text("A key governance challenge in FM is the principal-agent problem:")
    pdf.bullet("**Principal**: The investor/owner who provides capital")
    pdf.bullet("**Agent**: The management team who runs the company")
    pdf.bullet("**Problem**: Information asymmetry - management knows more about the company than investors")
    pdf.bullet("**Solution**: Financial reporting, auditing, corporate governance mechanisms")

    pdf.key_concept_box(
        "Principal-Agent Model in FM",
        "Investors (principals) entrust capital to management (agents). Because of information asymmetry, "
        "agents could act in self-interest. Auditing bridges this gap: independent auditors verify "
        "financial statements, providing principals with trustworthy information for decision-making."
    )

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 45,
        'Figure: Principal-Agent Model - Auditing bridges information asymmetry between investors and management (Summary Slide)')

    pdf.section_title("2.5 The Praxis Perspective of the SGMM")

    pdf.subsection_title("Decision-Making Praxis")
    pdf.body_text("FM supports all levels of management decision-making through financial data and analysis.")

    pdf.subsection_title("Frame of Orientation")
    pdf.body_text("The SGMM distinguishes three management levels:")
    pdf.bullet("**Normative management**: Purpose, values, legitimacy (Why does the company exist?)")
    pdf.bullet("**Strategic management**: Positioning, competitive advantage (Where is the company going?)")
    pdf.bullet("**Operational management**: Day-to-day execution, efficiency (How does the company operate?)")
    pdf.body_text("FM contributes at all three levels: normative (transparency, trust), strategic (investment analysis, capital structure), and operational (budgeting, cost control).")

    pdf.subsection_title("Management Praxis and Executive Management")
    pdf.body_text("FM provides the quantitative foundation for management praxis - the actual exercise of management through communication, decision-making, and action.")

    pdf.section_title("2.6 Summary: The Four Sub-Processes of FM")
    pdf.body_text("Chapter 2 establishes that FM consists of four essential sub-processes, each corresponding to a part of the textbook:")
    pdf.bullet("**(1) Financial Accounting & Reporting** (External FM): Recording transactions and communicating financial position to external stakeholders")
    pdf.bullet("**(2) Management Accounting** (Internal FM): Providing internal decision-makers with cost, revenue, and budget information")
    pdf.bullet("**(3) Performance Measurement** (Internal FM): Evaluating company performance using financial ratios and systems")
    pdf.bullet("**(4) Operating & Strategic Decisions** (Strategic FM): Making investment, financing, and capital structure decisions")

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 44,
        'Figure: Summary - FM sub-processes pyramid and FM in the SGMM (Summary Slide)')

    # ===== LECTURE: ON AG CASE STUDY =====
    pdf.add_page()
    pdf.chapter_title("LECTURE CASE STUDY: ON AG")

    pdf.section_title("Company Overview")
    pdf.body_text("On AG is a Swiss running shoe company used as the running case study throughout the FM lectures (complementing Nestle in the textbook).")
    pdf.bullet("**Founded**: 2010 in Zurich, Switzerland")
    pdf.bullet("**Product**: Running shoes with patented CloudTec cushioning technology")
    pdf.bullet("**Notable investor**: Roger Federer (joined 2019)")
    pdf.bullet("**IPO**: September 2021 on NYSE at a valuation of USD 7.3 billion")
    pdf.bullet("**Growth**: CAGR of 66% since founding")
    pdf.bullet("**Management**: Co-CEO and CFO Martin Hoffmann; new CFO Frank Sluis from May 1, 2026")

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 24,
        "Figure: On AG - Company history and key milestones")

    pdf.section_title("Financial Reporting Structure")
    pdf.body_text("On AG's financial reporting follows a hierarchical structure:")
    pdf.bullet("**Financial Reporting** encompasses all external financial communication")
    pdf.bullet("Types: Ad hoc publicity, Pro-forma reports, Interim reports, Annual report")
    pdf.bullet("The **Annual Report** is the most comprehensive, containing:")
    pdf.bullet("**Financial Statements** (mandatory): Statement of Financial Position, Statement of Profit or Loss and OCI, Statement of Cash Flow, Statement of Changes in Equity, Notes", level=1)
    pdf.bullet("**Reports** (voluntary/regulatory): Management Report, Corporate Governance Report, CSR/Sustainability Report, Value Adding Report", level=1)

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 27,
        "Figure: Financial Reporting structure - hierarchy from ad hoc to annual reports")

    pdf.section_title("The Five Financial Statements")
    pdf.body_text("Financial statements serve different information needs of stakeholders:")
    pdf.bullet("**Statement of Financial Position** (Balance Sheet): What does the company own and owe? -> Assets, Liabilities, Equity")
    pdf.bullet("**Statement of Profit or Loss and OCI**: How profitable is the company? -> Revenue, Costs, Profit")
    pdf.bullet("**Statement of Cash Flows**: Where does cash come from and go? -> Operating, Investing, Financing cash flows")
    pdf.bullet("**Statement of Changes in Equity**: How has owners' equity changed?")
    pdf.bullet("**Notes**: Detailed explanations and disclosures supporting the other four statements")

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 38,
        "Figure: The 5-statement relationship diagram - how all financial statements interconnect")

    pdf.section_title("Reporting Standards")
    pdf.body_text("Companies must follow specific reporting standards depending on their type:")

    w_type = 38
    w_or = 30
    w_fer = 32
    w_usgaap = 30
    w_ifrs = 30
    widths2 = [w_type, w_or, w_fer, w_usgaap, w_ifrs]
    if pdf.get_y() + 40 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["Company Type", "OR", "Swiss GAAP", "US GAAP", "IFRS"], widths2)
    pdf.table_row(["Small/Medium (SME)", "Required", "Optional", "Optional", "Optional"], widths2, fill=True)
    pdf.table_row(["Large private", "Required", "Required", "Optional", "Optional"], widths2)
    pdf.table_row(["SIX-listed (CH)", "Required", "Accepted", "Accepted", "Accepted"], widths2, fill=True)
    pdf.table_row(["NYSE/NASDAQ-listed", "n/a", "n/a", "Required*", "Accepted"], widths2)
    pdf.ln(2)
    pdf.body_text("*On AG uses IFRS and reports in CHF despite being listed on NYSE (accepted under SEC rules).")

    pdf.key_concept_box(
        "On AG's Reporting Choice",
        "Despite NYSE listing (which typically requires US GAAP), On AG reports under IFRS in CHF. "
        "The SEC accepts IFRS for foreign private issuers. This is a practical example of how "
        "reporting standards work in an international context."
    )

    pdf.section_title("On AG's IPO Impact on Financial Statements")
    pdf.body_text("The September 2021 IPO had measurable effects across all financial statements:")
    pdf.bullet("**Balance Sheet**: Cash and cash equivalents increased dramatically from IPO proceeds; equity increased from share issuance")
    pdf.bullet("**Income Statement**: Revenue growth accelerated (brand visibility from IPO/NYSE listing)")
    pdf.bullet("**Cash Flow Statement**: Large positive financing cash flow from IPO; operating cash flow was still negative (growth-stage company)")

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 34,
        "Figure: On AG - Impact of IPO on Balance Sheet (cash increase, equity increase)")

    # ===== CSR AND SUSTAINABILITY REPORTING =====
    pdf.section_title("Corporate Social Responsibility (CSR) Reporting")
    pdf.body_text("Since COVID-19, companies view responsibility and sustainability differently, emphasizing both profit and resilience. Public companies must consider CSR in their reporting:")
    pdf.bullet("**CSR Report** (Corporate Social Responsibility): Documents a company's efforts, achievements, and plans related to social and environmental responsibility")
    pdf.bullet("On AG calls its CSR report an **'Impact Report'**")
    pdf.bullet("Quality standards for CSR reports differ from financial reporting: requirements are largely **voluntary** and frequency is **volatile**")
    pdf.bullet("Recommendation: Check applicable regulations, compare with industry peers")

    # ===== INVESTOR RELATIONS =====
    pdf.section_title("Investor Relations")
    pdf.body_text("Investor Relations (IR) is the strategic communication function between a company and the financial community.")
    pdf.bullet("**Objective 1 - Low volatility/stable share price**: Advantages for raising capital; decreases cost of capital")
    pdf.bullet("**Objective 2 - High trading volume**: Provides high level of liquidity for shareholders")
    pdf.bullet("**Objective 3 - Building trust**: Promotes company image and reputation in financial markets")

    pdf.key_concept_box(
        "Investor Relations Objectives (Exam Question 1.3)",
        "Three objectives: (1) Low volatility & stable share price -> lower cost of capital, "
        "(2) High trading volume -> liquidity for shareholders, "
        "(3) Building trust -> promotion of company image."
    )

    # ===== EXAM PRACTICE =====
    pdf.add_page()
    pdf.chapter_title("EXAM PRACTICE QUESTIONS")

    pdf.section_title("Question 1.2 (5 points)")
    pdf.body_text("List five possible addressees of annual reports. For each of them: explain their main interest as well as the relevant information from the annual report that would best serve this interest.")
    pdf.ln(2)
    pdf.body_text("Model answer: See stakeholder table above. Key addressees include:")
    pdf.bullet("**Management** (internal): Planning -> Financial position, future outlook")
    pdf.bullet("**Shareholders** (external): Buy/sell decisions -> Return, financial position")
    pdf.bullet("**Creditors** (external): Creditworthiness assessment -> Liquidity")
    pdf.bullet("**Government/Tax authorities** (external): Tax assessment -> Profit, equity")
    pdf.bullet("**Media** (external): Reporting -> Background information, problems, future")

    pdf.section_title("Question 1.3 (3 points)")
    pdf.body_text("List the objectives of Investor Relations and explain why these objectives are relevant for a company.")
    pdf.ln(2)
    pdf.body_text("Model answer:")
    pdf.bullet("**Low volatility and stable share price performance**: Relevant because it provides advantages for raising capital and decreases the cost of capital")
    pdf.bullet("**High trading volume**: Relevant because it ensures a high level of liquidity for shareholders, making shares attractive")
    pdf.bullet("**Building trust**: Relevant because it promotes the company's image and reputation in financial markets")

    pdf.slide_figure('FM_lecture01_Introduction_News.pdf', 47,
        "Figure: Exam Question 1.3 - Investor Relations objectives and their relevance")

    # ===== KEY TERMS =====
    pdf.add_page()
    pdf.chapter_title("KEY TERMS AND DEFINITIONS")

    terms = [
        ("Financial Management (FM)", "The discipline of managing a company's financial resources, reporting, and decision-making"),
        ("SGMM", "St. Gallen Management Model - a framework for understanding how organizations function"),
        ("Goal Triangle", "The three competing objectives of FM: Profitability, Risk, Liquidity"),
        ("Financial Accounting", "Recording individual financial transactions according to standards"),
        ("Financial Reporting", "Communicating financial information to external stakeholders"),
        ("Management Accounting", "Internal cost analysis, budgeting, and planning"),
        ("Performance Measurement", "Evaluating performance using financial ratios and systems"),
        ("Principal-Agent Problem", "Information asymmetry between owners (principals) and managers (agents)"),
        ("Auditing", "Independent verification of financial statements to bridge principal-agent gap"),
        ("IFRS", "International Financial Reporting Standards - global accounting framework"),
        ("US GAAP", "Generally Accepted Accounting Principles - US accounting standards"),
        ("Swiss GAAP FER", "Swiss accounting standards for mid-sized and non-listed companies"),
        ("OR (Obligationenrecht)", "Swiss Code of Obligations - minimum accounting requirements"),
        ("Annual Report", "Comprehensive yearly financial communication containing statements + reports"),
        ("CSR Report", "Corporate Social Responsibility report on environmental/social impact"),
        ("Investor Relations", "Strategic communication between a company and the financial community"),
    ]

    w_term = 55
    w_def = 105
    widths3 = [w_term, w_def]
    pdf.table_header(["Term", "Definition"], widths3)
    for i, (term, defn) in enumerate(terms):
        pdf.table_row([term, defn], widths3, fill=(i % 2 == 0))

    # Output
    output_dir = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/busadmin'
    output_path = os.path.join(output_dir, 'Lecture1_Introduction_to_FM.pdf')
    pdf.output(output_path)
    print(f"Generated: {output_path}")


def generate_lecture2():
    """Generate Lecture 2 PDF: Statement of Financial Position (Schaefer Ch 3 & 4 + Lecture 2 Slides)."""
    pdf = NotesPDF(
        "FM Lecture 2: Statement of Financial Position",
        "Schaefer Chapters 3 & 4 + Lecture 2 Slides"
    )
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ===== LECTURE CONTEXT =====
    pdf.add_page()
    pdf.chapter_title("LECTURE CONTEXT: STATEMENT OF FINANCIAL POSITION")

    pdf.section_title("Recap from Lecture 1")
    pdf.bullet("Financial reporting objectives: true and fair view, decision usefulness")
    pdf.bullet("Framework conditions: CO, Swiss GAAP FER, IFRS, US GAAP")
    pdf.bullet("Basic assumptions: accrual principle, going concern")
    pdf.bullet("Primary principles: understandability, relevance, reliability, comparability")
    pdf.bullet("FM Processes Pyramid: Financial Accounting -> Reporting -> Management Accounting -> Performance Measurement -> Decisions")

    pdf.section_title("Learning Objectives for Lecture 2")
    pdf.bullet("Understand the structure of the Statement of Financial Position (SFP)")
    pdf.bullet("Know the definition and recognition criteria for assets and liabilities")
    pdf.bullet("Understand first valuation (acquisition cost, cost of conversion) and subsequent valuation (depreciation, impairment, fair value)")
    pdf.bullet("Apply these concepts to selected positions: inventories, intangible assets, goodwill, provisions")

    pdf.section_title("Running Example: Nestle Group (2024)")
    pdf.body_text("The lecture uses Nestle's 2024 consolidated SFP as the primary example:")
    pdf.bullet("**Total assets**: CHF 139,264M")
    pdf.bullet("**Goodwill**: CHF 30,595M (22% of total assets)")
    pdf.bullet("**Total equity**: CHF 36,693M (26.4% of total assets)")
    pdf.bullet("Founded 1867, CHF 91.4B sales, CHF 210B market cap, SMI-listed")

    pdf.slide_figure('FM_lecture02_StatementOfFinancialPosition_News.pdf', 14,
        'Figure: Nestle 2024 Consolidated SFP - Asset side and Liability/Equity side')

    # ===== CHAPTER 3: OBJECTIVES AND PRINCIPLES =====
    pdf.add_page()
    pdf.chapter_title("CHAPTER 3: OBJECTIVES AND PRINCIPLES OF FINANCIAL REPORTING")

    pdf.section_title("3.2 Objectives of Financial Reporting")
    pdf.bullet("**True and fair view**: Financial statements must present a faithful picture of the company's financial position")
    pdf.bullet("**Decision usefulness**: Information must be useful for stakeholders making economic decisions")

    pdf.section_title("3.3 Framework Conditions and Accounting Standards")

    pdf.subsection_title("Swiss Code of Obligations (CO)")
    pdf.bullet("Art. 957: Who must keep accounts (all companies with revenue > CHF 500k)")
    pdf.bullet("Art. 957a: Bookkeeping principles")
    pdf.bullet("Art. 958: True and fair view requirement")
    pdf.bullet("Art. 962: When recognized standards (IFRS, Swiss GAAP FER) are required")

    pdf.subsection_title("Accounting Standards Hierarchy")
    pdf.bullet("**CO (Obligationenrecht)**: Minimum legal requirements for all Swiss companies")
    pdf.bullet("**Swiss GAAP FER**: Modular structure, conceptual framework FER 1-6; for mid-sized and non-listed companies")
    pdf.bullet("**IFRS**: International standards by IASB; required for SIX Main Standard listing")
    pdf.bullet("**US GAAP**: FASB standards; required for US-listed companies")
    pdf.bullet("**IPSAS**: For public sector and non-profit organizations")

    pdf.subsection_title("SIX Swiss Exchange Requirements")
    pdf.bullet("International Main Standard: requires IFRS or US GAAP")
    pdf.bullet("Domestic Standard: permits Swiss GAAP FER")

    pdf.section_title("3.4 Fundamentals of Financial Reporting")

    pdf.subsection_title("Basic Assumptions")
    pdf.bullet("**Accrual principle**: Revenues and costs are recognized when they occur, not when cash is received/paid")
    pdf.bullet("**Going concern**: Financial statements assume the company will continue to operate")

    pdf.subsection_title("Primary Principles")
    pdf.bullet("(1) **Understandability**: Information must be comprehensible to users with reasonable business knowledge")
    pdf.bullet("(2) **Relevance**: Information must be useful for decisions; includes **materiality** sub-principle")
    pdf.bullet("(3) **Reliability**: Five sub-principles:")
    pdf.bullet("Credible presentation, Substance over form, Neutrality, Prudence, Completeness", level=1)
    pdf.bullet("(4) **Comparability**: Financial statements must be comparable over time and across companies")

    pdf.section_title("3.5 Dimensions of Reporting")
    pdf.bullet("**Components**: SFP, P&L/OCI, Cash Flow Statement, Changes in Equity, Notes")
    pdf.bullet("**Timing**: Annual, half-yearly, quarterly, interim, ad hoc")
    pdf.bullet("**Industry**: Different formats for industrial, banking, insurance, non-profit")
    pdf.bullet("**Scope**: Management report, financial section, supplemental (CSR, sustainability)")

    # ===== CHAPTER 4: SFP STRUCTURE =====
    pdf.add_page()
    pdf.chapter_title("CHAPTER 4: STATEMENT OF FINANCIAL POSITION")

    pdf.section_title("4.2 SFP Structure")
    pdf.body_text("The SFP shows a company's financial position at a specific point in time. It has two sides:")
    pdf.bullet("**Assets** = Current Assets (CA) + Non-Current Assets (NCA)")
    pdf.bullet("**Liabilities and Equity** = Current Liabilities (CL) + Non-Current Liabilities (NCL) + Equity (E)")

    pdf.key_concept_box("Fundamental Equation",
        "Assets = Liabilities + Equity. Equity is the residual: Equity = Assets - Liabilities. "
        "This equation must always hold.")

    pdf.subsection_title("Current Assets")
    pdf.bullet("Cash and cash equivalents")
    pdf.bullet("Marketable securities")
    pdf.bullet("Trade receivables (net of value adjustments)")
    pdf.bullet("Inventories (raw materials, work-in-progress, finished goods)")
    pdf.bullet("Prepaid expenses and accrued income")

    pdf.subsection_title("Non-Current Assets")
    pdf.bullet("Property, plant and equipment (PPE)")
    pdf.bullet("Intangible assets (patents, trademarks, goodwill)")
    pdf.bullet("Long-term investments")

    # ===== ASSET DEFINITION AND RECOGNITION =====
    pdf.section_title("Asset Definition and Recognition Criteria")
    pdf.body_text("An item must pass two tests to appear on the SFP:")

    pdf.subsection_title("Definition Criteria (all 3 must be met)")
    pdf.bullet("(1) **Control**: The entity controls the resource")
    pdf.bullet("(2) **Past event**: The resource arose from a past transaction or event")
    pdf.bullet("(3) **Future economic benefits**: The resource is expected to generate future economic benefits")

    pdf.subsection_title("Recognition Criteria (both must be met)")
    pdf.bullet("(1) **Probable economic benefit**: It is probable that future economic benefits will flow to the entity")
    pdf.bullet("(2) **Reliable valuation**: The cost or value can be measured reliably")

    pdf.body_text("If definition criteria are met but recognition criteria are not, the item may be disclosed in the **notes** rather than on the SFP.")

    pdf.slide_figure('FM_lecture02_StatementOfFinancialPosition_News.pdf', 16,
        'Figure: Asset Disclosure Decision Tree - Definition criteria -> Recognition criteria -> SFP or Notes')

    pdf.subsection_title("Example: FC St. Gallen Transfer Fee (Lecture)")
    pdf.body_text("FC St. Gallen buys football player 'Ramon Goal' for the following costs:")
    pdf.bullet("**Transfer fee**: CHF 10M (paid to selling club)")
    pdf.bullet("**Hand money**: CHF 1M (paid to player as signing bonus)")
    pdf.bullet("**Salary**: CHF 6M (over 3 years, CHF 2M/year)")

    pdf.body_text("Testing the transfer fee against the criteria:")
    pdf.bullet("Control: Yes, the club controls the player's registration")
    pdf.bullet("Past event: Yes, the transfer contract has been signed")
    pdf.bullet("Future economic benefits: Yes, the player will generate revenue (match income, merchandise, potential resale)")
    pdf.bullet("Probable benefit: Yes")
    pdf.bullet("Reliable valuation: Yes, CHF 10M is the contractual price")
    pdf.body_text("Conclusion: **Capitalize the transfer fee** (CHF 10M) as an intangible asset. The salary (CHF 6M) is expensed over the contract period. The hand money (CHF 1M) is part of the acquisition cost.")

    # ===== LIABILITY DEFINITION =====
    pdf.section_title("Liability Definition and Recognition Criteria")

    pdf.subsection_title("Definition Criteria (all 3 must be met)")
    pdf.bullet("(1) **Obligation**: The entity has a present obligation (legal or constructive)")
    pdf.bullet("(2) **Past event**: The obligation arose from a past event")
    pdf.bullet("(3) **Future outflow**: Settlement is expected to result in an outflow of resources")

    pdf.subsection_title("Recognition Criteria (both must be met)")
    pdf.bullet("(1) **Probable outflow**: It is probable that resources will flow out")
    pdf.bullet("(2) **Reliable determination**: The amount can be determined reliably")

    # ===== VALUATION =====
    pdf.add_page()
    pdf.chapter_title("VALUATION OF ASSETS AND LIABILITIES")

    pdf.section_title("First Valuation (Initial Recognition)")

    pdf.subsection_title("Acquisition Cost (Purchased Assets)")
    pdf.formula_block(r"\text{Acquisition cost} = \text{Purchase price} + \text{Incidental costs} - \text{Price reductions} + \text{Financial expenses (IAS 23)}", fontsize=11)
    pdf.bullet("**Incidental costs**: Import duties, transport, packaging, non-recoverable taxes, handling")
    pdf.bullet("**Price reductions**: Trade discounts, rebates, volume discounts")
    pdf.bullet("**IAS 23**: Borrowing costs directly attributable to acquisition may be capitalized")

    pdf.subsection_title("Cost of Conversion (Manufactured Assets)")
    pdf.formula_block(r"\text{Cost of conversion} = \text{Direct costs} + \text{Production overhead} + \text{Conveyance costs} + \text{Fin. expenses}", fontsize=11)
    pdf.bullet("Direct costs: raw materials, direct labor")
    pdf.bullet("Production overhead: factory rent, depreciation of production equipment, supervisor salaries")
    pdf.bullet("**Prohibited from inclusion**: Idle capacity costs, non-production inventory costs, admin overhead, distribution costs")

    pdf.section_title("Subsequent Valuation")
    pdf.body_text("After initial recognition, assets are valued using one of three approaches:")

    pdf.subsection_title("1. Depreciation (Systematic)")
    pdf.bullet("Allocates the cost of an asset over its useful life")
    pdf.bullet("Methods: straight-line, declining balance, activity-based")
    pdf.formula_block(r"\text{Depreciable amount} = \text{Acquisition cost} - \text{Residual value}", fontsize=12)

    pdf.subsection_title("2. Impairment (Non-Recurring)")
    pdf.bullet("A one-time write-down when the asset's carrying amount exceeds its recoverable amount")
    pdf.bullet("Per IAS 36: test when indicators of impairment exist")

    pdf.subsection_title("3. Fair Value (Market-Based)")
    pdf.bullet("The price that would be received to sell an asset in an orderly transaction")
    pdf.bullet("Used when market prices are available and reliable")

    pdf.subsection_title("Inventory Valuation Methods")
    pdf.bullet("**FIFO** (First In, First Out): Oldest inventory is sold first; ending inventory reflects recent prices")
    pdf.bullet("**Weighted Average**: Average cost of all units available; smooths price fluctuations")
    pdf.bullet("**Lower of cost or market**: Inventories carried at the lower of acquisition cost and net selling price")

    pdf.slide_figure('FM_lecture02_StatementOfFinancialPosition_News.pdf', 33,
        'Figure: Lower of Cost or Market - Cost vs. Net Selling Price over time; write-down when market falls below cost')

    # ===== INTANGIBLE ASSETS =====
    pdf.add_page()
    pdf.chapter_title("SELECTED FINANCIAL POSITIONS")

    pdf.section_title("Intangible Assets (IAS 38)")
    pdf.body_text("Beyond the standard 3 asset definition criteria, intangible assets must also be:")
    pdf.bullet("**Identifiable**: Can be separated from the entity or arises from contractual/legal rights")
    pdf.bullet("**Non-monetary**: Not cash or a right to receive cash")
    pdf.bullet("**Without physical substance**: No tangible form")

    pdf.subsection_title("Research vs Development (R&D)")
    pdf.body_text("The treatment of R&D costs differs sharply between the two phases:")
    pdf.bullet("**Research phase**: Always expensed immediately (too uncertain to capitalize)")
    pdf.bullet("**Development phase**: May be capitalized as an intangible asset if ALL 6 criteria are met:")
    pdf.bullet("(1) Technical feasibility of completing the asset", level=1)
    pdf.bullet("(2) Intention to complete and use/sell", level=1)
    pdf.bullet("(3) Ability to use or sell the asset", level=1)
    pdf.bullet("(4) Demonstration that the asset will generate future economic benefits", level=1)
    pdf.bullet("(5) Availability of adequate resources to complete development", level=1)
    pdf.bullet("(6) Ability to reliably attribute costs to the development phase", level=1)

    pdf.key_concept_box("R&D Treatment Summary",
        "Research = ALWAYS expense. Development = capitalize only if ALL 6 criteria met. "
        "In practice, many companies expense all R&D because proving the 6 criteria is difficult. "
        "Important: brands created in-house and customer lists CANNOT be capitalized (no reliable valuation).")

    # ===== GOODWILL =====
    pdf.section_title("Goodwill (IFRS 3)")

    pdf.subsection_title("Definition")
    pdf.body_text("Goodwill arises ONLY from acquisitions. It is the premium paid above the fair value of the acquired company's net assets:")
    pdf.formula_block(r"\text{Goodwill} = \text{Purchase Price} - \text{Revalued Net Assets of Acquired Company}")

    pdf.body_text("Reasons a buyer pays more than net asset value:")
    pdf.bullet("Expected excess returns (synergies, market position)")
    pdf.bullet("Non-capitalizable assets (employee know-how, customer relationships)")
    pdf.bullet("Strategic pricing (elimination of a competitor)")

    pdf.subsection_title("Example 1: Simple Acquisition (Textbook)")
    pdf.body_text("Parent buys Subsidiary for CHF 130M. Revalued equity of Subsidiary = CHF 110M.")
    pdf.formula_block(r"\text{Goodwill} = 130 - 110 = \text{CHF 20M}")
    pdf.bullet("Goodwill is capitalized as an intangible asset on the acquirer's SFP")
    pdf.bullet("Goodwill is NOT amortized but tested for impairment annually")

    pdf.subsection_title("Goodwill Impairment Test")
    pdf.body_text("Each year, compare the recoverable amount (sum of expected future cash flows) to the carrying amount:")
    pdf.bullet("If recoverable amount >= carrying amount: no impairment")
    pdf.bullet("If recoverable amount < carrying amount: write down to recoverable amount")
    pdf.bullet("**Impairment of goodwill can NEVER be reversed**")

    pdf.subsection_title("Example 2: Full vs Partial Goodwill (Lecture)")
    pdf.body_text("Parent buys 60% of Subsidiary for CHF 180M. Revalued equity of Subsidiary = CHF 200M.")

    pdf.body_text("**Full goodwill method**: Gross up to 100% of the purchase price:")
    pdf.formula_block(r"\text{Implied 100\% price} = \frac{180}{0.60} = 300")
    pdf.formula_block(r"\text{Full goodwill} = 300 - 200 = \text{CHF 100M}")

    pdf.body_text("**Partial goodwill method**: Only recognize the acquirer's share:")
    pdf.formula_block(r"\text{Partial goodwill} = 180 - (0.60 \times 200) = 180 - 120 = \text{CHF 60M}")

    pdf.key_concept_box("Full vs Partial Goodwill",
        "Full method: grosses up to 100%, recognizes goodwill for both majority and minority. "
        "Partial method: only recognizes goodwill attributable to the acquirer. "
        "IFRS allows both methods. Full method results in higher total assets and higher minority interest.")

    pdf.subsection_title("Kraft-Heinz: $7.3B Goodwill Impairment (Lecture)")
    pdf.body_text("Kraft-Heinz wrote down $7.3 billion in goodwill, causing a dramatic drop in equity. This illustrates the real-world impact of overpaying for acquisitions and the importance of goodwill impairment testing.")

    # ===== EXAM EXAMPLE =====
    pdf.add_page()
    pdf.section_title("Exam Example: AllMyServices / CreativeApp (Lecture)")
    pdf.body_text("AllMyServices Ltd. acquires CreativeApp Ltd. for CHF 20M. The individual positions must be revalued:")
    pdf.bullet("Step 1: Revalue all individual assets and liabilities to fair value")
    pdf.bullet("Step 2: Calculate revalued equity = Revalued assets - Revalued liabilities = CHF 7.5M")
    pdf.bullet("Step 3: Calculate goodwill:")
    pdf.formula_block(r"\text{Goodwill} = 20\text{M} - 7.5\text{M} = \text{CHF 12.5M}")
    pdf.bullet("Step 4: Record booking entries (debit assets at fair value, debit goodwill, credit cash/consideration)")

    pdf.slide_figure('FM_lecture02_StatementOfFinancialPosition_News.pdf', 45,
        'Figure: AllMyServices/CreativeApp Exam Example - Revaluation, booking entries, and goodwill calculation')

    # ===== PROVISIONS =====
    pdf.section_title("Provisions and Contingent Liabilities (IAS 37)")

    pdf.subsection_title("Provisions")
    pdf.body_text("A provision is a liability of uncertain timing or amount. Three preconditions:")
    pdf.bullet("(1) Present obligation from a past event")
    pdf.bullet("(2) Probable outflow of resources (> 50% probability)")
    pdf.bullet("(3) Reliable estimation of the amount")

    pdf.subsection_title("Decision Tree")
    pdf.bullet("**Probability > 50%** and reliable estimate: Recognize a **provision** on the SFP")
    pdf.bullet("**Probability < 50%** (but not negligible): Disclose as **contingent liability** in notes")
    pdf.bullet("**Negligible probability**: No disclosure required")

    pdf.slide_figure('FM_lecture02_StatementOfFinancialPosition_News.pdf', 43,
        'Figure: Decision Tree for Provisions vs Contingent Liabilities')

    pdf.subsection_title("Warranty Provision Example")
    pdf.body_text("L-Tech AG sells 500,000 keyboards. Historical data shows 10% defect rate, CHF 7 repair cost per unit:")
    pdf.formula_block(r"\text{Warranty provision} = 500{,}000 \times 10\% \times \text{CHF 7} = \text{CHF 350,000}")

    # ===== EQUITY =====
    pdf.section_title("Equity Positions")
    pdf.body_text("Equity = Paid-in capital + Earned capital (retained earnings, reserves).")
    pdf.bullet("**Share capital**: Swiss law requires minimum CHF 100,000 (Art. 621 CO), with at least 20% paid-in (Art. 632 CO)")
    pdf.bullet("**Legal reserves**: 5% of annual profit until reserve = 20% of share capital (Art. 671 CO)")
    pdf.bullet("**Retained earnings**: Accumulated profits not distributed as dividends")
    pdf.bullet("**Other comprehensive income (OCI)**: Currency translation, revaluation reserves, actuarial gains/losses")

    # ===== DEPRECIATION METHODS =====
    pdf.add_page()
    pdf.chapter_title("DEPRECIATION METHODS (TEXTBOOK DETAIL)")

    pdf.body_text("Three common methods for systematic depreciation of PPE and intangible assets. Example: Asset cost = CHF 500k, useful life = 5 years, residual value = 0.")

    pdf.section_title("1. Straight-Line")
    pdf.formula_block(r"\text{Annual depreciation} = \frac{500{,}000}{5} = \text{CHF 100,000 per year}", fontsize=12)
    pdf.bullet("Equal charge each year. Simplest and most common method.")

    pdf.section_title("2. Declining Balance")
    pdf.bullet("Fixed percentage applied to the **book value** (not original cost)")
    pdf.bullet("Higher depreciation in early years, decreasing over time")
    pdf.bullet("Example with 40% rate: Year 1 = 200k, Year 2 = 120k, Year 3 = 72k, etc.")

    pdf.section_title("3. Activity-Based (Units of Production)")
    pdf.formula_block(r"\text{Depreciation} = \frac{\text{Actual activity}}{\text{Total expected activity}} \times \text{Depreciable amount}", fontsize=12)
    pdf.bullet("Ties depreciation to actual usage (e.g., machine hours, units produced)")
    pdf.bullet("More accurate when asset wear depends on usage, not time")

    # ===== SUMMARY =====
    pdf.add_page()
    pdf.chapter_title("SUMMARY OF KEY EQUATIONS AND TERMS")

    pdf.section_title("Key Equations")
    pdf.formula_block(r"\text{Equity} = \text{Assets} - \text{Liabilities}", fontsize=12)
    pdf.formula_block(r"\text{Goodwill} = \text{Purchase Price} - \text{Revalued Net Assets}", fontsize=12)
    pdf.formula_block(r"\text{Full Goodwill} = \frac{\text{Purchase Price}}{\text{Ownership \%}} - \text{Revalued Equity}", fontsize=12)
    pdf.formula_block(r"\text{Partial Goodwill} = \text{Purchase Price} - (\text{Ownership \%} \times \text{Revalued Equity})", fontsize=12)
    pdf.formula_block(r"\text{Acquisition Cost} = \text{Price} + \text{Incidentals} - \text{Discounts} + \text{IAS 23}", fontsize=12)
    pdf.formula_block(r"\text{Depreciable Amount} = \text{Cost} - \text{Residual Value}", fontsize=12)
    pdf.formula_block(r"\text{Warranty Provision} = \text{Units} \times \text{Defect Rate} \times \text{Cost per Unit}", fontsize=12)

    pdf.section_title("Key Terms")
    terms = [
        ("Statement of Financial Position (SFP)", "Balance sheet showing assets, liabilities, and equity at a point in time"),
        ("Current Assets", "Assets expected to be converted to cash within 12 months"),
        ("Non-Current Assets", "Long-term assets: PPE, intangibles, investments"),
        ("Asset Definition Criteria", "Control + Past event + Future economic benefits"),
        ("Asset Recognition Criteria", "Probable benefit + Reliable valuation"),
        ("Liability Definition Criteria", "Obligation + Past event + Future outflow"),
        ("Acquisition Cost", "Purchase price + incidentals - discounts + IAS 23"),
        ("Cost of Conversion", "Direct costs + production overhead (excl. admin/distribution)"),
        ("Depreciation", "Systematic allocation of cost over useful life"),
        ("Impairment", "Non-recurring write-down when carrying > recoverable amount"),
        ("Fair Value", "Market-based exit price in orderly transaction"),
        ("Lower of Cost or Market", "Inventories carried at lower of cost and net selling price"),
        ("FIFO", "First In, First Out inventory method"),
        ("Intangible Asset", "Identifiable, non-monetary, no physical substance"),
        ("Goodwill", "Purchase premium over revalued net assets; only from acquisitions"),
        ("Full Goodwill Method", "Grosses up to 100%; higher assets and minority interest"),
        ("Partial Goodwill Method", "Only acquirer's share of goodwill recognized"),
        ("Goodwill Impairment", "Annual test; write-down if recoverable < carrying; never reversible"),
        ("Provision (IAS 37)", "Liability with uncertain timing/amount; > 50% probability"),
        ("Contingent Liability", "Possible obligation; < 50% probability; disclosed in notes only"),
        ("Accrual Principle", "Recognize revenues/costs when they occur, not when cash moves"),
        ("Going Concern", "Assumption that the company will continue operating"),
        ("IAS 23", "Borrowing costs standard; allows capitalization of directly attributable costs"),
        ("IAS 38", "Intangible assets standard; R&D, patents, goodwill rules"),
    ]

    w_term = 55
    w_def = 105
    widths3 = [w_term, w_def]
    pdf.table_header(["Term", "Definition"], widths3)
    for i, (term, defn) in enumerate(terms):
        pdf.table_row([term, defn], widths3, fill=(i % 2 == 0))

    # Output
    output_dir = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/busadmin'
    output_path = os.path.join(output_dir, 'Lecture2_Statement_of_Financial_Position.pdf')
    pdf.output(output_path)
    print(f"Generated: {output_path}")


def generate_lecture3():
    """Generate Lecture 3 PDF: Statement of Profit or Loss & Cash Flows (Schaefer Ch 5 excl. 5.5 & Ch 6 + Lecture 3 Slides)."""
    pdf = NotesPDF(
        "FM Lecture 3: Statement of Profit or Loss & Cash Flows",
        "Schaefer Chapters 5 (excl. 5.5) & 6 + Lecture 3 Slides"
    )
    pdf.alias_nb_pages()
    pdf.cover_page()

    SLIDES = 'FM_lecture03_P&L_CashFlow_News.pdf'

    # ===== LECTURE CONTEXT =====
    pdf.add_page()
    pdf.chapter_title("LECTURE CONTEXT & LEARNING OBJECTIVES")

    pdf.section_title("From the News: Cash Flow vs Revenue")
    pdf.body_text("If you run out of cash, you stop paying salaries and supplier invoices -- and you will be left alone. Cash is king.")
    pdf.bullet("**Revenue-driven bankruptcies**: Toys R Us (2017, Amazon/Walmart competition + heavy debt), Blockbuster (2010, streaming shift). Pattern: revenue declines -> fixed costs remain -> margins compress -> operating losses -> debt unserviceable -> liquidity crisis")
    pdf.bullet("**Cash-driven bankruptcies**: Toys R Us (leveraged buyout, profitable on paper but interest drained cash), DeLorean (1982, production delays exhausted working capital), Pan Am (1991, rising fuel costs + declining sales)")
    pdf.bullet("Lesson: profitable on paper does not mean solvent. Both revenue and cash matter -- together is better.")

    pdf.slide_figure(SLIDES, 6,
        'Figure: Revenue-related bankruptcy pattern -- from declining revenue to liquidity crisis')

    pdf.section_title("Nestle Context")
    pdf.body_text("Nestle underperformed peers over 5 years (normalized index ~130 vs Mondelez ~180, PepsiCo/Coca-Cola ~150-160). Revenue peaked at CHF 94.4B in 2022, declined to 89.5B by 2025. Factors: negative volume growth (RIG), Swiss Franc strength (-7.8% in 2023), strategic divestitures.")

    pdf.section_title("Learning Objectives")
    pdf.bullet("Be able to read and understand the statement of profit or loss")
    pdf.bullet("Be able to calculate and interpret the free cash flow")
    pdf.bullet("Understand the differences between the Statement of Profit or Loss and the Statement of Cash Flows")
    pdf.bullet("Preparation: Self-study of Schaefer chapters 5 and 6")

    # ===== CHAPTER 5: STATEMENT OF PROFIT OR LOSS =====
    pdf.add_page()
    pdf.chapter_title("CHAPTER 5: STATEMENT OF PROFIT OR LOSS")

    pdf.section_title("5.1 Introductory Example: Looser Group")
    pdf.body_text("The textbook uses the Looser industrial group to introduce P&L analysis. In 2012, Looser increased sales by 3.9% to CHF 472.9M. After adjusting for currency, acquisitions, and divestments, organic growth was 4.2%. Key questions:")
    pdf.bullet("What does sales development tell us about the company?")
    pdf.bullet("What figures besides sales are important for assessing earnings?")
    pdf.bullet("Why is segment reporting important?")

    pdf.section_title("5.2 Definition: P&L vs Comprehensive Income")
    pdf.body_text("The statement of profit or loss provides information about a company's profitability by comparing output (revenue) and input (expenses) for the reporting period. Under IFRS, it is an integral part of the statement of other comprehensive income.")

    pdf.key_concept_box("Two Components of Comprehensive Income",
        "Profit or Loss = Revenue - Expenses (the 'regular' P&L). "
        "Other Comprehensive Income (OCI) = items recognized outside P&L (currency translations, "
        "hedge reserves, revaluation surplus, actuarial gains/losses). "
        "Total Comprehensive Income = Profit or Loss + OCI.")

    pdf.body_text("Items in OCI are split into two categories:")
    pdf.bullet("**Items that may be reclassified** to P&L later (e.g., currency retranslations, hedge reserves)")
    pdf.bullet("**Items that will never be reclassified** to P&L (e.g., remeasurement of defined benefit plans, fair value changes of equity instruments)")

    # ===== COGS METHOD =====
    pdf.section_title("5.3 COGS Method (Cost of Goods Sold / Function of Expense)")
    pdf.body_text("The COGS method classifies expenses by their function (production, distribution, admin, R&D). This is the more modern approach and allows calculation of a gross profit margin.")

    pdf.formula_block(r"\text{Sales Revenue} - \text{COGS} = \mathbf{Gross Profit}", fontsize=12)
    pdf.formula_block(r"\text{Gross Profit} - \text{Distribution} - \text{Admin} - \text{Other} = \mathbf{EBIT}", fontsize=12)

    pdf.key_concept_box("COGS Method Characteristics",
        "Advantages: Allows gross profit calculation; shows costs by department (production, sales, R&D). "
        "Disadvantage: Total expense types (total personnel, total depreciation) are NOT disclosed -- "
        "important detail for cost-saving measures is hidden.")

    pdf.subsection_title("Example: Nestle 2024 (COGS Method)")
    # Nestle P&L table
    w_item = 80
    w_2024 = 35
    w_2023 = 35
    widths = [w_item, w_2024, w_2023]
    if pdf.get_y() + 100 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["Line Item (CHF millions)", "2024", "2023"], widths)
    pdf.table_row(["Sales", "91,354", "92,998"], widths, fill=True)
    pdf.table_row(["Cost of goods sold", "(48,670)", "(50,328)"], widths)
    pdf.table_row(["Distribution expenses", "(7,567)", "(7,765)"], widths, fill=True)
    pdf.table_row(["Marketing & admin expenses", "(18,112)", "(17,549)"], widths)
    pdf.table_row(["R&D costs", "(1,667)", "(1,656)"], widths, fill=True)
    pdf.table_row(["Other trading income/(expenses)", "(1,071)", "(1,533)"], widths)
    pdf.table_row(["Trading operating profit", "14,633", "14,520"], widths, fill=True)
    pdf.table_row(["Other operating income/(expenses)", "91", "(457)"], widths)
    pdf.table_row(["Operating profit (EBIT)", "14,724", "14,063"], widths, fill=True)
    pdf.table_row(["Financial result", "(1,485)", "(1,360)"], widths)
    pdf.table_row(["Profit before taxes", "13,239", "12,703"], widths, fill=True)
    pdf.table_row(["Taxes", "(3,314)", "(2,314)"], widths)
    pdf.table_row(["Income from associates/JV", "1,249", "1,120"], widths, fill=True)
    pdf.table_row(["Profit for the year", "11,174", "11,509"], widths)
    pdf.ln(2)
    pdf.body_text("Despite decreasing sales, most earnings increased. The increase in profit of the year is driven by income from non-controlled entities.")

    pdf.subsection_title("Key Definitions from Nestle P&L")
    pdf.bullet("**Associates**: Subsidiaries owned less than 50% by Nestle")
    pdf.bullet("**Joint ventures**: Owned 50% by Nestle")
    pdf.bullet("**Non-controlling interests (NCI)**: Other owners (e.g., Chinese subsidiary 20% owned by government)")

    pdf.subsection_title("Example: On AG 2024 (COGS Method)")
    pdf.body_text("On AG's P&L demonstrates the COGS method for a growth company:")
    w_item2 = 65
    w_24 = 30
    w_23 = 30
    w_22 = 30
    widths2 = [w_item2, w_24, w_23, w_22]
    if pdf.get_y() + 70 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["CHF millions", "2024", "2023", "2022"], widths2)
    pdf.table_row(["Net sales", "2,318", "1,792", "1,222"], widths2, fill=True)
    pdf.table_row(["Cost of sales", "(913)", "(725)", "(537)"], widths2)
    pdf.table_row(["Gross profit", "1,406", "1,067", "685"], widths2, fill=True)
    pdf.table_row(["SG&A expenses", "(1,194)", "(887)", "(600)"], widths2)
    pdf.table_row(["Operating result", "212", "180", "85"], widths2, fill=True)
    pdf.table_row(["FX gain/(loss)", "68", "(111)", "(7)"], widths2)
    pdf.table_row(["Net income", "242", "80", "58"], widths2, fill=True)
    pdf.ln(2)

    # ===== TOTAL COST METHOD =====
    pdf.add_page()
    pdf.section_title("5.4 Total Cost Method (Nature of Expense)")
    pdf.body_text("The total cost method classifies expenses by their nature (materials, personnel, depreciation). It was the method taught in the Accounting lecture.")

    pdf.formula_block(r"\text{Sales} + \Delta\text{Inventories} - \text{Materials} - \text{Personnel} - \text{Depreciation} - \text{Other} = \mathbf{EBIT}", fontsize=11)

    pdf.key_concept_box("Total Cost Method Characteristics",
        "Advantages: Discloses total amounts by expense type (total depreciation, total material, total personnel). "
        "Disadvantage: No expense details by department (production vs sales vs R&D); "
        "no gross profit calculation possible.")

    pdf.subsection_title("Example: Swatch Group 2024 (Total Cost Method)")
    w_item3 = 70
    w_24b = 25
    w_pct24 = 20
    w_23b = 25
    w_pct23 = 20
    widths3 = [w_item3, w_24b, w_pct24, w_23b, w_pct23]
    if pdf.get_y() + 90 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["CHF million", "2024", "%", "2023", "%"], widths3)
    pdf.table_row(["Net sales", "6,735", "100.0", "7,888", "100.0"], widths3, fill=True)
    pdf.table_row(["Other operating income", "263", "3.9", "136", "1.7"], widths3)
    pdf.table_row(["Changes in inventories", "213", "3.2", "687", "8.7"], widths3, fill=True)
    pdf.table_row(["Material purchases", "(1,345)", "(20.0)", "(1,864)", "(23.6)"], widths3)
    pdf.table_row(["Personnel expense", "(2,506)", "(37.2)", "(2,550)", "(32.3)"], widths3, fill=True)
    pdf.table_row(["Depreciation & impairment", "(416)", "(6.2)", "(390)", "(5.0)"], widths3)
    pdf.table_row(["Other operating expenses", "(2,640)", "(39.2)", "(2,716)", "(34.4)"], widths3, fill=True)
    pdf.table_row(["Operating result", "304", "4.5", "1,191", "15.1"], widths3)
    pdf.table_row(["Net result", "219", "3.3", "890", "11.3"], widths3, fill=True)
    pdf.ln(2)

    # ===== COMPARISON =====
    pdf.section_title("Comparison: COGS Method vs Total Cost Method")
    pdf.body_text("Both methods start with sales revenue and arrive at EBIT. Differences exist only above EBIT:")
    pdf.bullet("**COGS method**: Expenses classified by function (production, distribution, admin). Calculates **gross profit**. Below EBIT: identical.")
    pdf.bullet("**Total cost method**: Expenses classified by nature (materials, personnel, depreciation). Includes **inventory changes**. Below EBIT: identical.")

    pdf.slide_figure(SLIDES, 19,
        'Figure: COGS method vs Total Cost method -- both lead to EBIT, differences only above EBIT')

    pdf.body_text("Below EBIT, both methods follow the same structure:")
    pdf.formula_block(r"\text{EBIT} \pm \text{Financial Result} = \text{EBT}", fontsize=12)
    pdf.formula_block(r"\text{EBT} - \text{Taxes} + \text{Income from Associates} = \text{Profit for the Period}", fontsize=12)
    pdf.bullet("Profit split into: attributable to shareholders of the parent (net profit) and non-controlling interests")

    # ===== REVENUE RECOGNITION =====
    pdf.add_page()
    pdf.section_title("Revenue Recognition (IFRS 15)")
    pdf.body_text("Revenue is recognized when control of goods has transferred to the customer (mainly upon arrival), not when the contract is signed, invoice issued, or payment received.")

    pdf.subsection_title("IFRS 15 Five-Step Model (since January 2018)")
    pdf.bullet("(1) Identify the customer contract")
    pdf.bullet("(2) Identify the company's contractual delivery obligations (performance obligations)")
    pdf.bullet("(3) Determine the transaction price")
    pdf.bullet("(4) Allocate transaction price to contractual delivery obligations")
    pdf.bullet("(5) Recognize revenue as the company fulfills each delivery obligation")

    pdf.key_concept_box("Revenue Recognition Timing",
        "Revenue is recognized at the moment of 'handing over' to the customer, at the value "
        "the company can expect from the return service. IFRS 15 introduces more judgment, e.g.: "
        "long-term construction (percentage of completion), telecoms (24-month subscription with "
        "phone for CHF 1 -- each is a separate performance obligation).")

    pdf.subsection_title("Nestle Revenue Policy")
    pdf.bullet("Recognized when control of goods has transferred to the customer (mainly upon arrival)")
    pdf.bullet("Measured at expected consideration after deductions (returns, taxes, discounts, allowances, promotions)")
    pdf.bullet("Credit terms are short-term, in line with market practice, no financing component")

    pdf.subsection_title("Nestle COGS Policy")
    pdf.bullet("COGS includes: raw materials, packaging, direct labor, energy, manufacturing overheads, depreciation of factory assets")
    pdf.bullet("Adjusted for: inventory variation, royalties, amortization of acquired licenses")
    pdf.bullet("Also includes: maintenance/depreciation of equipment used in sales (coffee machines, water coolers)")

    # ===== IMPAIRMENTS =====
    pdf.section_title("Impairments (from Lecture)")

    pdf.subsection_title("Trade Receivables (IFRS 9)")
    pdf.bullet("Recognized initially at transaction price, measured at amortized cost less loss allowances")
    pdf.bullet("Nestle applies IFRS 9 simplified approach: expected credit losses (ECLs) based on 3-5 year actual loss experience")
    pdf.bullet("Credit impaired when: significant financial difficulty of customer, or bankruptcy becoming probable")

    pdf.subsection_title("Goodwill and Intangible Assets (Recap)")
    pdf.bullet("Indefinite life / not-yet-available assets: tested for impairment at least annually")
    pdf.bullet("Finite life assets: tested when indicators of impairment exist")
    pdf.bullet("Tests at CGU (cash generating unit) level, defined by product category per zone")
    pdf.bullet("Compare carrying amount with recoverable amount (usually fair value less disposal costs)")
    pdf.bullet("Goodwill impairment is **never subsequently reversed**")

    # ===== PROVISIONS =====
    pdf.section_title("Provisions and Contingencies (Lecture Detail)")
    pdf.bullet("**Provisions**: Liabilities of uncertain timing or amount from restructuring, environmental, litigation risks")
    pdf.bullet("Recognized when: legal/constructive obligation from past event + future cash outflows can be reliably estimated")
    pdf.bullet("Measured at present value unless discounting is immaterial")
    pdf.bullet("Recognition threshold: **>50% probability**")
    pdf.bullet("**Contingent assets/liabilities**: Possible rights/obligations confirmed only by uncertain future events not fully within the company's control")

    # ===== KEY ACCOUNTING JUDGMENTS =====
    pdf.section_title("Key Accounting Judgments and Estimates (Nestle)")
    pdf.body_text("Areas requiring higher degree of judgment and estimation:")
    pdf.bullet("Assessment of control and fair value in business combinations/disposals")
    pdf.bullet("Recognition and estimation of revenue")
    pdf.bullet("Identification of lease and lease term")
    pdf.bullet("Identification of CGUs and estimation of recoverable amounts for impairment tests")
    pdf.bullet("Assessment of useful lives of intangible assets (finite vs indefinite)")
    pdf.bullet("Measurement of employee benefit obligations")
    pdf.bullet("Recognition and measurement of provisions")
    pdf.bullet("Estimation of current and deferred taxes, including uncertain tax positions")

    # ===== CHAPTER 6: STATEMENT OF CASH FLOWS =====
    pdf.add_page()
    pdf.chapter_title("CHAPTER 6: STATEMENT OF CASH FLOWS")

    pdf.section_title("6.1 Introduction: Why Cash Flow Matters")
    pdf.body_text("Profit must not automatically result in more cash. The statement of cash flows complements the P&L with the 'cash is king' perspective. It shows where cash comes from and where it goes.")

    pdf.key_concept_box("Structure of the Statement of Cash Flows",
        "Cash flow from operating activities + Cash flow from investing activities + "
        "Cash flow from financing activities +/- Currency effects = Change in cash and cash equivalents")

    pdf.section_title("6.2 Cash Flow from Operating Activities")
    pdf.body_text("Two methods can be used to calculate operating cash flow:")

    pdf.subsection_title("Direct Method")
    pdf.body_text("Starts from actual cash receipts and payments:")
    pdf.bullet("(+) Cash receipts from sales of goods/services")
    pdf.bullet("(+) Cash receipts from fees, commissions, other earnings")
    pdf.bullet("(-) Cash payments to suppliers (COGS)")
    pdf.bullet("(-) Cash payments to/for employees")
    pdf.bullet("(-) Cash payments for other operating expenses")
    pdf.bullet("(+/-) Interest, dividends, and taxes (optional placement)")
    pdf.formula_block(r"= \mathbf{Cash Flow from Operating Activities (Direct)}", fontsize=12)
    pdf.body_text("Advantage: Offers additional information (cash-effective income and expenses). Disadvantage: Requires separate data collection, significant effort.")

    pdf.subsection_title("Indirect Method")
    pdf.body_text("Starts from EBIT and adjusts for non-cash items and working capital changes:")
    pdf.formula_block(r"\text{EBIT}", fontsize=12)
    pdf.formula_block(r"+ \text{Depreciation \& Impairments (non-cash expense)}", fontsize=11)
    pdf.formula_block(r"+ \text{Increase in provisions (non-cash expense)}", fontsize=11)
    pdf.formula_block(r"- \text{Extraordinary gains (non-cash revenue)}", fontsize=11)
    pdf.formula_block(r"\pm \text{Changes in operating working capital:}", fontsize=11)
    pdf.bullet("(-) Increase in accounts receivable (funds commitment)")
    pdf.bullet("(-) Increase in inventories (funds commitment)")
    pdf.bullet("(+) Increase in accounts payable (source of funds)")
    pdf.formula_block(r"\pm \text{Interest, dividends, taxes}", fontsize=11)
    pdf.formula_block(r"= \mathbf{Cash Flow from Operating Activities (Indirect)}", fontsize=12)
    pdf.body_text("Advantage: Minimal effort, uses information from existing financial reporting. Disadvantage: Companies can define it differently, making comparison difficult.")

    pdf.subsection_title("Example: Nestle 2024 Operating Cash Flow (Indirect)")
    w_item4 = 80
    w_v24 = 35
    w_v23 = 35
    widths4 = [w_item4, w_v24, w_v23]
    if pdf.get_y() + 90 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["CHF millions", "2024", "2023"], widths4)
    pdf.table_row(["Operating profit (EBIT)", "14,724", "14,063"], widths4, fill=True)
    pdf.table_row(["Depreciation and amortization", "3,582", "3,458"], widths4)
    pdf.table_row(["Impairment", "580", "647"], widths4, fill=True)
    pdf.table_row(["Other non-cash items", "(167)", "303"], widths4)
    pdf.table_row(["CF before WC changes", "18,719", "18,471"], widths4, fill=True)
    pdf.table_row(["Working capital changes", "1,208", "1,134"], widths4)
    pdf.table_row(["Other operating assets/liab.", "(334)", "(425)"], widths4, fill=True)
    pdf.table_row(["Cash from operations", "19,593", "19,180"], widths4)
    pdf.table_row(["Interest paid", "(1,539)", "(1,330)"], widths4, fill=True)
    pdf.table_row(["Interest/dividends received", "273", "193"], widths4)
    pdf.table_row(["Taxes paid", "(2,411)", "(2,801)"], widths4, fill=True)
    pdf.table_row(["Dividends from associates/JV", "759", "699"], widths4)
    pdf.table_row(["Operating cash flow", "16,675", "15,941"], widths4, fill=True)
    pdf.ln(2)

    # ===== ON AG CASH FLOW CASE =====
    pdf.add_page()
    pdf.section_title("Case Study: On AG -- Negative Operating Cash Flow Despite Profit")
    pdf.body_text("On AG's IPO year (9 months ended Sep 30, 2021) illustrates the disconnect between profit and cash:")
    pdf.bullet("Net income: CHF 16.8M (positive)")
    pdf.bullet("But: trade receivables increased CHF 51.2M, inventories increased CHF 40.9M (growth requires WC)")
    pdf.bullet("**Cash flow from operating activities: CHF (8.5M)** -- negative despite profit!")
    pdf.bullet("Financed by IPO: Cash flow from financing = CHF 609M (one-time event)")

    pdf.body_text("One year later (9 months ended Sep 30, 2022), the situation worsened:")
    pdf.bullet("Net income: CHF 84.1M (higher profit)")
    pdf.bullet("But: receivables grew CHF 74.9M, inventories grew CHF 123M")
    pdf.bullet("**Cash flow from operating activities: CHF (157M)** -- even more negative!")
    pdf.bullet("**Total change in cash: CHF (196M)** -- burning through IPO cash")

    pdf.key_concept_box("Key Lesson: Profit Does Not Equal Cash",
        "A fast-growing company can be profitable but cash-negative because growth requires "
        "building up inventories and receivables (working capital investment). An IPO provides "
        "a one-time cash injection, but the underlying operating cash flow must eventually turn positive.")

    pdf.slide_figure(SLIDES, 30,
        'Figure: On AG 2021 Cash Flow Statement -- negative operating CF despite >50% sales growth')

    # ===== INVESTING CASH FLOW =====
    pdf.section_title("6.3 Cash Flow from Investing Activities")
    pdf.body_text("Always calculated using the direct method:")
    pdf.bullet("(+) Cash receipts from sales of PPE, intangibles, and other long-term assets")
    pdf.bullet("(+) Cash receipts from sale of subsidiaries (less relinquished cash)")
    pdf.bullet("(+) Cash receipts from other investments")
    pdf.bullet("(-) Payments for acquisition of PPE, intangibles, long-term assets")
    pdf.bullet("(-) Payments for acquisition of subsidiaries (less cash acquired)")
    pdf.bullet("(-) Payments for other investments")

    pdf.key_concept_box("Interpreting Investing Cash Flow",
        "For large companies, negative investing CF is normal (replacement investment + acquisitions). "
        "A positive CF from investing typically indicates restructuring or asset disposal.")

    pdf.subsection_title("Example: Nestle 2024 Investing Cash Flow")
    if pdf.get_y() + 55 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["CHF millions", "2024", "2023"], widths4)
    pdf.table_row(["Capital expenditure", "(5,638)", "(5,714)"], widths4, fill=True)
    pdf.table_row(["Intangible assets", "(325)", "(489)"], widths4)
    pdf.table_row(["Acquisition of businesses", "(809)", "(211)"], widths4, fill=True)
    pdf.table_row(["Disposal of businesses", "(23)", "215"], widths4)
    pdf.table_row(["Investments in associates/JV", "(532)", "(582)"], widths4, fill=True)
    pdf.table_row(["Treasury investments", "(1,251)", "(80)"], widths4)
    pdf.table_row(["Other investing", "(46)", "665"], widths4, fill=True)
    pdf.table_row(["Investing cash flow", "(8,624)", "(6,196)"], widths4)
    pdf.ln(2)

    # ===== FINANCING CASH FLOW =====
    pdf.section_title("6.4 Cash Flow from Financing Activities")
    pdf.body_text("Always calculated using the direct method:")
    pdf.bullet("(+) Cash receipts from issuance of equity instruments (e.g., IPO, capital increase)")
    pdf.bullet("(+) Cash receipts from assumption of financial liabilities (new bonds, loans)")
    pdf.bullet("(-) Outflows for repayment of financial liabilities (bonds, loans maturing)")
    pdf.bullet("(-) Outflows for repayment of capital to shareholders (buybacks)")
    pdf.bullet("(-) Lease liability payments")
    pdf.bullet("(-) Dividend payments")

    pdf.subsection_title("Example: Nestle 2023 Financing Cash Flow")
    if pdf.get_y() + 55 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["CHF millions", "2023", "2022"], widths4)
    pdf.table_row(["Dividend paid (parent)", "(7,816)", "(7,829)"], widths4, fill=True)
    pdf.table_row(["Dividends paid (NCI)", "(174)", "(323)"], widths4)
    pdf.table_row(["Purchase of treasury shares", "(4,678)", "(5,234)"], widths4, fill=True)
    pdf.table_row(["Inflows from bonds/LT debt", "7,992", "9,806"], widths4)
    pdf.table_row(["Outflows bonds/leases/LT debt", "(5,055)", "(3,589)"], widths4, fill=True)
    pdf.table_row(["Short-term financial debt", "2,396", "(2,537)"], widths4)
    pdf.table_row(["Financing cash flow", "(7,362)", "(9,758)"], widths4, fill=True)
    pdf.ln(2)
    pdf.body_text("Note: Inflows from issuing new bonds and outflows for maturing bonds apply simultaneously.")

    # ===== FREE CASH FLOW =====
    pdf.add_page()
    pdf.section_title("6.5 Free Cash Flow (FCF)")
    pdf.body_text("Free cash flow indicates how much flexibility a company had during the year to decide on its future and ventures.")

    pdf.formula_block(r"\text{Free Cash Flow} = \text{CF from Operating} + \text{CF from Investing} - \text{Minimum Dividend}", fontsize=12)

    pdf.key_concept_box("FCF Is Not Regulated",
        "FCF is currently NOT regulated by IFRS, US GAAP, or Swiss GAAP FER. Companies may "
        "choose different calculations. FCF uses known positions but compares them to indicate "
        "financial flexibility. Often used as an indication for next year (if business is stable).")

    pdf.subsection_title("Example: Nestle FCF 2024")
    w_item5 = 75
    w_v5a = 35
    w_v5b = 35
    widths5 = [w_item5, w_v5a, w_v5b]
    pdf.table_header(["CHF millions", "2024", "2023"], widths5)
    pdf.table_row(["Operating cash flow", "16,675", "15,941"], widths5, fill=True)
    pdf.table_row(["Capital expenditure", "(5,638)", "(5,714)"], widths5)
    pdf.table_row(["Intangible assets", "(325)", "(489)"], widths5, fill=True)
    pdf.table_row(["Other investing", "(46)", "665"], widths5)
    pdf.table_row(["Free cash flow", "10,666", "10,403"], widths5, fill=True)
    pdf.ln(2)

    pdf.subsection_title("Example: Geberit FCF 2024 (Different Calculation)")
    pdf.table_header(["MCHF", "2024", "2023"], widths5)
    pdf.table_row(["Net cash from operations", "847.6", "857.9"], widths5, fill=True)
    pdf.table_row(["Purchase/sale PPE & intangibles", "(188.9)", "(193.0)"], widths5)
    pdf.table_row(["Lease repayments", "(16.5)", "(16.7)"], widths5, fill=True)
    pdf.table_row(["Interest & financing costs", "(29.2)", "(22.9)"], widths5)
    pdf.table_row(["Free cashflow", "613.0", "625.3"], widths5, fill=True)
    pdf.ln(2)
    pdf.body_text("Note: Geberit includes lease repayments and interest in FCF; Nestle does not. This shows why cross-company FCF comparison requires caution.")

    pdf.subsection_title("FCF Decision Tree")
    pdf.body_text("What to do with free cash flow:")
    pdf.bullet("**Positive FCF** -> Options: repay debt, invest in new businesses, buy back shares, increase dividends, increase cash reserves ('war chest')")
    pdf.bullet("**Negative FCF** -> Options: increase equity (capital increase) or take on new debt")
    pdf.body_text("These decisions appear in the cash flow from financing activities. Cash flow should never be evaluated for just one year -- always look at 3 to 5 years.")

    # ===== PART 3: PROFIT EFFECT VS CASH EFFECT =====
    pdf.add_page()
    pdf.chapter_title("PROFIT EFFECT VS CASH EFFECT")

    pdf.section_title("Timing Differences")
    pdf.body_text("Profit effect and cash effect may apply in different periods. Understanding when each occurs is critical:")

    w_event = 35
    w_pl = 40
    w_sfp = 40
    w_cf = 35
    widths6 = [w_event, w_pl, w_sfp, w_cf]
    pdf.table_header(["Event", "P&L Effect", "SFP Effect", "Cash Flow"], widths6)
    pdf.table_row(["Purchase (invoice)", "No effect", "+Inventory, +Payables", "No effect"], widths6, fill=True)
    pdf.table_row(["Pay supplier", "No effect", "-Cash, -Payables", "Cash outflow"], widths6)
    pdf.table_row(["Sale (invoice)", "Profit recognized", "+Receivables, -Inv.", "No effect"], widths6, fill=True)
    pdf.table_row(["Customer pays", "No effect", "+Cash, -Receivables", "Cash inflow"], widths6)
    pdf.ln(2)

    pdf.key_concept_box("Key Insight",
        "Profit is recognized when goods are sold (delivery), not when cash is received. "
        "Cash moves when payments are made/received. These events occur at different times. "
        "The indirect CF method reconciles EBIT back to actual cash by adjusting for these timing differences.")

    pdf.section_title("Worked Example: Trend Ltd.")
    pdf.body_text("Trend Ltd. trades shirts. Three transactions:")
    pdf.bullet("Aug 30, 2023: Receives shirts from supplier for CHF 100,000 (invoice)")
    pdf.bullet("Sep 29, 2023: Pays the invoice by bank transfer")
    pdf.bullet("Oct 30, 2023: Sells all shirts to customer for CHF 150,000 (invoice)")
    pdf.ln(2)

    w_date = 25
    w_pos = 40
    w_pnl = 45
    w_cash = 40
    widths7 = [w_date, w_pos, w_pnl, w_cash]
    pdf.table_header(["Date", "Financial Pos.", "Profit/Loss", "Cash Flow"], widths7)
    pdf.table_row(["Aug 30", "+Pay 100, +Inv 100", "(nothing)", "(nothing)"], widths7, fill=True)
    pdf.table_row(["Sep 29", "-Cash 100, -Pay 100", "(nothing)", "Oper. -100"], widths7)
    pdf.table_row(["Oct 30", "+Rec 150, -Inv 100", "Sales +150, Exp -100", "(nothing)"], widths7, fill=True)
    pdf.ln(2)
    pdf.body_text("Profit of CHF 50,000 is recognized in October (when goods are sold), but cash outflow of CHF 100,000 occurred in September. The cash inflow from the customer has not yet occurred.")

    # ===== INTERCONNECTION OF STATEMENTS =====
    pdf.section_title("Interconnection of All Financial Statements")
    pdf.body_text("All five financial statements are connected:")
    pdf.bullet("**P&L**: Revenue - Costs = Profit")
    pdf.bullet("**Statement of OCI**: Profit + Other comprehensive income = Comprehensive income")
    pdf.bullet("**Statement of Changes in Equity**: Comprehensive income + Transactions with shareholders = Change in equity")
    pdf.bullet("**Statement of Cash Flows**: Operating + Investing + Financing = Change in cash")
    pdf.bullet("Both change in cash and change in equity feed into the **SFP**: Cash + Other assets = Liabilities + Equity")
    pdf.bullet("**Notes** provide explanations and details for all statements")

    pdf.slide_figure(SLIDES, 46,
        'Figure: Interconnection of all five financial statements -- how P&L, OCI, equity, cash flows, and SFP relate')

    # ===== STATEMENT OF COMPREHENSIVE INCOME =====
    pdf.add_page()
    pdf.section_title("Statement of Comprehensive Income (Nestle 2024)")
    pdf.body_text("OCI represents 'shortly expected profit or loss' -- items where the effective P&L impact may change before settlement.")

    w_oci_item = 80
    w_oci24 = 35
    w_oci23 = 35
    widths_oci = [w_oci_item, w_oci24, w_oci23]
    pdf.table_header(["CHF millions", "2024", "2023"], widths_oci)
    pdf.table_row(["Profit for the year", "11,174", "11,509"], widths_oci, fill=True)
    pdf.table_row(["Currency retranslations", "798", "(4,154)"], widths_oci)
    pdf.table_row(["Cash flow hedge reserves", "895", "194"], widths_oci, fill=True)
    pdf.table_row(["Share of OCI from associates", "14", "(197)"], widths_oci)
    pdf.table_row(["May-be-reclassified items", "1,707", "(4,157)"], widths_oci, fill=True)
    pdf.table_row(["Defined benefit remeasurement", "318", "(623)"], widths_oci)
    pdf.table_row(["Equity instrument fair value", "33", "163"], widths_oci, fill=True)
    pdf.table_row(["Never-reclassified items", "576", "(500)"], widths_oci)
    pdf.table_row(["Other comprehensive income", "2,283", "(4,657)"], widths_oci, fill=True)
    pdf.table_row(["Total comprehensive income", "13,457", "6,852"], widths_oci)
    pdf.ln(2)
    pdf.body_text("Example: If a USD payment on Jan 15 is hedged, the profit/loss from this hedge exists as of Dec 31, but the actual profit/loss may change until Jan 15 as exchange rates move. The Dec 31 value is 'theoretical' and goes in OCI.")

    # ===== STATEMENT OF CHANGES IN EQUITY =====
    pdf.section_title("Statement of Changes in Equity (Nestle 2024)")
    pdf.body_text("The statement shows how equity changes during the year:")
    pdf.bullet("Opening equity (Jan 1, 2024): CHF 36,387M")
    pdf.bullet("(+) Profit for the year: CHF 11,174M")
    pdf.bullet("(+) Other comprehensive income: CHF 2,283M")
    pdf.bullet("= Total comprehensive income: CHF 13,457M")
    pdf.bullet("(-) Dividends: CHF (7,990M)")
    pdf.bullet("(-) Treasury share movements: CHF (4,559M)")
    pdf.bullet("(+) Equity compensation plans: CHF 132M")
    pdf.bullet("= Total transactions with owners: CHF (12,601M)")
    pdf.bullet("Closing equity (Dec 31, 2024): CHF 36,693M")

    pdf.key_concept_box("Equity Growth Condition",
        "Equity increases when comprehensive income exceeds transactions with owners (dividends + buybacks). "
        "In 2024 Nestle: comprehensive income CHF 13,457M > owner transactions CHF 12,601M, so equity grew by CHF 306M.")

    # ===== EXAM PRACTICE =====
    pdf.add_page()
    pdf.chapter_title("EXAM PRACTICE QUESTIONS")

    pdf.section_title("Exercise 4.1 (8 points): Motor Ltd. -- Total Cost Approach")
    pdf.body_text("Motor Ltd. produced 1,500 cars, sold 1,300 at CHF 20,000 each. COGS per car = CHF 11,000.")

    w_dept = 30
    w_prod = 30
    w_admin = 30
    w_mkt = 30
    w_tot = 30
    widths8 = [w_dept, w_prod, w_admin, w_mkt, w_tot]
    pdf.table_header(["Expense (CHF)", "Production", "Admin", "Marketing", "Total"], widths8)
    pdf.table_row(["Material", "5,000,000", "1,000,000", "800,000", "6,800,000"], widths8, fill=True)
    pdf.table_row(["Personnel", "8,500,000", "3,700,000", "3,400,000", "15,600,000"], widths8)
    pdf.table_row(["Depreciation", "3,000,000", "300,000", "300,000", "3,600,000"], widths8, fill=True)
    pdf.table_row(["Total", "16,500,000", "5,000,000", "4,500,000", ""], widths8)
    pdf.ln(2)
    pdf.body_text("Additional: Interest paid CHF 1,000,000. Dividend CHF 500,000. Tax rate 30%.")

    pdf.subsection_title("Solution: Total Cost Approach")
    pdf.formula_block(r"\text{Revenue} = 1{,}300 \times 20{,}000 = 26{,}000{,}000", fontsize=12)
    pdf.formula_block(r"\Delta\text{Inventory} = (1{,}500 - 1{,}300) \times 11{,}000 = 2{,}200{,}000", fontsize=12)

    w_sol = 65
    w_amt = 40
    widths9 = [w_sol, w_amt]
    pdf.table_header(["Item", "Amount (M CHF)"], widths9)
    pdf.table_row(["Revenue", "26.00"], widths9, fill=True)
    pdf.table_row(["Change in inventory", "2.20"], widths9)
    pdf.table_row(["Material expenses", "(6.80)"], widths9, fill=True)
    pdf.table_row(["Personnel expenses", "(15.60)"], widths9)
    pdf.table_row(["Depreciation", "(3.60)"], widths9, fill=True)
    pdf.table_row(["EBIT", "2.20"], widths9)
    pdf.table_row(["Financial expenses", "(1.00)"], widths9, fill=True)
    pdf.table_row(["EBT", "1.20"], widths9)
    pdf.table_row(["Taxes (30%)", "(0.36)"], widths9, fill=True)
    pdf.table_row(["Profit of the period", "0.84"], widths9)
    pdf.ln(2)

    pdf.section_title("Exercise 4.2 (2 points): COGS vs Total Cost Differences")
    pdf.body_text("Four differences (0.5 points each):")
    pdf.bullet("(1) COGS structures by function (department); total cost by nature (cost type)")
    pdf.bullet("(2) COGS does not disclose total expense types; total cost does")
    pdf.bullet("(3) COGS discloses costs related to revenue; total cost includes inventory changes")
    pdf.bullet("(4) COGS allows gross profit margin calculation; total cost does not")

    pdf.section_title("Exercise 1.7 (6 points): David Harleyson -- Operating CF")
    pdf.body_text("Trades motorcycles. Purchased 40 at CHF 35,000 each, sold 35 at CHF 44,000 each.")

    pdf.subsection_title("Direct Method")
    pdf.formula_block(r"\text{Cash from sales} = 35 \times 44{,}000 = 1{,}540{,}000", fontsize=12)
    pdf.formula_block(r"\text{Cash paid} = 40 \times 35{,}000 = 1{,}400{,}000", fontsize=12)
    pdf.formula_block(r"\mathbf{CF from operations (direct)} = 1{,}540{,}000 - 1{,}400{,}000 = \mathbf{140,000}", fontsize=12)

    pdf.subsection_title("Indirect Method")
    pdf.formula_block(r"\text{Profit} = 35 \times (44{,}000 - 35{,}000) = 315{,}000", fontsize=12)
    pdf.formula_block(r"\text{Increase in inventory} = 5 \times 35{,}000 = -175{,}000", fontsize=12)
    pdf.formula_block(r"\mathbf{CF from operations (indirect)} = 315{,}000 - 175{,}000 = \mathbf{140,000}", fontsize=12)

    pdf.body_text("Both methods yield the same result. Direct provides more detail but requires more effort; indirect uses existing reporting data.")

    # ===== KEY TERMS =====
    pdf.add_page()
    pdf.chapter_title("SUMMARY OF KEY EQUATIONS AND TERMS")

    pdf.section_title("Key Equations")
    pdf.formula_block(r"\text{Gross Profit} = \text{Sales} - \text{COGS}", fontsize=12)
    pdf.formula_block(r"\text{EBIT} = \text{Gross Profit} - \text{Distribution} - \text{Admin} - \text{Other} \quad \text{(COGS method)}", fontsize=11)
    pdf.formula_block(r"\text{EBIT} = \text{Sales} + \Delta\text{Inv.} - \text{Mat.} - \text{Pers.} - \text{Depr.} - \text{Other} \quad \text{(Total cost)}", fontsize=11)
    pdf.formula_block(r"\text{EBT} = \text{EBIT} \pm \text{Financial Result}", fontsize=12)
    pdf.formula_block(r"\text{Profit} = \text{EBT} - \text{Taxes} + \text{Income from Associates}", fontsize=12)
    pdf.formula_block(r"\text{Comprehensive Income} = \text{Profit} + \text{OCI}", fontsize=12)
    pdf.formula_block(r"\text{FCF} = \text{CF Operating} + \text{CF Investing} - \text{Min. Dividend}", fontsize=12)
    pdf.formula_block(r"\text{CF Operating (indirect)} = \text{EBIT} + \text{D\&A} \pm \Delta\text{Provisions} \pm \Delta\text{WC} \pm \text{Int/Tax}", fontsize=11)

    pdf.section_title("Key Terms")
    terms = [
        ("Statement of Profit or Loss", "Shows revenue minus expenses = profit for the period"),
        ("COGS Method", "Expenses by function: production, distribution, admin, R&D"),
        ("Total Cost Method", "Expenses by nature: materials, personnel, depreciation"),
        ("Gross Profit", "Sales - COGS; only calculable under COGS method"),
        ("EBIT", "Earnings Before Interest and Taxes (operating profit)"),
        ("EBT", "Earnings Before Taxes = EBIT +/- financial result"),
        ("OCI", "Other Comprehensive Income: unrealized gains/losses outside P&L"),
        ("IFRS 15", "Revenue recognition: 5-step model, recognize at delivery"),
        ("ECL (IFRS 9)", "Expected Credit Loss model for trade receivable impairment"),
        ("Statement of Cash Flows", "Operating + Investing + Financing = Change in cash"),
        ("Direct Method", "CF from actual cash receipts/payments; more detail, more effort"),
        ("Indirect Method", "CF from EBIT adjusted for non-cash + WC; less effort"),
        ("Operating CF", "Cash generated by core business operations"),
        ("Investing CF", "Cash for/from long-term assets; normally negative for large companies"),
        ("Financing CF", "Cash from/for equity and debt; dividends, buybacks, bond issuance"),
        ("Free Cash Flow (FCF)", "CF operating + CF investing - min dividend; not IFRS-regulated"),
        ("Working Capital", "Receivables + Inventories - Payables; ties up cash"),
        ("Accrual vs Cash", "Profit when sold (accrual); cash when paid/received"),
        ("Associates", "Subsidiaries owned <50%; income reported separately"),
        ("Non-Controlling Interests", "Minority shareholders' portion of profit/equity"),
    ]

    w_term = 55
    w_def = 105
    widths_t = [w_term, w_def]
    pdf.table_header(["Term", "Definition"], widths_t)
    for i, (term, defn) in enumerate(terms):
        pdf.table_row([term, defn], widths_t, fill=(i % 2 == 0))

    # Output
    output_dir = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/busadmin'
    output_path = os.path.join(output_dir, 'Lecture3_PnL_and_Cash_Flows.pdf')
    pdf.output(output_path)
    print(f"Generated: {output_path}")


if __name__ == '__main__':
    generate_lecture1()
    generate_lecture2()
    generate_lecture3()
