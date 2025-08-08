"""
Fetch latest UN reports from the UN Digital Library and extract data from MARCXML.

This script pulls reports from 2025 and extracts structured data using pandas.
URL: https://digitallibrary.un.org/search?ln=en&as=1&rm=&sf=latest+first&so=d&rg=100&c=Resource+Type&c=UN+Bodies&c=&of=hb&fti=0&fct__1=Reports&fti=0&as_query=JTdCJTIyZGF0ZV9zZWxlY3RvciUyMiUzQSU3QiUyMmRhdGVUeXBlJTIyJTNBJTIyY3JlYXRpb25fZGF0ZSUyMiUyQyUyMmRhdGVQZXJpb2QlMjIlM0ElMjJzcGVjaWZpY2RhdGVwZXJpb2QlMjIlMkMlMjJkYXRlRnJvbSUyMiUzQSUyMjIwMjUtMDEtMDElMjIlMkMlMjJkYXRlVG8lMjIlM0ElMjIlMjIlN0QlMkMlMjJjbGF1c2VzJTIyJTNBJTVCJTdCJTIyc2VhcmNoSW4lMjIlM0ElMjJhbGwtZmllbGQlMjIlMkMlMjJjb250YWluJTIyJTNBJTIyYWxsLXdvcmRzJTIyJTJDJTIydGVybSUyMiUzQSUyMiUyMiUyQyUyMm9wZXJhdG9yJTIyJTNBJTIyQU5EJTIyJTdEJTJDJTdCJTIyc2VhcmNoSW4lMjIlM0ElMjJ5ZWFyJTIyJTJDJTIyY29udGFpbiUyMiUzQSUyMmFsbC13b3JkcyUyMiUyQyUyMnRlcm0lMjIlM0ElMjIyMDI1JTIyJTJDJTIyb3BlcmF0b3IlMjIlM0ElMjJBTkQlMjIlN0QlNUQlN0Q%3D&action_search=placeholder#searchresultsbox
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import json
import re
import time
from typing import List, Dict, Any


def get_marcxml_url(base_url: str) -> str:
    """Convert the search URL to return MARCXML format."""
    # Replace 'of=hb' with 'of=xm' to get MARCXML format
    return base_url.replace('of=hb', 'of=xm')


def get_alternative_formats(base_url: str) -> Dict[str, str]:
    """Get different format URLs to try."""
    return {
        'marcxml': base_url.replace('of=hb', 'of=xm'),
        'json': base_url.replace('of=hb', 'of=recjson'),
        'dublin_core': base_url.replace('of=hb', 'of=xd'),
        'csv': base_url.replace('of=hb', 'of=xe'),
        'rss': base_url.replace('of=hb', 'of=xr'),
    }


def fetch_data_with_session(url: str, format_type: str = 'marcxml') -> str:
    """Fetch data using a session with better browser simulation."""
    session = requests.Session()
    
    # More realistic headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    session.headers.update(headers)
    
    # Try different formats
    formats = get_alternative_formats(url)
    target_url = formats.get(format_type, formats['marcxml'])
    
    print(f"Trying {format_type} format: {target_url}")
    
    try:
        # First, visit the main site to establish session
        main_site = "https://digitallibrary.un.org/"
        print("Establishing session with main site...")
        session.get(main_site, timeout=30)
        
        # Wait a bit
        import time
        time.sleep(2)
        
        # Now try the actual request
        print(f"Requesting data...")
        response = session.get(target_url, timeout=30)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content length: {len(response.text)}")
        print(f"First 500 chars of response: {response.text[:500]}")
        
        if response.status_code == 200 and len(response.text) > 0:
            return response.text
        else:
            raise Exception(f"Failed to get data: Status {response.status_code}, Length {len(response.text)}")
            
    except Exception as e:
        print(f"Error with {format_type}: {e}")
        return ""


def try_simple_search() -> str:
    """Try a simpler search that might work better."""
    # Simple search for 2025 reports
    simple_url = "https://digitallibrary.un.org/search?ln=en&p=year:2025&f=&rm=&ln=en&sf=latest+first&so=d&rg=25&c=Resource+Type&of=xm&fct__1=Reports"
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/xml,text/xml,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    session.headers.update(headers)
    
    print(f"Trying simple search: {simple_url}")
    response = session.get(simple_url, timeout=30)
    
    print(f"Simple search - Status: {response.status_code}, Length: {len(response.text)}")
    print(f"Content preview: {response.text[:500]}")
    
    return response.text if response.status_code == 200 else ""


def parse_marc_field(field_element: ET.Element) -> Dict[str, Any]:
    """Parse a MARC field element into a dictionary."""
    field_data = {
        'tag': field_element.get('tag'),
        'ind1': field_element.get('ind1', ''),
        'ind2': field_element.get('ind2', ''),
        'subfields': {}
    }
    
    # Handle subfields
    for subfield in field_element.findall('.//subfield'):
        code = subfield.get('code')
        value = subfield.text or ''
        
        # Handle multiple subfields with same code
        if code in field_data['subfields']:
            if isinstance(field_data['subfields'][code], list):
                field_data['subfields'][code].append(value)
            else:
                field_data['subfields'][code] = [field_data['subfields'][code], value]
        else:
            field_data['subfields'][code] = value
    
    return field_data


def extract_report_data(record: ET.Element) -> Dict[str, Any]:
    """Extract structured data from a MARC record."""
    report_data = {
        'record_id': '',
        'title': '',
        'author': '',
        'publisher': '',
        'publication_date': '',
        'publication_year': '',
        'language': '',
        'subject': [],
        'description': '',
        'url': '',
        'isbn': '',
        'issn': '',
        'document_symbol': '',
        'series': '',
        'notes': '',
        'physical_description': '',
        'edition': '',
        'un_body': '',
        'report_type': ''
    }
    
    # Parse all fields
    for field in record.findall('.//datafield'):
        field_info = parse_marc_field(field)
        tag = field_info['tag']
        subfields = field_info['subfields']
        
        # Extract specific data based on MARC tags
        if tag == '001':  # Control number
            report_data['record_id'] = field.text or ''
        elif tag == '245':  # Title
            title_parts = []
            if 'a' in subfields:
                title_parts.append(subfields['a'])
            if 'b' in subfields:
                title_parts.append(subfields['b'])
            report_data['title'] = ' '.join(title_parts).strip()
        elif tag == '100' or tag == '110' or tag == '111':  # Author/Corporate author
            if 'a' in subfields:
                report_data['author'] = subfields['a']
        elif tag == '260' or tag == '264':  # Publication info
            if 'b' in subfields:
                report_data['publisher'] = subfields['b']
            if 'c' in subfields:
                pub_date = subfields['c']
                report_data['publication_date'] = pub_date
                # Extract year
                year_match = re.search(r'\d{4}', pub_date)
                if year_match:
                    report_data['publication_year'] = year_match.group()
        elif tag == '041':  # Language
            if 'a' in subfields:
                report_data['language'] = subfields['a']
        elif tag == '650':  # Subject
            if 'a' in subfields:
                subject = subfields['a']
                if isinstance(subject, list):
                    report_data['subject'].extend(subject)
                else:
                    report_data['subject'].append(subject)
        elif tag == '520':  # Summary/Description
            if 'a' in subfields:
                report_data['description'] = subfields['a']
        elif tag == '856':  # Electronic location and access
            if 'u' in subfields:
                report_data['url'] = subfields['u']
        elif tag == '020':  # ISBN
            if 'a' in subfields:
                report_data['isbn'] = subfields['a']
        elif tag == '022':  # ISSN
            if 'a' in subfields:
                report_data['issn'] = subfields['a']
        elif tag == '191':  # Document symbol (UN specific)
            if 'a' in subfields:
                report_data['document_symbol'] = subfields['a']
        elif tag == '490' or tag == '830':  # Series
            if 'a' in subfields:
                report_data['series'] = subfields['a']
        elif tag == '500':  # General note
            if 'a' in subfields:
                report_data['notes'] = subfields['a']
        elif tag == '300':  # Physical description
            desc_parts = []
            if 'a' in subfields:
                desc_parts.append(subfields['a'])
            if 'b' in subfields:
                desc_parts.append(subfields['b'])
            if 'c' in subfields:
                desc_parts.append(subfields['c'])
            report_data['physical_description'] = ' '.join(desc_parts).strip()
        elif tag == '250':  # Edition
            if 'a' in subfields:
                report_data['edition'] = subfields['a']
        elif tag == '710':  # Corporate name (UN Body)
            if 'a' in subfields:
                report_data['un_body'] = subfields['a']
        elif tag == '655':  # Genre/form (Report type)
            if 'a' in subfields:
                report_data['report_type'] = subfields['a']
    
    # Clean up subject list
    report_data['subject'] = [s.strip() for s in report_data['subject'] if s.strip()]
    
    return report_data


def marcxml_to_dataframe(marcxml_content: str) -> pd.DataFrame:
    """Convert MARCXML content to a pandas DataFrame."""
    # Parse XML
    root = ET.fromstring(marcxml_content)
    
    # Find all records
    records = root.findall('.//record')
    
    # Extract data from each record
    reports_data = []
    for record in records:
        report_data = extract_report_data(record)
        reports_data.append(report_data)
    
    # Create DataFrame
    df = pd.DataFrame(reports_data)
    
    # Convert subject list to string for CSV compatibility
    if 'subject' in df.columns:
        df['subject'] = df['subject'].apply(lambda x: '; '.join(x) if isinstance(x, list) else x)
    
    return df


def filter_secretary_general_reports(df: pd.DataFrame) -> pd.DataFrame:
    """Filter to Secretary-General reports based on MARC tags and content."""
    # Filter criteria for SG reports
    sg_filters = (
        df['document_symbol'].str.contains('A/', na=False) |  # UN General Assembly documents
        df['author'].str.contains('Secretary-General', case=False, na=False) |
        df['title'].str.contains('Secretary-General', case=False, na=False) |
        df['subject'].str.contains('Secretary-General', case=False, na=False)
    )
    
    return df[sg_filters].copy()


def main():
    """Main function to fetch and process UN reports."""
    # Original search URL (2025 reports)
    search_url = "https://digitallibrary.un.org/search?ln=en&as=1&rm=&sf=latest+first&so=d&rg=100&c=Resource+Type&c=UN+Bodies&c=&of=hb&fti=0&fct__1=Reports&fti=0&as_query=JTdCJTIyZGF0ZV9zZWxlY3RvciUyMiUzQSU3QiUyMmRhdGVUeXBlJTIyJTNBJTIyY3JlYXRpb25fZGF0ZSUyMiUyQyUyMmRhdGVQZXJpb2QlMjIlM0ElMjJzcGVjaWZpY2RhdGVwZXJpb2QlMjIlMkMlMjJkYXRlRnJvbSUyMiUzQSUyMjIwMjUtMDEtMDElMjIlMkMlMjJkYXRlVG8lMjIlM0ElMjIlMjIlN0QlMkMlMjJjbGF1c2VzJTIyJTNBJTVCJTdCJTIyc2VhcmNoSW4lMjIlM0ElMjJhbGwtZmllbGQlMjIlMkMlMjJjb250YWluJTIyJTNBJTIyYWxsLXdvcmRzJTIyJTJDJTIydGVybSUyMiUzQSUyMiUyMiUyQyUyMm9wZXJhdG9yJTIyJTNBJTIyQU5EJTIyJTdEJTJDJTdCJTIyc2VhcmNoSW4lMjIlM0ElMjJ5ZWFyJTIyJTJDJTIyY29udGFpbiUyMiUzQSUyMmFsbC13b3JkcyUyMiUyQyUyMnRlcm0lMjIlM0ElMjIyMDI1JTIyJTJDJTIyb3BlcmF0b3IlMjIlM0ElMjJBTkQlMjIlN0QlNUQlN0Q%3D&action_search=placeholder"
    
    try:
        print("Fetching MARCXML data from UN Digital Library...")
        marcxml_content = fetch_marcxml_data(search_url)
        
        print("Parsing MARCXML and creating DataFrame...")
        df = marcxml_to_dataframe(marcxml_content)
        
        print(f"Found {len(df)} reports total")
        
        # Filter for Secretary-General reports
        sg_df = filter_secretary_general_reports(df)
        print(f"Found {len(sg_df)} Secretary-General reports")
        
        # Save to CSV
        output_file = "../../data/latest_un_reports_2025.csv"
        df.to_csv(output_file, index=False)
        print(f"All reports saved to {output_file}")
        
        # Save SG reports separately
        sg_output_file = "../../data/latest_sg_reports_2025.csv"
        sg_df.to_csv(sg_output_file, index=False)
        print(f"Secretary-General reports saved to {sg_output_file}")
        
        # Display summary
        print("\nDataFrame Info:")
        print(df.info())
        
        print("\nSample of latest reports:")
        print(df[['title', 'author', 'publication_date', 'un_body']].head())
        
        if not sg_df.empty:
            print("\nSecretary-General reports:")
            print(sg_df[['title', 'document_symbol', 'publication_date']].head())
        
        return df, sg_df
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None


if __name__ == "__main__":
    all_reports, sg_reports = main()