#!/usr/bin/env python3
"""
ATS-Optimized LaTeX to PDF Converter
Quick conversion using online API with ATS best practices
"""

import requests
import os
import sys

def convert_latex_to_pdf():
    """Convert ATS-optimized LaTeX resume to PDF using online API"""
    
    # Use the final single-page ATS-optimized LaTeX file
    latex_file = "assets/pdf/Yaswanth_Ampolu_Resume_Final.tex"
    if not os.path.exists(latex_file):
        print("❌ ATS-optimized LaTeX file not found!")
        return False
    
    print("🎯 Converting ATS-Optimized LaTeX to PDF...")
    
    try:
        # Read LaTeX content
        with open(latex_file, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        # Use online LaTeX compilation service
        url = "https://latex.ytotech.com/builds/sync"
        
        files = {
            'document.tex': latex_content
        }
        
        # Make request with timeout
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code in [200, 201]:
            # Save PDF with final naming
            pdf_path = "assets/pdf/Yaswanth_Ampolu_Resume_Final.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            
            print("✅ ATS-Optimized PDF generated successfully!")
            print(f"📄 Output: {pdf_path}")
            print(f"📏 File size: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_pdf_pages():
    """Check if PDF has multiple pages"""
    try:
        import PyPDF2
        pdf_path = "assets/pdf/Yaswanth_Ampolu_Resume_Final.pdf"
        
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = len(reader.pages)
                print(f"📄 PDF has {pages} page(s)")
                
                if pages > 1:
                    print("⚠️  Resume spans multiple pages - consider further compacting")
                else:
                    print("✅ Resume fits on single page - ATS Friendly!")
        
    except ImportError:
        print("💡 Install PyPDF2 to check page count: pip install PyPDF2")
    except Exception as e:
        print(f"❌ Error checking PDF: {e}")

if __name__ == "__main__":
    print("🎯 ATS-Optimized LaTeX to PDF Converter")
    print("=" * 50)
    
    # Auto-install requests if needed
    try:
        import requests
    except ImportError:
        print("📦 Installing requests...")
        os.system("pip install requests")
        import requests
    
    # Convert the LaTeX file
    success = convert_latex_to_pdf()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 ATS-Optimized Resume Ready!")
        
        # Check page count
        check_pdf_pages()
        
        print("\n✅ ATS Optimization Features Applied:")
        print("   • Single-column layout (ATS parsable)")
        print("   • Professional summary with keywords")
        print("   • 15+ technical skills clearly listed")
        print("   • Quantified achievements with metrics")
        print("   • Job titles explicitly stated")
        print("   • Action verbs and industry keywords")
        print("   • Clean formatting without fancy elements")
        
        print("\n💼 Ready for Job Applications!")
        
    else:
        print("\n❌ Conversion failed!")
        print("💡 Try alternative methods:")
        print("   • python convert_resume_to_pdf.py")
        print("   • Online LaTeX editors (Overleaf)")
        print("   • Local LaTeX installation") 