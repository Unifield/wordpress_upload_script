A simple upload script for Wordpress based on Selenium


## How to use
1. Copy the .doc/.docx files into the `files_to_upload` folder
2. Fill the credentials.py file with the username, password in base64 and a list of tags for the upload. (The tags need to be exactly the way they are on the website including lowercase and upppercase letters.)
3. Make sure the files are alphabetically in order how they should be uploaded
4. Run the `main.py` file from the root folder of the project
    - `python3 main.py`


## Requirements
- Python 3
- Selenium - https://pypi.org/project/selenium/
