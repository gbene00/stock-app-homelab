import importlib


def test_main_imports():
    # Just checks that the module imports without errors
    importlib.import_module("stock_app")
