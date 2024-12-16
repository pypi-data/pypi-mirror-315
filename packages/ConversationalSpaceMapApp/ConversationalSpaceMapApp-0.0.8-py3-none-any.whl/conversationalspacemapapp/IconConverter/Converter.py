import icnsutil

# Load the PNG file
file = "./resources/icon.png"
output = ""

# compose
img = icnsutil.IcnsFile()
img.add_media(file=file)
img.write('./resources/icon.icns')
