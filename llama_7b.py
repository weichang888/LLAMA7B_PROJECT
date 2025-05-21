import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch

# If this is your first time using a Hugging Face token, you need to log in once. You can comment out this line after logging in.
# login()

# Initialize model
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

#  Directory settings
data_dir = "./data"
output_dir = "./summaries"
os.makedirs(output_dir, exist_ok=True)

#  Summarize each article one by one
for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        #  Extract title and text
        try:
            title = content.split("title:")[1].split("text:")[0].strip()
            article = content.split("text:")[1].strip()
        except IndexError:
            print(f"⚠️ Unable to parse format: {filename}")
            continue

        #  Control length (keep at most 3500 tokens for model input)
        max_input_tokens = 3500
        tokens = tokenizer.tokenize(article)
        if len(tokens) > max_input_tokens:
            tokens = tokens[:max_input_tokens]
            article = tokenizer.convert_tokens_to_string(tokens)

        chat = [
            {"role": "system", "content": "You are a helpful language model assistant skilled at summarization."},
            {"role": "user", "content": f"Please list the main points of the following article in bullet points, using clear and concise English sentences:\n\n{article}"}
        ]

        prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        # Model generation
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.7
        )

        # Only extract the newly generated tokens (excluding the prompt entirely)
        input_len = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_len:]
        summary = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

        # Save result (only include title + summary)
        output_path = os.path.join(output_dir, f"{filename}_summary.txt")
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(f"Title: {title}\n\nSummary:\n{summary}")

        print(f"Completed: {filename}")
