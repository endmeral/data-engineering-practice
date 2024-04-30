import requests
import pandas as pd 
import re

url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
date = "2024-01-19 10:24"

def download_file(url, date):
    print("Accessing URL: %s" % url)
    response = requests.get(url)
    if response.status_code == 200:   
        html_content = response.text
        
        lines = html_content.split('\n')
        
        for line in lines:
            if date in line:
                href_pattern = r'<a\s+href="([^"]+)"'
                href_match = re.search(href_pattern, line)
                
                if href_match:
                    full_url = url + href_match.group(1)
                    response = requests.get(full_url)
                    if response.status_code == 200:      
                        with open(href_match.group(1), 'wb') as file:
                            file.write(response.content)
                        print("Saved file as '%s'." % href_match.group(1))
                        return href_match.group(1)
                    else:
                        print("Failed to download. Status code: %s." % response.status_code)
                        return False
                else:
                    print("Could not find pattern.")
                    return False
        else:
            print("Could not find specified file.")       
        return False
    else:
        print("Failed to download. Status code: %s." % response.status_code)
        return False

def main():
    filepath = download_file(url, date)
    if filepath:
        df = pd.read_csv(filepath, low_memory=False)
        
        df_numeric_temp = df[df['HourlyDryBulbTemperature'].str.isnumeric()]
        
        df_numeric_temp.loc[:, 'HourlyDryBulbTemperature'] = pd.to_numeric(df_numeric_temp['HourlyDryBulbTemperature'])
        
        max_temp_value = df_numeric_temp['HourlyDryBulbTemperature'].max()
        
        rows_with_max_temp = df_numeric_temp[df_numeric_temp['HourlyDryBulbTemperature'] == max_temp_value]
        print("Rows with the highest temperature value:")
        print(rows_with_max_temp.iloc[:, [0, 1, 10]])

if __name__ == "__main__":
    main()
