import streamlit as st
import pdfkit
import base64
from jinja2 import Environment, FileSystemLoader, select_autoescape

st.set_page_config(layout="centered", page_icon="💰", page_title="Invoice Generator")
st.title("💰 Invoice Generator")

st.write(
    "This app shows how you can use Streamlit to make an invoice generator app in just a few lines of code!"
)


env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("invoice_template.html")


with st.form("template_form"):
    left, right = st.columns((1, 10))
    color = left.color_picker("Color", value="#b4cffa")
    company_name = right.text_input("Company name", value="SkiFoo")
    left, right = st.columns(2)
    customer_name = left.text_input("Customer name", value="Slope Corporation")
    customer_address = right.text_input("Customer address", value="Red skiing runs")
    product_type = left.selectbox("Product type", ["Data app crafting", "ML model training"])
    quantity = right.number_input("Quantity", 1, 10)
    price_per_unit = st.slider("Price per unit", 1, 100, 60)
    total = price_per_unit * quantity
    submit = st.form_submit_button()

if submit:
    html = template.render(
        color=color,
        company_name=company_name,
        customer_name=customer_name,
        customer_address=customer_address,
        product_type=product_type,
        quantity=quantity,
        price_per_unit=price_per_unit,
        total=total,
    )

    # print(html)
    config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")  
    
    # converting html file to pdf file  
    # pdfkit.from_file('sample.html', 'output.pdf', configuration = config)
    pdf = pdfkit.from_string(html, configuration = config)
    # pdf = HTML(string=html)
    st.balloons()

    st.success("🎉 Your invoice was generated!")
    print(type(pdf))
    base64_pdf = base64.b64encode(pdf).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)
    # st.download_button(
    #     "⬇️ Download PDF",
    #     data=pdf,
    #     file_name="invoice.pdf",
    #     mime="application/octet-stream",
    #)
