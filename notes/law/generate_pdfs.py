#!/usr/bin/env python3
"""Generate PDF notes for Constitutional Law Lectures 1, 2, 3, and 4."""

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


# ============================================================
# LECTURE 4: Democracy, Political Rights, Popular Initiative
#            & Referendum, Swiss Citizenship, Social Justice
# ============================================================

def generate_lecture4():
    """Generate Lecture 4 PDF: Democracy, Political Rights, Initiative & Referendum."""
    pdf = NotesPDF("Lecture 4: Democracy & Political Rights",
                   "Chapter E, Sections 3-4 (pp. 70-116)")
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ---- 3. DEMOCRACY ----
    pdf.add_page()
    pdf.chapter_title("3. DEMOCRACY")

    pdf.remember_box("Remember", [
        "**Democracy** implies that all state power is based on the will of the people.",
        "Main characteristics: **popular self-determination** and **public control over political power**.",
        "Three basic forms: **direct democracy**, **semi-direct democracy**, and **representative democracy**.",
    ])

    pdf.section_title("3.1 Concept: Overview")
    pdf.bullet("From Greek: **demos** (people) + **kratos** (power, rule)")
    pdf.bullet("Lincoln's Gettysburg Address (1863): 'government of the people, by the people, for the people'")
    pdf.bullet("All citizens participate equally -- directly or through elected representatives -- in the political and legal system")
    pdf.bullet("Most important political leaders are elected in **free and fair elections** and are accountable under the rule of law")

    pdf.subsection_title("Key Characteristics")
    pdf.bullet("**Popular self-determination and equality**: all citizens participate with equal rights")
    pdf.bullet("**Governmental responsibility**: democratic systems must provide for public control of political power")
    pdf.bullet("**Contrast: Autocracy** -- power held by one person or group, not subject to legal restraints or popular control")

    # ---- 3.2 BASIC FORMS OF DEMOCRACY ----
    pdf.section_title("3.2 Basic Forms of Democracy")

    pdf.subsection_title("a) Representative Democracy")
    pdf.bullet("Sovereign power remains with citizens; political power exercised **indirectly through elected representatives**")
    pdf.bullet("People's participation limited to **election of government officials**; people do not decide policy questions directly")
    pdf.bullet("Two main forms: **parliamentary** and **presidential** democracy")

    widths = [30, 55, 55]
    pdf.table_header(["Aspect", "Parliamentary Democracy", "Presidential Democracy"], widths)
    pdf.table_row(["Powers", "Close interconnection", "Strict separation"], widths, True)
    pdf.table_row(["Government", "Parliament forms/supports", "People elect president"], widths)
    pdf.table_row(["Dismissal", "Vote of no confidence", "Fixed term, no dismissal"], widths, True)
    pdf.table_row(["Head of state", "Separate from PM", "President = head of state"], widths)
    pdf.table_row(["Party line", "Strong discipline", "Members vote conscience"], widths, True)
    pdf.table_row(["Examples", "UK, Germany", "USA"], widths)
    pdf.ln(3)

    pdf.subsection_title("b) Direct Democracy")
    pdf.bullet("People decide policy questions **directly**; all eligible citizens actively participate")
    pdf.bullet("In ideal form, there is **no parliament**")
    pdf.bullet("Practiced in ancient Greek city-state of **Athens**; hardly implementable in modern complex states")

    pdf.subsection_title("c) Semi-Direct Democracy")
    pdf.bullet("A **representative democracy combined with instruments of direct democracy**")
    pdf.bullet("Parliament and government are main decision-makers, but people can **directly influence policy** through:")
    pdf.bullet("**Referendum** (mandatory or optional) -- on constitution, statutes, treaties, administrative acts", level=1)
    pdf.bullet("**Popular initiative** (specific draft or general proposal) -- for constitutional revision or legislation", level=1)
    pdf.bullet("**Right to recall** -- dismiss parliament, government, or judges", level=1)
    pdf.bullet("**Extended right to vote** -- elect head of state, government, officials, judges", level=1)

    # ---- 3.3 DEMOCRACY IN THE SWISS SYSTEM ----
    pdf.add_page()
    pdf.section_title("3.3 Democracy in the Swiss System")

    pdf.remember_box("Remember", [
        "Switzerland is a **semi-direct democracy**: elected parliament + powerful instruments of direct participation.",
        "The Swiss model is also called a **consensus-oriented democracy** -- legislation must find fair compromise.",
        "Switzerland is **neither purely parliamentary nor presidential** -- it combines elements of both.",
    ])

    pdf.subsection_title("a) Characteristics")
    pdf.bullet("The people elect representatives in the **Federal Assembly** (primary decision-making institution with Federal Council)")
    pdf.bullet("Citizens can **directly influence** decisions on Constitution and legislation through **referendum and initiative**")
    pdf.bullet("Decisions subject to direct participation are systematically selected according to **importance**")

    pdf.sub_subsection_title("Parliamentary Features")
    pdf.bullet("Constitution establishes parliament as **highest authority** (limited by rights of people and cantons)")
    pdf.bullet("**Parliament elects** the Federal Council (not the people)")
    pdf.bullet("No directly elected head of state; Federal President is **primus inter pares**")
    pdf.bullet("Federal Council **cannot veto** decisions of parliament")

    pdf.sub_subsection_title("Presidential Features")
    pdf.bullet("Federal Council is **personally and functionally independent** of parliament")
    pdf.bullet("Federal Council is a **multi-party coalition** government (not based on coalition agreement)")
    pdf.bullet("Members serve for a **specific term** and **cannot be dismissed** by parliament; Federal Council cannot dissolve parliament")
    pdf.bullet("Federal Council members decide as a **collegium** and defend decisions even if individual members disagree")
    pdf.bullet("**No strong party discipline**; representatives can vote against their own Federal Council member's proposals")

    pdf.subsection_title("b) Key Constitutional Provisions")

    pdf.article_box([
        "**Art. 1 Cst**: The people and the cantons form the Swiss Confederation",
        "**Art. 2 para. 1 Cst**: Protection of liberty and rights of the people",
        "**Art. 33 Cst**: Right of petition (every person, without prejudice)",
        "**Art. 34 Cst**: Guarantee of political rights; freedom to form opinions and express will",
        "**Art. 51 Cst**: Cantons must adopt democratic constitutions",
        "**Art. 136 Cst**: All Swiss citizens over 18 have political rights (unless lacking capacity)",
        "**Art. 138-142 Cst**: Initiatives and referenda",
        "**Art. 148 para. 1 Cst**: Federal Assembly is supreme authority (subject to rights of people and cantons)",
        "**Art. 190 Cst**: Courts must apply federal statutes (even if unconstitutional) -- supremacy of democratic principle over Rechtsstaat",
    ])

    pdf.key_concept_box("Art. 190 Cst and Democracy",
        "The democratic legitimacy of parliament (elected by the people) is considered higher than that of judicial authorities "
        "(elected by parliament, not directly by the people). Therefore, constitutional review of federal statutes is NOT provided "
        "for in the Swiss system. Art. 190 illustrates the supremacy of the democratic principle over the Rechtsstaat principle.")

    # ---- POLITICAL RIGHTS ----
    pdf.add_page()
    pdf.subsection_title("c) Political Rights (Art. 34, Art. 39-40 Cst)")
    pdf.bullet("Political rights enable **direct participation** in elections and policy decisions at federal, cantonal, and communal level")
    pdf.bullet("**Art. 34 para. 2 Cst**: the result of an election or vote must **accurately express the free will** of voters")
    pdf.bullet("Public authorities may **not propagate inaccurate or biased information** that unduly influences voters")
    pdf.bullet("Popular initiatives and governmental proposals must respect **unity of subject matter** -- voters must express their opinion on each subject separately")

    pdf.sub_subsection_title("Distribution of Competencies (Art. 39-40 Cst)")
    pdf.bullet("**Art. 39 para. 1 Cst**: Federation regulates political rights in federal matters; cantons regulate cantonal and communal matters")
    pdf.bullet("**Federal Act on Political Rights (PRA)** of 17 December 1976 contains detailed provisions")
    pdf.bullet("Political rights exercised at **place of domicile** (Art. 39 para. 2 Cst)")
    pdf.bullet("No person may exercise political rights in **more than one canton** (Art. 39 para. 3 Cst)")
    pdf.bullet("Waiting period of max. **3 months** for newly registered residents (Art. 39 para. 4 Cst)")

    pdf.subsection_title("d) Right to Vote")
    pdf.bullet("All Swiss citizens over **18** entitled to participate in National Council elections and popular votes (Art. 136 para. 1 Cst)")
    pdf.bullet("Exception: persons lacking capacity due to **mental illness or incapacity**")
    pdf.bullet("**Active right (aktives Wahlrecht)**: right to elect (vote in elections)")
    pdf.bullet("**Passive right (passives Wahlrecht)**: right to be elected (stand as candidate) -- Art. 143 Cst")

    pdf.sub_subsection_title("Elections to Parliament")
    pdf.bullet("**National Council** (200 members): elected directly by the people, **proportional representation**, every 4 years (Art. 149 Cst)")
    pdf.bullet("Seats allocated to cantons by population; each canton has at least **one seat**")
    pdf.bullet("**Council of States**: elections determined by **cantonal law** (Art. 150 para. 3 Cst)")

    # ---- INITIATIVE ON FEDERAL LEVEL ----
    pdf.add_page()
    pdf.section_title("3.4 Initiative on Federal Level")

    pdf.remember_box("Remember", [
        "Any **100,000 citizens** entitled to vote may request a **total** or **partial revision** of the Constitution.",
        "A partial revision may take the form of a **general proposal** or a **specific draft**.",
        "The initiative must respect: **consistency of form**, **consistency of subject matter**, **jus cogens**, and **implementability**.",
    ])

    pdf.subsection_title("a) Overview")

    widths = [45, 30, 30, 50]
    pdf.table_header(["Instrument", "Form", "Signatures", "Approval"], widths)
    pdf.table_row(["Total revision (Art. 138)", "General proposal", "100,000", "Preliminary vote + double majority"], widths, True)
    pdf.table_row(["Partial revision (Art. 139)", "General or draft", "100,000", "Double majority (people + cantons)"], widths)
    pdf.ln(3)

    pdf.subsection_title("b) Total Revision (Art. 138 Cst)")
    pdf.bullet("May only take the form of a **general proposal**")
    pdf.bullet("First: preliminary vote of the people on whether Constitution should be totally revised (Art. 138 para. 2 Cst)")
    pdf.bullet("If approved: **Federal Assembly dissolved**, new elections held (Art. 193 para. 3 Cst)")
    pdf.bullet("New parliament drafts the constitution; approved by **double majority** (people + cantons)")
    pdf.bullet("Historically insignificant: only one attempt, dropped after negative vote in **1935**")

    pdf.subsection_title("c) Partial Revision (Art. 139 Cst) -- Detailed Procedure")
    pdf.bullet("The most **frequently utilized** democratic instrument at the federal level")
    pdf.bullet("Topics range from footpaths in the Alps to abolition of the armed forces")

    pdf.sub_subsection_title("9-Step Procedure")
    pdf.bullet("**(1) Signature list**: sent to Federal Chancellery for preliminary examination (Art. 68-69 PRA); must include canton/commune of signatories, title/text, withdrawal clause, criminal warning, names of at least 7 authors")
    pdf.bullet("**(2) Collection of signatures**: 100,000 within 18 months of official publication (Art. 139 para. 1 Cst); ~1 in 3 cases fail to collect enough")
    pdf.bullet("**(3) Verification**: cantonal authorities verify signatories' voting rights; lists submitted to Federal Chancellery before 18-month deadline (Art. 71 PRA)")
    pdf.bullet("**(4) Federal Chancellery decision**: determines if required number of valid signatures reached (Art. 72 PRA)")
    pdf.bullet("**(5) Federal Council dispatch**: presents parliament a 'Botschaft' and draft decree on validity (Art. 97 ParlA)")
    pdf.bullet("**(6) Validity check by parliament** (see validity requirements below)")
    pdf.bullet("**(7) Parliament decides on support**: recommends adoption or rejection; may submit a **counterproposal** (Art. 139 para. 5 Cst, Art. 100-101 ParlA)")
    pdf.bullet("**(8) Popular vote**: nationwide vote requiring **double majority** (Art. 75a PRA)")
    pdf.bullet("**(9) Entry into force**: published in official compilation (Art. 195 Cst, Art. 7 PubA)")

    pdf.subsection_title("d) Validity Requirements (Art. 139 para. 3 Cst)")

    pdf.bullet("**i. Consistency of form**: must be exclusively a general proposal OR a specific draft -- no mixture (Art. 75 para. 3 PRA)")
    pdf.bullet("**ii. Consistency of subject matter**: individual parts must have an **intrinsic connection** (Art. 75 para. 2 PRA); voters must be able to express opinion on each subject separately")
    pdf.bullet("**iii. Compliance with jus cogens**: must respect mandatory provisions of international law (Art. 194 para. 2 Cst); if it violates jus cogens, parliament must declare it **invalid**")
    pdf.bullet("**iv. Implementability**: must be possible to execute")

    # ---- LECTURE EXAMPLE: VALIDITY EXERCISES ----
    pdf.add_page()
    pdf.key_concept_box("Lecture Exercise: 'For less military expenses and more peace policy'",
        "The initiative proposes cutting the national defence budget by 10% annually, with 1/3 of savings "
        "going to international peace policy and social security.\n\n"
        "Analysis: Check consistency of form (specific draft -- OK), consistency of subject matter "
        "(military spending + peace policy + social security -- is there an intrinsic connection?), "
        "jus cogens (no violation), and implementability (feasible).")

    pdf.key_concept_box("Lecture Exercise: 'For a new organisation of military service'",
        "The initiative proposes: (1) clarify duty for Swiss men to do military service, (2) alternative civilian "
        "service for conscientious objectors, (3) establish a federal civilian service organization -- all in Art. 18 Cst. "
        "PLUS: 'Every Swiss woman is required to do military service' as a new Art. 18.\n\n"
        "Analysis: Consistency of form? (specific draft -- OK). Consistency of subject matter? "
        "(Military service organization for men + mandatory service for women -- is there an intrinsic connection?). "
        "Jus cogens? (No violation). Implementability? (Feasible).")

    pdf.subsection_title("e) Functions of the Popular Initiative")
    pdf.bullet("An **innovative** part of the Swiss political system")
    pdf.bullet("Provides a **political platform** for groups whose interests are not sufficiently represented")
    pdf.bullet("Gives people **control over the political agenda**")
    pdf.bullet("Even **unsuccessful** initiatives encourage the population and authorities to address certain questions")
    pdf.bullet("Since 1891: ~523 initiatives launched, 353 successfully submitted, only **4 declared invalid**, 228 voted on, **25 accepted**")

    pdf.subsection_title("f) Initiative and International Law")
    pdf.bullet("Initiatives conflicting with **jus cogens**: declared **null and void** by Federal Assembly")
    pdf.bullet("Initiatives conflicting with **other international law**: declared valid and submitted to vote")
    pdf.bullet("Problem: several accepted initiatives are arguably **inconsistent with international law**:")
    pdf.bullet("Art. 123a Cst (2004): life custody for dangerous sex offenders", level=1)
    pdf.bullet("Art. 72 para. 3 Cst (2009): prohibition of minaret construction", level=1)
    pdf.bullet("Art. 121 para. 3-6 Cst (2010): expulsion of criminal foreigners", level=1)
    pdf.bullet("Art. 121a Cst (2014): control of immigration -- potential conflict with EU bilateral agreements", level=1)
    pdf.bullet("Federal Assembly tries to implement such provisions **in conformity with international obligations** (e.g., hardship clauses, prioritizing Swiss residents instead of quotas)")

    # ---- LECTURE EXAMPLE: CASH IS FREEDOM ----
    pdf.key_concept_box("Lecture Example: 'Cash is freedom' Initiative (March 2026)",
        "On 8 March 2026, voters and cantons decided whether to guarantee the availability of cash in the Constitution "
        "(new Art. 99 Cst). The initiative demanded that banknotes and coins be forever available in sufficient quantities "
        "and that any attempt to replace the Swiss franc must be adopted by voters and cantons.\n\n"
        "The Federal Council and Parliament prepared a counterproposal with different wording: "
        "the Swiss franc is the national currency and the SNB must guarantee the supply of cash.")

    pdf.key_concept_box("Lecture Example: 'Internet Initiative'",
        "The Guido Fluri Foundation launched an initiative for a new Art. 93a Cst demanding that platforms, "
        "search engines and AI providers analyse the risks of their services and take measures to limit them. "
        "The initiators criticise that the business model of corporations aims to maximise attention without accountability.")

    # ---- REFERENDUM ON FEDERAL LEVEL ----
    pdf.add_page()
    pdf.section_title("3.5 Referendum on Federal Level")

    pdf.remember_box("Remember", [
        "Through the referendum, the people **approve or reject** constitutional amendments, statutes, treaties, or parliamentary decisions.",
        "Two types: **mandatory** (automatically triggered) and **optional** (requested by 50,000 citizens or 8 cantons).",
        "Two effects: **suspensive** (prevents entry into force) and **abrogative** (repeals acts already in force).",
    ])

    pdf.subsection_title("a) Mandatory Referendum (Art. 140 Cst)")

    pdf.sub_subsection_title("Category 1: Double Majority Required (people + cantons)")
    pdf.bullet("All **constitutional amendments** (Art. 140 para. 1 lit. a Cst)")
    pdf.bullet("Accession to **organizations for collective security** (e.g., NATO) or **supranational communities** (e.g., EU) (Art. 140 para. 1 lit. b Cst)")
    pdf.bullet("**Emergency federal statutes** not based on Constitution, validity > 1 year (Art. 140 para. 1 lit. c Cst) -- vote within 1 year; this is an **abrogative** mandatory referendum")

    pdf.sub_subsection_title("Category 2: Simple Majority of People")
    pdf.bullet("Popular initiatives for a **total revision** of the Constitution")
    pdf.bullet("Popular initiatives for a **partial revision** (general proposal) rejected by Federal Assembly")
    pdf.bullet("Whether a **total revision** should be carried out when the two Councils disagree")

    pdf.subsection_title("b) Optional Referendum (Art. 141 Cst)")
    pdf.bullet("Within **100 days** of official publication, **50,000 citizens** or **8 cantons** may request a popular vote")
    pdf.bullet("Only requires majority of **voting population** (not cantonal majority)")

    pdf.sub_subsection_title("Suspensive Optional Referendum (Art. 141 para. 1 lit. a, c-d Cst)")
    pdf.bullet("**Federal statutes**")
    pdf.bullet("**Specific federal decrees** (if referendum provided for in Constitution or statute)")
    pdf.bullet("**Specific international treaties** (unlimited duration, may not be terminated, accession to international organization, or containing important legislative provisions)")

    pdf.sub_subsection_title("Abrogative Optional Referendum (Art. 141 para. 1 lit. b Cst)")
    pdf.bullet("**Emergency federal statutes** whose term of validity exceeds one year")

    pdf.subsection_title("c) Functions of the Referendum")
    pdf.bullet("Over **482 issues** subject to mandatory referendum; about 1/4 rejected (proposals often succeed only on 2nd or 3rd attempt)")
    pdf.bullet("Since 1874, optional referendum successfully requested in about **211 cases** (~7% of parliamentary decisions)")
    pdf.bullet("In about **half** of optional referendum cases, the majority rejected the parliamentary decision")
    pdf.bullet("Referendum = a **right of popular opposition** and **veto power**")
    pdf.bullet("Consequence: political authorities try to minimize referendum risk via **inclusive decision-making**")
    pdf.bullet("Downside: constant threat of referendum may **weaken responsiveness** to challenges")

    # ---- LECTURE EXAMPLES: REFERENDUM ----
    pdf.key_concept_box("Lecture Example: War Materials Statute Referendum",
        "Germany asked Switzerland to allow re-export of Gepard tank ammunition to Ukraine. Switzerland's War Materials "
        "Statute bans exports/re-exports to countries in conflict. Parliament revised the statute to allow arms exports to 25 "
        "countries even during conflict. The Green Party opposed this amendment.\n\n"
        "Analysis: This is a revision of a federal statute. The Green Party could launch an optional referendum "
        "(Art. 141 para. 1 lit. a Cst) by collecting 50,000 signatures within 100 days.")

    pdf.key_concept_box("Lecture Example: Airport Zurich AG",
        "Although Zurich Airport AG is a listed company, decisions on runway changes require: "
        "(1) approval by cantonal representatives on the board, (2) Government Council directive approved by "
        "Cantonal Council (Parliament), and (3) the Cantonal Council decision is subject to optional referendum "
        "(e.g., 3,000 citizens in Zurich can request a popular vote). This illustrates how democratic participation "
        "affects even corporate infrastructure decisions.")

    # ---- REFERENDUM PRACTICE EXERCISE ----
    pdf.add_page()
    pdf.key_concept_box("Lecture Exercise: Referendum Type Identification",
        "Which type of democratic participation applies at the federal level?\n\n"
        "1. Art. 8 Cst (equality) is repealed\n"
        "   -> Constitutional amendment -> mandatory referendum (double majority)\n\n"
        "2. Switzerland accedes to the EU\n"
        "   -> Supranational community -> mandatory referendum (double majority)\n\n"
        "3. Amendment of Art. 2a of the Ordinance on Political Rights\n"
        "   -> Ordinance -> NO referendum (ordinances not subject to referendum)\n\n"
        "4. A commune in Thurgau wants to become part of St. Gallen\n"
        "   -> Change in cantonal territory -> Art. 53 para. 3 Cst (federal decree, optional referendum)\n\n"
        "5. A new federal statute on forced marriages\n"
        "   -> Federal statute -> optional referendum (50,000 signatures or 8 cantons)\n\n"
        "6. Appenzell IR and AR want to merge\n"
        "   -> Change in existence of cantons -> Art. 53 para. 2 Cst (constitutional amendment, mandatory referendum)")

    # ---- POLITICAL RIGHTS ON CANTONAL LEVEL ----
    pdf.section_title("3.6 Political Rights on the Cantonal Level")
    pdf.bullet("Key federal instruments exist in **all cantons**: mandatory constitutional referendum, optional legislative referendum, popular initiative for constitutional amendments")
    pdf.bullet("**Art. 51 para. 1 Cst** requires cantons to provide mandatory constitutional referendum AND initiative")
    pdf.bullet("Cantonal semi-direct democracy allows **more diverse participation** than the federal level:")
    pdf.bullet("Popular initiative extends to **ordinary legislation** (not just constitutional amendments)", level=1)
    pdf.bullet("In some cantons, the legislative referendum is **mandatory**", level=1)
    pdf.bullet("Important **individual acts and administrative decisions** can be challenged (e.g., financial referenda for large investments)", level=1)
    pdf.bullet("In **all cantons**, the executive is directly elected by the people; in some, also judges and prosecutors", level=1)

    # ---- 3.7 SWISS CITIZENSHIP ----
    pdf.add_page()
    pdf.section_title("3.7 Swiss Citizenship")

    pdf.remember_box("Remember", [
        "Switzerland has a **three-level citizenship**: federal, cantonal, and communal (Art. 37 para. 1 Cst).",
        "Citizenship is based on **ius sanguinis** (descent), not ius soli (place of birth).",
        "Naturalization follows a **cantonal-federal-cantonal** process.",
    ])

    pdf.subsection_title("a) General Concept")
    pdf.bullet("Every Swiss has at least **three citizenships**: Swiss, cantonal, and communal (Art. 37 para. 1 Cst)")
    pdf.bullet("Federal and cantonal citizenship **cannot be obtained** without communal citizenship")
    pdf.bullet("Special rights from Swiss citizenship: **political rights** (Art. 34), **domicile anywhere** (Art. 24), **no expulsion** (Art. 25 para. 1), diplomatic protection, military duty (Art. 59 para. 1)")

    pdf.subsection_title("b) Acquisition by Law (Ius Sanguinis)")
    pdf.bullet("Based on **parents' origins**, not place of birth (Art. 38 para. 1 Cst)")
    pdf.bullet("Swiss at birth if (Art. 1 SCA):")
    pdf.bullet("Child of married parents where **at least one parent** is Swiss", level=1)
    pdf.bullet("Child of a Swiss mother **not married** to the father", level=1)
    pdf.bullet("Minor foreign child of Swiss father upon **recognition of paternity**", level=1)

    pdf.subsection_title("c) Ordinary Naturalization")
    pdf.bullet("**Cantonal-federal-cantonal** process:")
    pdf.bullet("(1) Canton/commune agree in principle; forward application to **SEM** (State Secretariat for Migration) (Art. 13 para. 2 SCA)", level=1)
    pdf.bullet("(2) SEM grants federal naturalization license if all requirements met (Art. 13 para. 3 SCA)", level=1)
    pdf.bullet("(3) Canton makes final naturalization decision within 1 year (Art. 14 para. 1 SCA)", level=1)
    pdf.bullet("Requirements: **integrated** into Swiss society, familiar with Swiss way of life, no security risk (Art. 11 SCA)")
    pdf.bullet("Residence: **10 years** total in Switzerland (3 of last 5 years); years aged 8-18 count double (min. 6 actual years)")
    pdf.bullet("Denial of naturalization must be based on **sound reasoning** (Art. 16 SCA) -- secret ballots not allowed (BGE 129 I 217)")

    pdf.subsection_title("d) Simplified Naturalization (Art. 20-25 SCA)")
    pdf.bullet("Spouse of a Swiss citizen")
    pdf.bullet("Persons who believed in good faith they were Swiss")
    pdf.bullet("Stateless children")
    pdf.bullet("Foreign child not included in parents' naturalization")
    pdf.bullet("**Third-generation immigrants** (before age 25, meeting certain conditions)")

    pdf.subsection_title("e) Loss of Swiss Citizenship")
    pdf.bullet("**By law** (automatic): annulment of parentage link (Art. 5 SCA); adoption by foreigners (Art. 6 SCA); at age 25 if born abroad, always lived abroad, holds other citizenship, and never registered (Art. 7 SCA)")
    pdf.bullet("**By decree**: dual citizen living abroad who wishes to renounce (Art. 37 SCA)")
    pdf.bullet("**Revocation**: dual citizens who seriously violate Swiss interests, e.g., espionage (Art. 42 SCA)")
    pdf.bullet("**Nullification**: naturalization obtained by false information or concealment (Art. 36 SCA)")

    # ---- 4. SOCIAL JUSTICE ----
    pdf.add_page()
    pdf.chapter_title("4. SOCIAL JUSTICE")

    pdf.remember_box("Remember", [
        "**Social justice** aims at establishing just and equal conditions within society, particularly between social classes.",
        "The Constitution contains **social objectives** (guidelines for legislators, NOT directly enforceable in courts).",
        "A few **social rights** are directly enforceable: right to assistance (Art. 12), children's protection (Art. 11), free basic education (Art. 19).",
    ])

    pdf.section_title("4.1 Concept")
    pdf.bullet("Relatively new compared to other structural principles; emerged from the **industrial revolution** and socialist doctrine")
    pdf.bullet("Aimed at improving living conditions of working classes")
    pdf.bullet("Fundamental rights and democratic processes are of **limited value** for those who lack the means to benefit from them")
    pdf.bullet("The Swiss Constitution does not explicitly label Switzerland a **'Sozialstaat'** (welfare state)")

    pdf.section_title("4.2 Social Objectives (Art. 41 Cst)")
    pdf.bullet("**Guidelines for the legislature** -- NOT directly enforceable in courts, do NOT confer individual rights (Art. 41 para. 4 Cst)")
    pdf.bullet("Federation and cantons must endeavor to ensure:")
    pdf.bullet("Access to **social security** and required **health care**", level=1)
    pdf.bullet("**Families** are protected and encouraged", level=1)
    pdf.bullet("Everyone fit to work can earn a living under **fair conditions**", level=1)
    pdf.bullet("Suitable **accommodation** on reasonable terms", level=1)
    pdf.bullet("**Education and training** according to abilities", level=1)
    pdf.bullet("Protection against economic consequences of **old age, invalidity, illness, accident, unemployment, maternity** (Art. 41 para. 2 Cst)")

    pdf.section_title("4.3 Competencies in Social Matters")
    pdf.bullet("Constitution of 1848 had **no federal social competencies**; 1874 added fragmentary employee protection")
    pdf.bullet("Today: extensive federal competencies, some with **substantive guidelines** (e.g., Art. 114 Cst on unemployment insurance)")

    pdf.subsection_title("Three-Pillar System (Art. 111 Cst)")
    pdf.bullet("**1st Pillar**: Federal old-age, survivors' and invalidity insurance (AHV/IV) -- covers basic living expenses (Art. 112 Cst)")
    pdf.bullet("**2nd Pillar**: Compulsory occupational pension scheme (BVG) -- supplements AHV/IV (Art. 113 Cst)")
    pdf.bullet("**3rd Pillar**: Voluntary private pension schemes -- optional additional security (Art. 111 para. 4 Cst)")
    pdf.bullet("Additional: unemployment insurance (Art. 114), child allowances/maternity (Art. 116), health/accident insurance (Art. 117)")
    pdf.bullet("**Subsidiary support** by canton of residence when social security is insufficient (Art. 115 Cst)")

    pdf.section_title("4.4 Social Rights (Enforceable)")
    pdf.bullet("**Art. 12 Cst**: Right to assistance and care, financial means for a decent standard of living (for persons in need)")
    pdf.bullet("**Art. 11 Cst**: Children and young people have the right to special protection and encouragement of development")
    pdf.bullet("**Art. 19 Cst**: Right to adequate and **free basic school education**")
    pdf.bullet("**Art. 29 para. 3 Cst**: Right to free legal advice and representation for those without sufficient means")
    pdf.bullet("**Art. 28 para. 3 Cst**: Right to strike (debated whether this is a social right)")

    # ---- KEY ABBREVIATIONS ----
    pdf.add_page()
    pdf.chapter_title("KEY TERMS AND ABBREVIATIONS")

    pdf.subsection_title("Key Terms")
    pdf.bullet("**Aktives Wahlrecht** = active right to vote (right to elect)")
    pdf.bullet("**Passives Wahlrecht** = passive right to vote (right to be elected)")
    pdf.bullet("**Stimmrecht** = right to participate in popular votes")
    pdf.bullet("**Primus inter pares** = first among equals (Federal President)")
    pdf.bullet("**Ius sanguinis** = citizenship by descent (blood)")
    pdf.bullet("**Ius soli** = citizenship by place of birth")
    pdf.bullet("**Suspensive referendum** = prevents entry into force")
    pdf.bullet("**Abrogative referendum** = repeals acts already in force")
    pdf.bullet("**Sozialstaat** = welfare state")

    pdf.subsection_title("Key Abbreviations")
    pdf.bullet("**Cst** = Federal Constitution of the Swiss Confederation")
    pdf.bullet("**PRA** = Federal Act on Political Rights (SR 161.1)")
    pdf.bullet("**ParlA** = Parliament Act")
    pdf.bullet("**SCA** = Swiss Citizenship Act (SR 141.0)")
    pdf.bullet("**SEM** = State Secretariat for Migration")
    pdf.bullet("**AHV** = Alters- und Hinterlassenenversicherung (old-age/survivors' insurance)")
    pdf.bullet("**IV** = Invalidenversicherung (invalidity insurance)")
    pdf.bullet("**BVG** = Berufliche Vorsorge (occupational pension)")

    out = os.path.join(os.path.dirname(__file__), "Lecture4_Democracy_Political_Rights.pdf")
    pdf.output(out)
    print(f"Generated: {out}")


def generate_lecture5():
    """Generate Lecture 5 PDF: Fundamental Rights (Egli pp. 117-128 + Lecture 5 Slides)."""
    pdf = NotesPDF("Lecture 5: Fundamental Rights",
                   "Chapter G (pp. 117-128) + Lecture 5 Slides")
    pdf.alias_nb_pages()
    pdf.cover_page()

    # ---- REMEMBER BOX ----
    pdf.add_page()
    pdf.remember_box("Remember (Chapter G)", [
        "Fundamental rights are constitutionally and internationally guaranteed legal entitlements of individuals in their relationship with the state, protecting essential freedoms.",
        "Categories: civil liberties, equality before the law, social rights, procedural rights, political rights.",
        "Main sources: the Constitution and international human rights treaties (ECHR, ICCPR, ICESCR).",
        "Restrictions require ALL four preconditions of Art. 36 Cst: legal basis, public interest or protection of others, proportionality, and respect for the essence of fundamental rights.",
    ])

    # ---- LECTURE CASE STUDY ----
    pdf.chapter_title("LECTURE CASE STUDY: IDENTIFICATION MEASURES")

    pdf.body_text("The following case is used throughout the lecture to apply the two-step analysis framework:")

    pdf.key_concept_box("Case: DNA Buccal Swab (Basel-Stadt)",
        "The public prosecutor's office of Basel-Stadt is conducting a criminal investigation against friend A. "
        "He is accused of surrounding the UBS building during climate action days: writing slogans with coal, "
        "taping surveillance cameras, and partially blocking entrances with wooden barricades. A. remained on "
        "the spot despite being ordered to leave and organized a sit-in blockade. He was carried away by police "
        "and temporarily detained. The police issued an order for identification measures based on Art. 255 "
        "Swiss Criminal Procedure Code (a federal statute), in particular a buccal swab (non-invasive sample "
        "of DNA from cells on the inside of the cheek) for a DNA profile.\n\n"
        "Question: Is a fundamental right affected, and is the restriction lawful?")

    pdf.subsection_title("Art. 255 Swiss Criminal Procedure Code")
    pdf.body_text("Para. 1: For the purpose of solving a felony or misdemeanor, a sample may be taken and a DNA profile may be obtained from:")
    pdf.bullet("(a) the accused person")
    pdf.bullet("(b) other persons, insofar as necessary to distinguish biological material originating from them from that of the accused")
    pdf.body_text("Para. 2: The police may order:")
    pdf.bullet("(a) the non-invasive taking of samples from persons")
    pdf.bullet("(b) the creation of a DNA profile of biological material relevant to the offence")

    # ---- TWO-STEP FRAMEWORK ----
    pdf.add_page()
    pdf.chapter_title("TWO-STEP ANALYSIS FRAMEWORK")

    pdf.body_text("The lecture introduces a two-step method for solving fundamental rights cases. This framework structures all exam answers.")

    pdf.section_title("Step 1: Is a Fundamental Right Affected?")
    pdf.bullet("(1) Is the fundamental right guaranteed on a national or international level?")
    pdf.bullet("(2) Is the scope of application of the fundamental right affected?")
    pdf.bullet("(3) Is the victim a beneficiary of the fundamental right?")
    pdf.bullet("(4) Is the claim filed against an addressee of the fundamental right?")
    pdf.bullet("Conclusion: A fundamental right is affected.", level=1)

    pdf.section_title("Step 2: Is the Restriction Lawful? (Art. 36 Cst)")
    pdf.bullet("(1) Is there a legal basis for the restriction? (Art. 36 para. 1)")
    pdf.bullet("(2) Is there a public interest or need to protect others' rights? (Art. 36 para. 2)")
    pdf.bullet("(3) Is the restriction proportionate? (Art. 36 para. 3)")
    pdf.bullet("(4) Is the essence of the fundamental right respected? (Art. 36 para. 4)")
    pdf.bullet("Conclusion: The restriction is lawful / unlawful.", level=1)

    # ---- CHAPTER G: FUNDAMENTAL RIGHTS ----
    pdf.add_page()
    pdf.chapter_title("CHAPTER G: FUNDAMENTAL RIGHTS -- GENERAL CONCEPT")

    pdf.section_title("1.1 Definition")
    pdf.body_text("Fundamental rights = constitutionally and internationally guaranteed legal entitlements of individuals in their relationship with the state, protecting essential freedoms.")

    pdf.body_text("Five key aspects:")
    pdf.bullet("**Beneficiaries**: Generally natural persons, but some rights extend to legal persons (companies)")
    pdf.bullet("**Addressees**: Can only be asserted against the state or entities fulfilling state functions, generally NOT against private persons")
    pdf.bullet("**Entitlements**: Individual entitlements, directly enforceable in courts (differ from mere state obligations)")
    pdf.bullet("**Content**: Protect freedoms necessary to safeguard human dignity and development of essential personal characteristics")
    pdf.bullet("**Sources**: Federal and cantonal constitutions + international treaties (ECHR, ICESCR, ICCPR)")

    pdf.subsection_title("Distinctions")
    pdf.bullet("**Fundamental rights vs. Human rights**: Human rights are pre-constitutional, inalienable, indivisible rights inherent in every individual (natural law theory), guaranteed independently of a state. Fundamental rights are part of the positive law of a state, written legal rules.")
    pdf.bullet("**Fundamental rights vs. Constitutional rights**: Constitutional rights ('verfassungsmassige Rechte') is a broader procedural term from Federal Supreme Court case law. It encompasses all fundamental rights PLUS additional principles (legality in criminal matters, prohibition of intercantonal double taxation, communal autonomy, etc.).")

    # ---- CATEGORIZATION ----
    pdf.section_title("1.2 Categories of Fundamental Rights")

    pdf.subsection_title("a) Civil Liberties")
    pdf.body_text("Rooted in 18th century American and French declarations. Defensive rights against unwanted state action -- they confer spheres of freedom on the individual.")
    pdf.bullet("Personal liberty (Art. 10 para. 2 Cst)")
    pdf.bullet("Right to privacy (Art. 13 Cst)")
    pdf.bullet("Freedom of expression and information (Art. 16 Cst)")
    pdf.bullet("Freedom of the media (Art. 17 Cst)")
    pdf.bullet("Freedom of religion (Art. 15 Cst)")
    pdf.bullet("Freedom of assembly (Art. 22 Cst), Freedom of association (Art. 23 Cst)")
    pdf.bullet("Right to property (Art. 26 Cst), Economic freedom (Art. 27 Cst)")
    pdf.body_text("May also guarantee institutions: right to property (Art. 26 para. 1), marriage (Art. 14). Now recognized as guiding principles for overall state activity influencing the entire legal system.")

    pdf.subsection_title("b) Equality Before the Law")
    pdf.body_text("Every person is equal before the law and has the right to equal treatment by all state authorities (Art. 8 Cst). No discrimination on grounds of origin, race, gender, age, language, social position, way of life, or religious/ideological/political convictions. Also encompasses good faith and non-arbitrary treatment (Art. 9 Cst). Not restricted to a particular activity -- informs ALL state action.")

    pdf.subsection_title("c) Social Rights")
    pdf.body_text("Origins in 19th century industrialization. Oblige the state to take positive action -- give individuals access to specific resources, goods, and services:")
    pdf.bullet("Right to assistance when in need (Art. 12 Cst)")
    pdf.bullet("Right to basic education (Art. 19 Cst)")
    pdf.bullet("Protection of children and young people (Art. 11 Cst)")

    pdf.subsection_title("d) Procedural Rights")
    pdf.body_text("Swiss Constitution Arts. 29-32, greatly influenced by Art. 6 ECHR:")
    pdf.bullet("Right to public hearing before independent and impartial tribunal within reasonable time")
    pdf.bullet("Presumption of innocence")
    pdf.bullet("Adequate time and facilities to prepare defense")
    pdf.bullet("Access to legal representation")
    pdf.bullet("Right to examine witnesses")
    pdf.bullet("Right to free assistance of an interpreter")

    pdf.subsection_title("e) Political Rights")
    pdf.body_text("Right to participate in the political process (Art. 33-34 Cst). As a general rule, beneficiaries must be citizens of the state.")

    # ---- LEGAL SOURCES ----
    pdf.add_page()
    pdf.section_title("1.3 Legal Sources")

    pdf.subsection_title("a) National Level")
    pdf.body_text("The Constitution of 1999 contains a catalogue of fundamental rights in Chapter One of Title Two (Arts. 7-34 Cst):")
    pdf.bullet("Human dignity (Art. 7)")
    pdf.bullet("Equal protection (Art. 8)")
    pdf.bullet("Civil liberties and freedoms (Arts. 10, 13-18, 20-28)")
    pdf.bullet("Basic procedural rights (Arts. 29-32)")
    pdf.bullet("Political rights (Arts. 33-34)")
    pdf.bullet("Basic social rights (Arts. 11-12, 19)")
    pdf.bullet("Effective realization (Art. 35), Restrictions (Art. 36)")

    pdf.body_text("The catalogue is NOT exhaustive. Courts may recognize implied, unwritten fundamental rights if:")
    pdf.bullet("The right is a precondition for exercising other written fundamental rights, AND")
    pdf.bullet("The right is essential to the democratic order and the Rechtsstaat, AND")
    pdf.bullet("The right reflects widely shared cantonal constitutional practice and is generally accepted")

    pdf.subsection_title("b) International Level")
    pdf.body_text("The ECHR is of supreme importance. Drawn up within the Council of Europe after WWII as a reaction to wartime human rights violations. Key features: both interstate and individual applications, establishes a European minimum standard.")
    pdf.bullet("Switzerland ratified the ECHR in 1974 (monistic approach -- directly part of Swiss law)")
    pdf.bullet("ECHR rights are directly applicable before domestic courts")
    pdf.bullet("If both ECHR and Federal Constitution are invoked, whichever offers more protection applies (Art. 53 ECHR)")
    pdf.bullet("After exhausting domestic remedies, appeal to the European Court of Human Rights in Strasbourg")

    # Comparison table
    pdf.subsection_title("ECHR vs Swiss Constitution -- Comparison")
    w_right = 50
    w_echr = 50
    w_cst = 50
    widths = [w_right, w_echr, w_cst]
    if pdf.get_y() + 90 > pdf.h - pdf.b_margin:
        pdf.add_page()
    pdf.table_header(["Right", "ECHR", "Swiss Cst"], widths)
    pdf.table_row(["Right to life", "Art. 2, Prot. 6 & 13", "Art. 10 para. 1"], widths, fill=True)
    pdf.table_row(["Prohibition of torture", "Art. 3", "Art. 7, 10(3), 25(3)"], widths)
    pdf.table_row(["Prohibition of slavery", "Art. 4", "Art. 7, 10(2)"], widths, fill=True)
    pdf.table_row(["Right to liberty/security", "Art. 5", "Art. 10(2), 31"], widths)
    pdf.table_row(["Right to a fair trial", "Art. 6", "Art. 29-30, 32"], widths, fill=True)
    pdf.table_row(["No punishment without law", "Art. 7", "(Art. 1 Crim. Code)"], widths)
    pdf.table_row(["Private and family life", "Art. 8", "Art. 13"], widths, fill=True)
    pdf.table_row(["Freedom of conscience/religion", "Art. 9", "Art. 15"], widths)
    pdf.table_row(["Freedom of expression", "Art. 10", "Art. 16-17, 20-21"], widths, fill=True)
    pdf.table_row(["Freedom of assembly/assoc.", "Art. 11", "Art. 22-23, 28"], widths)
    pdf.table_row(["Right to marry", "Art. 12", "Art. 14"], widths, fill=True)
    pdf.table_row(["Right to effective remedy", "Art. 13", "Art. 29a"], widths)
    pdf.table_row(["Prohibition of discrimination", "Art. 14", "Art. 8 para. 2"], widths, fill=True)
    pdf.ln(2)

    pdf.subsection_title("Other Ratified International Conventions")
    pdf.bullet("UN Covenant on Economic, Social and Cultural Rights (1966), SR 0.103.1")
    pdf.bullet("UN Covenant on Civil and Political Rights (1966), SR 0.103.2")
    pdf.bullet("International Convention on the Elimination of All Forms of Racial Discrimination (1965), SR 0.104")
    pdf.bullet("UN Convention against Torture (1984), SR 0.105")
    pdf.bullet("European Convention for the Prevention of Torture (1987), SR 0.106")
    pdf.bullet("UN Convention on the Rights of the Child (1989), SR 0.107")
    pdf.body_text("These are directly applicable (self-executing) in Switzerland insofar as they are clearly formulated and have direct bearing on a specific case.")

    # ---- DIMENSIONS ----
    pdf.add_page()
    pdf.section_title("1.4 Dimensions of Fundamental Rights")

    pdf.subsection_title("Defensive Dimension (Primary, Historical)")
    pdf.body_text("Individuals defend their private sphere from state interference. The state must respect the protected sphere and refrain from undue intrusions.")

    pdf.subsection_title("Constitutive Dimension")
    pdf.body_text("Fundamental rights also act as guiding principles for overall state activity, influencing the entire legal system. Expressed by their placement in Title Two of the Constitution and Art. 35 para. 1 Cst.")

    pdf.subsection_title("Negative vs Positive Obligations")
    pdf.bullet("**Negative obligations**: The state must refrain from interfering with the enjoyment of rights")
    pdf.bullet("**Positive obligations**: The state must take action to ensure individuals can enjoy civil liberties without interference from third parties and free from natural or human-made risks")
    pdf.body_text("Forms of positive obligations:")
    pdf.bullet("General legislation (e.g., penalizing murder to protect right to life)")
    pdf.bullet("Individual measures protecting specific persons or groups")
    pdf.bullet("Individual obligation to protect arises only if the state is aware (or should have been aware) of the violation/threat AND has practical and legal means to prevent it")

    # ---- SPECIFIC RIGHTS FROM LECTURE ----
    pdf.section_title("Specific Rights Detailed in Lecture")

    pdf.subsection_title("Right to Personal Liberty (Art. 10 para. 2 Cst)")
    pdf.body_text("Encompasses three sub-rights:")
    pdf.bullet("**Physical integrity**: Affected by any interference with the body of an individual, even if it does not cause any pain or damage")
    pdf.bullet("**Mental integrity**: Protects the psychological well-being of the individual")
    pdf.bullet("**Freedom of movement**: Protects against deprivation of liberty without legal justification, e.g., detention against one's will")

    pdf.subsection_title("Right to Informational Self-Determination (Art. 13 Cst)")
    pdf.body_text("Must be interpreted broadly as a general fundamental right to informational self-determination:")
    pdf.bullet("Protects against unlimited collection, processing, storage and dissemination of personal data")
    pdf.bullet("In particular covers the collection and storage of **biometric and genetic data** by the authorities")

    # ---- BENEFICIARIES ----
    pdf.section_title("1.5 Beneficiaries")

    pdf.bullet("**Natural persons**: Can invoke all fundamental rights. Foreign nationals can invoke all rights EXCEPT: political rights (Art. 34), freedom of domicile (Art. 24), protection against expulsion (Art. 25 para. 1). May face restrictions on economic freedom depending on legal status (Art. 27).")
    pdf.bullet("**Persons with special state relationship** (Sonderstatusverhaltnis): Public officers, soldiers, prisoners, students. They are beneficiaries but their special relationship can justify specific restrictions (e.g., freedom of speech restricted by duty of loyalty).")
    pdf.bullet("**Legal persons under private law** (companies): Can invoke rights not exclusively tied to human existence. Cannot invoke right to life or right to marriage. CAN invoke freedom of property, equality before the law.")
    pdf.bullet("**Legal persons under public law** (e.g., communes): Can only invoke fundamental rights under exceptional circumstances -- when they act under private law and are affected by state activities in the same way as an individual.")

    # ---- ADDRESSEES ----
    pdf.section_title("1.6 Addressees")
    pdf.body_text("Fundamental rights can only be asserted against the state (all state authorities at every level):")
    pdf.bullet("**Legislature**: Must account for fundamental rights when enacting new laws")
    pdf.bullet("**Executive**: Must observe fundamental rights in day-to-day enforcement AND when preparing legislation/ordinances")
    pdf.bullet("**Judiciary**: Must redress violations, interpret provisions in conformity with fundamental rights, refuse to apply conflicting norms")

    pdf.body_text("Art. 35 para. 2 Cst: Those exercising a state function must also respect fundamental rights, including private entities performing delegated public tasks (e.g., a private security firm mistreating a prisoner).")

    pdf.subsection_title("Third-Party Applicability (Drittwirkung)")
    pdf.body_text("Private persons are generally NOT addressees. Two exceptions:")
    pdf.bullet("**Direct third-party applicability** (direkte Drittwirkung): Art. 8 para. 3 Cst, last sentence -- men and women have the right to equal pay for work of equal value. Private enterprises must respect this.")
    pdf.bullet("**Indirect third-party applicability** (indirekte Drittwirkung, Art. 35 para. 3 Cst): Fundamental rights as essential values influence private relationships indirectly. Courts must consider fundamental rights when applying general clauses or open legal terms.")

    pdf.article_box([
        "**Art. 8 para. 3 Cst** (last sentence): Men and women have the right to equal pay for work of equal value -> direct third-party applicability",
        "**Art. 35 para. 2 Cst**: Those exercising a state function must respect fundamental rights",
        "**Art. 35 para. 3 Cst**: Authorities must ensure fundamental rights apply to private relations where appropriate -> indirect third-party applicability",
    ])

    # ---- RESTRICTIONS (ART. 36 CST) ----
    pdf.add_page()
    pdf.chapter_title("RESTRICTIONS OF FUNDAMENTAL RIGHTS (ART. 36 CST)")

    pdf.body_text("Fundamental rights are NOT absolute. Art. 36 Cst prescribes four **cumulative** conditions -- ALL must be met for a restriction to be lawful.")

    # a) Legal Basis
    pdf.section_title("a) Legal Basis (Art. 36 para. 1)")
    pdf.body_text("Two elements must be satisfied:")

    pdf.subsection_title("Element 1: Legal Rule (Rechtssatz)")
    pdf.bullet("Must be **generally applicable** (indefinite number of individuals) and **abstract** (indefinite number of cases) -- links to equality before the law")
    pdf.bullet("Must be formulated with **sufficient precision** so individuals can understand what conduct is prohibited and foresee consequences -- links to legal certainty")
    pdf.bullet("Degree of precision depends on: identity of addressees, gravity of limitation, complexity and foreseeability")

    pdf.subsection_title("Element 2: Legal Form (Gesetzesform)")
    pdf.bullet("**Significant restrictions** (imprisonment, monitoring communications): Must be based in a statute enacted by the legislature (federal or cantonal), subject to referendum. An executive ordinance does NOT suffice.")
    pdf.bullet("**Minor restrictions**: May be provided for in an executive ordinance adopted by executive authorities.")
    pdf.bullet("The democratic legitimacy needs to be higher, the more significant a restriction is.")

    pdf.subsection_title("Exception: General Police Clause (Art. 36 para. 1, sentence 3)")
    pdf.body_text("In cases of serious and immediate danger where no other course of action is possible, the general police clause may temporarily substitute for a legal basis. Four conditions must ALL be met:")
    pdf.bullet("(1) Very important public interests or interests of individuals are endangered")
    pdf.bullet("(2) Serious danger exists or these interests have already been disrupted")
    pdf.bullet("(3) The situation calls for immediate action")
    pdf.bullet("(4) No adequate legal measures are provided for")

    pdf.key_concept_box("Case: Jura Separatist Struggle (BGE 103 Ia 310)",
        "In 1977, the executive of Canton Bern prohibited all political assemblies in Moutier for two days "
        "based on the general police clause, during the Jura separatist movement (arson attacks by separatists). "
        "The Federal Supreme Court held it legitimate. However, the textbook notes that nowadays such a general "
        "prohibition would likely be considered problematic.")

    # b) Public Interest
    pdf.section_title("b) Public Interest or Protection of Others (Art. 36 para. 2)")
    pdf.body_text("Restrictions must be justified by public interests or by the need to protect fundamental rights of others. Public interest encompasses all measures available to the state for the promotion of the common good:")
    pdf.bullet("**Police interests**: Protection of public order, safety, peace, health, morals, and good faith in business dealings")
    pdf.bullet("**Other examples**: Environmental protection, land-use planning, socio-political considerations restricting economic freedom")
    pdf.bullet("Civil liberties must be limited to permit concurrent exercise by the entire population (one person's enjoyment must not overly interfere with another's)")

    # c) Proportionality
    pdf.section_title("c) Proportionality (Art. 36 para. 3)")
    pdf.body_text("Three sub-conditions must EACH be fulfilled:")

    pdf.subsection_title("(1) Adequacy (Eignung)")
    pdf.body_text("The regulatory measure must be adequate to achieve the legitimate public purpose.")

    pdf.subsection_title("(2) Necessity (Erforderlichkeit)")
    pdf.body_text("The measure must be necessary. If less restrictive measures could achieve the same goal, the restriction is disproportionate.")

    pdf.subsection_title("(3) Proportionality in the Narrow Sense (Verhaltnismassigkeit i.e.S.)")
    pdf.body_text("The public and private interests must be balanced. If the negative effects on the individual outweigh the public interests, the measure is disproportionate.")

    pdf.key_concept_box("Proportionality Balancing",
        "LEFT side: Private interests in the protection of the fundamental right concerned.\n"
        "RIGHT side: Public interests in restricting the fundamental right + protection of fundamental rights of third persons.\n"
        "The two sides must be weighed against each other. If private interests outweigh, the restriction is unlawful.")

    # d) Essence
    pdf.section_title("d) Essence of Fundamental Rights (Art. 36 para. 4)")
    pdf.body_text("The core content of each fundamental right can never be restricted. If a restriction disregards the essence, it is per se a violation of the Constitution -- no justification is possible.")
    pdf.body_text("Some rights are per se inviolable:")
    pdf.bullet("Human dignity (Art. 7 Cst) -- absolutely prohibited to compromise")
    pdf.bullet("Prohibition of death penalty (Art. 10 para. 1 Cst)")
    pdf.bullet("Prohibition of torture and cruel/inhuman/degrading treatment (Art. 10 para. 3 Cst)")
    pdf.body_text("For other rights, the essence cannot be defined abstractly but must be determined through Federal Supreme Court case law.")

    pdf.article_box([
        "**Art. 36 para. 1 Cst**: Restrictions require a legal basis; significant restrictions need a formal statute",
        "**Art. 36 para. 2 Cst**: Restrictions must serve a public interest or protect others' fundamental rights",
        "**Art. 36 para. 3 Cst**: Restrictions must be proportionate (adequate, necessary, proportionate in narrow sense)",
        "**Art. 36 para. 4 Cst**: The essence of fundamental rights may not be violated under any circumstances",
    ])

    # ---- CASE APPLICATION ----
    pdf.add_page()
    pdf.chapter_title("CASE APPLICATION: IDENTIFICATION MEASURES")

    pdf.section_title("Step 1: Is a Fundamental Right Affected?")

    pdf.subsection_title("(1) Guarantee on national/international level?")
    pdf.body_text("Yes. Right to personal liberty (Art. 10 para. 2 Cst) and right to informational self-determination/privacy (Art. 13 Cst) are guaranteed in the Federal Constitution. Also protected under ECHR Art. 8 (right to private life).")

    pdf.subsection_title("(2) Scope of application affected?")
    pdf.body_text("Yes. A buccal swab is an interference with the body (physical integrity under Art. 10 para. 2), even though it is non-invasive and causes no pain. The creation of a DNA profile involves collection of biometric/genetic data (informational self-determination under Art. 13).")

    pdf.subsection_title("(3) Is A. a beneficiary?")
    pdf.body_text("Yes. A. is a natural person and can invoke all fundamental rights.")

    pdf.subsection_title("(4) Claim against an addressee?")
    pdf.body_text("Yes. The police and public prosecutor's office are state authorities.")

    pdf.body_text("**Conclusion**: Fundamental rights (personal liberty and informational self-determination) are affected.")

    pdf.section_title("Step 2: Is the Restriction Lawful?")

    pdf.subsection_title("(1) Legal basis?")
    pdf.body_text("Yes. Art. 255 Swiss Criminal Procedure Code is a federal statute enacted by the legislature. It authorizes the police to order non-invasive sampling and DNA profiling of accused persons. The provision is sufficiently precise and has the required legal form for a significant restriction.")

    pdf.subsection_title("(2) Public interest?")
    pdf.body_text("Yes. The investigation and prosecution of criminal offences (here: criminal damage, trespass) serves the public interest in maintaining public order and safety.")

    pdf.subsection_title("(3) Proportionate?")
    pdf.bullet("**Adequate**: DNA identification is suitable for identifying the accused and linking them to evidence at the crime scene")
    pdf.bullet("**Necessary**: A buccal swab is the least invasive method for obtaining DNA (compared to blood samples); alternative identification methods may be insufficient")
    pdf.bullet("**Proportionate in narrow sense**: The interference is minor (non-invasive, no pain) relative to the public interest in solving criminal offences. The measure appears proportionate.")

    pdf.subsection_title("(4) Essence respected?")
    pdf.body_text("Yes. A non-invasive buccal swab does not touch the essence of personal liberty or informational self-determination. Human dignity is not compromised.")

    pdf.body_text("**Conclusion**: The restriction of A.'s fundamental rights is lawful under Art. 36 Cst.")

    # ---- KEY ARTICLES ----
    pdf.add_page()
    pdf.chapter_title("KEY ARTICLES AND ABBREVIATIONS")

    pdf.article_box([
        "**Art. 7 Cst**: Human dignity (inviolable core)",
        "**Art. 8 Cst**: Equality before the law; para. 2: non-discrimination; para. 3: equal pay (direct Drittwirkung)",
        "**Art. 9 Cst**: Protection against arbitrariness and good faith",
        "**Art. 10 Cst**: Right to life (para. 1), personal liberty (para. 2), prohibition of torture (para. 3)",
        "**Art. 11 Cst**: Protection of children and young people",
        "**Art. 12 Cst**: Right to assistance when in need",
        "**Art. 13 Cst**: Right to privacy and informational self-determination",
        "**Art. 14 Cst**: Right to marry and found a family",
        "**Art. 15 Cst**: Freedom of religion and conscience",
        "**Art. 16-17 Cst**: Freedom of expression, freedom of the media",
        "**Art. 19 Cst**: Right to basic education",
        "**Art. 22-23 Cst**: Freedom of assembly, freedom of association",
        "**Art. 26 Cst**: Right to property; Art. 27: Economic freedom",
        "**Art. 29-32 Cst**: Procedural rights (fair trial, presumption of innocence, etc.)",
        "**Art. 33-34 Cst**: Political rights",
        "**Art. 35 Cst**: Realization of fundamental rights (para. 1: throughout legal system; para. 2: state functions; para. 3: indirect Drittwirkung)",
        "**Art. 36 Cst**: Restrictions (legal basis, public interest, proportionality, essence)",
        "**ECHR Arts. 2-14**: European Convention rights (see comparison table above)",
        "**Art. 255 CrimPC**: DNA sampling/profiling for criminal investigation",
    ])

    pdf.section_title("Key Abbreviations")
    pdf.bullet("**Cst** = Federal Constitution of the Swiss Confederation")
    pdf.bullet("**ECHR** = European Convention on Human Rights")
    pdf.bullet("**ICCPR** = International Covenant on Civil and Political Rights")
    pdf.bullet("**ICESCR** = International Covenant on Economic, Social and Cultural Rights")
    pdf.bullet("**CrimPC** = Swiss Criminal Procedure Code")
    pdf.bullet("**BGE** = Bundesgerichtsentscheid (Federal Supreme Court decision)")
    pdf.bullet("**ECtHR** = European Court of Human Rights (Strasbourg)")
    pdf.bullet("**Drittwirkung** = Third-party applicability of fundamental rights")
    pdf.bullet("**Sonderstatusverhaltnis** = Special state relationship (officers, prisoners, students)")

    out = os.path.join(os.path.dirname(__file__), "Lecture5_Fundamental_Rights.pdf")
    pdf.output(out)
    print(f"Generated: {out}")


if __name__ == "__main__":
    generate_lecture1()
    generate_lecture2()
    generate_lecture3()
    generate_lecture4()
    generate_lecture5()
    print("\nAll law lecture notes generated successfully!")
