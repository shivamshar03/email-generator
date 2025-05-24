from backend import *
import streamlit as st

# Streamlit app
st.set_page_config(page_title="Generate Emails", page_icon='📧', layout='centered')
st.header("Generate Emails 📧")

EMAIL_USER = st.sidebar.text_input("Your Email ID(sender's) : ")
EMAIL_PASS = st.sidebar.text_input("APP Password key :")
with st.sidebar.expander("How to generate APP Password key :"):
    st.markdown("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Generate Gmail App Password</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f7f9fc;
      padding: 30px;
      color: #333;
    }
    h1 {
      color: #d93025;
    }
    a {
      color: #1a73e8;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    ul {
      line-height: 1.8;
    }
    .note {
      background-color: black;
      padding: 10px;
      border-left: 4px solid white;
      margin-top: 20px;
    }
    .code {
      font-family: monospace;
      background-color: grey;
      padding: 3px 6px;
      border-radius: 3px;
    }
  </style>
</head>
<body>

  <h1>🔐 How to Generate Gmail App Password</h1>

  <p><strong>You must have 2-Step Verification enabled on your Google account.</strong><br>
     If not, set it up here: <a href="https://myaccount.google.com/security" target="_blank">https://myaccount.google.com/security</a></p>

  <h2>Steps to Generate Gmail App Password:</h2>
  <ol>
    <li>Go to Google Account Security Settings: 
      <a href="https://myaccount.google.com/security" target="_blank">https://myaccount.google.com/security</a></li>
    <li>Enable <strong>2-Step Verification</strong> (if not already enabled)</li>
    <li>Under <strong>"Signing in to Google"</strong>, click <strong>2-Step Verification</strong></li>
    <li>Follow the setup process using your phone number or authenticator app.</li>
    <li>After enabling 2FA, go back to the <strong>Security</strong> page.</li>
    <li>Scroll down to <strong>"Signing in to Google"</strong> section and click on <strong>“App passwords”</strong>.</li>
    <li>Sign in again if prompted.</li>
    <li>Under <strong>"Select app"</strong>, choose the app you're using (e.g., <em>Mail</em>)<br>
        Or choose <em>Other (Custom name)</em> and enter a custom name (e.g., “Python App”).</li>
    <li>Click <strong>Generate</strong>.</li>
    <li>Copy the 16-character app password shown in yellow.<br>
        🔑 Example: <span class="code">abcd efgh ijkl mnop</span> (no spaces needed when pasting it in code)</li>
    <li>Use this password in your application <strong>instead of your Google account password</strong>.</li>
  </ol>

  <div class="note">
    💡 <strong>Note:</strong> You can revoke or generate new app passwords anytime from the same settings page. Never share your app password publicly.
  </div>

</body>
</html>
""",unsafe_allow_html=True)



# Inputs
form_input = st.text_area('✍️ Enter the email topic', height=275)
col1, col2= st.columns([10, 10])

with col1:
    email_recipient = st.text_input('👥 Recipient Email')
with col2:
    email_style = st.selectbox('✒️ Writing Style',
                               ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral', 'Casual', 'Friendly'),
                               index=0)

# Attachment toggle ( file upload ) Optional
togglebar = st.toggle("📎 Add Attachment")
if togglebar:
    docs = st.file_uploader("📤 Upload Your Attachments", accept_multiple_files=True)
    if docs:
        st.success("✅ Successfully Uploaded:")


if "generated_email" not in st.session_state:
    st.session_state.generated_email = None


if st.button("🚀 Generate Email"):
    if not form_input and not EMAIL_USER and not email_recipient:
        st.error("🚨 Please fill in all required fields.")
    else:
        with st.spinner("Generating email..."):
            email_output = getLLMResponse(form_input, EMAIL_USER, email_recipient, email_style)
            if email_output:
                st.session_state.generated_email = email_output

if st.session_state.generated_email:
    mail_content = st.text_area("📨 Generated Email", value=st.session_state.generated_email, height=500)

    if st.button("📬 Send Mail"):
        if togglebar:
            send_email(email_recipient, mail_content,attachments=docs)
        else:
            send_email(email_recipient, mail_content)



