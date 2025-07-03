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
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ LaTeX installation found")
            return True
        else:
            print("✗ LaTeX not found or not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("✗ LaTeX (pdflatex) not found in system PATH")
        return False

def convert_latex_to_pdf(tex_file_path, output_dir=None):
    """
    Convert LaTeX file to PDF using pdflatex.
    
    Args:
        tex_file_path (str): Path to the .tex file
        output_dir (str, optional): Output directory for PDF. Defaults to same as tex file.
    
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
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory', str(output_dir),
                str(tex_path.name)
            ], capture_output=True, text=True, timeout=60)
            
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
    if not check_latex_installation():
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
    success = convert_latex_to_pdf(tex_file, output_dir)
    
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