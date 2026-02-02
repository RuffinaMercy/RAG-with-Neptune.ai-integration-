# import fitz  # PyMuPDF
# import os
# from typing import List


# class PDFHighlighter:
#     def highlight_pdf(self, pdf_path: str, keywords: str):
#         if not os.path.exists(pdf_path):
#             return None, [], ["PDF not found"]

#         doc = fitz.open(pdf_path)
#         keywords_list = [k.strip() for k in keywords.split(",") if k.strip()]

#         highlighted_words = []

#         for page in doc:
#             for word in keywords_list:
#                 text_instances = page.search_for(word)
#                 for inst in text_instances:
#                     highlight = page.add_highlight_annot(inst)
#                     highlight.update()
#                     highlighted_words.append(word)

#         output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
#         doc.save(output_path)
#         doc.close()

#         return output_path, highlighted_words, []





import fitz  # PyMuPDF
import os
from typing import List


class PDFHighlighter:
    def highlight_pdf(self, pdf_path: str, keywords: str):
        if not os.path.exists(pdf_path):
            return None, [], [], ["PDF not found"]

        doc = fitz.open(pdf_path)

        keywords_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]

        found_words = set()
        not_found_words = set(keywords_list)

        for page in doc:
            text = page.get_text().lower()
            for word in keywords_list:
                if word in text:
                    text_instances = page.search_for(word)
                    for inst in text_instances:
                        highlight = page.add_highlight_annot(inst)
                        highlight.update()
                    found_words.add(word)
                    if word in not_found_words:
                        not_found_words.remove(word)

        output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
        doc.save(output_path)
        doc.close()

        return output_path, list(found_words), list(not_found_words), []
