"""
Controller for PDF API endpoints
"""
from flask import Blueprint, request, jsonify, send_file, Response
import io
from app.services.pdf_service import embed_pdfs, extract_pdfs

# Create blueprint
pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')


@pdf_bp.route('/create_embedded_pdf', methods=['POST'])
def create_embedded_pdf():
    """
    Embeds multiple PDFs inside a host PDF
    ---
    tags:
      - PDF Operations
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: host_pdf
        type: file
        required: true
        description: The host PDF file
      - in: formData
        name: attachments[]
        type: array
        items:
          type: file
        required: true
        description: One or more PDF files to embed
    responses:
      200:
        description: PDF with embedded files
        content:
          application/pdf:
            schema:
              type: string
              format: binary
      400:
        description: Bad request, missing files or invalid PDF
        schema:
          type: object
          properties:
            error:
              type: string
    """
    # Check if host_pdf is in the request
    if 'host_pdf' not in request.files:
        return jsonify({'error': 'No host PDF provided'}), 400
    
    # Get the host PDF file
    host_pdf = request.files['host_pdf']
    host_pdf_bytes = host_pdf.read()
    
    # Check if attachments are in the request
    attachments = request.files.getlist('attachments[]')
    if not attachments:
        return jsonify({'error': 'No attachment PDFs provided'}), 400
    
    # Read all attachments
    attachment_bytes = [attachment.read() for attachment in attachments]
    
    try:
        # Call the service to embed PDFs
        result_bytes = embed_pdfs(host_pdf_bytes, attachment_bytes)
        
        # Return the result as a downloadable file
        return send_file(
            io.BytesIO(result_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='embedded_result.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@pdf_bp.route('/extract_embedded_pdf', methods=['POST'])
def extract_embedded_pdf():
    """
    Extracts all embedded PDFs from a document
    ---
    tags:
      - PDF Operations
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: pdf
        type: file
        required: true
        description: A PDF file potentially containing embedded files
    responses:
      200:
        description: Successfully extracted PDFs
        schema:
          type: object
          properties:
            count:
              type: integer
              description: Number of extracted PDFs
            files:
              type: object
              additionalProperties:
                type: string
                format: byte
                description: Base64-encoded PDF content
      400:
        description: Bad request, missing file or invalid PDF
        schema:
          type: object
          properties:
            error:
              type: string
    """
    # Check if pdf is in the request
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    # Get the PDF file
    pdf_file = request.files['pdf']
    pdf_bytes = pdf_file.read()
    
    try:
        # Call the service to extract PDFs
        count, extracted_files = extract_pdfs(pdf_bytes)
        
        # Return the result as JSON
        return jsonify({
            'count': count,
            'files': extracted_files
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400