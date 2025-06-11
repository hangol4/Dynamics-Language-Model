# documentation: https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html

import pymupdf4llm
md_text = pymupdf4llm.to_markdown('../Binney_and_Tremaine_Extract.pdf')

with open("output/pymupdf4llm Binney_and_Tremaine.md", "w") as f:
    f.write(md_text)