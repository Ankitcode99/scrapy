
def generateIdFromProductTitle(productTitle: str) -> str:
    return productTitle.strip().lower().replace(' ','_')

