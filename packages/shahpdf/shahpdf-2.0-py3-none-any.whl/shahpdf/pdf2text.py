# -------------- Taking from Chapter 10 "Python Package Index" and Section 8 --------------
# As a best level practice, we should create a folder with same name as our project i.e., 'shahpdf' which will hold all our source code
# We can also have two other folders "tests" which will have unit tests file, and "data" which will have some sample data
# We should add __init__.py file inside shahpdf so that python see this as a package

# Lets create a basic function
def convert():
    print("pdf2text")

# Make sure you change your python interpreter back to the globar interpreter either by clicking in the bottom lower corner or shift + command + P to open "show ALL commands" --> type interpreter --> select "Python:selected interpreter" --> choose /usr/local/bin/python3

# We can also add another module "pdf2image.py" (without any code let's say), just to mimic basic picture of a how package looks like

# To publish this package to pypi, we need to import three files
#     setup.py (at the root level) --> rest of the code in this file
#     README.md file (at the root level; all in CAPS, and md short for 'marked down') which will display on homepage of our package on pypi --> rest of the code in this file
#     LICENSE file (at the root level with no extension) --> Find the generic basic template on https://choosealicense.com and paste in the file

# After generating three files (setup.py, README, and LICENSE), we need to generate distribution package
# Syntax: python3 setup.py sdist bdist_wheel (with this command we will build source ditribution and built distribution package)

# It created two directories in our project : 'build' and 'dist'. In dist directory we have .whl file (build distribution) and .gz file (source distribution). Both are zip files, we can unzip them to see what's inside

# With these two distribution packages in the dist folder, the final step to upload your package to pypi is to upload them using 'twine'
# Syntax: twine upload dist/*