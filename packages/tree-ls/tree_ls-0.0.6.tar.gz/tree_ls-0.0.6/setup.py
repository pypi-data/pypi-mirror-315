from setuptools import setup, find_packages

setup(
    name="tree-ls",  # Paket adı
    version="0.0.6",  # Sürüm numarası
    author="GAbaci",  # Yazar adı
    description="A tool to print directory tree structure",  # Paket açıklaması
    long_description=open("README.md").read(),  # README.md dosyasının içeriği
    long_description_content_type="text/markdown",  # Markdown formatında açıklama
    packages=find_packages(),  # Paketleri otomatik bulur
    install_requires=[
        # Bağımlılıkları buraya ekleyin (örn. 'requests>=2.0')
    ],
    entry_points={
        'console_scripts': [
            # Komut satırı arayüzü (CLI) oluşturmak için
            'tree-ls=tree_ls.tree_ls:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)