#!/usr/bin/env python3

import os
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

import webbrowser
import threading
from attendance_processor import AttendanceProcessor


class SimpleWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.get_html().encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/process":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)

                # multipart/form-dataを簡単にパース
                boundary = self.headers["Content-Type"].split("boundary=")[1]
                parts = post_data.split(f"--{boundary}".encode())

                form_data = {}
                for part in parts:
                    if b"Content-Disposition" in part:
                        lines = part.split(b"\r\n")
                        for i, line in enumerate(lines):
                            if b"name=" in line:
                                name = line.decode().split('name="')[1].split('"')[0]
                                if name == "employee_name":
                                    form_data["employee_name"] = (
                                        lines[i + 2].decode().strip()
                                    )
                                elif name == "template_filename":
                                    form_data["template_filename"] = (
                                        lines[i + 2].decode().strip()
                                    )
                                elif name in ["csv_file", "template_file"]:
                                    # ファイルデータを取得
                                    data_start = part.find(b"\r\n\r\n") + 4
                                    file_data = part[data_start:].rstrip(b"\r\n")
                                    form_data[name] = file_data

                result = self.process_files(form_data)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def process_files(self, form_data):
        employee_name = form_data.get("employee_name", "").strip()
        if not employee_name:
            raise ValueError("作業者名が入力されていません")

        # 元のテンプレートファイル名を取得
        original_template_name = form_data.get(
            "template_filename", "Quco_〇〇_勤務表・立替経費精算書.xlsx"
        )

        # 一時ファイルに保存
        csv_path = "temp_upload.csv"
        template_path = "temp_template.xlsx"

        with open(csv_path, "wb") as f:
            f.write(form_data["csv_file"])
        with open(template_path, "wb") as f:
            f.write(form_data["template_file"])

        try:
            processor = AttendanceProcessor()
            processor.load_csv(csv_path)
            processor.load_excel_template(template_path)

            # 元のファイル名から出力ファイル名を生成
            import re

            output_path = re.sub(
                r"Quco_[^_]+_", f"Quco_{employee_name}_", original_template_name
            )
            processor.process_attendance(employee_name, output_path)

            # ファイルをBase64エンコード
            with open(output_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode("utf-8")

            return {"success": True, "filename": output_path, "file_data": file_data}
        finally:
            # 一時ファイルを削除
            for path in [csv_path, template_path, output_path]:
                if os.path.exists(path):
                    os.remove(path)

    def get_html(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>勤怠表自動作成ツール</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .result { margin-top: 20px; padding: 10px; border-radius: 4px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>勤怠表自動作成ツール</h1>
    
    <form id="form">
        <div class="form-group">
            <label>作業者名:</label>
            <input type="text" id="employeeName" required>
        </div>
        
        <div class="form-group">
            <label>CSVファイル:</label>
            <input type="file" id="csvFile" accept=".csv" required>
        </div>
        
        <div class="form-group">
            <label>Excelテンプレート:</label>
            <input type="file" id="templateFile" accept=".xlsx" required>
        </div>
        
        <button type="submit">勤怠表を作成</button>
    </form>
    
    <div id="result"></div>
    
    <script>
        document.getElementById('form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">処理中...</div>';
            
            const formData = new FormData();
            formData.append('employee_name', document.getElementById('employeeName').value);
            formData.append('csv_file', document.getElementById('csvFile').files[0]);
            formData.append('template_file', document.getElementById('templateFile').files[0]);
            formData.append('template_filename', document.getElementById('templateFile').files[0].name);
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    const blob = new Blob([Uint8Array.from(atob(result.file_data), c => c.charCodeAt(0))], 
                        {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = result.filename;
                    a.click();
                    
                    resultDiv.innerHTML = '<div class="result success">完了！ファイルがダウンロードされました。</div>';
                } else {
                    resultDiv.innerHTML = `<div class="result error">エラー: ${result.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result error">エラー: ${error.message}</div>`;
            }
        });
    </script>
</body>
</html>"""


def start_server(port=8081):
    server = HTTPServer(("localhost", port), SimpleWebHandler)
    print(f"サーバー起動: http://localhost:{port}")
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    server.serve_forever()


if __name__ == "__main__":
    start_server()
