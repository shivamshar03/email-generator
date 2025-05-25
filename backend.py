import streamlit as st
import yagmail
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9)

# Function to send email
def send_email(to_email, email_content,email_user, email_pass,attachments = None):
    try:
        if not email_user and not email_pass:
            st.error("🚫 Email credentials are missing")
            return

        subject, body = extract_email_parts(email_content)
        email_contents = [body]
        if attachments:
            email_contents.extend(attachments)

        yag = yagmail.SMTP(user=email_user, password=email_pass)
        yag.send(to=to_email, subject=subject, contents=email_contents)
        st.success(f"✅ Mail sent successfully to {to_email}")
    except Exception as e:
        st.error(f"🚫 Failed to send email: {e}")


# Function to generate email
def getLLMResponse(form_input, email_sender, email_recipient, email_style):
    try:
        template = """
        Write an email in a {style} tone about the following topic: {email_topic}.

        Sender: {sender}
        Recipient: {recipient}

        Email Text:
        """
        prompt = PromptTemplate(
            input_variables=["style", "email_topic", "sender", "recipient"],
            template=template
        )

        final_prompt = prompt.format(
            email_topic=form_input,
            sender=email_sender,
            recipient=email_recipient,
            style=email_style
        )

        response = llm.invoke(final_prompt)
        return response.content
    except Exception as e:
        st.error(f"⚠️ Error generating email: {e}")
        return None

# Function to split email into subject and body
def extract_email_parts(email_text):
    try:
        lines = email_text.strip().split("\n")
        subject = ""
        body_lines = []
        for i, line in enumerate(lines):
            if line.lower().startswith("subject:"):
                subject = line.replace("Subject:", "").strip()
                body_lines = lines[i + 1:]
                break
        body = "\n".join(body_lines).strip()
        return subject, body
    except Exception as e:
        st.error(f"❌ Failed to extract subject and body: {e}")
        return "", ""