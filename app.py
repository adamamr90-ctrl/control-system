import streamlit as st
import pandas as pd
from controller import read_excel_file, highlight_failed, export_to_excel

Subject = ["اللغه العربية","اللغه الانجليزية","الرياضيات","علوم متكاملة","التاريخ","فلسفة و منطق","التربية الدينية",
"البرمجة والذكاء الاصطناعي","E.H.L","G/F.H.L","تكنولوجيا الصناعة"]

def main():
    st.title("نظام الكنترول")

    with st.expander("تعليمات الاستخدام"):
        st.write("""
        1. ارفع ملف Excel يحتوي على أسماء الطلاب
        2. اختر المواد الدراسية
        3. ادخل الدرجة العظمى لكل مادة
        4. ادخل درجات الطلاب في الجدول
        5. اضغط تحديد الراسبين لعرض النتائج
        6. حمل ملف Excel بالنتائج
        """)
    
    file = st.file_uploader("ارفع ملف الاكسيل", type=["xlsx"])

    if file is not None:
        df = read_excel_file(file)
        
        if "اسم الطالب" not in df.columns:
            st.error(" الملف لا يحتوي على عمود اسم الطالب — تأكد من صحة الملف!")
            return

        selected_subjects = st.multiselect("اختر المواد", Subject)

        max_grades = {}
        min_grades = {}
        
        for subject in selected_subjects:
            max_grade = st.number_input(f"العظمي - {subject}",min_value=0)
            min_grade = max_grade / 2 
            st.write(f"الصغري : {min_grade}")
            max_grades[subject] = max_grade
            min_grades[subject] = min_grade
            df[subject] = 0 
            
        search = st.text_input("ابحث عن طالب")
        if search:
            df = df[df["اسم الطالب"].str.contains(search)]

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            column_config={
            subject: st.column_config.NumberColumn(
            subject,
            min_value=0,
            max_value=max_grades[subject]
            )
            for subject in selected_subjects
            }
            )
        edited_df["المجموع"] = edited_df[selected_subjects].sum(axis=1)
        edited_df = edited_df.sort_values(by="اسم الطالب", ascending=True )

        if not selected_subjects:
            st.warning("⚠️ من فضلك اختر مادة واحدة على الأقل!")

        if st.button("تحديد الراسبين"):
            styled_df = highlight_failed(edited_df, min_grades)
            st.dataframe(styled_df)
            for subject in selected_subjects:
                failed = (edited_df[subject] < min_grades[subject]).sum()
                total = len(edited_df)
                passed = total - failed
                pass_percentage = (passed / total)*100

                col1,col2 = st.columns(2)
                with col1:
                    st.metric(f"عدد الراسبين - {subject}", failed)
                with col2:
                    st.metric(f"نسبة النجاح - {subject}", f"{pass_percentage:.1f}%")
        
        

        output = export_to_excel(edited_df)
        st.download_button(
            label="Download Excel File",
            data=output,
            file_name="results.xlsx",
            mime="application/vnd.ms-excel"
        )


if __name__ == "__main__":
    main()
        

    
    


