import os
import sys
import pikepdf

def attach_pdfs_to_host(host_pdf_path, attachment_pdf_paths, output_path):
    """
    Attach multiple PDFs to a host PDF document using pikepdf.
    
    Args:
        host_pdf_path (str): Path to the host PDF file
        attachment_pdf_paths (list): List of paths to PDF files to attach
        output_path (str): Path where the resulting PDF will be saved
    """
    try:
        # Open the host PDF
        print(f"Reading host PDF: {host_pdf_path}")
        pdf = pikepdf.open(host_pdf_path)
        
        # Get or create the embedded files name tree
        names = pdf.Root.get('/Names', pikepdf.Dictionary())
        if '/Names' not in pdf.Root:
            pdf.Root.Names = names
            
        ef_tree = names.get('/EmbeddedFiles', pikepdf.Dictionary())
        if '/EmbeddedFiles' not in names:
            names.EmbeddedFiles = ef_tree
            
        if '/Names' not in ef_tree:
            ef_tree.Names = pikepdf.Array()
        
        # Process each attachment
        for i, attachment_path in enumerate(attachment_pdf_paths):
            print(f"Attaching: {attachment_path}")
            
            # Use basename as filename
            filename = os.path.basename(attachment_path)
            
            # Read attachment file as binary
            with open(attachment_path, 'rb') as attachment_file:
                attachment_data = attachment_file.read()
            
            # Create file specification dictionary
            filespec = pikepdf.Dictionary(
                Type=pikepdf.Name.Filespec,
                F=filename,
                UF=filename,
                EF=pikepdf.Dictionary(
                    F=pdf.make_stream(attachment_data)
                )
            )
            
            # Add to the EmbeddedFiles name tree
            ef_tree.Names.append(pikepdf.String(filename))
            ef_tree.Names.append(filespec)
            
            print(f"  - Added attachment {i+1}: {filename}")
        
        # Write the output file
        print(f"Writing output to: {output_path}")
        pdf.save(output_path)
        
        print("PDF with attachments created successfully!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Command line interface for the PDF attachment tool."""
    if len(sys.argv) < 4:
        print("Usage: python pikepdf_attachment.py host_pdf.pdf output.pdf attachment1.pdf [attachment2.pdf] [...]")
        sys.exit(1)
    
    host_pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    attachment_pdf_paths = sys.argv[3:]
    
    # Check if files exist
    if not os.path.exists(host_pdf_path):
        print(f"Error: Host PDF '{host_pdf_path}' not found.")
        sys.exit(1)
    
    for attachment_path in attachment_pdf_paths:
        if not os.path.exists(attachment_path):
            print(f"Error: Attachment PDF '{attachment_path}' not found.")
            sys.exit(1)
    
    # Attach PDFs
    success = attach_pdfs_to_host(host_pdf_path, attachment_pdf_paths, output_path)
    
    if not success:
        sys.exit(1)
    
    print("\nNote: You'll need to install pikepdf to use this script:")
    print("  pip install pikepdf")

if __name__ == "__main__":
    main()