import os
from pypdf import PdfReader


folder = "reports/tearsheets"


files = sorted(os.listdir(folder))[:5]


for file in files:

    path = os.path.join(folder,file)

    print("\n====================")
    print(file)

    reader = PdfReader(path)

    print("Pages =", len(reader.pages))

    for i,page in enumerate(reader.pages):

        text = page.extract_text()

        if text is None:
            print("Page", i+1, "No text extracted")
        else:
            print(
                "Page",
                i+1,
                "Characters:",
                len(text)
            )