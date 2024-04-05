import streamlit as st
from tabula import convert_into

def main():
    st.title("PDF to CSV Converter")

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("PDF file uploaded successfully!")

        # Generate CSV button
        if st.button("Generate CSV"):
            # Define output CSV file path
            output_csv = "output.csv"
            
            # Convert PDF to CSV
            convert_pdf_to_csv(uploaded_file, output_csv)

            # Display download link for CSV file
            st.write("CSV file generated successfully!")
            file_path = "output.csv"
            with open(file_path, "rb") as file:
                file_content = file.read()
            st.download_button(
                label="Download",
                data=file_content,
                file_name="output.csv",
                mime="text/plain"  )
            
            

def convert_pdf_to_csv(pdf_file, output_csv):
    # Convert PDF to CSV
    try:
        convert_into(pdf_file, output_csv, output_format='csv', lattice=False, stream=True, pages="all")
    except Exception as e:
        st.error(f"Error occurred during PDF to CSV conversion: {e}")



if __name__ == "__main__":
    main()
