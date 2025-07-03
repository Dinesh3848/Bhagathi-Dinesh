#!/usr/bin/env python3
"""
LaTeX to PDF Converter for Resume
Multiple methods to convert LaTeX resume to PDF using Python
"""

import os
import subprocess
import sys
from pathlib import Path

def method1_pdflatex_subprocess():
    """
    Method 1: Using subprocess to call pdflatex directly
    Requires: pdflatex installed on system
    """
    print("🔄 Method 1: Using pdflatex subprocess...")
    
    tex_file = "assets/pdf/Yaswanth_Ampolu_Resume_Updated.tex"
    
    try:
        # Run pdflatex command
        result = subprocess.run([
            'pdflatex', 
            '-output-directory=assets/pdf',
            tex_file
        ], capture_output=True, text=True, check=True)
        
        print("✅ PDF generated successfully using pdflatex!")
        print(f"📄 Output: assets/pdf/Yaswanth_Ampolu_Resume_Updated.pdf")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error with pdflatex: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ pdflatex not found. Please install LaTeX distribution.")
        return False

def method2_pylatex():
    """
    Method 2: Using PyLaTeX library
    Install: pip install pylatex
    """
    print("🔄 Method 2: Using PyLaTeX library...")
    
    try:
        from pylatex import Document, Section, Subsection, Command
        from pylatex.utils import italic, NoEscape
        
        # Read the existing LaTeX file
        with open("assets/pdf/Yaswanth_Ampolu_Resume_Updated.tex", 'r') as f:
            latex_content = f.read()
        
        # Write to a new file and compile
        with open("temp_resume.tex", 'w') as f:
            f.write(latex_content)
        
        # Compile using pylatex
        os.system("pdflatex temp_resume.tex")
        
        # Move the generated PDF
        if os.path.exists("temp_resume.pdf"):
            os.rename("temp_resume.pdf", "assets/pdf/Yaswanth_Ampolu_Resume_Updated.pdf")
            print("✅ PDF generated successfully using PyLaTeX!")
            
            # Cleanup temporary files
            for ext in ['.tex', '.aux', '.log']:
                temp_file = f"temp_resume{ext}"
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            return True
        else:
            print("❌ Failed to generate PDF with PyLaTeX")
            return False
            
    except ImportError:
        print("❌ PyLaTeX not installed. Run: pip install pylatex")
        return False
    except Exception as e:
        print(f"❌ Error with PyLaTeX: {e}")
        return False

def method3_online_api():
    """
    Method 3: Using online LaTeX compilation API
    Install: pip install requests
    """
    print("🔄 Method 3: Using online LaTeX API...")
    
    try:
        import requests
        
        # Read LaTeX content
        with open("assets/pdf/Yaswanth_Ampolu_Resume_Updated.tex", 'r') as f:
            latex_content = f.read()
        
        # Using LaTeX.Online API (free service)
        url = "https://latex.ytotech.com/builds/sync"
        
        files = {
            'document.tex': latex_content
        }
        
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            # Save the PDF
            with open("assets/pdf/Yaswanth_Ampolu_Resume_Updated.pdf", 'wb') as f:
                f.write(response.content)
            print("✅ PDF generated successfully using online API!")
            return True
        else:
            print(f"❌ API request failed with status: {response.status_code}")
            return False
            
    except ImportError:
        print("❌ requests library not installed. Run: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Error with online API: {e}")
        return False

def method4_docker_latex():
    """
    Method 4: Using Docker LaTeX container
    Requires: Docker installed
    """
    print("🔄 Method 4: Using Docker LaTeX container...")
    
    try:
        # Create a simple script to run LaTeX in Docker
        docker_command = [
            'docker', 'run', '--rm',
            '-v', f'{os.getcwd()}:/workspace',
            'texlive/texlive:latest',
            'pdflatex', '-output-directory=/workspace/assets/pdf',
            '/workspace/assets/pdf/Yaswanth_Ampolu_Resume_Updated.tex'
        ]
        
        result = subprocess.run(docker_command, capture_output=True, text=True, check=True)
        print("✅ PDF generated successfully using Docker!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker command failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker.")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    
    packages = ["pylatex", "requests"]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def main():
    """Main function to try different conversion methods"""
    print("🚀 LaTeX to PDF Converter for Resume")
    print("=" * 50)
    
    # Create output directory if it doesn't exist
    Path("assets/pdf").mkdir(parents=True, exist_ok=True)
    
    # Check if LaTeX file exists
    if not os.path.exists("assets/pdf/Yaswanth_Ampolu_Resume_Updated.tex"):
        print("❌ LaTeX file not found!")
        return
    
    print("\nChoose conversion method:")
    print("1. pdflatex (requires LaTeX installation)")
    print("2. PyLaTeX (requires: pip install pylatex)")
    print("3. Online API (requires: pip install requests)")
    print("4. Docker LaTeX (requires Docker)")
    print("5. Install Python dependencies")
    print("6. Try all methods")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        method1_pdflatex_subprocess()
    elif choice == "2":
        method2_pylatex()
    elif choice == "3":
        method3_online_api()
    elif choice == "4":
        method4_docker_latex()
    elif choice == "5":
        install_dependencies()
    elif choice == "6":
        # Try all methods until one succeeds
        methods = [
            method3_online_api,  # Try online first (no installation needed)
            method1_pdflatex_subprocess,
            method2_pylatex,
            method4_docker_latex
        ]
        
        for method in methods:
            if method():
                break
            print("Trying next method...\n")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main() 