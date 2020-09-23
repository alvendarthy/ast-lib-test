import ast


add_arg = "test()"

with open("target.py") as f:
    tree = ast.parse(f.read())


import astpretty

astpretty.pprint(tree)


class Visitor(ast.NodeVisitor):
    def visit_Import(self, node):
        for alias in node.names:
            print("package {} imported.".format(alias.name))

    def visit_Call(self, node):
        print("calling func: ", node.func.id)

        if node.func.id != "print":
            return

        print("origin args:")
        args = node.args
        for arg in args:
            if isinstance(arg, ast.Constant):
                print("type:", type(arg), arg.value)

            else:
                print("None static arg.")

        print("set arg to 'hello world'")

        args[0] = ast.Constant(s = "hello world", kind=None)
        ast.fix_missing_locations(args[0])
        print("add another arg")

        last_index = len(args)
        print("last index: ", last_index)        

        args.insert(last_index, ast.Constant(s = "!!!!!", kind=None))
        ast.fix_missing_locations(args[last_index])

        print("add test call one more time.")
        node = ast.parse(add_arg).body[0].value
        args.insert(last_index + 1, node)
        ast.fix_missing_locations(args[last_index + 1])


v = Visitor()

v.visit(tree)


co = compile(tree, "log.log", "exec")

exec(co)


import astunparse

print(astunparse.unparse(tree))
