"""
Service for PDF manipulation operations
"""
import io
import base64
import uuid
import logging
import os
import tempfile
from typing import List, Dict, Tuple
import pikepdf

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def embed_pdfs(host_pdf: bytes, attachments: List[bytes]) -> bytes:
    """
    Embeds multiple PDF files into a host PDF document using pikepdf
    
    Args:
        host_pdf: Bytes of the host PDF file
        attachments: List of bytes for each attachment PDF file
    
    Returns:
        bytes: The host PDF with embedded files
    """
    host_pdf_path = None
    attachment_paths = []
    output_path = None
    
    try:
        # Create temporary files but close them immediately after writing
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as host_temp:
            host_temp.write(host_pdf)
            host_pdf_path = host_temp.name
        
        for idx, attachment in enumerate(attachments):
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as attachment_temp:
                attachment_temp.write(attachment)
                attachment_paths.append(attachment_temp.name)
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as output_temp:
            output_path = output_temp.name
        
        logger.info(f"Embedding {len(attachments)} attachments")
        
        # Open the host PDF
        logger.info(f"Reading host PDF: {host_pdf_path}")
        with pikepdf.open(host_pdf_path) as pdf:
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
            for i, attachment_path in enumerate(attachment_paths):
                logger.info(f"Attaching: {attachment_path}")
                
                # Generate a unique filename
                filename = f"attachment_{i+1}_{uuid.uuid4().hex[:8]}.pdf"
                
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
                
                logger.info(f"  - Added attachment {i+1}: {filename}")
            
            # Write the output file
            logger.info(f"Writing output to: {output_path}")
            pdf.save(output_path)
        
        # Read the output file
        with open(output_path, 'rb') as f:
            result = f.read()
        
        logger.info("PDF with attachments created successfully!")
        return result
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise Exception(f"Failed to create embedded PDF: {str(e)}")
    finally:
        # Clean up temporary files
        if host_pdf_path and os.path.exists(host_pdf_path):
            try:
                os.unlink(host_pdf_path)
            except Exception as e:
                logger.warning(f"Could not delete temporary file {host_pdf_path}: {str(e)}")
                
        for path in attachment_paths:
            if os.path.exists(path):
                try:
                    os.unlink(path)
                except Exception as e:
                    logger.warning(f"Could not delete temporary file {path}: {str(e)}")
                    
        if output_path and os.path.exists(output_path):
            try:
                os.unlink(output_path)
            except Exception as e:
                logger.warning(f"Could not delete temporary file {output_path}: {str(e)}")

def extract_pdfs(pdf_data: bytes) -> Tuple[int, Dict[str, str]]:
    """
    Extracts all embedded PDFs from a PDF document using pikepdf
    
    Args:
        pdf_data: Bytes of the PDF file
    
    Returns:
        Tuple containing:
          - int: Count of extracted files
          - Dict: Dictionary mapping filenames to base64-encoded PDF content
    """
    input_pdf_path = None
    temp_dir = None
    
    try:
        # Create a temporary file for the input PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as input_temp:
            input_temp.write(pdf_data)
            input_pdf_path = input_temp.name
        
        logger.info("Starting PDF extraction")
        
        # Create temporary directory for extracted files
        temp_dir = tempfile.mkdtemp()
        
        # Read the PDF file
        logger.info(f"Reading PDF: {input_pdf_path}")
        extracted_files = {}
        
        with pikepdf.open(input_pdf_path) as pdf:
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
                        logger.info(f"Extracting: {filename}")
                        
                        # Get the file data
                        file_data = bytes(filespec.EF.F.read_bytes())
                        
                        # Encode as base64
                        file_b64 = base64.b64encode(file_data).decode('utf-8')
                        
                        # Store in the result dictionary
                        extracted_files[filename] = file_b64
                        logger.info(f"Extracted: {filename}")
        
        if not extracted_files:
            logger.info("No attachments found in the PDF.")
        else:
            logger.info(f"Successfully extracted {len(extracted_files)} attachments")
        
        return len(extracted_files), extracted_files
    
    except Exception as e:
        logger.error(f"Error extracting attachments: {str(e)}")
        raise Exception(f"Failed to extract attachments: {str(e)}")
    finally:
        # Clean up temporary files
        if input_pdf_path and os.path.exists(input_pdf_path):
            try:
                os.unlink(input_pdf_path)
            except Exception as e:
                logger.warning(f"Could not delete temporary file {input_pdf_path}: {str(e)}")
                
        if temp_dir and os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except Exception as e:
                logger.warning(f"Could not delete temporary directory {temp_dir}: {str(e)}")
    
    