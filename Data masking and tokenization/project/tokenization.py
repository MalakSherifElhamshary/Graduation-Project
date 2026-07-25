import uuid
import re


def tokenize_data(input_path, output_path):
    import pandas as pd
    df = pd.read_csv(input_path)

    # نمط (Pattern) للتعرف على الإيميلات تلقائياً داخل البيانات
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    for col in df.columns:
        # لو أول قيمة في العمود شكلها إيميل، يبقى العمود كله إيميلات
        first_val = str(df[col].iloc[0])
        if re.match(email_pattern, first_val) or 'email' in col.lower():
            df[col] = [str(uuid.uuid4())[:8] for _ in range(len(df))]

    df.to_csv(output_path, index=False)
