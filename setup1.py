from cx_Freeze import setup, Executable

setup(name = sum,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("sum.py")])
