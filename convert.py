import os
import re

def batch_convert_to_utf8(directory):
    # 用來尋找舊式 meta 標籤的正規表示法 (忽略大小寫)
    meta_pattern = re.compile(r'<meta http-equiv="Content-Type" content="text/html; charset=big5">', re.IGNORECASE)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".htm", ".html")):
                file_path = os.path.join(root, file)
                
                try:
                    # 1. 讀取 Big5 內容
                    with open(file_path, 'r', encoding='big5', errors='ignore') as f:
                        content = f.read()
                    
                    # 2. 修改 Meta 標籤
                    # 如果找不到舊標籤，建議也在 <head> 後面補上，確保瀏覽器正確識別
                    if meta_pattern.search(content):
                        new_content = meta_pattern.sub('<meta charset="UTF-8">', content)
                    else:
                        # 若沒找到舊標籤，則在 <head> 下方插入
                        new_content = content.replace('<head>', '<head>\n<meta charset="UTF-8">')
                    
                    # 3. 以 UTF-8 覆蓋存檔
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                        
                    print(f"成功轉換: {file}")
                except Exception as e:
                    print(f"處理 {file} 時發生錯誤: {e}")

if __name__ == "__main__":
    # 執行當前目錄下的所有檔案轉換
    batch_convert_to_utf8(".")
    print("\n--- 全部轉換完成！ ---")