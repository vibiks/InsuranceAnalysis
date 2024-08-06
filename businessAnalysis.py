import pandas as pd
import requests
import json

def get_reference_number(json_data):
    # Check if 'Data' key is in json_data and it has at least one item
    if 'Data' in json_data and len(json_data['Data']) > 0:
        # Get the first item in the 'Data' list
        first_item = json_data['Data'][0]
        # Extract the 'Reference Number'
        reference_number = first_item.get('Reference Number', None)
        return reference_number
    return None

#Get firm details
def getfirmdetails(firmname):
  url = f"https://register.fca.org.uk/services/V0.1/Search?q={firmname}&type=firm"
  headers = {
      "X-Auth-Email": "kgs.sri@gmail.com",
      "X-Auth-Key": "debd761d67d74624a424198528c89945",
      "Content-Type": "application/json"
  }

  response = requests.get(url, headers=headers)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the JSON response
      data = response.json()
      ref_num = get_reference_number(data)
  else:
      print(f"Failed to retrieve data: {response.status_code}")
      print(response.text)
  return ref_num




def load_business_complaints_data():
  # Load the Excel file
  excel_file_path = "/content/insurancedata/business-complaints-data-h1-2022.xlsx"

  # Load sheet into separate DataFrames
  df_bdata = pd.read_excel(excel_file_path, sheet_name='New cases')
  df = df_bdata.loc[:, df_bdata.columns != 'Business Group']
  df = df.loc[:, df.columns != 'New Cases']
  df.drop(df.tail(1).index,inplace=True)
  df.drop(df.head(1).index,inplace=True)
  df.fillna(0, inplace=True)
  df = df.rename(columns={'Unnamed: 4': 'BankingCredit', 'Unnamed: 5': 'MortgageHomefin','Unnamed: 6': 'GenInsPurprotect','Unnamed: 7': 'PPI','Unnamed: 8': 'Investments'})

  # List of firm names
  firm_names_tmp = df['Business Name'].unique()
  firm_names = firm_names_tmp[:20]
  print(firm_names)

  # List to store the JSON responses
  firm_details_list = []

  # Iterate over the list of firm names and call the function
  for firm_name in firm_names:
      firm_refno = getfirmdetails(firm_name)
      if firm_refno is not None:
          firm_details_list.append(firm_refno)

  print(firm_details_list)

load_business_complaints_data()