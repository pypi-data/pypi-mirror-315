# This is a PyInstaller hook for pywebio3.
# https://pyinstaller.readthedocs.io/en/stable/hooks.html

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('pywebio3')
