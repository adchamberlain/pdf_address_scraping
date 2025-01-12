import PyPDF2
import pandas as pd
import re

def extract_addresses_from_pdf(pdf_path):
    # Create a PDF file object
    pdf_file = open(pdf_path, 'rb')
    
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    # Initialize lists to store data
    data = []
    
    # Iterate through all pages
    for page in pdf_reader.pages:
        # Extract text from the page
        text = page.extract_text()
        
        # Split text into lines
        lines = text.split('\n')
        
        # Process each line
        for line in lines:
            # Skip header lines and empty lines
            if line.strip() == '' or 'Service Address' in line or 'County Acct #' in line or 'Parcel ID' in line:
                continue
            
            # Use regex to find the components
            # Looking for: address pattern, R-number pattern, and numerical ID pattern
            match = re.match(r'^(.*?)\s+(R\d+)\s+(\d+)$', line.strip())
            
            if match:
                address, acct_num, parcel_id = match.groups()
                data.append({
                    'Street_Address': address.strip(),
                    'Account_Number': acct_num.strip(),
                    'Parcel_ID': parcel_id.strip()
                })
    
    # Close the PDF file
    pdf_file.close()
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    return df

# Add debugging prints
def debug_pdf_content(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    print(f"Number of pages: {len(pdf_reader.pages)}")
    
    # Print first few lines of first page
    first_page_text = pdf_reader.pages[0].extract_text()
    print("\nFirst 500 characters of first page:")
    print(first_page_text[:500])
    
    # Print some example lines after processing
    lines = first_page_text.split('\n')
    print("\nFirst 5 non-empty lines after splitting:")
    count = 0
    for line in lines:
        if line.strip() and count < 5:
            print(f"Line: '{line}'")
            count += 1
    
    pdf_file.close()

# Use the functions
try:
    # First debug the PDF content
    print("Debugging PDF content:")
    debug_pdf_content('/Users/andrewchamberlain/Desktop/address_list.pdf')
    
    print("\nAttempting to extract addresses:")
    df = extract_addresses_from_pdf('/Users/andrewchamberlain/Desktop/address_list.pdf')
    
    # Print DataFrame info
    print("\nDataFrame info:")
    print(df.info())
    
    # Save to CSV
    df.to_csv('/Users/andrewchamberlain/Desktop/addresses.csv', index=False)
    print("\nSuccessfully created addresses.csv")
    
    # Display first few rows to verify
    print("\nFirst few rows of the extracted data:")
    print(df.head())
    
except FileNotFoundError:
    print("Error: PDF file not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
