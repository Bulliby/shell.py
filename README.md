# Shell.py

A basic shell, the grammar used is the following : [grammar](mygrammar)

I handle **Pipe**, **Redirection** and **Command**. It's schedule to make grow the grammar handled.

> I realised this project will reading  [Let's build a simple interpreter](https://ruslanspivak.com/archives.html)

## AstDot

```shell
python generateAstDot.py test > ast.dot && dot -Tpng -o ast.png ast.dot
```
