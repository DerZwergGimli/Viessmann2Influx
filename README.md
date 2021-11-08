
![v2i_logo](v2i_icon.png)
# ViessmannAPI to InfluxDB  - [Converter]
This library accesses the ViessmannAPI and converts the data to a InfluxDB friendly style.

## Note
The application itself is in `./app/..`!

## Requirements:
- Internet Access (for API)
- ViessmannAPI (Account and Token)
- InfluxDB Server

## Setup:
1. Install Python3 and pip3
2. `cd` into `app`
3. Run: `python3 -m venv venv` to create venv
   1. This step is optional to install dependecies not system wide
   2. You can also use the existing `./venv` and continue with `step 4`
4. Activate Python-venv
   1. Linux: `source venv/bin/activate`
   2. Windows: `venv/bin/activate.ps1` [no tested]
5. Install Python-Requirements `pip3 install -r requirements.txt`
6. Configure 'conf' file (in ./conf):
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
## DB-Structure
Influx DB is a Time-Value-Database it stores 'one' value per timestamp.
An entry contains:
- measurement(name)
- tags
- field(s)
- timestamp

To explore the db structure and create queries use chronograf. 
```text
[heating]                               {influx database}
|
|-[viessmann.Device.Info]               {contains system information}
|-[viessmann.<deviceName>.Data]         {contains data about the device (mostly temperature)}
|-[viessmann.<deviceName>.Data.dict]    {contains mostly schedule data}
|-[viessmann.<deviceName>.Data.list]    {contains mostly historic data}
|-[...]
[...]
```
- Naming
  - `<deviceName>`: is the device name for example: GazBoiler/GazBurner/HeatingCircuit/...
- Tags:
  - `<tag>`: influx db uses tags for structuring
  - If more than one device exist (see bolow)
  - You may find more tags than explained here per measurement
- Types: There are 3 types implemented as shown above 
   - `[...].Data.<array>`: If existing a `count` tag is places in the measurement tag name
   - `[...].Data.<array><dict>`: If existing a `count` and `index` tag is places in the measurement tag name
   - `[...].Data.<array><list>`: If existing a `count` and `number` tag is places in the measurement tag name
- Data-types:
  - `<bool>` casted to `<bool>`
  - `<int>` casted to `<float>`
  - `<float>` casted to `<float>`
  - `<str>` casted to `<str>`
  - `<dict>` casted to `[...].<dict>` see above
  - `<list>` casted to `[...].<list>` see above
  

## Useful Links:
- [API-Doc] https://developer.viessmann.com/
- [Forum] https://www.viessmann-community.com/ 

## Testing
- Tested with 'Vitodens 300'
- others should work - if not create an issue!

## Cards of thanks :
- PyViCare: https://github.com/somm15/PyViCare
- InfluxDB: https://github.com/influxdata/influxdb
