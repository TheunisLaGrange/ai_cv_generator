from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfWriter

def compile_document_package(base_dir: Path, target_data: dict, user_profile: dict):
    """Generates the base CV PDF and appends verification certificates using dynamic user profile settings."""
    output_folder = base_dir / "Output"
    output_folder.mkdir(exist_ok=True)
    
    file_prefix = user_profile.get("output_file_prefix", "Candidate_CV")
    cv_without_qual_path = output_folder / f"{file_prefix}_without_qualifications.pdf"
    
    # SimpleDocTemplate Layout Configuration
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
        story.append(Paragraph(contact.get("Full Name", default_name), title_style))
        story.append(Paragraph(contact.get("Profession", default_role), subtitle_style))
        story.append(Paragraph(f"<b>Address:</b> {contact.get('Address', '')}", contact_style))
        story.append(Paragraph(f"<b>Cell:</b> {contact.get('Cell', '')}", contact_style))
        story.append(Paragraph(f"<b>Mail:</b> {contact.get('Mail', '')}", contact_style))
        story.append(Spacer(1, 8))

    for section_title, section_content in target_data.items():
        if section_title == "Contact Details":
            continue
            
        header_group = [
            Paragraph(section_title, heading_style),
            HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=6, spaceAfter=6)
        ]
        
        if isinstance(section_content, list) and section_content:
            header_group.append(Paragraph(f"&bull;&nbsp;&nbsp;{section_content[0]}", bullet_style))
            story.append(KeepTogether(header_group))
            
            for item in section_content[1:]:
                story.append(Paragraph(f"&bull;&nbsp;&nbsp;{item}", bullet_style))
        else:
            story.append(KeepTogether(header_group))
            
        story.append(Spacer(1, 2))

    doc.build(story)

    # PyPDF Credentials Append Layer
    qual_folder = base_dir / "User_Data" / "Qualifications"
    merger = PdfWriter()
    merger.append(str(cv_without_qual_path))
    
    for cert in user_profile.get("certificates", []):
        cert_file = qual_folder / cert
        if cert_file.exists():
            merger.append(str(cert_file))

    cv_with_qual_path = output_folder / f"{file_prefix}_with_qualifications.pdf"
    merger.write(str(cv_with_qual_path))
    merger.close()
