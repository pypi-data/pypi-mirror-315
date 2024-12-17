#!/usr/bin/env python
import typer

app = typer.Typer()

@app.command()
def main(name: str):
    # 函数实现
    print(f"你好123, {name}!")
    pass

if __name__ == "__main__":
    app()