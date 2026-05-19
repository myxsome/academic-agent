import streamlit as st
import os
import time
from agent_core import run_academic_workflow
 

# ================= 1. 页面配置与可爱风 CSS =================
st.set_page_config(page_title="神奇森林智能卷宗处", page_icon="🐰", layout="centered")

st.markdown("""
    <style>
    /* 引入国内镜像的开源卡通字体：站酷快乐体 */
    @import url('https://fonts.loli.net/css2?family=ZCOOL+KuaiLe&display=swap');

    /* 核心背景与字体 */
    .stApp {
        background-color: #FFF9F0; 
    }
    
    html, body, [class*="css"]  {
        font-family: 'ZCOOL KuaiLe', 'YouYuan', '幼圆', cursive !important;
    }

    h1, h2, h3 {
        color: #1A3C6C !important; 
    }
    
    /* ---------------- 【本次修复核心】 ---------------- */
    /* 统一所有聊天气泡的样式，干掉默认的丑灰色！ */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF !important; /* 统一改成干净纯白底色 */
        border: 2px dashed #FFAB40 !important; /* 加上可爱的胡萝卜橙色虚线边框 */
        border-radius: 20px !important;       /* 大圆角，更可爱 */
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 10px rgba(255, 171, 64, 0.15); /* 微微的橙色发光阴影 */
    }
    
    /* 让头像也变得圆润可爱，加上一圈绿色的描边 */
    div[data-testid="stChatMessageAvatar"] {
        border: 2px solid #4CAF50 !important; 
        border-radius: 50% !important;
        background-color: #FFF9F0 !important;
    }
    /* ------------------------------------------------ */
    
    /* 卡片式容器 (文件上传区和结果区) */
    .stFileUploader, .stMarkdownContainer {
        border-radius: 20px !important;
        border: 2px dashed #FFAB40 !important; 
        padding: 20px;
        background: white;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: #4CAF50 !important; 
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background-color: #FF7043 !important; 
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

# ================= 2. 朱迪与尼克的角色引导 =================
st.title("神奇森林智能卷宗处")

if os.path.exists("banner.png"):
    st.image("banner.png", caption="欢迎来到森林分局！", use_container_width=True)

# 【修复核心】写一个安全读取图片的辅助函数
# 自动获取当前 app.py 所在的“绝对路径”文件夹
current_dir = os.path.dirname(os.path.abspath(__file__))

# 极简版安全函数：直接返回绝对路径，抛弃笨重的 PIL
def get_safe_avatar(image_name, fallback_emoji):
    image_path = os.path.join(current_dir, image_name)
    if os.path.exists(image_path):
        return image_path  # Streamlit 支持直接传路径，这样最稳定！
    return fallback_emoji

# 使用极简函数加载头像
avatar_judy = get_safe_avatar("rabbit.png", "🐰")
avatar_nick = get_safe_avatar("fox.png", "🦊")

# 聊天框：把 st.write 改成 st.markdown，并强制加深颜色，杜绝“隐身”
with st.chat_message("assistant", avatar=avatar_judy):
    st.markdown("<span style='color:#333333; font-size:16px;'>我是兔子警官！在神奇森林里，“任何人都能成为任何人”，包括成为学术大神！别被那些英文长篇大论吓到了。</span>", unsafe_allow_html=True)

with st.chat_message("user", avatar=avatar_nick):
    st.markdown("<span style='color:#333333; font-size:16px;'>嘿，小兔子，别太卷了。让 Agent 帮我们干活吧，咱们去喝🍹。</span>", unsafe_allow_html=True)


# ================= 3. 核心交互区 =================
uploaded_file = st.file_uploader("📂 投喂一份卷宗 (PDF 论文)", type="pdf")

if uploaded_file is not None:
    temp_pdf_path = "temp_paper.pdf"
    output_md_path = "论文拆解脑图.md"
    
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    st.success(f"✅ 警员报告：卷宗《{uploaded_file.name}》已存入档案库！")

    if st.button("🚨 呼叫Flash开始拆解", use_container_width=True):
        
        progress_bar = st.progress(0)
        with st.status("🦥 正在努力加载中... 请耐心... 等...... 待......", expanded=True) as status:
            st.write("正在识别动物字符...")
            time.sleep(1)
            progress_bar.progress(30)
            
            st.write("正在查阅 Tundratown 知识库...")
            run_academic_workflow(temp_pdf_path, output_md_path)
            progress_bar.progress(100)
            status.update(label="🎉 拆解完成！速度比Flash本尊快多了！", state="complete", expanded=False)
            
            if os.path.exists(output_md_path):
                with open(output_md_path, "r", encoding="utf-8") as f:
                    result_text = f.read()
                
                st.balloons() 
                st.markdown("### 📋 智能脑图简报")
                with st.container(border=True):
                    st.markdown(result_text)
                
                st.download_button(
                    label="📥 领取你的调查报告 (Markdown 格式)",
                    data=result_text,
                    file_name=output_md_path,
                    mime="text/markdown",
                    use_container_width=True
                )