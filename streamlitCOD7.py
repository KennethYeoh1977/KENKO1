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
        data['SS F/D_MA'] = apply_moving_average(data['SS F/D'])
        data['BOD F/D_MA'] = apply_moving_average(data['BOD F/D'])
        data['Zn F/D_MA'] = apply_moving_average(data['Zn F/D'])

        # Plotting COD F/D
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['COD F/D'], label='Actual COD F/D')
        plt.plot(data['Date'], data['COD F/D_MA'], label='Moving Average (window=5)')
        plt.axhline(y=80, color='blue', linestyle='--', label='Standard A (80 mg/L)')
        plt.axhline(y=100, color='green', linestyle='--', label='Standard B (100 mg/L)')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 80, 'Standard A', fontsize=10, color='blue', ha='right', va='bottom')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 100, 'Standard B', fontsize=10, color='green', ha='right', va='bottom')
        plt.xlabel('Date')
        plt.ylabel('COD F/D')
        plt.title('Actual vs Moving Average COD F/D with Standards')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        # Plotting SS F/D
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['SS F/D'], label='Actual SS F/D')
        plt.plot(data['Date'], data['SS F/D_MA'], label='Moving Average (window=5)')
        plt.axhline(y=50, color='red', linestyle='--', label='Standard A (50 mg/L)')
        plt.axhline(y=100, color='orange', linestyle='--', label='Standard B (100 mg/L)')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 50, 'Standard A', fontsize=10, color='red', ha='right', va='bottom')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 100, 'Standard B', fontsize=10, color='orange', ha='right', va='bottom')
        plt.xlabel('Date')
        plt.ylabel('SS F/D')
        plt.title('Actual vs Moving Average SS F/D with Standards')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        # Plotting BOD F/D
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['BOD F/D'], label='Actual BOD F/D')
        plt.plot(data['Date'], data['BOD F/D_MA'], label='Moving Average (window=5)')
        plt.axhline(y=20, color='purple', linestyle='--', label='Standard A (20 mg/L)')
        plt.axhline(y=50, color='brown', linestyle='--', label='Standard B (50 mg/L)')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 20, 'Standard A', fontsize=10, color='purple', ha='right', va='bottom')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 50, 'Standard B', fontsize=10, color='brown', ha='right', va='bottom')
        plt.xlabel('Date')
        plt.ylabel('BOD F/D')
        plt.title('Actual vs Moving Average BOD F/D with Standards')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        # Plotting Zn F/D
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['Zn F/D'], label='Actual Zn F/D')
        plt.plot(data['Date'], data['Zn F/D_MA'], label='Moving Average (window=5)')
        plt.axhline(y=2, color='orange', linestyle='--', label='Standard (2 mg/L)')
        plt.text(data['Date'].iloc[int(len(data) * 0.8)], 2, 'Standard', fontsize=10, color='orange', ha='right', va='bottom')
        plt.xlabel('Date')
        plt.ylabel('Zn F/D')
        plt.title('Actual vs Moving Average Zn F/D with Standard')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        return data
    except Exception as e:
        st.error(f"Error processing the data: {e}")
        return None

st.title("Performance Monitoring Data + Visualization ©")

st.markdown("""
This application allows you to upload an Excel file, clean the data, and visualize the Industrial Effluent levels using A.I moving average.
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

