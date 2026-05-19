import os
# 从刚刚封装的核心逻辑文件中引入工作流函数
from agent_core import run_academic_workflow

if __name__ == "__main__":
    # 配置你的输入和输出
    target_pdf = "sample_paper.pdf"  # 请确保同目录下有这个 PDF 文件
    output_md = "论文拆解脑图.md"
    
    # 检查文件是否存在并执行
    if os.path.exists(target_pdf):
        print("🚀 启动学术科研与深度逻辑拆解 Agent...")
        run_academic_workflow(target_pdf, output_md)
        print("✅ 任务全部结束。")
    else:
        print(f"⚠️ 找不到文件: {target_pdf}\n请先将需要拆解的 PDF 放入同一文件夹，并确认名称正确。")