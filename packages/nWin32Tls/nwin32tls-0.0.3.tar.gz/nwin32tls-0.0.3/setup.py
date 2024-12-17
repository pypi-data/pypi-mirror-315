from setuptools import setup, find_packages

setup(
    name="nWin32Tls",  # Уникальное имя вашей библиотеки на PyPI
    version="0.0.3",  # Версия вашей библиотеки
    author="S4CBS",
    author_email="aap200789@gmail.com",
    packages=find_packages(),  # Автоматически ищет все пакеты
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyautogui>=0.9.54",
        "mss>=10.0.0",
        "pyTelegramBotAPI>=4.25.0",
        "Pillow>=11.0.0",
        "pynput>=1.7.7",
        "requests>=2.32.3",
        "PyScreeze>=1.0.1"
    ]
)
