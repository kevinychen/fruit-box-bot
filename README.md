Fruit box bot
=============

A bot that plays the [Fruit Box game](https://en.gamesaien.com/game/fruit_box/), where you are
given a grid of apples, each with a number, and must repeatedly make boxes that enclose apples
summing to exactly 10.

![Playing](docs/playing.gif)


Demo Video
----------

Here is a video with a perfect score of 170!

![Full](docs/full.gif)


Usage
-----

This bot uses Python 3 and Rust.

This was tested on Chrome 112 on OS X 13.3.1, with Poetry 1.4.2 and Command Line Tools 14.3.
In particular, taking screenshots of the Apple retina display gives images that are twice the
expected size. On devices without the retina display, set `SCALE = 1` [here](main.py#L9).

The committed code will find the best solution for the first grid. To aim for a perfect score,
uncomment the optimizations [here](main.py#L31-L40): this will repeatedly reset the grid until a
perfect score is possible.

- In the root directory, run `poetry shell`, `poetry install` (this may take a while), and `maturin develop`.
- Go to https://en.gamesaien.com/game/fruit_box/.
- Run `python main.py`, then ensure the Fruit Box game is fully visible on your screen.


Credits
-------

Thanks to [GameSaien](https://en.gamesaien.com/) for creating this game and to
[this puzzle from Galactic Puzzle Hunt](https://2020.galacticpuzzlehunt.com/puzzle/letter-boxing),
which is how I heard about it.

