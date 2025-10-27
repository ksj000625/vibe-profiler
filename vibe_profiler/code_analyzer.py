import ast
import inspect

class CodeAnalyzer:
    """
    Analyze function code to detect common slow patterns.
    """

    def analyze(self, func):
        warnings = []
        source = inspect.getsource(func)
        tree = ast.parse(source)

        for node in ast.walk(tree):
            # Detect File I/O inside loops
            if isinstance(node, ast.For):
                for inner in ast.walk(node):
                    if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                        if inner.func.id in ("open",):
                            warnings.append("↳⚠️ File I/O inside loop — may cause slow performance")

            # Detect requests.get inside loops
            if isinstance(node, ast.For):
                for inner in ast.walk(node):
                    if isinstance(inner, ast.Attribute) and inner.attr == "get":
                        warnings.append("↳⚠️ Network request inside loop — consider batching")

            # Detect deepcopy
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in ("copy", "deepcopy"):
                    warnings.append("↳⚠️ Unnecessary deepcopy — optimize data usage")

        return list(set(warnings))  # deduplicate
