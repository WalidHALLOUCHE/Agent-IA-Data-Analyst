from setuptools import setup, find_packages

setup(
    name="sales-insight-ai-agents",
    version="0.1.0",
    description="Mini data analyst IA pour l'analyse de ventes e-commerce",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "streamlit",
        "pandas",
        "plotly",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pytest",
        "openpyxl",
        "openai",
    ],
)
