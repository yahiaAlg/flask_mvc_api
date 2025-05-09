import json
import base64
import pikepdf
import os
from io import BytesIO

def extract_attachments_from_json(json_file_path, output_dir=None):
    """
    Extract and save PDF attachments from a JSON file containing base64-encoded PDFs.
    
    Args:
        json_file_path (str): Path to the JSON file with encoded PDFs
        output_dir (str, optional): Directory to save extracted PDFs. Defaults to current directory.
    
    Returns:
        list: Paths to the extracted PDF files
    """
    # Create output directory if specified and doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    extracted_files = []
    
    # Check if the JSON has the expected structure
    if 'count' in data and 'files' in data:
        print(f"Found {data['count']} embedded PDF files")
        
        # Process each embedded file
        for filename, base64_content in data['files'].items():
            # Decode base64 content
            pdf_bytes = base64.b64decode(base64_content)
            
            # Determine output path
            output_path = os.path.join(output_dir, filename) if output_dir else filename
            
            # Save decoded PDF
            with open(output_path, 'wb') as pdf_file:
                pdf_file.write(pdf_bytes)
            
            print(f"Extracted: {output_path}")
            extracted_files.append(output_path)
    else:
        print("Invalid JSON format: Expected 'count' and 'files' fields")
    
    return extracted_files

def extract_attachments_from_pdf(pdf_path, output_dir=None):
    """
    Extract embedded files directly from a PDF using pikepdf.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str, optional): Directory to save extracted files. Defaults to current directory.
    
    Returns:
        list: Paths to the extracted files
    """
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    extracted_files = []
    
    try:
        # Open the PDF
        with pikepdf.Pdf.open(pdf_path) as pdf:
            # Check if the PDF has embedded files
            if '/Names' in pdf.Root and '/EmbeddedFiles' in pdf.Root.Names:
                name_dict = pdf.Root.Names.EmbeddedFiles.Names
                
                # Process name dictionary for embedded files (pairs of name and reference)
                for i in range(0, len(name_dict), 2):
                    filename = str(name_dict[i])
                    filespec = name_dict[i+1]
                    
                    # Get the embedded file stream
                    embedded_file = filespec.EF.F
                    
                    # Save the extracted file
                    output_path = os.path.join(output_dir, filename) if output_dir else filename
                    
                    with open(output_path, 'wb') as f:
                        f.write(embedded_file.read_bytes())
                    
                    print(f"Extracted: {output_path}")
                    extracted_files.append(output_path)
                
                print(f"Found and extracted {len(extracted_files)} embedded files")
            else:
                print("No embedded files found in the PDF")
    
    except Exception as e:
        print(f"Error extracting files: {str(e)}")
    
    return extracted_files

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract PDF attachments from JSON or PDF file")
    parser.add_argument("input_file", help="Path to input JSON or PDF file")
    parser.add_argument("--output-dir", help="Directory to save extracted files")
    parser.add_argument("--type", choices=["json", "pdf"], 
                        help="Input file type (auto-detected by extension if not specified)")
    
    args = parser.parse_args()
    
    # Determine file type if not specified
    if not args.type:
        if args.input_file.lower().endswith('.json'):
            args.type = "json"
        elif args.input_file.lower().endswith('.pdf'):
            args.type = "pdf"
        else:
            parser.error("Could not determine file type. Please specify --type")
    
    # Process the file
    if args.type == "json":
        extract_attachments_from_json(args.input_file, args.output_dir)
    else:
        extract_attachments_from_pdf(args.input_file, args.output_dir)