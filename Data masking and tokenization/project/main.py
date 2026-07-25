from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
import os
from datetime import datetime  # المكتبة الجديدة
from masking import mask_data
from tokenization import tokenize_data

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
    <div style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h2>🛡️ Data Privacy Tool</h2>
        <form action="/process" method="post" enctype="multipart/form-data" style="display: inline-block; text-align: left; border: 1px solid #ccc; padding: 20px; border-radius: 10px;">
            <label>Choose Method:</label><br>
            <select name="method" style="width: 100%; margin: 10px 0; padding: 5px;">
                <option value="mask">Masking</option>
                <option value="token">Tokenization</option>
            </select><br>
            <label>Select CSV File:</label><br>
            <input type="file" name="file" required style="margin: 10px 0;"><br><br>
            <button type="submit" style="background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%;">Process & Download</button>
        </form>
    </div>
    """
    return content


@app.post("/process")
async def process_file(method: str = Form(...), file: UploadFile = File(...)):
    # 1. حفظ الملف الأصلي
    input_path = os.path.join("uploads", file.filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # 2. إنشاء اسم الملف الجديد مع الوقت والتاريخ
    timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%p")
    output_filename = f"result_{timestamp}_{file.filename}"
    output_path = os.path.join("outputs", output_filename)

    # 3. المعالجة
    if method == "mask":
        mask_data(input_path, output_path)
    else:
        tokenize_data(input_path, output_path)

    # 4. إرسال الملف للتحميل
    return FileResponse(path=output_path, filename=output_filename)
