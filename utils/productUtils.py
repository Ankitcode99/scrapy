
def generateIdFromProductTitle(productTitle: str) -> str:
    return productTitle.strip().lower().replace(' ','_')


aa = "Advanced Biotech Hemocoll - Dentalstall India"
print(generateIdFromProductTitle(aa))