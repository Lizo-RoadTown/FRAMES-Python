"""
Extract CADENCE project data from Notion export.

This script processes the 1.1GB CADENCE export zip file and:
1. Extracts markdown files (training content)
2. Extracts CSV files (team/collaboration data)
3. Identifies useful PDFs for module references
4. Organizes for import into FRAMES

Usage:
    python scripts/extract_cadence_project.py
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
import csv
import json

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ZIP_FILE = PROJECT_ROOT / "539febca-778f-4de9-97d3-1ece55645f17_ExportBlock-e881308d-93d4-492e-bdac-6d92e7bb342e.zip"
OUTPUT_DIR = PROJECT_ROOT / "data" / "projects" / "CADENCE"
TEMP_DIR = PROJECT_ROOT / "temp_cadence_extract"

# Create output directories
MARKDOWN_DIR = OUTPUT_DIR / "markdown"
CSV_DIR = OUTPUT_DIR / "databases"
PDF_LIST_FILE = OUTPUT_DIR / "useful_pdfs.json"
REPORT_FILE = OUTPUT_DIR / "extraction_report.md"


def extract_zip():
    """Extract the nested zip files"""
    print("Extracting zip file...")
    print(f"Source: {ZIP_FILE}")
    print(f"Target: {TEMP_DIR}")

    # Clean temp directory
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # Extract outer zip
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)

    # Find and extract inner zip
    inner_zips = list(TEMP_DIR.glob("*.zip"))
    if inner_zips:
        print(f"Found inner zip: {inner_zips[0].name}")
        with zipfile.ZipFile(inner_zips[0], 'r') as zip_ref:
            zip_ref.extractall(TEMP_DIR / "content")
        print(f"Extracted to: {TEMP_DIR / 'content'}")
    else:
        print("No inner zip found, using outer extraction")


def categorize_files():
    """Categorize extracted files"""
    print("\nCategorizing files...")

    content_dir = TEMP_DIR / "content"
    if not content_dir.exists():
        content_dir = TEMP_DIR

    stats = {
        'markdown': [],
        'csv': [],
        'pdf': [],
        'images': [],
        'other': []
    }

    for file_path in content_dir.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext == '.md':
                stats['markdown'].append(file_path)
            elif ext == '.csv':
                stats['csv'].append(file_path)
            elif ext == '.pdf':
                stats['pdf'].append(file_path)
            elif ext in ['.png', '.jpg', '.jpeg']:
                stats['images'].append(file_path)
            else:
                stats['other'].append(file_path)

    print(f"  Markdown files: {len(stats['markdown'])}")
    print(f"  CSV files: {len(stats['csv'])}")
    print(f"  PDF files: {len(stats['pdf'])}")
    print(f"  Images: {len(stats['images'])}")
    print(f"  Other: {len(stats['other'])}")

    return stats


def identify_useful_content(stats):
    """Identify files useful for modules and research"""
    print("\nIdentifying useful content...")

    # Useful markdown files (training/onboarding)
    useful_keywords = [
        'guide', 'tutorial', 'recruits', 'onboarding', 'software',
        'github', 'setup', 'how', 'getting', 'started'
    ]

    useful_md = []
    for md_file in stats['markdown']:
        name_lower = md_file.stem.lower()
        if any(keyword in name_lower for keyword in useful_keywords):
            useful_md.append(md_file)

    print(f"  Found {len(useful_md)} useful markdown files")

    # Useful CSVs (team/collaboration data)
    csv_keywords = [
        'meeting', 'notes', 'tasks', 'tracker', 'daily', 'logs',
        'calendar', 'progress', 'team'
    ]

    useful_csv = []
    for csv_file in stats['csv']:
        name_lower = csv_file.stem.lower()
        if any(keyword in name_lower for keyword in csv_keywords):
            # Skip "_all.csv" duplicates
            if not csv_file.stem.endswith('_all'):
                useful_csv.append(csv_file)

    print(f"  Found {len(useful_csv)} useful CSV files")

    # Useful PDFs (training materials)
    pdf_keywords = [
        'guide', 'tutorial', 'unp', 'nasa', 'training', 'course',
        'presentation', 'systems', 'power', 'communication', 'outlook'
    ]

    useful_pdf = []
    for pdf_file in stats['pdf']:
        name_lower = pdf_file.stem.lower()
        if any(keyword in name_lower for keyword in pdf_keywords):
            # Skip project-specific documents
            if not any(skip in name_lower for skip in ['pdr', 'budget', 'ieee', 'mission_design_document']):
                useful_pdf.append(pdf_file)

    print(f"  Found {len(useful_pdf)} useful PDF files")

    return {
        'markdown': useful_md,
        'csv': useful_csv,
        'pdf': useful_pdf
    }


def copy_useful_files(useful_files):
    """Copy useful files to organized output directory"""
    print("\nCopying useful files...")

    # Create output directories
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    # Copy markdown files
    print(f"  Copying {len(useful_files['markdown'])} markdown files...")
    for md_file in useful_files['markdown']:
        dest = MARKDOWN_DIR / md_file.name
        shutil.copy2(md_file, dest)

    # Copy CSV files
    print(f"  Copying {len(useful_files['csv'])} CSV files...")
    for csv_file in useful_files['csv']:
        dest = CSV_DIR / csv_file.name
        shutil.copy2(csv_file, dest)

    # Create PDF reference list (don't copy large files)
    print(f"  Creating PDF reference list...")
    pdf_info = []
    for pdf_file in useful_files['pdf']:
        pdf_info.append({
            'name': pdf_file.name,
            'size_mb': round(pdf_file.stat().st_size / (1024 * 1024), 2),
            'path_in_archive': str(pdf_file.relative_to(TEMP_DIR))
        })

    with open(PDF_LIST_FILE, 'w') as f:
        json.dump(pdf_info, f, indent=2)

    print(f"  PDF list saved to: {PDF_LIST_FILE}")


def generate_report(stats, useful_files):
    """Generate extraction report"""
    print("\nGenerating extraction report...")

    total_size = sum(f.stat().st_size for f in stats['markdown'] + stats['csv'] + stats['pdf'] + stats['images'])
    useful_size = sum(f.stat().st_size for f in useful_files['markdown'] + useful_files['csv'])

    report = f"""# CADENCE Project Extraction Report

## Summary

**Extraction Date:** {os.popen('date').read().strip()}
**Original Archive:** 1.1 GB
**Total Files Extracted:** {sum(len(v) for v in stats.values())}

### File Breakdown
- Markdown files: {len(stats['markdown'])}
- CSV files: {len(stats['csv'])}
- PDF files: {len(stats['pdf'])}
- Images: {len(stats['images'])}
- Other: {len(stats['other'])}

### Useful Content Identified
- Markdown (training/guides): {len(useful_files['markdown'])}
- CSV (team/collaboration data): {len(useful_files['csv'])}
- PDF (reference materials): {len(useful_files['pdf'])}

### Storage Impact
- Total archive size: {total_size / (1024**3):.2f} GB
- Useful content copied: {useful_size / (1024**2):.2f} MB
- **Space saved: {(total_size - useful_size) / (1024**3):.2f} GB**

---

## Useful Markdown Files (Training Content)

"""

    for md_file in useful_files['markdown']:
        report += f"- `{md_file.name}` - Copy at: `{MARKDOWN_DIR / md_file.name}`\n"

    report += "\n---\n\n## Useful CSV Files (Team Data)\n\n"

    for csv_file in useful_files['csv']:
        report += f"- `{csv_file.name}` - Copy at: `{CSV_DIR / csv_file.name}`\n"

    report += "\n---\n\n## Useful PDF Files (Reference Materials)\n\nThese PDFs should be uploaded to external storage (S3/Google Drive):\n\n"

    for pdf_file in useful_files['pdf']:
        size_mb = pdf_file.stat().st_size / (1024 * 1024)
        report += f"- `{pdf_file.name}` ({size_mb:.1f} MB)\n"

    report += f"\nSee `{PDF_LIST_FILE}` for full PDF details and archive paths.\n"

    report += """

---

## Next Steps

1. **Upload PDFs to external storage:**
   - Option A: Google Drive (free, 15GB)
   - Option B: AWS S3 (`aws s3 sync ...`)

2. **Create modules from markdown files:**
   ```bash
   # Review markdown files
   ls data/projects/CADENCE/markdown/

   # Create module in Notion Module Library
   # Link to external PDFs for reference
   ```

3. **Extract team data from CSVs:**
   ```bash
   python scripts/extract_team_data_from_csvs.py
   ```

4. **Archive original zip file:**
   - Upload to Google Drive / OneDrive
   - Or: Create GitHub release
   - Or: Upload to S3 Glacier Deep Archive
   - **Then delete local 1.1GB file**

5. **Clean up temp directory:**
   ```bash
   rm -rf temp_cadence_extract/
   ```
"""

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"  Report saved to: {REPORT_FILE}")


def main():
    print("="*60)
    print("CADENCE Project Data Extraction")
    print("="*60)

    # Check if zip file exists
    if not ZIP_FILE.exists():
        print(f"Error: Zip file not found at {ZIP_FILE}")
        sys.exit(1)

    # Step 1: Extract
    extract_zip()

    # Step 2: Categorize
    stats = categorize_files()

    # Step 3: Identify useful content
    useful_files = identify_useful_content(stats)

    # Step 4: Copy useful files
    copy_useful_files(useful_files)

    # Step 5: Generate report
    generate_report(stats, useful_files)

    print("\n" + "="*60)
    print("Extraction Complete!")
    print("="*60)
    print(f"\nUseful content saved to: {OUTPUT_DIR}")
    print(f"  - Markdown: {MARKDOWN_DIR}")
    print(f"  - CSV: {CSV_DIR}")
    print(f"  - PDF list: {PDF_LIST_FILE}")
    print(f"\nReport: {REPORT_FILE}")
    print("\nNext steps:")
    print("  1. Review extraction report")
    print("  2. Upload PDFs to external storage")
    print("  3. Create modules from markdown files")
    print("  4. Extract team data from CSVs")
    print("  5. Archive original 1.1GB zip file")
    print("  6. Clean up temp directory")


if __name__ == '__main__':
    main()
