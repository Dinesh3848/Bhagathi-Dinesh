#!/usr/bin/env python3
"""
LaTeX to PDF Converter for Dinesh Kumar Bagathi's Resume
This script converts the LaTeX resume file to a professional PDF document.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_latex_installation():
    """Check if LaTeX is installed on the system."""
    # Common MiKTeX installation paths
    miktex_paths = [
        r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
        r"C:\Program Files (x86)\MiKTeX\miktex\bin\pdflatex.exe",
        r"C:\Users\{}\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe".format(os.getenv('USERNAME', '')),
        "pdflatex"  # Try system PATH as fallback
    ]
    
    for pdflatex_path in miktex_paths:
        try:
            result = subprocess.run([pdflatex_path, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✓ LaTeX installation found at: {pdflatex_path}")
                return pdflatex_path
            else:
                continue
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    print("✗ LaTeX (pdflatex) not found in system PATH or common installation locations")
    return None

def convert_latex_to_pdf(tex_file_path, output_dir=None, pdflatex_path='pdflatex'):
    """
    Convert LaTeX file to PDF using pdflatex.
    
    Args:
        tex_file_path (str): Path to the .tex file
        output_dir (str, optional): Output directory for PDF. Defaults to same as tex file.
        pdflatex_path (str): Path to pdflatex executable
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    tex_path = Path(tex_file_path)
    
    if not tex_path.exists():
        print(f"✗ LaTeX file not found: {tex_file_path}")
        return False
    
    if not tex_path.suffix.lower() == '.tex':
        print(f"✗ File must have .tex extension: {tex_file_path}")
        return False
    
    # Set output directory
    if output_dir is None:
        output_dir = tex_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 Converting: {tex_path.name}")
    print(f"📁 Output directory: {output_dir}")
    
    try:
        # Change to the directory containing the tex file
        original_cwd = os.getcwd()
        os.chdir(tex_path.parent)
        
        # Run pdflatex twice for proper cross-references and formatting
        for run_number in [1, 2]:
            print(f"🔄 Running pdflatex (pass {run_number}/2)...")
            
            result = subprocess.run([
                pdflatex_path,
                '-interaction=nonstopmode',
                '-output-directory', str(output_dir),
                str(tex_path.name)
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                print(f"✗ pdflatex failed on pass {run_number}")
                print("Error output:")
                print(result.stdout)
                print(result.stderr)
                return False
        
        # Check if PDF was created
        pdf_path = output_dir / f"{tex_path.stem}.pdf"
        if pdf_path.exists():
            print(f"✅ PDF created successfully: {pdf_path}")
            
            # Clean up auxiliary files
            cleanup_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls', '.synctex.gz']
            for ext in cleanup_extensions:
                aux_file = output_dir / f"{tex_path.stem}{ext}"
                if aux_file.exists():
                    aux_file.unlink()
                    print(f"🧹 Cleaned up: {aux_file.name}")
            
            return True
        else:
            print(f"✗ PDF file was not created: {pdf_path}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ LaTeX compilation timed out")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during conversion: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir(original_cwd)

def main():
    """Main function to handle command line arguments and execute conversion."""
    print("🚀 Dinesh Kumar Bagathi Resume PDF Converter")
    print("=" * 50)
    
    # Check LaTeX installation
    pdflatex_path = check_latex_installation()
    if not pdflatex_path:
        print("\n💡 To install LaTeX:")
        print("   • Windows: Install MiKTeX or TeX Live")
        print("   • macOS: Install MacTeX")
        print("   • Linux: sudo apt-get install texlive-full (Ubuntu/Debian)")
        print("           sudo yum install texlive-scheme-full (CentOS/RHEL)")
        sys.exit(1)
    
    # Define file paths
    tex_file = "assets/pdf/Dinesh_Kumar_Bagathi_Resume.tex"
    output_dir = "assets/pdf/"
    
    # Check if tex file exists
    if not os.path.exists(tex_file):
        print(f"✗ LaTeX file not found: {tex_file}")
        print("Please ensure the file exists before running this script.")
        sys.exit(1)
    
    print(f"\n📋 Input file: {tex_file}")
    print(f"📁 Output directory: {output_dir}")
    
    # Convert to PDF
    success = convert_latex_to_pdf(tex_file, output_dir, pdflatex_path)
    
    if success:
        print("\n🎉 Resume PDF generated successfully!")
        print(f"📄 Location: {output_dir}Dinesh_Kumar_Bagathi_Resume.pdf")
        print("\n💼 Your AI-focused resume is ready for job applications!")
    else:
        print("\n❌ Failed to generate PDF")
        print("Please check the LaTeX file for syntax errors.")
        sys.exit(1)

if __name__ == "__main__":
    main() 