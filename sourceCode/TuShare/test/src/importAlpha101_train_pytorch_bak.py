'''
Created on 2017年9月30日

@author: moonlit
'''
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from torch.autograd import Variable
    
#参数配置
input_size = 46
output_size = 1
num_epochs = 60
learning_rate = 0.001    

# Linear Regression Model
class LinearRegression(nn.Module):
    def __init__(self, input_size, output_size):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(input_size, output_size)  
    
    def forward(self, X ,code_return  ):
        out  = []
        
        data = pd.DataFrame()
        
        data["code"] = X["code"].values
        X = X.drop('code', 1)
        X = np.array(X, dtype=np.float32)       

        for x in X :
            x = x.reshape(1,-1)
#             print(x.shape)
            x = Variable(torch.from_numpy(x))
            res = self.linear( x )
            out.append( res.data.numpy() )
        
        data["score"] = out 
        
        data = data.sort_values(by = "score", ascending =False)
        
        codes = data["code"].values
        codes = codes[:20]

        Return = code_return[code_return["code"].isin(codes) == True ]
        Return = Return["return"].values
         
        return Variable(torch.from_numpy(np.array([Return.sum()],dtype=np.float32))) , codes

def train(  X , code_returns , total_returns ,model,epochs_num = 0):
    # Loss and Optimizer
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    
    # Train the Model 
    for epoch in range(epochs_num):
        # Convert numpy array to torch Variable
        for x , code_return , total_return in zip (X , code_returns , total_returns) :
            targets = Variable(torch.from_numpy(np.array(total_return, dtype=np.float32)))
        
            # Forward + Backward + Optimize
            optimizer.zero_grad()  
            outputs,_ = model(x,code_return)
            
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
        
        if (epoch+1) % 5 == 0:
            print ('Epoch [%d/%d], Loss: %.4f' 
                   %(epoch+1, epochs_num, loss.data[0]))
            
def get_data(begin = "2017-01-01" , split ="2017-02-01" , end = "2017-10-01"):
    import getStockData as gsd
        
    train_data = gsd.get_101_data(start=begin, end = split)
    test_data  = gsd.get_101_data(start=split, end = end  )
    return train_data , test_data 
    
train_data , test_data = get_data(begin="2017-01-01", split="2017-01-15", end="2017-02-01")
        
model = LinearRegression(input_size, output_size)
train(
      X            = train_data["data_101"]    ,
      code_returns = train_data["CodeReturn"]  ,
      total_returns= train_data["TotalReturn"] , 
      model        = model                     , 
      epochs_num   = num_epochs                ,
      )


        
# Plot the graph
prereturn , codes = model(Variable(torch.from_numpy(test_data["data_101"])),
                  test_data["code_return"]
                  )

prereturn = prereturn.data.numpy()

plt.plot(train_data["data_101"], train_data["total_return"], 'ro', label='Original data')
plt.plot(test_data["data_101"], prereturn, label='Fitted line')
plt.legend()
plt.show()

# Save the Model
torch.save(model.state_dict(), 'd:\101_model.pkl')        