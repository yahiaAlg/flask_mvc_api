import os
import sys
import pikepdf

def extract_attachments_from_pdf(input_pdf_path, output_directory):
    """
    Extract all PDF attachments from a PDF file using pikepdf.
    
    Args:
        input_pdf_path (str): Path to the PDF file containing attachments
        output_directory (str): Directory where the extracted files will be saved
    
    Returns:
        list: List of extracted file paths
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            print(f"Created output directory: {output_directory}")
        
        # Read the PDF file
        print(f"Reading PDF: {input_pdf_path}")
        pdf = pikepdf.open(input_pdf_path)
        
        extracted_files = []
        
        # Check if PDF has attachments in the Names tree
        if '/Names' in pdf.Root and '/EmbeddedFiles' in pdf.Root.Names:
            names_array = pdf.Root.Names.EmbeddedFiles.Names
            
            # Process the names array (alternating name, filespec)
            for i in range(0, len(names_array), 2):
                if i+1 >= len(names_array):
                    break
                    
                filename = str(names_array[i])
                filespec = names_array[i+1]
                
                # Extract the embedded file stream if it exists
                if filespec.get('/EF') and filespec.EF.get('/F'):
                    print(f"Extracting: {filename}")
                    
                    output_path = os.path.join(output_directory, filename)
                    
                    # Get the file data
                    file_data = bytes(filespec.EF.F.read_bytes())
                    
                    # Write the attachment to a file
                    with open(output_path, 'wb') as output_file:
                        output_file.write(file_data)
                    
                    extracted_files.append(output_path)
                    print(f"Saved to: {output_path}")
        
        if not extracted_files:
            print("No attachments found in the PDF.")
        else:
            print(f"Successfully extracted {len(extracted_files)} attachments")
        
        return extracted_files
    
    except Exception as e:
        print(f"Error extracting attachments: {e}")
        return []

def main():
    """Command line interface for the PDF attachment extraction tool."""
    if len(sys.argv) != 3:
        print("Usage: python pikepdf_extract.py input.pdf output_directory")
        sys.exit(1)
    
    input_pdf_path = sys.argv[1]
    output_directory = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(input_pdf_path):
        print(f"Error: Input PDF '{input_pdf_path}' not found.")
        sys.exit(1)
    
    # Extract attachments
    extracted_files = extract_attachments_from_pdf(input_pdf_path, output_directory)
    
    if not extracted_files:
        print("No attachments were extracted.")
        sys.exit(1)
    else:
        print(f"Extracted {len(extracted_files)} files:")
        for file_path in extracted_files:
            print(f"  - {file_path}")
            
    print("\nNote: You'll need to install pikepdf to use this script:")
    print("  pip install pikepdf")

if __name__ == "__main__":
    main()