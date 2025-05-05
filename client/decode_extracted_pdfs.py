"""
Decode extracted PDFs from JSON to actual PDF files.
"""

import json
import base64
import os
import argparse
from pathlib import Path


def decode_pdfs(json_file, output_dir=None):
    """
    Decode base64-encoded PDFs from JSON and save them to files.
    
    Args:
        json_file (str): Path to the JSON file containing base64-encoded PDFs
        output_dir (str, optional): Directory to save extracted PDFs to.
                                   If None, use current directory.
    
    Returns:
        int: Number of PDFs extracted
    """
    # Create output directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = "."
    
    # Load the JSON
    with open(json_file, 'r') as f:
        result = json.load(f)
    
    count = result.get('count', 0)
    files = result.get('files', {})
    
    # Write each extracted file
    for filename, content_b64 in files.items():
        # Clean the filename to ensure it's safe
        safe_filename = Path(filename).name
        output_path = os.path.join(output_dir, f"extracted_{safe_filename}")
        
        # Decode base64 content
        content = base64.b64decode(content_b64)
        
        # Write to file
        with open(output_path, 'wb') as f:
            f.write(content)
            print(f"Saved: {output_path}")
    
    print(f"Extracted {count} PDF files.")
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode base64-encoded PDFs from JSON")
    parser.add_argument("json_file", help="Path to the JSON file with base64-encoded PDFs")
    parser.add_argument("--output", "-o", help="Directory to save extracted PDFs")
    
    args = parser.parse_args()
    decode_pdfs(args.json_file, args.output)