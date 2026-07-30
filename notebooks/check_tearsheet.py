import os

folder = "reports/tearsheets"

print("Exists:", os.path.exists(folder))

pdfs = sorted(
    f for f in os.listdir(folder)
    if f.endswith(".pdf")
)

print("PDF Count:", len(pdfs))

print("\nTCS files:")
for pdf in pdfs:
    if "TCS" in pdf.upper():
        print(pdf)