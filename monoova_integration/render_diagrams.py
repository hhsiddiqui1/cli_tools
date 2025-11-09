import glob
import os
import requests
from plantuml import PlantUML

# --- Configuration ---
DOCS_DIR = "docs"
# Try HTTPS and different URL formats
PLANTUML_SERVER_URL = "https://www.plantuml.com/plantuml"
PLANTUML_PNG_URL = "https://www.plantuml.com/plantuml/png"

def render_plantuml_diagrams():
    """
    Finds all .plantuml files in the specified directory and renders them
    as PNG images in the same location.
    """
    # Initialize the PlantUML client
    # Try using HTTPS URL
    pl = PlantUML(url=PLANTUML_SERVER_URL)

    # Find all .plantuml files in the docs directory
    search_path = os.path.join(DOCS_DIR, "*.plantuml")
    plantuml_files = glob.glob(search_path)

    if not plantuml_files:
        print(f"No .plantuml files found in '{DOCS_DIR}/'.")
        return

    print(f"Found {len(plantuml_files)} diagram(s) to render...")

    for file_path in plantuml_files:
        print(f"Rendering '{file_path}'...")
        try:
            # Read the PlantUML source
            with open(file_path, 'r', encoding='utf-8') as f:
                plantuml_content = f.read()
            
            # Determine output file path
            base_name = os.path.splitext(file_path)[0]
            output_file = f"{base_name}.png"
            
            # Remove existing file to ensure fresh render
            if os.path.exists(output_file):
                os.remove(output_file)
            
            # Use get_url to get the encoded URL and convert to PNG format
            try:
                encoded_url = pl.get_url(plantuml_content)
                # Convert the URL to PNG format
                # The get_url can return different formats:
                # - https://www.plantuml.com/plantumll{encoded_string} (text format, double l)
                # - https://www.plantuml.com/plantuml{encoded_string} (text format, single l)
                # We need: https://www.plantuml.com/plantuml/png/{encoded_string}
                if encoded_url.startswith('http'):
                    encoded_part = None
                    if '/plantumll' in encoded_url:
                        # Extract the encoded part (everything after /plantumll)
                        encoded_part = encoded_url.split('/plantumll', 1)[1]
                    elif '/plantuml' in encoded_url and '/plantuml/png/' not in encoded_url:
                        # Extract the encoded part (everything after /plantuml)
                        # But we need to be careful - the encoded part starts right after /plantuml
                        parts = encoded_url.split('/plantuml', 1)
                        if len(parts) > 1:
                            encoded_part = parts[1]
                    
                    if encoded_part:
                        # Construct the PNG URL
                        # Try without ~1 first (works for most cases)
                        png_url = f"https://www.plantuml.com/plantuml/png/{encoded_part}"
                        
                        # Fetch the PNG directly
                        response = requests.get(png_url, timeout=30)
                        
                        # Check if we got a PNG response (even if status is not 200)
                        if response.content[:8] == b'\x89PNG\r\n\x1a\n':
                            # Check if it's an error message image or got a bad status code
                            if (response.status_code != 200 or 
                                b'HUFFMAN' in response.content or 
                                b'bad URL' in response.content or 
                                b'encoding' in response.content.lower()):
                                # This is an error message image or bad status, try with ~1 header
                                print(f" -> Detected issue (status {response.status_code}), retrying with ~1 header...")
                                png_url_with_header = f"https://www.plantuml.com/plantuml/png/~1{encoded_part}"
                                response = requests.get(png_url_with_header, timeout=30)
                                if response.status_code == 200 and response.content[:8] == b'\x89PNG\r\n\x1a\n':
                                    # Verify it's not an error message this time
                                    if b'HUFFMAN' not in response.content and b'bad URL' not in response.content:
                                        with open(output_file, 'wb') as f:
                                            f.write(response.content)
                                        file_size = os.path.getsize(output_file)
                                        print(f" -> Successfully created '{output_file}' ({file_size} bytes) with ~1 header")
                                        continue
                            else:
                                # Valid PNG without error message and good status
                                with open(output_file, 'wb') as f:
                                    f.write(response.content)
                                file_size = os.path.getsize(output_file)
                                print(f" -> Successfully created '{output_file}' ({file_size} bytes)")
                                continue
                        elif response.status_code == 200:
                            # Not a PNG, might be HTML error page
                            if response.content.startswith(b'<html') or b'HUFFMAN' in response.content or b'encoding' in response.content.lower():
                                # Try with ~1 header
                                print(f" -> Detected HTML/encoding error, retrying with ~1 header...")
                                png_url_with_header = f"https://www.plantuml.com/plantuml/png/~1{encoded_part}"
                                response = requests.get(png_url_with_header, timeout=30)
                                if response.status_code == 200 and response.content[:8] == b'\x89PNG\r\n\x1a\n':
                                    if b'HUFFMAN' not in response.content and b'bad URL' not in response.content:
                                        with open(output_file, 'wb') as f:
                                            f.write(response.content)
                                        file_size = os.path.getsize(output_file)
                                        print(f" -> Successfully created '{output_file}' ({file_size} bytes) with ~1 header")
                                        continue
                            print(f" -> Warning: Response is not a PNG image (Content-Type: {response.headers.get('Content-Type', 'N/A')})")
                        else:
                            # Bad status code, try with ~1 header
                            print(f" -> Got status {response.status_code}, retrying with ~1 header...")
                            png_url_with_header = f"https://www.plantuml.com/plantuml/png/~1{encoded_part}"
                            response = requests.get(png_url_with_header, timeout=30)
                            if response.status_code == 200 and response.content[:8] == b'\x89PNG\r\n\x1a\n':
                                if b'HUFFMAN' not in response.content and b'bad URL' not in response.content:
                                    with open(output_file, 'wb') as f:
                                        f.write(response.content)
                                    file_size = os.path.getsize(output_file)
                                    print(f" -> Successfully created '{output_file}' ({file_size} bytes) with ~1 header")
                                    continue
                            print(f" -> Warning: Failed with status {response.status_code} (Content-Type: {response.headers.get('Content-Type', 'N/A')})")
                    else:
                        print(f" -> Warning: Could not extract encoded part from URL: {encoded_url[:100]}")
                else:
                    print(f" -> Warning: URL does not start with http: {encoded_url[:100]}")
            except Exception as e:
                print(f" -> Direct URL method failed: {e}")
                import traceback
                traceback.print_exc()
            
            # If we get here, the direct URL method failed
            print(f" -> Error: Could not render '{file_path}' using direct URL method")
                        
        except Exception as e:
            print(f" -> Exception while rendering '{file_path}': {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    render_plantuml_diagrams()
    print("\nDiagram rendering complete.")
