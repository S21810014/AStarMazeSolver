# A* Maze Solver

## Usage
It is recommended to run this inside a virtual environment
```
$ python -m venv venv

// *nix
$ source venv/bin/activate

// Windows
C:\path\to\project> venv\Scripts\activate.bat
```
Install all dependencies
```
(venv) $ pip install -r requirements.txt
```
Run it. You can try one of the examples in ``example maze`` foder
```
(venv) $ python main.py example_maze/pixelPerfect.bmp
```
## Commandline Arguments
```
usage: main.py [-h] [--windowSize WINDOWSIZE] [--showExplored [SHOWEXPLORED]] [--gridScale GRIDSCALE] [--exploreInterval EXPLOREINTERVAL]
               [--pathInterval PATHINTERVAL]
               grid

positional arguments:
  grid                  Bitmap File to be solved

optional arguments:
  -h, --help            show this help message and exit
  --windowSize WINDOWSIZE
                        Size of the window
  --showExplored [SHOWEXPLORED]
                        Render explored area
  --gridScale GRIDSCALE
                        Scale of each cells within the grid
  --exploreInterval EXPLOREINTERVAL
                        How frequent should the algorithm tracks the explored area
  --pathInterval PATHINTERVAL
                        How many frames to skip when displaying the solved path

```