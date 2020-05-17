from PIL import Image


def photoConverter(photoList, filename="untitle"):
    imageList = []
    for path in photoList:
        imageList.append(Image.open(path))

    first = imageList[0]
    del imageList[0]
    path = "docs/" + filename + ".pdf"
    print(filename)
    if len(imageList) != 0:
      first.save(path, save_all=True, append_images=imageList)
    else:
        first.save(path)
    return path

if __name__ == '__main__':
    pathList = ["photos/arpufuer.png",]
    photoConverter(pathList)