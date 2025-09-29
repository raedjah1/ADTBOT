// Part Number Mapping Database
// Maps what operators see on units to what should be processed in the system

export const partNumberMappings = [
  // Complete mapping from your reference sheet - EVERY ENTRY
  { original: "SA5816", processAs: "5816", description: "HONEYWELL SENOR", notes: "", disposition: "" },
  { original: "5853", processAs: "5853", description: "HONEYWELL SENOR (DO NOT PROCESS FG-1625 AS 5853)", notes: "", disposition: "" },
  { original: "PROTECTION 1", processAs: "2GIG-CP21-345E", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "tx id: 013-3285", processAs: "2GIG-DW10-345", description: "SMALL WINDOW/DOOR SENSOR", notes: "", disposition: "" },
  { original: "2GIG-GB1", processAs: "2GIG-GB1-345", description: "HEAT SENSOR", notes: "", disposition: "" },
  { original: "2GIG-GC2E-ADT", processAs: "2GIG-GC2E-345", description: "KEYPAD", notes: "", disposition: "" },
  { original: "2GIG-PAD1-345", processAs: "2GIG-PAD1-345", description: "2GIG NON TOUCH SECONDARY", notes: "", disposition: "" },
  { original: "2GIG-PIR1E-345", processAs: "2GIG-PIR1E-345", description: "BOX SHAPE SENSOR", notes: "", disposition: "" },
  { original: "2GIG-SMKT3-345", processAs: "2GIG-SMKT3-345", description: "smoke detector", notes: "", disposition: "" },
  { original: "300-11260", processAs: "300-10260", description: "RESIDEO CLASS 2 POWER SUPPLY", notes: "", disposition: "" },
  { original: "3G4000RF", processAs: "3G4000RF-ADTUSA", description: "ROUTER", notes: "", disposition: "" },
  { original: "5800PIR-RES", processAs: "5800PIR-RES", description: "HONEYWELL SENOR", notes: "", disposition: "" },
  { original: "60-362N", processAs: "60-362N-10-319.5", description: "UTC FIRE & SECURITY", notes: "", disposition: "" },
  { original: "BP6024", processAs: "60-670-95R", description: "UL SENSORS", notes: "", disposition: "" },
  { original: "SA6150AS-VE", processAs: "6150ADT", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "SA6150RF-2", processAs: "6150RF", description: "HONEYWELL UL KEYPAD", notes: "", disposition: "" },
  { original: "SA6160PL2", processAs: "6160PL2", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "SA6160RF", processAs: "6160RFPL2", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "SA6160V-4", processAs: "6160VADT", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "SA6160VPADT", processAs: "6160VPADT", description: "ADT (SAFEPASS) KEYPAD", notes: "", disposition: "" },
  { original: "SIMON XT", processAs: "80-632-3N-XT", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "875936B", processAs: "875936B", description: "ADT SECURITY SERVICES", notes: "", disposition: "" },
  { original: "????", processAs: "A-CB7D36PI", description: "OLD MINI CAMERA - ADT CAMERA HEAD", notes: "", disposition: "" },
  { original: "????", processAs: "A-CB7D60PI", description: "OLD MINI CAMERA - ADT CAMERA HEAD", notes: "", disposition: "" },
  { original: "A-CB7T2812PI", processAs: "A-CB7T2812PI", description: "OLD ADT - SMALL HEAD CAMERA W/STAND", notes: "", disposition: "" },
  { original: "????", processAs: "A-CBVD36PI", description: "OLD MINI CAMERA - ADT CAMERA HEAD", notes: "", disposition: "" },
  { original: "ADC-SVR122", processAs: "ADC-SVR122-2T", description: "2TB Hard Drive", notes: "", disposition: "" },
  { original: "ADC-V724", processAs: "ADC-V724X", description: "OLD ADT CAMERA HEAD", notes: "", disposition: "" },
  { original: "ADC-VDB105X", processAs: "ADC-VDB105", description: "777TS032", notes: "", disposition: "" },
  { original: "ADC-VDB770", processAs: "ADC-VDB770", description: "ALARM.COM CAMERA", notes: "", disposition: "" },
  { original: "AMADT2X16LTE-3", processAs: "ADT2X16AIO-1", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "ADT5AIO-1", processAs: "ADT5AIO-2", description: "NEED TO SET UP -1", notes: "", disposition: "" },
  { original: "AMADT7AIO-1", processAs: "ADT7AIO-1", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "AMADT7AIO-3", processAs: "ADT7AIO-3", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "AMADT7AIO-5", processAs: "ADT7AIO-5", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "DS-2CD2123G0", processAs: "DS-2CD2123G0-I 2.8mm", description: "HIKVISION camera", notes: "", disposition: "" },
  { original: "DS-2CD2143G2-IU", processAs: "DS-2CD2143G0-I 2.8MM", description: "HIKVISION", notes: "", disposition: "" },
  { original: "DS-7604NI-E1/4P-2T", processAs: "DS-7604NI-E1/4P-2TB", description: "VIDEO", notes: "", disposition: "" },
  { original: "DS-7604NI-Q1/4P", processAs: "DS-7604NI-Q1/4P-2TB", description: "VIDEO", notes: "", disposition: "" },
  { original: "DS-7608NI-Q2/8P-2TB", processAs: "DS-7608NI-Q2/8P-2TB", description: "VIDEO", notes: "", disposition: "" },
  { original: "DS-7608NI-Q2/8P-4TB", processAs: "DS-7608NI-Q2/8P-4TB", description: "VIDEO", notes: "", disposition: "" },
  { original: "EV-DW4927SS", processAs: "EV-DW4927SS", description: "SENSOR", notes: "", disposition: "" },
  { original: "EX3700", processAs: "EX3700-100NAS", description: "NETGEAR EXTENDER", notes: "", disposition: "" },
  { original: "EX6120", processAs: "EX6120-1ADNAS", description: "NETGEAR WIFI EXTENDER AC1200", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA00426-US", description: "NEST HUB MAX - LIGHT GRAY BACK W/STAND", notes: "", disposition: "" },
  { original: "H2D", processAs: "GA00595-US", description: "Google Nest Wifi Router", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA00638-US", description: "GOOGLE NEST MINI - CHALK", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA00639-US", description: "NEST HUB MAX (DARK GRAY", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA00781-US", description: "GOOGLE NEST DOORBELL MINI - CHARCOAL", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA01317-US", description: "GOOGLE NEST CAM G3AL9", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA01318-US", description: "Google Nest Doorbell (snow)", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA01331-US", description: "GOOGLE NEST HUB MINI (WHITE/GRAY)", notes: "", disposition: "" },
  { original: "GJQ9T", processAs: "GA01998-US", description: "Indoor Google Nest Cam - SMALL HEAD CAMERA", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA02076-US", description: "Google Nest Doorbell (Ash, US)", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA02411-US", description: "Google Nest w/ Flood lights", notes: "", disposition: "" },
  { original: "Google sign", processAs: "GA02767-US", description: "GOOGLE NEST DOORBELL MINI (COTTON WHITE)", notes: "", disposition: "" },
  { original: "GS305Pv2", processAs: "GS305-300PAS", description: "NETGEAR 5-PORT ETHERNET UNMANAGED", notes: "", disposition: "" },
  { original: "HSS301", processAs: "HSS301-2ADNAS", description: "ADT NETGEAR", notes: "", disposition: "" },
  { original: "IHUB-3001B-ADT", processAs: "IHUB-3001B-ADT", description: "ROUTER", notes: "", disposition: "" },
  { original: "IP CAMERA", processAs: "IPC-HDBW4231E-ADT36", description: "BUBBLE CAMERA", notes: "", disposition: "" },
  { original: "IPC-HFW4120E-ADT36", processAs: "IPC-HFW4120E-ADT36", description: "IP CAMERA", notes: "", disposition: "" },
  { original: "IQPANEL4", processAs: "IQP4001", description: "OLSYS KEYPAD", notes: "", disposition: "" },
  { original: "IQPANEL4", processAs: "IQP4001BLK", description: "OLSYS KEYPAD - BLACK KEYPAD", notes: "", disposition: "" },
  { original: "AMAZON SIGN", processAs: "ISC-BDL2-WP12G", description: "Amazon Sensor", notes: "", disposition: "" },
  { original: "Medium Size Amazon Sensor", processAs: "ISC-BDL2-WP12G", description: "bosch sensor", notes: "", disposition: "" },
  { original: "LYNXPLUS2", processAs: "L3000", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "LE2077-NA", processAs: "LE2077-ADTAT", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "LE4000RF", processAs: "LE4000RF-ADTAT", description: "ADT WIRELESS COMMUNICATOR", notes: "", disposition: "" },
  { original: "LTEL3A", processAs: "LTEL3A-ADT", description: "MEMORY BOARD", notes: "", disposition: "" },
  { original: "LYNXTOUCH2/L5000", processAs: "LTEL5A-ADT", description: "HONEYWELL KEYPAD - ON DISPLAY RACK", notes: "", disposition: "" },
  { original: "ADEMCO LYNXR-I", processAs: "LYNXR", description: "OLD ADT KEYPAD", notes: "", disposition: "" },
  { original: "MR70", processAs: "MR70S-1ADNAS", description: "NIGHTHAWK MESH WIFI 6 ROUTER", notes: "", disposition: "" },
  { original: "821LMB", processAs: "MYQ-821LMB", description: "My Q Garage Bundle box", notes: "", disposition: "" },
  { original: "NV412A-ADT", processAs: "NV412A-ADT", description: "ETHERNET BLACK BOX", notes: "", disposition: "" },
  { original: "51000-601", processAs: "OTHER C02 DETECTOR", description: "DETECTOR", notes: "", disposition: "" },
  { original: "ADC-V515", processAs: "OTHER CAMERA", description: "ADT OLDER CAMERA HEAD", notes: "", disposition: "" },
  { original: "IPC216A (2.8MM)", processAs: "OTHER CAMERA", description: "BUBBLE CAMERA", notes: "", disposition: "" },
  { original: "DS-2CE5AD3T-AVPIT3ZF", processAs: "OTHER CAMERA", description: "HIKVISION", notes: "", disposition: "" },
  { original: "ANBW240", processAs: "OTHER CAMERA", description: "NETWORK BULLET CAMERA", notes: "", disposition: "" },
  { original: "ADC-VDB750", processAs: "OTHER CAMERA", description: "CAMERA", notes: "", disposition: "" },
  { original: "GATEWAY-ALTE", processAs: "OTHER KEYPAD", description: "GATEWAY KEYPAD", notes: "", disposition: "" },
  { original: "GS108PEv3", processAs: "OTHER RECEIVER", description: "NETGEAR PROSAFE 8-PORT", notes: "", disposition: "" },
  { original: "5890PI or SA5809PI", processAs: "OTHER SENSOR", description: "ADEMCO SENSOR", notes: "", disposition: "" },
  { original: "YRD624-ZW3", processAs: "OTHER SMART LOCK", description: "SMART LOCK COMBO", notes: "", disposition: "" },
  { original: "2GIG-SMKT8-345", processAs: "OTHER SMOKE DETECTOR", description: "DETECTOR", notes: "", disposition: "" },
  { original: "SA5881CC430H", processAs: "OTHER-RECEIVER", description: "RECTANGLE WHITE BOX W/ ANTENNAS", notes: "", disposition: "" },
  { original: "PGZNG1", processAs: "PGZNG1-1ADNAS", description: "ROUTER", notes: "", disposition: "" },
  { original: "WHITE FLAT ADT MOUNT", processAs: "PROWLTOUCH", description: "PUT ON DISPLAY RACK", notes: "", disposition: "" },
  { original: "QC3ADTPKC", processAs: "QC3ADT", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "ANO-L7012R", processAs: "QNO-8010R", description: "CAMERA", notes: "", disposition: "" },
  { original: "RE524XC", processAs: "RE524X", description: "WIRELESS TRANSLATOR", notes: "", disposition: "" },
  { original: "S40LR0-01-GR", processAs: "S40LR0-01-GR", description: "S40 Base Station V4 Lite, Graphite", notes: "", disposition: "" },
  { original: "S40LR0-01-PG-R", processAs: "S40LR0-01-PG-R", description: "Smart Home Hub - Pearl Gray Refurbished", notes: "", disposition: "" },
  { original: "S40LR1-01-CW", processAs: "S40LR1-01-CW", description: "Blue Lite Smart Home Hub - Chalk White", notes: "", disposition: "" },
  { original: "S40LR1-01-CW-S", processAs: "S40LR1-01-CW-S", description: "ADT Self Set Up Smart Home Hub - White", notes: "", disposition: "" },
  { original: "S40LR1-01-GR-R", processAs: "S40LR1-01-GR-R", description: "Blue Lite Smart Home Hub - Graphite-Refurbished", notes: "", disposition: "" },
  { original: "S40LR1-01-PG", processAs: "S40LR1-01-PG", description: "Blue Lite Smart Home Hub - Pearl Gray-Refurbished", notes: "", disposition: "" },
  { original: "S501R0-01", processAs: "S501R0-01-WH", description: "ADT BASE", notes: "", disposition: "" },
  { original: "SAH5R0-29", processAs: "SAH5R0-29-WH", description: "INDOOR SIREN", notes: "", disposition: "" },
  { original: "SCW9057(G)-433", processAs: "SCW457HADT", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "WA3000-9.13", processAs: "SFP3000PCB", description: "MEMORY BOARD", notes: "", disposition: "" },
  { original: "SASIXC2WA", processAs: "SIXC2WA", description: "WIRELESS CONVERTER BOX", notes: "", disposition: "" },
  { original: "SASIXCTA", processAs: "SIXCTA", description: "SENSOR", notes: "", disposition: "" },
  { original: "SASIXFLOODA", processAs: "SIXFLOODA", description: "SENSOR", notes: "", disposition: "" },
  { original: "SIXRPTR", processAs: "SIXRPTRA", description: "REPEATER (SQUARE BOX)", notes: "", disposition: "" },
  { original: "SIXRPTRA REPEATER", processAs: "SIXRPTRA", description: "WIRELESS REPEATER RECTANGLE BOX", notes: "", disposition: "" },
  { original: "SASIXSHOCK2", processAs: "SIXSHOCK2A", description: "SENSOR", notes: "", disposition: "" },
  { original: "SSCO5R0-29", processAs: "SSCO5R0-29-WH", description: "carbon monoxide", notes: "", disposition: "" },
  { original: "SSH5R0-29", processAs: "SSH5R0-29-WH", description: "SENSOR", notes: "", disposition: "" },
  { original: "SSHX5R0-29", processAs: "SSHX5R0-29-WH", description: "SENSOR", notes: "", disposition: "" },
  { original: "SSM5R0-29", processAs: "SSM5R0-29-WH", description: "ADT MOTION SENSOR", notes: "", disposition: "" },
  { original: "SSS5R0-29", processAs: "SSS5R0-29-WH", description: "smoke detector", notes: "", disposition: "" },
  { original: "SSSX5R0-29", processAs: "SSSX5R0-29-WH", description: "carbon monoxide", notes: "", disposition: "" },
  { original: "STS5R0-01", processAs: "STS5R0-01-WH-PRO", description: "KEYPAD", notes: "", disposition: "" },
  { original: "SW-SCM01N", processAs: "SW-SCM01N", description: "NOT SET UP IN THE SYSTEM", notes: "", disposition: "" },
  { original: "Google sign", processAs: "T3007ES", description: "NEST LEARNING THERMOSTAT", notes: "", disposition: "" },
  { original: "TP-LINK", processAs: "TL-PA7017KIT", description: "ADAPTERS", notes: "", disposition: "" },
  { original: "TSSC SERIES - TSSC-KP", processAs: "TSSKP310021U", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "TSSC SERIES - TSSCBASE", processAs: "TSSKP311011U", description: "ADT KEYPAD - LONG SQUARE SHAPE", notes: "", disposition: "" },
  { original: "SECURITY UL MODEL 89X0", processAs: "WLS922L-433", description: "SENSOR", notes: "", disposition: "" },
  { original: "AMWLTP100", processAs: "WLTP100", description: "SMALL KEYPAD", notes: "", disposition: "" },
  { original: "WN3000RPHv3", processAs: "WN3000RPH-3ADPAS", description: "NETGEAR ADAPTER Wifi Ext", notes: "", disposition: "" },
  { original: "W5500-433-ADT", processAs: "WT5500PADTHE", description: "ADT KEYPAD", notes: "", disposition: "" },
  { original: "WTK5504-433", processAs: "WTK5504ADT", description: "SMALL KEYPAD", notes: "", disposition: "" },
  { original: "YRD226", processAs: "YRD226-ZW2-619", description: "YALE SMART DOOR LOCK", notes: "", disposition: "" },
  { original: "YRD410-ZW3", processAs: "YRD410ZW3-619", description: "SMART LOCK COMBO", notes: "", disposition: "" },
  { original: "YRD410ZW3", processAs: "YRD410ZW3-619", description: "YALE SMART DOOR LOCK", notes: "", disposition: "" },
  
  // Recently added entries
  { original: "RFK5501ENG", processAs: "PK5501", description: "DSC KEYPAD", notes: "ADDED 09/10", disposition: "" },
  { original: "IQPANEL2", processAs: "QS9201-1208-840", description: "KEYPAD", notes: "ADDED 09/10", disposition: "" },
  { original: "HONDWA01", processAs: "HONDWA01", description: "SMALL SENDSORS", notes: "ADDED 09/10", disposition: "" },
  { original: "ECI-T24F2", processAs: "ECI-T24F2", description: "OTHER CAMERA", notes: "ADDED 09/10", disposition: "" },
  { original: "OC845", processAs: "OC845", description: "CAMERA", notes: "ADDED 09/10", disposition: "" },
  { original: "WTS700", processAs: "WTS700", description: "KEYPAD", notes: "ADDED 09/10", disposition: "" },
  { original: "WLS922L-433", processAs: "WLS922L-433", description: "SMART DOOR LOCK", notes: "ADDED 09/10", disposition: "" },
  { original: "RC845", processAs: "RC845", description: "CAMERA", notes: "ADDED 09/10", disposition: "" },
  { original: "WS4904P", processAs: "WS4904P", description: "SENSOR", notes: "ADDED 09/10", disposition: "" },
  { original: "A0WDG-DBCB35", processAs: "A0WDG-DBCB35", description: "??", notes: "ADDED 09/10", disposition: "" },
  { original: "99140-023", processAs: "99140-023", description: "NICKEL", notes: "ADDED 09/10", disposition: "" },
  { original: "99140-024", processAs: "99140-024", description: "BRONZE DARK", notes: "ADDED 09/10", disposition: "" },
  { original: "99140-022", processAs: "99140-022", description: "POLISH BRASS", notes: "ADDED 09/10", disposition: "" },
  { original: "WT4911B", processAs: "WT4911B", description: "BLUE OVAL/WHITE RECV BOX", notes: "ADDED 09/10", disposition: "" },
  { original: "QW9104-840-RX", processAs: "QW9104-840-RX", description: "OLSYS MODELS", notes: "ADDED 09/10", disposition: "" },
  { original: "PG9933", processAs: "OTHER SMOKE DETECTOR", description: "DETECTOR", notes: "ADDED 09/11", disposition: "" },
  { original: "IQ4HUB / IQPH054", processAs: "OTHER KEYPAD", description: "OLSYS KEYPAD MODELS", notes: "ADDED 09/11", disposition: "" },
  { original: "ZW4101", processAs: "OTHER TRANSFORMERS", description: "JASCO ADAPTER", notes: "ADDED 09/11", disposition: "" }
];

// Helper functions for smart lookup
export const searchPartNumber = (input) => {
  if (!input || input.trim() === '') return [];
  
  const searchTerm = input.trim().toUpperCase();
  
  // Direct matches first
  const exactMatches = partNumberMappings.filter(mapping => 
    mapping.original.toUpperCase() === searchTerm
  );
  
  if (exactMatches.length > 0) {
    return exactMatches;
  }
  
  // Partial matches
  const partialMatches = partNumberMappings.filter(mapping => 
    mapping.original.toUpperCase().includes(searchTerm) ||
    mapping.processAs.toUpperCase().includes(searchTerm) ||
    mapping.description.toUpperCase().includes(searchTerm)
  );
  
  return partialMatches.slice(0, 10); // Limit to 10 results
};

export const getAutoConversion = (input) => {
  if (!input || input.trim() === '') return null;
  
  const searchTerm = input.trim().toUpperCase();
  const exactMatch = partNumberMappings.find(mapping => 
    mapping.original.toUpperCase() === searchTerm
  );
  
  return exactMatch || null;
};

export const addNewPartMapping = async (originalPart, processAsPart, description, notes = '', disposition = '') => {
  // This would typically save to a backend database
  // For now, we'll add it to the local array
  const newMapping = {
    original: originalPart.toUpperCase(),
    processAs: processAsPart.toUpperCase(),
    description: description,
    notes: notes,
    disposition: disposition
  };
  
  partNumberMappings.unshift(newMapping); // Add to beginning
  return newMapping;
};

export const getPartCategories = () => {
  const categories = {};
  
  partNumberMappings.forEach(mapping => {
    const desc = mapping.description.toUpperCase();
    
    if (desc.includes('KEYPAD')) categories['Keypads'] = (categories['Keypads'] || 0) + 1;
    else if (desc.includes('CAMERA')) categories['Cameras'] = (categories['Cameras'] || 0) + 1;
    else if (desc.includes('SENSOR')) categories['Sensors'] = (categories['Sensors'] || 0) + 1;
    else if (desc.includes('ROUTER') || desc.includes('WIFI')) categories['Network'] = (categories['Network'] || 0) + 1;
    else if (desc.includes('SMOKE') || desc.includes('DETECTOR')) categories['Detectors'] = (categories['Detectors'] || 0) + 1;
    else if (desc.includes('LOCK')) categories['Smart Locks'] = (categories['Smart Locks'] || 0) + 1;
    else categories['Other'] = (categories['Other'] || 0) + 1;
  });
  
  return categories;
};