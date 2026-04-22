from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)  # Set to True to enable plugins
result = md.convert("./.local/input_doc.docx")

with open("./.local/output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
