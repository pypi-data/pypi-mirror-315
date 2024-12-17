import requests
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import enum
# [{'BLOOMBERG_ID': 'LULU US', 'METRIC': 'TOTAL_wgtavgprice_total_instock_wholesale', 'WEEK_START_DATE': 1732492800000, 'VALUE': 100.5477408568}]

@dataclass
class EcomInsightsMetric:
    BLOOMBERG_ID: str
    METRIC: str
    WEEK_START_DATE: int
    VALUE: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def stream_api(api_key:str, ticker: str, report_frequency: str):
    """
    Connects to the streaming API and processes incoming data.
    """
    try:
        with requests.post(
            "https://ecom-api.ad.flywheeldigital.com/stream",
            data=json.dumps({"ticker": ticker, "report_frequency": report_frequency}),
            headers={"Content-Type": "application/json",
                     "x-api-key": api_key},
            timeout=None,
        ) as response:
            if response.status_code != 200:
                print(f"Failed to connect: {response.status_code}")
                return
            x = response.json()
            results = []
            
            for i in x:
                ecom_insight = EcomInsightsMetric(**i)
                results.append(ecom_insight)
                
            return results

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
