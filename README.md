# Shell.py

A basic shell, the grammar used is the following : [grammar](mygrammar)

I handle **Pipe**, simple **Redirection**, **Command** and **Semicolon**. It's schedule to make grow the grammar handled.

It's a **POSIX** shell *(I believe)* because it follow GNU **sh** behaviour. 

On my **TODO** list i can put the **AND** and **OR** operator and error handling for commands. 

## AstDot

I made a long jump in this project when i was able to visualize how my AST was after parsing step.

Look at the end of this README for example

## lsbasi

> I realised this project will reading  [Let's build a simple interpreter](https://ruslanspivak.com/archives.html)

### Fork

For the **forks** logic and behaviour I one more time really appreciated the **lsbasi** tutorial on processes. It make me close the gap of my understanding on it works.

[Let's build a web server](https://ruslanspivak.com/lsbasi-part1)

## Graph

Look this output for the following command it's awesome :

```
ls -l | grep --color=never ast | wc -l > toto | ls | grep I > tata > tutu | ls | wc -c > titi ; cat tata; cat toto; cat tutu
```

![graph](/github/graph.png)

> When you have this, and validated it, you can tackle the interpretation  :moneybag:
