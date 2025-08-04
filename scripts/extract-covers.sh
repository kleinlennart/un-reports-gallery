#!/bin/bash

# Script to extract first page of PDFs as images
# Requirements: Install ImageMagick with PDF support
# On macOS: brew install imagemagick
# On Ubuntu: sudo apt-get install imagemagick

# Create covers directory if it doesn't exist
mkdir -p public/covers

# Directory containing the PDF files
PDF_DIR="./docs"
OUTPUT_DIR="./public/covers"

echo "Extracting PDF covers..."

# Function to extract first page of PDF as image
extract_cover() {
    local pdf_file="$1"
    local filename=$(basename "$pdf_file" .pdf)
    
    # Map specific filenames to expected output names based on reports.json
    local output_name=""
    case "$filename" in
        "CTBTO_Annual Report_2023") output_name="ctbto-2023.jpg" ;;
        "ECLAC_Annual Report_2024_not the corporate report") output_name="eclac-2024.jpg" ;;
        "FAO_Investment Centre_Annual Report_2024") output_name="fao-investment-2024.jpg" ;;
        "FAO_SOFA_2024") output_name="fao-sofa-2024.jpg" ;;
        "IAEA_Annual Report_2023") output_name="iaea-2023.jpg" ;;
        "ICAO_Annual Report_2024") output_name="icao-2024.jpg" ;;
        "ICC_Annual Report_2024") output_name="icc-2024.jpg" ;;
        "ICJ_Annual Report_2024") output_name="icj-2024.jpg" ;;
        "ICSC_Annual Report_2024") output_name="icsc-2024.jpg" ;;
        "IFAD_Annual Report_2024") output_name="ifad-2024.jpg" ;;
        "ILO_Annual Report_2023_2024") output_name="ilo-2023-2024.jpg" ;;
        "ILO_GFP_Annual Report_2024") output_name="ilo-gfp-2024.jpg" ;;
        "IMF_Annual Report_2024") output_name="imf-2024.jpg" ;;
        "IMO_Annual Report_2024") output_name="imo-2024.jpg" ;;
        "IOM_Annual Report_2023") output_name="iom-2023.jpg" ;;
        "ISA_Annual Report_2024") output_name="isa-2024.jpg" ;;
        "ITC_Annual Report_2024") output_name="itc-2024.jpg" ;;
        "ITLOS_Annual Report_2023") output_name="itlos-2023.jpg" ;;
        "ITU_Annual Report_2023") output_name="itu-2023.jpg" ;;
        "JIU_Annual Report_2024") output_name="jiu-2024.jpg" ;;
        "OPCW_Annual Report_2024") output_name="opcw-2024.jpg" ;;
        "UN Secretariat_Annual Report_2024") output_name="un-secretariat-2024.jpg" ;;
        "UN-Habitat_Annual Report_2024") output_name="un-habitat-2024.jpg" ;;
        "UNAIDS_Annual Report_2024") output_name="unaids-2024.jpg" ;;
        "UNCTAD_Annual Report_2023") output_name="unctad-2023.jpg" ;;
        "UNDP_Annual Report_2024") output_name="undp-2024.jpg" ;;
        "UNECE_Annual Report_2023") output_name="unece-2023.jpg" ;;
        "UNEP_Annual Report_2024") output_name="unep-2024.jpg" ;;
        "UNESCAP_Annual Report_2024") output_name="unescap-2024.jpg" ;;
        "UNESCAP_Annual Report_2025") output_name="unescap-2025.jpg" ;;
        "UNESCO_Strategic Results Report_2024") output_name="unesco-2024.jpg" ;;
        "UNFPA_Annual Report_2024") output_name="unfpa-2024.jpg" ;;
        "UNGEGN_Annual Report_2024") output_name="ungegn-2024.jpg" ;;
        "UNGGIM_Annual Report_2024") output_name="unggim-2024.jpg" ;;
        "UNHCR_Annual Report_2024") output_name="unhcr-2024.jpg" ;;
        "UNICEF_Annual Report_2024") output_name="unicef-2024.jpg" ;;
        "UNIDO_Annual Report_2024") output_name="unido-2024.jpg" ;;
        "UNITAR_Annual Report_2022") output_name="unitar-2022.jpg" ;;
        "UNOPS_Annual Report_2024") output_name="unops-2024.jpg" ;;
        "UNRWA_Annual Report_2023") output_name="unrwa-2023.jpg" ;;
        "UNSSC_Annual Report_2023") output_name="unssc-2023.jpg" ;;
        "UNU_Annual Report_2024") output_name="unu-2024.jpg" ;;
        "UNWOMEN_Annual Report_2024") output_name="unwomen-2024.jpg" ;;
        "UPU_Annual Report_2024") output_name="upu-2024.jpg" ;;
        "WFP_Annual Report_2023") output_name="wfp-2023.jpg" ;;
        "WHO_Annual Report_2024") output_name="who-2024.jpg" ;;
        "WIPO_Annual Report_2024") output_name="wipo-2024.jpg" ;;
        "World Bank_Annual Report_2024") output_name="world-bank-2024.jpg" ;;
        "WTO_Annual Report_2024") output_name="wto-2024.jpg" ;;
        "mya_annual_report_2024") output_name="mya-2024.jpg" ;;
        *) output_name="${filename,,}.jpg" ;;  # Convert to lowercase as fallback
    esac
    
    local output_file="$OUTPUT_DIR/$output_name"
    
    # Convert first page to JPG with specific settings for web
    magick "${pdf_file}[0]" -density 150 -quality 85 -resize 600x800 -strip "$output_file"
    
    echo "✓ Extracted: $output_file"
}

# Check if ImageMagick is installed
if ! command -v magick &> /dev/null; then
    echo "Error: ImageMagick is not installed."
    echo "Please install it first:"
    echo "  macOS: brew install imagemagick"
    echo "  Ubuntu: sudo apt-get install imagemagick"
    exit 1
fi

# Extract covers from all PDF files
for pdf_file in "$PDF_DIR"/*.pdf; do
    if [ -f "$pdf_file" ]; then
        extract_cover "$pdf_file"
    fi
done

echo ""
echo "Cover extraction complete!"
echo "Check the $OUTPUT_DIR directory for the generated images."
echo ""
echo "Note: You may need to rename the generated files to match the coverImage"
echo "names in data/reports.json for the gallery to display them correctly."
