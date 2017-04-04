# **Anemone_1**
**Project objective** - OCR bank statements and attempt to understand and classify content.

##`Anemone_1_Trainer.py` 
Train 3 Artificial Neural Network (ANN) agents with the data from Anemone_1_Parser.py. The data is split into training and test data using the ratio specified by `testDataPercentage`. The test data is then fed to the agents where their output is fed to Weighted Majority Rule Ensemble Classifier. The output of the final classifier is a normalized probability for every class.

The code takes no arguments but expects a text file to be in a specific directory as detailed by `srcDocPath` (line 18). The text file contains the extracted data from the statements. It also expects to write the resulting text file into the path detailed by `dstDocPath` (line 19). Please change these values to the appropriate paths on your machine. (If running on Windows use "\\\\" instead of "/" to separate the folders in the path name.)

**Dependencies:** The code requires the Natural Language Tool Kit (NLTK) and PyBrain as dependancies. Standard dependancies are; `sys`,`os`, `glob`, `re`, `time`, `mmap`and `contextlib`. The code requires the `random` library to split the data into taining and test randomly and also requires `tabulate` library to display the results correctly.

Output is currently to screen only but the trained agents can be saved after execution and display of results.

##`Anemone_1_Parser.py` 
Extract basic information from the statement.

Current implementation includes; *Bank Name*, *Sort Code*, *Account Number* and *List of transactions* including whether the transaction is **_"Paid In"_** or **_"Paid Out"_**. Data is being saved to a text file. The file name is made up of the sort code and account number separated by an underscore. The output files can be located in the `\Converted\Statements\` folder. The file structure is made up of a harmonized date, harmonized transaction type, transaction description (limited to 50 characters), **_"Paid In"_** boolean (0 or 1) and the value of the transaction. The fields are separated by a questionmark "?".

The code takes no arguments but expects text files to be in a specific directory as detailed by `srcDocPath` (line 26). These text files are the OCRed documents using Anemone_1_OCR.py. It also expects to write the resulting text file into the path detailed by `dstDocPath` (line 27). Please change these values to the appropriate paths on your machine. (If running on Windows use "\\\\" instead of "/" to separate the folders in the path name.)

**Dependencies:** The code has no special dependancies. Standard dependancies are; `sys`,`os`, `glob`, `re`, `time`, `mmap`and `contextlib`. The code also calls `HSBC.py` or `NATWEST.py` depending on the identified bank statement. The code in these files are very similar but they are tweaked to work with their respective issuing bank and contian various extraction method routines. Also the PDF files need to be only one page long when OCRed in order to generate Markovian text files and spacing (See Processed/Statements/ folder)

##`Anemone_1_OCR.py` 
OCRs bank statements into text files using ABBYY Cloud OCR SDK. The OCR account details can be changed from AbbyyOnlineSdk.py lines 38 and 39. **To register for a free account** go to http://ocrsdk.com/ then enter the ApplicationId and Password in their respective lines.

Anemone_1_OCR.py takes no arguments but expects pdf files to be in a specific directory as detailed by `srcDocPath` (line 23). It also expects to write the resulting text file into the path detailed by `dstDocPath` (line 24). Please change these values to the appropriate paths on your machine. (If running on Windows use "\\\\" instead of "/" to separate the folders in the path name.)

**Dependencies:** ABBYY Cloud OCR SDK contianing `AbbyyOnlineSdk.py`, `MultipartPostHandler.py`and `process.py`. `subprocess`, `sys`, `os`, `glob` and `re` for file handling and general calls.

Please also preserve the current file structure as it has been created with future development in mind.

**_Therefore, the steps required to use Anemone_1_OCR.py are:_**
  1. Edit the file `Anemone_1_OCR.py` using notepad or Python IDLE.
  2. Change `srcDocPath = '\\Projects\\Anemone_1\\PDFs\\Statements\\'` to the path where your pdf statements are located.
  3. Change `dstDocPath = '\\Projects\\Anemone_1\\Processed\\Statements\\'` to the path where you want the OCRed text file to be stored. 
  4. Save the file and exit.
  5. Open a console window (Start button then type `cmd`)
  6. Type `cd <Directory>` where `<Directory>` is the location of Anemone_1_OCR.py
  7. Type `python Anemone_1_OCR.py` and press Enter. The console should display the current process.
  8. Wait for "Done." and close the console window.

You should now find the text files in the specified directory.

END.
