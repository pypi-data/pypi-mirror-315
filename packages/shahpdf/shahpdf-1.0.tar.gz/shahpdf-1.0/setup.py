# Let's import setuptools module in this file

import setuptools  # installed earlier

# setuptools module have this method called setup, and we pass important key word arguments
setuptools.setup(
    # Set the unique name of your package which does not conflict with other package
    name="shahpdf",

    version=1.0,  # Set the version number

    long_description="",  # Put long description of your package

    # Setup up how many "packages" & "modules" will be distributed, note in this project we have only one package "shahpdf" (which has two modules), but we could have multiple package in a project.
    # find_packages method will find all the packages in the project folder, we could pass argument to skip 2 directories "test" and "data" since they usually don't include source code
    packages=setuptools.find_packages(["tests", "data"])
)

# Now let's create a readme file, which will display on homepage of our package on pypi
