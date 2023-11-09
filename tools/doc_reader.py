import os,docx
def transfer_doc2string(file_location):
    """
    将doc转换成string
    """
    doc = docx.Document(file_location)
    lines = ""
    for i in range(len(doc.paragraphs)):
        lines = lines + doc.paragraphs[i].text+"\n"
    return lines