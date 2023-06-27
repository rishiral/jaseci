"""Abstract class for IR Passes for Jac."""
from typing import TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.transform import Transform
from jaclang.jac.utils import pascal_to_snake

T = TypeVar("T", bound=ast.AstNode)


class Pass(Transform):
    """Abstract class for IR passes."""

    def __init__(
        self, mod_path: str, input_ir: ast.AstNode, base_path: str = ""
    ) -> None:
        """Initialize parser."""
        self.term_signal = False
        self.prune_signal = False
        self.cur_node = input_ir  # tracks current node during traversal
        Transform.__init__(self, mod_path, input_ir, base_path)

    def before_pass(self) -> None:
        """Run once before pass."""
        pass

    def after_pass(self) -> None:
        """Run once after pass."""
        pass

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering node."""
        if hasattr(self, f"enter_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"enter_{pascal_to_snake(type(node).__name__)}")(node)
        if isinstance(node, ast.Parse) and hasattr(self, f"enter_{node.name}"):
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        if hasattr(self, f"exit_{pascal_to_snake(type(node).__name__)}"):
            getattr(self, f"exit_{pascal_to_snake(type(node).__name__)}")(node)
        if isinstance(node, ast.Parse) and hasattr(self, f"exit_{node.name}"):
            getattr(self, f"exit_{node.name}")(node)

    def term_traverse(self) -> None:
        """Terminate traversal."""
        self.term_signal = True

    def prune_traverse(self) -> None:
        """Prune traversal."""
        self.prune_signal = True

    def get_all_sub_nodes(
        self, node: ast.AstNode, typ: type[T], brute_force: bool = False
    ) -> list[T]:
        """Get all sub nodes of type."""
        result = []
        # Assumes pass built the sub node table
        if not node:
            return result
        elif len(node._sub_node_tab):
            result.extend(node._sub_node_tab[typ] if typ in node._sub_node_tab else [])
        elif len(node.kid):
            if not brute_force:
                raise ValueError(f"Node has no sub_node_tab. {node}")
            # Brute force search if pass didn't build table
            else:
                for i in node.kid:
                    if isinstance(i, typ):
                        result.append(i)
                    result.extend(self.get_all_sub_nodes(i, typ))
        return result

    # Transform Implementations
    # -------------------------
    def transform(self, ir: ast.AstNode) -> ast.AstNode:
        """Run pass."""
        self.before_pass()
        if not isinstance(ir, ast.AstNode):
            raise ValueError("Current node is not an AstNode.")
        self.traverse(ir)
        self.after_pass()
        # Checks if self.ir is created during traversal
        return self.ir if hasattr(self, "ir") else ir

    def traverse(self, node: ast.AstNode) -> None:
        """Traverse tree."""
        if self.term_signal:
            return
        self.cur_node = node
        self.enter_node(node)
        if not self.prune_signal:
            for i in node.kid:
                if i:
                    self.traverse(i)
        else:
            self.prune_signal = False
        self.exit_node(node)

    def error(self, msg: str) -> None:
        """Pass Error."""
        if not isinstance(self.cur_node, ast.AstNode):
            self.ice("Current node is not an AstNode.")
        self.cur_line = self.cur_node.line
        self.log_error(f"{msg}")

    def warning(self, msg: str) -> None:
        """Pass Error."""
        if not isinstance(self.cur_node, ast.AstNode):
            self.ice("Current node is not an AstNode.")
        self.cur_line = self.cur_node.line
        self.log_warning(f"{msg}")

    def ice(self, msg: str) -> None:
        """Pass Error."""
        if isinstance(self.cur_node, ast.AstNode):
            self.cur_line = self.cur_node.line
        self.log_error(f"ICE: Pass {self.__class__.__name__} - {msg}")
        raise RuntimeError(
            f"Internal Compiler Error: Pass {self.__class__.__name__} - {msg}"
        )


class PrinterPass(Pass):
    """Printer Pass for Jac AST."""

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering node."""
        print("Entering:", node)
        super().enter_node(node)

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        super().exit_node(node)
        print("Exiting:", node)
