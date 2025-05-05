"""
Service for PDF manipulation operations
"""
import io
import base64
import uuid
from typing import List, Dict, Tuple
from PyPDF2 import PdfReader, PdfWriter


def embed_pdfs(host_pdf: bytes, attachments: List[bytes]) -> bytes:
    """
    Embeds multiple PDF files into a host PDF document
    
    Args:
        host_pdf: Bytes of the host PDF file
        attachments: List of bytes for each attachment PDF file
    
    Returns:
        bytes: The host PDF with embedded files
    """
    # Create PDF reader and writer
    reader = PdfReader(io.BytesIO(host_pdf))
    writer = PdfWriter()
    
    # Copy all pages from the host PDF
    for page in reader.pages:
        writer.add_page(page)
    
    # Embed each attachment
    for idx, attachment in enumerate(attachments):
        # Generate a unique filename for each attachment
        filename = f"attachment_{idx + 1}.pdf"
        writer.add_attachment(filename, attachment)
    
    # Write the result to a BytesIO buffer
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    
    return output_buffer.getvalue()


def extract_pdfs(pdf_data: bytes) -> Tuple[int, Dict[str, str]]:
    """
    Extracts all embedded PDFs from a PDF document
    
    Args:
        pdf_data: Bytes of the PDF file
    
    Returns:
        Tuple containing:
          - int: Count of extracted files
          - Dict: Dictionary mapping filenames to base64-encoded PDF content
    """
    # Create PDF reader
    reader = PdfReader(io.BytesIO(pdf_data))
    extracted_files = {}
    
    try:
        # PyPDF2 >= 2.0.0 uses named_destinations property which is a dictionary
        attachments = []
        
        # Handle different PyPDF2 versions
        if hasattr(reader, 'attachments'):
            # Try the attachments property for newer versions
            for name, data in reader.attachments:
                attachments.append((name, data))
        elif hasattr(reader, '_objects'):
            # For PyPDF2 3.0+, use the trailer's Root/Names/EmbeddedFiles if available
            if hasattr(reader, 'trailer') and '/Root' in reader.trailer:
                root = reader.trailer['/Root']
                if '/Names' in root and '/EmbeddedFiles' in root['/Names']:
                    embedded_files = root['/Names']['/EmbeddedFiles']
                    if '/Names' in embedded_files:
                        names = embedded_files['/Names']
                        i = 0
                        while i < len(names):
                            if isinstance(names[i], str) and i + 1 < len(names):
                                name = names[i]
                                file_spec = names[i + 1]
                                if '/EF' in file_spec and '/F' in file_spec['/EF']:
                                    ef_stream = file_spec['/EF']['/F']
                                    if '/Filter' in ef_stream and ef_stream['/Filter'] == '/FlateDecode':
                                        stream_data = ef_stream.get_data()
                                        attachments.append((name, stream_data))
                            i += 2
        
        # If no attachments found with default methods, try the catalog
        if not attachments and hasattr(reader, 'trailer'):
            try:
                catalog = reader.trailer["/Root"]
                if "/Names" in catalog:
                    names = catalog["/Names"]
                    if "/EmbeddedFiles" in names:
                        files_dict = names["/EmbeddedFiles"]
                        if "/Names" in files_dict:
                            files = files_dict["/Names"]
                            i = 0
                            while i < len(files):
                                if i+1 < len(files):
                                    filename = files[i]
                                    filespec = files[i+1]
                                    if "/EF" in filespec:
                                        ef = filespec["/EF"]
                                        if "/F" in ef:
                                            stream = ef["/F"]
                                            data = stream.get_data()
                                            attachments.append((filename, data))
                                i += 2
            except Exception:
                pass
                
        # Process found attachments
        for filename, attachment_data in attachments:
            # If no filename was provided, generate a random one
            if not filename:
                filename = f"extracted_{uuid.uuid4()}.pdf"
            
            # Ensure the filename ends with .pdf
            if not filename.lower().endswith('.pdf'):
                filename = f"{filename}.pdf"
                
            # Encode the attachment as base64
            attachment_b64 = base64.b64encode(attachment_data).decode('utf-8')
            extracted_files[filename] = attachment_b64
    
    except Exception as e:
        # Last resort: try to use extract_attachment method for PyPDF2 v3.0+
        try:
            if hasattr(reader, 'attachment_names'):
                attachment_names = reader.attachment_names()
                for name in attachment_names:
                    attachment_data = reader.extract_attachment(name)
                    if attachment_data:
                        # Ensure the filename ends with .pdf
                        filename = name
                        if not filename.lower().endswith('.pdf'):
                            filename = f"{filename}.pdf"
                            
                        # Encode the attachment as base64
                        attachment_b64 = base64.b64encode(attachment_data).decode('utf-8')
                        extracted_files[filename] = attachment_b64
        except Exception as inner_e:
            raise Exception(f"Failed to extract attachments: {str(e)}. Inner error: {str(inner_e)}")
    
    return len(extracted_files), extracted_files