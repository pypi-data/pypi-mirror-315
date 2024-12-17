# Readme

Quid is a tool for quotation detection in two texts, called source and target. If possible, the source text should be
the one that is quoted by the target text. This allows the algorithm to handle common properties of quotations, for
example, ellipses or inaccurate quotations. The following is an example output: 

~~~
0	52	This is a long Text and the long test goes on and on
0	45	This is a long Text [...] test goes on and on
~~~

## Demo Website
A [demo website](https://pages.cms.hu-berlin.de/schluesselstellen/quidweb/) is available for testing Quid.

## Installation
~~~
pip install Quid
~~~

## Usage
There are two ways to use the algorithm, in code and from the command line.

### In Code

The algorithm can be found in the package `quid`. To use it create a `Quid` object which can be configured with a number
of arguments. To use all default arguments, the most basic use would like this:

~~~
from quid.core.Quid import Quid

quid = Quid()
matches = quid.compare('file 1 content', 'file 2 content')
~~~

`Compare` returns a list with the following structure: `List[Match]`. `Match` stores two `MatchSpans`. One for the
source text and one for the target text. `MatchSpan` stores the `start` and `end` character positions for the matching
spans in the source and target text.

<details>
<summary>All arguments to configure the Quid object.</summary>

- The minimum number of tokens of a match (default: 5)
- The maximum number of tokens to skip when extending a match backwards (default: 10)
- The maximum number of tokens to skip when extending a match forwards (default: 3)
- The maximum distance in tokens between to matches considered for merging (default: 2)
- The maximum distance in tokens between two matches considered for merging where the target text contains an ellipses between the matches (default: 10)
- Whether to include matched text in the returned data structure (default: True)
- How to handle ambiguous matches. If False, for a match with multiple matched segments in the source text, multiple matches will be returned. Otherwise, only the first match will be returned. (default: False)
- The threshold for the minimal levenshtein similarity between tokens (and the initial n-grams) to be accepted as a match (default: 0.85)
- Whether to split texts which are longer than the threshold (in words) defined with `split_length` for faster processing (default: False)
- The threshold for splitting texts (in number of words) (default: 30000)
- The maximum number of processes for parallel processing (default: 1)

</details>

### Command line
The `quid compare` command provides a command line interface to the algorithm.

To use all default arguments, the most basic command would look like this:

~~~
quid compare file_1_path file_2_path
~~~

By default, the result is returned as a json structure: `List[Match]`. `Match` stores two `MatchSpans`. One for
the source text and one for the target text. `MatchSpan` stores the `start` and `end` character positions for the
matching spans in the source and target text. For example:

~~~
[
  {
    "source_span": {
      "start": 0,
      "end": 52,
      "text": "This is a long Text and the long test goes on and on"
    },
    "target_span": {
      "start": 0,
      "end": 45,
      "text": "This is a long Text [...] test goes on and on"
    }
  }
]
~~~

Alternatively, the result can be printed in a human-readable text format with the command line option
`--output-type text`. This will result in the following output:

~~~
0	52	This is a long Text and the long test goes on and on
0	45	This is a long Text [...] test goes on and on 
~~~

In case the matching text is not needed, the option `--no-text` allows to exclude the text from the output.

<details>
<summary>All command line options</summary>

~~~
usage: quid compare [-h] [--text | --no-text] [--output-type {json,text,csv}]
                    [--csv-sep CSV_SEP]
                    [--output-folder-path OUTPUT_FOLDER_PATH]
                    [--min-match-length MIN_MATCH_LENGTH]
                    [--look-back-limit LOOK_BACK_LIMIT]
                    [--look-ahead-limit LOOK_AHEAD_LIMIT]
                    [--max-merge-distance MAX_MERGE_DISTANCE]
                    [--max-merge-ellipsis-distance MAX_MERGE_ELLIPSIS_DISTANCE]
                    [--create-dated-subfolder | --no-create-dated-subfolder]
                    [--max-num-processes MAX_NUM_PROCESSES]
                    [--keep-ambiguous-matches | --no-keep-ambiguous-matches]
                    [--min-levenshtein-similarity MIN_LEVENSHTEIN_SIMILARITY]
                    [--split-long-texts | --no-split-long-texts]
                    [--split-length SPLIT_LENGTH]
                    source-file-path target-path

Quid compare allows the user to find quotations in two texts, a source text
and a target text. If known, the source text should be the one that is quoted
by the target text. This allows the algorithm to handle things like ellipsis
in quotations.

positional arguments:
  source-file-path      Path to the source text file
  target-path           Path to the target text file or folder

options:
  -h, --help            show this help message and exit
  --text, --no-text     Include matched text in the returned data structure
                        (default: True)
  --output-type {json,text,csv}
                        The output type
  --csv-sep CSV_SEP     output separator for csv (default: '\t')
  --output-folder-path OUTPUT_FOLDER_PATH
                        The output folder path. If this option is set the
                        output will be saved to a file created in the
                        specified folder
  --min-match-length MIN_MATCH_LENGTH
                        The minimum number of tokens of a match (>= 1,
                        default: 5)
  --look-back-limit LOOK_BACK_LIMIT
                        The maximum number of tokens to skip when extending a
                        match backwards (>= 0, default: 10)
  --look-ahead-limit LOOK_AHEAD_LIMIT
                        The maximum number of tokens to skip when extending a
                        match forwards (>= 0, default: 3)
  --max-merge-distance MAX_MERGE_DISTANCE
                        The maximum distance in tokens between two matches
                        considered for merging (>= 0, default: 2)
  --max-merge-ellipsis-distance MAX_MERGE_ELLIPSIS_DISTANCE
                        The maximum distance in tokens between two matches
                        considered for merging where the target text contains
                        an ellipsis between the matches (>= 0, default: 10)
  --create-dated-subfolder, --no-create-dated-subfolder
                        Create a subfolder named with the current date to
                        store the results (default: False)
  --max-num-processes MAX_NUM_PROCESSES
                        Maximum number of processes to use for parallel
                        processing
  --keep-ambiguous-matches, --no-keep-ambiguous-matches
                        For a match with multiple matched segments in the
                        source text, multiple matches will be returned.
                        (default: False)
  --min-levenshtein-similarity MIN_LEVENSHTEIN_SIMILARITY
                        The threshold for the minimal levenshtein similarity
                        between tokens (and the initial n-grams) to be
                        accepted as a match (between 0 and 1, default: 0.85)
  --split-long-texts, --no-split-long-texts
                        Split texts longer than split-length words for faster
                        processing (default: False)
  --split-length SPLIT_LENGTH
                        If split-long-texts is set to True, texts longer (in
                        number of words) than this threshold will be split for
                        faster processing.
~~~

</details>

## Parallel processing
Quid supports using multiple processes when comparing multiple target texts with the source texts. To use multiple
processes the command line option `--max-num-processes` is used. The default is 1.

## Processing "long" texts
Depending on the length of the texts and the hardware used, processing times can get quite long. For texts longer than
a couple of hundreds of thousands characters, it can make sense to use the `--split-long-texts` command line option (or
`split_long_texts` argument) and set `--max-num-processes` (or `max_num_processes` argument) to define the number of
parallel processes to be used. If `--split-long-texts` is used, texts longer than the default of 30000 tokens will be
split. This limit can also be changed using the `--split-length` command line option (or `split_length` argument).
When run from the command line, using `--split-long-texts` automatically shows a progress bar. To show a progress bar
when using Quid in code, the `show_progress` argument can be set to `True`.

*Note*: `--split-long-texts` does not work in combination with comparing multiple target texts (i.e. passing a folder as
`target-path`).

## Passager
The package `passager` contains code to extract key passages from the found matches. The `passage` command produces
several json files.
The resulting data structure is documented in the [data structure readme](DATA_STRUCTURE_README.md).

<details>
<summary>All command line options</summary>

~~~
usage: quid passage [-h]
                    source-file-path target-folder-path
                    matches-folder-path output-folder-path

Quid passage allows the user to extract key passages from the found
matches.

positional arguments:
  source-file-path     Path to the source text file
  target-folder-path   Path to the target texts folder path
  matches-folder-path  Path to the folder with the match files
  output-folder-path   Path to the output folder
~~~

</details>

## Visualization
The package `visualization` contains code to create the content for a web page to visualize the key passages.
For a white label version of the website, see [QuidEx-wh](https://scm.cms.hu-berlin.de/schluesselstellen/quidex-wh).

<details>
<summary>All command line options</summary>

~~~
usage: quid visualize [-h] [--title TITLE] [--author AUTHOR]
                      [--year YEAR] [--censor]
                      source-file-path target-folder-path
                      passages-folder-path output-folder-path

Quid visualize allows the user to create the files needed for a website that
visualizes the Quid algorithm results.

positional arguments:
  source-file-path      Path to the source text file
  target-folder-path    Path to the target texts folder path
  passages-folder-path
                        Path to the folder with the key passages files, i.e.
                        the resulting files from Quid passage
  output-folder-path    Path to the output folder

optional arguments:
  -h, --help            show this help message and exit
  --title TITLE         Title of the work
  --author AUTHOR       Author of the work
  --year YEAR           Year of the work
~~~

</details>

## Logging
By default, the log level is set to `WARN`. This can be changed with the `--log-level` command line option.
For example:

~~~
quid --log-level INFO compare …
~~~

## Performance
For in-depth information on the evaluation, see our [publication](https://aclanthology.org/2021.nlp4dh-1.7).
Performance of the current version of Quid is as follows:

| Work             | Precision | Recall | F-Score |
|------------------|-----------|--------|---------|
| Die Judenbuche   | 0.83      | 0.92   | 0.87    |
| Micheal Kohlhaas | 0.71      | 0.93   | 0.81    |

## History
Quid was formerly known as Lotte and later renamed. Earlier publications use the name Lotte.

## Data
All data, which can be made available, can be found in our [Quid Resource Repository](https://scm.cms.hu-berlin.de/schluesselstellen/quid-resources).
Due to copyright restrictions, it is unfortunately not possible to publish the complete scholarly works.

## Citation
If you use Quid or base your work on our code, please cite our paper:

~~~
@inproceedings{arnold2021lotte,
  title = {{L}otte and {A}nnette: {A} {F}ramework for {F}inding and {E}xploring {K}ey {P}assages in {L}iterary {W}orks},
  author = {Arnold, Frederik and Jäschke, Robert},
  booktitle = {Proceedings of the Workshop on Natural Language Processing for Digital Humanities},
  year = {2021},
  publisher = {NLP Association of India (NLPAI)},
  url = {https://aclanthology.org/2021.nlp4dh-1.7},
  pages = {55--63}
}
~~~

## Acknowledgements
The algorithm is inspired by _sim_text_ by Dick Grune [^1]
and _Similarity texter: A text-comparison web tool based on the “sim_text” algorithm_ by Sofia Kalaidopoulou (2016) [^2]

[^1]: https://dickgrune.com/Programs/similarity_tester/ (Stand: 12.04.2021)

[^2]: https://people.f4.htw-berlin.de/~weberwu/simtexter/522789_Sofia-Kalaidopoulou_bachelor-thesis.pdf (Stand: 12.04.2021)
