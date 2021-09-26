Fruit box bot
=============

A bot that plays the [Fruit Box game](https://en.gamesaien.com/game/fruit_box/), where you are
given a grid of apples, each with a number, and must repeatedly make boxes that enclose apples
summing to exactly 10.

![Playing](docs/playing.gif)


Demo Video
----------

Here is a full video with a score of 151 (parts without activity are sped up).

![Full](docs/full.gif)


Usage
-----

This bot uses Python 3 and Java 8.

This was tested on Chrome 94 on OSX 10.15.7. In particular, taking screenshots of the OSX retina
display gives images that are twice the expected size. On devices without the retina display, set
`SCALE = 1` [here](fruit_box_bot/__main__.py#11).

- In the java directory, run `javac FruitBoxSolver.java`.
- In the root directory, run `poetry install`.
- Go to https://en.gamesaien.com/game/fruit\_box/.
- Run `poetry shell` and in the fruit\_box\_bot directory, run `python .`.


Notes
-----

My highest manual scores in this game are in the low 130s. Writing a simple greedy bot that just
boxes in order (with the simple heuristic of making smaller boxes first) gave scores that averaged
about 105 with a standard deviation of about 13, which was not enough to overtake my scores. This
is implemented in the repository as `solve1`.

So I set out to write a smarter bot. I tried some better heuristics such as choosing a box that
would open up as many new boxes as possible, but ultimately I went with as thorough of a brute
force search as possible. The large grid (17x10) is too large to do an exhaustive search, so I
had to add some pruning strategies:

1. Stop if you end up in a grid state that's seen before. I keep a set of all grid hashes. It's
   possible that a new grid may be pruned away due to a hash collision, but the chance of this is
   negligible.
2. Keep track of where we're boxing in the grid at which scores. For example, if I'm currently
   trying to box toward the end of the grid for my 50th apple (the search is done in reading
   order), but I previously already found a solution where the 50th apple is boxed toward the
   beginning of the grid, then I might as well give up my search because it's unlikely I'll catch
   up to my best solution.
3. Add a hard stop after checking a given number of grids.

Unfortunately, in Python I had to provide a hard stop of at most 300,000 to have time to actually
perform the boxing motions in the game itself. This resulted in scores that were about 5-10 higher
than the greedy algorithm (just a rough estimate, as I don't have many data points here). Now I
was able to get scores that beat my manual ones (the bot got a 142), but I wanted to do better.

Instead of taking more time to implement more heuristics, not knowing which ones would be
fruitful, I decided to just implement the algorithm in Java. Turns out this let me crank up the
limit to 10 million (a ~30x increase) and even relax my Heuristic #2 as well. And that's the
latest version of the bot!


Credits
-------

Thanks to [GameSaien](https://en.gamesaien.com/) for creating this fun game and to
[Galactic Puzzle Hunt](https://2020.galacticpuzzlehunt.com/puzzle/letter-boxing), which is
how I heard about it.

