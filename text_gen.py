import os
import PyPDF2

def extract_text_from_pdfs(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDFs found in the directory.")
        return
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_directory, pdf_file)
        text_filename = os.path.splitext(pdf_file)[0] + ".txt"
        text_path = os.path.join(output_directory, text_filename)
        
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                
                with open(text_path, "w", encoding="utf-8") as text_file:
                    text_file.write(text)
                print(f"Extracted text saved to {text_path}")
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

def main():
    input_directory = "uscis_pdfs"
    output_directory = "uscis_texts"
    extract_text_from_pdfs(input_directory, output_directory)

if __name__ == "__main__":
    main()
