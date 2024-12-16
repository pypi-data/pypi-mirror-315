# A wrapper function for pytorch NN model

import torch
import numpy as np
from tqdm import tqdm    
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

class NNWrapper():
    def __init__(self, model, criterion, optimizer, reconstruct=False, 
                 device='cpu'):
        """
        Parameters
        ----------
        model: torch.nn.Module
            The model to use / train
        criterion: criterion in torch.nn
            E.g., torch.nn.CrossEntropyLoss()
        optimizer: optimizer in torch.optim
            E.g., torch.optim.SGD(model.parameters(), lr=0.003, momentum=0.8)
        reconstruct: bool
            If True, it will constructure the same format of input, e.g., (X, y)
        device: str
            To set the device for CPU or GPU, e.g., 'cuda:0'
        """
        self.model = model.to(torch.device(device))
        self.device = device
        self.criterion = criterion
        self.optimizer = optimizer
        self.reconstruct = reconstruct
        
    def train(self, train_loader, verbose=False):
        self.model.train()
        train_loss = 0
        for sample in train_loader:
            if len(sample) == 1:
                data = sample[0].to(torch.device(self.device))
                target = data
            elif len(sample) == 2:
                data, label = sample
                data = data.to(torch.device(self.device))
                label = label.to(torch.device(self.device))
                target = (data, label) if self.reconstruct else label
            else:
                raise NotImplementedError
            
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()
            train_loss += loss.item() * data.size(0)
            
        train_loss = train_loss / len(train_loader.dataset)
        return train_loss
    
    def predict(self, test_loader, compute_loss=False):
        self.model.eval()
        y_outputs = []
        test_loss = 0
        with torch.no_grad():
            for sample in test_loader:
                if len(sample) == 1:
                    data = sample[0].to(torch.device(self.device))
                    target = data
                elif len(sample) == 2:
                    data, label = sample
                    data = data.to(torch.device(self.device))
                    label = label.to(torch.device(self.device))
                    target = (data, label) if self.reconstruct else label
                else:
                    raise NotImplementedError
                
                output = self.model(data)
                y_outputs.append(output)
                
                if compute_loss:
                    loss = self.criterion(output, target)
                    test_loss += loss.item() * data.size(0)
        
        y_outputs = torch.cat(y_outputs)     
        test_loss = test_loss / len(test_loader.dataset)
        return y_outputs, test_loss
    
    def fit(self, train_loader, epoch, validation_loader=None, verbose=False):
        self.train_losses = np.zeros(epoch)
        self.valid_losses = np.zeros(epoch)
        for i in tqdm(range(epoch)):
            self.train_losses[i] = self.train(train_loader, verbose=verbose)
            
            if validation_loader is not None:
                _y_pred, self.valid_losses[i] = self.predict(
                    validation_loader, compute_loss=True
                )
            
            if verbose:
                print('Loss - Epoch: %s \tTraining: %.6f \tValidation: %.6f\n'
                      %(i, self.train_losses[i], self.valid_losses[i]))
    

def evaluate(y_scores, y_obs, mode='classification'):
    """Under development
    """
    y_preds  = torch.argmax(y_scores, 1).cpu().data.numpy()
    y_scores = y_scores[:, 1].cpu().data.numpy() 
    y_obs    = y_obs[:, 1].cpu().data.numpy()
    
    acc = np.sum(y_preds == y_obs) / len(y_preds)
    auc = roc_auc_score(y_obs, y_scores)
    confu = confusion_matrix(y_obs, y_preds)
    
    return acc, auc, confu
