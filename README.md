# Flask-MVC PDF Embed/Extract API

A Flask-based RESTful API for embedding and extracting PDF files, following the MVC pattern.

## Project Structure

```
/flask-pdf-embed-extract/
├── app/
│   ├── __init__.py                 # App factory
│   ├── config.py                   # Configuration settings
│   ├── controllers/
│   │   ├── __init__.py             # Empty file to make directory a package
│   │   ├── pdf_controller.py       # API endpoints for PDF operations
│   │   └── ui_controller.py        # UI routes
│   ├── services/
│   │   ├── __init__.py             # Empty file to make directory a package
│   │   └── pdf_service.py          # PDF processing logic
│   └── templates/
│       └── pdf_embed_extract.html  # UI template for Flask
├── tests/
│   ├── __init__.py                 # Empty file to make directory a package
│   ├── conftest.py                 # Pytest configuration
│   ├── test_api.py                 # API integration tests
│   └── test_pdf_service.py         # Service unit tests
├── run.py                          # Application entry point
├── requirements.txt                # Dependencies
└── README.md                       # Project documentation
```

## Features

- Embed multiple PDFs inside a host PDF document
- Extract all embedded PDFs from a document
- In-memory PDF processing (no filesystem I/O)
- Interactive Swagger UI documentation
- Clean MVC architecture
- Simple web UI for manual testing

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/flask-pdf-embed-extract.git
   cd flask-pdf-embed-extract
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the application

```
python run.py
```

The application will start on http://localhost:5000

### API Documentation

Access the Swagger UI at: http://localhost:5000/apidocs/

### Web Interface

A simple web interface is available at the root URL (http://localhost:5000/). This interface allows you to:

- Embed PDFs into a host document
- Extract PDFs from a document with embedded files
- View API documentation

### API Endpoints

1. **Create Embedded PDF**

   - URL: `/api/pdf/create_embedded_pdf`
   - Method: `POST`
   - Input:
     - `host_pdf`: The host PDF file
     - `attachments[]`: One or more PDF files to embed (can be multiple)
   - Output: Binary PDF with embedded attachments

2. **Extract Embedded PDFs**
   - URL: `/api/pdf/extract_embedded_pdf`
   - Method: `POST`
   - Input:
     - `pdf`: A PDF file which may contain embedded files
   - Output: JSON with count and base64-encoded embedded PDFs

## Example Usage with cURL

### Embedding PDFs

```bash
curl -X POST \
  http://localhost:5000/api/pdf/create_embedded_pdf \
  -H "Content-Type: multipart/form-data" \
  -F "host_pdf=@/path/to/host.pdf" \
  -F "attachments[]=@/path/to/attachment1.pdf" \
  -F "attachments[]=@/path/to/attachment2.pdf" \
  --output embedded_result.pdf
```

### Extracting PDFs

```bash
curl -X POST \
  http://localhost:5000/api/pdf/extract_embedded_pdf \
  -H "Content-Type: multipart/form-data" \
  -F "pdf=@/path/to/embedded_result.pdf" \
  --output extracted_result.json
```

## Architecture

This project follows the Model-View-Controller (MVC) pattern:

- **Models**: Placeholder for future extension
- **Views/Controllers**: Routes and request/response handling in `app/controllers/`
- **Services**: PDF manipulation logic in `app/services/`

## Testing

Run the tests with pytest:

```
pytest
```

The tests cover both unit testing of the PDF service functionality and integration testing of the API endpoints.

## Key Design Decisions

1. **In-Memory Processing**: All PDF operations are performed in memory using io.BytesIO to avoid filesystem I/O.
2. **MVC Architecture**: Clear separation of concerns between controllers (routing), services (business logic), and templates.
3. **API Documentation**: Auto-generated Swagger UI for easy API exploration and testing.
4. **Web Interface**: Simple HTML/JS frontend for manual testing without requiring external tools.
5. **Comprehensive Testing**: Both unit tests for the PDF service and integration tests for the API endpoints.

## License

This project is licensed under the MIT License.

## colab link

https://colab.research.google.com/drive/12kg_44SliZlVjN8DLf4kpYRItPyUpljI?usp=sharing
