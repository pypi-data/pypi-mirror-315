from setuptools import setup, find_packages
import pathlib 

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup( name ="pyrepohistory", 
       version = "0.0.8",
       author = "Matt Gaughan",
       long_description = long_description, 
       long_description_content_type="text/markdown", 
       py_modules=["pyrepohistory"]
)

