$directoryPath = ".\python-win"
if (Test-Path -Path $directoryPath -PathType Container) {
    Write-Host "Python 3.9 Embedded already configured. Moving on."
} else {
    Write-Host "Downloading and Configuring Python Embedded..."
    wget https://www.python.org/ftp/python/3.9.10/python-3.9.10-embed-win32.zip -o python-win.zip
    Expand-Archive python-win.zip
    Write-Host "Downloading pip..."
    wget https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    mv .\python-win\python39._pth .\python-win\python39.pth
    mkdir .\python-win\DLLs
    Write-Host "Installing pip..."
    .\python-win\python.exe get-pip.py
    Write-Host "Cleaning up..."
    Remove-Item -Path ".\get-pip.py"
    Remove-Item -Path ".\python-win.zip"
}