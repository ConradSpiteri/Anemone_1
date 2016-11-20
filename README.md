# **Anemone_1**
**Project objective** - OCR bank statements and attempt to understand and classify content.

##`Anemone_1_Parser.py` 
Extract basic information from the statement. Current implementation includes; *Bank Name*, *Sort Code*, *Account Number* and *List of transactions*. Currently no data is being saved as the transaction list requires some cleaning up before being passed on to the data sorter in order to be saved.

The code takes no arguments but expects text files to be in a specific directory as detailed by `srcDocPath` (line 26). These text files are the OCRed documents using Anemone_1_OCR.py. It also expects to write the resulting text file into the path detailed by `dstDocPath` (line 27). Please change these values to the appropriate paths on your machine. (If running on Windows use "\\\\" instead of "/" to separate the folders in the path name.)

**Dependencies:** The code has no special dependancies. Standard dependancies are; `sys`,`os`, `glob`, `re`, `time`, `mmap`and `contextlib`. The code also calls `findData.py` which contians the various extraction method routines.

Current output is to screen only.

##`Anemone_1_OCR.py` 
OCRs bank statements into text files using ABBYY Cloud OCR SDK. The OCR account details can be changed from AbbyyOnlineSdk.py lines 38 and 39. **To register for a free account** go to http://ocrsdk.com/ then enter the ApplicationId and Password in their respective lines.

Anemone_1_OCR.py takes no arguments but expects pdf files to be in a specific directory as detailed by `srcDocPath` (line 23). It also expects to write the resulting text file into the path detailed by `dstDocPath` (line 24). Please change these values to the appropriate paths on your machine. (If running on Windows use "\\\\" instead of "/" to separate the folders in the path name.)

**Dependencies:** ABBYY Cloud OCR SDK contianing `AbbyyOnlineSdk.py`, `MultipartPostHandler.py`and `process.py`. `subprocess`, `sys`, `os`, `glob` and `re` for file handling and general calls.

If you get an error saying `urllib2.HTTPError: HTTP Error 401: Unauthorized` then the account details entered in AbbyyOnlineSdk.py lines 38 and 39 are incorrect. See steps 1 to 7 below.

Please also preserve the current file structure as it has been created with future development in mind.

**_Therefore, the steps required to use Anemone_1_OCR.py are:_**
  1. Go to http://ocrsdk.com/ and register for a free account.
  2. Create or add a new application and give it a name.
  3. You will be sent the password for the new application via e-mail.
  4. Edit the file `AbbyyOnlineSdk.py` using notepad or Python IDLE.
  5. Change `ApplicationId = "user"` where `user` is the application name you created in step 2.
  6. Change `Password = "password"` where `password` is the password you received via e-mail in step 3.
  7. Save the file and exit.
  8. Edit the file `Anemone_1_OCR.py` using notepad or Python IDLE.
  9. Change `srcDocPath = '/home/pdf417/Dropbox/Projects/Anemone_1/PDFs/Statements/'` to the path where your pdf statements are located.
  10. Change `dstDocPath = '/home/pdf417/Dropbox/Projects/Anemone_1/Processed/Statements/'` to the path where you want the OCRed text file to be stored. 
  11. Save the file and exit.
  12. Open a console window (Start button then type `cmd`)
  13. Type `cd <Directory>` where `<Directory>` is the location of Anemone_1_OCR.py
  14. Type `python Anemone_1_OCR.py` and press Enter. The console should display the current process.
  15. Wait for "Done." and close the console window.

You should now find the text files in the specified directory.

END.

