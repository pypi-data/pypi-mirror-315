"""Databricks Gen AI Package, aliased as databricks"""
# https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages
# This file should only contain the following line. Otherwise other sub-packages databricks.* namespace
# may not be importable.
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

try:
    import pyspark
    del pyspark
except ImportError as e:
    raise ImportError("PySpark is not installed. Please install databricks-connect to use this package.") from e

try:
    from databricks.connect import DatabricksSession
    del DatabricksSession
except ImportError as e:
    raise ImportError(
        "Databricks Connect is not installed. Please install databricks-connect to use this package.") from e
