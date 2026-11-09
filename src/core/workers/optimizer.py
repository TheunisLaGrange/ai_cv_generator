import json
from google.genai import types
from pydantic import BaseModel, Field

class TailoredProfile(BaseModel):
    professional_profile: list[str] = Field(
        description="4 tailored bullet points selling the candidate's real experience for the target job."
    )

class ExtractedSkills(BaseModel):
    key_skills_and_technical_expertise: list[str] = Field(
        description="A prioritized list of 6 to 10 technical skills from the CV that best match the job spec."
    )

async def run_cognitive_pipeline(client, model_name: str, source_data: dict) -> dict:
    """Dispatches asynchronous structural optimization prompts to the Gemini endpoints."""
    job_spec = source_data["job_spec"]
    print(f"🚀 [Optimizer] Sending job_spec ({len(job_spec)} chars) + CV context to {model_name}...")
    
    # A. Execute Profile Optimization (Strict Grounding + Persuasive Framing)
    profile_prompt = f"""
You are an expert technical resume writer. Rewrite the 'Professional Profile' into 4 sharp, persuasive bullet points tailored specifically to the Job Specification below.

STRICT RULES:
1. ZERO FABRICATION: Every claim, tool, industry, and year of experience MUST come strictly from the provided Source CV data. Do not invent new skills or employers.
2. MIRROR TERMINOLOGY: Use the exact keywords, equipment types, and responsibilities mentioned in the Job Specification where they match the candidate's real background.
3. LEAD WITH STRENGTHS: Highlight the candidate's most relevant qualifications (e.g., Trade Tested Electrician, N6 Electrotechnology, Mechatronics, PLC/SCADA, preventative maintenance, safety compliance) first.
4. REMOVE NOISE: Omit background details from the summary that do not help sell the candidate for this specific role.

Job Specification:
{job_spec}

Source CV Data:
{json.dumps(source_data['profile_only'], indent=2)}
"""
    profile_res = await client.aio.models.generate_content(
        model=model_name, 
        contents=profile_prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json', 
            response_schema=TailoredProfile, 
            temperature=0.2
        )
    )
    tailored_profile = json.loads(profile_res.text)
    print("\n✨ [AI Tailored Professional Profile]:")
    for bullet in tailored_profile.get("professional_profile", []):
        print(f"   • {bullet}")

    # B. Execute Technical Skills Extraction & Filtering
    tasks = [
        "1. SELECT & FILTER: Review the candidate's 'Key Skills and Technical Expertise', 'Professional Experience', and 'Education & Certifications'. Keep ONLY the skills that directly support the Job Specification. Remove skills that are irrelevant to this role.",
        "2. REORDER BY IMPACT: Place the highest-priority skills matching the job spec at the very top of the list.",
        "3. REPHRASE TO SELL: Rewrite the kept skill bullets using strong, employer-facing phrasing from the Job Specification, while remaining 100% faithful to the candidate's actual documented experience.",
        "4. NO HALLUCINATIONS: Never add a tool, PLC brand, or certification that is not explicitly present in the Source CV Data."
    ]
    
    if any(k in job_spec.lower() for k in ["erp", "mes", "sap", "ipro"]):
        tasks.append('5. MANDATE: Include this exact phrase: "Used SAP iPro ERP/MES while working on Mercedes Benz contract".')
    if any(k in job_spec.lower() for k in ["safety", "compliance", "electrical compliance"]):
        tasks.append('6. MANDATE: Include this exact phrase: "Ensured strict compliance with national electrical wiring codes (e.g., SANS 10142 / NEC) during installation and maintenance".')

    skills_prompt = f"""
You are an expert technical recruiter and resume optimizer. Tailor the 'Key Skills and Technical Expertise' section to maximize interview selection for the Job Specification below.

Tasks:
{chr(10).join(tasks)}

Job Specification:
{job_spec}

Source CV Data:
{json.dumps(source_data['skills_only'], indent=2)}
"""
    skills_res = await client.aio.models.generate_content(
        model=model_name, 
        contents=skills_prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json', 
            response_schema=ExtractedSkills, 
            temperature=0.1
        )
    )
    extracted_skills = json.loads(skills_res.text)
    print("\n✨ [AI Tailored Key Skills]:")
    for skill in extracted_skills.get("key_skills_and_technical_expertise", []):
        print(f"   • {skill}")

    return {
        "Contact Details": source_data["my_cv"].get("Contact Details", {}),
        "Professional Profile": tailored_profile.get("professional_profile", []),
        "Key Skills and Technical Expertise": extracted_skills.get("key_skills_and_technical_expertise", []),
        "Professional Experience": source_data["my_cv"].get("Professional Experience", []),
        "Education & Certifications": source_data["my_cv"].get("Education & Certifications", []),
        "Core Competencies": source_data["my_cv"].get("Core Competencies", []),
        "Languages": source_data["my_cv"].get("Languages", [])
    }
