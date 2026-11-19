import json
from groq import AsyncGroq

async def run_cognitive_pipeline(client: AsyncGroq, model_name: str, source_data: dict) -> dict:
    """Dispatches a single unified prompt to combine profile tailoring and skills formatting."""
    job_spec = source_data["job_spec"]
    templates = source_data.get("cognitive_templates", {})
    
    # Extract rules cleanly from yaml mappings to ensure modular flexibility
    profile_rules = templates.get("profile_optimization", {}).get("rules", [])
    skills_tasks = templates.get("skills_extraction", {}).get("core_tasks", [])
    
    print(f"🚀 [Optimizer] Sending unified workspace mapping pipeline to Groq: [{model_name}]...")
    
    # Evaluate conditional validation rules downstream before formatting prompt vectors
    conditional_tasks = []
    if any(k in job_spec.lower() for k in ["erp", "mes", "sap", "ipro"]):
        conditional_tasks.append('Include this exact phrase in skills: "Used SAP iPro ERP/MES while working on Mercedes Benz contract".')
    if any(k in job_spec.lower() for k in ["safety", "compliance", "electrical compliance", "overtime", "weekend", "shutdown"]):
        conditional_tasks.append('Include this exact phrase in skills: "Proven history of executing under-pressure industrial shutdown operations, with absolute willingness to work flexible overtime and weekend shifts".')

    unified_prompt = f"""
You are an expert technical resume writer and recruiter. Optimize the candidate's CV data based strictly on the Job Specification provided.

--- PROFILE OBJECTIVE RULES ---
{chr(10).join([f"- {r}" for r in profile_rules])}

--- SKILLS OBJECTIVE TASKS ---
{chr(10).join([f"- {t}" for t in skills_tasks])}
{chr(10).join([f"- {c}" for c in conditional_tasks])}

Target Job Specification:
{job_spec}

Source CV Profile Data:
{json.dumps(source_data['profile_only'], indent=2)}

Source CV Skills Data:
{json.dumps(source_data['skills_only'], indent=2)}

You MUST output your response strictly as a JSON object matching this schema structure:
{{
    "professional_profile": ["sharp bullet 1", "sharp bullet 2", "sharp bullet 3", "sharp bullet 4"],
    "key_skills_and_technical_expertise": ["prioritized skill 1", "prioritized skill 2", ...]
}}
"""

    response = await client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": unified_prompt}],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("❌ Received empty text content packet response from Groq cloud cloud servers.")
        
    result_payload = json.loads(content)
    
    print("\n✨ [AI Tailored Professional Profile]:")
    for bullet in result_payload.get("professional_profile", []):
        print(f"   • {bullet}")
        
    print("\n✨ [AI Tailored Key Skills]:")
    for skill in result_payload.get("key_skills_and_technical_expertise", []):
        print(f"   • {skill}")

    return {
        "professional_profile": result_payload.get("professional_profile", []),
        "key_skills_and_technical_expertise": result_payload.get("key_skills_and_technical_expertise", [])
    }
