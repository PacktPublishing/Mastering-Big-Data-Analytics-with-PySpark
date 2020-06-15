# Example of pyspark compatible package structure

This is just a tiny demo to show how a pyspark compatible package can look like.

__Creating an `.egg file`__  
Requires: `setuptools` (`pip install setuptools`)
```shell script
python setup.py bdist_egg
```

__Creating a `.whl` file__  
Requires: `wheel` (`pip install wheel`)
```shell script
python setup.py bdist_wheel
```

Resulting package should look something like this:
```yaml
- package_test-0.0.1-py3.7.egg
  - EGG-INFO
    - dependency_links.txt
    - PKG-INFO
    - SOURCES.txt
    - top_level.txt
    - zip-safe
  - src
    - __init__.py
    - jobs
      - __init__.py
      - hello_world_job.py
    - main.py
```

This package can be submitted to spark using
```shell script
spark-submit --py-files package_test-0.0.1-py3.7.egg main.py
```
> __note__: that for the above example to work, `main.py` and `package...egg` files need 
to be in the same directory. Else use absolute/relative paths to point to the files.
