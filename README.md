# Homomorphic-Encryption
The repo follows this structure:
the trials folder contains various attempts at homomorphic encryption which failed or are incomplete and give erronneous output.
these attempts include files like trial.py and trial2.py 
Currently, the correctly and best-working code files are demo_bgv.py and bgv.py
To run the code and see the output, use:
```bash
python demo_bgv.py
```
All the codes are inside bgv.py which the demo_bgv file imports and uses to keep the code clean.
As of now, demo_bgv performs addition correctly but multiplication is producing output with noise and errors.

## Steps to run the code: ##
1] Using code editor like VsCode:
* navigate into the desired location where you want to clone the repository. Next, in the terminal use code:
```bash
git clone https://github.com/sammymallya/Homomorphic-Encryption.git
```
* this will create a local copy of the chosen repo files inside your folder. next to run the python file:
* Next , download all required libraries using:
```bash
pip install requirements.txt
```
Now you are ready to run the code files
```bash
  python demo_bgv.py
```


2] Using Google Colab
Import the necessary libraries and then paste our code into a code cell and run.

For any other assistance or feedback please contact us :)
