# Homomorphic-Encryption
So this repo has 3 Python files as of now.
the first file is Paillier_Homomorphic_Encryption.py which we made to see the working and implement the Paillier HomoMorphic Encryption system and see how the homomorphic encryption would work with another algorithm. So this file code is fully functional and gives accurate output.

the next file to note is trial.py in which we have implemented BGV method on a very small scale just to simulate its working and observe output. The model has been given very specific values which we knew prior that it would work accurately and produce the desired output
The last file is bgv-main.py which is our main attempt at implementation of BGV method of homomorphic encryption. But in the output part of this code, we notice that the values of addition and multiplication are not accurate.This is because of noise becoming incorporated in our data which exponentially increases during multiplication so then the values in the output are not accurate or correct. On continued tuning of parameter values and implementing the actual math of  polynomial arithmetic and modulus switching, the accuracy of results may be improved and this is our work in progress.

## Steps to run the code: ##
1] Using code editor like VsCode:
pull our repository into your local system or download the .py file you wish to run. After that run it following the normal procedure.

2] Using Google Colab
Import the necessary libraries and then paste our code into a code cell and run.

For any other assistance or feedback please contact us :)
