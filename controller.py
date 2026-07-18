import pandas as pd
from io import BytesIO

def read_excel_file(file):
    df = pd.read_excel(file)
    return df

def highlight_failed(df, min_grades):
    styled = df.style
    for column in df.columns:
        if column in min_grades:
            min_grade = min_grades[column]

            def color_cell(val, mg=min_grade):
                if isinstance(val, (int,float)) and val < mg:
                    return "background-color: red"
                else:
                    return""

            styled = styled.map(color_cell, subset=[column])
    return styled
    
    
def export_to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output
