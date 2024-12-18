# Adjidev proxy scraper

> ===================================
# Guide
Let's get started if you don't know about my project
## 1. Installation
### requirements
> 1. python 3.8 or later
> 2. python installed on you device
> 3. Code editor or notepad etc

### for windows
- install python if python is not installed [click here](https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe)
- install my pypi packages
  ```powershell
  python -m pip install adjisan-proxy-scraper
  ```

### for debian based linux
- install python if not installed
  ```bash
  sudo apt install python
  ```
- install my pypi package
  ```bash
  pip install adjisan-proxy-scraper
  ```

### for arch based linux
- install python if not installed
  ```bash
  sudo pacman -S python
  ```
- install my pypi packages
  ```bash
  pip install adjisan-proxy-scraper
  ```

### for red hat based linux
- install python if not installed
  ```bash
  sudo dnf install python3
  ```
- install my pypi packages
  ```bash
  pip install adjisan-proxy-scraper
  ```

## EXAMPLE
  ```python
  from ProxyScraper import GetProxy

  if __name__ == "__main__":
    #Init
    proxy = GetProxy(type="http", timeout=5, max_workers=20)

    #get
    proxies = proxy.get()
    print(f"Fetched {len(proxies)} proxies.")

    #save
    proxy.save("http.txt")
  ```

> ===================================