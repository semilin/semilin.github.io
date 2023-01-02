```{=org}
#+SETUPFILE: https://fniessen.github.io/org-html-themes/org/theme-readtheorg.setup
```
# Basic Usage

Genkey is a command line tool. This means that you perform actions by
running the binary through the terminal.

The binary is called `genkey.exe`{.verbatim} on Windows, or simply
`genkey`{.verbatim} on Linux or MacOS. From now on, the binary will just
be referred to as `genkey`{.verbatim}, so if you\'re using Windows, make
sure to correct it. Also note that you can autocomplete with TAB, in the
likely case that you don\'t want to type out the full name every time.

The general format of commands looks like this:

``` {.bash org-language="sh"}
./genkey COMMAND ARGUMENT
```

# Layouts

Layouts are stored as basic text files in the `layouts`{.verbatim}
subdirectory. Here is an example of its format, using the unholy layout
as reference.

    QWERTY
    q w e r t y u i o p [ ] \
    a s d f g h j k l ; '
    z x c v b n m , . /
    0 1 2 3 3 4 4 5 6 7 7 7 7
    0 1 2 3 3 4 4 5 6 7 7
    0 1 2 3 3 4 4 5 6 7 

The first line is used as the name of the layout - the name of the file
is **not** used by the program. Note that if two files have the same
layout name, only one will show up; the program will output no error if
this happens, so make sure that you rename it!

The next block of lines is the layout itself. This is pretty much
self-explanatory. However, at the moment genkey only supports 3 rows,
adding more will confuse it.

The final block defines what finger is used to hit each key. Each
finger, not including thumbs, is a digit from 0 to 7. Left pinky is 0,
right pinky is 7, and everything in between follows the order you would
expect. Thumb keys are not supported in genkey, but [Apsu\'s
fork](https://github.com/apsu/genkey) does add experimental support.

## ~generate~

The `_generate`{.verbatim} layout file is used to define the fingermap
for layouts created with the generate function. In addition, the main
key block can be used to pin keys for the improve function. Free keys
are labeled with `*`{.verbatim}, and pinned keys are labeled with
`X`{.verbatim}.

# Weighting

The weights that determine how layouts are scored is configured in
`weights.hjson`{.verbatim}. Though the base weights are made to be an
okay starting point, you are intended to experiment with them and shape
them to your liking.

The \"score\" is a very arbitrary number that should not be considered
an actual indicator of a layout\'s \"objective\" quality. The score is
calculated from the user\'s approximations of their personal
preferences. Anything that comes from personal preference can\'t be
objective, so do not treat it as such. Beating some layout\'s score is
great, but that doesn\'t mean it\'s actually better.

Note: higher score is worse, lower score is better.

## Distance

This is the way to calculate distance between any two given keys on a
layout.

Where $l$ is the lateral movement multiplier, the expression for
weighted distance is as follows:

```{=latex}
\begin{equation}
(l \times \Delta{x}^2) + (\Delta{y}^2)
\end{equation}
```
This is the formula for distance, except not square rooted as to treat
distance exponentially.

## Finger Speed

At a high level, finger speed is basically just looking at bigrams and
skipgrams with an adaptation of the rate equation:

```{=latex}
\begin{equation}
   r=\frac{d}{n}
\end{equation}
```
$d$ is the distance between the two keys (see
[*\*Distance*]{.spurious-link target="*Distance"}). $n$ is the
\'length\' of the skip-gram, or how the distance between characters in
the sequence. For a bigram, $n$ is 1. For a skip-1-gram, (e.g.
`t_e`{.verbatim} in `the`{.verbatim}) $n$ is 2.

This equation effectively results in a time required to move a finger
from one key to another. Finger speed as a metric is the average of all
these times.

However, in reality there are more factors that affect this time.
Namely, different fingers differ greatly in how fast they can be moved.
Because of this, genkey has a KPS array, which defines how dexterous
each finger is. KPS stands for \"keys per second\", which is what the
numbers were originally based on.

In addition, though it would theoretically work out that a skip-1-gram
has exactly twice the time to travel as a bigram, some people care about
skipgrams less than others. Because of this, genkey allows you to weight
it.[^1]

Also, a KeyTravel weight is provided, which can help avoid the problem
of double letters (e.g. \"oo\") having 0 distance, and thus not being
counted at all. It\'s used as a baseline value for distance.

Considering these factors, the equation for a pair of keys ends up more
like the following (where $k$ is key travel, $F$ is the finger\'s
dexterity, and $c$ is the count of how many times the pair appears):

```{=latex}
\begin{equation}
r=c \times \frac{(d+k)\times F}{n}
\end{equation}
```
Genkey then gets the average time all of these same-finger pairs. The
lower that this metric is, the better. Though the original idea for this
was to be able to calculate how fast your fingers need to move to
maintain a given wpm, (hence the name) it is in reality much more
complicated than this. It\'s still a very useful metric, but take it
with a grain of salt.

## Index Balance

This is a very simple metric that punishes one index finger being used
much more than the other. It\'s just the expression $|l-r|$ where $l$
and $r$ are left and right index usage respectively. Increasing the
weight increases its addition to the score.

## LSB

LSB stands for Lateral Stretch Bigram. It refers to any adjacent finger
bigram where $\Delta x \ge 2$. This typically is used to mean bigrams
between index and middle fingers, but genkey also includes pinky and
ring in this calculation. More is worse, so increasing the weight value
increases how much it affects the score.

## Trigrams

Genkey uses trigrams to calculate rolls, alternation, redirects, and
onehand rolls.

The TrigramPrecision value determines how many of the most common
trigrams are used for this calculation. Since there are far more
trigrams than SFBs, the calculation slows down generation a lot, so you
probably don\'t want to use all of them. However, if you do, you can set
the value to 0. Otherwise, setting the value to -1 disables the
calculation.

### Rolls

Rolls are defined as 2 (not-same-finger) keys typed on one hand,
following or preceding 1 key pressed on the other. An inward roll is
where the direction of the 2 keys on the same hand approaches the index,
whereas an outward roll approaches the pinky. Since rolls are generally
desired, they subtract from the score.

### Alternation

Alternates are defined as trigrams where each key in the sequence
switches hands. Since alternation is generally desired, it subtracts
from the score.

### Redirects

Redirects are defined as trigrams where all keys are on the same hand,
but they do not all follow the same direction. For example,
`sfd`{.verbatim} would be a redirect on QWERTY, because the direction of
`sf`{.verbatim} is inward, but the direction of `fd`{.verbatim} is
outward. Since redirects are generally undesired, they add to the score.

### Onehands

Onehand rolls are defined as trigrams where all keys are on the same,
and they all follow the same direction. For example, `sdf`{.verbatim} on
QWERTY would be a onehand roll. Since onehands are generally desired,
they subtract from the score.

# Commands

## Load

Usage: `./genkey load FILEPATH`{.verbatim}

This takes in a text file path, processes it as a corpus, and updates
`data.json`{.verbatim} according to the text data that it collects. This
bigram and trigram frequency data is used for all other functions of the
program.

## Rank

Usage: `./genkey r`{.verbatim}

Outputs a ranked list of layouts next to their scores.

## Analyze

Usage: `./genkey a LAYOUT`{.verbatim}

Outputs detailed analysis of a layout.

## Generate

Usage: `./genkey g`{.verbatim}

Generate simply creates a new layout, and tries to minimize score. How
long this takes varies, but calculating trigrams significantly increases
the time. Otherwise, how long it takes is probably most dependent on
your CPU\'s multicore efficiency.

## Improve

Usage: `./genkey improve LAYOUT`{.verbatim}

Attempts to optimize the score of the given layout, without moving the
pinned keys (see [*\*\_generate*]{.spurious-link target="*_generate"}).

## Interactive

Usage: `./genkey i LAYOUT`{.verbatim}

The interactive mode is one of the more powerful parts of genkey. It
gives you tools to easily modify a layout and see the effects in
real-time. It\'s a fast and dynamic way to approach layout creation.

### Swap

Usage: `s key1 key2`{.verbatim}

Swaps two letters with each other.

Example: `s a b`{.verbatim}

### Column Swap

Usage: `cs key1 key2`{.verbatim} or `cs col1 col2`{.verbatim}

Swaps two columns with each other. If you provide a key, then it targets
the column where that key is located. If you provide a number, it
targets the column corresponding to that number.

Examples:

-   `cs a b`{.verbatim}
-   `cs 0 1`{.verbatim}

### Suggest

Usage: `g`{.verbatim}

Provides a suggestion of what two keys to swap. It does this with a
superficial neighbor search. It reports what score it will immediately
result in, and what score it can lead to.

### Save

Usage: `save`{.verbatim}

Asks you for a layout name, and writes the file. If the name is already
taken, you\'ll be asked if you want to overwrite it.

### Quit

Usage: `q`{.verbatim}

Is an explanation for this necessary

# Footnotes

[^1]: When semi came up with the finger speed concept, they coined the
    term \"disjointed bigram\". Though a fancy sounding name, skipgram
    is an already existing term that fits better. Despite this, DSFB
    (\"disjointed same-finger bigram\") is still used relatively
    frequently, which is why it\'s called that in genkey.