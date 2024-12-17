from setuptools import setup, find_packages

setup(
    name='pymindbot',  # The new name of your package
    version='0.1',  # Version 0.1
    packages=find_packages(),  # Automatically finds all the packages (like pymindbot/)
    install_requires=[  # List your dependencies here
        'google-generativeai',  # For AI and Google services
        'httpx',  # For HTTP requests
        'pytesseract',  # For OCR
        'Pillow',  # For image processing (PIL)
    ],
    author='Ahmed Helmy Ali Eletr',  # Replace with your name
    author_email='ahmedhelmyali.dev@gmail.com',  # Replace with your email address
    description='PyMindBot: MindBot Ai Library Large Language Model.',
    long_description=open('README.md').read(),  # A detailed description
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pymindbot',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the required Python version
)
