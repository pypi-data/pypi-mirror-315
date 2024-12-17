from setuptools import setup, find_packages

setup(
    name="stubh",  # Имя вашего пакета
    version="1.0.0",  # Версия пакета
    packages=find_packages(),  # Поиск всех пакетов в директории
    install_requires=[  # Зависимости
        # Здесь можно указать другие библиотеки, которые ваш пакет использует
        # Например: "requests", "numpy"
    ],
    long_description=open("README.md").read(),  # Описание из README
    long_description_content_type="text/markdown",  # Формат описания
    author="PodonokA",  # Ваше имя
    author_email="podonki@tuta.io",  # Ваш email
    url="https://github.com/reyzovw",  # URL вашего проекта
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
