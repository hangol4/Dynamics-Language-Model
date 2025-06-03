# documentation: https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html

import pymupdf4llm
md_text = pymupdf4llm.to_markdown('../Petersen2021.pdf')

print(md_text)
with open("pymupdf4llm Petersen2021.md", "w") as f:
    f.write(md_text)