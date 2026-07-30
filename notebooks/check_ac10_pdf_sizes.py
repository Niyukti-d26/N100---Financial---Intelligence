import os

folder = "reports/tearsheets"

pdfs = sorted(
    [
        f
        for f in os.listdir(folder)
        if f.endswith(".pdf")
    ]
)

print(
    "PDF Count =",
    len(pdfs)
)

print()

for pdf in pdfs[:15]:
    size = (
        os.path.getsize(
            os.path.join(folder, pdf)
        )
        / 1024
    )

    print(
        pdf,
        round(size, 2),
        "KB"
    )