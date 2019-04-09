# -*-coding:utf-8-*- 

import Device
import FingerprintDict
from ICSScanEngine import Utility
import struct

_logger = Utility.ThreadLog('BACNet', 'Device.log')


_vendor_dict = {
  0 : "ASHRAE",
  1 : "NIST",
  2 : "The Trane Company",
  3 : "McQuay International",
  4 : "PolarSoft",
  5 : "Johnson Controls Inc.",
  6 : "American Auto-Matrix",
  7 : "Siemens Schweiz AG (Formerly: Landis & Staefa Division Europe)",
  8 : "Delta Controls",
  9 : "Siemens Schweiz AG",
  10 : "Schneider Electric",
  11 : "TAC",
  12 : "Orion Analysis Corporation",
  13 : "Teletrol Systems Inc.",
  14 : "Cimetrics Technology",
  15 : "Cornell University",
  16 : "United Technologies Carrier",
  17 : "Honeywell Inc.",
  18 : "Alerton / Honeywell",
  19 : "TAC AB",
  20 : "Hewlett-Packard Company",
  21 : "Dorsette.s Inc.",
  22 : "Siemens Schweiz AG (Formerly: Cerberus AG)",
  23 : "York Controls Group",
  24 : "Automated Logic Corporation",
  25 : "CSI Control Systems International",
  26 : "Phoenix Controls Corporation",
  27 : "Innovex Technologies Inc.",
  28 : "KMC Controls Inc.",
  29 : "Xn Technologies Inc.",
  30 : "Hyundai Information Technology Co. Ltd.",
  31 : "Tokimec Inc.",
  32 : "Simplex",
  33 : "North Building Technologies Limited",
  34 : "Notifier",
  35 : "Reliable Controls Corporation",
  36 : "Tridium Inc.",
  37 : "Sierra Monitor Corporation/FieldServer Technologies",
  38 : "Silicon Energy",
  39 : "Kieback & Peter GmbH & Co KG",
  40 : "Anacon Systems Inc.",
  41 : "Systems Controls & Instruments LLC",
  42 : "Lithonia Lighting",
  43 : "Micropower Manufacturing",
  44 : "Matrix Controls",
  45 : "METALAIRE",
  46 : "ESS Engineering",
  47 : "Sphere Systems Pty Ltd.",
  48 : "Walker Technologies Corporation",
  49 : "H I Solutions Inc.",
  50 : "MBS GmbH",
  51 : "SAMSON AG",
  52 : "Badger Meter Inc.",
  53 : "DAIKIN Industries Ltd.",
  54 : "NARA Controls Inc.",
  55 : "Mammoth Inc.",
  56 : "Liebert Corporation",
  57 : "SEMCO Incorporated",
  58 : "Air Monitor Corporation",
  59 : "TRIATEK LLC",
  60 : "NexLight",
  61 : "Multistack",
  62 : "TSI Incorporated",
  63 : "Weather-Rite Inc.",
  64 : "Dunham-Bush",
  65 : "Reliance Electric",
  66 : "LCS Inc.",
  67 : "Regulator Australia PTY Ltd.",
  68 : "Touch-Plate Lighting Controls",
  69 : "Amann GmbH",
  70 : "RLE Technologies",
  71 : "Cardkey Systems",
  72 : "SECOM Co. Ltd.",
  73 : "ABB GebÃ¤etechnik AG Bereich NetServ",
  74 : "KNX Association cvba",
  75 : "Institute of Electrical Installation Engineers of Japan (IEIEJ)",
  76 : "Nohmi Bosai Ltd.",
  77 : "Carel S.p.A.",
  78 : "AirSense Technology Inc.",
  79 : "Hochiki Corporation",
  80 : "Fr. Sauter AG",
  81 : "Matsushita Electric Works Ltd.",
  82 : "Mitsubishi Electric Corporation Inazawa Works",
  83 : "Mitsubishi Heavy Industries Ltd.",
  84 : "ITT Bell & Gossett",
  85 : "Yamatake Building Systems Co. Ltd.",
  86 : "The Watt Stopper Inc.",
  87 : "Aichi Tokei Denki Co. Ltd.",
  88 : "Activation Technologies LLC",
  89 : "Saia-Burgess Controls Ltd.",
  90 : "Hitachi Ltd.",
  91 : "Novar Corp./Trend Control Systems Ltd.",
  92 : "Mitsubishi Electric Lighting Corporation",
  93 : "Argus Control Systems Ltd.",
  94 : "Kyuki Corporation",
  95 : "Richards-Zeta Building Intelligence Inc.",
  96 : "Scientech R&D Inc.",
  97 : "VCI Controls Inc.",
  98 : "Toshiba Corporation",
  99 : "Mitsubishi Electric Corporation Air Conditioning & Refrigeration Systems Works",
  100 : "Custom Mechanical Equipment LLC",
  101 : "ClimateMaster",
  102 : "ICP Panel-Tec Inc.",
  103 : "D-Tek Controls",
  104 : "NEC Engineering Ltd.",
  105 : "PRIVA BV",
  106 : "Meidensha Corporation",
  107 : "JCI Systems Integration Services",
  108 : "Freedom Corporation",
  109 : "Neuberger GebÃ¤eautomation GmbH",
  110 : "Sitronix",
  111 : "Leviton Manufacturing",
  112 : "Fujitsu Limited",
  113 : "Emerson Network Power",
  114 : "S. A. Armstrong Ltd.",
  115 : "Visonet AG",
  116 : "M&M Systems Inc.",
  117 : "Custom Software Engineering",
  118 : "Nittan Company Limited",
  119 : "Elutions Inc. (Wizcon Systems SAS)",
  120 : "Pacom Systems Pty. Ltd.",
  121 : "Unico Inc.",
  122 : "Ebtron Inc.",
  123 : "Scada Engine",
  124 : "AC Technology Corporation",
  125 : "Eagle Technology",
  126 : "Data Aire Inc.",
  127 : "ABB Inc.",
  128 : "Transbit Sp. z o. o.",
  129 : "Toshiba Carrier Corporation",
  130 : "Shenzhen Junzhi Hi-Tech Co. Ltd.",
  131 : "Tokai Soft",
  132 : "Blue Ridge Technologies",
  133 : "Veris Industries",
  134 : "Centaurus Prime",
  135 : "Sand Network Systems",
  136 : "Regulvar Inc.",
  137 : "AFDtek Division of Fastek International Inc.",
  138 : "PowerCold Comfort Air Solutions Inc.",
  139 : "I Controls",
  140 : "Viconics Electronics Inc.",
  141 : "Yaskawa America Inc.",
  142 : "DEOS control systems GmbH",
  143 : "Digitale Mess- und Steuersysteme AG",
  144 : "Fujitsu General Limited",
  145 : "Project Engineering S.r.l.",
  146 : "Sanyo Electric Co. Ltd.",
  147 : "Integrated Information Systems Inc.",
  148 : "Temco Controls Ltd.",
  149 : "Airtek International Inc.",
  150 : "Advantech Corporation",
  151 : "Titan Products Ltd.",
  152 : "Regel Partners",
  153 : "National Environmental Product",
  154 : "Unitec Corporation",
  155 : "Kanden Engineering Company",
  156 : "Messner GebÃ¤etechnik GmbH",
  157 : "Integrated.CH",
  158 : "Price Industries",
  159 : "SE-Elektronic GmbH",
  160 : "Rockwell Automation",
  161 : "Enflex Corp.",
  162 : "ASI Controls",
  163 : "SysMik GmbH Dresden",
  164 : "HSC Regelungstechnik GmbH",
  165 : "Smart Temp Australia Pty. Ltd.",
  166 : "Cooper Controls",
  167 : "Duksan Mecasys Co. Ltd.",
  168 : "Fuji IT Co. Ltd.",
  169 : "Vacon Plc",
  170 : "Leader Controls",
  171 : "Cylon Controls Ltd.",
  172 : "Compas",
  173 : "Mitsubishi Electric Building Techno-Service Co. Ltd.",
  174 : "Building Control Integrators",
  175 : "ITG Worldwide (M) Sdn Bhd",
  176 : "Lutron Electronics Co. Inc.",
  178 : "LOYTEC Electronics GmbH",
  179 : "ProLon",
  180 : "Mega Controls Limited",
  181 : "Micro Control Systems Inc.",
  182 : "Kiyon Inc.",
  183 : "Dust Networks",
  184 : "Advanced Building Automation Systems",
  185 : "Hermos AG",
  186 : "CEZIM",
  187 : "Softing",
  188 : "Lynxspring",
  189 : "Schneider Toshiba Inverter Europe",
  190 : "Danfoss Drives A/S",
  191 : "Eaton Corporation",
  192 : "Matyca S.A.",
  193 : "Botech AB",
  194 : "Noveo Inc.",
  195 : "AMEV",
  196 : "Yokogawa Electric Corporation",
  197 : "GFR Gesellschaft fÃ¼elungstechnik",
  198 : "Exact Logic",
  199 : "Mass Electronics Pty Ltd dba Innotech Control Systems Australia",
  200 : "Kandenko Co. Ltd.",
  201 : "DTF Daten-Technik Fries",
  202 : "Klimasoft Ltd.",
  203 : "Toshiba Schneider Inverter Corporation",
  204 : "Control Applications Ltd.",
  205 : "KDT Systems Co. Ltd.",
  206 : "Onicon Incorporated",
  207 : "Automation Displays Inc.",
  208 : "Control Solutions Inc.",
  209 : "Remsdaq Limited",
  210 : "NTT Facilities Inc.",
  211 : "VIPA GmbH",
  212 : "TSC21 Association of Japan",
  213 : "Strato Automation",
  214 : "HRW Limited",
  215 : "Lighting Control & Design Inc.",
  216 : "Mercy Electronic and Electrical Industries",
  217 : "Samsung SDS Co.Ltd",
  218 : "Impact Facility Solutions Inc.",
  219 : "Aircuity",
  220 : "Control Techniques Ltd.",
  221 : "OpenGeneral Pty. Ltd.",
  222 : "WAGO Kontakttechnik GmbH & Co. KG",
  223 : "Cerus Industrial",
  224 : "Chloride Power Protection Company",
  225 : "Computrols Inc.",
  226 : "Phoenix Contact GmbH & Co. KG",
  227 : "Grundfos Management A/S",
  228 : "Ridder Drive Systems",
  229 : "Soft Device SDN BHD",
  230 : "Integrated Control Technology Limited",
  231 : "AIRxpert Systems Inc.",
  232 : "Microtrol Limited",
  233 : "Red Lion Controls",
  234 : "Digital Electronics Corporation",
  235 : "Ennovatis GmbH",
  236 : "Serotonin Software Technologies Inc.",
  237 : "LS Industrial Systems Co. Ltd.",
  238 : "Square D Company",
  239 : "S Squared Innovations Inc.",
  240 : "Aricent Ltd.",
  241 : "EtherMetrics LLC",
  242 : "Industrial Control Communications Inc.",
  243 : "Paragon Controls Inc.",
  244 : "A. O. Smith Corporation",
  245 : "Contemporary Control Systems Inc.",
  246 : "Intesis Software SL",
  247 : "Ingenieurgesellschaft N. Hartleb mbH",
  248 : "Heat-Timer Corporation",
  249 : "Ingrasys Technology Inc.",
  250 : "Costerm Building Automation",
  251 : "WILO SE",
  252 : "Embedia Technologies Corp.",
  253 : "Technilog",
  254 : "HR Controls Ltd. & Co. KG",
  255 : "Lennox International Inc.",
  256 : "RK-Tec Rauchklappen-Steuerungssysteme GmbH & Co. KG",
  257 : "Thermomax Ltd.",
  258 : "ELCON Electronic Control Ltd.",
  259 : "Larmia Control AB",
  260 : "BACnet Stack at SourceForge",
  261 : "G4S Security Services A/S",
  262 : "Exor International S.p.A.",
  263 : "Cristal Controles",
  264 : "Regin AB",
  265 : "Dimension Software Inc.",
  266 : "SynapSense Corporation",
  267 : "Beijing Nantree Electronic Co. Ltd.",
  268 : "Camus Hydronics Ltd.",
  269 : "Kawasaki Heavy Industries Ltd.",
  270 : "Critical Environment Technologies",
  271 : "ILSHIN IBS Co. Ltd.",
  272 : "ELESTA Energy Control AG",
  273 : "KROPMAN Installatietechniek",
  274 : "Baldor Electric Company",
  275 : "INGA mbH",
  276 : "GE Consumer & Industrial",
  277 : "Functional Devices Inc.",
  278 : "ESAC",
  279 : "M-System Co. Ltd.",
  280 : "Yokota Co. Ltd.",
  281 : "Hitranse Technology Co.LTD",
  282 : "Federspiel Controls",
  283 : "Kele Inc.",
  284 : "Opera Electronics Inc.",
  285 : "Gentec",
  286 : "Embedded Science Labs LLC",
  287 : "Parker Hannifin Corporation",
  288 : "MaCaPS International Limited",
  289 : "Link4 Corporation",
  290 : "Romutec Steuer-u. Regelsysteme GmbH",
  291 : "Pribusin Inc.",
  292 : "Advantage Controls",
  293 : "Critical Room Control",
  294 : "LEGRAND",
  295 : "Tongdy Control Technology Co. Ltd.",
  296 : "ISSARO Integrierte Systemtechnik",
  297 : "Pro-Dev Industries",
  298 : "DRI-STEEM",
  299 : "Creative Electronic GmbH",
  300 : "Swegon AB",
  301 : "Jan Brachacek",
  302 : "Hitachi Appliances Inc.",
  303
  : "Real Time Automation Inc.",
  304 : "ITEC Hankyu-Hanshin Co.",
  305 : "Cyrus E&M Engineering Co. Ltd.",
  306 : "Racine Federated Inc.",
  307 : "Cirrascale Corporation",
  308 : "Elesta GmbH Building Automation",
  309 : "Securiton",
  310 : "OSlsoft Inc.",
  311 : "Hanazeder Electronic GmbH",
  312 : "Honeywell Security DeutschlandNovar GmbH",
  313 : "Siemens Energy & Automation Inc.",
  314 : "ETM Professional Control GmbH",
  315 : "Meitav-tec Ltd.",
  316 : "Janitza Electronics GmbH",
  317 : "MKS Nordhausen",
  318 : "De Gier Drive Systems B.V.",
  319 : "Cypress Envirosystems",
  320 : "SMARTron s.r.o.",
  321 : "Verari Systems Inc.",
  322 : "K-W Electronic Service Inc.",
  323 : "ALFA-SMART Energy Management",
  324 : "Telkonet Inc.",
  325 : "Securiton GmbH",
  326 : "Cemtrex Inc.",
  327 : "Performance Technologies Inc.",
  328 : "Xtralis (Aust) Pty Ltd",
  329 : "TROX GmbH",
  330 : "Beijing Hysine Technology Co.Ltd",
  331 : "RCK Controls Inc.",
  332 : "Distech Controls SAS",
  333 : "Novar/Honeywell",
  334 : "The S4 Group Inc.",
  335 : "Schneider Electric",
  336 : "LHA Systems",
  337 : "GHM engineering Group Inc.",
  338 : "Cllimalux S.A.",
  339 : "VAISALA Oyj",
  340 : "COMPLEX (Beijing) TechnologyCo. Ltd.",
  341 : "SCADAmetrics",
  342 : "POWERPEG NSI Limited",
  343 : "BACnet Interoperability Testing Services Inc.",
  344 : "Teco a.s.",
  345 : "Plexus Technology Inc.",
  346 : "Energy Focus Inc.",
  347 : "Powersmiths International Corp.",
  348 : "Nichibei Co. Ltd.",
  349 : "HKC Technology Ltd.",
  350 : "Ovation Networks Inc.",
  351 : "Setra Systems",
  352 : "AVG Automation",
  353 : "ZXC Ltd.",
  354 : "Byte Sphere",
  355 : "Generiton Co. Ltd.",
  356 : "Holter Regelarmaturen GmbH & Co. KG",
  357 : "Bedford Instruments LLC",
  358 : "Standair Inc.",
  359 : "WEG Automation - R&D",
  360 : "Prolon Control Systems ApS",
  361 : "Inneasoft",
  362 : "ConneXSoft GmbH",
  363 : "CEAG Notlichtsysteme GmbH",
  364 : "Distech Controls Inc.",
  365 : "Industrial Technology Research Institute",
  366 : "ICONICS Inc.",
  367 : "IQ Controls s.c.",
  368 : "OJ Electronics A/S",
  369 : "Rolbit Ltd.",
  370 : "Synapsys Solutions Ltd.",
  371 : "ACME Engineering Prod. Ltd.",
  372 : "Zener Electric Pty Ltd.",
  373 : "Selectronix Inc.",
  374 : "Gorbet & Banerjee LLC.",
  375 : "IME",
  376 : "Stephen H. Dawson Computer Service",
  377 : "Accutrol LLC",
  378 : "Schneider Elektronik GmbH",
  379 : "Alpha-Inno Tec GmbH",
  380 : "ADMMicro Inc.",
  381 : "Greystone Energy Systems Inc.",
  382 : "CAP Technologie",
  383 : "KeRo Systems",
  384 : "Domat Control System s.r.o.",
  385 : "Efektronics Pty. Ltd.",
  386 : "Hekatron Vertriebs GmbH",
  387 : "Securiton AG",
  388 : "Carlo Gavazzi Controls SpA",
  389 : "Chipkin Automation Systems",
  390 : "Savant Systems LLC",
  391 : "Simmtronic Lighting Controls",
  392 : "Abelko Innovation AB",
  393 : "Seresco Technologies Inc.",
  394 : "IT Watchdogs",
  395 : "Automation Assist Japan Corp.",
  396 : "Thermokon Sensortechnik GmbH",
  397 : "EGauge Systems LLC",
  398 : "Quantum Automation (ASIA) PTE Ltd.",
  399 : "Toshiba Lighting & Technology Corp.",
  400 : "SPIN Engenharia de AutomaÃ§ Ltda.",
  401 : "Logistics Systems & Software Services India PVT. Ltd.",
  402 : "Delta Controls Integration Products",
  403 : "Focus Media",
  404 : "LUMEnergi Inc.",
  405 : "Kara Systems",
  406 : "RF Code Inc.",
  407 : "Fatek Automation Corp.",
  408 : "JANDA Software Company LLC",
  409 : "Open System Solutions Limited",
  410 : "Intelec Systems PTY Ltd.",
  411 : "Ecolodgix LLC",
  412 : "Douglas Lighting Controls",
  413 : "iSAtech GmbH",
  414 : "AREAL",
  415 : "Beckhoff Automation GmbH",
  416 : "IPAS GmbH",
  417 : "KE2 Therm Solutions",
  418 : "Base2Products",
  419 : "DTL Controls LLC",
  420 : "INNCOM International Inc.",
  421 : "BTR Netcom GmbH",
  422 : "Greentrol AutomationInc",
  423 : "BELIMO Automation AG",
  424 : "Samsung Heavy Industries CoLtd",
  425 : "Triacta Power Technologies Inc.",
  426 : "Globestar Systems",
  427 : "MLB Advanced MediaLP",
  428 : "SWG Stuckmann Wirtschaftliche GebÃ¤esysteme GmbH",
  429 : "SensorSwitch",
  430 : "Multitek Power Limited",
  431 : "Aquametro AG",
  432 : "LG Electronics Inc.",
  433 : "Electronic Theatre Controls Inc.",
  434 : "Mitsubishi Electric Corporation Nagoya Works",
  435 : "Delta Electronics Inc.",
  436 : "Elma Kurtalj Ltd.",
  437 : "ADT Fire and Security Sp. A.o.o.",
  438 : "Nedap Security Management",
  439 : "ESC Automation Inc.",
  440 : "DSP4YOU Ltd.",
  441 : "GE Sensing and Inspection Technologies",
  442 : "Embedded Systems SIA",
  443 : "BEFEGA GmbH",
  444 : "Baseline Inc.",
  445 : "M2M Systems Integrators",
  446 : "OEMCtrl",
  447 : "Clarkson Controls Limited",
  448 : "Rogerwell Control System Limited",
  449 : "SCL Elements",
  450 : "Hitachi Ltd.",
  451 : "Newron System SA",
  452 : "BEVECO Gebouwautomatisering BV",
  453 : "Streamside Solutions",
  454 : "Yellowstone Soft",
  455 : "Oztech Intelligent Systems Pty Ltd.",
  456 : "Novelan GmbH",
  457 : "Flexim Americas Corporation",
  458 : "ICP DAS Co. Ltd.",
  459 : "CARMA Industries Inc.",
  460 : "Log-One Ltd.",
  461 : "TECO Electric & Machinery Co. Ltd.",
  462 : "ConnectEx Inc.",
  463 : "Turbo DDC SÃ¼",
  464 : "Quatrosense Environmental Ltd.",
  465 : "Fifth Light Technology Ltd.",
  466 : "Scientific Solutions Ltd.",
  467 : "Controller Area Network Solutions (M) Sdn Bhd",
  468 : "RESOL - Elektronische Regelungen GmbH",
  469 : "RPBUS LLC",
  470 : "BRS Sistemas Eletronicos",
  471 : "WindowMaster A/S",
  472 : "Sunlux Technologies Ltd.",
  473 : "Measurlogic",
  474 : "Frimat GmbH",
  475 : "Spirax Sarco",
  476 : "Luxtron",
  477 : "Raypak Inc",
  478 : "Air Monitor Corporation",
  479 : "Regler Och Webbteknik Sverige (ROWS)",
  480 : "Intelligent Lighting Controls Inc.",
  481 : "Sanyo Electric Industry Co.Ltd",
  482 : "E-Mon Energy Monitoring Products",
  483 : "Digital Control Systems",
  484 : "ATI Airtest Technologies Inc.",
  485 : "SCS SA",
  486 : "HMS Industrial Networks AB",
  487 : "Shenzhen Universal Intellisys Co Ltd",
  488 : "EK Intellisys Sdn Bhd",
  489 : "SysCom",
  490 : "Firecom Inc.",
  491 : "ESA Elektroschaltanlagen Grimma GmbH",
  492 : "Kumahira Co Ltd",
  493 : "Hotraco",
  494 : "SABO Elektronik GmbH",
  495 : "Equip'Trans",
  496 : "TCS Basys Controls",
  497 : "FlowCon International A/S",
  498 : "ThyssenKrupp Elevator Americas",
  499 : "Abatement Technologies",
  500 : "Continental Control Systems LLC",
  501 : "WISAG Automatisierungstechnik GmbH & Co KG",
  502 : "EasyIO",
  503 : "EAP-Electric GmbH",
  504 : "Hardmeier",
  505 : "Mircom Group of Companies",
  506 : "Quest Controls",
  507 : "MestekInc",
  508 : "Pulse Energy",
  509 : "Tachikawa Corporation",
  510 : "University of Nebraska-Lincoln",
  511 : "Redwood Systems",
  512 : "PASStec Industrie-Elektronik GmbH",
  513 : "NgEK Inc.",
  514 : "FAW Electronics Ltd",
  515 : "Jireh Energy Tech Co. Ltd.",
  516 : "Enlighted Inc.",
  517 : "El-Piast Sp. Z o.o",
  518 : "NetxAutomation Software GmbH",
  519 : "Invertek Drives",
  520 : "Deutschmann Automation GmbH & Co. KG",
  521 : "EMU Electronic AG",
  522 : "Phaedrus Limited",
  523 : "Sigmatek GmbH & Co KG",
  524 : "Marlin Controls",
  525 : "CircutorSA",
  526 : "UTC Fire & Security",
  527 : "DENT Instruments Inc.",
  528 : "FHP Manufacturing Company - Bosch Group",
  529 : "GE Intelligent Platforms",
  530 : "Inner Range Pty Ltd",
  531 : "GLAS Energy Technology",
  532 : "MSR-Electronic-GmbH",
  533 : "Energy Control Systems Inc.",
  534 : "EMT Controls",
  535 : "Daintree Networks Inc.",
  536 : "EURO ICC d.o.o",
  537 : "TE Connectivity Energy",
  538 : "GEZE GmbH",
  539 : "NEC Corporation",
  540 : "Ho Cheung International Company Limited",
  541 : "Sharp Manufacturing Systems Corporation",
  542 : "DOT CONTROLS a.s.",
  543 : "BeaconMedÃ¦0220",
  544 : "Midea Commercial Aircon",
  545 : "WattMaster Controls",
  546 : "Kamstrup A/S",
  547 : "CA Computer Automation GmbH",
  548 : "Laars Heating Systems Company",
  549 : "Hitachi Systems Ltd.",
  550 : "Fushan AKE Electronic Engineering Co. Ltd.",
  551 : "Toshiba International Corporation",
  552 : "Starman Systems LLC",
  553 : "Samsung Techwin Co. Ltd.",
  554 : "ISAS-Integrated Switchgear and Systems P/L",
  556 : "Obvius",
  557 : "Marek Guzik",
  558 : "Vortek Instruments LLC",
  559 : "Universal Lighting Technologies",
  560 : "Myers Power Products Inc.",
  561 : "Vector Controls GmbH",
  562 : "Crestron Electronics Inc.",
  563 : "A&E Controls Limited",
  564 : "Projektomontaza A.D.",
  565 : "Freeaire Refrigeration",
  566 : "Aqua Cooler Pty Limited",
  567 : "Basic Controls",
  568 : "GE Measurement and Control Solutions Advanced Sensors",
  569 : "EQUAL Networks",
  570 : "Millennial Net",
  571 : "APLI Ltd",
  572 : "Electro Industries/GaugeTech",
  573 : "SangMyung University",
  574 : "Coppertree Analytics Inc.",
  575 : "CoreNetiX GmbH",
  576 : "Acutherm",
  577 : "Dr. Riedel Automatisierungstechnik GmbH",
  578 : "Shina System Co.Ltd",
  579 : "Iqapertus",
  580 : "PSE Technology",
  581 : "BA Systems",
  582 : "BTICINO",
  583 : "Monico Inc.",
  584 : "iCue",
  585 : "tekmar Control Systems Ltd.",
  586 : "Control Technology Corporation",
  587 : "GFAE GmbH",
  588 : "BeKa Software GmbH",
  589 : "Isoil Industria SpA",
  590 : "Home Systems Consulting SpA",
  591 : "Socomec",
  592 : "Everex Communications Inc.",
  593 : "Ceiec Electric Technology",
  594 : "Atrila GmbH",
  595 : "WingTechs",
  596 : "Shenzhen Mek Intellisys Pte Ltd.",
  597 : "Nestfield Co. Ltd.",
  598 : "Swissphone Telecom AG",
  599 : "PNTECH JSC",
  600 : "Horner APG LLC",
  601 : "PVI Industries LLC",
  602 : "Ela-compil",
  603 : "Pegasus Automation International LLC",
  604 : "Wight Electronic Services Ltd.",
  605 : "Marcom",
  606 : "Exhausto A/S",
  607 : "Dwyer Instruments Inc.",
  608 : "Link GmbH",
  609 : "Oppermann Regelgerate GmbH",
  610 : "NuAire Inc.",
  611 : "Nortec Humidity Inc.",
  612 : "Bigwood Systems Inc.",
  613 : "Enbala Power Networks",
  614 : "Inter Energy Co. Ltd.",
  615 : "ETC",
  616 : "COMELEC S.A.R.L",
  617 : "Pythia Technologies",
  618 : "TrendPoint Systems Inc.",
  619 : "AWEX",
  620 : "Eurevia",
  621 : "Kongsberg E-lon AS",
  622 : "FlaktWoods",
  623 : "E + E Elektronik GES M.B.H.",
  624 : "ARC Informatique",
  625 : "SKIDATA AG",
  626 : "WSW Solutions",
  627 : "Trefon Electronic GmbH",
  628 : "Dongseo System",
  629 : "Kanontec Intelligence Technology Co. Ltd.",
  630 : "EVCO S.p.A.",
  631 : "Accuenergy (CANADA) Inc.",
  632 : "SoftDEL",
  633 : "Orion Energy Systems Inc.",
  634 : "Roboticsware",
  635 : "DOMIQ Sp. z o.o.",
  636 : "Solidyne",
  637 : "Elecsys Corporation",
  638 : "Conditionaire International Pty. Limited",
  639 : "Quebec Inc.",
  640 : "Homerun Holdings",
  641 : "RFM Inc.",
  642 : "Comptek",
  643 : "Westco Systems Inc.",
  644 : "Advancis Software & Services GmbH",
  645 : "Intergrid LLC",
  646 : "Markerr Controls Inc.",
  647 : "Toshiba Elevator and Building Systems Corporation",
  648 : "Spectrum Controls Inc.",
  649 : "Mkservice",
  650 : "Fox Thermal Instruments",
  651 : "SyxthSense Ltd",
  652 : "DUHA System S R.O.",
  653 : "NIBE",
  654 : "Melink Corporation",
  655 : "Fritz-Haber-Institut",
  656 : "MTU Onsite Energy GmbHGas Power Systems",
  657 : "Omega Engineering Inc.",
  658 : "Avelon",
  659 : "Ywire Technologies Inc.",
  660 : "M.R. Engineering Co. Ltd.",
  661 : "Lochinvar LLC",
  662 : "Sontay Limited",
  663 : "GRUPA Slawomir Chelminski",
  664 : "Arch Meter Corporation",
  665 : "Senva Inc.",
  667 : "FM-Tec",
  668 : "Systems Specialists Inc.",
  669 : "SenseAir",
  670 : "AB IndustrieTechnik Srl",
  671 : "Cortland Research LLC",
  672 : "MediaView",
  673 : "VDA Elettronica",
  674 : "CSS Inc.",
  675 : "Tek-Air Systems Inc.",
  676 : "ICDT",
  677 : "The Armstrong Monitoring Corporation",
  678 : "DIXELL S.r.l",
  679 : "Lead System Inc.",
  680 : "ISM EuroCenter S.A.",
  681 : "TDIS",
  682 : "Trade FIDES",
  683 : "KnÃ¼bH (Emerson Network Power)",
  684 : "Resource Data Management",
  685 : "Abies Technology Inc.",
  686 : "Amalva",
  687 : "MIRAE Electrical Mfg. Co. Ltd.",
  688 : "HunterDouglas Architectural Projects Scandinavia ApS",
  689 : "RUNPAQ Group Co.Ltd",
  690 : "Unicard SA",
  691 : "IE Technologies",
  692 : "Ruskin Manufacturing",
  693 : "Calon Associates Limited",
  694 : "Contec Co. Ltd.",
  695 : "iT GmbH",
  696 : "Autani Corporation",
  697 : "Christian Fortin",
  698 : "HDL",
  699 : "IPID Sp. Z.O.O Limited",
  700 : "Fuji Electric Co.Ltd",
  701 : "View Inc.",
  702 : "Samsung S1 Corporation",
  703 : "New Lift",
  704 : "VRT Systems",
  705 : "Motion Control Engineering Inc.",
  706 : "Weiss Klimatechnik GmbH",
  707 : "Elkon",
  708 : "Eliwell Controls S.r.l.",
  709 : "Japan Computer Technos Corp",
  710 : "Rational Network ehf",
  711 : "Magnum Energy Solutions LLC",
  712 : "MelRok",
  713 : "VAE Group",
  714 : "LGCNS",
  715 : "Berghof Automationstechnik GmbH",
  716 : "Quark Communications Inc.",
  717 : "Sontex",
  718 : "mivune AG",
  719 : "Panduit",
  720 : "Smart Controls LLC",
  721 : "Compu-Aire Inc.",
  722 : "Sierra",
  723 : "ProtoSense Technologies",
  724 : "Eltrac Technologies Pvt Ltd",
  725 : "Bektas Invisible Controls GmbH",
  726 : "Entelec",
  727 : "Innexiv",
  728 : "Covenant"
}


class _Requests:
    # 各种请求的消息码流
    # 末位79表示请求vendor name,  78表示请求vendor id
    query_vendor_by_id = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF1978')
    query_vendor_by_name = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF1979')
    query_firmware = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF192c')
    query_appsoft = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF190c')
    query_object = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF194d')
    query_model = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF1946')
    query_desc = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF191c')
    # 查询位置码流
    query_location = Utility.Common.pack_from_str('810a001101040005010c0c023FFFFF193A')
    # 查询bbmd码流
    query_bbmd = Utility.Common.pack_from_str('81020004')
    # 查询fdt码流
    query_fdt = Utility.Common.pack_from_str('81060004')


# 元素标志位
class _Element:
    # 空字节
    flag_null = '\x00'
    # 字节位标识
    flag_error = '\x50'
    # offset=15
    flag_vendor_id = '\x78'
    flag_vendor_name = '\x79'
    # offset=17
    flag_vendor_id_byte = '\x21'    # ID占用一个字节
    flag_vendor_id_short = '\x22'   # ID占用两个字节
    # offset=15
    flag_firmware_revision = '\x2c'
    flag_app_soft_version = '\x0c'
    flag_model = '\x46'
    flag_description = '\x1c'
    flag_location = '\x3a'
    flag_object = '\x4d'

    # function码
    flag_bbmd = '\x03'
    flag_fdt = '\x07'

    # 响应消息解析状态标志
    NORMAL_RESPONSE = 0
    ERROR_RESPONSE = -1
    UNKNOWN_RESPONSE = 99


# 获取read_broadcast_distribution_table_ack内容
# 抓取 bbmd 响应信息，是一个列表
def _read_broadcast_distribution_table_ack(response):
    # 获取列表
    result = None
    try:
        if not response or response[1] != _Element.flag_bbmd:
            return None

        # 获取长度
        length = struct.unpack_from('>H', response, 2)[0]
        if length < 14:
            return None
        for offset in range(0, length, 14):
            ips = struct.unpack_from('4B', response, 3+offset)
            port, mask = struct.unpack_from('>HI', response,7+offset)
            # ip, port, mask = struct.unpack_from('')
            if not result:
                result = '[IP]%u.%u.%u.%u:%u [Mask]%X' % (ips[0], ips[1], ips[2], ips[3], port, mask)
            else:
                result += ',[IP]%u.%u.%u.%u:%u [Mask]%X' % (ips[0], ips[1], ips[2], ips[3], port, mask)
    except:
        pass

    return result


def _read_foreign_device_table_ack(response):
    # 获取列表
    result = None
    try:
        if not response or response[1] != _Element.flag_fdt:
            return None

        # 获取长度
        length = struct.unpack_from('>H', response, 2)[0]
        if length < 10:
            return None
        for offset in range(0, length, 10):
            ips = struct.unpack_from('4B', response, 3+offset)
            port, ttl, timeout = struct.unpack_from('>3H', response, 7+offset)
            # ip, port, mask = struct.unpack_from('')
            if not result:
                result = '[IP]%u.%u.%u.%u:%u [TTL]%u [Timeout]%u' % (ips[0], ips[1], ips[2], ips[3], port, ttl, timeout)
            else:
                result += ',[IP]%u.%u.%u.%u:%u [TTL]%u [Timeout]%u' % (ips[0], ips[1], ips[2], ips[3], port, ttl, timeout)
    except:
        pass

    return result


class BACNetDevice(Device.UDPDevice):
    DEFAULT_PORTS = [47808, ]
    PROTOCOL_NAME = 'BACnet'

    def __init__(self, ip, port=DEFAULT_PORTS[0]):
        super(BACNetDevice, self).__init__(ip, port)
        self.protocol = self.PROTOCOL_NAME
        self.instance_number = 0
        # 需要通过代理，源端口和响应端口都为47808
        self.src_port = port
        self.rsp_port = port

    def __str__(self):
        return self.fingerprint
        # return '类型=%s\n产商=%s\n型号=%s\n版本=%s' % (self.type, self.vendor, self.model, self.version)

    # 校验是否合法的BACNet响应报文
    def _check_response(self, response):
      try:
        # 不是标准的BACNet响应报文，或者不是本IP端口的响应
        if not response or not response.startswith('\x81'):
          return _Element.UNKNOWN_RESPONSE
        else:
          # 正常响应报文
          if response[6] is not _Element.flag_error:
            return _Element.NORMAL_RESPONSE
          # 错误响应报文
          else:
            return _Element.ERROR_RESPONSE
      # 异常场景下，返回未知消息
      except:
        return _Element.UNKNOWN_RESPONSE

    # 校验返回结果
    def request_bacnet(self, request_data):
        response = self.request_through_proxy(request_data)
        result = self._check_response(response)
        # error报文直接返回，由解析程序解析，此种情况下，判断对端仍然是BACNet设备，只是相关信息会获取失败
        if result in(_Element.NORMAL_RESPONSE, _Element.ERROR_RESPONSE):
            return response
        else:
            return False

    # 获取vendor id和设备id
    def _get_vendor_id(self):
        vendor_response = self.request_bacnet(_Requests.query_vendor_by_id)
        # 获取name报文异常，直接返回false
        if not vendor_response:
            return None

        # 解析vendor name
        try:
            # 如果是标志位方式
            if vendor_response[15] == _Element.flag_vendor_id:
                # 后续一个字节为厂商标识
                if vendor_response[17] == _Element.flag_vendor_id_byte:
                    vendor_id = struct.unpack_from('B', vendor_response, 18)[0]
                    self.vendor = _vendor_dict.get(int(vendor_id), '')
                # 后续两个字节为厂商标识，大端
                elif vendor_response[17] == _Element.flag_vendor_id_short:
                    vendor_id = struct.unpack_from('>H', vendor_response, 18)[0]
                    self.vendor = _vendor_dict.get(int(vendor_id), '')
                else:
                    pass
                # 从第11个字节开始，后面4个字节包含instance number
                # 前面10个bit位是device类型,后面22个bit是instance number
                self.instance_number = struct.unpack_from('>I', vendor_response, 10)[0] & 4194303
        except:
            pass

        return True

    # 获取第29个字节开始的字符串长度
    def _get_name(self, request, response_type):
        # 发送请求消息码流，获取响应消息
        model_response = self.request_bacnet(request)
        if not model_response:
            return None

        try:
            # 第16个字节位是标志位，判断是否符合预期
            if model_response[15] == response_type:
                # 第19个字节位是字符串长度
                length = struct.unpack_from('B', model_response, 18)[0]
                # 从第30个字节位开始获取字符串
                return Utility.Common.get_string(model_response, 19, length)
        except:
            return None

    # 获取设备指纹
    def get_identity(self):
        # flag = False
        # 获取厂商等信息，只有任意有效的协议报文，则返回True
        # result = self._get_name(_Requests.query_vendor_by_name, _Element.flag_vendor_name)
        # if result is not None:
        #     self.vendor = result
        #     flag = True
        # 获取vendor id失败直接返回False
        self.fingerprint = ''
        result = self._get_vendor_id()
        if not result:
            return False

        # self.type = 'BACNetIP设备'
        self.fingerprint += "设备厂商:{}\n设备编号:{}".format(self.vendor, self.instance_number)

        # 获取Model
        # print self.model
        result = self._get_name(_Requests.query_model, _Element.flag_model)
        if result:
            self.model = result
            self.fingerprint += "\n设备型号:{}".format(self.model)

        # 获取software version
        result = self._get_name(_Requests.query_appsoft, _Element.flag_app_soft_version)
        if result:
            self.version = result
            self.fingerprint += "\n软件版本:{}".format(self.version)

        # 获取object
        result = self._get_name(_Requests.query_object, _Element.flag_object)
        if result:
            self.fingerprint += "\n对象名称:{}".format(result)

        # 获取firmware
        result = self._get_name(_Requests.query_firmware, _Element.flag_firmware_revision)
        if result:
            self.version = result
            self.fingerprint += "\n固件版本:{}".format(result)

        # 获取detail
        result = self._get_name(_Requests.query_desc, _Element.flag_description)
        if result:
            self.fingerprint += "\n设备描述:{}".format(result)

        # 获取location
        result = self._get_name(_Requests.query_location, _Element.flag_location)
        if result:
            self.fingerprint += "\n设备位置:{}".format(result)

        # 获取BBMD
        response = self.request_bacnet(_Requests.query_bbmd)
        result = _read_broadcast_distribution_table_ack(response)
        if result:
            self.fingerprint += "\nBBMD:{}".format(result)

        # 获取FDT
        response = self.request_bacnet(_Requests.query_fdt)
        result = _read_foreign_device_table_ack(response)
        if result:
            self.fingerprint += "\nFDT:{}".format(result)

        self.detail = '{}'.format(self.ip)

        # 匹配指纹
        results = FingerprintDict.GenericFingerprintDict.match(self.fingerprint)
        if results:
            self.type = results[0]
            self.vendor = results[1]
            self.model = results[2]
        # 默认的设备类型
        else:
            self.type = FingerprintDict.TYPE_WEB_SCADA
        self.type = '智能楼宇控制器'
        return True


def scan(ip, port):
    """扫描BACNet PLC设备，成功则返回BACNetDevice对象，否则返回None"""
    device = BACNetDevice(ip, port)
    result = None
    for i in range(device.retry):
        try:
            if device.get_identity():
                result = device
                break
        except:
            pass

    device.release_proxy()
    return result


if __name__ == '__main__':
    import time

    start = time.time()
    device = scan('211.217.185.132', 47808)
    print device
    #print 'cost:', time.time() - start

    # count = 0
    # while count < 0:
    #   count += 1
    #   start = time.time()
    #   device = scan('101.37.78.224', 47808)
    #   print device
    #   print '*'*200
    #   print 'cost:', time.time() - start
    #
    #   start = time.time()
    #   device = scan('164.52.229.11', 47808)
    #   print device
    #   print 'cost:', time.time() - start

