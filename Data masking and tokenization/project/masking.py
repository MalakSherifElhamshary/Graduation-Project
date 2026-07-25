import pandas as pd


def mask_data(input_path, output_path):
    # قراءة الملف
    df = pd.read_csv(input_path)

    # العلمية دي بتلف على كل الأعمدة وتدور على كلمة name
    found_col = False
    for col in df.columns:
        if 'name' in col.lower():  # بيبحث عن كلمة name بأي شكل (Name, NAME, full_name)
            # التأكد إن البيانات نصية (String) عشان نعرف نعمل لها Masking
            df[col] = df[col].astype(str).apply(
                lambda x: x[:2] + "*" * (len(x) - 2) if len(x) > 2 else x)
            found_col = True
            print(f"Done Masking for column: {col}")

    if not found_col:
        print("Warning: No column with 'name' was found in the file!")

    # حفظ الملف الناتج
    df.to_csv(output_path, index=False)
