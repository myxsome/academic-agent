import fitz  # PyMuPDF
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中安全读取 API Key，如果没有找到会返回 None
API_KEY = os.getenv("MY_API_KEY")
BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def parse_pdf(file_path):
    """
    Parser Agent: 提取 PDF 文本并做简单清洗
    """
    print(f"📄 [Parser] 正在解析文献: {file_path}")
    text = ""
    try:
        pdf_document = fitz.open(file_path)
        # 学术论文通常前 5-8 页包含了核心的 Abstract, Intro 和 Method
        num_pages = min(8, pdf_document.page_count) 
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text") + "\n"
        print(f"✅ [Parser] 解析完成，共提取 {len(text)} 个字符。")
        return text
    except Exception as e:
        print(f"❌ [Parser] 解析失败: {e}")
        return None

def call_llm_agent(role_prompt, user_content, temperature=0.3):
    """
    基础调用模块：输入系统设定（Prompt）和用户内容，返回模型结果
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-pro", # 替换为你使用的具体模型名称
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=temperature,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ [LLM] 调用失败: {e}")
        return None

def run_academic_workflow(pdf_path, output_filename):
    """
    核心工作流：串联解析、总结、拆解和格式化
    """
    # 1. 启动 Parser
    paper_text = parse_pdf(pdf_path)
    if not paper_text:
        return

    # 2. 启动 Summarizer Agent (总结摘要)
    print("🤖 [Summarizer] 正在提取核心摘要...")
    summarizer_prompt = """
    你是一个资深的学术研究员。请阅读以下论文文本，并用 300 字以内的中文大白话，
    总结这篇文章的 1. 研究背景 2. 核心贡献 3. 最终结论。
    不需要任何寒暄，直接输出结果。
    """
    summary = call_llm_agent(summarizer_prompt, paper_text[:15000])

    # 3. 启动 Logician Agent (深度逻辑拆解)
    print("🧠 [Logician] 正在剥离核心逻辑脑图...")
    logician_prompt = """
    你是一个顶级的学术拆解专家，擅长从复杂的论文中剥离出最核心的逻辑骨架。
    你的任务是阅读提供的论文文本，并严格按照以下结构输出内容：

    ## 一、 一句话痛点
    (现有的技术/方案存在什么根本缺陷？)

    ## 二、 核心创新机制
    (作者提出了什么创新机制来解决这个痛点？请用通俗的比喻解释)

    ## 三、 核心逻辑论证链
    - 论点 A：... （支撑证据或实验数据：...）
    - 论点 B：... （支撑证据或实验数据：...）
    
    必须严格使用 Markdown 格式输出，不要包含多余的解释。
    注意排版规范：每个标题（##）和列表（-）的上方和下方，必须保留一个空行！
    """
    logic_tree = call_llm_agent(logician_prompt, paper_text[:20000])

    # 4. 启动 Formatter Agent (保存输出)
    print("💾 [Formatter] 正在生成 Markdown 笔记...")
    final_output = f"# 论文深度拆解笔记\n\n## 快速摘要\n\n{summary}\n\n---\n\n{logic_tree}\n"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(final_output)
    print(f"🎉 跑通啦！拆解报告已保存至：{output_filename}")