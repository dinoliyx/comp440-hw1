"""
Part 1: whose data is this?

    uv run python part1_data.py

Write your own cut rule and your two checks before you run anything here. Doing it in that
order is what Part 1 is asking for. What this script must print, under the labels shown:

    == (a) how much ==
        Rows in each of the four files, distinct users, distinct movies, and the share of
        all 32,000,204 MovieLens ratings this set holds.

    == (b) spread ==
        Ratings per user and ratings per movie: median, minimum and maximum of each. Tag
        applications per user and per movie: the same three. How many of the users who
        rated anything ever applied a tag, as a count and as a share.

    == (c) top tags, two ways ==
        The 20 most-used tags by number of applications, and the 20 most-used tags by number
        of distinct users who applied them. Print the two lists one after the other, with
        both numbers on every row, so you can see where a tag's two ranks differ.

    == (d) two checks ==
        Two claims from (a) to (c) re-derived by a route that does not reuse the code that
        produced them, printed with both numbers side by side and the word MATCH or DIFFER.
        Targets that exist in this data: the share of all 32M ratings the set holds
        (`data/README.md` says 15.6 percent); the number of distinct users who applied a
        tag (14,019); the rating count of the least-rated kept movie (83); the 6 tag
        rows whose text is literally `NA`, which vanish if a reader is built without
        `keep_default_na=False`.

No figures are required in Part 1. `WRITEUP.md` takes one interesting thing from
`data/README.md`, your own cut rule and the rule you rejected, how `data/make_compact.py`'s
rule differs from yours, and your two checks.
"""

import csv
import gzip

from load_data import DATA, load_all


FULL_RATINGS = 32_000_204   # MovieLens 32M, from data/README.md


def three(s):
    """Median, minimum and maximum of a count series, on one line."""
    return f"median {s.median():g}, min {s.min():,}, max {s.max():,}"


def top_decile_share(counts):
    """Share of all rows contributed by the top 10% of contributors."""
    counts = counts.sort_values(ascending=False)
    n = max(1, round(len(counts) * 0.10))
    return n, counts.head(n).sum() / counts.sum()


def part1_data(ratings, tags, movies, links):
    print("== (a) how much ==")
    for name, df in [("ratings", ratings), ("tags", tags), ("movies", movies), ("links", links)]:
        print(f"{name:8} {len(df):>10,} rows")
    print(f"distinct users who rated: {ratings.userId.nunique():,}")
    print(f"distinct users who tagged: {tags.userId.nunique():,}")
    print(f"distinct users in either: {len(set(ratings.userId) | set(tags.userId)):,}")
    print(f"distinct movies rated: {ratings.movieId.nunique():,}")
    print(f"distinct movies tagged: {tags.movieId.nunique():,}")
    print(f"share of all {FULL_RATINGS:,} MovieLens 32M ratings: {len(ratings) / FULL_RATINGS:.1%}")

    print("== (b) spread ==")
    r_user = ratings.groupby("userId").size()
    r_movie = ratings.groupby("movieId").size()
    t_user = tags.groupby("userId").size()
    t_movie = tags.groupby("movieId").size()
    print(f"ratings per user:  {three(r_user)}")
    print(f"ratings per movie: {three(r_movie)}")
    print(f"tags per tagging user:  {three(t_user)}")
    print(f"tags per tagged movie:  {three(t_movie)}")
    raters = set(ratings.userId)
    raters_who_tagged = raters & set(tags.userId)
    print(f"users who rated anything and ever applied a tag: {len(raters_who_tagged):,} "
          f"of {len(raters):,} ({len(raters_who_tagged) / len(raters):.1%})")
    n, share = top_decile_share(r_user)
    print(f"top 10% of raters ({n:,} users) account for {share:.1%} of all ratings")
    n, share = top_decile_share(t_user)
    print(f"top 10% of taggers ({n:,} users) account for {share:.1%} of all tag applications")

    print("== (c) top tags, two ways ==")
    print("Raw tag strings, exactly as typed: `Cult classic` and `cult classic` are two rows here.")
    by_tag = tags.groupby("tag").agg(applications=("userId", "size"), users=("userId", "nunique"))
    for col in ["applications", "users"]:
        print(f"-- top 20 by {col} --")
        top = by_tag.sort_values([col, "tag"], ascending=[False, True]).head(20)
        print(top.to_string())

    print("== (d) two checks ==")
    # Check 1, the student's route: rank taggers by how many distinct tags they used, keep
    # the top 10%, and divide their tag applications by all tag applications.
    pairs = tags[["userId", "tag"]].drop_duplicates()
    distinct = pairs["userId"].value_counts().sort_index().sort_values(ascending=False, kind="stable")
    k = round(len(distinct) * 0.10)
    top_users = distinct.index[:k]
    tied = (distinct == distinct.iloc[k - 1]).sum()
    mine = tags["userId"].isin(top_users).sum() / len(tags)
    _, claude = top_decile_share(t_user)
    print(f"check 1: top 10% of taggers' share of tag applications")
    print(f"  (b), ranked by applications:   {claude:.1%}")
    print(f"  ranked by distinct tags used:  {mine:.1%}  ({k:,} users; "
          f"{tied:,} users tie at the cutoff of {distinct.iloc[k - 1]:,} distinct tags, broken by userId)")
    print(f"  {'MATCH' if round(claude, 3) == round(mine, 3) else 'DIFFER'}")
    # Check 2, the student's route: read tags.csv.gz with the csv module, which parses quoted
    # fields and never turns a string into a missing value, and count tags that are exactly NA.
    with gzip.open(DATA / "tags.csv.gz", "rt", encoding="utf-8", newline="") as f:
        csv_na = sum(1 for row in csv.DictReader(f) if row["tag"] == "NA")
    pandas_na = (tags["tag"] == "NA").sum()
    print("check 2: tag rows whose text is exactly NA")
    print(f"  load_tags() (pandas, keep_default_na=False): {pandas_na:,}")
    print(f"  csv module on tags.csv.gz:                   {csv_na:,}")
    print(f"  {'MATCH' if pandas_na == csv_na else 'DIFFER'}")


if __name__ == "__main__":
    ratings, tags, movies, links = load_all()
    part1_data(ratings, tags, movies, links)
