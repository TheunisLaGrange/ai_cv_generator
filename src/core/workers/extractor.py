import json
from pathlib import Path

def load_cv_source_data(base_dir: Path) -> dict:
    """Reads and parses all user datasets safely from the User_Data directory."""
    user_data_dir = base_dir / "User_Data"
    user_data_dir.mkdir(exist_ok=True)
    
    job_spec_path = user_data_dir / "job_spec.txt"
    my_cv_path = user_data_dir / "my_cv.json"
    profile_cfg_path = user_data_dir / "user_profile.json"

    for required_file in [job_spec_path, my_cv_path, profile_cfg_path]:
        if not required_file.exists():
            raise FileNotFoundError(f"Missing required user data file: {required_file}")

    with open(job_spec_path, 'r', encoding='utf-8') as f:
        job_spec_data = f.read()
    with open(my_cv_path, 'r', encoding='utf-8') as f:
        my_cv_data = json.load(f)
    with open(profile_cfg_path, 'r', encoding='utf-8') as f:
        user_profile_data = json.load(f)
        
    return {
        "job_spec": job_spec_data,
        "my_cv": my_cv_data,
        "user_profile": user_profile_data,
        "profile_only": {
            "Professional Profile": my_cv_data.get("Professional Profile", []),
            "Professional Experience": my_cv_data.get("Professional Experience", []),
            "Education & Certifications": my_cv_data.get("Education & Certifications", [])
        },
        "skills_only": {
            "Key Skills and Technical Expertise": my_cv_data.get("Key Skills and Technical Expertise", []),
            "Professional Experience": my_cv_data.get("Professional Experience", []),
            "Education & Certifications": my_cv_data.get("Education & Certifications", [])
        }
    }
