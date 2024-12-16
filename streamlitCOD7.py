import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def apply_moving_average(data_series, window_size=5):
    return data_series.rolling(window_size).mean()

def clean_data(data):
    # Remove rows with missing values
    data = data.dropna()
    # Remove duplicates
    data = data.drop_duplicates()
    return data

def plot_data(data):
    try:
        # Clean the data
        data = clean_data(data)

        # Apply moving average
        data['COD F/D_MA'] = apply_moving_average(data['COD F/D'])

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['COD F/D'], label='Actual COD F/D')
        plt.plot(data['Date'], data['COD F/D_MA'], label='Moving Average (window=5)')

        # Add horizontal lines for COD standards
        plt.axhline(y=80, color='blue', linestyle='--', label='Standard A (80 mg/L)')
        plt.axhline(y=100, color='green', linestyle='--', label='Standard B (100 mg/L)')

        # Add labels for remarks
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 80, 'Standard A', fontsize=10, color='blue', ha='right', va='bottom')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 100, 'Standard B', fontsize=10, color='green', ha='right', va='bottom')

        plt.xlabel('Date')
        plt.ylabel('COD F/D')
        plt.title('Actual vs Moving Average COD F/D with Standards')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        return data
    except Exception as e:
        st.error(f"Error processing the data: {e}")
        return None

st.title("Effluent Data Visualization")

st.markdown("""
This application allows you to upload an Excel file, clean the data, and visualize the Industrial Effluent levels using a moving average.
""")

uploaded_file = st.file_uploader("Upload your Excel file (max 50KB)", type=['xlsx'], key='1', accept_multiple_files=False)

if uploaded_file:
    if uploaded_file.size > 50000:
        st.error("File size exceeds 50KB limit. Please upload a smaller file.")
    else:
        try:
            data = pd.read_excel(uploaded_file)
            st.write("Uploaded Data")
            st.dataframe(data)

            result = plot_data(data)
            if result is not None:
                st.write("Data Visualization")
                st.dataframe(result)

                csv = result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Processed Data as CSV",
                    data=csv,
                    file_name='processed_data.csv',
                    mime='text/csv',
                )
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")

