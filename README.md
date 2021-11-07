
![v2i_logo](v2i_icon.png)
# ViessmannAPI to InfluxDB  - [Converter]
This library accesses the ViessmannAPI and converts the data to a InfluxDB friendly style.

## Requirements:
- Internet Access (for API)
- ViessmannAPI (Account and Token)
- InfluxDB Server

## Setup:
1. Install Python3 and pip3
2. Run: `python3 -m venv venv` to create venv
3. Activate Python-venv
   1. Linux: `source venv/bin/activate`
   2. Windows: `venv/bin/activate.ps1` [no tested]
4. Install Python-Requirements `pip3 install -r requirements.txt`
5. Configure 'conf' file (in ./conf):
   1. `conf/conf.json`
         1. Copy the file `conf/conf.json.sample` to `conf/conf.json`
         2. Edit the file according to your `ViessmannAPI_Credentials` and `InfluxDB_Server_Config`
   
---

## ViessmannAPI Configuration:
<< https://raw.githubusercontent.com/somm15/PyViCare/master/README.md >>
### Migrate to PyViCare 1.x and above

To use PyViCare 1.x, every user has to register and create their private API key. Follow these steps to create your API key:

1. Login to the [Viessmann Developer Portal](https://developer.viessmann.com/) with your existing ViCare username from the ViCare app.
2. In the menu navigate to `API Keys`.
3. Create a new OAuth client using following data:
   - Name: PyViCare
   - Google reCAPTCHA: Disabled
   - Redirect URIs: `vicare://oauth-callback/everest`
4. Copy the `Client ID` to use in your code. Pass it as constructor parameter to the device.

Please not that not all previous properties are available in the new API. Missing properties were removed and might be added later if they are available again.

---

## Useful Links:
 -  [API-Doc] https://developer.viessmann.com/
 - [Forum] https://www.viessmann-community.com/ 

## Testing
- Tested with 'Vitodens 300'
- others should work - if not create an issue!

## Cards of thanks :
- PyViCare: https://github.com/somm15/PyViCare
- InfluxDB: https://github.com/influxdata/influxdb
