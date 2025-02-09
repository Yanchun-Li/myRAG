
import glob
import os
from docx2pdf import convert

# 需要转换的文件夹路径（含中文及特殊字符时，建议使用原始字符串 r"..."）
folder_path = r"D:\MemoTrace\data\聊天记录\罗曼蒂克·怀芙💗(wxid_wq8yrwon1se022)"

# 获取该文件夹下所有 .docx 文件（通配符 * 可以匹配多份 docx）
docx_files = glob.glob(os.path.join(folder_path, "*.docx"))

# 遍历并逐个转换
for docx_file in docx_files:
    # 不带扩展名的文件路径（如 "D:\MemoTrace\data\...\罗曼蒂克·怀芙💗_1"）
    base_name = os.path.splitext(docx_file)[0]
    # 目标 PDF 路径（与 docx 同名、同文件夹）
    pdf_file = base_name + ".pdf"

    # 调用 docx2pdf 进行转换
    try:
        convert(docx_file, pdf_file)
        print(f"转换成功: {docx_file} → {pdf_file}")
    except Exception as e:
        print(f"转换失败: {docx_file}, 错误原因: {e}")
