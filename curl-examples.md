# API Usage Examples with cURL

This document provides examples of how to use the PDF Embed/Extract API using cURL commands.

## Embedding PDFs

This command embeds multiple PDFs into a host PDF:

```bash
curl -X POST http://localhost:5000/api/pdf/create_embedded_pdf \
  -F "host_pdf=@/path/to/host.pdf" \
  -F "attachments[]=@/path/to/attachment1.pdf" \
  -F "attachments[]=@/path/to/attachment2.pdf" \
  -o embedded_result.pdf
```

```bash
curl -X POST https://c81e-34-55-120-169.ngrok-free.app/api/pdf/create_embedded_pdf \
  -F "host_pdf=@./docs/django_dynamic_listings_and_detail_views.pdf" \
  -F "attachments[]=@./docs/django_templates__a_comprehensive_tutorial_on_inheritance_and_inclusion.pdf" \
  -o embedded_result.pdf
```

### Parameters:

- `host_pdf`: The main PDF that will contain the embedded files
- `attachments[]`: One or more PDF files to embed (can specify multiple)
- `-o embedded_result.pdf`: Saves the output to a file named "embedded_result.pdf"

## Extracting PDFs

This command extracts all embedded PDFs from a document:

```bash
curl -X POST http://localhost:5000/api/pdf/extract_embedded_pdf \
  -F "pdf=@/path/to/document_with_embedded_files.pdf" \
  -o extracted_files.json
```

### Parameters:

- `pdf`: A PDF file which may contain embedded PDFs
- `-o extracted_files.json`: Saves the JSON response to a file

### Response Format:

The extract endpoint returns a JSON response with the following structure:

```json
{
  "count": 2,
  "files": {
    "attachment_1.pdf": "base64_encoded_pdf_content...",
    "attachment_2.pdf": "base64_encoded_pdf_content..."
  }
}
```

## Saving Extracted PDFs

You can use a simple script to save the extracted PDFs from the JSON response:

```bash
# Extract the PDFs
curl -X POST http://localhost:5000/api/pdf/extract_embedded_pdf \
  -F "pdf=@document_with_embedded_files.pdf" \
  -o extracted_files.json

# Parse and save the PDFs using jq and base64
cat extracted_files.json | jq -r '.files | to_entries[] | "\(.key) \(.value)"' | \
  while read -r filename content; do
    echo "$content" | base64 -d > "$filename"
    echo "Saved $filename"
  done
```

```bash
# Extract the PDFs
curl -X POST https://c81e-34-55-120-169.ngrok-free.app/api/pdf/extract_embedded_pdf \
  -F "pdf=@./embedded_result.pdf" \
  -o extracted_files.json

# Parse and save the PDFs using jq and base64
cat extracted_files.json | jq -r '.files | to_entries[] | "\(.key) \(.value)"' | \
  while read -r filename content; do
    echo "$content" | base64 -d > "$filename"
    echo "Saved $filename"
  done
```

This requires [jq](https://stedolan.github.io/jq/) to be installed.

## Additional Options

### Using with HTTP Basic Authentication (if configured)

```bash
curl -X POST http://localhost:5000/api/pdf/create_embedded_pdf \
  -u username:password \
  -F "host_pdf=@/path/to/host.pdf" \
  -F "attachments[]=@/path/to/attachment1.pdf" \
  -o embedded_result.pdf
```

### Adding Custom Headers

```bash
curl -X POST http://localhost:5000/api/pdf/extract_embedded_pdf \
  -H "X-Custom-Header: Value" \
  -F "pdf=@/path/to/document_with_embedded_files.pdf"
```

### Verbose Output for Debugging

Add the `-v` flag to see detailed request and response information:

```bash
curl -v -X POST http://localhost:5000/api/pdf/create_embedded_pdf \
  -F "host_pdf=@/path/to/host.pdf" \
  -F "attachments[]=@/path/to/attachment1.pdf" \
  -o embedded_result.pdf
```
