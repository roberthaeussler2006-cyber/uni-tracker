#!/usr/bin/env python3
"""Generate PDF notes for Macroeconomics KW 8, 9, and 10."""

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
_FORMULA_DIR = tempfile.mkdtemp(prefix="macro_formulas_")
_FORMULA_COUNTER = 0

# Slide extraction directory
_SLIDE_DIR = tempfile.mkdtemp(prefix="macro_slides_")
_SLIDE_COUNTER = 0

# Base path for lecture slides
_SLIDES_BASE = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/econ/Lecture slides (reference for notes creation)'


def extract_slide(pdf_filename, page_num, crop_sidebar=True):
    """Extract a slide page from a lecture PDF as a cropped PNG image.

    Args:
        pdf_filename: Name of the PDF file (e.g., '2026-Economics-B_Folien-01.pdf')
        page_num: 1-based page number to extract
        crop_sidebar: If True, crop the right ~13% to remove green navigation sidebar

    Returns:
        Path to the extracted PNG image
    """
    global _SLIDE_COUNTER
    _SLIDE_COUNTER += 1
    pdf_path = os.path.join(_SLIDES_BASE, pdf_filename)
    output_prefix = os.path.join(_SLIDE_DIR, f"slide_{_SLIDE_COUNTER}")

    # Use pdftoppm to render the page at high resolution
    subprocess.run([
        'pdftoppm', '-png', '-r', '300',
        '-f', str(page_num), '-l', str(page_num),
        pdf_path, output_prefix
    ], check=True, capture_output=True)

    # pdftoppm names output as prefix-PAGENUMBER.png (zero-padded)
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
        # Crop right 13% (green sidebar) and bottom 3% (page number)
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
                transparent=False, facecolor='#F0F5FF')
    plt.close(fig)
    return path


class NotesPDF(FPDF):
    """Custom PDF class for generating study notes."""

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
        self.set_text_color(25, 60, 120)
        self.multi_cell(0, 12, self.title_text, align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, self.subtitle_text, align="C")
        self.ln(15)
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 7, "Blanchard - Macroeconomics, 7th Global Edition", align="C")
        self.ln(5)
        self.multi_cell(0, 7, "Study Notes", align="C")
        self.set_text_color(0, 0, 0)

    def chapter_title(self, text):
        self.ln(6)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(25, 60, 120)
        self.multi_cell(0, 9, text)
        self.set_draw_color(25, 60, 120)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def section_title(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(40, 90, 160)
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
        # Process bold markers
        self._write_rich_text(text, indent=0)
        self.ln(2)

    def bullet(self, text, level=0):
        indent = 8 + level * 8
        self.set_x(self.l_margin + indent)
        bullet_char = "-" if level == 0 else "  >"
        self.set_font("Helvetica", "", 10)
        w = self.w - self.l_margin - self.r_margin - indent
        self.cell(5, 5, bullet_char)
        self.set_x(self.l_margin + indent + 5)
        self._write_rich_text(text, indent=indent + 5)
        self.ln(1.5)

    def formula_block(self, latex, fontsize=14):
        """Render a LaTeX formula as an image and embed it centered."""
        self.ln(2)
        img_path = render_latex(latex, fontsize=fontsize)
        # Get image dimensions to scale properly
        from PIL import Image
        with Image.open(img_path) as img:
            w_px, h_px = img.size
        # Convert to mm at 200 dpi (1 inch = 25.4mm, 200 pixels = 1 inch)
        w_mm = w_px * 25.4 / 200
        h_mm = h_px * 25.4 / 200
        # Cap width to page width
        max_w = self.w - self.l_margin - self.r_margin - 20
        if w_mm > max_w:
            scale = max_w / w_mm
            w_mm *= scale
            h_mm *= scale
        # Check if we need a new page
        if self.get_y() + h_mm + 4 > self.h - self.b_margin:
            self.add_page()
        # Center the image
        x = self.l_margin + (self.w - self.l_margin - self.r_margin - w_mm) / 2
        self.image(img_path, x=x, y=self.get_y(), w=w_mm, h=h_mm)
        self.set_y(self.get_y() + h_mm + 2)
        self.set_font("Helvetica", "", 10)

    def slide_figure(self, pdf_filename, page_num, caption, width_pct=0.85):
        """Embed a lecture slide as a captioned figure.

        Args:
            pdf_filename: Lecture PDF filename
            page_num: 1-based page number
            caption: Caption text below the figure
            width_pct: Figure width as fraction of page width (0.0-1.0)
        """
        img_path = extract_slide(pdf_filename, page_num)
        from PIL import Image
        with Image.open(img_path) as img:
            w_px, h_px = img.size

        # Scale to desired width
        avail_w = (self.w - self.l_margin - self.r_margin) * width_pct
        w_mm = avail_w
        h_mm = (h_px / w_px) * w_mm

        # Check if we need a new page (image + caption + padding)
        needed = h_mm + 14
        if self.get_y() + needed > self.h - self.b_margin:
            self.add_page()

        self.ln(4)
        # Center the image
        x = self.l_margin + (self.w - self.l_margin - self.r_margin - w_mm) / 2
        self.image(img_path, x=x, y=self.get_y(), w=w_mm, h=h_mm)
        self.set_y(self.get_y() + h_mm + 2)

        # Caption (sanitize unicode for Helvetica)
        safe_caption = caption.replace('\u2014', '-').replace('\u2013', '-').replace('\u2019', "'")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 4, safe_caption, align="C")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 10)
        self.ln(3)

    def key_concept_box(self, title, text):
        self.ln(3)
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(200, 170, 80)
        x = self.l_margin + 5
        w = self.w - self.l_margin - self.r_margin - 10
        y_start = self.get_y()
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
        self.set_fill_color(25, 60, 120)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6, col, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)

    def table_row(self, cols, widths, fill=False):
        self.set_font("Helvetica", "", 9)
        if fill:
            self.set_fill_color(240, 245, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 5.5, col, border=1, fill=fill, align="C" if i > 0 else "L")
        self.ln()

    def _write_rich_text(self, text, indent=0):
        """Write text with **bold** markers converted to actual bold."""
        parts = re.split(r'(\*\*.*?\*\*)', text)
        w = self.w - self.l_margin - self.r_margin - indent
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


def generate_kw8():
    """Generate KW 8 PDF: Introduction & National Accounts (Ch 1 + Ch 2 + Lecture 1)."""
    pdf = NotesPDF("KW 8: Introduction & National Accounts", "Chapters 1 & 2 + Lecture 1")
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ===== LECTURE 1 CONTEXT =====
    pdf.add_page()
    pdf.chapter_title("LECTURE 1 CONTEXT: INTRODUCTION TO MACROECONOMICS")

    pdf.section_title("Course Overview and Learning Objectives")
    pdf.body_text("Economics studies the allocation of scarce resources. While microeconomics examines allocation at the individual level (persons, firms), macroeconomics discusses this at the aggregated level.")
    pdf.bullet("Learning objectives of this course:")
    pdf.bullet("Introductory understanding of macroeconomics", level=1)
    pdf.bullet("Economic models: benefits, applications, and limitations", level=1)
    pdf.bullet("Analysis and contextualization of current economic policy problems", level=1)
    pdf.bullet("Main goal: Ability to analyze current macroeconomic topics in a structured manner using suitable model frameworks")

    pdf.subsection_title("Importance of Macroeconomics for Managers")
    pdf.bullet("A company's success depends critically on **external** factors")
    pdf.bullet("Economic developments and economic policy decisions must be correctly interpreted by managers")
    pdf.bullet("Example: In which countries should a company produce? In which markets will demand increase?")

    pdf.subsection_title("Course Structure")
    pdf.bullet("12 lectures (90 min) + 8 tutorials (90 min) + 3 self-study units")
    pdf.bullet("Mock exam in the middle of the semester")
    pdf.bullet("Thematic structure: short term -> medium term -> long term")
    pdf.bullet("Perspective: demand-side -> supply-side")

    pdf.section_title("From Micro to Macro: The Linking of Markets")
    pdf.body_text("Economics distinguishes three levels of investigation:")
    pdf.bullet("**Individual economic level**: Behavior of individual economic entities; above all households (maximization of utility) and companies (maximization of profits)")
    pdf.bullet("**Level of interaction (markets)**: Relations and cooperation between economic entities")
    pdf.bullet("**Macroeconomic level**: Overall result of individual economic actions and the environment in which individual economic decisions are made")
    pdf.bullet("Modern macroeconomics is microeconomically sound, i.e., it is based on decisions of individual households and enterprises")

    pdf.subsection_title("Example 1: Immigration to Switzerland and Wages")
    pdf.bullet("Simple model with labor supply and demand: additional labor supply -> lower wages")
    pdf.bullet("Advanced model: immigrants bring new ideas, companies invest more, structural change occurs")
    pdf.bullet("From research: David Card (1990) 'Mariel boatlift' - natural experiment showing minimal wage effects from immigration")

    pdf.subsection_title("Example 2: European Real Estate Boom and Crash")
    pdf.bullet("Ireland, Latvia, and Spain experienced interconnected crises:")
    pdf.bullet("Housing prices doubled then crashed after 2008", level=1)
    pdf.bullet("Unemployment surged (above 15% in all three countries)", level=1)
    pdf.bullet("Public debt exploded as governments bailed out banks and funded stimulus", level=1)
    pdf.bullet("Key question: What connects these three charts? -> The macroeconomic perspective")

    pdf.slide_figure('2026-Economics-B_Folien-01.pdf', 19,
        'Figure: European Real Estate Crisis - Housing Prices, Unemployment, and Public Debt (Ireland, Latvia, Spain)')

    pdf.section_title("(Macro-)Economic Markets")
    pdf.body_text("Several markets are of central importance at the macroeconomic level:")
    pdf.bullet("**Goods market**")
    pdf.bullet("**Financial market** (including money and capital market)")
    pdf.bullet("**Labor market**")
    pdf.bullet("We are interested in the **general equilibrium** on all markets, as well as the interdependence of markets")
    pdf.bullet("Using suitable models, we want to analyze macroeconomic developments and possible political interventions")

    pdf.section_title("Central Economic Variables")
    pdf.body_text("A key learning objective is understanding the definition, determinants, and measurement of these variables:")
    pdf.bullet("(1) **The total production and its growth rate** -> GDP")
    pdf.bullet("(2) **The unemployment rate**")
    pdf.bullet("(3) **The rate of inflation**")

    pdf.section_title("Long-Term Trend and Short-Term Fluctuations")
    pdf.body_text("Swiss real GDP (in billion CHF, source: SECO) shows a long-term trend of approximately 1.5% growth per year, with short-term fluctuations around this trend.")
    pdf.bullet("What explains the short-term fluctuations and the return to the trend line?")
    pdf.bullet("What explains the long-term path of GDP?")
    pdf.bullet("These are the central questions of this course")

    pdf.slide_figure('2026-Economics-B_Folien-01.pdf', 7,
        'Figure: Swiss Real GDP (2000-2024) with 1.5% trend line (Source: SECO)')

    # CHAPTER 1
    pdf.add_page()
    pdf.chapter_title("CHAPTER 1: A TOUR OF THE WORLD")

    pdf.section_title("1-1 The Crisis")
    pdf.subsection_title("Pre-Crisis Period (2000-2007)")
    pdf.bullet("From 2000 to 2007, the world economy experienced a sustained expansion")
    pdf.bullet("Annual average world output growth was 4.5%")
    pdf.bullet("Advanced economies (~30 richest countries) grew at 2.7% per year")
    pdf.bullet("Other economies (~150 countries) grew even faster at 6.6% per year")

    pdf.subsection_title("Origins of the Crisis (2007-2008)")
    pdf.bullet("In 2007, signs emerged that the U.S. expansion was ending")
    pdf.bullet("U.S. housing prices, which had doubled since 2000, started declining")
    pdf.bullet("Two camps formed:")
    pdf.bullet("**Optimists**: Lower housing prices would reduce construction and consumer spending, but the Fed could lower interest rates to stimulate demand and avoid recession", level=1)
    pdf.bullet("**Pessimists**: The decrease in interest rates might not be enough; the U.S. might go through a short recession", level=1)
    pdf.bullet("The pessimists turned out to be not pessimistic enough")

    pdf.subsection_title("How Housing Became a Financial Crisis")
    pdf.bullet("Many mortgages given during the expansion were of poor quality")
    pdf.bullet("Borrowers had taken too large loans and could not make monthly payments")
    pdf.bullet("With declining housing prices, mortgage values often exceeded house prices, giving incentive to default")
    pdf.bullet("Banks had bundled mortgages into new securities (securitization), sold them to other banks, repackaged into further new securities")
    pdf.bullet("Banks held highly complex securities whose value was nearly impossible to assess")
    pdf.bullet("Banks became reluctant to lend to each other, fearing counterparties might not be able to repay")

    pdf.subsection_title("Figure 1-1: Output Growth Rates")
    pdf.bullet("Shows world output growth rates from 2000-2016")
    pdf.bullet("Advanced economies experienced sharp decline in 2008-2009 (negative growth)")
    pdf.bullet("Other economies slowed but maintained positive growth")
    pdf.bullet("Recovery was slow and uneven across regions")

    pdf.subsection_title("The Crisis Unfolds (2008-2009)")
    pdf.bullet("September 2008: Lehman Brothers went bankrupt - marked the worst phase of the crisis")
    pdf.bullet("Most major banks were highly leveraged and at risk")
    pdf.bullet("Stock markets crashed worldwide (U.S. stock index fell ~30%)")
    pdf.bullet("U.S. output growth was -3.0% in 2009")
    pdf.bullet("Advanced economies collectively contracted by -3.4% in 2009")
    pdf.bullet("World trade collapsed, spreading the crisis to countries that had not experienced housing booms")

    pdf.subsection_title("Policy Response and Recovery")
    pdf.bullet("Central banks cut interest rates to near zero")
    pdf.bullet("Governments implemented fiscal stimulus (increased spending, reduced taxes)")
    pdf.bullet("These measures prevented a repeat of the Great Depression")
    pdf.bullet("Recovery has been slow - called the 'Great Recession'")
    pdf.bullet("By 2010, positive growth returned but remained sluggish in advanced economies")

    pdf.section_title("1-2 The United States")
    pdf.body_text("The U.S. is the world's largest economy, accounting for about 22% of world output. Understanding U.S. macroeconomic performance is essential.")

    pdf.subsection_title("Key U.S. Macroeconomic Data (Table 1-1)")
    widths = [40, 25, 25, 25, 25]
    pdf.table_header(["", "2000-07", "2008-10", "2011-13", "2014-16"], widths)
    pdf.table_row(["Output growth %", "2.7", "-0.3", "2.0", "2.2"], widths, True)
    pdf.table_row(["Unempl. rate %", "5.0", "7.5", "8.3", "5.3"], widths)
    pdf.table_row(["Inflation rate %", "2.5", "1.6", "1.8", "1.1"], widths, True)
    pdf.table_row(["Interest rate %", "3.6", "1.6", "0.1", "0.1"], widths)
    pdf.ln(3)

    pdf.bullet("Output growth averaged 2.7% from 2000-2007, dropped to -0.3% during 2008-10, recovered to about 2% since 2011")
    pdf.bullet("Unemployment rate jumped from 5% pre-crisis to 7.5% during crisis, peaked at 10% in October 2009, slowly came down to around 5% by 2016")
    pdf.bullet("Inflation remained low and stable (under 2.5%), even during the crisis")
    pdf.bullet("The Fed cut the policy interest rate (federal funds rate) from about 3.6% to essentially 0% by 2009")

    pdf.subsection_title("Low Interest Rates and the Zero Lower Bound")
    pdf.bullet("The federal funds rate reached 0% in late 2008 and stayed near zero until 2015")
    pdf.bullet("This is the **zero lower bound** (ZLB) problem - interest rates cannot go below zero (or very slightly negative)")
    pdf.bullet("At the ZLB, conventional monetary policy becomes ineffective")
    pdf.bullet("The Fed turned to **unconventional monetary policy**: buying long-term bonds (quantitative easing/QE) to reduce long-term interest rates")

    pdf.subsection_title("How Worrisome Is Low Productivity Growth?")
    pdf.bullet("U.S. productivity growth has slowed since mid-2000s")
    pdf.bullet("Average annual productivity growth: 2.2% from 1996-2006, only 0.6% from 2006-2016")
    pdf.bullet("This is a major concern because productivity growth is the main driver of long-run improvements in living standards")
    pdf.bullet("Debate exists over whether this is temporary or a new normal:")
    pdf.bullet("**Pessimists** (e.g., Robert Gordon): major innovations are behind us, growth will remain low", level=1)
    pdf.bullet("**Optimists**: new technologies (AI, robotics) will eventually boost productivity; there is a lag between invention and productivity gains", level=1)

    pdf.section_title("1-3 The Euro Area")
    pdf.body_text("The euro area comprises the countries of the EU that have adopted the euro as their common currency. As of 2016, 19 countries, with a combined population of 340 million and combined output roughly equal to that of the United States.")

    pdf.subsection_title("Key Euro Area Macroeconomic Data (Table 1-2)")
    widths = [40, 25, 25, 25, 25]
    pdf.table_header(["", "2000-07", "2008-10", "2011-13", "2014-16"], widths)
    pdf.table_row(["Output growth %", "2.2", "-0.5", "0.3", "1.7"], widths, True)
    pdf.table_row(["Unempl. rate %", "8.4", "8.9", "10.8", "10.8"], widths)
    pdf.table_row(["Inflation rate %", "2.2", "1.5", "1.8", "0.4"], widths, True)
    pdf.table_row(["Interest rate %", "3.1", "2.1", "0.4", "0.0"], widths)
    pdf.ln(3)

    pdf.bullet("Pre-crisis growth was lower than the U.S. (2.2% vs 2.7%)")
    pdf.bullet("The crisis hit the Euro area harder and longer - growth was only 0.3% during 2011-2013")
    pdf.bullet("The Euro area experienced a **double-dip recession** - second downturn in 2011-12")
    pdf.bullet("Unemployment remained very high at 10.8% even during 2014-16")
    pdf.bullet("The ECB (European Central Bank) also cut rates to near zero")
    pdf.bullet("Inflation dropped to very low levels (0.4%), raising concerns about deflation")

    pdf.subsection_title("Can European Unemployment Be Reduced?")
    pdf.bullet("European unemployment has been structurally higher than U.S. unemployment for decades")
    pdf.bullet("Some argue this reflects rigid labor markets (strong worker protections, high minimum wages, generous unemployment benefits)")
    pdf.bullet("Others point to insufficient demand (the demand-side explanation)")
    pdf.bullet("Reality: both supply-side (structural) and demand-side factors play a role")
    pdf.bullet("Different Euro area countries have very different unemployment rates:")
    pdf.bullet("Germany: around 4% (well below the Euro average)", level=1)
    pdf.bullet("Spain and Greece: above 20% during the crisis", level=1)

    pdf.subsection_title("What Has the Euro Done for Its Members?")
    pdf.bullet("The euro was introduced in 1999 (notes and coins in 2002)")
    pdf.bullet("**Benefits**: elimination of exchange rate uncertainty, lower transaction costs for trade, potentially lower interest rates for some countries")
    pdf.bullet("**Costs**: loss of independent monetary policy - each country cannot set its own interest rate")
    pdf.bullet("When a country-specific shock hits, it cannot devalue its currency or lower its own interest rate")
    pdf.bullet("The crisis exposed tensions: countries like Greece, Ireland, Portugal, Spain faced sovereign debt crises")
    pdf.bullet("Debate continues about whether the euro area is an **optimal currency area** - whether the benefits outweigh the costs of sharing a single monetary policy")

    pdf.section_title("1-4 China")
    pdf.body_text("China's rapid economic growth over the past 40 years has transformed it into one of the world's largest economies.")

    pdf.subsection_title("Key China Macroeconomic Data (Table 1-3)")
    widths = [40, 25, 25, 25, 25]
    pdf.table_header(["", "2000-07", "2008-10", "2011-13", "2014-16"], widths)
    pdf.table_row(["Output growth %", "10.5", "9.9", "8.2", "6.8"], widths, True)
    pdf.table_row(["Inflation rate %", "1.7", "3.0", "3.1", "1.7"], widths)
    pdf.ln(3)

    pdf.bullet("China's growth has been extraordinary: averaging 10.5% from 2000-07")
    pdf.bullet("Growth has slowed from 10.5% to 6.8% - but this is still very high by world standards")
    pdf.bullet("China's GDP in purchasing power parity (PPP) terms is now larger than the U.S.")
    pdf.bullet("However, per capita income is still about 1/4 of U.S. levels (PPP-adjusted)")
    pdf.bullet("At market exchange rates, China's GDP is about 60% of U.S. GDP")

    pdf.subsection_title("Key Issues for China")
    pdf.bullet("**Rebalancing growth**: China's growth has been driven by investment (45% of GDP) and exports; needs to shift toward consumption")
    pdf.bullet("**Shadow banking**: Large financial sector outside traditional banking, with less regulation and potentially risky lending")
    pdf.bullet("**Exchange rate management**: China has maintained a partly managed exchange rate, keeping the yuan relatively weak to boost exports")
    pdf.bullet("**Inequality**: Growing income inequality between urban and rural areas, and between coastal and inland regions")
    pdf.bullet("**Environmental costs**: Rapid industrialization has caused severe pollution and environmental degradation")

    pdf.section_title("1-5 Looking Ahead")
    pdf.body_text("The book is organized around a core set of chapters that provide the fundamental framework for thinking about macroeconomics, with extensions that build on the core.")
    pdf.bullet("The core covers: the goods market, financial markets, the IS-LM model, the labor market, the Phillips curve, and the IS-LM-PC model")
    pdf.bullet("Extensions cover: expectations, the open economy, and policy")
    pdf.bullet("Each extension enriches the basic model to address more realistic and complex questions")

    pdf.subsection_title("Appendix: Where to Find the Numbers")
    pdf.bullet("Key data sources for macroeconomic statistics:")
    pdf.bullet("**National sources**: Bureau of Economic Analysis (BEA) for U.S. GDP data, Bureau of Labor Statistics (BLS) for employment/inflation data", level=1)
    pdf.bullet("**International organizations**: IMF (World Economic Outlook), OECD, World Bank", level=1)
    pdf.bullet("**Central banks**: Federal Reserve (FRED database), ECB", level=1)
    pdf.bullet("The FRED database (Federal Reserve Bank of St. Louis) is particularly useful: free, comprehensive, with easy-to-use graphing tools")

    # CHAPTER 2
    pdf.add_page()
    pdf.chapter_title("CHAPTER 2: A TOUR OF THE BOOK")

    pdf.section_title("2-1 Aggregate Output")
    pdf.body_text("GDP is the single most important measure of the overall level of economic activity.")

    pdf.subsection_title("GDP: Production and Income")
    pdf.bullet("There are three equivalent ways to think about GDP:")
    pdf.bullet("(1) **From the production side**: GDP is the value of the final goods and services produced in the economy during a given period", level=1)
    pdf.bullet("(2) **From the income side**: GDP is the sum of incomes in the economy during a given period", level=1)
    pdf.bullet("(3) **From the expenditure side**: GDP is the value of final goods and services purchased during a given period", level=1)

    pdf.subsection_title("Key Definitions")
    pdf.key_concept_box("Final vs. Intermediate Goods",
        "Final goods: goods destined for final consumption.\n"
        "Intermediate goods: used in the production of final goods.\n"
        "GDP counts only final goods to avoid double-counting.\n"
        "Value added by a firm = value of production - value of intermediate goods used.")

    pdf.bullet("**GDP = sum of value added by all firms in the economy** (equivalently, the value of all final goods)")
    pdf.bullet("Why production equals income: A firm's value added goes to pay workers (wages) or remains as profit to the firm. So the value added is distributed as income.")
    pdf.bullet("Hence: **aggregate production = aggregate income**")

    pdf.subsection_title("Nominal and Real GDP")
    pdf.bullet("**Nominal GDP** = sum of quantities of final goods x their current prices. Also called GDP in current dollars or GDP at current prices.")
    pdf.bullet("Nominal GDP can increase either because production increases or because prices increase")
    pdf.bullet("**Real GDP** = sum of quantities of final goods x constant prices (base year prices). Also called GDP in constant dollars, GDP adjusted for inflation, or GDP in terms of goods.")
    pdf.bullet("Real GDP is constructed using a reference year's prices, so changes in real GDP reflect only changes in quantities, not prices")

    pdf.key_concept_box("Nominal vs Real GDP - Example",
        "Economy produces only cars:\n"
        "Year 1: 10 cars at $20,000 each -> Nominal GDP = $200,000\n"
        "Year 2: 12 cars at $22,000 each -> Nominal GDP = $264,000\n"
        "Real GDP (Year 1 prices): Year 2 = 12 x $20,000 = $240,000\n"
        "Nominal GDP growth: 32%. Real GDP growth: 20%.")

    pdf.bullet("The Bureau of Economic Analysis (BEA) constructs real GDP using 2009 as the reference year")
    pdf.bullet("U.S. real GDP in 2014: $16.2 trillion (2009 dollars). Nominal GDP in 2014: $17.3 trillion")
    pdf.bullet("**GDP growth rate**: the rate of change of real GDP. Positive = expansion. Negative = recession.")

    pdf.subsection_title("GDP: Level versus Growth Rate")
    pdf.bullet("Both the level and the growth rate of real GDP are important:")
    pdf.bullet("**Level of real GDP** (relative to population): determines the standard of living", level=1)
    pdf.bullet("**Growth rate of real GDP**: determines whether the standard of living is rising or falling", level=1)
    pdf.bullet("An economy can have a high level of GDP but low growth (e.g., Japan), or a lower level but high growth (e.g., China)")

    pdf.key_concept_box("Expansions and Recessions",
        "Expansion: period of positive GDP growth.\n"
        "Recession: period of negative GDP growth.\n"
        "U.S. convention (NBER): A recession requires at least two consecutive\n"
        "quarters of negative GDP growth, plus a significant decline in activity.")

    pdf.section_title("2-2 The Unemployment Rate")
    pdf.subsection_title("Definitions")
    pdf.bullet("**Employment (N)**: the number of people who have a job")
    pdf.bullet("**Unemployment (U)**: the number of people who do not have a job but are looking for one")
    pdf.bullet("**Labor force (L)**: employment + unemployment:")
    pdf.formula_block(r"L = N + U", fontsize=12)
    pdf.bullet("**Unemployment rate (u)**: the ratio of unemployed to the labor force:")
    pdf.formula_block(r"u = \frac{U}{L}", fontsize=12)
    pdf.bullet("**Out of the labor force**: people who are neither employed nor looking for work (e.g., retirees, students, discouraged workers)")
    pdf.bullet("**Participation rate**: the ratio of the labor force to the total working-age population")

    pdf.subsection_title("Why Do Economists Care about Unemployment?")
    pdf.bullet("Unemployment represents wasted productive resources - people who want to work but cannot find a job")
    pdf.bullet("It directly affects the welfare of the unemployed: loss of income, psychological distress")
    pdf.bullet("It signals the overall state of the economy: high unemployment = weak economy")
    pdf.bullet("A very low unemployment rate can also be a concern - it may signal an overheating economy and rising inflation")

    pdf.key_concept_box("Okun's Law",
        "There is a reliable negative relationship between GDP growth\n"
        "and changes in the unemployment rate:\n"
        "High output growth -> decreasing unemployment\n"
        "Low/negative output growth -> increasing unemployment")

    pdf.section_title("2-3 The Inflation Rate")
    pdf.subsection_title("The GDP Deflator")
    pdf.bullet("**Inflation**: a sustained rise in the general level of prices (the price level)")
    pdf.bullet("**Inflation rate**: the rate at which the price level increases")
    pdf.bullet("**Deflation**: a sustained decline in the price level (negative inflation)")
    pdf.bullet("The **GDP deflator** is defined as:")
    pdf.formula_block(r"\text{GDP Deflator} = \frac{\text{Nominal GDP}}{\text{Real GDP}}", fontsize=12)
    pdf.bullet("It is an index number: equal to 1 (or 100) in the base year")
    pdf.bullet("The GDP deflator gives the average price of output - the final goods produced in the economy")

    pdf.subsection_title("The Consumer Price Index (CPI)")
    pdf.bullet("The **CPI** measures the cost of living - the cost of a given basket of consumer goods")
    pdf.bullet("The GDP deflator and CPI generally move together but can differ because:")
    pdf.bullet("The GDP deflator covers all goods produced domestically; the CPI covers goods consumed (including imports)", level=1)
    pdf.bullet("The GDP deflator uses changing weights; the CPI uses a fixed basket", level=1)

    pdf.subsection_title("Why Do Economists Care about Inflation?")
    pdf.bullet("If all prices and wages rose proportionally, inflation would be irrelevant")
    pdf.bullet("In reality, inflation matters because:")
    pdf.bullet("Not all prices and wages rise proportionally - inflation changes relative prices and redistributes income", level=1)
    pdf.bullet("Inflation creates uncertainty about future prices, making planning harder", level=1)
    pdf.bullet("Inflation interacts with the tax system (e.g., capital gains taxes on nominal gains)", level=1)
    pdf.bullet("**Very high inflation** (hyperinflation) is extremely disruptive to the economy")
    pdf.bullet("**Deflation** is also problematic: increases the real burden of debt, and interacts with the zero lower bound on interest rates")

    pdf.section_title("2-4 Output, Unemployment, and the Inflation Rate: Okun's Law and the Phillips Curve")

    pdf.subsection_title("Okun's Law")
    pdf.bullet("**Okun's Law**: Above-average output growth leads to a decrease in the unemployment rate; below-average growth leads to an increase")
    pdf.bullet("Quantitative relationship (for the U.S.): A 1 percentage point increase in GDP growth above normal leads to about a 0.4 percentage point decrease in unemployment")
    pdf.bullet("This means that to significantly reduce unemployment, you need sustained above-average GDP growth")
    pdf.bullet("Figure 2-3 plots changes in unemployment vs. GDP growth for the U.S. (1960-2014) - the negative relationship is clear")

    pdf.subsection_title("The Phillips Curve")
    pdf.bullet("**The Phillips Curve**: a relationship between unemployment and inflation")
    pdf.bullet("When unemployment is **below** a certain level (the natural rate), inflation tends to **increase**")
    pdf.bullet("When unemployment is **above** the natural rate, inflation tends to **decrease**")
    pdf.bullet("The 'natural rate of unemployment' is the unemployment rate at which inflation remains stable")
    pdf.bullet("This creates a policy trade-off: reducing unemployment below the natural rate causes inflation to rise")
    pdf.bullet("Figure 2-4 plots changes in inflation vs. unemployment for the U.S. - the negative relationship is visible")

    pdf.section_title("2-5 The Short Run, the Medium Run, and the Long Run")
    pdf.body_text("Macroeconomists think about economic fluctuations at three time horizons:")

    pdf.subsection_title("The Short Run (Year to Year)")
    pdf.bullet("Focus on movements in output, unemployment, and inflation from year to year")
    pdf.bullet("Key assumption: prices are sticky (slow to adjust)")
    pdf.bullet("Demand plays a central role: changes in demand lead to changes in output")
    pdf.bullet("Monetary and fiscal policy have powerful effects on output")
    pdf.bullet("Models used: IS-LM framework (Chapters 3-6)")

    pdf.subsection_title("The Medium Run (About a Decade)")
    pdf.bullet("Over the medium run, the economy tends to return to a 'normal' level of output")
    pdf.bullet("Prices adjust, and the economy returns to the natural rate of unemployment")
    pdf.bullet("Key factors: labor market institutions, technology, demographics")
    pdf.bullet("Models used: IS-LM-PC model (Chapters 7-9)")

    pdf.subsection_title("The Long Run (Decades to Centuries)")
    pdf.bullet("Focus on what determines the growth of output over long periods")
    pdf.bullet("Key factors: capital accumulation, technological progress, education")
    pdf.bullet("Models used: Growth models (Chapters 10-13)")

    pdf.section_title("2-6 A Tour of the Book")
    pdf.body_text("The book is organized in four main parts:")

    pdf.subsection_title("The Core (Chapters 3-9)")
    pdf.bullet("Chapters 3-6: The short run (goods market, financial markets, IS-LM model)")
    pdf.bullet("Chapters 7-9: The medium run (labor market, Phillips curve, IS-LM-PC model)")

    pdf.subsection_title("Extensions")
    pdf.bullet("Chapters 14-16: Expectations and their role in the economy")
    pdf.bullet("Chapters 17-20: The open economy (trade, exchange rates)")

    pdf.subsection_title("Back to Policy (Chapters 21-24)")
    pdf.bullet("Chapters 21-23: Fiscal and monetary policy analysis")
    pdf.bullet("Chapter 24: Epilogue - the history of macroeconomics")

    pdf.subsection_title("Appendix: The Construction of Real GDP and Chain-Type Indexes")
    pdf.bullet("Real GDP is constructed using **chain-type indexes** (Fisher index)")
    pdf.bullet("Rather than using a fixed base year, chain-type indexes compute growth rates using prices from adjacent years and then chain them together")
    pdf.bullet("This avoids the problem that a fixed base year becomes increasingly unrepresentative over time")
    pdf.bullet("The BEA uses 2009 as the reference year (where real GDP = nominal GDP)")
    pdf.bullet("For any other year, the growth rate of real GDP is computed by averaging growth rates calculated using prices from two consecutive years")

    # ===== LECTURE 1 ADDITIONS TO CHAPTER 2 =====
    pdf.add_page()
    pdf.chapter_title("NATIONAL ACCOUNTS: LECTURE PERSPECTIVES")

    pdf.section_title("The Gross Domestic Product (Lecture Framing)")
    pdf.bullet("Since the mid-20th century, GDP has been the most commonly used measure of economic performance")
    pdf.bullet("**Nominal GDP** measures the value of all final goods and services, expressed in current prices, produced in a country during a given period")
    pdf.bullet("Geographic focus, flow size, value added (no double counting)", level=1)
    pdf.bullet("**Real GDP** uses constant prices (base year), i.e., it corrects for inflation")
    pdf.bullet("If the (seasonally adjusted) real GDP falls for two consecutive quarters, economists speak of a **recession**")

    pdf.subsection_title("Nominal vs Real (Lecture Emphasis)")
    pdf.body_text("Separation of real and nominal quantities:")
    pdf.bullet("**Nominal values** are expressed in monetary units -> nominal wages, nominal interest rates")
    pdf.bullet("**Real values** are measured in physical goods (purchasing power) -> relative prices, real wages, real interest rates")
    pdf.bullet("Increase of the nominal GDP: production increases AND/OR prices increase")

    pdf.section_title("Economic Cycle as a Framework for Macroeconomics")
    pdf.body_text("The simple economic cycle: Households are suppliers of production factors and buyers of goods. They own factors of production that are traded on the financial market and labor market.")
    pdf.bullet("**Circular flow** links three markets: Goods Markets, Firms, Factor Markets, Households")
    pdf.bullet("Three equivalent measures of GDP in the circular flow:")
    pdf.bullet("Sales revenue (firms) = GDP (production approach)", level=1)
    pdf.bullet("Expenditure (households) = GDP (expenditure approach)", level=1)
    pdf.bullet("Factor compensation / Income = GDP (income approach)", level=1)

    pdf.slide_figure('2026-Economics-B_Folien-01.pdf', 26,
        'Figure: The Circular Flow - Goods Markets, Firms, Factor Markets, and Households')

    pdf.section_title("The Three Types of GDP Measurement")
    pdf.bullet("**Production approach**: GDP equals the value of final goods and services produced in the economy during a given period")
    pdf.bullet("**Income approach**: GDP is the sum of all payments to factors of production (labor, capital, land) in a given period")
    pdf.bullet("**Expenditure approach**: GDP is the sum of all spending on final goods produced within a country for private or public consumption, investment, or net exports")
    pdf.body_text("Example (production approach, value added):")
    pdf.bullet("Aluminum factory: sales revenue = 100, wages = 80, profit = 20")
    pdf.bullet("Car manufacturer: sales revenue = 210, intermediate consumption (aluminum) = 100, wages = 70, profit = 40")
    pdf.bullet("Total value added = 20 + (210 - 100) = 130 = total wages + total profits = 150 + (-20)... -> all three approaches yield the same GDP")

    pdf.section_title("Total Demand and Total Supply")
    pdf.body_text("Total supply and total demand in an open economy:")
    pdf.bullet("Total supply: domestic production (Y) + imports (M)")
    pdf.bullet("Total demand (Z): household consumption (C) + private sector investment (I) + government expenditure (G) + exports (X)")
    pdf.formula_block(r"Y + M = Z = C + I + G + X")
    pdf.body_text("Rearranging:")
    pdf.formula_block(r"Y = C + I + G + (X - M)")
    pdf.bullet("For the economy in the **short run**, demand is decisive, which is why we examine this equation in detail (-> Lecture 2)")

    pdf.section_title("Swiss GDP Data 2024")
    pdf.body_text("How large were Y, C, I, G, X, M in Switzerland in 2024? (Data at current prices, trade incl. gold; Source: Federal Statistical Office)")
    widths_ch = [55, 15, 25]
    pdf.table_header(["Component", "Symbol", "bn CHF"], widths_ch)
    pdf.table_row(["Private consumption", "C", "421"], widths_ch, True)
    pdf.table_row(["Private investment", "I", "228"], widths_ch)
    pdf.table_row(["Government consumption", "G", "102"], widths_ch, True)
    pdf.table_row(["Exports", "X", "608"], widths_ch)
    pdf.table_row(["Imports", "M", "505"], widths_ch, True)
    pdf.table_row(["GDP", "Y", "854"], widths_ch)
    pdf.ln(3)

    pdf.section_title("Value Added by Economic Sector (Switzerland)")
    pdf.body_text("Gross value added (GVA) by sector, nominal share in %, seasonally adjusted (Source: SECO):")
    pdf.bullet("**Primary sector** (agricultural): ~1% of GVA")
    pdf.bullet("**Secondary sector** (industry): ~27% of GVA")
    pdf.bullet("**Tertiary sector** (services): ~73% of GVA")
    pdf.bullet("These shares have been remarkably stable since 1990")

    pdf.section_title("GDP as a Welfare Measure (Lecture Discussion)")
    pdf.body_text("GDP measures overall economic performance. But is it also a useful measure of well-being (welfare)?")

    pdf.subsection_title("Limitations of GDP")
    pdf.bullet("Unpaid, non-market-based work (housework, bringing up children) is NOT captured")
    pdf.bullet("Black market and illegal activities are only partly included")
    pdf.bullet("Quality improvements are often hard to capture")
    pdf.bullet("New forms of economic activity are often captured with a delay")
    pdf.bullet("Free access to unprecedented amount of information due to new technologies is not captured (Hulten & Nakamura, NBER 2021)")

    pdf.subsection_title("Advantages of GDP")
    pdf.bullet("Comparability over time and between countries")
    pdf.bullet("Cannot be corrupted by politics (corrective by international institutions)")
    pdf.bullet("Relatively easy to measure, clear international standards")

    pdf.subsection_title("The Myth of the Broken Window")
    pdf.bullet("With fully utilized capacities: destruction does NOT increase GDP")
    pdf.bullet("With underutilized capacities: GDP increases but NOT net national income")

    pdf.subsection_title("GDP Per Capita vs GDP Per Hour Worked")
    pdf.bullet("Is maximization of GDP per capita the goal at all?")
    pdf.bullet("Germany has a higher per capita income than France, but GDP per hour worked is almost identical")
    pdf.bullet("Real GDP is theoretically grounded as a welfare measure")

    pdf.subsection_title("GDP and Complementary Indicators")
    pdf.bullet("High correlation between GDP per capita and complementary indicators: median income, Human Development Index (HDI)")
    pdf.bullet("GDP per capita vs life expectancy: strong positive relationship, but diminishing returns at higher income levels")
    pdf.bullet("GDP per capita vs HDI: strong positive relationship, concave shape")

    pdf.slide_figure('2026-Economics-B_Folien-01.pdf', 34,
        'Figure: GDP Per Capita vs. Life Expectancy — Strong positive relationship with diminishing returns')

    pdf.subsection_title("Excursion: GDP Measurement from Space")
    pdf.bullet("No GDP data available for many poorer countries; at regional level, reliable data often hardly exist")
    pdf.bullet("New approach since 2012: **satellite data on nighttime light intensity**")
    pdf.bullet("Example: North Korea vs South Korea - dramatic difference in light intensity reflects economic disparity")
    pdf.bullet("Source: Jiaxiong Yao, Illuminating Economic Growth, IMF F&D, September 2019")

    pdf.section_title("GDP Per Capita: International Comparison (2024)")
    pdf.body_text("GDP per capita in 1000 USD PPP (Source: World Bank, 2024 data):")
    pdf.bullet("Uganda: 3.3 | China: 27.1 | Russia: 47.4 | Japan: 51.7 | Italy: 60.9 | France: 61.3 | Austria: 71.6 | Germany: 72.3 | USA: 85.8 | Switzerland: 94.1")
    pdf.bullet("World average: approximately 27 (shown by red dashed line)")

    pdf.slide_figure('2026-Economics-B_Folien-01.pdf', 4,
        'Figure: GDP Per Capita in 1000 USD PPP (Source: World Bank, 2024) — World average shown by red dashed line')

    # Save
    path = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/econ/KW8_Intro_and_National_Accounts.pdf'
    pdf.output(path)
    print(f"Generated: {path}")


def generate_kw9():
    """Generate KW 9 PDF: The Goods Market (Ch 3 + Ch 5.1 + Ch 14.1-14.2 + Lecture 2)."""
    pdf = NotesPDF("KW 9: The Goods Market", "Ch 3, Ch 5.1, Ch 14.1-14.2 + Lecture 2")
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ===== LECTURE 2 CONTEXT =====
    pdf.add_page()
    pdf.chapter_title("LECTURE 2 CONTEXT: THE GOODS MARKET")

    pdf.section_title("Motivation: The Corona Crisis")
    pdf.body_text("Using the years 2020-2023, marked by the Corona crisis, we can illustrate many macroeconomic issues with real-world examples.")
    pdf.bullet("Private consumption and GDP fell sharply in 2020")
    pdf.bullet("At the same time, government spending increased")
    pdf.bullet("Swiss data (real index, 2020 = 100): GDP and private consumption dropped ~3-4%, while government consumption rose")
    pdf.bullet("Recovery was uneven: GDP recovered faster than private consumption")

    pdf.slide_figure('2026-Economics-B_Folien-02.pdf', 2,
        'Figure: Corona Crisis — Swiss GDP, Private Consumption, and Government Consumption (real index, 2015-2025)')

    pdf.section_title("How Economists Analyze Economic Policy Problems")
    pdf.body_text("Using (mathematical) models:")
    pdf.bullet("Precision of the problem, transparent assumptions, consistent analysis")
    pdf.bullet("Clear indication of model assumptions and causal relationships")
    pdf.bullet("Basic concept of an economic model:")
    pdf.bullet("Mathematical functions describe causal relationships", level=1)
    pdf.bullet("Model assumptions influence both causality and dynamics", level=1)
    pdf.bullet("**Exogenous** (independent) and **endogenous** (dependent) variables", level=1)
    pdf.bullet("Model parameters", level=1)
    pdf.bullet("The model shows dynamics and is suitable for **comparative statics**")
    pdf.bullet("Comparison of model statements with empirical analysis")

    pdf.section_title("Empirical Macroeconomics")
    pdf.bullet("Empirical analyses require experiences and real events")
    pdf.bullet("In macroeconomics there are no artificial laboratory data to test hypotheses - one must use available data based on past real situations")
    pdf.bullet("Important econometric insights are based on:")
    pdf.bullet("Time series data", level=1)
    pdf.bullet("'Natural experiments' (e.g. German reunification)", level=1)
    pdf.bullet("Comparisons between countries (or states, cantons)", level=1)
    pdf.bullet("Example: Did the Hartz reforms reduce German unemployment?")

    pdf.section_title("Learning Objectives (Lecture 2)")
    pdf.bullet("The economy in the short-run")
    pdf.bullet("Idea and construction of a macroeconomic model")
    pdf.bullet("Components of gross domestic product (GDP) and their determinants")
    pdf.bullet("Consumption theories according to Keynes and Friedman")
    pdf.bullet("Derivation of the IS curve for the IS-LM model")
    pdf.bullet("Literature: Blanchard Chapter 3, 5.1, 14.1 & 14.2")

    pdf.section_title("GDP Over Time and Course Structure")
    pdf.body_text("In the long run GDP follows a (hopefully rising) path. At any given time there is a GDP value on the trend line:")
    pdf.formula_block(r"Y_{n,t} \quad \text{(natural/trend GDP at time } t \text{)}")
    pdf.bullet("We first examine **short-term fluctuations** (-> Lectures 2 to 4)")
    pdf.formula_block(r"\text{Then we determine } Y_{n,t} \text{ at a given time } t \text{ (-> Lectures 5 to 7)}", fontsize=11)
    pdf.formula_block(r"\text{Finally we analyze the trend of } Y_{n,t} \text{ (-> Lectures 10 to 11)}", fontsize=11)

    pdf.section_title("The Economy in the Short-Run")
    pdf.bullet("In lectures 2, 3, and 4 we focus on the **short-run**:")
    pdf.bullet("Short-run (< 5 years), medium-run (5-10 years), long-run (> 10 years)", level=1)
    pdf.bullet("The subdivision is based on how quickly economic processes unfold", level=1)
    pdf.bullet("Each requires a different perspective and economic analysis tools", level=1)
    pdf.bullet("Economic variables behave differently in the short-run than in the long-run")
    pdf.bullet("Example: Government spending is increased. Short-term GDP increase; the long-term effect is much less clear.")
    pdf.bullet("In the short-run, we ignore resource constraints and analyze economic fluctuations. Prices and wages are rigid in the short run.")

    pdf.section_title("The IS-LM Model Preview")
    pdf.body_text("We use the well-known IS-LM model for short-run analysis:")
    pdf.bullet("As simple as possible, but not too simple")
    pdf.bullet("We essentially need: **goods market** + **financial market**")
    pdf.bullet("We leave out for now: labor market, stocks, foreign countries, ...")
    pdf.bullet("Goods market in equilibrium (IS curve): supply and demand")
    pdf.bullet("Financial market in equilibrium (LM curve): supply and demand")
    pdf.bullet("Goal: Understanding model, applying model, questioning model")

    pdf.subsection_title("Example: Japan VAT Increase (2019)")
    pdf.bullet("Japan raised the value added tax from 8% to 10% as of October 1, 2019")
    pdf.bullet("Bigger than expected hit from the sales tax rise; drop in spending")
    pdf.bullet("Japan's government increased VAT knowing the short-term negative effects - the goal was to reduce the public deficit")
    pdf.bullet("How is the measure to be assessed in the medium-term? -> This is what our models help answer")

    # CHAPTER 3
    pdf.add_page()
    pdf.chapter_title("CHAPTER 3: THE GOODS MARKET")

    pdf.body_text("Year-to-year movements in economic activity are driven by the interactions among production, income, and demand. Changes in demand lead to changes in production, which lead to changes in income, which in turn lead to changes in demand.")

    pdf.subsection_title("The Economy in the Short-Term (Lecture)")
    pdf.body_text("With annual fluctuations in economic activity, the interrelation between production, income, and demand is central to macroeconomic understanding:")
    pdf.bullet("Changes in demand lead to adjustments in production")
    pdf.bullet("Adjustments in production trigger changes in income")
    pdf.bullet("Changes in income cause changes in demand")
    pdf.bullet("In the analysis of the goods market we therefore focus on demand for goods, production, and income - as seen in Lecture 1, all three correspond to GDP")

    pdf.subsection_title("Swiss GDP Growth Over Time (Lecture)")
    pdf.body_text("Expenditure-side growth contributions to nominal GDP (Source: SECO, 2000-2024): Private consumption, public consumption, investment, net exports all contribute to GDP growth. Key observation:")
    pdf.bullet("**Consumption fluctuates much less than GDP** (consumption smoothing)")
    pdf.bullet("Investment and net exports are the main sources of volatility")

    pdf.section_title("3-1 The Composition of GDP")
    pdf.body_text("GDP can be decomposed from the point of view of different buyers for goods. The terms 'output' and 'production' are synonymous.")
    pdf.body_text("The GDP can be determined in three ways: production approach, income approach, expenditure approach (see Lecture 1). Here we use the expenditure approach:")
    pdf.formula_block(r"\text{GDP} = Y = C + I + G + NX", fontsize=12)
    pdf.body_text("where NX = X - IM (net exports). Assumption for a closed economy: X = IM = 0.")

    pdf.subsection_title("The Five Components of GDP")
    widths = [55, 15, 25, 25]
    pdf.table_header(["Component", "Symbol", "US 2014 ($B)", "% of GDP"], widths)
    pdf.table_row(["Consumption", "C", "11,865", "68.3%"], widths, True)
    pdf.table_row(["Investment", "I", "2,782", "16.0%"], widths)
    pdf.table_row(["  - Nonresidential", "", "2,233", "12.9%"], widths, True)
    pdf.table_row(["  - Residential", "", "549", "3.1%"], widths)
    pdf.table_row(["Government spending", "G", "3,152", "18.1%"], widths, True)
    pdf.table_row(["Net exports", "X-IM", "-530", "-3.1%"], widths)
    pdf.table_row(["Inventory investment", "", "77", "0.4%"], widths, True)
    pdf.table_row(["GDP (Y)", "", "17,348", "100.0%"], widths)
    pdf.ln(3)

    pdf.subsection_title("Detailed Definitions")
    pdf.bullet("**Consumption (C)**: Goods and services purchased by consumers. Largest component at 68% of GDP.")
    pdf.bullet("**Investment (I)**: Also called fixed investment. Sum of nonresidential investment (firms buying plants/machines) and residential investment (people buying houses). NOT financial investment.")
    pdf.bullet("**Government spending (G)**: Purchases of goods and services by government. Does NOT include government transfers (Medicare, Social Security) or interest on government debt. G = 18.1% of GDP, much less than total government spending (~33%) because transfers are excluded.")
    pdf.bullet("**Net exports (X - IM)**: Exports minus imports. Trade surplus if X > IM; trade deficit if X < IM. U.S. had a trade deficit of 3.1% in 2014.")
    pdf.bullet("**Inventory investment**: Difference between goods produced and goods sold. Production > Sales = positive inventory investment.")

    pdf.section_title("3-2 The Demand for Goods")
    pdf.body_text("Total demand for goods is denoted by Z:")
    pdf.formula_block(r"Z \equiv C + I + G + X - IM")

    pdf.subsection_title("Three Simplifying Assumptions")
    pdf.bullet("(1) All firms produce the same good (one market)")
    pdf.bullet("(2) Firms supply any amount at a given price P (focus on demand; valid in short run)")
    pdf.bullet("(3) Closed economy: no trade")
    pdf.formula_block(r"X = IM = 0", fontsize=12)
    pdf.body_text("Under closed economy assumption:")
    pdf.formula_block(r"Z = C + I + G", fontsize=12)

    pdf.subsection_title("Consumption (C)")
    pdf.bullet("Consumption depends primarily on **disposable income**:")
    pdf.formula_block(r"Y_D = Y - T", fontsize=12)
    pdf.formula_block(r"C = C(Y_D) \quad (+)")
    pdf.body_text("Linear specification:")
    pdf.formula_block(r"C = c_0 + c_1 \cdot Y_D = c_0 + c_1(Y - T)")

    pdf.bullet("**Marginal propensity to consume**: effect of an additional $1 of disposable income on consumption:")
    pdf.formula_block(r"c_1 \quad \text{with restriction} \quad 0 < c_1 < 1", fontsize=12)
    pdf.bullet("Example: if c1 = 0.6, an additional $1 of income raises consumption by $0.60")
    pdf.bullet("**Autonomous consumption**: consumption when disposable income is zero. Must be positive (people still need to eat):")
    pdf.formula_block(r"c_0 > 0", fontsize=12)
    pdf.bullet("Changes in c0 reflect changes in consumer confidence, ease of borrowing, etc.")

    pdf.slide_figure('2026-Economics-B_Folien-02.pdf', 17,
        'Figure: The Linear Consumption Function — C = c0 + c1 * Y_D (slope = c1, intercept = c0)')

    pdf.sub_subsection_title("Consumption Theories (Lecture)")
    pdf.body_text("Two main theories of consumption:")
    pdf.bullet("**Keynesian consumption function** (used in this model): Consumption is based only on current disposable income. The propensity to save/consume is postulated from aggregated data (no micro-foundation).")
    pdf.bullet("**Permanent income hypothesis** (Friedman): Households with a longer-term planning horizon choose consumption to maximize an intertemporal utility function (-> consumption smoothing)")
    pdf.bullet("Elements of the permanent income model:", level=1)
    pdf.bullet("Lifetime income: all present and future income", level=1)
    pdf.bullet("Utility function: consumption and leisure generate utility", level=1)
    pdf.bullet("Intertemporal budget constraint: households cannot spend more than they earn", level=1)
    pdf.bullet("Optimization within the constraints (-> tutorials)", level=1)
    pdf.bullet("We focus on the Keynesian approach in this chapter")

    pdf.sub_subsection_title("Keynesian Consumption: Swiss Empirical Data (Lecture)")
    pdf.body_text("Based on Swiss data for disposable income (Y_D) and consumption (C), the estimated function is:")
    pdf.formula_block(r"\hat{C} = \hat{c}_0 + \hat{c}_1 \, Y_D = 68 + 0.8 \, Y_D", fontsize=12)
    pdf.bullet("The estimated marginal propensity to consume is approximately 0.8")
    pdf.bullet("Source: Federal Statistical Office, data 1990-2024 in billion CHF")

    pdf.slide_figure('2026-Economics-B_Folien-02.pdf', 18,
        'Figure: Swiss Empirical Consumption Function — C = 68 + 0.8 * Y_D (scatter + regression, 1990-2024)')

    pdf.sub_subsection_title("Critique of Keynesian Consumption (Lecture)")
    pdf.bullet("Every economic model requires simplifying assumptions - it is important to critically examine them")
    pdf.bullet("Fundamental critique: the function is postulated and not derived (not micro-founded)")
    pdf.bullet("Important factors NOT considered: income shifts over the life cycle, consideration of future income (and taxes), savings and interest rate, wealth")

    pdf.subsection_title("Investment (I)")
    pdf.bullet("Treated as **exogenous** (taken as given) in this chapter:")
    pdf.formula_block(r"I = \bar{I}")
    pdf.bullet("This simplification is relaxed in Chapter 5 where investment depends on output and the interest rate")

    pdf.sub_subsection_title("Investment: Lecture Detail (Preview of Ch 5)")
    pdf.body_text("Three components of private investment: investment in equipment by firms, investment in construction, changes in inventories.")
    pdf.bullet("Private investment is important for two reasons:")
    pdf.bullet("(1) Part of GDP: investment explains the level and (short-term) fluctuations in output", level=1)
    pdf.bullet("Investment is much more volatile than consumption (-> household consumption smoothing)", level=1)
    pdf.bullet("(2) Increase the stock of productive capital:")
    pdf.formula_block(r"K_{\text{tomorrow}} = K_{\text{today}} + I - \text{Depreciation}", fontsize=12)
    pdf.bullet("Investment central to long-term economic growth (-> Lecture 10)")

    pdf.bullet("What determines the level of private investment?")
    pdf.bullet("**(1) The interest rate**: Companies have many potential investment projects with different returns-on-investment (RoI). Every project has a **net present value**:")
    pdf.formula_block(r"NPV = CF_0 + \frac{CF_1}{1+i} + \frac{CF_2}{(1+i)^2} + \frac{CF_3}{(1+i)^3} + \ldots")
    pdf.formula_block(r"CF_0 = \text{investment today (negative cash flow)}", fontsize=11)
    pdf.formula_block(r"CF_1, CF_2, CF_3, \ldots = \text{future earnings (expected)}", fontsize=11)
    pdf.bullet("A lower interest rate makes more projects profitable (-> lower opportunity costs)")

    pdf.bullet("**(2) The level of production**: To produce more, additional machines are necessary")
    pdf.body_text("Summarizing both aspects mathematically:")
    pdf.formula_block(r"I = I(\underset{(+)}{Y},\; \underset{(-)}{i})")
    pdf.bullet("In contrast to Blanchard, who often writes just I(i), the lecture emphasizes I(Y, i)")
    pdf.bullet("The model could be supplemented by other factors: expectations about the future (-> PMI), risk preferences")
    pdf.bullet("**Endogenous variables**: depend on other variables in the model")
    pdf.bullet("**Exogenous variables**: not explained in the model (taken as given)")

    pdf.subsection_title("Government Spending (G) - The State")
    pdf.formula_block(r"\text{GDP:} \quad Y = C + I + G + NX", fontsize=12)
    pdf.body_text("How can the state act to influence GDP?")
    pdf.bullet("Direct and indirect taxes -> T")
    pdf.bullet("Transfer payments (e.g., unemployment benefit) -> T")
    pdf.bullet("Government spending on goods and services -> G")
    pdf.bullet("Decisions on government spending G, and the amount of taxes and transfers T, are called **fiscal policy**")
    pdf.bullet("Both G and T treated as exogenous: (1) governments don't behave with simple regularity, (2) we want to analyze policy scenarios")

    pdf.section_title("3-3 The Determination of Equilibrium Output")
    pdf.body_text("Combining all components:")
    pdf.formula_block(r"Z = c_0 + c_1(Y - T) + \bar{I} + G")
    pdf.body_text("Equilibrium condition (production = demand):")
    pdf.formula_block(r"Y = Z")

    pdf.key_concept_box("Three Types of Equations in Models",
        "1. Identities (e.g., disposable income definition)\n"
        "2. Behavioral equations (e.g., consumption function)\n"
        "3. Equilibrium conditions (e.g., production = demand)")

    pdf.body_text("Substituting demand into equilibrium:")
    pdf.formula_block(r"Y = c_0 + c_1(Y - T) + \bar{I} + G")

    pdf.subsection_title("Using Algebra")
    pdf.body_text("Solving for Y:")
    pdf.formula_block(r"Y = \frac{1}{1 - c_1} \left[ c_0 + \bar{I} + G - c_1 T \right]")

    pdf.bullet("**Autonomous spending**: the part of demand that does NOT depend on output")
    pdf.formula_block(r"\text{Autonomous spending} = c_0 + \bar{I} + G - c_1 T", fontsize=12)
    pdf.bullet("**The Multiplier**: multiplies autonomous spending. Always > 1 because 0 < c1 < 1:")
    pdf.formula_block(r"\text{Multiplier} = \frac{1}{1 - c_1}", fontsize=12)
    pdf.bullet("Example:")
    pdf.formula_block(r"\text{if } c_1 = 0.6, \quad \text{multiplier} = \frac{1}{0.4} = 2.5", fontsize=12)
    pdf.bullet("A $1 billion increase in autonomous spending increases output by $2.5 billion")

    pdf.subsection_title("Using a Graph: The Keynesian Cross (Figure 3-2)")
    pdf.body_text("The Keynesian cross diagram (lecture version):")
    pdf.bullet("Y-axis: Demand Z, Production Y")
    pdf.bullet("X-axis: Income Y")
    pdf.bullet("**45-degree line** (Production: Y = Y, slope = 1)")
    pdf.bullet("**ZZ curve** (demand): intercept = autonomous spending, slope = c1 (< 1, flatter than 45-degree line)")
    pdf.body_text("The ZZ curve equation:")
    pdf.formula_block(r"ZZ: \quad Z = (c_0 + \bar{I} + G - c_1 T) + c_1 Y")
    pdf.bullet("Equilibrium at point A where ZZ crosses the 45-degree line (Y = Z)")
    pdf.bullet("Left of A: demand > production -> firms increase output")
    pdf.bullet("Right of A: production > demand -> firms decrease output")
    pdf.bullet("Note: the ZZ curve is drawn for a given interest rate")

    pdf.slide_figure('2026-Economics-B_Folien-02.pdf', 26,
        'Figure: The Keynesian Cross — ZZ demand curve (slope c1), 45-degree line, equilibrium at point A')

    pdf.subsection_title("Comparative Statics: Increase in G (Lecture)")
    pdf.body_text("How does the equilibrium change if government spending G increases?")
    pdf.bullet("The demand for goods Z increases if: autonomous consumption (c0) rises, government spending (G) rises, taxes (T) are reduced, interest rate (i) is lowered")
    pdf.body_text("In equilibrium, solving for Y:")
    pdf.formula_block(r"Y = \frac{1}{1-c_1}\left[c_0 + \bar{I} + G - c_1 T\right]")
    pdf.formula_block(r"\Longrightarrow \quad \frac{1}{1-c_1} = \text{multiplier}", fontsize=12)
    pdf.bullet("If G increases by 1, Y increases by 1/(1-c1) > 1")
    pdf.body_text("Graphically (step by step): ZZ shifts up to ZZ'. Starting at A, demand rises to B, then production adjusts to C, then demand rises to D, then to E, converging to the new equilibrium A'.")
    pdf.formula_block(r"\Delta Y = \frac{1}{1-c_1} \cdot \Delta G > \Delta G", fontsize=12)

    pdf.slide_figure('2026-Economics-B_Folien-02.pdf', 28,
        'Figure: Comparative Statics — Increase in G shifts ZZ up; multiplier mechanism (A -> B -> C -> D -> E -> A\')')

    pdf.subsection_title("How Large Is the Multiplier? (Lecture)")
    pdf.bullet("Valid only for **unutilized capacities**; hence the amount is often overestimated")
    pdf.bullet("Real-world examples: HSG expansion, EU Green Deal, Juncker Plan")

    pdf.subsection_title("The Multiplier Effect: Numerical Example (Lecture)")
    pdf.body_text("The state pays 100 CHF for road repair (with c1 = 0.8):")
    pdf.bullet("Road builder spends 80 CHF in a shop and saves 20 CHF")
    pdf.bullet("Retailers spend 80 x 0.8 = 64 CHF and save 16 CHF")
    pdf.bullet("After 2 rounds: cumulative increase = 100 + 80 + 64 = 244 CHF")
    pdf.bullet("After all rounds: increase in GDP by 500 CHF")
    pdf.formula_block(r"\text{Multiplier} = \frac{1}{1-c_1} = \frac{1}{1-0.8} = \frac{1}{0.2} = 5", fontsize=12)
    pdf.body_text("The geometric series:")
    pdf.formula_block(r"1 + c_1 + c_1^2 + \ldots + c_1^n = \frac{1}{1 - c_1} \quad (n \to \infty)")

    pdf.subsection_title("The Multiplier Effect (Figure 3-3)")
    pdf.body_text("If c0 increases by $1 billion:")
    pdf.bullet("Round 1: Demand increases by $1B -> Production rises $1B -> Income rises $1B")
    pdf.bullet("Round 2: Consumption rises by c1 x $1B -> Production rises by c1 billion:")
    pdf.formula_block(r"\Delta C_2 = c_1 \times \$1B", fontsize=11)
    pdf.bullet("Round 3: Consumption rises further:")
    pdf.formula_block(r"\Delta C_3 = c_1^2 \times \$1B", fontsize=11)
    pdf.bullet("Total effect is a geometric series:")
    pdf.formula_block(r"1 + c_1 + c_1^2 + \cdots + c_1^n \;\longrightarrow\; \frac{1}{1 - c_1} \quad (n \to \infty)")

    pdf.subsection_title("How Long Does Output Take to Adjust?")
    pdf.bullet("In the model (no inventories, instant responses): adjustment is instantaneous")
    pdf.bullet("In reality: adjustment takes time. Firms revise production quarterly, inventory adjustments occur first")
    pdf.bullet("Output does not jump to Y' but increases gradually over time")

    pdf.key_concept_box("Focus Box: Lehman Bankruptcy",
        "During the 2008 crisis, consumption fell sharply despite disposable\n"
        "income initially not declining much. This represents a decrease in c0\n"
        "(consumer confidence collapsed). Together with falling autonomous\n"
        "investment (housing), the multiplier amplified these into large output declines.")

    pdf.section_title("3-4 Investment Equals Saving: An Alternative Equilibrium View")

    pdf.subsection_title("Private Saving")
    pdf.formula_block(r"S = Y - T - C = -c_0 + (1 - c_1)(Y - T)")
    pdf.bullet("**Propensity to save**: how much of an additional dollar is saved:")
    pdf.formula_block(r"(1 - c_1) = \text{propensity to save}", fontsize=12)

    pdf.subsection_title("The IS Relation")
    pdf.body_text("Starting from the equilibrium condition, rearranging:")
    pdf.formula_block(r"Y = C + I + G", fontsize=12)
    pdf.formula_block(r"I = S + (T - G)")
    pdf.bullet("In equilibrium, **investment = private saving + public saving**")
    pdf.bullet("This is called the **IS relation** (Investment = Saving)")
    pdf.bullet("Public saving: T - G. If T > G: budget surplus. If T < G: budget deficit.")

    pdf.key_concept_box("Paradox of Saving (Paradox of Thrift)",
        "If consumers try to save more (c0 decreases):\n"
        "- Equilibrium output DECREASES\n"
        "- But total saving does NOT change (because I = I-bar is fixed)\n"
        "- Mechanism: more saving -> less consumption -> less demand -> less output\n"
        "  -> less income -> the fall in income offsets the attempt to save more\n"
        "- Warning: only in the short run. In the medium/long run, higher saving can\n"
        "  lead to higher investment and income.")

    pdf.section_title("3-5 Is the Government Omnipotent? A Warning")
    pdf.bullet("Eq. (3.8) suggests the government can choose any output level. In reality:")
    pdf.bullet("(1) Changing G or T is slow and contentious (legislative process)")
    pdf.bullet("(2) Investment responds to output; imports leak demand abroad; exchange rates change")
    pdf.bullet("(3) Expectations matter: consumer response depends on whether tax cuts are perceived as temporary or permanent")
    pdf.bullet("(4) Side effects: too-high output can lead to increasing inflation")
    pdf.bullet("(5) Budget deficits accumulate into public debt with long-run adverse effects")

    # CHAPTER 5.1
    pdf.add_page()
    pdf.chapter_title("CHAPTER 5, SECTION 5-1: The Goods Market and the IS Relation")

    pdf.section_title("Investment Now Depends on Output and Interest Rate")
    pdf.body_text("In Chapter 3, investment was constant. Now investment depends on two factors:")
    pdf.bullet("**(1) Level of sales/output (+)**: Higher sales -> firms need to invest to expand capacity")
    pdf.bullet("**(2) Interest rate (-)**: Higher interest rate -> more costly to borrow -> less attractive to invest. Even with own funds, high i means it's more profitable to lend than to buy machines.")
    pdf.formula_block(r"I = I(Y,\, i) \quad \underset{(+,\;-)}{}")

    pdf.section_title("Determining Output")
    pdf.body_text("Replacing I-bar with I(Y, i) in the equilibrium condition:")
    pdf.formula_block(r"Y = C(Y - T) + I(Y,\, i) + G")
    pdf.bullet("Demand now depends on income Y (through C and I), interest rate i (through I), and fiscal policy (G, T)")

    pdf.section_title("Deriving the IS Curve")
    pdf.bullet("For a given interest rate, the ZZ line shows demand as a function of output")
    pdf.bullet("ZZ is upward sloping with slope < 1 (increase in demand < increase in output)")
    pdf.bullet("Equilibrium where ZZ crosses 45-degree line")

    pdf.subsection_title("Figure 5-3: The IS Curve")
    pdf.bullet("An increase in i decreases investment at any level of output -> ZZ shifts DOWN")
    pdf.bullet("Equilibrium output DECREASES")
    pdf.bullet("Plotting all (i, Y) pairs: the **IS curve is downward sloping**")

    pdf.key_concept_box("IS Curve Properties",
        "- Downward sloping: higher interest rate -> lower output\n"
        "- Represents all (i, Y) combinations where goods market is in equilibrium\n"
        "- Shifts RIGHT with: increase in G, decrease in T, increase in consumer confidence\n"
        "- Shifts LEFT with: decrease in G, increase in T, decrease in confidence")

    pdf.subsection_title("IS Curve Derivation: Two-Panel Graph (Lecture)")
    pdf.body_text("The IS curve is derived from the goods market equilibrium using a two-panel approach:")
    pdf.bullet("**Left panel** (Keynesian cross): As i rises from i0 to i1 > i0, investment falls, ZZ shifts down from ZZ(i0) to ZZ(i1), equilibrium output falls from Y0 to Y1")
    pdf.bullet("**Right panel** (IS curve): Plot the pairs (Y0, i0) as point A and (Y1, i1) as point B, connect to get the downward-sloping IS curve")
    pdf.bullet("**Above** the IS curve: Excess supply on the goods market (production > demand)")
    pdf.bullet("**Below** the IS curve: Excess demand on the goods market (demand > production)")
    pdf.bullet("**On** the IS curve: Equilibrium on the goods market")

    pdf.slide_figure('2026-Economics-B_Folien-02.pdf', 32,
        'Figure: IS Curve Derivation — Two-panel: Keynesian cross (left) and downward-sloping IS curve (right)')

    pdf.subsection_title("IS Curve: Investments and Savings (Lecture)")
    pdf.body_text("The name 'IS' stands for Investment = Savings. An alternative approach to the goods market equilibrium:")
    pdf.bullet("Private consumer savings:")
    pdf.formula_block(r"S = Y - T - C", fontsize=12)
    pdf.body_text("GDP equation (excluding exports and imports):")
    pdf.formula_block(r"Y = C + I + G", fontsize=12)
    pdf.body_text("Rearranging:")
    pdf.formula_block(r"S + T + C = C + I + G \quad \Longrightarrow \quad I = S + (T - G)")
    pdf.bullet("With trade:")
    pdf.formula_block(r"I = S + (T - G) + (IM - X)", fontsize=12)
    pdf.bullet("The goods market is only in equilibrium if investment equals savings (the sum of private and state savings)")
    pdf.bullet("Is S or I the driver? Theory of effective demand (Keynes) vs supply-oriented theories (Say's law, (neo-)classical)")

    pdf.subsection_title("The IS Curve: Discussion (Lecture)")
    pdf.body_text("The implicit IS curve:")
    pdf.formula_block(r"Y = C(Y - T) + I(Y,\, i) + G \quad \text{(assumption: } X = IM = 0 \text{)}")
    pdf.bullet("The IS curve depends negatively on the interest rate: with increasing interest rates, investment demand and total production decrease")
    pdf.bullet("Where does the interest rate come from? -> Financial Market, LM curve, Lecture 3")
    pdf.bullet("**Movement along the IS curve**: Interest rate change -> endogenous adjustment of production volume")
    pdf.bullet("**Shifts in the IS curve**: Factors that trigger a decrease (increase) in the demand for goods at a given interest rate shift the IS curve to the left (right). Example: increased government spending shifts IS right.")

    pdf.subsection_title("The Savings Paradox: Discussion (Lecture)")
    pdf.bullet("Y **decreases** with increasing propensity to save (i.e., with smaller c0 or c1)")
    pdf.bullet("The higher c1, the higher the multiplier")
    pdf.bullet("Is saving bad? In the short run, more saving -> less consumption -> less demand -> less output")
    pdf.bullet("In the medium/long run, higher saving can lead to higher investment and income")

    pdf.subsection_title("Application: Swiss Consumer Sentiment (Lecture)")
    pdf.body_text("Consumer sentiment in Switzerland, calculated by SECO, has continued to recover in 2025. What does this mean for the Swiss economy?")
    pdf.bullet("Higher consumer sentiment -> higher c0 (autonomous consumption) -> ZZ shifts up -> Y increases")
    pdf.bullet("This is a real-world application of the multiplier mechanism")

    # CHAPTER 14.1-14.2
    pdf.add_page()
    pdf.chapter_title("CHAPTER 14: Financial Markets and Expectations")
    pdf.section_title("14-1 Expected Present Discounted Values")

    pdf.body_text("The expected present discounted value of a sequence of future payments is the value today of this expected sequence. It allows comparing a current cost against a stream of future benefits.")

    pdf.subsection_title("Basic Concepts")
    pdf.bullet("$1 today is worth $(1 + i) next year (if lent at rate i)")
    pdf.bullet("$1 next year is worth less than $1 today = the **present discounted value**:")
    pdf.formula_block(r"\text{Present value of \$1 next year} = \frac{\$1}{1+i}", fontsize=12)
    pdf.bullet("i is the **discount rate**; the **discount factor** is:")
    pdf.formula_block(r"\text{Discount factor} = \frac{1}{1+i}", fontsize=12)
    pdf.bullet("Higher interest rate -> lower present value of future payments")
    pdf.bullet("Example: i = 5% -> $1 next year is worth $0.95 today")
    pdf.bullet("Example: i = 10% -> $1 next year is worth $0.91 today")

    pdf.subsection_title("The General Formula")
    pdf.formula_block(r"\$V_t = \$z_t + \frac{1}{1+i_t}\,\$z^e_{t+1} + \frac{1}{(1+i_t)(1+i^e_{t+1})}\,\$z^e_{t+2} + \cdots")

    pdf.bullet("Each future payment is multiplied by its discount factor")
    pdf.bullet("More distant payments have smaller discount factors -> lower present value")
    pdf.bullet("Present value depends **positively** on future payments and **negatively** on interest rates")

    pdf.subsection_title("Special Cases")

    pdf.sub_subsection_title("Constant Interest Rates")
    pdf.formula_block(r"\$V_t = \$z_t + \frac{1}{1+i}\,\$z^e_{t+1} + \frac{1}{(1+i)^2}\,\$z^e_{t+2} + \cdots")
    pdf.bullet("Weights decline geometrically:")
    pdf.formula_block(r"1, \;\; \frac{1}{1+i}, \;\; \frac{1}{(1+i)^2}, \;\; \ldots", fontsize=12)
    pdf.bullet("i = 10%: payment in 10 years -> weight = 0.386; payment in 30 years -> weight = 0.057")

    pdf.sub_subsection_title("Constant Rates and Payments (n years)")
    pdf.formula_block(r"\$V_t = \$z \;\frac{1 - \left(\frac{1}{1+i}\right)^n}{1 - \frac{1}{1+i}}")
    pdf.bullet("Example: 'Win $1M' lottery paying $50,000/year for 20 years at i=6%: actual present value is only ~$608,000")

    pdf.sub_subsection_title("Perpetuity (Consol) - Payments Forever")
    pdf.formula_block(r"\$V_t = \frac{\$z}{i}")
    pdf.bullet("$10/year forever at i=5% -> worth $200. At i=10% -> worth $100")

    pdf.sub_subsection_title("Zero Interest Rates")
    pdf.bullet("If i = 0, present value = simple sum of all payments (useful approximation)")

    pdf.subsection_title("Nominal vs. Real Present Values")
    pdf.bullet("**Nominal**: discount dollar payments using nominal interest rates")
    pdf.bullet("**Real**: discount real payments (in terms of goods) using real interest rates")
    pdf.bullet("The two approaches are equivalent:")
    pdf.formula_block(r"\frac{\$V_t}{P_t} = V_t", fontsize=12)
    pdf.bullet("Use nominal for bond pricing; use real for consumption/investment decisions")

    pdf.section_title("14-2 Bond Prices and Bond Yields")

    pdf.subsection_title("Bond Basics")
    pdf.bullet("Two key dimensions: **maturity** (time of payments) and **risk** (default risk, price risk)")
    pdf.bullet("**Discount bonds** (zero-coupon): single payment at maturity (the face value)")
    pdf.bullet("**Coupon bonds**: periodic coupon payments plus face value at maturity")
    pdf.bullet("Coupon rate = coupon payment / face value")
    pdf.bullet("Current yield = coupon payment / bond price")
    pdf.bullet("**Yield to maturity**: the correct measure of return")

    pdf.key_concept_box("Bond Market Vocabulary",
        "- Government bonds (Treasuries, Bunds) vs Corporate bonds\n"
        "- Bond ratings: Moody's Aaa to C; S&P AAA to D\n"
        "- Risk premium: extra rate on risky bonds vs safest bonds\n"
        "- Junk bonds: high default risk bonds\n"
        "- T-bills: short-term government bonds (< 1 year)\n"
        "- Consols: perpetual bonds (pay forever)\n"
        "- TIPS: Treasury Inflation Protected Securities (indexed to inflation)")

    pdf.subsection_title("Bond Prices as Present Values")
    pdf.body_text("One-year discount bond (face value $100):")
    pdf.formula_block(r"\$P_{1t} = \frac{\$100}{1 + i_{1t}}")
    pdf.body_text("Two-year discount bond (face value $100):")
    pdf.formula_block(r"\$P_{2t} = \frac{\$100}{(1 + i_{1t})(1 + i^e_{1,t+1})}")

    pdf.subsection_title("Arbitrage and Bond Prices")
    pdf.bullet("**Arbitrage**: if investors care only about expected returns (expectations hypothesis), expected returns must be equal across bonds")
    pdf.formula_block(r"1 + i_{1t} = \frac{\$P^e_{1,t+1}}{\$P_{2t}}")
    pdf.bullet("This implies: bond prices = expected present values of future payments")

    pdf.subsection_title("From Bond Prices to Bond Yields")
    pdf.bullet("**Yield to maturity** for a 2-year bond: the constant annual rate making price = present value")
    pdf.formula_block(r"\$P_{2t} = \frac{\$100}{(1 + i_{2t})^2}")
    pdf.body_text("Relationship between yield and short-term rates:")
    pdf.formula_block(r"(1 + i_{2t})^2 = (1 + i_{1t})(1 + i^e_{1,t+1})")
    pdf.body_text("Approximation:")
    pdf.formula_block(r"i_{2t} \approx \frac{1}{2}\left(i_{1t} + i^e_{1,t+1}\right)")
    pdf.bullet("The 2-year rate is approximately the average of the current and expected future 1-year rate")
    pdf.bullet("Generalizes: n-year rate = average of current and expected future 1-year rates over n years")

    pdf.subsection_title("The Yield Curve (Term Structure of Interest Rates)")
    pdf.bullet("A graph of yield vs. maturity for bonds observed on a given day")
    pdf.bullet("**Upward-sloping**: markets expect future short rates to RISE (e.g., expected economic expansion)")
    pdf.bullet("**Downward-sloping (inverted)**: markets expect future short rates to FALL (e.g., expected slowdown)")

    pdf.key_concept_box("Figure 14-2: U.S. Yield Curves",
        "November 2000: Slightly downward sloping\n"
        "  - 3-month rate: 6.2%, 30-year rate: 5.8%\n"
        "  - Markets expected rates to decrease slightly (economy slowing)\n"
        "June 2001: Steeply upward sloping\n"
        "  - 3-month rate: 3.5%, 30-year rate: 5.7%\n"
        "  - Fed had cut rates sharply; markets expected recovery and rate rises")

    # Summary of Key Formulas
    pdf.add_page()
    pdf.chapter_title("SUMMARY OF KEY FORMULAS")

    pdf.formula_block(r"\text{(3.2)} \quad C = c_0 + c_1 \, Y_D \quad \text{Linear consumption function}", fontsize=12)
    pdf.formula_block(r"\text{(3.3)} \quad C = c_0 + c_1(Y - T) \quad \text{Consumption (income and taxes)}", fontsize=12)
    pdf.formula_block(r"\text{(3.8)} \quad Y = \frac{1}{1 - c_1}\left[c_0 + \bar{I} + G - c_1 T\right] \quad \text{Equilibrium output}", fontsize=12)
    pdf.formula_block(r"\text{(3.10)} \quad I = S + (T - G) \quad \text{IS relation}", fontsize=12)
    pdf.formula_block(r"\text{(3.11)} \quad S = -c_0 + (1 - c_1)(Y - T) \quad \text{Private saving}", fontsize=12)
    pdf.formula_block(r"\text{(5.1)} \quad I = I(Y,\, i) \;\; (+,\, -) \quad \text{Investment function}", fontsize=12)
    pdf.formula_block(r"\text{(5.2)} \quad Y = C(Y - T) + I(Y,\, i) + G \quad \text{Goods mkt equilibrium}", fontsize=12)
    pdf.formula_block(r"\text{(14.1)} \quad V = z + \frac{z^e}{1+i} + \cdots \quad \text{Present discounted value}", fontsize=12)
    pdf.formula_block(r"\text{(14.4)} \quad \$P_{1t} = \frac{100}{1 + i_{1t}} \quad \text{1-year bond price}", fontsize=12)
    pdf.formula_block(r"\text{(14.5)} \quad \$P_{2t} = \frac{100}{(1+i_{1t})(1+i^e_{1,t+1})} \quad \text{2-year bond price}", fontsize=12)
    pdf.formula_block(r"\text{(14.12)} \quad i_{2t} \approx \frac{1}{2}(i_{1t} + i^e_{1,t+1}) \quad \text{Yield approximation}", fontsize=12)
    pdf.formula_block(r"V = \frac{z}{i} \quad \text{Perpetuity value}", fontsize=12)
    pdf.formula_block(r"\frac{1}{1 - c_1} \quad \text{The Multiplier}", fontsize=12)

    path = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/econ/KW9_The_Goods_Market.pdf'
    pdf.output(path)
    print(f"Generated: {path}")


def generate_kw10():
    """Generate KW 10 PDF: Financial Markets (Ch 4 + Ch 5.2 + Ch 5.3 + Lecture 3 slides)."""
    pdf = NotesPDF("KW 10: Financial Markets", "Ch 4, Ch 5.2, Ch 5.3 + Lecture 3")
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ===== LECTURE CONTEXT =====
    pdf.add_page()
    pdf.chapter_title("LECTURE 3 CONTEXT: FINANCIAL MARKET OVERVIEW")

    pdf.body_text("The financial market plays a central role in an economy. It is complementary to the goods market (covered in Lecture 2). A financial market is a generic term for any market in which trading of financial instruments takes place.")

    pdf.section_title("Financial Market Taxonomy")
    pdf.bullet("**Money market**: Short-term money supply and demand")
    pdf.bullet("**Bonds market** (also credit market): Financial assets and liabilities")
    pdf.bullet("**Capital market**: Medium and long-term capital requirements and supply")

    pdf.body_text("Simplifying assumption for this course: only two forms of assets exist - money and bonds. This allows us to understand how the interest rate is set and the role of the central bank.")
    pdf.bullet("**Money**: Can be used for transactions, but does not earn interest")
    pdf.bullet("**Bonds**: Yield an interest rate i, but cannot be used for transactions")
    pdf.bullet("Individuals choose what fraction of their wealth to hold as money vs. bonds")

    pdf.section_title("Learning Objectives (Lecture 3)")
    pdf.bullet("The role of money in the national economy")
    pdf.bullet("Money supply and demand")
    pdf.bullet("Monetary policy through central banks")
    pdf.bullet("Financial market for a model of the economy in the short run")
    pdf.bullet("Derivation of the LM curve for the IS-LM model")
    pdf.bullet("Literature: Blanchard, Chapters 4 and 5.2")

    pdf.section_title("What Is Money?")
    pdf.bullet("Three classical functions (from Microeconomics): medium of exchange, unit of account, means of storing value")
    pdf.bullet("Historically many forms: stones, shells, gold, receipts, cigarettes, Bitcoin, ...")
    pdf.bullet("Inflation affects the functioning of money (covered in Lecture 6)")

    pdf.section_title("Types of Money in a Modern Economy")
    pdf.body_text("Central banks measure money supply using monetary aggregates. Definitions used by the Swiss National Bank (SNB):")
    pdf.bullet("**Monetary base (M0)**: Banknotes in circulation + sight deposits of domestic commercial banks held at the SNB")
    pdf.bullet("**M1**: Currency + sight deposits in Swiss francs from residents")
    pdf.bullet("**M2**: M1 + savings deposits held at banks (excluding pillar 2/3a) in Swiss francs")
    pdf.bullet("**M3**: M2 + time deposits held at banks in Swiss francs")

    pdf.key_concept_box("SNB Money Aggregates (1990-2025)",
        "All three aggregates grew substantially since 1990. M3 (broadest) reached\n"
        "~1,100B CHF by 2025. M1 spiked around 2020 (pandemic monetary expansion),\n"
        "peaking near 800B CHF before declining. Monetary base is the smallest.")

    # CHAPTER 4
    pdf.add_page()
    pdf.chapter_title("CHAPTER 4: FINANCIAL MARKETS I")

    pdf.body_text("Financial markets determine the cost of funds for firms, households, and the government. The chapter simplifies to two financial assets: money (pays no interest) and bonds (pay interest rate i). Focus is on how the interest rate is determined and the role of the central bank.")

    pdf.key_concept_box("Semantic Traps: Money, Income, and Wealth",
        "Money: Currency + checkable deposits. Used for transactions. A STOCK variable.\n"
        "Income: What you earn (wages + interest + dividends). A FLOW variable.\n"
        "Saving: Part of after-tax income not spent. A FLOW.\n"
        "Financial wealth: All financial assets minus liabilities. A STOCK.\n"
        "Investment: Purchase of NEW capital goods (NOT financial assets).\n"
        "Financial investment: Purchase of shares/bonds.")

    pdf.section_title("4-1 The Demand for Money")

    pdf.subsection_title("The Portfolio Choice: Money vs. Bonds")
    pdf.bullet("**Money**: Can be used for transactions, pays no interest. Two types: currency (coins/bills) and checkable deposits (bank accounts with checks/debit cards)")
    pdf.bullet("**Bonds**: Pay positive interest rate i, but cannot be used directly for transactions. Transaction costs exist for buying/selling bonds.")
    pdf.bullet("You should hold BOTH: enough money for transactions, rest in bonds for interest")

    pdf.subsection_title("Two Key Determinants")
    pdf.bullet("**(1) Level of transactions**: More transactions -> need more money on hand. Roughly proportional to nominal income ($Y).")
    pdf.bullet("**(2) Interest rate on bonds**: Higher i -> more willing to deal with inconvenience of selling bonds -> hold less money. At very high rates, minimize money holdings.")

    pdf.subsection_title("The Money Demand Equation")
    pdf.formula_block(r"M^d = \$Y \cdot L(i) \quad \underset{(-)}{}")
    pdf.formula_block(r"M^d = \text{demand for money}", fontsize=11)
    pdf.formula_block(r"\$Y = \text{nominal income}", fontsize=11)
    pdf.formula_block(r"L(i) = \text{decreasing function of interest rate}", fontsize=11)
    pdf.bullet("Money demand increases **proportionally** to nominal income")
    pdf.bullet("Money demand depends **negatively** on the interest rate")
    pdf.bullet("What matters is NOMINAL income (not real) - if prices double, need twice as much money for same transactions")

    pdf.subsection_title("Figure 4-1: Money Demand Curve")
    pdf.bullet("Downward sloping: lower interest rate -> more money demanded")
    pdf.bullet("An increase in nominal income shifts the entire curve RIGHT (more money demanded at every interest rate)")
    pdf.bullet("At a given interest rate i, an increase in nominal income shifts the money demand curve to the RIGHT")
    pdf.bullet("Points along the curve: moving from low i to high i, money demand DECREASES (liquidity preference falls)")

    pdf.slide_figure('2026-Economics-B_Folien-03.pdf', 11,
        'Figure: Money Demand Curve — Downward-sloping M^d(PY) with points a, b, c at different interest rates')

    pdf.slide_figure('2026-Economics-B_Folien-03.pdf', 12,
        'Figure: Money Demand Shift — Increase in nominal income (PY\' > PY) shifts M^d curve to the right')

    pdf.subsection_title("Empirical Validation: Swiss Cash-Deposit Ratio (Lecture)")
    pdf.body_text("The lecture presents Swiss empirical data (1990-2025) showing the cash-holding coefficient alongside the return on 10-year Swiss government bonds:")
    pdf.formula_block(r"L(\hat{\imath}) = \frac{M^d}{PY} \quad \text{(cash-deposit ratio)}", fontsize=12)
    pdf.bullet("As the 10Y bond return fell from ~6% (early 1990s) to near 0% (2015-2020), the cash-holding coefficient INCREASED from ~30% to over 100%")
    pdf.bullet("This is consistent with the theory: lower interest rates -> higher money demand relative to income")
    pdf.bullet("When bonds pay almost nothing, the opportunity cost of holding money vanishes")

    pdf.key_concept_box("Who Holds U.S. Currency?",
        "Total U.S. currency in circulation: $750 billion (2006)\n"
        "U.S. households held only $170 billion\n"
        "~$500 billion (66%) held by FOREIGNERS\n"
        "Countries like Russia ($80B), Argentina ($50B+) hold dollars as safe assets\n"
        "Result: The rest of the world makes an interest-free loan to the U.S.")

    pdf.section_title("4-2 Determining the Interest Rate: I")
    pdf.body_text("Assumes only money is currency (central bank money). Checkable deposits introduced in 4-3.")

    pdf.subsection_title("Equilibrium Condition")
    pdf.formula_block(r"M = \$Y \cdot L(i)")
    pdf.bullet("The interest rate i must be such that people are willing to hold exactly the existing money supply M")

    pdf.subsection_title("Figure 4-2: Interest Rate Determination")
    pdf.bullet("Money demand curve: downward-sloping")
    pdf.bullet("Money supply curve: vertical line at M")
    pdf.bullet("Equilibrium at intersection point A")

    pdf.subsection_title("Effects of Changes in Nominal Income (Figure 4-3)")
    pdf.bullet("Increase in nominal income -> money demand shifts RIGHT -> interest rate INCREASES")
    pdf.bullet("Reason: at old rate, money demand > supply. Higher i reduces demand back to equilibrium")

    pdf.subsection_title("Effects of Increase in Money Supply (Figure 4-4)")
    pdf.bullet("Increase in M -> money supply shifts RIGHT -> interest rate DECREASES")
    pdf.bullet("Reason: lower i increases demand to match the now larger supply")

    pdf.subsection_title("Monetary Policy and Open Market Operations")
    pdf.bullet("Central bank changes money supply by **buying or selling bonds in the bond market**")
    pdf.bullet("**Open market operations**: transactions in the 'open market' for bonds")

    pdf.key_concept_box("Open Market Operations",
        "EXPANSIONARY OMO: Central bank BUYS bonds, pays with newly created money\n"
        "  -> Money supply increases -> Bond prices increase -> Interest rate DECREASES\n\n"
        "CONTRACTIONARY OMO: Central bank SELLS bonds, removes money from circulation\n"
        "  -> Money supply decreases -> Bond prices decrease -> Interest rate INCREASES")

    pdf.subsection_title("Central Bank Balance Sheet (Figure 4-5)")
    pdf.bullet("Assets: Bonds held by the central bank")
    pdf.bullet("Liabilities: Money (currency) in the economy")
    pdf.bullet("OMOs lead to equal changes in assets and liabilities")

    pdf.subsection_title("Bond Prices and Bond Yields")
    pdf.body_text("Consider a one-year bond (T-bill) with face value $100:")
    pdf.formula_block(r"i = \frac{\$100 - \$P_B}{\$P_B}")
    pdf.formula_block(r"\$P_B = \frac{\$100}{1 + i}")
    pdf.bullet("Higher bond price -> lower interest rate (and vice versa)")
    pdf.bullet("'Bond markets went up' = bond prices rose = interest rates fell")

    pdf.subsection_title("Interest Rates in Practice (Lecture)")
    pdf.body_text("Global context: Interest rates on 10-year government bonds fell worldwide for decades (USA, Germany, Japan, Switzerland). From peaks of 10-16% in the early 1980s, rates declined to near zero or even negative by 2020.")
    pdf.bullet("**Zero lower bound**: How negative can an interest rate be?")
    pdf.bullet("Cash pays zero interest, but holding it causes costs (storage, insurance, theft risk)", level=1)
    pdf.bullet("In practice, rates went slightly negative in Europe and Japan (investors accepted small losses for safety)", level=1)

    pdf.subsection_title("Choosing Money or Choosing the Interest Rate?")
    pdf.body_text("The lecture presents these as two distinct equilibrium regimes with equal importance:")

    pdf.sub_subsection_title("Regime 1: Money Supply Control")
    pdf.bullet("The central bank provides money supply M, so that M = M_S")
    pdf.bullet("The interest rate is determined endogenously in equilibrium")
    pdf.formula_block(r"M^s = M^d \quad \Longleftrightarrow \quad M^s = PY \cdot L(i)", fontsize=12)
    pdf.bullet("Graph: vertical M_S line intersects downward-sloping M_d curve at equilibrium point A")

    pdf.slide_figure('2026-Economics-B_Folien-03.pdf', 17,
        'Figure: Money Market Equilibrium — Money Supply Control (vertical M^s intersects M^d at point A)')

    pdf.sub_subsection_title("Regime 2: Interest Rate Control")
    pdf.bullet("The central bank sets the interest rate to i_0")
    pdf.bullet("The money supply is determined endogenously: the central bank provides as much money as demanded at i_0")
    pdf.formula_block(r"M^d(i_0) = M^s \quad \text{(money supply adjusts to demand at } i_0 \text{)}", fontsize=12)
    pdf.bullet("Graph: horizontal line at i_0 intersects downward-sloping M_d curve at equilibrium point A")

    pdf.slide_figure('2026-Economics-B_Folien-03.pdf', 18,
        'Figure: Money Market Equilibrium — Interest Rate Control (horizontal i_0 intersects M^d at point A)')

    pdf.subsection_title("Expansionary Monetary Policy: Both Regimes (Lecture)")
    pdf.body_text("The lecture shows both regimes side by side for an expansionary policy:")

    pdf.sub_subsection_title("Under Money Supply Control")
    pdf.bullet("Central bank increases money supply from M_1 to M_2 (supply curve shifts right)")
    pdf.bullet("Equilibrium interest rate falls from i_1 to i_2")
    pdf.bullet("Money demand rises accordingly")
    pdf.bullet("The interest rate is determined **endogenously**")

    pdf.sub_subsection_title("Under Interest Rate Control")
    pdf.bullet("Central bank aims for a lower interest rate: reduces i from i_1 to i_2")
    pdf.bullet("At the lower rate, money demand increases from M_1 to M_2")
    pdf.bullet("Central bank increases money supply to M_2 to satisfy demand")
    pdf.bullet("The money supply is determined **endogenously**")

    pdf.slide_figure('2026-Economics-B_Folien-03.pdf', 20,
        'Figure: Expansionary Monetary Policy — Money supply control (left) vs. Interest rate control (right), A1 -> A2')

    pdf.key_concept_box("Equivalence of the Two Descriptions",
        "Money supply control and interest rate control produce the SAME outcome.\n"
        "Modern central banks think in terms of choosing the interest rate.\n"
        "News says: 'The Fed decided to increase the interest rate'\n"
        "(not 'decrease the money supply').\n"
        "Historically: money supply targeting (late 1970s to early 1990s),\n"
        "then shift to interest rate targeting (since the early 1990s),\n"
        "with QE revival of money supply operations for long-term bonds.")

    pdf.section_title("4-3 Determining the Interest Rate: II (With Banks)")
    pdf.body_text("In reality, money includes currency AND checkable deposits. Checkable deposits are supplied by private banks, not the central bank.")

    pdf.subsection_title("What Banks Do")
    pdf.bullet("Banks are **financial intermediaries** - receive funds and use them to buy assets or make loans")
    pdf.bullet("Special because their liabilities are money (checkable deposits)")

    pdf.subsection_title("Bank Balance Sheet (Figure 4-6)")
    widths = [45, 45]
    pdf.table_header(["Assets", "Liabilities"], widths)
    pdf.table_row(["Reserves", "Checkable deposits"], widths, True)
    pdf.table_row(["Loans (~70%)", ""], widths)
    pdf.table_row(["Bonds (~30%)", ""], widths, True)
    pdf.ln(3)

    pdf.subsection_title("Reserves")
    pdf.bullet("Banks keep some funds as reserves (cash + deposits at central bank)")
    pdf.bullet("Three reasons: (1) daily cash flow mismatches, (2) interbank check clearing, (3) **reserve requirements**")
    pdf.bullet("U.S. reserve requirement: at least **10% of checkable deposits**")

    pdf.subsection_title("Central Bank Money (The Monetary Base)")
    pdf.formula_block(r"H = CU + R \quad \text{(Central Bank Money = Currency + Reserves)}", fontsize=13)

    pdf.subsection_title("Demand for Central Bank Money")
    pdf.body_text("Simplifying assumption: people hold only checkable deposits (no currency).")
    pdf.bullet("Demand for checkable deposits = demand for money by people:")
    pdf.formula_block(r"M^d = \$Y \cdot L(i)")
    pdf.body_text("Demand for reserves by banks (theta = reserve ratio):")
    pdf.formula_block(r"H^d = \theta \cdot M^d = \theta \cdot \$Y \cdot L(i)")

    pdf.subsection_title("Equilibrium")
    pdf.formula_block(r"H = \theta \cdot \$Y \cdot L(i)")
    pdf.bullet("H = supply of central bank money (controlled by central bank via OMOs)")
    pdf.bullet("Same qualitative results as before: increase in H -> lower interest rate")

    pdf.key_concept_box("Federal Funds Market and Federal Funds Rate",
        "In the U.S., banks trade reserves in the FEDERAL FUNDS MARKET.\n"
        "The interest rate in this market = FEDERAL FUNDS RATE.\n"
        "This is the main indicator of U.S. monetary policy.\n"
        "Changes in the federal funds rate make front-page news.")

    pdf.section_title("4-4 The Liquidity Trap")

    pdf.subsection_title("The Zero Lower Bound")
    pdf.bullet("The interest rate on bonds **cannot be negative** -> the **zero lower bound (ZLB)**")
    pdf.bullet("When i = 0, monetary policy cannot decrease it further -> **liquidity trap**")

    pdf.subsection_title("Why the Zero Lower Bound Exists")
    pdf.bullet("At i = 0, both money and bonds pay the same interest rate: zero")
    pdf.bullet("People are **indifferent** between holding money or bonds")
    pdf.bullet("Additional money supply is simply absorbed without lowering rates")

    pdf.subsection_title("Figure 4-8: The Liquidity Trap")
    pdf.bullet("Money demand curve becomes **horizontal at i = 0**")
    pdf.bullet("If money supply is at/beyond the flat portion: interest rate = 0")
    pdf.bullet("Further increases in money supply have NO effect on interest rate")
    pdf.bullet("Monetary policy is **ineffective** in the liquidity trap")

    pdf.key_concept_box("The Liquidity Trap in Practice",
        "During the 2008 crisis:\n"
        "- Bank of England cut rate from 5% to 0.5%\n"
        "- Bank reserves expanded from 23.6B to 265.5B pounds\n"
        "- Rate remained at 0.5% despite massive money expansion\n"
        "- This is exactly what liquidity trap theory predicts")

    pdf.subsection_title("Money Creation by Commercial Banks (Lecture Detail)")
    pdf.body_text("The lecture uses the following notation for money creation:")
    pdf.formula_block(r"M = \text{money supply}, \quad H = \text{central bank money (high-powered money, M0)}", fontsize=11)
    pdf.formula_block(r"CU = \text{cash in circulation}, \quad D = \text{deposits of non-banks}", fontsize=11)
    pdf.formula_block(r"R = \text{reserves}, \quad \theta = \text{reserve ratio}, \quad b = \text{cash proportion}", fontsize=11)

    pdf.body_text("In an economy with commercial banks, the central bank can only control the monetary base H directly. The money supply M is controlled indirectly.")

    pdf.sub_subsection_title("Why Banks Hold Reserves")
    pdf.bullet("Deposits and withdrawals are not equal - banks must hold cash on hand")
    pdf.bullet("To cover debts to other banks")
    pdf.bullet("To fulfill legal **reserve requirements**")
    pdf.bullet("Reserve ratio: banks hold fraction theta of deposits as reserves")
    pdf.formula_block(r"R = \theta \cdot D", fontsize=12)

    pdf.sub_subsection_title("The Money Creation Multiplier (Geometric Series)")
    pdf.body_text("The monetary base H consists of cash in circulation plus reserves:")
    pdf.formula_block(r"H = CU + R \quad \Longleftrightarrow \quad H = CU + \theta D")
    pdf.body_text("Cash and deposits are fixed proportions b and (1-b) of total money M:")
    pdf.formula_block(r"CU = b \cdot M, \qquad D = (1-b) \cdot M", fontsize=12)
    pdf.body_text("If the central bank increases H by one unit, how does this affect M?")
    pdf.bullet("The commercial bank can lend a fraction (1-theta) of the deposit")
    pdf.bullet("Of that loan, fraction (1-b) flows back into the banking system as new deposits")
    pdf.bullet("This process continues indefinitely, yielding a geometric series:")
    pdf.formula_block(r"1 + (1-\theta)(1-b) + [(1-\theta)(1-b)]^2 + \ldots = \frac{1}{1-(1-\theta)(1-b)}", fontsize=12)
    pdf.body_text("The money creation multiplier result:")
    pdf.formula_block(r"M = \frac{1}{b + \theta(1-b)} \cdot H")
    pdf.bullet("The multiplier is always > 1 (since b < 1 and theta < 1)")

    pdf.sub_subsection_title("Textbook Notation (Blanchard)")
    pdf.body_text("Blanchard uses c instead of b for the cash proportion. The formulas are equivalent:")
    pdf.formula_block(r"CU^d = c \cdot M^d, \quad D^d = (1-c) \cdot M^d, \quad R^d = \theta(1-c) \cdot M^d", fontsize=12)
    pdf.body_text("Demand for central bank money:")
    pdf.formula_block(r"H^d = \left[c + \theta(1-c)\right] \cdot \$Y \cdot L(i)")
    pdf.body_text("Equilibrium:")
    pdf.formula_block(r"H = \left[c + \theta(1-c)\right] \cdot \$Y \cdot L(i)")
    pdf.body_text("Money multiplier (textbook):")
    pdf.formula_block(r"M = \frac{H}{c + \theta(1-c)} = \text{Money Multiplier} \times H")
    pdf.formula_block(r"\text{Money multiplier} = \frac{1}{c + \theta(1-c)} > 1", fontsize=12)
    pdf.bullet("Example:")
    pdf.formula_block(r"c = 0.4, \;\; \theta = 0.1 \quad \Longrightarrow \quad \text{multiplier} = \frac{1}{0.46} = 2.2", fontsize=11)
    pdf.bullet("Each dollar of central bank money leads to $2.20 of total money")

    pdf.subsection_title("Central Bank Control Channels (Lecture)")
    pdf.body_text("With commercial banks, the central bank controls money supply through three channels:")
    pdf.bullet("**Policy rate** (0.00% in Jan 2026): The price at which commercial banks can obtain central bank money")
    pdf.bullet("**Deposit rate** (0.00% in Jan 2026): Interest on deposits by commercial banks with the central bank")
    pdf.bullet("**Minimum reserve rate** (4.00% in Jan 2026): Compulsory reserve balances of commercial banks with the central bank")
    pdf.body_text("The central bank indirectly influences the volume of lending by commercial banks and thus the amount of their deposits and the money supply M.")

    pdf.key_concept_box("SNB Monetary Policy in Practice (Lecture)",
        "In October 2022, the SNB had to intervene directly in the market\n"
        "because the SARON (Swiss Average Rate Overnight) differed from\n"
        "the SNB policy rate. The SARON is the actual market rate at which\n"
        "banks lend to each other overnight. When SARON diverges from the\n"
        "policy rate, the central bank must act to restore the transmission\n"
        "mechanism of monetary policy.")

    # CHAPTER 5.2
    pdf.add_page()
    pdf.chapter_title("CHAPTER 5, SECTION 5-2: Financial Markets and the LM Relation")

    pdf.section_title("Why the IS-LM Model? (Lecture)")
    pdf.body_text("Repetition from Lecture 2: the goal is a simple model of the economy in the short run.")
    pdf.bullet("In the last lecture: balance on the goods market (implicit IS curve)")
    pdf.formula_block(r"Y = c_0 + c_1(Y - T) + I(Y, i) + G", fontsize=12)
    pdf.bullet("On the basis of today's lecture we can add i as an equilibrium result from the financial market")
    pdf.bullet("IS-LM model in the diagram with i and Y on the axes")
    pdf.bullet("Equilibrium in the financial market in the diagram: the **LM curve**")
    pdf.bullet("'LM' stands for **liquidity** and **money supply**")

    pdf.section_title("The LM Relation")
    pdf.body_text("From Chapter 4, the interest rate is determined by money market equilibrium:")
    pdf.formula_block(r"M = PY \cdot L(i)")
    pdf.body_text("Dividing both sides by the price level P to get real terms:")
    pdf.formula_block(r"\frac{M}{P} = Y \cdot L(i)")
    pdf.bullet("**Real money supply** = money stock in terms of goods:")
    pdf.formula_block(r"\text{Real money supply} = \frac{M}{P}", fontsize=12)
    pdf.bullet("**Real money demand** depends on real income Y and interest rate i")
    pdf.bullet("Note: in the short term, the price level P is fixed")
    pdf.bullet("If the money market is in equilibrium, the bonds market will be as well (Walras' law)")

    pdf.subsection_title("Deriving the LM Curve: Two Regimes")
    pdf.body_text("The lecture derives the LM curve under both regimes with equal emphasis:")

    pdf.sub_subsection_title("Regime 1: Interest Rate Control (Modern, Horizontal LM)")
    pdf.bullet("Central bank sets the interest rate to i_0")
    pdf.bullet("The central bank endogenously adjusts the supply of money to the demand for money at that rate")
    pdf.bullet("If income rises from Y_1 to Y_2, money demand increases")
    pdf.bullet("The central bank increases money supply from M_1 to M_2 to maintain i_0")
    pdf.bullet("Result: the LM curve is a **horizontal line** at i_0")
    pdf.formula_block(r"\text{LM curve (interest rate control):} \quad i = \bar{\imath}_0", fontsize=12)
    pdf.bullet("Graph: left panel shows money market (M_S shifts right to match higher M_d), right panel shows flat LM line with points A (Y_1) and B (Y_2) both at i_0")

    pdf.slide_figure('2026-Economics-B_Folien-03.pdf', 28,
        'Figure: LM Curve Derivation — Interest Rate Control: money market (left) and horizontal LM(i_0) curve (right)')

    pdf.sub_subsection_title("Regime 2: Money Supply Control (Traditional, Upward-Sloping LM)")
    pdf.bullet("Central bank keeps money supply M_S constant")
    pdf.bullet("If income rises from Y to Y', money demand increases (curve shifts right)")
    pdf.bullet("With constant M_S, the interest rate must INCREASE from i_A to i_B to restore equilibrium")
    pdf.bullet("Result: the LM curve is **upward-sloping** - higher income requires higher interest rate")
    pdf.formula_block(r"\text{LM curve (money supply control):} \quad \frac{M}{P} = Y \cdot L(i)", fontsize=12)
    pdf.bullet("Graph: left panel shows money market (M_d shifts right along fixed M_S), right panel shows upward-sloping LM curve with points A (Y, i_A) and B (Y', i_B)")

    pdf.slide_figure('2026-Economics-B_Folien-03.pdf', 29,
        'Figure: LM Curve Derivation — Money Supply Control: money market (left) and upward-sloping LM(M/P) curve (right)')

    pdf.key_concept_box("The LM Curve: Summary (Lecture Slide 30)",
        "The textbook (usually) assumes the central bank controls interest rates,\n"
        "and therefore uses a flat LM curve.\n\n"
        "Summary of positions relative to the LM curve:\n"
        "- ABOVE the LM curve: excess supply on the money market\n"
        "- BELOW the LM curve: excess demand on the money market\n"
        "- ON the LM curve: equilibrium on the money market\n\n"
        "The bonds market is the mirror image of the money market.\n"
        "The LM curve also describes the balance on the bonds market.")

    # CHAPTER 5.3
    pdf.add_page()
    pdf.chapter_title("CHAPTER 5, SECTION 5-3: Putting the IS and LM Relations Together")

    pdf.section_title("The IS-LM Model")
    pdf.body_text("Two relations that jointly determine output and the interest rate:")

    pdf.formula_block(r"\text{IS:} \quad Y = C(Y - T) + I(Y,\, i) + G")
    pdf.formula_block(r"\text{LM:} \quad i = \bar{\imath}")

    pdf.subsection_title("Figure 5-5: The IS-LM Model")
    pdf.bullet("IS curve: downward sloping (higher i -> lower Y)")
    pdf.bullet("LM curve: horizontal line at i-bar")
    pdf.bullet("Equilibrium at intersection (point A): both goods market and financial markets are in equilibrium")

    pdf.section_title("Fiscal Policy in the IS-LM Model")

    pdf.subsection_title("An Increase in Taxes (Figure 5-6)")
    pdf.bullet("Higher T -> lower disposable income -> lower consumption -> lower demand -> lower output")
    pdf.bullet("IS curve shifts LEFT (from IS to IS')")
    pdf.bullet("LM curve unchanged (central bank keeps i-bar)")
    pdf.bullet("Result: Output DECREASES, interest rate UNCHANGED")
    pdf.bullet("Similarly: increase in G shifts IS RIGHT -> output increases, rate unchanged")

    pdf.section_title("Monetary Policy in the IS-LM Model")

    pdf.subsection_title("An Increase in the Interest Rate (Figure 5-7)")
    pdf.bullet("Central bank raises rate from i-bar to i-bar'")
    pdf.bullet("IS curve does NOT shift")
    pdf.bullet("LM curve shifts UP (from LM to LM')")
    pdf.bullet("Economy moves along the IS curve to new equilibrium")
    pdf.bullet("Result: Output DECREASES, interest rate INCREASES")
    pdf.bullet("Mechanism: higher i -> lower investment -> lower demand -> lower output (multiplier effect)")

    pdf.key_concept_box("Policy Mix: Summary of Effects",
        "| Policy Change         | IS    | LM    | i       | Y        |\n"
        "|----------------------|-------|-------|---------|---------|\n"
        "| Increase T           | LEFT  | Same  | Same    | DOWN    |\n"
        "| Decrease T           | RIGHT | Same  | Same    | UP      |\n"
        "| Increase G           | RIGHT | Same  | Same    | UP      |\n"
        "| Decrease G           | LEFT  | Same  | Same    | DOWN    |\n"
        "| Raise i-bar (tight)  | Same  | UP    | UP      | DOWN    |\n"
        "| Lower i-bar (loose)  | Same  | DOWN  | DOWN    | UP      |")

    pdf.body_text("Both fiscal policy (G, T shifting the IS curve) and monetary policy (i-bar shifting the LM curve) can affect output. The combination of these two policies - the policy mix - determines the overall outcome.")

    # Summary of Key Formulas
    pdf.add_page()
    pdf.chapter_title("SUMMARY OF KEY EQUATIONS AND TERMS")

    pdf.section_title("Core Equations")
    pdf.formula_block(r"\text{(4.1)} \quad M^d = PY \cdot L(i) \quad \text{Money demand}", fontsize=12)
    pdf.formula_block(r"\text{(4.2)} \quad M = PY \cdot L(i) \quad \text{Money market equilibrium}", fontsize=12)
    pdf.formula_block(r"\text{(4.4)} \quad H^d = \theta \cdot PY \cdot L(i) \quad \text{Reserves demand (no currency)}", fontsize=12)
    pdf.formula_block(r"\text{(4.6)} \quad H = \theta \cdot PY \cdot L(i) \quad \text{Central bank money equilibrium}", fontsize=12)
    pdf.formula_block(r"i = \frac{100 - P_B}{P_B} \quad \text{Interest rate from bond price}", fontsize=12)
    pdf.formula_block(r"P_B = \frac{100}{1 + i} \quad \text{Bond price from interest rate}", fontsize=12)
    pdf.formula_block(r"R = \theta \cdot D \quad \text{Reserves = reserve ratio} \times \text{deposits}", fontsize=12)
    pdf.formula_block(r"H = CU + R \quad \text{Monetary base = cash + reserves}", fontsize=12)

    pdf.section_title("Money Creation")
    pdf.formula_block(r"\text{(Lecture)} \quad M = \frac{1}{b + \theta(1-b)} \cdot H \quad \text{Money multiplier (lecture notation)}", fontsize=12)
    pdf.formula_block(r"\text{(Blanchard)} \quad M = \frac{H}{c + \theta(1-c)} \quad \text{Money multiplier (textbook notation)}", fontsize=12)
    pdf.formula_block(r"\text{(4.A9)} \quad H = \left[c + \theta(1-c)\right] \cdot \$Y \cdot L(i) \quad \text{General equilibrium}", fontsize=12)

    pdf.section_title("IS-LM Model")
    pdf.formula_block(r"\text{(5.2)} \quad Y = C(Y-T) + I(Y,\,i) + G \quad \text{IS relation}", fontsize=12)
    pdf.formula_block(r"\text{(5.3)} \quad \frac{M}{P} = Y \cdot L(i) \quad \text{LM relation (real terms)}", fontsize=12)
    pdf.formula_block(r"\text{(5.4)} \quad i = \bar{\imath} \quad \text{LM curve (interest rate control, horizontal)}", fontsize=12)
    pdf.formula_block(r"\text{LM:} \quad \frac{M}{P} = Y \cdot L(i) \quad \text{(money supply control, upward-sloping)}", fontsize=12)

    pdf.ln(5)
    pdf.section_title("Key Terms")
    terms = [
        ("Federal Reserve (Fed)", "The U.S. central bank"),
        ("Swiss National Bank (SNB)", "The Swiss central bank; uses SARON as key market rate"),
        ("Open Market Operation (OMO)", "Central bank buying/selling bonds to change money supply"),
        ("Expansionary OMO", "Buy bonds -> increase M -> decrease i"),
        ("Contractionary OMO", "Sell bonds -> decrease M -> increase i"),
        ("Quantitative Easing (QE)", "OMOs for long-term bonds; revival since 2008"),
        ("Forward guidance", "Central bank expectation management regarding future policy"),
        ("Treasury bill (T-bill)", "Government bond with maturity < 1 year"),
        ("Central bank money (H)", "Currency + Reserves (= Monetary Base = High-powered money = M0)"),
        ("Reserve ratio (theta)", "Reserves / Checkable deposits (min 10% in U.S., 4% SNB)"),
        ("SARON", "Swiss Average Rate Overnight; actual interbank lending rate in Switzerland"),
        ("Federal funds rate", "Interest rate in the federal funds market; main U.S. policy indicator"),
        ("Zero lower bound (ZLB)", "Interest rates cannot go (much) below zero"),
        ("Liquidity trap", "At i=0, more money has no effect on interest rate"),
        ("IS curve", "Downward-sloping: all (i,Y) pairs where goods market is in equilibrium"),
        ("LM curve (modern)", "Horizontal line at i-bar; financial market equilibrium under interest rate control"),
        ("LM curve (traditional)", "Upward-sloping; financial market equilibrium under money supply control"),
        ("Money multiplier", "Total money as multiple of central bank money: 1/(c + theta(1-c))"),
        ("Real money supply", "Money stock measured in terms of goods: M/P"),
        ("Policy mix", "Combination of fiscal and monetary policy"),
        ("Monetary aggregates", "M0 (base), M1, M2, M3 - progressively broader definitions of money"),
        ("Money supply control", "Central bank sets M, interest rate adjusts endogenously"),
        ("Interest rate control", "Central bank sets i, money supply adjusts endogenously"),
    ]
    for term, defn in terms:
        pdf.bullet(f"**{term}**: {defn}")

    pdf.ln(3)
    pdf.body_text("Key formulas for quick reference:")
    pdf.formula_block(r"\text{Money multiplier} = \frac{1}{c + \theta(1-c)} > 1", fontsize=12)
    pdf.formula_block(r"\text{Real money supply} = \frac{M}{P}", fontsize=12)
    pdf.formula_block(r"\text{Bond price} \uparrow \;\Longleftrightarrow\; \text{Interest rate} \downarrow", fontsize=12)

    path = '/Users/roberthaeussler/Claude Coding/Apps/uni tracker/notes/econ/KW10_Financial_Markets.pdf'
    pdf.output(path)
    print(f"Generated: {path}")


if __name__ == "__main__":
    generate_kw8()
    generate_kw9()
    generate_kw10()
    print("\nAll PDFs generated successfully!")
