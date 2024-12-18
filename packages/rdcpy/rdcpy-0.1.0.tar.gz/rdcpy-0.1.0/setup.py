from pathlib import Path
from setuptools import setup, find_packages

# Define the directory containing the package
package_dir = Path(r"W:\_PRJ\_prj__wrk_ndc\_packages\rdcpy")

# Load the long description from the README file if it exists
readme_path = package_dir / "README.md"
long_description = (
    readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
)

# Call setup function
setup(
    author="Владимирова Алина Валерьевна",
    author_email="alina.v.vladimirova@gmail.com",
    description="Пакет для работы на платформе НЦСЭД.",
    name="rdcpy",
    long_description=long_description,  # Use the README file content
    long_description_content_type="text/markdown",  # Specify the README format
    packages=find_packages(include=["rdcpy","rdcpy.*"]),
    version="0.1.0",
    install_requires=['numpy','pandas','re','IPython'], 
    python_requires='>=2.7'
)