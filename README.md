# Shell.py

This a shell implementation of a **shell** in python following this : [grammar](mygrammar)

I handle **Pipe**, simple **Redirection**, **Command**, **AND**, **OR** and **Semicolon**. It's schedule to make grow the grammar handled.

It's a **POSIX** shell *(I believe)* because it follow GNU **sh** behaviour. 

## AstDot

I made a long jump in this project when i was able to visualize how my AST was after parsing step.

Look at the end of this README for example or the [generateAstDot file](generateAstDot.py)

## lsbasi

> I realised this project will reading  [Let's build a simple interpreter](https://ruslanspivak.com/archives.html)

### Fork

For the **forks** logic and behaviour I one more time really appreciated the **lsbasi** tutorial on processes. It make me close the gap of my understanding on it works.

[Let's build a web server](https://ruslanspivak.com/lsbasi-part1)

## Graph

Look this output for the following command:

```
ls -2 || echo "YES"; ls -l > test1 > test2 > test3 && cat test3 || echo "NO"; cat test3 | grep 1 > test1 | cat test3
```

![graph](/github/graph.png)

> When you have this, and validated it, you can tackle the interpretation  :moneybag:

# TODO

On my **TODO** list i can put **backtick** expansion, handle (simple|double) quote and error handling for commands.
