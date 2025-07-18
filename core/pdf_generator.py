from weasyprint import HTML

def create_pdf_from_html(html_content: str, base_url: str):
    """
    Generates a PDF file from a string of HTML content.

    Args:
        html_content: A string containing the full HTML of the page to be converted.
        base_url: The base URL of the application, used to resolve relative paths
                  for CSS files and images.

    Returns:
        A PDF file object in bytes.
    """
    # The base_url is crucial for WeasyPrint to find the static CSS files
    return HTML(string=html_content, base_url=base_url).write_pdf()
