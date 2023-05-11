import numpy as np  # mainly used for arrays, vectors and matrices 
import matplotlib.pyplot as plt # plotting everything you can think of 
import pandas as pd  # deals with tables 



#arrays 
a = np.array([1,2,3,4,5])
#print("a: \n", a)
a = a**2
#print("a: \n", a)

#print(sum(a), "\n" )
#print(np.arange(0,3))

b = np.array([[0,1], [2,3]])
#print("b: \n", b)

c = np.zeros([3,4])
#print("c: \n", c)

d = np.full([3,2], 1)
#print("d: \n", d)

e = np.linspace(0,5,20)
e = np.around(e, decimals = 2)
#print("e: \n", e)

# Plots 
idx = np.array([1,2,3,4,5])
data = np.array([5,10,12,16,18])
plt.plot(idx, data, label='method1'); 
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Line plot')
plt.plot(idx, [5,7,11,15,19], label='method2')
plt.legend(loc='lower right')
plt.savefig('figure.png')


#pandas 
dict = {'name': 'josh', 'date':23, 'school':'byu'}
series_from_dict = pd.Series(dict)
print(series_from_dict)


x = np.linspace(0, 2, 100)

# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
fig, ax = plt.subplots()  # Create a figure and an axes.
ax.plot(x, x, label='linear')  # Plot some data on the axes.
ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
ax.plot(x, x**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.
plt.savefig('figure2.png')



