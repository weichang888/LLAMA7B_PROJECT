import subprocess
from datetime import datetime

print("Starting automation process")

# Step 1: Crawl data
print("Step 1: Running crawler")
subprocess.run(["python", "CrawlerScript.py"], check=True)

# Step 2: Generate summary
print("Step 2: Generating summary")
subprocess.run(["python", "llama_7b.py"], check=True)

# Step 3: Compile Word document
print("Step 3: Compiling Word document")
subprocess.run(["python", "word.py"], check=True)

# Step 4: Send Email
print("Step 4: Sending Email")
subprocess.run(["python", "receive.py"], check=True)

print("All tasks completed at", datetime.now())
