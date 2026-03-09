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


if __name__ == '__main__':
    generate_lecture1()
