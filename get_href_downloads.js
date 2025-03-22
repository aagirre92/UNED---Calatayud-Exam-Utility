function get_href_pdf_download_links() {
    // Get all links on the page
    const links = Array.from(document.getElementsByTagName('a'));

    // Filter for PDF links and remove duplicates
    const pdfLinks = [...new Set(
        links
            .filter(link => link.href.toLowerCase().endsWith('.pdf'))
            .map(link => link.href)
    )];

    // Create JSON object
    const json = { urls: pdfLinks };

    // Convert JSON object to string
    const jsonString = JSON.stringify(json, null, 2);

    // Save JSON string to file
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'list_downloads.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    return pdfLinks;
}

// Run the download function
get_href_pdf_download_links();