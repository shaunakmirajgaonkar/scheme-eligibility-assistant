"""
schemes_data.py
Local, offline database of Indian public-benefit schemes.
No internet connection or external API required.
Edit / extend this list to add more schemes.
"""

SCHEMES = [
    {
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "category": "Agriculture",
        "description": "Income support of Rs. 6,000/year to small and marginal farmer families, paid in 3 installments.",
        "criteria": {
            "occupation": ["farmer"],
            "land_owner": [True],
            "max_income": None,
        },
        "documents": [
            "Aadhaar Card",
            "Land ownership papers / Records of Rights (RoR)",
            "Bank account passbook (linked to Aadhaar)",
            "Passport-size photograph",
        ],
        "benefit": "Rs. 6,000 per year in 3 equal installments directly to bank account",
        "apply_mode": "Online via pmkisan.gov.in or nearest Common Service Centre (CSC)",
    },
    {
        "name": "Ayushman Bharat - PM Jan Arogya Yojana (PM-JAY)",
        "category": "Health",
        "description": "Health insurance cover of Rs. 5 lakh per family per year for secondary and tertiary hospitalization.",
        "criteria": {
            "max_income": 250000,
            "bpl_card": [True, None],
        },
        "documents": [
            "Aadhaar Card",
            "Ration Card / BPL Card",
            "Income Certificate",
            "Family ID / SECC database entry (if applicable)",
        ],
        "benefit": "Cashless health cover up to Rs. 5,00,000 per family per year",
        "apply_mode": "Common Service Centre (CSC), empanelled hospital, or setu.pmjay.gov.in",
    },
    {
        "name": "Pradhan Mantri Awas Yojana (PMAY) - Urban/Gramin",
        "category": "Housing",
        "description": "Financial assistance for construction/purchase of a house for economically weaker sections.",
        "criteria": {
            "max_income": 300000,
            "owns_pucca_house": [False],
        },
        "documents": [
            "Aadhaar Card",
            "Income Certificate",
            "Certificate stating no pucca house owned",
            "Bank account details",
            "Passport-size photograph",
        ],
        "benefit": "Subsidy up to Rs. 2.67 lakh on home loan interest / direct assistance for construction",
        "apply_mode": "Online via pmaymis.gov.in or through local municipal office",
    },
    {
        "name": "National Scholarship Portal - Post-Matric Scholarship",
        "category": "Education",
        "description": "Financial assistance to students from SC/ST/OBC/minority/EWS backgrounds studying post-matriculation.",
        "criteria": {
            "is_student": [True],
            "max_income": 250000,
            "min_age": 13,
            "max_age": 35,
        },
        "documents": [
            "Aadhaar Card",
            "Caste Certificate (if applicable)",
            "Income Certificate",
            "Previous year mark sheet",
            "Bonafide/Admission certificate from institution",
            "Bank account passbook",
        ],
        "benefit": "Tuition fee reimbursement + maintenance allowance (amount varies by state/category)",
        "apply_mode": "Online via scholarships.gov.in",
    },
    {
        "name": "Pradhan Mantri Ujjwala Yojana (PMUY)",
        "category": "Household",
        "description": "Free LPG gas connection to women from Below Poverty Line (BPL) households.",
        "criteria": {
            "gender": ["female"],
            "bpl_card": [True],
            "min_age": 18,
        },
        "documents": [
            "Aadhaar Card",
            "BPL Ration Card",
            "Bank account passbook",
            "Passport-size photograph",
            "Address proof",
        ],
        "benefit": "Free LPG connection with first refill and stove, subsidy on subsequent refills",
        "apply_mode": "Nearest LPG distributor or pmuy.gov.in",
    },
    {
        "name": "Atal Pension Yojana (APY)",
        "category": "Pension",
        "description": "Guaranteed minimum pension scheme for workers in the unorganized sector.",
        "criteria": {
            "min_age": 18,
            "max_age": 40,
            "has_bank_account": [True],
        },
        "documents": [
            "Aadhaar Card",
            "Bank account passbook",
            "Mobile number linked to bank account",
        ],
        "benefit": "Guaranteed monthly pension of Rs. 1,000 to Rs. 5,000 after age 60",
        "apply_mode": "Through any bank branch or post office offering APY",
    },
    {
        "name": "Pradhan Mantri Mudra Yojana (PMMY)",
        "category": "Employment/Business",
        "description": "Collateral-free loans up to Rs. 10 lakh for non-corporate, non-farm small/micro enterprises.",
        "criteria": {
            "occupation": ["self-employed", "business_owner", "unemployed"],
            "min_age": 18,
        },
        "documents": [
            "Aadhaar Card",
            "PAN Card",
            "Business plan / proof of existing business",
            "Bank account statement",
            "Passport-size photograph",
        ],
        "benefit": "Loans categorized as Shishu (up to Rs 50,000), Kishor (up to Rs 5 lakh), Tarun (up to Rs 10 lakh)",
        "apply_mode": "Any nationalized bank, RRB, or online via mudra.org.in",
    },
    {
        "name": "National Old Age Pension Scheme (NOAPS/IGNOAPS)",
        "category": "Pension",
        "description": "Monthly pension for elderly citizens living below the poverty line.",
        "criteria": {
            "min_age": 60,
            "bpl_card": [True],
        },
        "documents": [
            "Aadhaar Card",
            "Age proof",
            "BPL Certificate",
            "Bank/Post office account details",
        ],
        "benefit": "Monthly pension (amount varies by state, typically Rs. 200-1000+)",
        "apply_mode": "District Social Welfare Office or state e-Governance portal",
    },
    {
        "name": "Pradhan Mantri Matru Vandana Yojana (PMMVY)",
        "category": "Maternity/Women",
        "description": "Cash incentive for pregnant and lactating mothers for first live birth.",
        "criteria": {
            "gender": ["female"],
            "is_pregnant_or_lactating": [True],
            "min_age": 19,
        },
        "documents": [
            "Aadhaar Card",
            "MCP (Mother and Child Protection) Card",
            "Bank account passbook",
            "Husband's Aadhaar (if available)",
        ],
        "benefit": "Rs. 5,000 in three installments for first living child",
        "apply_mode": "Anganwadi Centre or nearest health facility",
    },
    {
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "category": "Savings/Girl Child",
        "description": "Small savings scheme for the girl child, offering high interest and tax benefits.",
        "criteria": {
            "gender": ["female"],
            "max_age": 10,
        },
        "documents": [
            "Birth Certificate of girl child",
            "Aadhaar Card of guardian",
            "Address proof",
            "Passport-size photograph",
        ],
        "benefit": "High interest savings account maturing when girl turns 21; tax benefits under 80C",
        "apply_mode": "Any post office or authorized bank branch",
    },
    {
        "name": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        "category": "Employment/Business",
        "description": "Collateral-free working capital loan for street vendors.",
        "criteria": {
            "occupation": ["street_vendor"],
            "min_age": 18,
        },
        "documents": [
            "Aadhaar Card",
            "Vending Certificate / Letter of Recommendation from ULB",
            "Bank account details",
        ],
        "benefit": "Working capital loan up to Rs. 10,000 (first tranche), increasing on repayment",
        "apply_mode": "Online via pmsvanidhi.mohua.gov.in or nearest Urban Local Body",
    },
    {
        "name": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)",
        "category": "Skill Development",
        "description": "Free skill training and placement assistance for rural youth.",
        "criteria": {
            "min_age": 15,
            "max_age": 35,
            "location": ["rural"],
        },
        "documents": [
            "Aadhaar Card",
            "Educational certificates",
            "Domicile/Residence certificate",
            "Bank account passbook",
        ],
        "benefit": "Free residential/non-residential skill training + guaranteed placement assistance",
        "apply_mode": "Nearest DDU-GKY training center or ddugky.gov.in",
    },
]

# Fields the eligibility engine understands (for the form UI)
OCCUPATIONS = ["farmer", "self-employed", "business_owner", "salaried", "unemployed", "street_vendor", "other"]
LOCATIONS = ["rural", "urban"]
GENDERS = ["male", "female", "other"]
