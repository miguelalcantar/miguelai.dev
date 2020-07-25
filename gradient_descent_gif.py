import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import imageio

# Generating numbers
X = 10 * np.random.rand(100,1)
y = 5 + 3 * X + 2 * np.random.randn(100,1)

def batch_gradient_descent(X,y,alpha=0.0001,it=15):
    """
    where:
    X -> are the input variables
    y -> the output value
    alpha -> the learning rate
    it -> iterations
    """
    # concatenating X's with X0's which are equal to 1
    X_ = np.c_[np.ones((len(X),1)),X]
    # Initializing theta randomly
    theta = np.random.randn(len(X[0]) + 1,1)
    i = 0

    yield theta

    while i < it:
        
        # pred: theta * X for every value
        pred = X_.dot(theta)
        # difference between prediction and actual output
        diff = y - pred
        
        J_theta = diff.T.dot(X_)
        # theta := theta + alpha * J_theta
        theta += alpha * J_theta.T
        
        i += 1

        yield theta

def stochastic_gradient_descent(X,y,alpha=0.001):
    """
    where:
    X -> are the input variables
    y -> the output value
    alpha -> the learning rate
    """
    # concatenating X's with X0's which are equal to 1
    X_ = np.c_[np.ones((len(X),1)),X]
    # Initializing theta randomly
    theta = np.random.randn(len(X[0]) + 1,1)
    # Number of samples
    m = len(X_)
    
    yield theta

    #Iterating over the samples
    for i in range(m):
        
        # Calculating theta:
        # theta := theta + alpha * (y_i - ((theta_i * x_i)) * x_i)
        x = X_[i].reshape((1,len(X[0]) + 1))
        theta += alpha * ((y[i] - x.dot(theta)).dot(x)).T
        
        yield theta


def plot_for_offset(t, y_max):

    fig, ax = plt.subplots(figsize=(5,5))

    plt.plot(X, t[0] + X * t[1])
    ax.scatter(X,y)
    ax.grid()

    # Used to return the plot as an image rray
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'batch':
        imageio.mimsave('./batch_GD.gif',[plot_for_offset(i, 20) for i in batch_gradient_descent(X,y)], fps=2)
    elif len(sys.argv) > 1 and sys.argv[1] == 'stochastic':
        imageio.mimsave('./stochastic_GD.gif',[plot_for_offset(i, 20) for i in stochastic_gradient_descent(X,y)], fps=6)
    else:
        print('Batch or Stochastic Gradient Descent')