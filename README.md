# **Anemone_1**
**Project objective** - OCR bank statements and attempt to understand and classify content.

##`Anemone_1_Parser.py` 
Extract basic information from the statement.

Current implementation includes; *Bank Name*, *Sort Code*, *Account Number* and *List of transactions* including whether the transaction is **_"Paid In"_** or **_"Paid Out"_**. Currently no data is being saved but the data is in the correct format where a debit transaction would have the Paid Out field set to `0.00` (last field entry) while a Paid In field is the other way around (zero field in the penultimate position).

The code takes no arguments but expects text files to be in a specific directory as detailed by `srcDocPath` (line 26). These text files are the OCRed documents using Anemone_1_OCR.py. It also expects to write the resulting text file into the path detailed by `dstDocPath` (line 27). Please change these values to the appropriate paths on your machine. (If running on Windows use "\\\\" instead of "/" to separate the folders in the path name.)

**Dependencies:** The code has no special dependancies. Standard dependancies are; `sys`,`os`, `glob`, `re`, `time`, `mmap`and `contextlib`. The code also calls `findData.py` which contians the various extraction method routines.

Current output is to screen only.

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

