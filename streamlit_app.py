import streamlit as st
import pandas as pd
import datetime
from openpyxl import load_workbook

def log_cred():
    if 'cred_mail' not in st.session_state:
        st.session_state.cred_mail = st.session_state.email
    df_1 = pd.read_excel('attendance_register.xlsx', sheet_name='Sheet2')
    n = len(df_1)
    for i in range(n):
        if st.session_state.email==df_1['email'][i] and st.session_state.passkey == str(df_1['password'][i]):
            st.session_state.authenticated=True
            return True
            break
        if i==n:
            st.session_state.authenticated=False
            st.error("Invalid email or password", icon="❌")

def clicked_p():
    # df_date = pd.read_excel('attendance_register.xlsx', sheet_name="Sheet1")
    # if df_date['Date'] =! str(datetime.date.today()):
    new_row = [str(datetime.date.today()), str(datetime.datetime.now().time()), "Present", st.session_state.remark, st.session_state.cred_mail]
    attendance_sheet.append(new_row)
    wb.save('attendance_register.xlsx')
    st.session_state.instances='done_p'
    st.session_state.button='out'

def clicked_l():
    new_row = [str(datetime.date.today()), str(datetime.datetime.now().time()), "Leave", st.session_state.reason, st.session_state.cred_mail]
    attendance_sheet.append(new_row)
    wb.save('attendance_register.xlsx')
    st.session_state.instances='done_l'
    st.session_state.button='out'

def sign_cred():
    df_cred = pd.read_excel('attendance_register.xlsx', sheet_name='Sheet2')
    if st.session_state.new_mail not in df_cred['email'].values:
        new_row2 = [st.session_state.new_name, st.session_state.new_mail, st.session_state.new_passkey]
        cred_sheet.append(new_row2)
        wb.save('attendance_register.xlsx')
        st.write(f"<h2>Welcome {st.session_state.new_name}</h2>", unsafe_allow_html=True)
        st.success("Account created Successfully", icon='🎉')
        st.write("Now login to your account")
    else:
        st.error("Email already exists", icon="❌")

def home():
    st.title(":green[Attendance Register]")
    st.write("")
    st.write("<h3>Steps to register your attendance:</h3>", unsafe_allow_html=True)
    st.write("- Go to **Attendance** tab.\n- You will have two options, *Mark Your Present* and *Mark Your Leave*.\n- **For Present**: Fill any remarks (optional) and click **Mark Attendance**.\n- **For Leave**: Fill reason for leave and click **Mark Leave**.\n- **Reports**: Check your attendance reports in the reports tab.")

def done_p():
    st.success("Present Marked Successfully!")
def done_l():
    st.success("Leave Marked Successfully!")

def atten():
    df_date = pd.read_excel('attendance_register.xlsx', sheet_name="Sheet1")
    fil_df = df_date[(df_date['Email']==st.session_state.cred_mail)]
    if 'button' not in st.session_state:
        st.session_state.button=''
    
    for mail in df_date['Email'].tolist():
        if st.session_state.cred_mail not in mail:
            st.session_state.button='mark'

    today_str = str(datetime.date.today())
    for date_str in fil_df['Date'].tolist():
        if today_str in date_str:  # Check if today's string is present in any date string
            st.session_state.button = 'out'
            break  # Exit loop after finding a match
        else:
            st.session_state.button = 'mark'

    if st.session_state.button=='mark':
        st.write("<h3>Mark your Present here</h3>", unsafe_allow_html=True)
        st.text_input("Any remarks? (optional)", key='remark')
        st.button("**Mark attendance**", on_click=clicked_p)
        st.divider()
        st.write("<h3>Mark your Leave here</h3>", unsafe_allow_html=True)
        st.text_input("Reason for leave", key='reason')
        st.button("**Mark Leave**", on_click=clicked_l)
    if st.session_state.button=='out':
        st.success("Attendance Registered Already!")


def reports():
    df_r = pd.read_excel('attendance_register.xlsx', sheet_name="Sheet1")
    st.write("<h2>Check your attendance reports here</h2>", unsafe_allow_html=True)
    fil_df = df_r[(df_r['Email']==st.session_state.cred_mail)]
    per_df = fil_df[['Date', 'Time', 'Attendance', 'Remarks']].reset_index(drop=True)
    st.dataframe(per_df, width=600)

def home_page():
    if 'instances' not in st.session_state:
        st.write("<h2>Welcome to Technodyne Informatics Attendance Register</h2>", unsafe_allow_html=True)
        st.session_state.instances=''
    with st.sidebar:
        logo = """
        <div style="text-align: center;">
            <img src="https://www.technodyne.in/_next/static/media/logo.181d24ff.png" alt='Logo' width='200'>
        </div>
        """
        st.markdown(logo, unsafe_allow_html=True)
        bg_img="""
        <style>
        [data-testid="stSidebarContent"]{
        background-image: url(https://media.istockphoto.com/id/517802126/photo/office-table-with-notebook-computer-keyboard-mouse-cup-of-coffee.jpg?s=612x612&w=0&k=20&c=l7gFox9XAsxB2MtLqmT8tQrgfX8pmaJITppWV2JKkbw=);
        background-size: cover;
        }
        [data-testid="stAppViewContainer"]{
        background-image: url(https://i.pinimg.com/564x/dd/f3/0e/ddf30e0132ac7476e981d7ba7fb3995c.jpg);
        background-size: cover;
        }
        [data-testid="stHeader"]{
        background-color: rgba(0,0,0,0);
        background-size: cover;
        }
        </style>
        """
        st.markdown(bg_img, unsafe_allow_html=True)
        col1,col2 = st.columns([1,1])
        if st.button("**Home**"):
            st.session_state.instances='home'
        if st.button("**Attendance**"):
            st.session_state.instances='attendance'
        if st.button("**Reports**"):
            st.session_state.instances='reports'

    if 'pres' not in st.session_state:
        st.session_state.pres='att'
    
    if st.session_state.instances=='home':
        home()
    if st.session_state.instances=='attendance':
        atten()
    if st.session_state.instances=='reports':
        reports()
    if st.session_state.instances=='done_p':
        done_p()
    if st.session_state.instances=='done_l':
        done_l()
    

def login():
    if 'authenticated' not in st.session_state:
        st.title(":green[Login/Sign Up]")
        col1, col2 = st.columns([1,1])
        col1.button("**Login**", key="login_but")
        col2.button("**Sign Up**", key="sign_but")

        ## Login - 1
        if st.session_state.login_but:
            with st.form(key="login_form"):
                st.text_input('**Email ID**', key='email')
                st.text_input('**Password**', type="password", key="passkey")
                st.form_submit_button("Login", on_click=log_cred)
        ## Sign Up - 1
        if st.session_state.sign_but:
            with st.form(key='sign_form'):
                st.text_input("**Full Name**", key='new_name')
                st.text_input("**Email ID**", key='new_mail')
                st.text_input("**Set Password**", type="password", key='new_passkey')
                st.form_submit_button("**Sign Up**", on_click=sign_cred)
        return False
    else:
        if st.session_state.authenticated:
            st.session_state.pages = 'home'
            return True
        else:
            st.title("Login/Sign Up")
            st.error("Invalid email or password", icon="❌")
            col1, col2 = st.columns([1,1])
            col1.button("**Login**", key="login_but")
            col2.button("**Sign Up**", key="sign_but")

            ## Login - 2
            if st.session_state.login_but:
                with st.form(key="login_form"):
                    st.text_input('**Email ID**', key='email')
                    st.text_input('**Password**', type="password", key='passkey')
                    st.form_submit_button("Login", on_click=log_cred)
            ## Sign Up - 2
            if st.session_state.sign_but:
                with st.form(key='sign_form'):
                    st.text_input("**Full Name**", key='new_name')
                    st.text_input("**Email ID**", key='new_mail')
                    st.text_input("**Set Password**", type="password", key='new_passkey')
                    st.form_submit_button("**Sign Up**", on_click=sign_cred)
            return False


if __name__=="__main__":
    # url = "https://www.technodyne.in/_next/static/media/logo.181d24ff.png"
    # st.image(url)


    with open('syle.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    logo = """
    <div style="text-align: center;">
        <img src="https://www.technodyne.in/_next/static/media/logo.181d24ff.png" alt='Logo' width='200'>
    </div>
    """
    st.markdown(logo, unsafe_allow_html=True)
    bg_img="""
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url(https://i.pinimg.com/564x/dd/f3/0e/ddf30e0132ac7476e981d7ba7fb3995c.jpg);
    background-size: cover;
    }
    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    background-size: cover;
    }
    </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)

    wb = load_workbook('attendance_register.xlsx')
    attendance_sheet = wb['Sheet1']
    cred_sheet = wb['Sheet2']

    if 'df1' not in st.session_state:
        st.session_state.df1 = pd.read_excel('attendance_register.xlsx', sheet_name='Sheet1')
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.read_excel('attendance_register.xlsx', sheet_name='Sheet2')

    if 'pages' not in st.session_state:
        st.session_state.pages = "first"

    if st.session_state.pages == "first":
        login()
    if st.session_state.pages=='home':
        home_page()
