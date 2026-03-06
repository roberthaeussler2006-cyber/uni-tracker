#!/usr/bin/env python3
"""Generate PDF notes for Constitutional Law Lectures 1, 2, and 3."""

import sys
sys.path.insert(0, '/Users/roberthaeussler/Library/Python/3.9/lib/python/site-packages')

from fpdf import FPDF
import re
import os


class NotesPDF(FPDF):
    """Custom PDF class for generating law study notes."""

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
        self.set_text_color(0, 80, 40)
        self.multi_cell(0, 12, self.title_text, align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, self.subtitle_text, align="C")
        self.ln(15)
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 7, "P. Egli - Introduction to Swiss Constitutional Law, 3rd Edition", align="C")
        self.ln(5)
        self.multi_cell(0, 7, "Study Notes", align="C")
        self.set_text_color(0, 0, 0)

    def chapter_title(self, text):
        self.ln(6)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(0, 80, 40)
        self.multi_cell(0, 9, text)
        self.set_draw_color(0, 80, 40)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def section_title(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 100, 60)
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
        bullet_char = "-" if level == 0 else ">"
        self.set_font("Helvetica", "", 10)
        self.cell(5, 5, bullet_char)
        self.set_x(self.l_margin + indent + 5)
        self._write_rich_text(text, indent=indent + 5)
        self.ln(1.5)

    def remember_box(self, title, items):
        """Green 'Remember' box for key concepts."""
        self.ln(3)
        self.set_fill_color(230, 245, 235)
        self.set_draw_color(0, 120, 60)
        x = self.l_margin + 3
        w = self.w - self.l_margin - self.r_margin - 6
        self.set_x(x)
        self.set_font("Helvetica", "B", 10)
        self.cell(w, 7, "  " + title, fill=True, border="LTR")
        self.ln()
        self.set_font("Helvetica", "", 9)
        for item in items:
            self.set_x(x)
            # Write each item with rich text support
            self.set_x(x + 3)
            text = "- " + item
            self._write_rich_text_cell(text, w - 6, fill_color=(230, 245, 235), border="LR")
        self.set_x(x)
        self.cell(w, 2, "", fill=True, border="LBR")
        self.ln(3)

    def key_concept_box(self, title, text):
        self.ln(3)
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(200, 170, 80)
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

    def article_box(self, articles):
        """Blue box for listing key constitutional articles."""
        self.ln(3)
        self.set_fill_color(230, 240, 255)
        self.set_draw_color(40, 80, 160)
        x = self.l_margin + 3
        w = self.w - self.l_margin - self.r_margin - 6
        self.set_x(x)
        self.set_font("Helvetica", "B", 10)
        self.cell(w, 7, "  Key Constitutional Articles", fill=True, border="LTR")
        self.ln()
        self.set_font("Helvetica", "", 9)
        for art in articles:
            self.set_x(x + 3)
            self._write_rich_text_cell("- " + art, w - 6, fill_color=(230, 240, 255), border="LR")
        self.set_x(x)
        self.cell(w, 2, "", fill=True, border="LBR")
        self.ln(3)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 80, 40)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6, col, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)

    def table_row(self, cols, widths, fill=False):
        self.set_font("Helvetica", "", 9)
        if fill:
            self.set_fill_color(230, 245, 235)
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

    def _write_rich_text_cell(self, text, width, fill_color=None, border=""):
        """Write rich text in a filled cell area."""
        if fill_color:
            self.set_fill_color(*fill_color)
        parts = re.split(r'(\*\*.*?\*\*)', text)
        start_x = self.get_x()
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.set_font("Helvetica", "B", 9)
                content = part[2:-2]
            else:
                self.set_font("Helvetica", "", 9)
                content = part
            if content:
                self.write(5, content)
        self.ln(5)


# ============================================================
# LECTURE 1: Introduction, Historical Development, Sources
# ============================================================

def generate_lecture1():
    """Generate Lecture 1 PDF: Introduction, Historical Development, Sources of Constitutional Law."""
    pdf = NotesPDF("Lecture 1: Introduction to Constitutional Law",
                   "Chapters A, B & C (pp. 1-23)")
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ---- CHAPTER A: INTRODUCTION ----
    pdf.add_page()
    pdf.chapter_title("CHAPTER A: INTRODUCTION")

    pdf.remember_box("Remember", [
        "A **constitution** is a set of fundamental principles and rules according to which a state is governed.",
        "**Constitutional law** refers to a set of basic legal principles and rules that define the nature, function and organization of a state.",
    ])

    pdf.body_text("The **Federal Constitution of the Swiss Confederation of 18 April 1999** features all essential elements of a modern constitutional state. It defines the main features of the state order, regulates the organization and workings of state organs, and assigns legal rights to individuals, thereby limiting state power.")

    pdf.body_text("As the basic legal order, the Constitution **takes precedence over all other legal norms** and may be modified only through a specific procedure. It is the supreme legal act forming the legal basis for all legislation.")

    pdf.section_title("1. Terms and Definitions")

    pdf.remember_box("Remember", [
        "The constitution in the **formal sense** encompasses all legal provisions enacted in the special enactment procedure of the constitution.",
        "The constitution in the **substantive sense** encompasses all essential legal principles concerning the nature of the state and its relation to individuals.",
    ])

    pdf.subsection_title("1.1 Constitution in the Formal Sense")
    pdf.bullet("Focuses on the **form/process** in which legal norms are enacted")
    pdf.bullet("Constitutional norms are enacted by a **special procedure** that differs from ordinary legislation")
    pdf.bullet("This guarantees constitutional stability and higher democratic legitimacy")
    pdf.bullet("In Switzerland, the Constitution consists of one single written document")
    pdf.bullet("Can be totally or partially revised at any time (**Art. 192 para. 1 Cst**)")
    pdf.bullet("All constitutional provisions require a **mandatory referendum** approved by the majority of the people AND the majority of the cantons (**Art. 140 para. 1 lit. a, Art. 142 para. 2, Art. 195 Cst**)")

    pdf.subsection_title("Hierarchy of Legislation")
    widths = [60, 60]
    pdf.table_header(["Level", "Democratic Legitimacy"], widths)
    pdf.table_row(["Federal Constitution", "Highest (double majority)"], widths, True)
    pdf.table_row(["Federal statutes", "Optional referendum"], widths)
    pdf.table_row(["Federal ordinances", "No referendum"], widths, True)
    pdf.table_row(["Cantonal constitutions", "Cantonal procedures"], widths)
    pdf.table_row(["Cantonal statutes", "Cantonal procedures"], widths, True)
    pdf.table_row(["Cantonal ordinances", "No referendum"], widths)
    pdf.table_row(["Communal legal acts", "Communal procedures"], widths, True)
    pdf.ln(3)

    pdf.subsection_title("1.2 Constitution in the Substantive Sense")
    pdf.bullet("Focuses on the **content** of legal norms, not the form")
    pdf.bullet("Encompasses all essential rules and fundamental principles on the nature of the state")
    pdf.bullet("Includes both written and unwritten rules of constitutional dimension")
    pdf.bullet("Fundamental principles: rules on **organization and powers**, **fundamental rights**, **procedures** for enactment, **competencies** in a federal state")

    pdf.subsection_title("1.3 Formal and Substantive Sense Compared")
    pdf.bullet("In most states, the two senses correspond but may not be fully congruent")
    pdf.bullet("Some formal provisions may be obsolete; some substantive principles may be unwritten")
    pdf.bullet("The **Swiss Constitution of 1999** ('Nachfuhrung') aimed to eliminate provisions of minor importance and include previously unwritten principles")
    pdf.bullet("In Switzerland, the formal and substantive senses now **coincide on essential points**")
    pdf.bullet("Contrast: The **UK** has no constitution in the formal sense but does in the substantive sense; the **US** has case law (e.g., judicial review from Marbury v. Madison) as part of the substantive constitution")

    pdf.subsection_title("1.4 Flexibility of Constitutions")
    pdf.bullet("**Rigid constitutions**: harder to change than ordinary legislation (e.g., US, Germany, Switzerland)")
    pdf.bullet("**Flexible constitutions**: no special amendment procedure (e.g., UK)")
    pdf.bullet("Switzerland: revision must only respect **mandatory norms of international law (jus cogens)** -- Art. 193 para. 4, Art. 194 para. 2 Cst")
    pdf.bullet("**Jus cogens** includes: prohibition of genocide, slavery, torture, wars of aggression, and non-refoulement", level=1)

    pdf.section_title("2. Functions of a Constitution")

    pdf.subsection_title("2.1 Constitutional Conceptions")
    pdf.bullet("**Instrumental conception**: only provisions on state organization")
    pdf.bullet("**Substantive conception**: also defines core values, fundamental rights, state goals")
    pdf.bullet("Most modern constitutions follow the **substantive conception**")

    pdf.subsection_title("2.2 Three Main Functions")
    pdf.bullet("**Order and Organization**: specifies how the state is constituted, creates organs, describes powers (e.g., Art. 148 para. 1 Cst -- Federal Assembly as supreme authority)")
    pdf.bullet("**Limits of Power and Guarantees of Freedom**: delimits state powers to guarantee fundamental freedoms; restricts abuse of power (Chapter One, Title Two of the Constitution)")
    pdf.bullet("**Creation and Direction**: describes basic substantive goals; sets direction for future state action (e.g., Art. 2 para. 1 Cst -- liberty, rights, independence, security)")

    # ---- CHAPTER B: HISTORICAL DEVELOPMENT ----
    pdf.add_page()
    pdf.chapter_title("CHAPTER B: HISTORICAL DEVELOPMENT")

    pdf.remember_box("Remember", [
        "The Swiss Confederation dates back to an alliance of independent territories in **1291**.",
        "After French conquest: **Helvetic Republic** (1798-1803) as centralized state.",
        "**Mediation Act of 1803** restored cantons; **Restoration** (1814-1830) with 22 cantons.",
        "**Regeneration** (1830-1848): Sonderbund-Krieg 1847 led to the **Federal Constitution of 1848**.",
        "**Constitution of 1874** broadened federal powers; **Constitution of 1999** consolidated all developments.",
    ])

    pdf.section_title("1. Before 1798: The Old Confederation")
    pdf.bullet("1291: **Bundesbrief** between Uri, Schwyz, and Unterwalden -- mutual assistance pact")
    pdf.bullet("Growth to eight members: Lucerne (1332), Zurich (1351), Glarus (1352), Zug (1352), Bern (1353)")
    pdf.bullet("Five more: Fribourg & Solothurn (1481), Basel & Schaffhausen (1501), Appenzell (1513)")
    pdf.bullet("Old Confederation = **league of sovereign states**, focused on defense and arbitration")
    pdf.bullet("The **Diet (Tagsatzung)** was a council of ambassadors, not a central government; decisions required unanimity")

    pdf.section_title("2. Helvetic Republic (1798-1803)")
    pdf.bullet("1798: French invasion transformed Switzerland into a **unitary state**")
    pdf.bullet("Territory divided into administrative cantons modeled on French departements")
    pdf.bullet("Unitary structure quickly disintegrated into civil war")
    pdf.bullet("French legacy: ideals of **equality, division of powers, popular sovereignty**")

    pdf.section_title("3. Mediation (1803-1813)")
    pdf.bullet("**Napoleon** restored the Confederation via the **Mediation Act of 1803**")
    pdf.bullet("13 original cantons regained sovereignty; 6 new cantons: St. Gallen, Graubunden, Aargau, Thurgau, Ticino, Vaud")
    pdf.bullet("19 cantons total; limited confederate powers (foreign relations, defense)")

    pdf.section_title("4. Restoration (1814-1830)")
    pdf.bullet("Three new territories: **Valais, Neuchatel, Geneva** (now 22 cantons)")
    pdf.bullet("**Confederate Treaty of 7 August 1815**: loose framework for 22 cantons")
    pdf.bullet("**Congress of Vienna (1815)**: recognized Swiss frontiers and **perpetual neutrality**")

    pdf.section_title("5. Regeneration (1830-1848)")
    pdf.bullet("Liberal cantons drafted new constitutions with popular sovereignty and civil liberties")
    pdf.bullet("1845: Seven conservative Catholic cantons formed the secret **Sonderbund**")
    pdf.bullet("1847: Diet voted to abolish the alliance; **Sonderbund-Krieg** in November 1847")

    pdf.section_title("6. Federal Constitution of 1848")
    pdf.bullet("Established Switzerland as a **federal state** of 19 cantons and 6 half-cantons")
    pdf.bullet("Combined cantonal experience, French Revolution ideas, and elements from the **US Constitution**")
    pdf.bullet("Centralized: foreign policy, customs, postal sector, currency")
    pdf.bullet("Introduced: **bicameral parliament**, **Federal Council** of 7 members, **universal male suffrage**, **compulsory referendum** for constitutional amendments")
    pdf.bullet("Revolutionary character: enacted despite the Confederate Treaty of 1815 requiring unanimity")

    pdf.section_title("7. Federal Constitution of 1874")
    pdf.bullet("Driven by industrialization and demands for more centralization")
    pdf.bullet("Introduced: **optional legislative referendum** (30,000 citizens or 8 cantons)")
    pdf.bullet("New federal powers: private law, criminal law, unified army, single economic market")
    pdf.bullet("Additional rights: economic freedom, free primary education, freedom of belief")
    pdf.bullet("Established **Federal Supreme Court as a permanent institution**")
    pdf.bullet("Created 'Public Law Appeal' -- challenge constitutionality of cantonal acts")
    pdf.bullet("Limitation: Art. 113 required courts to apply federal statutes even if unconstitutional")

    pdf.section_title("8. Developments 1874-1999")
    pdf.bullet("Additional federal powers: civil/criminal law (1898), social security, transportation, energy, environment")
    pdf.bullet("**Women's suffrage (1971)**; proportional representation (1918)")
    pdf.bullet("**Canton of Jura** created (1978)")
    pdf.bullet("Trend toward interventionist and 'prevention state'")
    pdf.bullet("Constitution became increasingly incoherent -- formal sense did not reflect substantive sense")

    # ---- CHAPTER C: SOURCES ----
    pdf.add_page()
    pdf.chapter_title("CHAPTER C: SOURCES OF CONSTITUTIONAL LAW")

    pdf.remember_box("Remember", [
        "The **Federal Constitution of 18 April 1999** is the most important source.",
        "Other sources: **public international law**, **federal statutes**, and **customary law**.",
        "**Case law** of the Federal Supreme Court plays a very significant role (though not a formal source).",
    ])

    pdf.section_title("1. Federal Constitution of 1999 (Nachfuhrung)")
    pdf.bullet("The old Constitution of 1874 had become confusing and incoherent")
    pdf.bullet("'Verfassungsreform im Baukastensystem' -- modular constitutional reform:")
    pdf.bullet("**Package 1**: Updated coherent text ('Nachfuhrung') -- approved 18 April 1999, in force 1 January 2000", level=1)
    pdf.bullet("**Package 2**: Reform of direct democracy instruments -- approved 2003", level=1)
    pdf.bullet("**Package 3**: Reform of judicial system -- approved 2000", level=1)
    pdf.bullet("Revenue-sharing reform between Federation and cantons: 2004", level=1)

    pdf.subsection_title("Structure of the Federal Constitution")
    widths = [80, 40]
    pdf.table_header(["Section", "Articles"], widths)
    pdf.table_row(["Preamble", "--"], widths, True)
    pdf.table_row(["Title 1: General Provisions", "Art. 1-6"], widths)
    pdf.table_row(["Title 2: Fundamental Rights, Citizenship", "Art. 7-41"], widths, True)
    pdf.table_row(["Title 3: Confederation, Cantons, Communes", "Art. 42-135"], widths)
    pdf.table_row(["Title 4: The People and the Cantons", "Art. 136-142"], widths, True)
    pdf.table_row(["Title 5: Federal Authorities", "Art. 143-191c"], widths)
    pdf.table_row(["Title 6: Revision & Transitional", "Art. 192-197"], widths, True)
    pdf.ln(3)

    pdf.section_title("2. Other Sources")

    pdf.subsection_title("2.1 Public International Law")
    pdf.bullet("Main sources (Art. 38 ICJ Statute): international treaties, customs, general principles of law")
    pdf.bullet("Key treaties of constitutional dimension: **ECHR**, **ICCPR**, ICESCR, Convention against Torture, Convention on the Rights of the Child")
    pdf.bullet("International conventions and treaties become **applicable and binding after states' ratification**")
    pdf.bullet("Switzerland follows a **monistic approach**: international law is part of the domestic legal order without need for incorporation")
    pdf.bullet("Contrast: **Dualist approach** (UK, Germany) requires domestic legislation to incorporate international law")
    pdf.bullet("Only **self-executing provisions** can be directly relied on by individuals in courts (must directly regulate rights/duties and be sufficiently clear)")

    pdf.sub_subsection_title("Customary International Law vs. Ius Cogens")
    pdf.bullet("**Customary international law**: unwritten principles requiring (1) continuous and coherent practice, (2) **opinio iuris** (belief practice is a legal obligation), (3) a lacuna in written law")
    pdf.bullet("**Chain**: vital rules of customary international law + opinio iuris => **ius cogens** => **erga omnes/inter omnes effect**")
    pdf.bullet("**General principles of law** recognized by civilized nations (fairness, justice, good faith, impartiality of judges) also serve as PIL sources")
    pdf.bullet("**Judicial decisions and legal scholarship** serve as subsidiary means for determining rules of law")

    pdf.sub_subsection_title("Examples: Customary International Law")
    pdf.bullet("Prohibition of execution of offenders under the age of 18 at the time of their crime")
    pdf.bullet("Immunity of visiting foreign heads of state")

    pdf.sub_subsection_title("Examples: Ius Cogens (Peremptory Norms)")
    pdf.bullet("Prohibition of torture")
    pdf.bullet("Prohibition of crimes against humanity")
    pdf.bullet("Prohibition of genocide")
    pdf.bullet("Prohibition of human trafficking")
    pdf.bullet("Prohibition of slavery")
    pdf.bullet("**Non-refoulement principle**: prohibition of returning persons to a state where they face persecution or torture")

    pdf.key_concept_box("Exercise Case: Tamil Asylum Seeker (2013)",
        "In 2013, Switzerland deported a Tamil asylum seeker to Sri Lanka where he was arrested and severely mistreated. "
        "An international court found TWO principles of ius cogens violated: (1) the non-refoulement principle (by Switzerland) "
        "and (2) the prohibition of torture (by Sri Lanka).")

    pdf.subsection_title("2.2 Federal Statutes")
    pdf.bullet("Federal statutes covering matters of constitutional importance belong to the substantive constitution")
    pdf.bullet("Cover matters such as **citizenship, political rights, activities of federal authorities**")
    pdf.bullet("Key statutes:")
    pdf.bullet("Federal Act of 20 June 2014 on Swiss Citizenship (**SCA**)", level=1)
    pdf.bullet("Federal Act of 17 December 1976 on Political Rights (**PRA**)", level=1)
    pdf.bullet("Federal Act of 13 December 2002 on the Federal Assembly (**ParlA**)", level=1)
    pdf.bullet("Organization of the Government and the Administration (**GAOA**)", level=1)
    pdf.bullet("Federal Act of 17 June 2005 on the Federal Supreme Court (**FSCA**), SR 173.110", level=1)

    pdf.subsection_title("2.3 Customary Law")
    pdf.bullet("Unwritten principles such as **good faith** are examples of customary law")
    pdf.bullet("Three conditions: (1) continuous, uninterrupted practice; (2) **opinio iuris** (belief practice is legally required); (3) a **lacuna** (gap) in written law")
    pdf.bullet("Since 1999 Constitution encompasses most unwritten principles, customary law plays a **negligible role**")

    pdf.subsection_title("2.4 Case Law")
    pdf.bullet("Case law of the Federal Supreme Court plays a **significant role**, although it is **not a formal source** of constitutional law")
    pdf.bullet("Swiss judicial decisions are **only binding on the court whose decision has been overruled**; not binding upon other courts (even other panels of the Federal Supreme Court)")
    pdf.bullet("This is **different from the Common Law system** where precedent is binding (stare decisis)")
    pdf.bullet("However, Federal Supreme Court precedents play a **very significant role** due to textual indeterminacy of constitutional provisions")

    pdf.sub_subsection_title("Role in Developing Constitutional Law")
    pdf.bullet("The court may first **acknowledge unwritten fundamental rights**; if it does so regularly, these rights may later be **introduced into the Constitution**")
    pdf.bullet("Examples: personal liberty, freedom of opinion, freedom of assembly", level=1)
    pdf.bullet("The court may **derive other rights from constitutional provisions**, e.g., guarantee of equality before the law => fundamental procedural rights")
    pdf.bullet("Example: right to legal assistance for people who lack the necessary means", level=1)
    pdf.bullet("Under the 1874 Constitution, the Court derived fundamental procedural rights from equality (right to be heard, legal assistance, protection against arbitrariness)")
    pdf.bullet("These unwritten rights were later codified in the 1999 Constitution")

    # ---- CHAPTER D: CONSTITUTIONAL INTERPRETATION (intro) ----
    pdf.add_page()
    pdf.chapter_title("CHAPTER D: CONSTITUTIONAL INTERPRETATION (Overview)")

    pdf.remember_box("Remember", [
        "Constitutional interpretation is a **complex procedure** considering wording, systematic context, historical background, and purpose.",
        "Swiss courts follow **pluralism of methods** -- no single method has priority.",
    ])

    pdf.bullet("Legal texts must be **interpreted** to establish meaning; there is often more than one correct interpretation")
    pdf.bullet("Any application of law is a **creative act**; courts contribute to policy-making")
    pdf.bullet("Constitutional norms are frequently abstract -- normative openness defers important determinations to interpreters")
    pdf.bullet("The Federal Supreme Court applies the same methodological rules as for sub-constitutional law (BGE 139 II 243)")

    pdf.subsection_title("Four Methods of Interpretation")
    pdf.bullet("**1. Grammatical**: ordinary meaning of words, technical terms, three official languages carry equal weight (Art. 70 para. 1 Cst)")
    pdf.bullet("**2. Systematic**: norm interpreted in light of its context (external structure and internal value system)")
    pdf.bullet("**3. Historical**: meaning at the time of creation (subjective intent of drafters vs. objective meaning at enactment)")
    pdf.bullet("**4. Teleological**: purpose ('telos') of the norm; values and goals the provision aims to achieve")

    pdf.subsection_title("Additional Interpretation Principles")
    pdf.bullet("**Pluralism of methods** ('Methodenpluralismus'): no hierarchy; the court considers all approaches and combines them")
    pdf.bullet("**Interpretation in conformity with the Constitution** ('verfassungskonforme Auslegung'): among possible interpretations, prefer the one consistent with constitutional values (Art. 49 para. 1 Cst)")
    pdf.bullet("**Interpretation in conformity with international law** ('volkerrechtskonforme Auslegung'): interpret domestic law to conform with international obligations (especially ECHR)")

    pdf.key_concept_box("Exercise: Applying Interpretation Methods",
        "Practice applying all four methods to the following constitutional articles:\n"
        "- Art. 10a Cst (Prohibition of face-veiling)\n"
        "- Art. 18 Cst (Freedom of language)\n"
        "- Art. 36 Cst (Restrictions of fundamental rights)")

    # Key abbreviations
    pdf.add_page()
    pdf.chapter_title("KEY ABBREVIATIONS")
    pdf.bullet("**Cst** = Federal Constitution of the Swiss Confederation (18 April 1999)")
    pdf.bullet("**ECHR** = European Convention on Human Rights")
    pdf.bullet("**ECtHR** = European Court of Human Rights")
    pdf.bullet("**ICCPR** = International Covenant on Civil and Political Rights")
    pdf.bullet("**ICESCR** = International Covenant on Economic, Social and Cultural Rights")
    pdf.bullet("**ParlA** = Parliament Act")
    pdf.bullet("**PRA** = Political Rights Act")
    pdf.bullet("**SCA** = Swiss Citizenship Act")
    pdf.bullet("**FSCA** = Federal Supreme Court Act")
    pdf.bullet("**GAOA** = Government and Administration Organization Act")
    pdf.bullet("**PubA** = Publications Act")
    pdf.bullet("**SR** = Classified Compilation of Federal Legislation")
    pdf.bullet("**BGE** = Official Compilation of Federal Supreme Court Decisions")
    pdf.bullet("**BBl** = Federal Gazette")

    out = os.path.join(os.path.dirname(__file__), "Lecture1_Introduction_History_Sources.pdf")
    pdf.output(out)
    print(f"Generated: {out}")


# ============================================================
# LECTURE 2: Principle of the Rechtsstaat
# ============================================================

def generate_lecture2():
    """Generate Lecture 2 PDF: Principle of the Rechtsstaat."""
    pdf = NotesPDF("Lecture 2: Principle of the Rechtsstaat",
                   "Chapter E, Section 1 (pp. 24-42)")
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ---- STRUCTURAL PRINCIPLES INTRO ----
    pdf.add_page()
    pdf.chapter_title("CHAPTER E: STRUCTURAL PRINCIPLES OF THE CONSTITUTION")

    pdf.remember_box("Remember", [
        "Swiss constitutional law rests on **four fundamental structural principles**: (1) Rechtsstaat, (2) Federalism, (3) Democracy, (4) Social Justice.",
        "These principles **guide all state actions** but are too vague to be directly applicable in courts.",
        "They are **implied** in the Constitution's structure and content, not found explicitly.",
        "They may **evolve** as the Constitution is open to revision.",
    ])

    # ---- 1. PRINCIPLE OF THE RECHTSSTAAT ----
    pdf.chapter_title("1. PRINCIPLE OF THE RECHTSSTAAT")

    pdf.remember_box("Remember", [
        "The main idea: **limit the power of the state by law** to protect individuals from arbitrary exercise of authority.",
        "Modern understanding encompasses: **formal elements** (legality, division of powers, independent judiciary) and **substantive elements** (fundamental rights, social guarantees).",
    ])

    pdf.section_title("1.1 Concept: Overview")

    pdf.subsection_title("a) Historical Development in Continental Europe")
    pdf.bullet("Concept of the **Rechtsstaat** (law-based-state) dates back to **Plato** and **Aristotle**")
    pdf.bullet("In Germany, first used in connection with **liberal theories in the early 19th century**")
    pdf.bullet("Influenced by **Immanuel Kant**: rationalize political rule, institutionalize liberal claims against absolutism")
    pdf.bullet("The state should be shaped, bound, and limited by law in three ways:")
    pdf.bullet("State administration must be **based on law**", level=1)
    pdf.bullet("**Formal law** required for all state action affecting freedom and property", level=1)
    pdf.bullet("All administrative actions subject to **judicial review**", level=1)
    pdf.bullet("The term Rechtsstaat was intended as an **antonym for tyranny and arbitrariness**")

    pdf.subsection_title("b) Modern Understanding")
    pdf.bullet("Formal elements proved **insufficient** to secure human dignity during industrialization")
    pdf.bullet("19th century **Nachtwachterstaat** (minimal state): limited to ensuring order and security")
    pdf.bullet("Expanded to a **'thick' conception** with substantive dimension")
    pdf.bullet("After WWII: emphasis on **universal human rights**; in Germany, the anti-model to the Nazi state")

    pdf.section_title("1.2 Rechtsstaat in a Formal Sense")

    pdf.subsection_title("a) Three Formal Elements")

    pdf.sub_subsection_title("Element 1: Principle of Legality")
    pdf.bullet("All authorities must **comply with the law**")
    pdf.bullet("**Gesetzesvorrang** (precedence of statute): law takes precedence over any other authority")
    pdf.bullet("**Gesetzesvorbehalt** (statutory reservation): state actions must be based on law")
    pdf.bullet("Three qualitative requirements of the law:")
    pdf.bullet("**Requirement of a legal rule** (Erfordernis des Rechtssatzes): rules must be general and abstract, applying to indeterminate persons/cases -- guarantees **equality before the law**", level=1)
    pdf.bullet("**Requirement of sufficient precision**: law must allow individuals to adjust behaviour and foresee consequences", level=1)
    pdf.bullet("**Requirement of adequate legal form** (Normstufe): important questions require a **statute enacted by the legislature** (not just an ordinance) -- guarantees **democratic legitimacy**", level=1)

    pdf.sub_subsection_title("Element 2: Division of Powers")
    pdf.bullet("State divided into **three branches**: legislature, executive, judiciary")
    pdf.bullet("Each has separate powers and responsibilities")
    pdf.bullet("System of **checks and balances** -- each branch limits the others")

    pdf.sub_subsection_title("Element 3: Independent Judiciary")
    pdf.bullet("Judicial review is an **effective control mechanism** over state actions")
    pdf.bullet("Right to a **legally constituted, competent, independent and impartial court**")
    pdf.bullet("**Independent** = judges decide only based on law; **Impartial** = judges are unprejudiced")

    pdf.subsection_title("b) Formal Elements in Swiss Constitutional Law")

    pdf.article_box([
        "**Art. 5 para. 1 Cst**: All state activities must be based on and limited by law (legality)",
        "**Art. 164 para. 1 Cst**: Important legal rules enacted as federal statutes (democratic legitimacy)",
        "**Art. 141 para. 1 lit. a Cst**: Federal statutes subject to optional referendum",
        "**Art. 5 para. 4 Cst**: Federation and cantons shall respect international law",
        "**Art. 148-191c Cst**: Division of powers (Assembly, Council, Courts)",
        "**Art. 191c Cst**: Independence of the judiciary",
        "**Art. 29-32 Cst**: Procedural due process rights",
        "**Art. 190 Cst**: Courts must apply federal statutes even if unconstitutional (limitation!)",
    ])

    pdf.key_concept_box("Critical: Art. 190 Cst",
        "Courts are obliged to apply federal statutes even if they conflict with the Constitution. "
        "This restriction ONLY applies to federal statutes -- not to federal ordinances, cantonal or communal laws.")

    pdf.section_title("1.3 Rechtsstaat in a Substantive Sense")
    pdf.bullet("The formal Rechtsstaat is complemented by **substantive principles**: respect for human freedom, equality, and commitment to a liberal and just order")
    pdf.bullet("Core elements: **civil liberties**, **equality before the law**, **political rights**, **basic social guarantees**")
    pdf.bullet("Recognizes that effective exercise of rights requires **positive state measures** (linking to social justice)")

    pdf.article_box([
        "**Art. 7 Cst**: Human dignity as supreme value",
        "**Art. 36 para. 4 Cst**: Essence of fundamental rights may not be encroached upon",
        "**Art. 2 Cst**: Aims of the Confederation (liberty, welfare, equality)",
        "**Art. 41 Cst**: Social objectives",
        "**Art. 11, 12, 19 Cst**: Basic social rights",
    ])

    pdf.section_title("1.4 Rechtsstaat vs. Rule of Law")

    pdf.body_text("Both share a common core: all state authorities should be **accountable to laws** that are publicly promulgated, equally enforced, and independently adjudicated. But they developed in different historical contexts.")

    pdf.subsection_title("Rule of Law (Anglo-American Tradition)")
    pdf.bullet("Traced to the English **Petition of Rights of 1628**: no taxation without parliament, no arbitrary imprisonment")
    pdf.bullet("**Dicey's three principles**: (1) supremacy of law over arbitrary power; (2) equal subjection of all to ordinary law; (3) rights protected by ordinary law, not abstract declarations")
    pdf.bullet("**Parliament is not bound** by any higher law (parliamentary supremacy)")

    pdf.subsection_title("Key Contrasts")
    widths = [30, 55, 55]
    pdf.table_header(["Aspect", "Rechtsstaat", "Rule of Law"], widths)
    pdf.table_row(["Focus", "Written constitution", "Ordinary law & courts"], widths, True)
    pdf.table_row(["Limits", "All three branches", "Excludes parliament"], widths)
    pdf.table_row(["Rights source", "Constitutional guarantees", "Court-defined rights"], widths, True)
    pdf.ln(3)

    # ---- 1.5 LEGAL ENACTMENTS ----
    pdf.add_page()
    pdf.section_title("1.5 Form of Legal Enactments")

    pdf.subsection_title("a) Overview of Legal Forms")
    pdf.bullet("**Constitutional provisions**: general and abstract; mandatory referendum (double majority); highest precedence")
    pdf.bullet("**Federal statutes**: general and abstract; subject to optional referendum; high democratic legitimacy (Art. 163 Cst)")
    pdf.bullet("**(Parliamentary) ordinances**: general and abstract; NOT subject to referendum; lower legitimacy")
    pdf.bullet("**Federal decrees**: concrete, specific decisions (not general rules); some subject to referendum, some not")

    pdf.subsection_title("b) Federal Constitution -- Total Revision")
    pdf.bullet("Three ways to initiate:")
    pdf.bullet("**Popular initiative**: 100,000 signatures within 18 months (Art. 138 para. 1 Cst)", level=1)
    pdf.bullet("**One parliamentary chamber** proposes: requires preliminary popular vote (Art. 193 para. 2 Cst)", level=1)
    pdf.bullet("**Both chambers** agree: they draft a new constitution", level=1)
    pdf.bullet("If initiated by popular initiative or one chamber, the **Federal Assembly is dissolved** and new elections held (Art. 193 para. 3 Cst)")
    pdf.bullet("Must respect **mandatory provisions of international law (jus cogens)** -- Art. 193 para. 4 Cst")
    pdf.bullet("Must be approved by **mandatory referendum** (people + cantons)")

    pdf.subsection_title("c) Federal Constitution -- Partial Revision")
    pdf.bullet("**Popular initiative**: 100,000 signatures; form of a **general proposal** or **specific draft** (Art. 139 para. 2 Cst)")
    pdf.bullet("Parliament may submit a **counterproposal** (Art. 139 para. 5 Cst)")
    pdf.bullet("**Federal Assembly** may also initiate partial revision (Art. 194 para. 1 Cst)")
    pdf.bullet("Validity requirements: consistency of form, subject matter, mandatory international law, implementability")
    pdf.bullet("Must be approved by **mandatory referendum** (double majority)")

    pdf.subsection_title("d) Federal Statutes (Art. 164 Cst)")
    pdf.bullet("All **important legal norms** must be enacted as federal statutes")
    pdf.bullet("Subject to **optional referendum**: 50,000 signatures or 8 cantons within 100 days (Art. 141 Cst)")
    pdf.bullet("Only requires majority of **voting population** (not cantonal majority)")

    pdf.sub_subsection_title("Legislative Process")
    pdf.bullet("1. Initiated by Federal Council, parliament, or canton")
    pdf.bullet("2. **Public consultation (Vernehmlassung)** with cantons, parties, stakeholders (Art. 147 Cst)")
    pdf.bullet("3. Second draft with dispatch (Botschaft) published in Federal Gazette")
    pdf.bullet("4. Debated by both parliamentary chambers (committee then full chamber)")
    pdf.bullet("5. Published; 100-day referendum period starts")
    pdf.bullet("6. Enters into force after publication in official compilation (Art. 2, 7 PubA)")

    pdf.subsection_title("e) Emergency Federal Statutes (Art. 165 Cst)")
    pdf.bullet("Declared urgent by **absolute majority** of both chambers; duration must be limited")

    widths = [40, 40, 60]
    pdf.table_header(["Duration", "Const. Basis", "Referendum"], widths)
    pdf.table_row(["<= 1 year", "Either", "None"], widths, True)
    pdf.table_row(["> 1 year", "Yes", "Optional (abrogative)"], widths)
    pdf.table_row(["> 1 year", "No", "Mandatory (abrogative)"], widths, True)
    pdf.ln(2)

    pdf.bullet("Not approved in popular vote? **May not be renewed** (Art. 165 para. 4 Cst)")
    pdf.bullet("Example: **COVID-19 Act** (25 Sept 2020) -- emergency statute with constitutional basis, approved by popular vote 13 June 2021")

    pdf.subsection_title("f) Ordinances")
    pdf.bullet("Legal rules NOT enacted as constitutional amendments or statutes; **not subject to referendum**")
    pdf.bullet("Usually adopted by the **executive branch**; also by Federal Assembly or courts")
    pdf.bullet("Four delegation requirements (Art. 164 para. 2 Cst):")
    pdf.bullet("Not excluded by Constitution", level=1)
    pdf.bullet("Based on a statutory provision", level=1)
    pdf.bullet("Subject matter defined exactly in the statute", level=1)
    pdf.bullet("Most important provisions remain in the statute", level=1)
    pdf.bullet("**Emergency ordinances** (Art. 185 para. 3 Cst): Federal Council can issue directly based on Constitution; limited duration; cease after 6 months without a bill (Art. 7d GAOA)")

    pdf.subsection_title("g) Federal Decrees")
    pdf.bullet("Parliamentary decisions on **concrete, specific matters** (not general rules)")
    pdf.bullet("Some subject to optional referendum (if constitutionally/statutorily required)")
    pdf.bullet("**Simple federal decrees**: not subject to referendum (Art. 163 para. 2 Cst)")
    pdf.bullet("Examples: validity of popular initiatives (Art. 173 para. 1 lit. f), expenditure (Art. 167), cantonal constitution guarantees (Art. 172 para. 2)")

    # ---- 1.6 HIERARCHY OF NORMS ----
    pdf.add_page()
    pdf.section_title("1.6 Hierarchy of Norms")

    pdf.subsection_title("Domestic Hierarchy (Lex Superior)")
    pdf.bullet("**Federal Constitution** > **Federal statute** > **Federal ordinance**")
    pdf.bullet("**Federal law** (all levels) > **Cantonal law** > **Communal law** (Art. 49 Cst)")

    pdf.subsection_title("Conflict Resolution Rules (Same Level)")
    pdf.bullet("**Lex posterior derogat legi priori**: newer law overrides older law")
    pdf.bullet("**Lex specialis derogat legi generali**: specific law overrides general law")

    pdf.subsection_title("International Law vs. Domestic Law")
    pdf.bullet("**Jus cogens** (peremptory norms) always take precedence over national law")
    pdf.bullet("Art. 5 para. 4 Cst: obligation to respect international law")
    pdf.bullet("Art. 190 Cst: courts must apply both federal statutes AND international law")
    pdf.bullet("**Schubert case (BGE 99 Ib 39)**: later statute prevails if parliament **intentionally departed** from the treaty")
    pdf.bullet("**But for human rights treaties (BGE 139 I 16)**: international treaty prevails even if not more recent")
    pdf.bullet("Leading case: **Art. 8 ECHR** (family life) takes precedence over **Art. 121 Cst** (expulsion)")

    pdf.key_concept_box("Key Conflict Rules Summary",
        "1. Jus cogens ALWAYS prevails\n"
        "2. For human rights treaties (ECHR): treaty prevails\n"
        "3. For other treaties: Schubert rule (later statute may prevail if intentional)\n"
        "4. Federal law prevails over cantonal law (Art. 49 Cst)")

    out = os.path.join(os.path.dirname(__file__), "Lecture2_Rechtsstaat.pdf")
    pdf.output(out)
    print(f"Generated: {out}")


# ============================================================
# LECTURE 3: Federalism
# ============================================================

def generate_lecture3():
    """Generate Lecture 3 PDF: Federalism."""
    pdf = NotesPDF("Lecture 3: Federalism",
                   "Chapter E, Section 2 (pp. 43-69)")
    pdf.alias_nb_pages()
    pdf.cover_page()

    pdf.add_page()
    pdf.chapter_title("2. FEDERALISM")

    pdf.remember_box("Remember", [
        "**Federalism** describes the delicate balance of **unity and diversity** -- combining federal **shared rule** and **self-rule** of constituent units.",
        "The **principle of subsidiarity**: smaller units act autonomously; only tasks they cannot fulfill are assigned to the next level.",
        "A **federal state** is composed of a federal authority and constituent political units (cantons/states).",
    ])

    pdf.section_title("2.1 Concept: Overview")

    pdf.subsection_title("a) Federalism -- Term and Functions")
    pdf.bullet("From Latin **'foedus'** = covenant")
    pdf.bullet("A composite structure of two or more orders of government")
    pdf.bullet("**Shared rule**: constituent units participate in federal decision-making")
    pdf.bullet("**Self-rule**: constituent units have autonomous fields of competence")

    pdf.sub_subsection_title("Functions")
    pdf.bullet("Accommodates a **plurality of interests and identities** within a diverse society")
    pdf.bullet("Enhances **citizen participation** and **democratic control**")
    pdf.bullet("Leads to **innovation and diversity** ('**laboratory federalism**')")
    pdf.bullet("Reflects Switzerland's linguistic, cultural, and geographical diversity")
    pdf.bullet("Promotes **internal cohesion and cultural diversity** (Art. 2 para. 2 Cst)")

    pdf.subsection_title("b) Subsidiarity")
    pdf.bullet("**Art. 5a Cst**: principle of subsidiarity in allocation of state tasks")
    pdf.bullet("**Art. 43a para. 1 Cst**: Federation only undertakes tasks cantons cannot perform or requiring uniform regulation")
    pdf.bullet("**Default rule**: the smaller unit should be autonomous and responsible for its own rule, **unless**:")
    pdf.bullet("The smaller unit has no capacity/resources to act autonomously", level=1)
    pdf.bullet("The matter requires uniform regulation", level=1)
    pdf.bullet("Hard to derive a directly applicable, binding rule from this principle")

    pdf.subsection_title("c) Federal State vs. Unitary State vs. Confederation")

    widths = [35, 50, 50]
    pdf.table_header(["Type", "Key Feature", "Example"], widths)
    pdf.table_row(["Federal state", "Vertical power distribution", "CH, USA, Germany"], widths, True)
    pdf.table_row(["Unitary state", "Sovereignty at national level", "France, Italy"], widths)
    pdf.table_row(["Confederation", "Treaty between sovereign states", "Old CH pre-1848"], widths, True)
    pdf.ln(3)

    pdf.bullet("**Federal state** = constitution as common basis, amended by majority rule (bottom-up)")
    pdf.bullet("**Unitary state** = one constitution, central government decides powers (top-down)")
    pdf.bullet("**Confederation** = international treaty, amendment requires unanimity")
    pdf.bullet("The name '**Swiss Confederation**' is legally misleading -- Switzerland is a federal state since 1848")

    # ---- THREE LEVELS OF GOVERNMENT ----
    pdf.add_page()
    pdf.section_title("2.2 Three Levels of Government")

    pdf.remember_box("Remember", [
        "Switzerland has **three levels**: Federation, cantons (26), and communes (~2,100).",
        "Cantons are autonomous units with: sufficient tasks, organizational autonomy, and financial autonomy.",
        "Cantons participate in federal decision-making as specified in the Constitution.",
        "Six cantons have only **half a cantonal vote** in referenda and one delegate in the Council of States.",
    ])

    pdf.subsection_title("a) The Federation")
    pdf.bullet("Possesses all characteristics of a state (**Jellinek's Dreielementenlehre**):")
    pdf.bullet("**Permanent population** (Art. 1 Cst)", level=1)
    pdf.bullet("**Defined territory** (sum of 26 cantons; no exclusively federal territory)", level=1)
    pdf.bullet("**State authority** (expressed in federal executive, legislative, judiciary)", level=1)
    pdf.bullet("Designation of tasks defined in **Art. 42 Cst** and **Art. 3 Cst**")
    pdf.bullet("Federation assumes **only tasks explicitly transferred** by the Constitution (Art. 42 Cst)")
    pdf.bullet("Tasks not expressly federal are the **cantons' responsibility** (Art. 3 Cst)")
    pdf.bullet("Key federal powers: **foreign and security policy**, **customs and financial matters**, **national defense**")

    pdf.subsection_title("b) The Cantons")
    pdf.bullet("**26 cantons**, each a self-organizing governmental unit (not merely administrative)")
    pdf.bullet("**Art. 3 Cst**: cantons are sovereign to the extent not limited by the Federal Constitution")
    pdf.bullet("Responsible for: **health care, education, culture**, and can levy taxes")

    pdf.sub_subsection_title("i. Cantonal Autonomy (Art. 47 Cst)")
    pdf.bullet("**Tasks** (Art. 47 para. 2 Cst): Federation shall leave cantons sufficient tasks; cantons decide which, when, and by what means (Art. 43 Cst)")
    pdf.bullet("**Organization**: cantons have their own constitutions (Art. 51 Cst), parliaments (50-180 members), governments (5-7 members), and courts")
    pdf.bullet("**Finances**: cantons collect their own taxes (income, corporate, other within Art. 134 Cst limits)")

    pdf.sub_subsection_title("ii. Participation at Federal Level")
    pdf.bullet("**Referendum**: constitutional amendments require majority of cantons (Art. 140 para. 1 lit. a Cst); 8 cantons can trigger optional referendum (Art. 141 Cst)")
    pdf.bullet("**Initiative**: cantons can submit proposals to Federal Assembly (Art. 160 para. 1 Cst) -- but this is a petition, not a binding initiative")
    pdf.bullet("**Information and consultation**: Federation must inform and consult cantons on matters affecting their interests (Art. 45 para. 2, Art. 55, Art. 147 Cst)")

    pdf.sub_subsection_title("iii. Equality of Cantons")
    pdf.bullet("All cantons have the same competencies, rights and obligations")
    pdf.bullet("Exception: **six cantons** have half a cantonal vote in referenda (Art. 142 para. 4 Cst) and only one delegate in the Council of States (Art. 150 para. 2 Cst)")

    pdf.subsection_title("c) The Communes")
    pdf.bullet("Smallest political units; currently about **2,100** (declining through mergers)")
    pdf.bullet("Autonomy guaranteed by **cantonal law** (Art. 50 para. 1 Cst)")
    pdf.bullet("Four-fifths use **communal assembly** (direct democracy); one-fifth have their own parliament")
    pdf.bullet("Have general residual powers, own financial resources, subject to cantonal monitoring")

    # ---- FEDERAL GUARANTEES ----
    pdf.add_page()
    pdf.section_title("2.3 Federal Guarantees")

    pdf.remember_box("Remember", [
        "Federation guarantees **cantonal constitutions** (Art. 51 Cst)",
        "Federation protects the **constitutional order** of cantons (Art. 52 Cst)",
        "Federation guarantees the **existence and territory** of cantons (Art. 53 Cst)",
    ])

    pdf.subsection_title("a) Cantonal Constitutions (Art. 51 Cst)")
    pdf.bullet("Must be **democratic**: parliament elected by the people; division of powers; mandatory constitutional referendum AND initiative")
    pdf.bullet("Must be **not contrary to federal law** (Art. 51 para. 2 Cst)")
    pdf.bullet("Need **federal approval** by the Federal Assembly (simple federal decree)")

    pdf.subsection_title("b) Protection of Constitutional Order (Art. 52 Cst)")
    pdf.bullet("Federation intervenes when cantonal public order is disrupted and canton cannot maintain it alone")
    pdf.bullet("Hierarchy: first other cantons assist, then the Federation")
    pdf.bullet("Federal interventions are **extremely rare** (examples: World Economic Forum in Davos, COVID-19)")

    pdf.subsection_title("c) Existence and Territory (Art. 53 Cst)")
    pdf.bullet("No secession, exclusion, or creation of a new canton without constitutional amendment")
    pdf.bullet("Changes to existence: requires concerned population + concerned cantons + majority of Swiss people + majority of cantons (Art. 53 para. 2 Cst)")
    pdf.bullet("Changes to territory: requires concerned population + concerned cantons + Federal Assembly decree (Art. 53 para. 3 Cst)")
    pdf.bullet("Boundary adjustments: treaty between cantons with notification to Federation (Art. 53 para. 4 Cst)")

    # ---- DISTRIBUTION OF COMPETENCIES ----
    pdf.add_page()
    pdf.section_title("2.4 Distribution of Competencies")

    pdf.remember_box("Remember", [
        "The Federal Constitution **lists federal competencies explicitly**; cantons retain all **residual powers** (Art. 3, Art. 42 Cst).",
        "**Extent** of competency: comprehensive, fragmentary, framework, or promotion.",
        "**Effect** on cantonal jurisdiction: subsequently derogating, originally derogating, or parallel.",
    ])

    pdf.subsection_title("a) General Method")
    pdf.bullet("Switzerland follows the **predominant model**: enumerate federal competencies, cantons retain residual power (also used by USA, Australia, Germany)")
    pdf.bullet("To transfer power to the Federation requires a **constitutional amendment** approved by double majority (Art. 142 para. 2 Cst)")

    pdf.subsection_title("b) Extent of the Competency")

    pdf.sub_subsection_title("1. Comprehensive Competency")
    pdf.bullet("Federation may regulate **any matter** in a field ('federal matter')")
    pdf.bullet("Language: 'shall legislate', 'shall ensure legislation', 'shall take measures', 'has exclusive right'")
    pdf.bullet("Examples: monetary policy (Art. 99 Cst), economic policy (Art. 100 Cst), road transport (Art. 82 Cst)")

    pdf.sub_subsection_title("2. Fragmentary Competency")
    pdf.bullet("Federation authorized to regulate only a **limited part or aspect** of a particular subject matter")
    pdf.bullet("Examples: health protection (Art. 118 para. 2 Cst), direct taxes (Art. 128 Cst), VAT (Art. 130 Cst), special consumption taxes (Art. 131 Cst)")

    pdf.sub_subsection_title("3. Framework Competency")
    pdf.bullet("Federal competencies restricted to passing a **skeletal law or basic principles**, leaving cantons leeway for detailed regulation tailored to their special needs")
    pdf.bullet("Language: 'shall lay down principles...'")
    pdf.bullet("Examples: spatial planning (Art. 75 Cst), tax harmonization (Art. 129 Cst)")

    pdf.sub_subsection_title("4. Promotion Competency")
    pdf.bullet("Federation '**supports**' and '**encourages**' efforts in areas for which cantons are primarily responsible")
    pdf.bullet("Example: protection of natural and cultural heritage (Art. 78 Cst)")

    pdf.subsection_title("c) Effect on Cantonal Jurisdiction")

    pdf.sub_subsection_title("1. Subsequently Derogating Effect (General Rule)")
    pdf.bullet("Cantons have authority to legislate **as long and as far as** the Federation does not make use of its competency")
    pdf.bullet("Cantonal laws remain applicable in areas not covered by federal rules")
    pdf.bullet("Cantonal competency is **cancelled** once the Federation makes use of its competency")
    pdf.bullet("This is the **general rule** in Swiss constitutional law")
    pdf.bullet("Examples: fishing and hunting (Art. 79 Cst), civil law (Art. 122 Cst)")

    pdf.sub_subsection_title("2. Originally Derogating Effect (Rare)")
    pdf.bullet("From the moment a federal competency is established in the Cst, cantons have **no jurisdiction** in this area -- there is no room for cantonal legislation")
    pdf.bullet("Rare because it risks legal uncertainty when Federation hasn't legislated yet")
    pdf.bullet("Examples: armed forces organization, training and equipment (Art. 60 Cst), postal and telecommunications (Art. 92 Cst)")

    pdf.sub_subsection_title("3. Parallel Effect")
    pdf.bullet("Federation and cantons act **simultaneously and independently** from each other in a particular area")
    pdf.bullet("Examples: universities (Art. 63a Cst -- Federation operates ETH, cantons run cantonal universities), cinema (Art. 71 Cst)")

    pdf.subsection_title("d) Implementation of Federal Law")
    pdf.bullet("Switzerland generally entrusts **cantons** with implementing federal law (Art. 46 para. 1 Cst)")
    pdf.bullet("Few tasks directly administered federally: foreign relations, customs, postal/rail services")
    pdf.bullet("Federation must allow cantons **all possible discretion** (Art. 46 para. 3 Cst)")
    pdf.bullet("Federation must ensure cantons have **financial resources** (Art. 47 para. 2 Cst)")

    # ---- COOPERATION AND TREATIES ----
    pdf.add_page()
    pdf.section_title("2.5 Cooperation and Intercantonal Treaties")

    pdf.subsection_title("a) Cooperation (Art. 44 Cst)")
    pdf.bullet("Federation and cantons must cooperate, provide mutual respect and support")
    pdf.bullet("Disputes resolved by **negotiation or mediation** where possible")

    pdf.subsection_title("b) Intercantonal Treaties (Art. 48 Cst)")
    pdf.bullet("Cantons may conclude treaties (**concordats**) and create common organizations")
    pdf.bullet("The most important instrument of **horizontal cooperative federalism**")
    pdf.bullet("Treaties must NOT be contrary to law, federal interests, or rights of other cantons (Art. 48 para. 3 Cst)")
    pdf.bullet("**Art. 48a Cst**: Federation may declare intercantonal agreements **generally binding** or require cantonal participation (in enumerated fields: criminal penalties, education, higher education, waste, transport, medical science)")

    pdf.section_title("2.6 Competencies of the Federation: Overview")
    pdf.bullet("Most federal competencies in **Art. 54-135 Cst** (Chapters Two and Three, Title Three)")
    pdf.bullet("Key areas: foreign relations (Art. 54), defense (Art. 57-61), education (Art. 62-72), environment (Art. 73-80), transport (Art. 81-88), energy (Art. 89-93), economy (Art. 94-107), social security (Art. 108-120), civil/criminal law (Art. 122-125), finances (Art. 126-135)")

    pdf.section_title("2.7 Primacy of Federal Law (Art. 49 Cst)")
    pdf.bullet("**Art. 49 para. 1 Cst**: federal law takes precedence over any conflicting cantonal law")
    pdf.bullet("'Federal law' includes law at **all levels** (statutes, ordinances, and binding international law)")
    pdf.bullet("Thus: an international treaty or federal ordinance prevails over cantonal constitutional law")
    pdf.bullet("**Art. 190 Cst**: courts must apply federal statutes (even if unconstitutional), but all other acts (cantonal laws, ordinances) may be declared invalid if contrary to federal law")

    pdf.section_title("2.8 Federal Supervision and Coercion")
    pdf.bullet("**Art. 49 para. 2 Cst**: Federation must ensure cantonal compliance with federal law")
    pdf.bullet("Delegated tasks: closely scrutinized; residual cantonal powers: lighter supervision")
    pdf.bullet("Supervisory measures: objections, annulling decisions, directives, inspections, approval requirements")
    pdf.bullet("**Federal coercion** (rarely used): substitution, curbing subsidies, military intervention")

    pdf.section_title("2.9 Limits and Challenges")
    pdf.bullet("**Trend toward centralization**: tasks increasingly transferred to federal level; hardly any areas of complete cantonal autonomy remain")
    pdf.bullet("**International developments**: international cooperation (especially EU) limits sovereign powers at all levels")
    pdf.bullet("**Tension between federalism and democracy**: equal cantonal representation vs. equal individual representation")
    pdf.bullet("Example: 2020 initiative 'For responsible businesses' -- approved by 50.7% of voters but **rejected by majority of cantons** (11.5 smallest cantons can form a blocking majority)")

    # ---- EXERCISE CASE STUDIES ----
    pdf.add_page()
    pdf.section_title("EXERCISE: PRACTICE CASES")

    pdf.key_concept_box("Case 1: Child Allowances (Distribution of Competencies)",
        "Ms. X and Mr. Y live in the Canton of Fribourg with three children. Ms. X works part-time as a teacher in Fribourg; "
        "Mr. Y works part-time as a teacher in Solothurn. When Ms. X applied for child allowances in Fribourg, the cantonal "
        "authorities rejected her application based on a cantonal law stating only the father receives the allowance.\n\n"
        "Questions to consider:\n"
        "1. Give two examples of federal competencies in social matters.\n"
        "2. Is there a federal competency to regulate child allowances? If so, describe and explain the EXTENT "
        "and EFFECT of the federal competency on cantonal jurisdiction, with reference to relevant provisions.")

    pdf.key_concept_box("Case 2: Single-Use Plastic Ban (Federal Competency Analysis)",
        "Members of the Federal Assembly want to declare a total ban on single-use plastic in Switzerland "
        "to reduce plastic production by at least 50%.\n\n"
        "Questions to consider:\n"
        "1. Does the Federation have the competency to enact such a ban?\n"
        "2. What is the extent (scope) of any relevant federal competency?\n"
        "3. What is the effect on cantonal jurisdiction?")

    out = os.path.join(os.path.dirname(__file__), "Lecture3_Federalism.pdf")
    pdf.output(out)
    print(f"Generated: {out}")


if __name__ == "__main__":
    generate_lecture1()
    generate_lecture2()
    generate_lecture3()
    print("\nAll law lecture notes generated successfully!")
