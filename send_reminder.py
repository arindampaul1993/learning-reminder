import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

PLAN = [
    {
        "week": 1,
        "title": "Overview of LLMs",
        "hours": "~5h",
        "phase": "Foundations",
        "tasks": [
            {"type": "video", "title": "3Blue1Brown 'Neural Networks' videos 1-3", "time": "~1h", "topic": "Parameters, backpropagation basics", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"},
            {"type": "video", "title": "Karpathy 'Intro to Large Language Models'", "time": "~1h", "topic": "LLM landscape overview", "url": "https://www.youtube.com/watch?v=zjkBMFhNj_g"},
            {"type": "build", "title": "Karpathy 'Building Micrograd'", "time": "~2.5h", "topic": "Neural net from scratch in Python", "url": "https://www.youtube.com/watch?v=VMj-3S1tku0"},
        ],
        "supplemental": ["Read: <a href='https://arxiv.org/abs/2203.15556'>Scaling Laws paper (Chinchilla)</a> for LLM scaling insight"],
        "goal": "Understand neural network basics + LLM training paradigms",
    },
    {
        "week": 2,
        "title": "Tokenization & Embeddings",
        "hours": "~4h",
        "phase": "Foundations",
        "tasks": [
            {"type": "build", "title": "Karpathy 'Let's build the GPT Tokenizer'", "time": "~2.25h", "topic": "BPE tokenization from scratch", "url": "https://www.youtube.com/watch?v=zduSFxRajkE"},
            {"type": "video", "title": "3Blue1Brown 'But what is a GPT?'", "time": "~26min", "topic": "Visual GPT intuition", "url": "https://www.youtube.com/watch?v=wjZofJX0v4M"},
            {"type": "video", "title": "3Blue1Brown 'Attention in Transformers'", "time": "~26min", "topic": "Attention mechanism visual", "url": "https://www.youtube.com/watch?v=eMlx5fFNoYc"},
        ],
        "supplemental": ["Read: <a href='https://jalammar.github.io/illustrated-word2vec/'>Jay Alammar 'Illustrated Word2Vec'</a> (vectorization basics)"],
        "goal": "Learn tokenization (BPE), embeddings, and intro to attention",
    },
    {
        "week": 3,
        "title": "Transformer Architecture Internals",
        "hours": "~3h",
        "phase": "Foundations",
        "tasks": [
            {"type": "read", "title": "The Illustrated Transformer (Jay Alammar)", "time": "~1h", "topic": "Visual transformer walkthrough", "url": "https://jalammar.github.io/illustrated-transformer/"},
            {"type": "read", "title": "Sebastian Raschka 'Understanding & Coding all Attention Types'", "time": "~1h", "topic": "Attention variants", "url": "https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention"},
            {"type": "read", "title": "Annotated Transformer (Harvard NLP)", "time": "~1h", "topic": "Code-level transformer", "url": "https://nlp.seas.harvard.edu/annotated-transformer/"},
        ],
        "supplemental": ["Optional: <a href='https://www.youtube.com/watch?v=bQ5BoolX9Ag'>Umar Jamil transformer video</a>"],
        "goal": "Understand Q/K/V attention, multi-head, FFNN, and transformer building blocks",
    },
    {
        "week": 4,
        "title": "Causal Attention / Build GPT",
        "hours": "~3h",
        "phase": "Foundations",
        "tasks": [
            {"type": "build", "title": "Karpathy 'Let's build GPT' (transformer from scratch)", "time": "~2h", "topic": "Build autoregressive transformer", "url": "https://www.youtube.com/watch?v=kCc8FmEb1nY"},
            {"type": "read", "title": "nanoGPT repo — explore and run", "time": "~1h", "topic": "Solidify foundations", "url": "https://github.com/karpathy/nanoGPT"},
        ],
        "supplemental": ["Go deeper: <a href='https://github.com/karpathy/nanoGPT'>nanoGPT repo</a> exploration"],
        "goal": "Build a simple autoregressive transformer",
    },
    {
        "week": 5,
        "title": "LLM Training at Scale",
        "hours": "~3h",
        "phase": "Training & Optimization",
        "tasks": [
            {"type": "video", "title": "Karpathy 'Deep Dive into LLMs like ChatGPT'", "time": "~2h", "topic": "End-to-end training pipeline", "url": "https://www.youtube.com/watch?v=7xTGNNLPyMI"},
            {"type": "read", "title": "Hugging Face 'Illustrating RLHF'", "time": "~30min", "topic": "Reinforcement learning from human feedback", "url": "https://huggingface.co/blog/rlhf"},
        ],
        "supplemental": ["<a href='https://huggingface.co/blog'>Hugging Face training workflow blogs</a>"],
        "goal": "End-to-end view of LLM training lifecycle (pretrain → post-train)",
    },
    {
        "week": 6,
        "title": "Quantization & Fine-Tuning",
        "hours": "~5h",
        "phase": "Training & Optimization",
        "tasks": [
            {"type": "read", "title": "Introduction to Weight Quantization", "time": "~45min", "topic": "INT8/INT4, KV cache optimization", "url": "https://mlabonne.github.io/blog/posts/Introduction_to_Weight_Quantization.html"},
            {"type": "read", "title": "Practical LoRA/QLoRA tips", "time": "~30min", "topic": "Parameter-efficient fine-tuning", "url": "https://huggingface.co/blog/lora-adapters-dynamic-loading"},
            {"type": "build", "title": "Hugging Face PEFT Quickstart (LoRA fine-tuning)", "time": "~2h", "topic": "Hands-on fine-tuning exercise", "url": "https://huggingface.co/docs/peft/quicktour"},
        ],
        "supplemental": ["<a href='https://www.deeplearning.ai/short-courses/quantization-fundamentals/'>DeepLearning.AI quantization short course</a> (optional)"],
        "goal": "Learn quantization basics and perform a fine-tuning exercise",
    },
    {
        "week": 7,
        "title": "Retrieval Augmented Generation",
        "hours": "~4h",
        "phase": "RAG & Retrieval",
        "tasks": [
            {"type": "video", "title": "LangChain 'RAG from Scratch' videos 1-5", "time": "~2h", "topic": "RAG architecture fundamentals", "url": "https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x"},
            {"type": "read", "title": "Pinecone HNSW explainer", "time": "~20min", "topic": "Vector search algorithms", "url": "https://www.pinecone.io/learn/series/faiss/hnsw/"},
            {"type": "build", "title": "ChromaDB hands-on", "time": "~1h", "topic": "Local vector database experimentation", "url": "https://docs.trychroma.com/docs/overview/getting-started"},
        ],
        "supplemental": ["<a href='https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/'>DeepLearning.AI vector DB intro</a> (optional)"],
        "goal": "Understand RAG architecture, indexing, and vector search basics",
    },
    {
        "week": 8,
        "title": "Hands-On RAG Implementation",
        "hours": "~6h",
        "phase": "RAG & Retrieval",
        "tasks": [
            {"type": "video", "title": "LangChain 'RAG from Scratch' videos 6-10", "time": "~2h", "topic": "Advanced RAG patterns", "url": "https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x"},
            {"type": "read", "title": "Prompt-injection safety basics", "time": "~30min", "topic": "Guardrails and safety", "url": "https://simonwillison.net/2022/Sep/12/prompt-injection/"},
            {"type": "build", "title": "DeepLearning.AI 'Chat with Your Data' course", "time": "~3h", "topic": "Build a full RAG chatbot", "url": "https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/"},
        ],
        "supplemental": [],
        "goal": "Build a working RAG chatbot with safety/guardrails",
    },
    {
        "week": 9,
        "title": "LLM Agents & Tool Calling",
        "hours": "~4h",
        "phase": "Agents & Production",
        "tasks": [
            {"type": "read", "title": "Anthropic 'Building Effective Agents'", "time": "~1h", "topic": "Agent design patterns", "url": "https://docs.anthropic.com/en/docs/build-with-claude/agentic"},
            {"type": "read", "title": "Lilian Weng 'LLM Powered Autonomous Agents'", "time": "~45min", "topic": "Agent architectures survey", "url": "https://lilianweng.github.io/posts/2023-06-23-agent/"},
            {"type": "build", "title": "LangGraph customer support agent tutorial", "time": "~2h", "topic": "Build agent with tool integration", "url": "https://langchain-ai.github.io/langgraph/tutorials/customer-support/customer-support/"},
        ],
        "supplemental": ["<a href='https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/'>DeepLearning.AI agent tutorials</a>"],
        "goal": "Build a basic agent with tool integration",
    },
    {
        "week": 10,
        "title": "MCP & Context Engineering",
        "hours": "~4h",
        "phase": "Agents & Production",
        "tasks": [
            {"type": "read", "title": "MCP quickstart & architecture docs", "time": "~1h", "topic": "Model Context Protocol", "url": "https://modelcontextprotocol.io/quickstart"},
            {"type": "read", "title": "Agent memory concepts", "time": "~20min", "topic": "Memory and context management", "url": "https://lilianweng.github.io/posts/2023-06-23-agent/#memory"},
            {"type": "build", "title": "Build an MCP server hands-on", "time": "~2h", "topic": "Implement MCP server", "url": "https://modelcontextprotocol.io/quickstart/server"},
        ],
        "supplemental": [],
        "goal": "Understand multi-agent memory and context engineering",
    },
    {
        "week": 11,
        "title": "LLM Evals & Production Tradeoffs",
        "hours": "~4h",
        "phase": "Agents & Production",
        "tasks": [
            {"type": "read", "title": "Why evals matter (Hamel Husain)", "time": "~30min", "topic": "Eval philosophy", "url": "https://hamel.dev/blog/posts/evals/"},
            {"type": "read", "title": "LLM-as-judge tutorial", "time": "~30min", "topic": "Using LLMs to evaluate LLMs", "url": "https://eugeneyan.com/writing/llm-evaluators/"},
            {"type": "read", "title": "Patterns for LLM systems in production", "time": "~45min", "topic": "Production design patterns", "url": "https://eugeneyan.com/writing/llm-patterns/"},
            {"type": "build", "title": "Set up basic evals (DeepEval or custom)", "time": "~1.5h", "topic": "Build evaluation harness", "url": "https://docs.confident-ai.com/docs/getting-started"},
        ],
        "supplemental": [],
        "goal": "Evaluate LLM outputs & understand tradeoffs (prompting vs RAG vs fine-tune)",
    },
    {
        "week": 12,
        "title": "Reasoning Models",
        "hours": "~3h",
        "phase": "Agents & Production",
        "tasks": [
            {"type": "read", "title": "OpenAI 'Learning to Reason with LLMs'", "time": "~20min", "topic": "Reasoning model design", "url": "https://openai.com/index/learning-to-reason-with-llms/"},
            {"type": "read", "title": "Chain-of-Thought prompting guide", "time": "~20min", "topic": "CoT techniques", "url": "https://www.promptingguide.ai/techniques/cot"},
            {"type": "build", "title": "Try reasoning model demos (DeepSeek-R1, o1)", "time": "~1h", "topic": "Hands-on reasoning models", "url": "https://chat.deepseek.com/"},
        ],
        "supplemental": ["<a href='https://arxiv.org/abs/2501.12948'>DeepSeek-R1 paper</a> skim"],
        "goal": "Understand chain-of-thought prompting and reasoning-style outputs",
    },
    {
        "week": 13,
        "title": "Image & Video Models",
        "hours": "~3h",
        "phase": "Multimodal & Capstone",
        "tasks": [
            {"type": "read", "title": "CLIP and multimodal model basics", "time": "~1h", "topic": "Vision-language connection", "url": "https://openai.com/index/clip/"},
            {"type": "read", "title": "GAN fundamentals overview", "time": "~1h", "topic": "Generative adversarial networks", "url": "https://developers.google.com/machine-learning/gan"},
            {"type": "build", "title": "Explore multimodal API (Claude vision / GPT-4V)", "time": "~1h", "topic": "Hands-on multimodal", "url": "https://docs.anthropic.com/en/docs/build-with-claude/vision"},
        ],
        "supplemental": [],
        "goal": "Learn how to connect vision & text models",
    },
    {
        "week": 14,
        "title": "Diffusion Models",
        "hours": "~4h",
        "phase": "Multimodal & Capstone",
        "tasks": [
            {"type": "read", "title": "DDPM paper walkthrough / Lil'Log diffusion guide", "time": "~1.5h", "topic": "Diffusion fundamentals", "url": "https://lilianweng.github.io/posts/2021-07-11-diffusion-models/"},
            {"type": "build", "title": "Stable Diffusion pipeline hands-on", "time": "~2h", "topic": "Build image generation pipeline", "url": "https://huggingface.co/docs/diffusers/quicktour"},
        ],
        "supplemental": ["<a href='https://huggingface.co/learn/diffusion-course/'>Hugging Face diffusion models course</a>"],
        "goal": "Understand diffusion process and build an image generation pipeline",
    },
    {
        "week": 15,
        "title": "Capstone Build Phase",
        "hours": "~10h",
        "phase": "Multimodal & Capstone",
        "tasks": [
            {"type": "build", "title": "Build capstone: RAG + Agent + Evals system", "time": "~10h", "topic": "Full end-to-end AI application", "url": "https://github.com/arindampaul1993"},
        ],
        "supplemental": ["Options: Document Q&A, multi-tool agent, fine-tuned model deployment"],
        "goal": "Build a complete AI system using all learned techniques",
    },
    {
        "week": 16,
        "title": "AI Engineering Principles & Polish",
        "hours": "~3h",
        "phase": "Multimodal & Capstone",
        "tasks": [
            {"type": "read", "title": "AI engineering best practices roundup", "time": "~1h", "topic": "Production principles", "url": "https://applied-llms.org/"},
            {"type": "build", "title": "Polish capstone: docs, demo, deploy", "time": "~2h", "topic": "Ship it", "url": "https://huggingface.co/spaces"},
        ],
        "supplemental": ["Deploy on <a href='https://huggingface.co/spaces'>HuggingFace Spaces</a> or Vercel"],
        "goal": "Finalize capstone project and publish portfolio piece",
    },
]


def get_current_week(start_date_str):
    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    today = datetime.now()
    delta = (today - start).days
    week = delta // 7 + 1
    return min(max(week, 1), 16)


def build_email_html(week_data, week_num):
    type_icons = {"video": "🎥", "read": "📖", "build": "🛠"}

    tasks_html = ""
    for task in week_data["tasks"]:
        icon = type_icons.get(task["type"], "📌")
        url = task.get("url", "")
        title_html = f'<a href="{url}" style="color: #81c784; text-decoration: underline;">{task["title"]}</a>' if url else f'<span style="color: #e0e0e0;">{task["title"]}</span>'
        tasks_html += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #2d2d2d;">
                <span style="font-size: 18px;">{icon}</span>
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #2d2d2d;">
                <strong>{title_html}</strong><br>
                <span style="color: #888; font-size: 13px;">{task['time']} — {task['topic']}</span>
            </td>
        </tr>"""

    supplemental_html = ""
    if week_data["supplemental"]:
        items = "".join(f"<li style='color: #888; margin: 4px 0;'>{s}</li>" for s in week_data["supplemental"])
        supplemental_html = f"""
        <div style="margin-top: 20px; padding: 12px; background: #1a1a2e; border-radius: 6px;">
            <strong style="color: #64b5f6;">Supplemental (Optional):</strong>
            <ul style="margin: 8px 0; padding-left: 20px;">{items}</ul>
        </div>"""

    progress_pct = round(week_num / 16 * 100)
    progress_bar = f"""
    <div style="background: #2d2d2d; border-radius: 10px; height: 20px; margin: 16px 0; overflow: hidden;">
        <div style="background: linear-gradient(90deg, #4caf50, #81c784); height: 100%; width: {progress_pct}%; border-radius: 10px;"></div>
    </div>
    <p style="color: #888; text-align: center; font-size: 13px;">Week {week_num} of 16 — {progress_pct}% complete</p>"""

    return f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace; max-width: 600px; margin: 0 auto; background: #0d1117; color: #e0e0e0; padding: 32px; border-radius: 12px;">
        <h1 style="color: #4caf50; margin: 0;">🧠 Week {week_num}: {week_data['title']}</h1>
        <p style="color: #888; margin: 8px 0 0;">Phase: <strong style="color: #64b5f6;">{week_data['phase']}</strong> · Estimated: <strong>{week_data['hours']}</strong></p>

        {progress_bar}

        <h2 style="color: #81c784; border-bottom: 1px solid #2d2d2d; padding-bottom: 8px; margin-top: 28px;">This Week's Tasks</h2>
        <table style="width: 100%; border-collapse: collapse;">{tasks_html}</table>

        {supplemental_html}

        <div style="margin-top: 24px; padding: 16px; background: #1b2838; border-left: 4px solid #4caf50; border-radius: 4px;">
            <strong style="color: #4caf50;">🎯 Goal:</strong>
            <p style="color: #e0e0e0; margin: 8px 0 0;">{week_data['goal']}</p>
        </div>

        <p style="color: #555; font-size: 12px; margin-top: 32px; text-align: center;">
            Sent by your learning-reminder agent · <a href="https://github.com/arindampaul1993/learning-reminder" style="color: #4caf50;">GitHub</a>
        </p>
    </div>"""


def send_email():
    gmail_address = os.environ["GMAIL_ADDRESS"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    start_date = os.environ.get("START_DATE", "2026-05-05")

    week_num = get_current_week(start_date)
    week_data = PLAN[week_num - 1]

    subject = f"🧠 Week {week_num}/16: {week_data['title']} — AI Engineering Roadmap"
    html_body = build_email_html(week_data, week_num)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Learning Agent <{gmail_address}>"
    msg["To"] = gmail_address

    plain_text = f"Week {week_num}: {week_data['title']}\n\nTasks:\n"
    for task in week_data["tasks"]:
        plain_text += f"- [{task['type']}] {task['title']} ({task['time']})\n"
    plain_text += f"\nGoal: {week_data['goal']}\n"

    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, gmail_password)
        server.sendmail(gmail_address, gmail_address, msg.as_string())

    print(f"Sent Week {week_num} reminder: {week_data['title']}")


if __name__ == "__main__":
    send_email()
