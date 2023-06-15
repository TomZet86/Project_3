"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Tomas Zechmeister

email: t.zech@seznam.cz

discord: Tony Rocky Horror#9131

"""

import requests
import os
import csv
import sys
from bs4 import BeautifulSoup


def check_args() -> str:

    """

    Checking arguments provided while launching the script. 
    If one of the args is missing or URL and OUTPUT_FILE args don't contain correct values,
    the function prints out a message and terminates the execution of the script.
    If all args are in place and contain correct values, the script returns both args.

    """

    try:
        args_present = sys.argv[1] and sys.argv[2]
    except IndexError:
        print('At least on argument is missing','usage: script_name.py "<URL>" "<OUTPUT_FILE.csv>"', sep='\n')
        quit()
    else:
        url_response = requests.get(sys.argv[1])
        correct_url_response ='Response [200]' in str(url_response)
        correct_output_file = ".csv" in sys.argv[2]
        if correct_url_response and correct_output_file:
            output_file_path = os.getcwd() + os.sep
            url = sys.argv[1]
            output_file = sys.argv[2]
            print('Both URL and OUTPUT_FILE argumnets are correct.', "Generating report, please wait..", sep='\n')
        elif not correct_url_response:
            print('URL contains an incorrect value.', f'URL reponse: {url_response}', sep='\n')
            quit()
        elif not correct_output_file:
            print('OUTPUT_FILE argument contains an incorrect value.')
            quit()
        return url, output_file_path, output_file, url_response   
    

def data_writer(output_file_path:str, output_file:str, temp_dict:dict) -> csv:
    
    """

    Writing reuquired scraped data into a csv file

    """
    with open(output_file_path + output_file, mode="a", encoding='UTF-8') as new_csv:         
        writer = csv.writer(new_csv)
        writer.writerow(temp_dict.values())


def data_reader(output_file_path:str, output_file:str) -> list:

    """

    Collecting data for the final export into the final output file and storing them in a list

    """

    with open(output_file_path + output_file, newline='', encoding= 'UTF-8') as new_csv:
        reader = csv.reader(new_csv)
        data = [line for line in reader if line]
        return data


def data_finalizer(output_file_path, output_file, data, temp_dict) -> csv:

    """

    Adding a header from dict keys, importing data fromt he reader and removing blank rows

    """
     
    with open(output_file_path + output_file,'w',newline='', encoding= 'UTF-8') as new_csv:
        writer = csv.writer(new_csv,delimiter=';')
        writer.writerow(temp_dict.keys())
        writer.writerows(data)
    

def process_data():
    url, output_file_path, output_file, url_response = check_args()
    soup = BeautifulSoup(url_response.text, 'html.parser')
    regions_tables = soup.find_all("table", {"class": "table"})
    temp_dict = dict()  

    for table in regions_tables:
        all_tr = table.find_all("tr")
        for tr in all_tr[2:]:
            td_in_row = tr.find_all("td")
            code = td_in_row[0].get_text()
            location = td_in_row[1].get_text()
            temp_dict['code'] = code
            temp_dict['location'] = location
            td_a = tr.find_all("td", {"class": "cislo"})
            for a in td_a:
                base_url = url.rsplit('/', 1)[0] + '/'
                new_url = base_url + a.a["href"]
                new_url_response = requests.get(new_url)
                new_soup = BeautifulSoup(new_url_response.text, 'html.parser')
                
                top_tables = new_soup.find_all("table", {"id": "ps311_t1"})
                party_tables = new_soup.find_all("div", {"class":"t2_470"})
               
                for table in top_tables:
                    all_tr = table.find_all("tr")
                    
                    for tr in all_tr[1:]:
                        all_td =  tr.find_all("td",{"data-rel":"L1"})
                        if len(all_td) == 0:
                            continue
                        else:
                            registered = (all_td[0].get_text()).replace(u'\xa0', '')
                            envelopes = (all_td[2].get_text()).replace(u'\xa0', '')
                            valid = (all_td[3].get_text()).replace(u'\xa0', '')
                            temp_dict['registered'] = registered
                            temp_dict['envelopes'] = envelopes
                            temp_dict['valid'] = valid

                            for party_results in party_tables:
                                all_tr = party_results.find_all("tr")
                                
                                for tr in all_tr[2:]:
                                    all_td =  tr.find_all("td")
                                    if len(all_td) == 0:
                                        continue
                                    else:
                                        temp_dict[all_td[1].get_text()] = (all_td[2].get_text()).replace(u'\xa0', '')
                            data_writer(output_file_path, output_file, temp_dict)
                            
    data = data_reader(output_file_path, output_file)
    data_finalizer(output_file_path, output_file, data, temp_dict)


if __name__ == '__main__':
    process_data()
