import requests
import os
import sys
from rusta_tools.snowflake_connection import Snowflake as snowflake_connection

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)



import constants as const
import snowflake.connector.errors as snowflake_errors
import logging as logger

from pathlib import Path

home = Path.home()


sys.path.append(home)
log_dir = os.path.join(home, "rusta_logs")
try:
        os.makedirs(log_dir, exist_ok=True)
except Exception as e:
    print(f"Error creating log directory: {e}")
    SystemExit(1)

try:
    log = logger.getLogger(__name__)
    fh = logger.FileHandler(os.path.join(log_dir, "opti_loader.log"))
    formatter = logger.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    fh.setLevel(logger.INFO)
    log.addHandler(fh)

    

except Exception as e:
    log.error(f"Error in creating logger: {e}")
    sys.exit(1)




def get_missing_prices():
    #prep
    # url = f"https://prep.rusta.com/api/MissingPrices"
    url = f"https://prod.rusta.com/api/MissingPrices"
    headers = {
        "accept": "text/json",
        # prep
        # "Authorization": "AE184CFC3DC14025A6E4C13AECC96E24"
        "Authorization": "84722A714CBA49E9969EDEECBD6B3A45"
    }
    
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    if response.status_code == 200 and response.content != b'[]':
        result = response.json()
        if len(result) > 0:
            return result
        else:
            return None
    # elif response.status_code == 200 and response.content == b'[]':
    #     log.warning(f"Channels for entity id: {ent_id} wasn't found")
    # else:
    #     log.error(f"Error in getting channels for entity id: {ent_id}")
    else:
        log.error(f"Error in getting missing prices: {response.text}")
        return None

#=====================================================
def get_missing_articels_values(ent_ids):
    url = f"https://apieuw.productmarketingcloud.com/api/v1.0.1/entities:fetchdata"
    
    headers = {
        "accept": "text/json",
        "X-inRiver-APIKey": "82833a25339d857579b60a848c09caf0"
    }


    payload = {
        "entityIds": ent_ids,
        "objects": "FieldValues",
        "fieldTypeIds": f"ItemPublicationCode,ItemEcomStatusSE,ItemEnableEcomSE,ItemEcomStatusNO,ItemEnableEcomNO,ItemEcomStatusDE,ItemEnableEcomDE,ItemEcomStatusFI,ItemEnableEcomFI,ItemActiveWebSE,ItemActiveWebNO,ItemActiveWebDE,ItemActiveWebFI,ItemLongCopy,ResourceFilename,ResourceType,OptionLongCopy,ProductType,ProductCategory",        "outbound": {
                    "linkTypeIds": "ItemImage,",
                    "objects": "FieldValues",
                    }, 
        "inbound": {
                    "linkTypeIds": "ProductOption",
                    "objects": "FieldValues",
                    }
    }


    response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code == 200:
        if response.content != b'[]':
            result = response.json()
            if len(result) > 0:
                return result
        else:
            log.warning(f"Empty response for entity ids in API fetch data: {ent_ids}")
            return {}
    



def load_opti_missing_prices():
    import time
    snowflake = snowflake_connection()
    prices = []
    price_data = get_missing_prices()
    if price_data:
        for price in price_data:
            company = ""
            if price.get("marketId", "") == "SWE":
                company = "SE"
            elif price.get("marketId", "") == "FIN":
                company = "FI"
            elif price.get("marketId", "") == "NOR":
                company = "NO"
            elif price.get("marketId", "") == "DEU":
                company = "DE"
            
            if str(price.get("priceTypeId", "")) == "None":
                price["priceTypeId"] = "False"
            prices.append({
                const.ARTICLE_ID: price.get("catalogEntryCode", ""),
                const.ARTICLE_NAME: price.get("name", ""),
                const.COMPANY: company,
                const.PRICE_TYPE_ID: price.get("priceTypeId", ""),
                const.INSERT_DATE: time.strftime("%Y-%m-%d", time.localtime())
            })
        try:
            snowflake.execute_query("""DELETE FROM RUSTA_CRAWLER.RUSTA_WEB_CRAWLER.MISSING_PRICES""", "RUSTA_CRAWLER_DWH")
            snowflake.save_data_to_db(prices, "MISSING_PRICES")
        
        except snowflake_errors.DatabaseError as e:
            log.error(f"Error in saving price data to Snowflake: {e}")
            sys.exit(1)
    else:
        log.warning("No missing prices found")
        return

    print(prices)      
        

if __name__ == "__main__":
    print(load_opti_missing_prices())