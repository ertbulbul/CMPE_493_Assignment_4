import re

def punctiationCleaner(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'[^\w\s]', ' ', text)
    return text


ert = punctiationCleaner("hello,hello,slm,nsdh.dfsh")
print(ert)