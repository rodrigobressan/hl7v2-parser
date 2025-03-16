import streamlit as st
import openai
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Configure OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def analyze_hl7v2(document_text):
    """Analyze the HL7v2 document using OpenAI GPT-4."""
    prompt = f"""
    You are an expert in healthcare interoperability and HL7v2 message parsing. 
    
    Analyze the following hl7v2 message, and return your message in the following structure (an example, but feel free to modify it if needed):
    
    MSH (Message Header)
Sending Application: MegaReg

Sending Facility: XYZHospC

Receiving Application: SuperOE

Receiving Facility: XYZImgCtr

Message Timestamp: 2006-05-29 09:01:31 -0500

Message Type: ADT^A01 (Patient Admit)

Message Control ID: 01052901

HL7 Version: 2.5

EVN (Event Type)
Event Occurred Timestamp: 2006-05-29 09:01

Recorded Timestamp: 2006-05-29 09:00

PID (Patient Identification)
Patient ID: 56782445 (assigned by UAReg)

Patient Name: BARRY Q KLEINSAMPLE JR

Date of Birth: 1962-09-10

Gender: Male

Race: 2028-9 (American Indian or Alaska Native) (from HL70005)

Addresses:

260 Goodwin Crest Drive, Birmingham, AL 35209 (Mailing)

Nickell’s Pickles, 10000 W 100th Ave, Birmingham, AL 35200 (Office)

Patient Account Number: 0105I30001 (assigned by 99DEF)

PV1 (Patient Visit Information)
Patient Class: Inpatient (I)

Assigned Location: Ward W, Room 389, Bed 1, UABH

Admitting Doctor: Dr. Rex Morgan, MD (ID: 12345)

Attending Doctor: Dr. Lucy Grainger, MD (ID: 67890)

Consulting Doctor: Dr. Sherman Potter, MD (ID: 13579)

Admission Date/Time: 2006-05-29 09:00

Visit Number: 8675309

OBX (Observation Result)
Body Height: 1.80 m (Normal)

Body Weight: 79 kg (Normal)

AL1 (Allergy Information)
Aspirin Allergy

DG1 (Diagnosis)
Diagnosis Code: 786.50 (Chest Pain, Unspecified)

ICD Version: ICD-9

Diagnosis Type: Admitting Diagnosis (A)

    ===
    
    Provide your answer in markdown. Be fast!


    Here is the document to analyze:
    ```
    {document_text}
    ```
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an HL7v2 expert."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# Streamlit UI Configuration
st.set_page_config(page_title="HL7v2 Parser", layout="wide", initial_sidebar_state="expanded")

# Sidebar Navigation
with st.sidebar:
    page = option_menu(
        menu_title="📑 HL7v2 Parser",
        menu_icon="none",
        options=["Home", "Analyze"],
        icons=["info-circle", "search"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "5px", "color": "#333"},
            "nav-link-selected": {"background-color": "#2E7D32", "color": "white"},
        },
    )

# Home Page
if page == "Home":
    st.title("📑 HL7v2 Parser")
    st.markdown(
        """
        This tool analyzes **HL7v2 messages** to check for structure, format, and potential issues.
        - ✅ **Input your HL7v2 message**
        - ✅ **Get an AI-powered analysis**
        - ✅ **Identify potential structural inconsistencies**

        ## 🏥 What is HL7v2?
        **Health Level 7 Version 2 (HL7v2)** is a widely used healthcare data exchange standard. It defines a structured format for transmitting clinical and administrative data between healthcare systems.
        
        ### 🔹 Why is HL7v2 Important?
        - Standardizes communication between hospital systems like EHRs, LIS, and RIS.
        - Enables interoperability data exchange.
        - Used for **patient admission, lab results, medical orders, and more**.
        
        ### 🔹 HL7v2 Message Structure
        An HL7v2 message consists of **segments**, each identified by a three-letter code:
        - **MSH** (Message Header) - Identifies sender, receiver, timestamp, and message type.
        - **EVN** (Event Type) - Indicates the event trigger, such as patient admission.
        - **PID** (Patient Identification) - Contains patient demographics.
        - **PV1** (Patient Visit) - Provides visit details, attending physician, and location.
        - **OBX** (Observation Result) - Reports lab or clinical results.
        - **AL1** (Allergy Information) - Lists known allergies.
        - **DG1** (Diagnosis) - Contains patient diagnoses.
        
        **Example HL7v2 Message:**
        ```
        MSH|^~&|MegaReg|XYZHospC|SuperOE|XYZImgCtr|20060529090131-0500||ADT^A01^ADT_A01|01052901|P|2.5
        EVN||200605290901||||200605290900
        PID|||56782445^^^UAReg^PI||KLEINSAMPLE^BARRY^Q^JR||19620910|M||2028-9^^HL70005^RA99113^^XYZ|260 GOODWIN CREST DRIVE^^BIRMINGHAM^AL^35209^^M~NICKELL’S PICKLES^10000 W 100TH AVE^BIRMINGHAM^AL^35200^^O|||||||0105I30001^^^99DEF^AN
        PV1||I|W^389^1^UABH^^^^3||||12345^MORGAN^REX^J^^^MD^0010^UAMC^L||67890^GRAINGER^LUCY^X^^^MD^0010^UAMC^L|MED|||||A0||13579^POTTER^SHERMAN^T^^^MD^0010^UAMC^L||8675309|||||||||||||||||||||||||200605290900
        OBX|1|NM|^Body Height||1.80|m^Meter^ISO+||N|||F
        OBX|2|NM|^Body Weight||79|kg^Kilogram^ISO+||N|||F
        AL1|1||^ASPIRIN
        DG1|1||786.50^CHEST PAIN, UNSPECIFIED^I9|||A
        ```
        
        ## Explanation of it:
        
        #### MSH (Message Header)
        - **Sending Application:** MegaReg
        - **Sending Facility:** XYZHospC
        - **Receiving Application:** SuperOE
        - **Receiving Facility:** XYZImgCtr
        - **Message Timestamp:** 2006-05-29 09:01:31 -0500
        - **Message Type:** ADT^A01 (Patient Admit)
        - **Message Control ID:** 01052901
        - **HL7 Version:** 2.5
        
        #### EVN (Event Type)
        - **Event Occurred Timestamp:** 2006-05-29 09:01
        - **Recorded Timestamp:** 2006-05-29 09:00
        
        #### PID (Patient Identification)
        - **Patient ID:** 56782445 (assigned by UAReg)
        - **Patient Name:** BARRY Q KLEINSAMPLE JR
        - **Date of Birth:** 1962-09-10
        - **Gender:** Male
        - **Race:** 2028-9 (American Indian or Alaska Native) (from HL70005)
        - **Addresses:**
          - 260 Goodwin Crest Drive, Birmingham, AL 35209 (Mailing)
          - Nickell’s Pickles, 10000 W 100th Ave, Birmingham, AL 35200 (Office)
        - **Patient Account Number:** 0105I30001 (assigned by 99DEF)
        
        #### PV1 (Patient Visit Information)
        - **Patient Class:** Inpatient (I)
        - **Assigned Location:** Ward W, Room 389, Bed 1, UABH
        - **Admitting Doctor:** Dr. Rex Morgan, MD (ID: 12345)
        - **Attending Doctor:** Dr. Lucy Grainger, MD (ID: 67890)
        - **Consulting Doctor:** Dr. Sherman Potter, MD (ID: 13579)
        - **Admission Date/Time:** 2006-05-29 09:00
        - **Visit Number:** 8675309
        
        #### OBX (Observation Result)
        - **Body Height:** 1.80 m (Normal)
        - **Body Weight:** 79 kg (Normal)
        
        #### AL1 (Allergy Information)
        - **Allergy:** Aspirin Allergy
        
        #### DG1 (Diagnosis)
        - **Diagnosis Code:** 786.50 (Chest Pain, Unspecified)
        - **ICD Version:** ICD-9
        - **Diagnosis Type:** Admitting Diagnosis (A)

        #### Navigate to **'Analyze'** to start parsing HL7v2 messages!
        """
    )

# Analyze Page
elif page == "Analyze":
    st.title("🔍 Analyze HL7v2 Message")
    document_text = st.text_area("Enter your HL7v2 message below:", height=150)

    if st.button("Analyze HL7v2 📑", use_container_width=True):
        with st.spinner("Analyzing message..."):
            analysis_result = analyze_hl7v2(document_text)
            st.subheader("🔍 HL7v2 Analysis Result:")
            st.markdown(analysis_result)

elif page == "Example":
    st.title("Example HL7v2 Analysis")
    document_text = """
    MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|202203010830||ADT^A01|123456|P|2.3|
    PID|1||123456^^^HospitalMRN^MR||Doe^John||19800101|M|||123 Main St^^Metropolis^NY^10001||555-1234|||||123-45-6789||
    """
    st.text_area("📜 Example HL7v2 Document:", document_text, height=150)
    st.subheader("🔍 Sample Analysis Output:")
    st.write("MSH segment correctly formatted, PID contains expected fields, no structural errors detected.")
    st.write("Explanation:")

