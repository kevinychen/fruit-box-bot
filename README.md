Fruit box bot
=============

A bot that plays the [Fruit Box game](https://en.gamesaien.com/game/fruit_box/), where you are
given a grid of apples, each with a number, and must repeatedly make boxes that enclose apples
summing to exactly 10.

![Playing](docs/playing.gif)


Demo Video
----------

Here is a full video with a score of 151 (some parts are sped up).

![Full](docs/full.gif)


Usage
-----

This bot uses Python 3 and Java 8.

This was tested on Chrome 94 on OS X 10.15.7. In particular, taking screenshots of the Apple retina
display gives images that are twice the expected size. On devices without the retina display, set
`SCALE = 1` [here](fruit_box_bot/__main__.py#L11).

- In the java directory, run `javac FruitBoxSolver.java`.
- In the root directory, run `poetry install`.
- Go to https://en.gamesaien.com/game/fruit_box/.
- Run `poetry shell` and in the fruit\_box\_bot directory, run `python .`.


Notes
-----

My highest manual scores were in the low 130s. First I made a straightforward greedy bot that
boxes in order (with the simple heuristic of making smaller boxes first). It averaged about 105
with a standard deviation of about 13, which was not enough to overtake my scores. This is
implemented in the repository as `solve1`.

So I set out to write a better bot. I tried some more heuristics such as choosing a box that
would unblock as many new boxes as possible, but ultimately I went with a recursive search.
The large 17x10 grid is too large for an exhaustive search, so I added some pruning strategies:

1. Stop at grid states that've been seen before, by maintaining a set of all grid hashes.
2. Keep track of where we're boxing in the grid at which scores. For example, if I'm currently
   boxing near the end of the grid for my 50th apple, but I previously found a solution where the
   50th apple is boxed near the beginning, then I might as well give up on this branch because
   it's unlikely I'll catch up to my best solution.
3. Add a hard stop after checking a given number of grids.

Unfortunately, Python is only able to search about 300,000 grids within the game timer. I still
managed scores that were about 5-10 higher than the greedy algorithm, and was able to beat my
manual high score (the bot got a 142).

Instead of taking more time to implement more heuristics, not knowing which ones would be
fruitful, I decided to just implement the algorithm in Java. This let me crank up the limit to 10
million (a ~30x increase) and even relax my Heuristic #2 as well. I've ran this on a few dozen
grids, and the best score is 151.


Credits
-------

Thanks to [GameSaien](https://en.gamesaien.com/) for creating this game and to
[this puzzle from Galactic Puzzle Hunt](https://2020.galacticpuzzlehunt.com/puzzle/letter-boxing),
which is how I heard about it.

