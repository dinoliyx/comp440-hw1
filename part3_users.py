"""
Part 3: what tags best describe a user?

    uv run python part3_users.py

The handout's Part 3 is the spec. One piece is written for you, the piece that has to agree
with `WRITEUP.md` line for line: reading the 20 ratings out of your "My 20 ratings" slot and
adding you to the ratings table as a user of your own. Everything after that is yours.

You are added under userId 999999. Real userIds in `data/ratings.csv.gz` stop at 200,935, so
that number cannot be a real person's, and it is easy to pick out of a printout.

What this script must print, under the labels shown:

    == (1) my ratings ==
        How many ratings were read out of your slot, how many lines it could not read a
        rating from, and how many rows the ratings table has with yours in it. Twenty
        ratings is what the handout asks for; the script reports what it found and leaves
        the count to you.

    == (2) score(user, tag) ==
        Your `score(user, tag)` over the users you are looking at, your own row included.
        Write it in this file as

            score(ratings_df, tags_df, movies_df) -> DataFrame[userId, tag, score]

        one row per user-tag pair, higher score meaning the tag describes the user better.
        Print your own ten best tags, and the number of rows and distinct users it returned.
        What the score is, and why you started there, is yours and goes in `WRITEUP.md`.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from load_data import load_all
from part2_tags import score as movie_score   # the student's Part 2 score(movie, tag)
from part2_tags import tag_key

REPO = Path(__file__).resolve().parent
WRITEUP = REPO / "WRITEUP.md"

ME = 999999                 # your userId: above every real one, so it collides with nobody
SLOT = "My 20 ratings"      # the WRITEUP.md slot your ratings are read from


def read_my_ratings(writeup: Path = WRITEUP) -> tuple[pd.DataFrame, int]:
    """Your ratings from the "My 20 ratings" slot in WRITEUP.md, as movieId and rating.

    The same rule the judge uses for "My ten movies": every line in that slot starts with a
    movieId. The rating is the last number on the line, so the title between them is for
    people and may hold anything, the year included. Bare lines only: a bulleted or a
    numbered list reads as no ratings at all, or reads the list numbers as movieIds.

        296, Pulp Fiction (1994), 4.5

    A line whose last number is not a rating between 0.5 and 5.0 is left out and counted,
    because the year in a title is a number too: `296, Pulp Fiction (1994)` with the rating
    forgotten would otherwise be read as a rating of 1994. So is the `XXXX` an unfilled slot
    holds, which is why this is safe to run before you have written anything.

    Returns the ratings and how many lines were left out."""
    rows, skipped, inside = [], 0, False
    for line in writeup.read_text(encoding="utf-8").splitlines():
        if line.startswith("**"):            # a bold label opens the next slot
            inside = SLOT in line
            continue
        if not inside or not re.match(r"\s*\d", line):
            continue
        numbers = re.findall(r"\d+(?:\.\d+)?", line)
        rating = float(numbers[-1]) if len(numbers) > 1 else 0.0
        if not 0.5 <= rating <= 5.0:
            skipped += 1
            continue
        rows.append({"movieId": int(numbers[0].split(".")[0]), "rating": rating})
    return pd.DataFrame(rows, columns=["movieId", "rating"]), skipped


def add_me(ratings: pd.DataFrame, mine: pd.DataFrame) -> pd.DataFrame:
    """Your ratings appended to everybody else's, under userId ME.

    The timestamp is the newest one in the data: you rated these after everyone else did."""
    if mine.empty:
        return ratings
    mine = mine.assign(userId=ME, timestamp=int(ratings["timestamp"].max()))
    return pd.concat([ratings, mine[ratings.columns]], ignore_index=True)


# ------------------------------------------------------------------- yours to write ---

def favorites(ratings: pd.DataFrame, movies: pd.DataFrame, user: int) -> pd.DataFrame:
    """A user's TOP_MOVIES highest-rated movies, ties alphabetical by title: the films the
    description names, and since Improvement 1 the only films whose tags are scored."""
    theirs = ratings[ratings["userId"] == user].join(movies.set_index("movieId"), on="movieId")
    return theirs.sort_values(["rating", "title"], ascending=[False, True]).head(TOP_MOVIES)


def score(ratings: pd.DataFrame, tags: pd.DataFrame, movies: pd.DataFrame, users=(ME,),
          favorites_only=True):
    """The student's score(user, tag).

    Improvement 1 (favorites_only): only tags that appear on the user's TOP_MOVIES favorite
    movies, the ones their description lists, get a score; every other tag is dropped. The
    value of a kept tag is still the first version's sum over all the user's rated movies.

    First version:

    For each movie the user rated: distance = their rating minus the average rating of every
    other user on that movie. Each tag's weight on that movie is the Part 2 score(movie, tag).
    score(user, tag) is the sum, over the user's rated movies, of distance times weight.

    `users` is which users to score; the join is one row per rating per tag on the movie, so
    scoring all 23,000 users at once does not fit in memory."""
    stats = ratings.groupby("movieId")["rating"].agg(["sum", "count"])
    theirs = ratings[ratings["userId"].isin(users)].join(stats, on="movieId")
    # The average of every OTHER user: this user's own rating is taken out of the movie's mean.
    others = (theirs["count"] - 1).where(theirs["count"] > 1)
    theirs = theirs.assign(distance=theirs["rating"] - (theirs["sum"] - theirs["rating"]) / others)
    weights = movie_score(tags, ratings, movies)
    pairs = theirs[["userId", "movieId", "distance"]].merge(weights, on="movieId")
    pairs["score"] = pairs["distance"] * pairs["score"]
    out = pairs.groupby(["userId", "tag"], as_index=False)["score"].sum()
    if favorites_only:
        fav = pd.concat([favorites(ratings, movies, u)[["userId", "movieId"]] for u in users])
        on_fav = fav.merge(weights[["movieId", "tag"]], on="movieId")[["userId", "tag"]]
        out = out.merge(on_fav.drop_duplicates(), on=["userId", "tag"])
    return out


# The student's rule for who goes in judge/users.csv: them, plus three groups of three.
MIN_SHARED = 10      # overlap and contrasting users rated at least this many of my 20
PER_GROUP = 3
SEED = 452           # for the random three


def choose_people(ratings: pd.DataFrame, mine: pd.DataFrame) -> pd.DataFrame:
    """Me, the PER_GROUP users with the lowest and the highest mean absolute error against my
    ratings (over the movies we both rated, among users sharing at least MIN_SHARED of
    them), and PER_GROUP users drawn at random from everybody else, under SEED."""
    others = ratings[ratings["userId"] != ME]
    stars = mine.set_index("movieId")["rating"]
    shared = others[others["movieId"].isin(stars.index)]
    shared = shared.assign(err=(shared["rating"] - shared["movieId"].map(stars)).abs())
    by_user = shared.groupby("userId").agg(shared=("movieId", "size"), mae=("err", "mean"))
    pool = by_user[by_user["shared"] >= MIN_SHARED].sort_values(["mae", "shared"])
    close, far = pool.head(PER_GROUP), pool.tail(PER_GROUP).iloc[::-1]
    taken = set(close.index) | set(far.index)
    everyone = pd.Series(sorted(set(others["userId"]) - taken))
    drawn = everyone.sample(PER_GROUP, random_state=SEED).tolist()
    rows = ([{"userId": ME, "group": "me"}]
            + [{"userId": u, "group": "overlap"} for u in close.index]
            + [{"userId": u, "group": "contrasting"} for u in far.index]
            + [{"userId": u, "group": "random"} for u in drawn])
    people = pd.DataFrame(rows).join(by_user, on="userId")
    people.attrs["pool_mae"] = pool["mae"].mean()
    return people


TOP_MOVIES = 3       # favourite movies named in a description
TAGS_JUDGED = 10     # tags per person sent to the judge
USERS_CSV = REPO / "judge" / "users.csv"


def judged_tags(scored: pd.DataFrame) -> pd.DataFrame:
    """The student's rule for which tags the judge rates: keep only score rows whose tag is in
    judge/vocabulary.txt (both merged by tag_key), then each person's TAGS_JUDGED highest
    scores, ties alphabetical. The tag is sent in its vocabulary spelling."""
    words = [t.strip() for t in (REPO / "judge" / "vocabulary.txt").read_text().splitlines()
             if t.strip()]
    spelling = {tag_key(w): w for w in words}
    valid = scored[scored["tag"].isin(spelling)]
    top = (valid.sort_values(["userId", "score", "tag"], ascending=[True, False, True])
           .groupby("userId").head(TAGS_JUDGED))
    return top.assign(tag=top["tag"].map(spelling))


def describe(ratings: pd.DataFrame, movies: pd.DataFrame, people: pd.DataFrame,
             pool_mae: float) -> pd.Series:
    """The student's description of each person, for judge/users.csv: their group; "high
    alignment" when their MAE against me is below pool_mae (the average over the users who
    share at least MIN_SHARED of my movies), "low alignment" when above, NA with no MAE; their
    TOP_MOVIES highest-rated movies, ties alphabetical by title; and the one genre they rated
    most often, each movie counting once toward each of its genres, ties alphabetical."""
    films = movies.set_index("movieId")
    out = {}
    for row in people.itertuples():
        theirs = ratings[ratings["userId"] == row.userId].join(films, on="movieId")
        best = favorites(ratings, movies, row.userId)
        genres = theirs["genres"].str.split("|").explode().value_counts()
        genres = genres.rename_axis("genre").reset_index().sort_values(
            ["count", "genre"], ascending=[False, True])
        align = ("NA" if pd.isna(row.mae)
                 else "high alignment" if row.mae < pool_mae else "low alignment")
        out[row.userId] = (f"group: {row.group}; alignment with me: {align}; "
                           f"favorite movies: {', '.join(best['title'])}; "
                           f"top genre: {genres['genre'].iloc[0]}")
    return pd.Series(out, name="description")


def part3_users(ratings, tags, movies, links):
    print("== (1) my ratings ==")
    mine, skipped = read_my_ratings()
    print(f'{len(mine)} rating(s) read from the "{SLOT}" slot in WRITEUP.md.')
    if not len(mine):
        print(f'Nothing was read out of the "{SLOT}" slot. It is read one rating to a line, '
              f"with no bullets and no numbering: the movieId first, then the title, then "
              f"your rating, as in `296, Pulp Fiction (1994), 4.5`.")
    if skipped:
        print(f"{skipped} line(s) in that slot had no rating between 0.5 and 5.0 at the "
              f"end and were left out.")
    ratings = add_me(ratings, mine)
    if len(mine):
        print(f"{len(ratings):,} ratings with yours in, as userId {ME}.")
    else:
        print(f"{len(ratings):,} ratings, none of them yours yet.")

    print("== (2) score(user, tag) ==")
    scored = score(ratings, tags, movies)
    print(f"{len(scored):,} user-tag rows over {scored.userId.nunique():,} user(s).")
    top = scored[scored.userId == ME].sort_values(["score", "tag"], ascending=[False, True])
    print(f"my ten best tags (userId {ME}; tags shown as their Part 2 merged key):")
    print(top.head(10)[["tag", "score"]].to_string(index=False, float_format="{:.4f}".format))

    print("== (3) who goes to the judge ==")
    people = choose_people(ratings, mine)
    print(f"me, {PER_GROUP} lowest and {PER_GROUP} highest mean absolute error among users who "
          f"rated at least {MIN_SHARED} of my movies, {PER_GROUP} random (seed {SEED}):")
    print(people.to_string(index=False, float_format="{:.3f}".format))
    pool_mae = people.attrs["pool_mae"]
    print(f"average MAE over the users who rated at least {MIN_SHARED} of my movies: {pool_mae:.3f}")
    print("descriptions:")
    descriptions = describe(ratings, movies, people, pool_mae)
    for user, text in descriptions.items():
        print(f"  {user}: {text}")

    print("== (4) judge/users.csv ==")
    scored_people = score(ratings, tags, movies, users=list(people["userId"]))
    chosen = judged_tags(scored_people)
    for user in people["userId"]:
        mine_top = chosen[chosen["userId"] == user]
        print(f"  {user}: {len(mine_top)} tags: " + ", ".join(mine_top["tag"]))
    # Like judge/movies.csv: tags joined with | and sorted alphabetically, so their order does
    # not tell the judge which one scored highest.
    joined = chosen.groupby("userId")["tag"].apply(lambda t: "|".join(sorted(t)))
    users_csv = pd.DataFrame({"id": people["userId"],
                              "description": people["userId"].map(descriptions),
                              "tags": people["userId"].map(joined).fillna("")})
    users_csv.to_csv(USERS_CSV, index=False)
    print(f"wrote {USERS_CSV.relative_to(REPO)}: {len(users_csv)} people, "
          f"{len(chosen)} user-tag pairs")


if __name__ == "__main__":
    ratings, tags, movies, links = load_all()
    part3_users(ratings, tags, movies, links)
