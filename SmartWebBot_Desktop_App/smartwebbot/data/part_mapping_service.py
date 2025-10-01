"""
Part Number Mapping Service

Manages part number mappings for the Unit Receiving ADT system.
Provides search, add, and management functionality for part conversions.
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..utils.logger import get_logger


class PartMappingService:
    """Service for managing part number mappings."""
    
    def __init__(self, data_file: Optional[str] = None):
        """Initialize the service."""
        self.logger = get_logger(__name__)
        
        # Default data file location
        self.data_file = data_file or os.path.join(
            os.path.dirname(__file__), '..', '..', 'data', 'part_mappings.json'
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Initialize with default mappings if file doesn't exist
        self._initialize_default_mappings()
    
    def _initialize_default_mappings(self):
        """Initialize with complete part mappings if no data file exists."""
        if not os.path.exists(self.data_file):
            self.logger.info("Initializing complete part mappings (121 entries)")
            
            # Complete mapping of all 121 entries from reference sheet
            default_mappings = [
                {"original": "SA5816", "processAs": "5816", "description": "HONEYWELL SENOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "5853", "processAs": "5853", "description": "HONEYWELL SENOR (DO NOT PROCESS FG-1625 AS 5853)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "PROTECTION 1", "processAs": "2GIG-CP21-345E", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "tx id: 013-3285", "processAs": "2GIG-DW10-345", "description": "SMALL WINDOW/DOOR SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "2GIG-GB1", "processAs": "2GIG-GB1-345", "description": "HEAT SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "2GIG-GC2E-ADT", "processAs": "2GIG-GC2E-345", "description": "KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "2GIG-PAD1-345", "processAs": "2GIG-PAD1-345", "description": "2GIG NON TOUCH SECONDARY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "2GIG-PIR1E-345", "processAs": "2GIG-PIR1E-345", "description": "BOX SHAPE SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "2GIG-SMKT3-345", "processAs": "2GIG-SMKT3-345", "description": "smoke detector", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "300-11260", "processAs": "300-10260", "description": "RESIDEO CLASS 2 POWER SUPPLY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "3G4000RF", "processAs": "3G4000RF-ADTUSA", "description": "ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "5800PIR-RES", "processAs": "5800PIR-RES", "description": "HONEYWELL SENOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "60-362N", "processAs": "60-362N-10-319.5", "description": "UTC FIRE & SECURITY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "BP6024", "processAs": "60-670-95R", "description": "UL SENSORS", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SA6150AS-VE", "processAs": "6150ADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SA6150RF-2", "processAs": "6150RF", "description": "HONEYWELL UL KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SA6160PL2", "processAs": "6160PL2", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SA6160RF", "processAs": "6160RFPL2", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SA6160V-4", "processAs": "6160VADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SA6160VPADT", "processAs": "6160VPADT", "description": "ADT (SAFEPASS) KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SIMON XT", "processAs": "80-632-3N-XT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "875936B", "processAs": "875936B", "description": "ADT SECURITY SERVICES", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "????", "processAs": "A-CB7D36PI", "description": "OLD MINI CAMERA - ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "????", "processAs": "A-CB7D60PI", "description": "OLD MINI CAMERA - ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "A-CB7T2812PI", "processAs": "A-CB7T2812PI", "description": "OLD ADT - SMALL HEAD CAMERA W/STAND", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "????", "processAs": "A-CBVD36PI", "description": "OLD MINI CAMERA - ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADC-SVR122", "processAs": "ADC-SVR122-2T", "description": "2TB Hard Drive", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADC-V724", "processAs": "ADC-V724X", "description": "OLD ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADC-VDB105X", "processAs": "ADC-VDB105", "description": "777TS032", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADC-VDB770", "processAs": "ADC-VDB770", "description": "ALARM.COM CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "AMADT2X16LTE-3", "processAs": "ADT2X16AIO-1", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADT5AIO-1", "processAs": "ADT5AIO-2", "description": "NEED TO SET UP -1", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "AMADT7AIO-1", "processAs": "ADT7AIO-1", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "AMADT7AIO-3", "processAs": "ADT7AIO-3", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "AMADT7AIO-5", "processAs": "ADT7AIO-5", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "DS-2CD2123G0", "processAs": "DS-2CD2123G0-I 2.8mm", "description": "HIKVISION camera", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "DS-2CD2143G2-IU", "processAs": "DS-2CD2143G0-I 2.8MM", "description": "HIKVISION", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "DS-7604NI-E1/4P-2T", "processAs": "DS-7604NI-E1/4P-2TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "DS-7604NI-Q1/4P", "processAs": "DS-7604NI-Q1/4P-2TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "DS-7608NI-Q2/8P-2TB", "processAs": "DS-7608NI-Q2/8P-2TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "DS-7608NI-Q2/8P-4TB", "processAs": "DS-7608NI-Q2/8P-4TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "EV-DW4927SS", "processAs": "EV-DW4927SS", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "EX3700", "processAs": "EX3700-100NAS", "description": "NETGEAR EXTENDER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "EX6120", "processAs": "EX6120-1ADNAS", "description": "NETGEAR WIFI EXTENDER AC1200", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA00426-US", "description": "NEST HUB MAX - LIGHT GRAY BACK W/STAND", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "H2D", "processAs": "GA00595-US", "description": "Google Nest Wifi Router", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA00638-US", "description": "GOOGLE NEST MINI - CHALK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA00639-US", "description": "NEST HUB MAX (DARK GRAY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA00781-US", "description": "GOOGLE NEST DOORBELL MINI - CHARCOAL", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA01317-US", "description": "GOOGLE NEST CAM G3AL9", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA01318-US", "description": "Google Nest Doorbell (snow)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA01331-US", "description": "GOOGLE NEST HUB MINI (WHITE/GRAY)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "GJQ9T", "processAs": "GA01998-US", "description": "Indoor Google Nest Cam - SMALL HEAD CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA02076-US", "description": "Google Nest Doorbell (Ash, US)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA02411-US", "description": "Google Nest w/ Flood lights", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "GA02767-US", "description": "GOOGLE NEST DOORBELL MINI (COTTON WHITE)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "GS305Pv2", "processAs": "GS305-300PAS", "description": "NETGEAR 5-PORT ETHERNET UNMANAGED", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "HSS301", "processAs": "HSS301-2ADNAS", "description": "ADT NETGEAR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IHUB-3001B-ADT", "processAs": "IHUB-3001B-ADT", "description": "ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IP CAMERA", "processAs": "IPC-HDBW4231E-ADT36", "description": "BUBBLE CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IPC-HFW4120E-ADT36", "processAs": "IPC-HFW4120E-ADT36", "description": "IP CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IQPANEL4", "processAs": "IQP4001", "description": "OLSYS KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IQPANEL4", "processAs": "IQP4001BLK", "description": "OLSYS KEYPAD - BLACK KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "AMAZON SIGN", "processAs": "ISC-BDL2-WP12G", "description": "Amazon Sensor", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Medium Size Amazon Sensor", "processAs": "ISC-BDL2-WP12G", "description": "bosch sensor", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "LYNXPLUS2", "processAs": "L3000", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "LE2077-NA", "processAs": "LE2077-ADTAT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "LE4000RF", "processAs": "LE4000RF-ADTAT", "description": "ADT WIRELESS COMMUNICATOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "LTEL3A", "processAs": "LTEL3A-ADT", "description": "MEMORY BOARD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "LYNXTOUCH2/L5000", "processAs": "LTEL5A-ADT", "description": "HONEYWELL KEYPAD - ON DISPLAY RACK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADEMCO LYNXR-I", "processAs": "LYNXR", "description": "OLD ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "MR70", "processAs": "MR70S-1ADNAS", "description": "NIGHTHAWK MESH WIFI 6 ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "821LMB", "processAs": "MYQ-821LMB", "description": "My Q Garage Bundle box", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "NV412A-ADT", "processAs": "NV412A-ADT", "description": "ETHERNET BLACK BOX", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "51000-601", "processAs": "OTHER C02 DETECTOR", "description": "DETECTOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADC-V515", "processAs": "OTHER CAMERA", "description": "ADT OLDER CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IPC216A (2.8MM)", "processAs": "OTHER CAMERA", "description": "BUBBLE CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "DS-2CE5AD3T-AVPIT3ZF", "processAs": "OTHER CAMERA", "description": "HIKVISION", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ANBW240", "processAs": "OTHER CAMERA", "description": "NETWORK BULLET CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ADC-VDB750", "processAs": "OTHER CAMERA", "description": "CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "GATEWAY-ALTE", "processAs": "OTHER KEYPAD", "description": "GATEWAY KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "GS108PEv3", "processAs": "OTHER RECEIVER", "description": "NETGEAR PROSAFE 8-PORT", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "5890PI or SA5809PI", "processAs": "OTHER SENSOR", "description": "ADEMCO SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "YRD624-ZW3", "processAs": "OTHER SMART LOCK", "description": "SMART LOCK COMBO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "2GIG-SMKT8-345", "processAs": "OTHER SMOKE DETECTOR", "description": "DETECTOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SA5881CC430H", "processAs": "OTHER-RECEIVER", "description": "RECTANGLE WHITE BOX W/ ANTENNAS", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "PGZNG1", "processAs": "PGZNG1-1ADNAS", "description": "ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WHITE FLAT ADT MOUNT", "processAs": "PROWLTOUCH", "description": "PUT ON DISPLAY RACK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "QC3ADTPKC", "processAs": "QC3ADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ANO-L7012R", "processAs": "QNO-8010R", "description": "CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "RE524XC", "processAs": "RE524X", "description": "WIRELESS TRANSLATOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "S40LR0-01-GR", "processAs": "S40LR0-01-GR", "description": "S40 Base Station V4 Lite, Graphite", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "S40LR0-01-PG-R", "processAs": "S40LR0-01-PG-R", "description": "Smart Home Hub - Pearl Gray Refurbished", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "S40LR1-01-CW", "processAs": "S40LR1-01-CW", "description": "Blue Lite Smart Home Hub - Chalk White", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "S40LR1-01-CW-S", "processAs": "S40LR1-01-CW-S", "description": "ADT Self Set Up Smart Home Hub - White", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "S40LR1-01-GR-R", "processAs": "S40LR1-01-GR-R", "description": "Blue Lite Smart Home Hub - Graphite-Refurbished", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "S40LR1-01-PG", "processAs": "S40LR1-01-PG", "description": "Blue Lite Smart Home Hub - Pearl Gray-Refurbished", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "S501R0-01", "processAs": "S501R0-01-WH", "description": "ADT BASE", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SAH5R0-29", "processAs": "SAH5R0-29-WH", "description": "INDOOR SIREN", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SCW9057(G)-433", "processAs": "SCW457HADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WA3000-9.13", "processAs": "SFP3000PCB", "description": "MEMORY BOARD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SASIXC2WA", "processAs": "SIXC2WA", "description": "WIRELESS CONVERTER BOX", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SASIXCTA", "processAs": "SIXCTA", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SASIXFLOODA", "processAs": "SIXFLOODA", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SIXRPTR", "processAs": "SIXRPTRA", "description": "REPEATER (SQUARE BOX)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SIXRPTRA REPEATER", "processAs": "SIXRPTRA", "description": "WIRELESS REPEATER RECTANGLE BOX", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SASIXSHOCK2", "processAs": "SIXSHOCK2A", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SSCO5R0-29", "processAs": "SSCO5R0-29-WH", "description": "carbon monoxide", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SSH5R0-29", "processAs": "SSH5R0-29-WH", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SSHX5R0-29", "processAs": "SSHX5R0-29-WH", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SSM5R0-29", "processAs": "SSM5R0-29-WH", "description": "ADT MOTION SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SSS5R0-29", "processAs": "SSS5R0-29-WH", "description": "smoke detector", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SSSX5R0-29", "processAs": "SSSX5R0-29-WH", "description": "carbon monoxide", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "STS5R0-01", "processAs": "STS5R0-01-WH-PRO", "description": "KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SW-SCM01N", "processAs": "SW-SCM01N", "description": "NOT SET UP IN THE SYSTEM", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "Google sign", "processAs": "T3007ES", "description": "NEST LEARNING THERMOSTAT", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "TP-LINK", "processAs": "TL-PA7017KIT", "description": "ADAPTERS", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "TSSC SERIES - TSSC-KP", "processAs": "TSSKP310021U", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "TSSC SERIES - TSSCBASE", "processAs": "TSSKP311011U", "description": "ADT KEYPAD - LONG SQUARE SHAPE", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "SECURITY UL MODEL 89X0", "processAs": "WLS922L-433", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "AMWLTP100", "processAs": "WLTP100", "description": "SMALL KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WN3000RPHv3", "processAs": "WN3000RPH-3ADPAS", "description": "NETGEAR ADAPTER Wifi Ext", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "W5500-433-ADT", "processAs": "WT5500PADTHE", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WTK5504-433", "processAs": "WTK5504ADT", "description": "SMALL KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "YRD226", "processAs": "YRD226-ZW2-619", "description": "YALE SMART DOOR LOCK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "YRD410-ZW3", "processAs": "YRD410ZW3-619", "description": "SMART LOCK COMBO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "YRD410ZW3", "processAs": "YRD410ZW3-619", "description": "YALE SMART DOOR LOCK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "RFK5501ENG", "processAs": "PK5501", "description": "DSC KEYPAD", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IQPANEL2", "processAs": "QS9201-1208-840", "description": "KEYPAD", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "HONDWA01", "processAs": "HONDWA01", "description": "SMALL SENDSORS", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ECI-T24F2", "processAs": "ECI-T24F2", "description": "OTHER CAMERA", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "OC845", "processAs": "OC845", "description": "CAMERA", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WTS700", "processAs": "WTS700", "description": "KEYPAD", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WLS922L-433", "processAs": "WLS922L-433", "description": "SMART DOOR LOCK", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "RC845", "processAs": "RC845", "description": "CAMERA", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WS4904P", "processAs": "WS4904P", "description": "SENSOR", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "A0WDG-DBCB35", "processAs": "A0WDG-DBCB35", "description": "??", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "99140-023", "processAs": "99140-023", "description": "NICKEL", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "99140-024", "processAs": "99140-024", "description": "BRONZE DARK", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "99140-022", "processAs": "99140-022", "description": "POLISH BRASS", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "WT4911B", "processAs": "WT4911B", "description": "BLUE OVAL/WHITE RECV BOX", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "QW9104-840-RX", "processAs": "QW9104-840-RX", "description": "OLSYS MODELS", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "PG9933", "processAs": "OTHER SMOKE DETECTOR", "description": "DETECTOR", "notes": "ADDED 09/11", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "IQ4HUB / IQPH054", "processAs": "OTHER KEYPAD", "description": "OLSYS KEYPAD MODELS", "notes": "ADDED 09/11", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "ZW4101", "processAs": "OTHER TRANSFORMERS", "description": "JASCO ADAPTER", "notes": "ADDED 09/11", "disposition": "", "dateAdded": datetime.now().isoformat()},
            ]
            
            self._save_mappings(default_mappings)
    
    def _load_mappings(self) -> List[Dict[str, Any]]:
        """Load mappings from data file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Could not load mappings: {e}")
            return []
    
    def _save_mappings(self, mappings: List[Dict[str, Any]]):
        """Save mappings to data file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(mappings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Could not save mappings: {e}")
            raise
    
    def search_mappings(self, query: str) -> List[Dict[str, Any]]:
        """Search for part mappings based on query."""
        if not query or query.strip() == '':
            return []
        
        mappings = self._load_mappings()
        search_term = query.strip().upper()
        
        # Direct matches first
        exact_matches = [
            mapping for mapping in mappings 
            if mapping.get('original', '').upper() == search_term
        ]
        
        if exact_matches:
            return exact_matches
        
        # Partial matches
        partial_matches = [
            mapping for mapping in mappings 
            if (search_term in mapping.get('original', '').upper() or
                search_term in mapping.get('processAs', '').upper() or
                search_term in mapping.get('description', '').upper())
        ]
        
        return partial_matches[:10]  # Limit to 10 results
    
    def get_auto_conversion(self, input_part: str) -> Optional[Dict[str, Any]]:
        """Get automatic conversion for a part number."""
        if not input_part or input_part.strip() == '':
            return None
        
        mappings = self._load_mappings()
        search_term = input_part.strip().upper()
        
        # Look for exact match
        for mapping in mappings:
            if mapping.get('original', '').upper() == search_term:
                return mapping
        
        return None
    
    async def add_mapping(self, original: str, process_as: str, description: str, 
                         notes: str = '', disposition: str = '') -> Dict[str, Any]:
        """Add a new part mapping."""
        mappings = self._load_mappings()
        
        # Check if mapping already exists
        existing = next((m for m in mappings if m.get('original', '').upper() == original.upper()), None)
        if existing:
            raise ValueError(f"Mapping for '{original}' already exists")
        
        new_mapping = {
            'original': original.upper(),
            'processAs': process_as.upper(),
            'description': description,
            'notes': notes,
            'disposition': disposition.upper() if disposition else '',
            'dateAdded': datetime.now().isoformat(),
            'addedBy': 'system'  # Could be enhanced with user tracking
        }
        
        mappings.insert(0, new_mapping)  # Add to beginning
        self._save_mappings(mappings)
        
        self.logger.info(f"Added new part mapping: {original} -> {process_as}")
        return new_mapping
    
    def get_all_mappings(self) -> List[Dict[str, Any]]:
        """Get all part mappings."""
        return self._load_mappings()
    
    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about part mappings."""
        mappings = self._load_mappings()
        
        # Calculate categories
        categories = {}
        dispositions = {}
        
        for mapping in mappings:
            # Categorize by description keywords
            desc = mapping.get('description', '').upper()
            if 'KEYPAD' in desc:
                categories['Keypads'] = categories.get('Keypads', 0) + 1
            elif 'CAMERA' in desc:
                categories['Cameras'] = categories.get('Cameras', 0) + 1
            elif 'SENSOR' in desc:
                categories['Sensors'] = categories.get('Sensors', 0) + 1
            elif 'ROUTER' in desc or 'WIFI' in desc:
                categories['Network'] = categories.get('Network', 0) + 1
            elif 'SMOKE' in desc or 'DETECTOR' in desc:
                categories['Detectors'] = categories.get('Detectors', 0) + 1
            elif 'LOCK' in desc:
                categories['Smart Locks'] = categories.get('Smart Locks', 0) + 1
            else:
                categories['Other'] = categories.get('Other', 0) + 1
            
            # Count dispositions
            disposition = mapping.get('disposition', '') or 'None'
            dispositions[disposition] = dispositions.get(disposition, 0) + 1
        
        return {
            'totalMappings': len(mappings),
            'categories': categories,
            'dispositions': dispositions,
            'lastUpdated': datetime.now().isoformat()
        }
    
    def update_mapping(self, original: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing mapping."""
        mappings = self._load_mappings()
        
        # Find the mapping to update
        for i, mapping in enumerate(mappings):
            if mapping.get('original', '').upper() == original.upper():
                # Update fields
                for key, value in updates.items():
                    if key in ['original', 'processAs', 'description', 'notes', 'disposition']:
                        mapping[key] = value
                
                mapping['lastModified'] = datetime.now().isoformat()
                mappings[i] = mapping
                
                self._save_mappings(mappings)
                self.logger.info(f"Updated mapping for: {original}")
                return mapping
        
        raise ValueError(f"Mapping for '{original}' not found")
    
    def delete_mapping(self, original: str) -> bool:
        """Delete a mapping."""
        mappings = self._load_mappings()
        
        # Find and remove the mapping
        original_count = len(mappings)
        mappings = [m for m in mappings if m.get('original', '').upper() != original.upper()]
        
        if len(mappings) < original_count:
            self._save_mappings(mappings)
            self.logger.info(f"Deleted mapping for: {original}")
            return True
        
        return False
    
    def force_reload_all_mappings(self) -> Dict[str, Any]:
        """Force reload all 121 part mappings from scratch."""
        self.logger.info("Force reloading all 121 part mappings")
        
        # Complete mapping of all 121 entries from reference sheet
        complete_mappings = [
            {"original": "SA5816", "processAs": "5816", "description": "HONEYWELL SENOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "5853", "processAs": "5853", "description": "HONEYWELL SENOR (DO NOT PROCESS FG-1625 AS 5853)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "PROTECTION 1", "processAs": "2GIG-CP21-345E", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "tx id: 013-3285", "processAs": "2GIG-DW10-345", "description": "SMALL WINDOW/DOOR SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "2GIG-GB1", "processAs": "2GIG-GB1-345", "description": "HEAT SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "2GIG-GC2E-ADT", "processAs": "2GIG-GC2E-345", "description": "KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "2GIG-PAD1-345", "processAs": "2GIG-PAD1-345", "description": "2GIG NON TOUCH SECONDARY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "2GIG-PIR1E-345", "processAs": "2GIG-PIR1E-345", "description": "BOX SHAPE SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "2GIG-SMKT3-345", "processAs": "2GIG-SMKT3-345", "description": "smoke detector", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "300-11260", "processAs": "300-10260", "description": "RESIDEO CLASS 2 POWER SUPPLY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "3G4000RF", "processAs": "3G4000RF-ADTUSA", "description": "ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "5800PIR-RES", "processAs": "5800PIR-RES", "description": "HONEYWELL SENOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "60-362N", "processAs": "60-362N-10-319.5", "description": "UTC FIRE & SECURITY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "BP6024", "processAs": "60-670-95R", "description": "UL SENSORS", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SA6150AS-VE", "processAs": "6150ADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SA6150RF-2", "processAs": "6150RF", "description": "HONEYWELL UL KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SA6160PL2", "processAs": "6160PL2", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SA6160RF", "processAs": "6160RFPL2", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SA6160V-4", "processAs": "6160VADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SA6160VPADT", "processAs": "6160VPADT", "description": "ADT (SAFEPASS) KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SIMON XT", "processAs": "80-632-3N-XT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "875936B", "processAs": "875936B", "description": "ADT SECURITY SERVICES", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "????", "processAs": "A-CB7D36PI", "description": "OLD MINI CAMERA - ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "????", "processAs": "A-CB7D60PI", "description": "OLD MINI CAMERA - ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "A-CB7T2812PI", "processAs": "A-CB7T2812PI", "description": "OLD ADT - SMALL HEAD CAMERA W/STAND", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "????", "processAs": "A-CBVD36PI", "description": "OLD MINI CAMERA - ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADC-SVR122", "processAs": "ADC-SVR122-2T", "description": "2TB Hard Drive", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADC-V724", "processAs": "ADC-V724X", "description": "OLD ADT CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADC-VDB105X", "processAs": "ADC-VDB105", "description": "777TS032", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADC-VDB770", "processAs": "ADC-VDB770", "description": "ALARM.COM CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "AMADT2X16LTE-3", "processAs": "ADT2X16AIO-1", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADT5AIO-1", "processAs": "ADT5AIO-2", "description": "NEED TO SET UP -1", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "AMADT7AIO-1", "processAs": "ADT7AIO-1", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "AMADT7AIO-3", "processAs": "ADT7AIO-3", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "AMADT7AIO-5", "processAs": "ADT7AIO-5", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "DS-2CD2123G0", "processAs": "DS-2CD2123G0-I 2.8mm", "description": "HIKVISION camera", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "DS-2CD2143G2-IU", "processAs": "DS-2CD2143G0-I 2.8MM", "description": "HIKVISION", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "DS-7604NI-E1/4P-2T", "processAs": "DS-7604NI-E1/4P-2TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "DS-7604NI-Q1/4P", "processAs": "DS-7604NI-Q1/4P-2TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "DS-7608NI-Q2/8P-2TB", "processAs": "DS-7608NI-Q2/8P-2TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "DS-7608NI-Q2/8P-4TB", "processAs": "DS-7608NI-Q2/8P-4TB", "description": "VIDEO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "EV-DW4927SS", "processAs": "EV-DW4927SS", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "EX3700", "processAs": "EX3700-100NAS", "description": "NETGEAR EXTENDER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "EX6120", "processAs": "EX6120-1ADNAS", "description": "NETGEAR WIFI EXTENDER AC1200", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA00426-US", "description": "NEST HUB MAX - LIGHT GRAY BACK W/STAND", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "H2D", "processAs": "GA00595-US", "description": "Google Nest Wifi Router", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA00638-US", "description": "GOOGLE NEST MINI - CHALK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA00639-US", "description": "NEST HUB MAX (DARK GRAY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA00781-US", "description": "GOOGLE NEST DOORBELL MINI - CHARCOAL", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA01317-US", "description": "GOOGLE NEST CAM G3AL9", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA01318-US", "description": "Google Nest Doorbell (snow)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA01331-US", "description": "GOOGLE NEST HUB MINI (WHITE/GRAY)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "GJQ9T", "processAs": "GA01998-US", "description": "Indoor Google Nest Cam - SMALL HEAD CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA02076-US", "description": "Google Nest Doorbell (Ash, US)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA02411-US", "description": "Google Nest w/ Flood lights", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "GA02767-US", "description": "GOOGLE NEST DOORBELL MINI (COTTON WHITE)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "GS305Pv2", "processAs": "GS305-300PAS", "description": "NETGEAR 5-PORT ETHERNET UNMANAGED", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "HSS301", "processAs": "HSS301-2ADNAS", "description": "ADT NETGEAR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IHUB-3001B-ADT", "processAs": "IHUB-3001B-ADT", "description": "ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IP CAMERA", "processAs": "IPC-HDBW4231E-ADT36", "description": "BUBBLE CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IPC-HFW4120E-ADT36", "processAs": "IPC-HFW4120E-ADT36", "description": "IP CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IQPANEL4", "processAs": "IQP4001", "description": "OLSYS KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IQPANEL4", "processAs": "IQP4001BLK", "description": "OLSYS KEYPAD - BLACK KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "AMAZON SIGN", "processAs": "ISC-BDL2-WP12G", "description": "Amazon Sensor", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Medium Size Amazon Sensor", "processAs": "ISC-BDL2-WP12G", "description": "bosch sensor", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "LYNXPLUS2", "processAs": "L3000", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "LE2077-NA", "processAs": "LE2077-ADTAT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "LE4000RF", "processAs": "LE4000RF-ADTAT", "description": "ADT WIRELESS COMMUNICATOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "LTEL3A", "processAs": "LTEL3A-ADT", "description": "MEMORY BOARD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "LYNXTOUCH2/L5000", "processAs": "LTEL5A-ADT", "description": "HONEYWELL KEYPAD - ON DISPLAY RACK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADEMCO LYNXR-I", "processAs": "LYNXR", "description": "OLD ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "MR70", "processAs": "MR70S-1ADNAS", "description": "NIGHTHAWK MESH WIFI 6 ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "821LMB", "processAs": "MYQ-821LMB", "description": "My Q Garage Bundle box", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "NV412A-ADT", "processAs": "NV412A-ADT", "description": "ETHERNET BLACK BOX", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "51000-601", "processAs": "OTHER C02 DETECTOR", "description": "DETECTOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADC-V515", "processAs": "OTHER CAMERA", "description": "ADT OLDER CAMERA HEAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IPC216A (2.8MM)", "processAs": "OTHER CAMERA", "description": "BUBBLE CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "DS-2CE5AD3T-AVPIT3ZF", "processAs": "OTHER CAMERA", "description": "HIKVISION", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ANBW240", "processAs": "OTHER CAMERA", "description": "NETWORK BULLET CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ADC-VDB750", "processAs": "OTHER CAMERA", "description": "CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "GATEWAY-ALTE", "processAs": "OTHER KEYPAD", "description": "GATEWAY KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "GS108PEv3", "processAs": "OTHER RECEIVER", "description": "NETGEAR PROSAFE 8-PORT", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "5890PI or SA5809PI", "processAs": "OTHER SENSOR", "description": "ADEMCO SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "YRD624-ZW3", "processAs": "OTHER SMART LOCK", "description": "SMART LOCK COMBO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "2GIG-SMKT8-345", "processAs": "OTHER SMOKE DETECTOR", "description": "DETECTOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SA5881CC430H", "processAs": "OTHER-RECEIVER", "description": "RECTANGLE WHITE BOX W/ ANTENNAS", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "PGZNG1", "processAs": "PGZNG1-1ADNAS", "description": "ROUTER", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WHITE FLAT ADT MOUNT", "processAs": "PROWLTOUCH", "description": "PUT ON DISPLAY RACK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "QC3ADTPKC", "processAs": "QC3ADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ANO-L7012R", "processAs": "QNO-8010R", "description": "CAMERA", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "RE524XC", "processAs": "RE524X", "description": "WIRELESS TRANSLATOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "S40LR0-01-GR", "processAs": "S40LR0-01-GR", "description": "S40 Base Station V4 Lite, Graphite", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "S40LR0-01-PG-R", "processAs": "S40LR0-01-PG-R", "description": "Smart Home Hub - Pearl Gray Refurbished", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "S40LR1-01-CW", "processAs": "S40LR1-01-CW", "description": "Blue Lite Smart Home Hub - Chalk White", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "S40LR1-01-CW-S", "processAs": "S40LR1-01-CW-S", "description": "ADT Self Set Up Smart Home Hub - White", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "S40LR1-01-GR-R", "processAs": "S40LR1-01-GR-R", "description": "Blue Lite Smart Home Hub - Graphite-Refurbished", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "S40LR1-01-PG", "processAs": "S40LR1-01-PG", "description": "Blue Lite Smart Home Hub - Pearl Gray-Refurbished", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "S501R0-01", "processAs": "S501R0-01-WH", "description": "ADT BASE", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SAH5R0-29", "processAs": "SAH5R0-29-WH", "description": "INDOOR SIREN", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SCW9057(G)-433", "processAs": "SCW457HADT", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WA3000-9.13", "processAs": "SFP3000PCB", "description": "MEMORY BOARD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SASIXC2WA", "processAs": "SIXC2WA", "description": "WIRELESS CONVERTER BOX", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SASIXCTA", "processAs": "SIXCTA", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SASIXFLOODA", "processAs": "SIXFLOODA", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SIXRPTR", "processAs": "SIXRPTRA", "description": "REPEATER (SQUARE BOX)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SIXRPTRA REPEATER", "processAs": "SIXRPTRA", "description": "WIRELESS REPEATER RECTANGLE BOX", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SASIXSHOCK2", "processAs": "SIXSHOCK2A", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SSCO5R0-29", "processAs": "SSCO5R0-29-WH", "description": "carbon monoxide", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SSH5R0-29", "processAs": "SSH5R0-29-WH", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SSHX5R0-29", "processAs": "SSHX5R0-29-WH", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SSM5R0-29", "processAs": "SSM5R0-29-WH", "description": "ADT MOTION SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SSS5R0-29", "processAs": "SSS5R0-29-WH", "description": "smoke detector", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SSSX5R0-29", "processAs": "SSSX5R0-29-WH", "description": "carbon monoxide", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "STS5R0-01", "processAs": "STS5R0-01-WH-PRO", "description": "KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SW-SCM01N", "processAs": "SW-SCM01N", "description": "NOT SET UP IN THE SYSTEM", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "Google sign", "processAs": "T3007ES", "description": "NEST LEARNING THERMOSTAT", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "TP-LINK", "processAs": "TL-PA7017KIT", "description": "ADAPTERS", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "TSSC SERIES - TSSC-KP", "processAs": "TSSKP310021U", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "TSSC SERIES - TSSCBASE", "processAs": "TSSKP311011U", "description": "ADT KEYPAD - LONG SQUARE SHAPE", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "SECURITY UL MODEL 89X0", "processAs": "WLS922L-433", "description": "SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "AMWLTP100", "processAs": "WLTP100", "description": "SMALL KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WN3000RPHv3", "processAs": "WN3000RPH-3ADPAS", "description": "NETGEAR ADAPTER Wifi Ext", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "W5500-433-ADT", "processAs": "WT5500PADTHE", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WTK5504-433", "processAs": "WTK5504ADT", "description": "SMALL KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "YRD226", "processAs": "YRD226-ZW2-619", "description": "YALE SMART DOOR LOCK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "YRD410-ZW3", "processAs": "YRD410ZW3-619", "description": "SMART LOCK COMBO", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "YRD410ZW3", "processAs": "YRD410ZW3-619", "description": "YALE SMART DOOR LOCK", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "RFK5501ENG", "processAs": "PK5501", "description": "DSC KEYPAD", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IQPANEL2", "processAs": "QS9201-1208-840", "description": "KEYPAD", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "HONDWA01", "processAs": "HONDWA01", "description": "SMALL SENDSORS", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ECI-T24F2", "processAs": "ECI-T24F2", "description": "OTHER CAMERA", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "OC845", "processAs": "OC845", "description": "CAMERA", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WTS700", "processAs": "WTS700", "description": "KEYPAD", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WLS922L-433", "processAs": "WLS922L-433", "description": "SMART DOOR LOCK", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "RC845", "processAs": "RC845", "description": "CAMERA", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WS4904P", "processAs": "WS4904P", "description": "SENSOR", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "A0WDG-DBCB35", "processAs": "A0WDG-DBCB35", "description": "??", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "99140-023", "processAs": "99140-023", "description": "NICKEL", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "99140-024", "processAs": "99140-024", "description": "BRONZE DARK", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "99140-022", "processAs": "99140-022", "description": "POLISH BRASS", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "WT4911B", "processAs": "WT4911B", "description": "BLUE OVAL/WHITE RECV BOX", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "QW9104-840-RX", "processAs": "QW9104-840-RX", "description": "OLSYS MODELS", "notes": "ADDED 09/10", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "PG9933", "processAs": "OTHER SMOKE DETECTOR", "description": "DETECTOR", "notes": "ADDED 09/11", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "IQ4HUB / IQPH054", "processAs": "OTHER KEYPAD", "description": "OLSYS KEYPAD MODELS", "notes": "ADDED 09/11", "disposition": "", "dateAdded": datetime.now().isoformat()},
            {"original": "ZW4101", "processAs": "OTHER TRANSFORMERS", "description": "JASCO ADAPTER", "notes": "ADDED 09/11", "disposition": "", "dateAdded": datetime.now().isoformat()},
        ]
        
        # Force save all mappings
        self._save_mappings(complete_mappings)
        
        self.logger.info(f"Successfully reloaded {len(complete_mappings)} part mappings")
        
        return {
            "count": len(complete_mappings),
            "message": f"Loaded all {len(complete_mappings)} part mappings successfully"
        }
