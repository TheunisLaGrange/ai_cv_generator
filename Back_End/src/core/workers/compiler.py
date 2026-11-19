from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfWriter

# =====================================================================
# 🔬 REPORTLAB MARKUP CONVERSION LAYER
# =====================================================================
def clean_text_for_reportlab(text: str) -> str:
    """
    Converts raw text, unicode subscripts, and superscripts into 
    ReportLab-compatible HTML markup tags.
    """
    if not text:
        return ""
    
    # 1. Clean up common XML entities so the Paragraph parser doesn't crash
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # 2. Map common unicode subscripts/superscripts to HTML tags
    unicode_map = {
        # Subscripts
        "₀": "<sub>0</sub>", "₁": "<sub>1</sub>", "₂": "<sub>2</sub>", 
        "₃": "<sub>3</sub>", "₄": "<sub>4</sub>", "₅": "<sub>5</sub>",
        "₆": "<sub>6</sub>", "₇": "<sub>7</sub>", "₈": "<sub>8</sub>", "₉": "<sub>9</sub>",
        # Superscripts
        "⁰": "<sup>0</sup>", "¹": "<sup>1</sup>", "²": "<sup>2</sup>", 
        "³": "<sup>3</sup>", "⁴": "<sup>4</sup>", "⁵": "<sup>5</sup>",
        "⁶": "<sup>6</sup>", "⁷": "<sup>7</sup>", "⁸": "<sup>8</sup>", "⁹": "<sup>9</sup>"
    }
    
    for uni_char, html_tag in unicode_map.items():
        text = text.replace(uni_char, html_tag)
        
    # 3. Fallback: Catch raw escaped literal sequences if they slip through as text
    text = text.replace(r"\u2082", "<sub>2</sub>")
    text = text.replace(r"\u2072", "<sup>2</sup>")
    
    return text

def compile_document_package(base_dir: Path, target_data: dict, user_profile: dict):
    """Generates the base CV PDF and appends verification certificates using dynamic user profile settings."""
    output_folder = base_dir / "Output"
    output_folder.mkdir(exist_ok=True)
    
    file_prefix = user_profile.get("output_file_prefix", "Theunis_La_Grange")
    cv_without_qual_path = output_folder / f"{file_prefix}_without_qualifications.pdf"
    
    doc = SimpleDocTemplate(
        str(cv_without_qual_path), 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    
    c_primary = colors.HexColor("#2D3748")
    c_secondary = colors.HexColor("#9B2C2C")
    
    title_style = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=c_primary, spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSubtitle', fontName='Helvetica', fontSize=13, leading=17, textColor=c_secondary, spaceAfter=12)
    contact_style = ParagraphStyle('DocContactLine', fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor("#374151"), spaceAfter=3)
    heading_style = ParagraphStyle('SectionHeading', fontName='Helvetica-Bold', fontSize=14, leading=19, textColor=c_primary, spaceBefore=4, spaceAfter=4, keepWithNext=True)
    bullet_style = ParagraphStyle('BulletItem', fontName='Helvetica', fontSize=10, leading=16, textColor=colors.HexColor("#0B0F19"), leftIndent=15, firstLineIndent=-10, spaceAfter=5)

    story = []
    contact = target_data.get("Contact Details", {})
    if contact:
        default_name = user_profile.get("default_full_name", "CANDIDATE NAME")
        default_role = user_profile.get("default_profession", "Technical Specialist")
        
        # Extract and sanitize dynamic fields independently 
        name_val = clean_text_for_reportlab(contact.get("Full Name", default_name))
        role_val = clean_text_for_reportlab(contact.get("Profession", default_role))
        addr_val = clean_text_for_reportlab(contact.get('Address', ''))
        cell_val = clean_text_for_reportlab(contact.get('Cell', ''))
        mail_val = clean_text_for_reportlab(contact.get('Mail', ''))
        
        # 🎯 FIX: Wrap the sanitized values inside the structural markup strings safely
        story.append(Paragraph(name_val, title_style))
        story.append(Paragraph(role_val, subtitle_style))
        story.append(Paragraph(f"<b>Address:</b> {addr_val}", contact_style))
        story.append(Paragraph(f"<b>Cell:</b> {cell_val}", contact_style))
        story.append(Paragraph(f"<b>Mail:</b> {mail_val}", contact_style))
        story.append(Spacer(1, 8))

    for section_title, section_content in target_data.items():
        if section_title == "Contact Details":
            continue
            
        header_group = [
            Paragraph(clean_text_for_reportlab(section_title), heading_style),
            HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=6, spaceAfter=6)
        ]
        
        if isinstance(section_content, list) and section_content:
            # 🎯 FIX: Pull the individual list element out BEFORE sanitizing it
            sanitized_bullet_0 = clean_text_for_reportlab(section_content[0])
            header_group.append(Paragraph(f"&bull;&nbsp;&nbsp;{sanitized_bullet_0}", bullet_style))
            story.append(KeepTogether(header_group))
            
            for item in section_content[1:]:
                sanitized_bullet_item = clean_text_for_reportlab(item)
                story.append(Paragraph(f"&bull;&nbsp;&nbsp;{sanitized_bullet_item}", bullet_style))

        else:
            story.append(KeepTogether(header_group))
            
        story.append(Spacer(1, 2))

    doc.build(story)

    # =====================================================================
    # 🗂️ DYNAMIC CREDENTIALS AUTO-APPEND LAYER
    # =====================================================================
    qual_folder = base_dir / "User_Data" / "Qualifications"
    merger = PdfWriter()
    
    print(f"📊 [PyPDF Layer] Loading tailored base CV file: {cv_without_qual_path.name}")
    merger.append(str(cv_without_qual_path))
    
    if qual_folder.exists():
        found_certs = sorted(
            [f for f in qual_folder.iterdir() if f.suffix.lower() == '.pdf' and f.name != 'ID_of_T_La_Grange.pdf'],
            key=lambda x: x.name
        )
        
        for cert_file in found_certs:
            print(f"   📎 Auto-Bundling verified credential asset: {cert_file.name}")
            merger.append(str(cert_file))
    else:
        print(f"⚠️ [PyPDF Warning] Qualifications subfolder directory path not found: {qual_folder}")

    cv_with_qual_path = output_folder / f"{file_prefix}_with_qualifications.pdf"
    
    merger.write(str(cv_with_qual_path))
    merger.close()
    print(f"🎉 SUCCESS: Unified credentials bundle package compiled to: {cv_with_qual_path.name}\n")
