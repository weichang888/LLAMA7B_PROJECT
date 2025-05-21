
# 這是一個全自動化的 AI 新聞摘要系統，透過爬蟲抓取新聞、使用 LLaMA-7B 模型進行摘要生成、彙整成 Word 檔案，並定期寄送 Email。系統設計適用於每週產出一份新聞簡報。

---

## 專案結構
<pre>
LLAMA7B_PROJECT/
│
├── data/            ← 存放原始文章（.txt 檔案，含 title + text）
│
├── summaries/       ← 每篇文章產生的摘要結果（.txt 檔案，含 Title + Summary）
│
├── word/            ← 彙整後的 Word 檔案會放這裡（例如：AINEWS_2025-05-19.docx）
│
├── CrawlerScript.py ← 負責「爬蟲」：抓取新聞內容並儲存成 .txt（放進 data 資料夾）
│
├── llama_7b.py      ← 負責「生成摘要」：讀取 data/*.txt → 寫入 summaries/*.txt
│
├── word.py          ← 負責「彙整成 Word 檔」：從 summaries → 匯整到 word/AINEWS_日期.docx
│
├── receive.py       ← 負責「寄送 Email」：將最新的 Word 報告寄送到你的 Gmail
│
└── main.py          ← 自動化流程主控程式，串起上述四步流程

</pre>
## 資料來源
[AI News](https://www.artificialintelligence-news.com/)


## 安裝所有依賴套件
```
pip install -r requirements.txt
```

## Gmail 設定

```
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"
```

## 執行方式
```
python main.py
```
