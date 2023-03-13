# PianoScript


## Index
> - [Pianoscript 1](#pianoscript-1)
> - [Pianoscript 2](#pianoscript-2)
> - [Todo's](#todos)
> - [Design](#design)
> - [Executables](#executables)
> - [GUI](#gui)
> - [Packages](#packages)
> - [Package management](#package-management)
> - [PDF](#pdf)
> - [Testing](#testing)


## Pianoscript 1

```shell
$ py -m pianoscript
```

### Structure

| Section               | Lines       |
| --------------------- | ----------- |
| Introduction          |    1 -   17 |
| Imports               |   34 -   42 |
| GUI                   |   53 -  172 |
| File management       |  188 -  389 |
| Tools                 |  410 - 1003 |
| Render variables      | 1021 - 1047 |
| Constants             | 1061 - 1095 |
| Main render function  | 1111 - 2227 |
| Editor help functions | 2244 - 2354 |
| Export functions      | 2372 - 2543 |
| Editor tools          | 2561 - 2723 |
| Menu                  | 2741 - 2760 |
| Render management     | 2775 - 2827 |
| Shortcuts             | 2830 - 2847 |


### Issues
See [Pianoscript 2](#pianoscript-2)


## Pianoscript 2

```shell
$ py -m pianoscript-2
```

### Structure

| Section               | Lines       |
| --------------------- | ----------- |
| Imports               |    2 -   11 |
| GUI                   |   13 -  105 |
| Constants             |  107 -  138 |
| Tools                 |  141 -  894 |
| Save file structure   |  912 -  967 |
| File management       |  987 - 1097 |
| Piano roll            | 1114        |
|                       |      - 2093 |
| Text boxes            | 2110        |
|                       |      - 2367 |
| Export                | 2385 - 2506 |
| Engraving             | 2524 - 3271 |
| Menu                  | 3290 - 3340 |
| Bind                  | 3356 - 3405 |
| Main                  | 3417 - 3418 |
| Main loop (Tk)        | 3420 - 3423 |
| TODO                  | 3425 - 3430 |

### Issues
- "Spaghetti" code
- Import errors
    - imported, but not used
- Type errors (e.g. lines 1376, 3359)
    - especially involving None (e.g. lines 2303, 2405, 2640, 3301)
- Variables declared but not used (e.g. lines 828,829, 1301)
- Binding errors (e.g. line 2648)
- Linting errors
- Security issue (eval function, e.g. line 2121)
- Linguistic errors in text (e.g. "get's" in line 193)


## TODO's
- Set up project in GitHub
- Set up work environment (analysis tools, linting, build pipeline)
- Cleanup existing code (maintain a working program)
- Take some time to think about the design of the app
- Investigate and decide on language, platforms, libraries, etc.
- Test the application and its constituant parts
- Build a modular application
- Write documentation

 
## Design
- Project setup (see: [Project structure](#project-structure))
- Modular
- Loosely coupled if possible (e.g. core app, GUI, import module, export module)
- Test driven
- Develop in virtual environment with managed dependencies and packages
- Build for the future
- Architecture (Linux, Darwin, Windows, web based, platform independent, ?)
- Web app or desktop app?
- User interface (tkinter: Tcl + tk/ttk, Qt5/6, Kivy, HTML, ?)
- Design mode (Tk/Qt/svg?)
- Input format(s) (midi)
- Output format(s) (pdf)
- Data persistance (json?)
- Open source? (license!)
- Well documented
- Intuitive, inviting, creative?
- Create an app that delivers great results and is easy and fun to work with
- Create an app that invites people to play the piano and make music


## Executables
- [Create a directly-executable cross-platform GUI app using Python](https://stackoverflow.com/questions/2933/create-a-directly-executable-cross-platform-gui-app-using-python?noredirect=1&lq=1), Stack Overflow.

### PyInstaller
- [PyInstaller on PyPi](https://pypi.org/project/pyinstaller/)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/index.html)


## GUI
- [GUI Programming in Python](https://wiki.python.org/moin/GuiProgramming), wiki.python.org

### Kivy
- [Kivy](https://kivy.org/)
- [Kivy on PyPi](https://pypi.org/project/Kivy/)

### Qt
- [Qt Framework](https://www.qt.io/product/framework)

### tkinter
- [tkinter](https://docs.python.org/3/library/tkinter.html)


## Packages
- [Python Package Index (PyPi)](https://pypi.org/)


## Package management

### Project structure
- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/), [Python Packaging Authority](https://www.pypa.io/en/latest/)

### Poetry
- [Poetry on PyPi](https://pypi.org/project/poetry/)
- [Python Poetry](https://python-poetry.org/docs/), official documentation.
- [Python Poetry](https://python.land/virtual-environments/python-poetry), Python Land, 2022-08-13.


## PDF
- [ReportLab Docs](https://docs.reportlab.com/)
- David Amos, [Create and Modify PDF Files in Python](https://realpython.com/creating-modifying-pdf/), Real Python.
- [Creating PDF Documents With Python](https://www.geeksforgeeks.org/creating-pdf-documents-with-python/), Geeks for Geeks, 2022-05-17.


## Testing

### Pytest
- [pytest](https://docs.pytest.org/en/7.2.x/)
- [pytest on PyPi](https://pypi.org/project/pytest/)
