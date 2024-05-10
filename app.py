import streamlit as st
import pandas as pd

class TaskTemplarApp:
    def __init__(self):
        self.df = None

    def run(self):
        self.set_page_config()
        self.render_ui()

    def set_page_config(self):
        st.set_page_config(layout="wide")

    def render_ui(self):
        st.title("TASK TEMPLAR")
        self.open_file()

    def open_file(self):
        file_path = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
        if file_path:
            self.display_excel(file_path)

    def display_excel(self, file_path):
        self.df = pd.read_excel(file_path)
        self.update_dropdown()

    def update_dropdown(self):
        if self.df is not None and self.df.shape[1] > 1:
            service_line_and_code_values = self.df.iloc[:, 0].astype(str).unique()
            service_line_and_code_values.sort()
            if len(service_line_and_code_values) > 0:
                selected_service = st.selectbox("Select Service", service_line_and_code_values, key="service_selectbox")
                selected_service = selected_service.strip().replace('', '')
                self.update_secondary_dropdown(selected_service)
        else:
            st.write("DataFrame doesn't have enough columns.")

    def update_secondary_dropdown(self, selected_service):
        selected_service_column = self.df.columns[0]
        secondary_column_values = self.df[self.df[selected_service_column] == selected_service].iloc[:, 1].astype(str).unique()
        secondary_column_values.sort()
        selected_secondary_value = st.selectbox("Service Short Text:", ["Select Short Text"] + list(secondary_column_values), key="secondary_selectbox")
        if selected_secondary_value != "Select Short Text":
            selected_secondary_value = selected_secondary_value.strip().replace('', '')
            self.filter_by_service(selected_service, selected_secondary_value)
        else:
            self.filter_by_service(selected_service)

    def filter_by_service(self, selected_service, selected_secondary_value=None):
        if self.df is not None:
            if selected_secondary_value:
                filtered_df = self.df[(self.df.iloc[:, 0].astype(str) == selected_service) & (self.df.iloc[:, 1].astype(str) == selected_secondary_value)]
            else:
                filtered_df = self.df[self.df.iloc[:, 0].astype(str) == selected_service]
            self.display_transformed_df(filtered_df, selected_secondary_value)

    def display_transformed_df(self, filtered_df, selected_secondary_value):
        if selected_secondary_value and filtered_df.shape[0] <= 2:
            columns_and_values = {}
            info1, info2, info3 = st.columns(3)
            num_columns = 3  # Number of columns
            col_widgets = [info1, info2, info3]  # List of column widgets

            duplicate_widgets = False
            for col in filtered_df.columns:
                col_index = filtered_df.columns.get_loc(col) % num_columns  # Calculate the index of the column widget
                col_widget = col_widgets[col_index]  # Get the corresponding column widget
                values = filtered_df[col].astype(str).tolist()
                if any(values.count(x) > 1 for x in values):
                    duplicate_widgets = True
                    break

            if duplicate_widgets:
                st.write(filtered_df)
            else:
                for col in filtered_df.columns:
                    col_index = filtered_df.columns.get_loc(col) % num_columns  # Calculate the index of the column widget
                    col_widget = col_widgets[col_index]  # Get the corresponding column widget
                    values = filtered_df[col].astype(str).tolist()
                    for value in values:
                        col_widget.text_area(f"{col}", value=str(value), height=100)
        else:
            st.write(filtered_df)





if __name__ == "__main__":
    app = TaskTemplarApp()
    app.run()
