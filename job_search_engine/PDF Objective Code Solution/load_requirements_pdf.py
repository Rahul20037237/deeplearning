import pdfplumber
import os

# Load the requirements PDF from the filesystem
pdf_path = 'Fresher_Job_Search_Engine_Requirements.pdf'

if not os.path.exists(pdf_path):
    print(f"Error: File {pdf_path} not found in filesystem")
    available_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(f"Available files: {available_files}")
else:
    # Read and extract text from PDF using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        
        # Extract text from all pages
        requirements_text = ""
        for page in pdf.pages:
            requirements_text += page.extract_text() + "\n"
        
        print(f"Successfully loaded PDF with {num_pages} pages")
        print(f"Total text length: {len(requirements_text)} characters")
        print("\n" + "="*80)
        print("REQUIREMENTS DOCUMENT CONTENT:")
        print("="*80)
        print(requirements_text)
