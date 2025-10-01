import os

def create_project_structure(project_name="momentum"):
    """
    Creates the professional folder structure for the Momentum AI project.
    """
    print(f"🚀 Initializing project: {project_name}")

    # Define the structure as a list of tuples (path, is_directory)
    # If is_directory is False, it will create an empty file.
    structure = [
        (project_name, True),
        (os.path.join(project_name, ".env.example"), False),
        (os.path.join(project_name, ".gitignore"), False),
        (os.path.join(project_name, "README.md"), False),
        (os.path.join(project_name, "requirements.txt"), False),
        (os.path.join(project_name, "agent"), True),
        (os.path.join(project_name, "agent", "__init__.py"), False),
        (os.path.join(project_name, "agent", "main.py"), False),
        (os.path.join(project_name, "agent", "core"), True),
        (os.path.join(project_name, "agent", "core", "__init__.py"), False),
        (os.path.join(project_name, "agent", "core", "config.py"), False),
        (os.path.join(project_name, "agent", "core", "planner.py"), False),
        (os.path.join(project_name, "agent", "crud"), True),
        (os.path.join(project_name, "agent", "crud", "__init__.py"), False),
        (os.path.join(project_name, "agent", "crud", "crud_plan.py"), False),
        (os.path.join(project_name, "agent", "database.py"), False),
        (os.path.join(project_name, "agent", "models"), True),
        (os.path.join(project_name, "agent", "models", "__init__.py"), False),
        (os.path.join(project_name, "agent", "models", "schemas.py"), False),
        (os.path.join(project_name, "data"), True),
        (os.path.join(project_name, "data", ".gitkeep"), False),
        (os.path.join(project_name, "ui"), True),
        (os.path.join(project_name, "ui", "main.py"), False),
        (os.path.join(project_name, "ui", "pages"), True),
        (os.path.join(project_name, "ui", "pages", "1_🏠_Home.py"), False),
        (os.path.join(project_name, "ui", "pages", "2_📈_My_Plan.py"), False),
        (os.path.join(project_name, "ui", "pages", "3_⚙️_Settings.py"), False),
    ]

    # --- Content for our files ---
    file_contents = {
        ".gitignore": (
            "# Python\n"
            "__pycache__/\n"
            "*.pyc\n"
            "venv/\n\n"
            "# Environment Variables\n"
            ".env\n\n"
            "# Database\n"
            "data/*.db\n"
        ),
        "requirements.txt": (
            "fastapi\n"
            "uvicorn[standard]\n"
            "streamlit\n"
            "requests\n"
            "pydantic\n"
            "python-dotenv\n"
            "sqlalchemy\n"
        ),
        ".env.example": (
            "# Copy this file to .env and fill in your actual API keys\n"
            "OPENAI_API_KEY=\"your_openai_api_key_here\"\n"
            "SERPAPI_KEY=\"your_serpapi_key_here\"\n"
        ),
        "README.md": (
            f"# {project_name.capitalize()}\n\n"
            "Your AI-Powered Personal Growth Agent.\n"
        ),
        "data/.gitkeep": "# This file ensures the 'data' directory is tracked by Git.",
        "agent/__init__.py": "# This makes the 'agent' directory a Python package.",
        "agent/core/__init__.py": "# This makes the 'core' directory a Python package.",
        "agent/crud/__init__.py": "# This makes the 'crud' directory a Python package.",
        "agent/models/__init__.py": "# This makes the 'models' directory a Python package.",
    }

    # --- Create the structure ---
    for path, is_directory in structure:
        try:
            if is_directory:
                os.makedirs(path, exist_ok=True)
                print(f"  ✅ Created directory: {path}")
            else:
                # Get the filename to check if we have content for it
                filename = os.path.basename(path)
                if filename in file_contents:
                    with open(path, "w") as f:
                        f.write(file_contents[filename])
                    print(f"  ✅ Created file with content: {path}")
                else:
                    open(path, "w").close() # Create an empty file
                    print(f"  ✅ Created empty file: {path}")
        except OSError as e:
            print(f"  ❌ Error creating {path}: {e}")

    print(f"\n🎉 Project structure for '{project_name}' is ready!")
    print("\nNext steps:")
    print(f"1. cd {project_name}")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  (or .\\venv\\Scripts\\activate on Windows)")
    print("4. pip install -r requirements.txt")
    print("5. cp .env.example .env")
    print("6. Add your API keys to the .env file")
    print("7. You are ready to code!")


if __name__ == "__main__":
    create_project_structure()
