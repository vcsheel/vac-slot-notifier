calendarByDistrict_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
calendarByPin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
cowin_register_url = "https://selfregistration.cowin.gov.in/"
HOST_URL = 'https://vac-slot-notifier.herokuapp.com/'

doses = {1: 'available_capacity_dose1', 2: 'available_capacity_dose2'}
age_groups = {'18-44': 18, '45+': 45, 'Any': None}
dose_types = {'Dose 1': 1, 'Dose 2': 2, 'Any': None}
fee_types = {'Free': 'Free', 'Paid': 'Paid', 'Any': None}
vaccine_types = {'COVISHIELD': 'COVISHIELD', 'COVAXIN': 'COVAXIN', 'SPUTNIK V': 'SPUTNIK V', 'Any': None}
age_group_text = "Select your age group"
state_text = "Select your state"
dist_text = "Select your district"
dose_text = "Select your dose type"
fee_type_text = "Select your vaccine fee"
vaccine_text = "Select your vaccine"
min_slot_text = "Enter your minimum slot requirement"

stop_notification_text = "Notifications have been stopped!!!"
start_notification_text = "/subscribe anytime to start receiving notifications"

blocker_user_error = "Forbidden: bot was blocked by the user"

headers = {"Host": "cdn-api.co-vin.in",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
           "Accept": "*/*",
           "Accept-Language": "en-US,en;q=0.5",
           "Accept-Encoding": "gzip, deflate, br",
           "Connection": "keep-alive",
           "If-None-Match": 'W/"55c5-+0+jAVO44Xga8+gJMO08wQ0POnY"',
           "Cache-Control": 'max-age=0',
           "TE": "Trailers"}


command_list = ["start - Register your preferences",
                "filter - Add filters to your slot search (for eg. dose, vaccine, fee, age group)",
                "slots - Get district slots for next 7 days",
                "details - View your details",
                "subscribe - Subscribe for notifications every minute",
                "unsubscribe - Stop notifications",
                "add - Add a district to your list",
                "remove- Remove a district from your list",
                "lookup - Quick check for slot",
                "delete - Delete you saved data",
                "find_by_pin - Get pincode slots for next 7 days",
                ]

district_map = {
    "adilabad": 582,
    "agar": 320,
    "agatti island": 796,
    "agra": 622,
    "ahmedabad": 154,
    "ahmedabad corporation": 770,
    "ahmednagar": 391,
    "aizawl east": 425,
    "aizawl west": 426,
    "ajmer": 507,
    "akola": 364,
    "alappuzha": 301,
    "aligarh": 623,
    "alipurduar district": 710,
    "alirajpur": 357,
    "almora": 704,
    "alwar": 512,
    "ambala": 193,
    "ambedkar nagar": 625,
    "amethi": 626,
    "amravati": 366,
    "amreli": 174,
    "amritsar": 485,
    "amroha": 627,
    "anand": 179,
    "anantapur": 9,
    "anantnag": 224,
    "angul": 445,
    "anjaw": 22,
    "anuppur": 334,
    "aranthangi": 779,
    "araria": 74,
    "aravalli": 158,
    "ariyalur": 555,
    "arwal": 78,
    "ashoknagar": 354,
    "attur": 578,
    "auraiya": 628,
    "aurangabad": 77,
    "aurangabad ": 397,
    "ayodhya": 646,
    "azamgarh": 629,
    "bbmp": 294,
    "badaun": 630,
    "bagalkot": 270,
    "bageshwar": 707,
    "baghpat": 631,
    "bahraich": 632,
    "baksa": 46,
    "balaghat": 338,
    "balangir": 448,
    "balarampur": 633,
    "balasore": 447,
    "ballia": 634,
    "balod": 110,
    "baloda bazar": 111,
    "balrampur": 112,
    "banaskantha": 159,
    "banda": 635,
    "bandipore": 223,
    "bangalore rural": 276,
    "bangalore urban": 265,
    "banka": 83,
    "bankura": 711,
    "banswara": 519,
    "barabanki": 636,
    "baramulla": 225,
    "baran": 516,
    "bareilly": 637,
    "bargarh": 472,
    "barmer": 528,
    "barnala": 483,
    "barpeta": 47,
    "barwani": 343,
    "basirhat hd (north 24 parganas)": 712,
    "bastar": 113,
    "basti": 638,
    "bathinda": 493,
    "beed": 384,
    "begusarai": 98,
    "belgaum": 264,
    "bellary": 274,
    "bemetara": 114,
    "betul": 362,
    "bhadohi": 687,
    "bhadradri kothagudem": 583,
    "bhadrak": 454,
    "bhagalpur": 82,
    "bhandara": 370,
    "bharatpur": 508,
    "bharuch": 180,
    "bhavnagar": 175,
    "bhavnagar corporation": 771,
    "bhilwara": 523,
    "bhind": 351,
    "bhiwani": 200,
    "bhojpur": 99,
    "bhopal": 312,
    "bidar": 272,
    "bijapur": 115,
    "bijnour": 639,
    "bikaner": 501,
    "bilaspur": 219,
    "birbhum": 713,
    "bishnupur": 398,
    "bishnupur hd (bankura)": 714,
    "biswanath": 765,
    "bokaro": 242,
    "bongaigaon": 57,
    "botad": 176,
    "boudh": 468,
    "budgam": 229,
    "bulandshahr": 640,
    "buldhana": 367,
    "bundi": 514,
    "burhanpur": 342,
    "buxar": 100,
    "coochbehar": 783,
    "cachar": 66,
    "central delhi": 141,
    "chamarajanagar": 271,
    "chamba": 214,
    "chamoli": 699,
    "champawat": 708,
    "champhai": 429,
    "chandauli": 641,
    "chandel": 399,
    "chandigarh": 108,
    "chandrapur": 380,
    "changlang": 20,
    "charaideo": 766,
    "charkhi dadri": 201,
    "chatra": 245,
    "chengalpet": 565,
    "chennai": 571,
    "cheyyar": 778,
    "chhatarpur": 328,
    "chhindwara": 337,
    "chhotaudepur": 181,
    "chikamagalur": 273,
    "chikkaballapur": 291,
    "chirang": 58,
    "chitradurga": 268,
    "chitrakoot": 642,
    "chittoor": 10,
    "chittorgarh": 521,
    "churachandpur": 400,
    "churu": 530,
    "coimbatore": 539,
    "cooch behar": 715,
    "cuddalore": 547,
    "cuttack": 457,
    "dadra and nagar haveli": 137,
    "dahod": 182,
    "dakshin dinajpur": 716,
    "dakshina kannada": 269,
    "daman": 138,
    "damoh": 327,
    "dang": 163,
    "dantewada": 117,
    "darbhanga": 94,
    "darjeeling": 717,
    "darrang": 48,
    "datia": 350,
    "dausa": 511,
    "davanagere": 275,
    "dehradun": 697,
    "deogarh": 473,
    "deoghar": 253,
    "deoria": 643,
    "devbhumi dwaraka": 168,
    "dewas": 324,
    "dhalai": 614,
    "dhamtari": 118,
    "dhanbad": 257,
    "dhar": 341,
    "dharmapuri": 566,
    "dharwad": 278,
    "dhemaji": 62,
    "dhenkanal": 458,
    "dholpur": 524,
    "dhubri": 59,
    "dhule": 388,
    "diamond harbor hd (s 24 parganas)": 718,
    "dibang valley": 25,
    "dibrugarh": 43,
    "dima hasao": 67,
    "dimapur": 434,
    "dindigul": 556,
    "dindori": 336,
    "diu": 139,
    "doda": 232,
    "dumka": 258,
    "dungarpur": 520,
    "durg": 119,
    "east bardhaman": 719,
    "east champaran": 105,
    "east delhi": 145,
    "east garo hills": 424,
    "east godavari": 11,
    "east jaintia hills": 418,
    "east kameng": 23,
    "east khasi hills": 414,
    "east siang": 42,
    "east sikkim": 535,
    "east singhbhum": 247,
    "ernakulam": 307,
    "erode": 563,
    "etah": 644,
    "etawah": 645,
    "faridabad": 199,
    "faridkot": 499,
    "farrukhabad": 647,
    "fatehabad": 196,
    "fatehgarh sahib": 484,
    "fatehpur": 648,
    "fazilka": 487,
    "ferozpur": 480,
    "firozabad": 649,
    "gadag": 280,
    "gadchiroli": 379,
    "gajapati": 467,
    "ganderbal": 228,
    "gandhinagar": 153,
    "gandhinagar corporation": 772,
    "ganjam": 449,
    "garhwa": 243,
    "gariaband": 120,
    "gaurela pendra marwahi ": 136,
    "gautam buddha nagar": 650,
    "gaya": 79,
    "ghaziabad": 651,
    "ghazipur": 652,
    "gir somnath": 177,
    "giridih": 256,
    "goalpara": 60,
    "godda": 262,
    "golaghat": 53,
    "gomati": 615,
    "gonda": 653,
    "gondia": 378,
    "gopalganj": 104,
    "gorakhpur": 654,
    "gulbarga": 267,
    "gumla": 251,
    "guna": 348,
    "guntur": 5,
    "gurdaspur": 489,
    "gurgaon": 188,
    "gwalior": 313,
    "hailakandi": 68,
    "hamirpur": 217,
    "hanumangarh": 517,
    "hapur": 656,
    "harda": 361,
    "hardoi": 657,
    "haridwar": 702,
    "hassan": 289,
    "hathras": 658,
    "haveri": 279,
    "hazaribagh": 255,
    "hingoli": 386,
    "hisar": 191,
    "hojai": 764,
    "hoogly": 720,
    "hoshangabad": 360,
    "hoshiarpur": 481,
    "howrah": 721,
    "hyderabad": 581,
    "idukki": 306,
    "imphal east": 401,
    "imphal west": 402,
    "indore": 314,
    "itanagar capital complex": 17,
    "jabalpur": 315,
    "jagatsinghpur": 459,
    "jagtial": 584,
    "jaipur i": 505,
    "jaipur ii": 506,
    "jaisalmer": 527,
    "jajpur": 460,
    "jalandhar": 492,
    "jalaun": 659,
    "jalgaon": 390,
    "jalna": 396,
    "jalore": 533,
    "jalpaiguri": 722,
    "jammu": 230,
    "jamnagar": 169,
    "jamnagar corporation": 773,
    "jamtara": 259,
    "jamui": 107,
    "jangaon": 585,
    "janjgir-champa": 121,
    "jashpur": 122,
    "jaunpur": 660,
    "jayashankar bhupalpally": 586,
    "jehanabad": 91,
    "jhabua": 340,
    "jhajjar": 189,
    "jhalawar": 515,
    "jhansi": 661,
    "jhargram": 723,
    "jharsuguda": 474,
    "jhunjhunu": 510,
    "jind": 204,
    "jiribam": 410,
    "jodhpur": 502,
    "jogulamba gadwal": 587,
    "jorhat": 54,
    "junagadh": 178,
    "junagadh corporation": 774,
    "kaimur": 80,
    "kaithal": 190,
    "kakching": 413,
    "kalahandi": 464,
    "kalimpong": 724,
    "kallakurichi": 552,
    "kamareddy": 588,
    "kamjong": 409,
    "kamle": 24,
    "kamrup metropolitan": 49,
    "kamrup rural": 50,
    "kanchipuram": 557,
    "kandhamal": 450,
    "kangpokpi": 408,
    "kangra": 213,
    "kanker": 123,
    "kannauj": 662,
    "kannur": 297,
    "kanpur dehat": 663,
    "kanpur nagar": 664,
    "kanyakumari": 544,
    "kapurthala": 479,
    "karaikal": 476,
    "karauli": 525,
    "karbi-anglong": 51,
    "kargil": 309,
    "karimganj": 69,
    "karimnagar": 589,
    "karnal": 203,
    "karur": 559,
    "kasaragod": 295,
    "kasganj": 665,
    "kathua": 234,
    "katihar": 75,
    "katni": 353,
    "kaushambi": 666,
    "kawardha": 135,
    "kendrapara": 461,
    "kendujhar": 455,
    "khagaria": 101,
    "khammam": 590,
    "khandwa": 339,
    "khargone": 344,
    "kheda": 156,
    "khowai": 616,
    "khunti": 252,
    "khurda": 446,
    "kinnaur": 792,
    "kiphire": 444,
    "kishanganj": 76,
    "kishtwar": 231,
    "kodagu": 283,
    "koderma": 241,
    "kohima": 441,
    "kokrajhar": 61,
    "kolar": 277,
    "kolasib": 428,
    "kolhapur": 371,
    "kolkata": 725,
    "kollam": 298,
    "kondagaon": 124,
    "koppal": 282,
    "koraput": 451,
    "korba": 125,
    "koriya": 126,
    "kota": 503,
    "kottayam": 304,
    "kovilpatti": 780,
    "kozhikode": 305,
    "kra daadi": 27,
    "krishna": 4,
    "krishnagiri": 562,
    "kulgam": 221,
    "kullu": 211,
    "kumuram bheem": 591,
    "kupwara": 226,
    "kurnool": 7,
    "kurukshetra": 186,
    "kurung kumey": 21,
    "kushinagar": 667,
    "kutch": 170,
    "lahaul spiti": 210,
    "lakhimpur": 63,
    "lakhimpur kheri": 668,
    "lakhisarai": 84,
    "lakshadweep": 311,
    "lalitpur": 669,
    "latehar": 244,
    "latur": 383,
    "lawngtlai": 432,
    "leh": 310,
    "lepa rada": 33,
    "lohardaga": 250,
    "lohit": 29,
    "longding": 40,
    "longleng": 438,
    "lower dibang valley": 31,
    "lower siang": 18,
    "lower subansiri": 32,
    "lucknow": 670,
    "ludhiana": 488,
    "lunglei": 431,
    "madhepura": 70,
    "madhubani": 95,
    "madurai": 540,
    "mahabubabad": 592,
    "mahabubnagar": 593,
    "maharajganj": 671,
    "mahasamund": 127,
    "mahe": 477,
    "mahendragarh": 206,
    "mahisagar": 183,
    "mahoba": 672,
    "mainpuri": 673,
    "majuli": 767,
    "malappuram": 302,
    "malda": 726,
    "malkangiri": 469,
    "mamit": 427,
    "mancherial": 594,
    "mandi": 215,
    "mandla": 335,
    "mandsaur": 319,
    "mandya": 290,
    "mansa": 482,
    "mathura": 674,
    "mau": 675,
    "mayurbhanj": 456,
    "medak": 595,
    "medchal": 596,
    "meerut": 676,
    "mehsana": 160,
    "mirzapur": 677,
    "moga": 491,
    "mokokchung": 437,
    "mon": 439,
    "moradabad": 678,
    "morbi": 171,
    "morena": 347,
    "morigaon": 55,
    "mulugu": 612,
    "mumbai": 395,
    "mungeli": 128,
    "munger": 85,
    "murshidabad": 727,
    "muzaffarnagar": 679,
    "muzaffarpur": 86,
    "mysore": 266,
    "nabarangpur": 470,
    "nadia": 728,
    "nagaon": 56,
    "nagapattinam": 576,
    "nagarkurnool": 597,
    "nagaur": 532,
    "nagpur": 365,
    "nainital": 709,
    "nalanda": 90,
    "nalbari": 52,
    "nalgonda": 598,
    "namakkal": 558,
    "namsai": 36,
    "nanded": 382,
    "nandigram hd (east medinipore)": 729,
    "nandurbar": 387,
    "narayanpet": 613,
    "narayanpur": 129,
    "narmada": 184,
    "narsinghpur": 352,
    "nashik": 389,
    "navsari": 164,
    "nawada": 92,
    "nayagarh": 462,
    "neemuch": 323,
    "new delhi": 140,
    "nicobar": 3,
    "nilgiris": 577,
    "nirmal": 599,
    "nizamabad": 600,
    "noney": 412,
    "north 24 parganas": 730,
    "north delhi": 146,
    "north east delhi": 147,
    "north garo hills": 423,
    "north goa": 151,
    "north sikkim": 537,
    "north tripura": 617,
    "north west delhi": 143,
    "north and middle andaman": 1,
    "nuapada": 465,
    "nuh": 205,
    "osmanabad": 381,
    "pakke kessang": 19,
    "pakur": 261,
    "palakkad": 308,
    "palamu": 246,
    "palani": 564,
    "palghar": 394,
    "pali": 529,
    "palwal": 207,
    "panchkula": 187,
    "panchmahal": 185,
    "panipat": 195,
    "panna": 326,
    "papum pare": 39,
    "paramakudi": 573,
    "parbhani": 385,
    "paschim medinipore": 731,
    "patan": 161,
    "pathanamthitta": 300,
    "pathankot": 486,
    "patiala": 494,
    "patna": 97,
    "pauri garhwal": 698,
    "peddapalli": 601,
    "perambalur": 570,
    "peren": 435,
    "phek": 443,
    "pherzawl": 411,
    "pilibhit": 680,
    "pithoragarh": 706,
    "poonamallee": 575,
    "poonch": 238,
    "porbandar": 172,
    "prakasam": 12,
    "pratapgarh": 682,
    "prayagraj": 624,
    "puducherry": 475,
    "pudukkottai": 546,
    "pulwama": 227,
    "pune": 363,
    "purba medinipore": 732,
    "puri": 463,
    "purnia": 73,
    "purulia": 733,
    "raebareli": 681,
    "raichur": 284,
    "raigad": 393,
    "raigarh": 130,
    "raipur": 109,
    "raisen": 359,
    "rajanna sircilla": 602,
    "rajgarh": 358,
    "rajkot": 173,
    "rajkot corporation": 775,
    "rajnandgaon": 131,
    "rajouri": 237,
    "rajsamand": 518,
    "ramanagara": 292,
    "ramanathapuram": 567,
    "ramban": 235,
    "ramgarh": 254,
    "rampur": 683,
    "rampurhat hd (birbhum)": 734,
    "ranchi": 240,
    "rangareddy": 603,
    "ranipet": 781,
    "ratlam": 322,
    "ratnagiri": 372,
    "rayagada": 471,
    "reasi": 239,
    "rewa": 316,
    "rewari": 202,
    "ri-bhoi": 417,
    "rohtak": 192,
    "rohtas": 81,
    "rudraprayag": 700,
    "rup nagar": 497,
    "sas nagar": 496,
    "sbs nagar": 500,
    "sabarkantha": 162,
    "sagar": 317,
    "saharanpur": 684,
    "saharsa": 71,
    "sahebganj": 260,
    "salem": 545,
    "samastipur": 96,
    "samba": 236,
    "sambalpur": 452,
    "sambhal": 685,
    "sangareddy": 604,
    "sangli": 373,
    "sangrur": 498,
    "sant kabir nagar": 686,
    "saran": 102,
    "satara": 376,
    "satna": 333,
    "sawai madhopur": 534,
    "sehore": 356,
    "senapati": 403,
    "seoni": 349,
    "sepahijala": 618,
    "seraikela kharsawan": 248,
    "serchhip": 430,
    "shahdara": 148,
    "shahdol": 332,
    "shahjahanpur": 688,
    "shajapur": 321,
    "shamli": 689,
    "sheikhpura": 93,
    "sheohar": 87,
    "sheopur": 346,
    "shi yomi": 35,
    "shimla": 794,
    "shimoga": 287,
    "shivpuri": 345,
    "shopian": 222,
    "shravasti": 690,
    "siaha": 433,
    "siang": 37,
    "siddharthnagar": 691,
    "siddipet": 605,
    "sidhi": 331,
    "sikar": 513,
    "simdega": 249,
    "sindhudurg": 374,
    "singrauli": 330,
    "sirmaur": 212,
    "sirohi": 531,
    "sirsa": 194,
    "sitamarhi": 88,
    "sitapur": 692,
    "sivaganga": 561,
    "sivakasi": 580,
    "sivasagar": 44,
    "siwan": 103,
    "solan": 209,
    "solapur": 375,
    "sonbhadra": 693,
    "sonipat": 198,
    "sonitpur": 64,
    "south 24 parganas": 735,
    "south andaman": 2,
    "south delhi": 149,
    "south east delhi": 144,
    "south garo hills": 421,
    "south goa": 152,
    "south salmara mankachar": 768,
    "south sikkim": 538,
    "south tripura": 619,
    "south west delhi": 150,
    "south west garo hills": 422,
    "south west khasi hills": 415,
    "sri ganganagar": 509,
    "sri muktsar sahib": 490,
    "sri potti sriramulu nellore": 13,
    "srikakulam": 14,
    "srinagar": 220,
    "subarnapur": 466,
    "sukma": 132,
    "sultanpur": 694,
    "sundargarh": 453,
    "supaul": 72,
    "surajpur": 133,
    "surat": 165,
    "surat corporation": 776,
    "surendranagar": 157,
    "surguja": 134,
    "suryapet": 606,
    "tamenglong": 404,
    "tapi": 166,
    "tarn taran": 495,
    "tawang": 30,
    "tehri garhwal": 701,
    "tengnoupal": 407,
    "tenkasi": 551,
    "thane": 392,
    "thanjavur": 541,
    "theni": 569,
    "thiruvananthapuram": 296,
    "thoothukudi (tuticorin)": 554,
    "thoubal": 405,
    "thrissur": 303,
    "tikamgarh": 325,
    "tinsukia": 45,
    "tirap": 26,
    "tiruchirappalli": 560,
    "tirunelveli": 548,
    "tirupattur": 550,
    "tiruppur": 568,
    "tiruvallur": 572,
    "tiruvannamalai": 553,
    "tiruvarur": 574,
    "tonk": 526,
    "tuensang": 440,
    "tumkur": 288,
    "udaipur": 504,
    "udalguri": 65,
    "udham singh nagar": 705,
    "udhampur": 233,
    "udupi": 286,
    "ujjain": 318,
    "ukhrul": 406,
    "umaria": 329,
    "una": 218,
    "unakoti": 620,
    "unnao": 695,
    "upper siang": 34,
    "upper subansiri": 41,
    "uttar dinajpur": 736,
    "uttar kannada": 281,
    "uttarkashi": 703,
    "vadodara": 155,
    "vadodara corporation": 777,
    "vaishali": 89,
    "valsad": 167,
    "varanasi": 696,
    "vellore": 543,
    "vidisha": 355,
    "vijayapura": 293,
    "vikarabad": 607,
    "viluppuram": 542,
    "virudhunagar": 549,
    "visakhapatnam": 8,
    "vizianagaram": 15,
    "wanaparthy": 608,
    "warangal(rural)": 609,
    "warangal(urban)": 610,
    "wardha": 377,
    "washim": 369,
    "wayanad": 299,
    "west bardhaman": 737,
    "west champaran": 106,
    "west delhi": 142,
    "west garo hills": 420,
    "west godavari": 16,
    "west jaintia hills": 416,
    "west kameng": 28,
    "west karbi anglong": 769,
    "west khasi hills": 419,
    "west siang": 38,
    "west sikkim": 536,
    "west singhbhum": 263,
    "west tripura": 621,
    "wokha": 436,
    "ysr district, kadapa (cuddapah)": 6,
    "yadadri bhuvanagiri": 611,
    "yadgir": 285,
    "yamunanagar": 197,
    "yanam": 478,
    "yavatmal": 368,
    "zunheboto": 442
}
