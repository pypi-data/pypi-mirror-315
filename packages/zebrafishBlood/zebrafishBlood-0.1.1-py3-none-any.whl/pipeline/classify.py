import numpy as np
import torch
import torchvision.transforms as transforms

MPATH = '/home/eunhye/fishproj/pipeline_new/models/qcmodel.pkl'

# Predicts image quality class
#    Blank: returnVal == 0
#    Cluster: returnVal == 1
#    Standard: returnVal == 2

def classify(model, inImg, devicenum):
    returnVal = None

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x[:3, :, :]),
    ])

    inImg = inImg.resize((100, 50))
    inImg = np.array(inImg)
    inImg = transform(inImg)
    inImg = torch.unsqueeze(inImg, 0)
    inImg = inImg.to(devicenum)
    
    with torch.no_grad():
        out = model(inImg)
    _, returnVal = torch.max(out, 1)

    return returnVal