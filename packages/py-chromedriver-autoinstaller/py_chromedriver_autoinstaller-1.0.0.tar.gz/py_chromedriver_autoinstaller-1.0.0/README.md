# py-chromedriver-installer  

This repository is a fork of [python-chromedriver-autoinstaller](https://github.com/yeongbin-jo/python-chromedriver-autoinstaller), renamed to **py-chromedriver-installer**. It improves upon the original by fixing issues with detecting Chrome versions on Windows and introducing a new function to retrieve the download URL for Chromedriver.

## Key Updates  
- **Fixed:** Detection of Chrome versions on Windows.  
- **New Feature:** Added the `get_driver_url` function.  

### `get_driver_url` Function  
This function retrieves the download URL for Chromedriver without performing the actual download. It serves as an alternative to the existing `download_chromedriver` function.  

```python
def get_download_url(path: Optional[AnyStr] = None, no_ssl: bool = False):
```

---

## Installation  

```bash
pip install py-chromedriver-installer
```  

## Usage  
Import `py-chromedriver-installer` to automatically handle Chromedriver installation or fetch the driver URL.

### Example: Auto-Installation  
```python
from selenium import webdriver
import py_chromedriver_installer  

py_chromedriver_installer.install()  # Automatically downloads the correct version of Chromedriver,
                                     # then adds it to PATH.

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```  

### Example: Get Chromedriver Download URL  
```python
from py_chromedriver_installer import get_driver_url  

url = get_driver_url()  # Retrieves the Chromedriver download URL for the current Chrome version.
print("Chromedriver download URL:", url)
```  

---

## Authors & Contributors  

- **Farhan Ali** <[i.farhanali.dev@gmail.com](mailto:i.farhanali.dev@gmail.com)>  
  *Added new features and updates to improve functionality.*  
- **CHIDA** <[iam.yeongbin.jo@gmail.com](mailto:iam.yeongbin.jo@gmail.com)>  
- **shawnCaza** <[theshawn@gmail.com](mailto:theshawn@gmail.com)>  
