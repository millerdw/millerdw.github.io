import torch, torchvision
import matplotlib.pyplot as plt
import numpy as np

from IPython.core.debugger import set_trace

def ConfusionMatrix(model,dataSet):
    confusion = np.zeros((10,10))
    with torch.no_grad():
        images,labels = torch.utils.data.dataloader.default_collate(dataSet)
        _,predictedlabels = model.cpu()(images).max(1)
        for i in range(10):
            for j in range(10):
                confusion[i,j]+=((predictedlabels==i) & (labels==j)).sum()
    return confusion


def PrintConfusionMatrix(model,dataSet):
    confusionMatrix=ConfusionMatrix(model,dataSet)
    
    print("Confusion Matrix:")
    print("\n".join(["".join(["{:8.0f}".format(item) for item in row]) for row in confusionMatrix]))

    print("Recall")
    print("".join(["{:8.1%}".format(recall) for recall in np.diag(confusionMatrix/np.sum(confusionMatrix,0))]))

    print("Precision")
    print("".join(["{:8.1%}".format(precision) for precision in np.diag(confusionMatrix/np.sum(confusionMatrix,1))]))

    print("Accuracy")
    print("{:8.1%}".format(np.sum(np.diag(confusionMatrix))/np.sum(confusionMatrix)))
    
    
def PlotTrainingCurves(trainStatistics):
    fig,ax=plt.subplots(1,2,figsize=(14,5))
    ax[0].plot(trainStatistics[0],label="Training Log Loss")
    ax[0].plot(trainStatistics[2],label="Validation Log Loss")
    ax[0].legend()
    ax[1].plot(trainStatistics[1],label="Training Accuracy")
    ax[1].plot(trainStatistics[3],label="Validation Accuracy")
    ax[1].legend();
    
    
def PlotImages(images, ax=None) :
    """
    Plots images in a 4D mini-batch Tensor of shape (B x C x H x W) in a 2D grid
    """
    #convert 4D mini-batch Tensor of shape (B x C x H x W) into a list of 3D Tensors of shape (C x H x W)
    listImages=[images[i,:,:,:] for i in range(images.shape[0])]
    #convert list into a single 2d image (grid)
    gridImages=torchvision.utils.make_grid(listImages).numpy()
    #plot grid image
    if ax is None:
        ax = plt.gca()
    ax.imshow(np.transpose(gridImages,(1, 2, 0)))
