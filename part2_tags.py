"""
Part 2: what tags best describe a movie?

    uv run python part2_tags.py

Steps 1 to 4 of the handout's Part 2 live here, plus the scores and the rankings that steps 5
and 6 need. The judge itself runs through `/judge`, and its answer is read through
`agreement.py` and `results_viewer.py`. What this script must print, under the labels shown,
and what it must write:

    == (1) the obvious answer ==
        Your chosen movie's title, its rating count and its tag-application count, then
        every tag applied to it with how many times it was applied, most-applied first.
        Pick a movie with at least 500 ratings and 30 tag applications. The most misleading
        entry in that list is your sentence in `WRITEUP.md`, not this script's.

    == (2) up close ==
        The numbers behind the one required figure and the two tables, so that everything
        shown here has printed output a reader can check it against. Write, to `figures/`:

            figures/part2_when.png          when the tags arrived: tag applications over
                                            time, with the movie's ratings over time behind
                                            them.

        The figure has labeled axes and a caption naming the question it answers. Claude
        may draw and label it; the sentence in `WRITEUP.md` about what it shows is yours.

        Then two tables, each printed under its own label:

            who added each tag              the movie's heaviest taggers, how many tag
                                            applications each made, and what share of the
                                            movie's applications that is.
            how the taggers rated it        for each of the movie's top tags, how the
                                            people who applied it rated the movie, beside
                                            how everyone else rated it.

        Claude prints the tables and says what the columns are. What they show is your two
        interesting details in `WRITEUP.md`, not this script's.

    == (3) my definition ==
        Your `score` over the whole set. Write it in this file as

            score(tags_df, ratings_df, movies_df) -> DataFrame[movieId, tag, score]

        one row per movie-tag pair, higher score meaning the tag describes the movie better.
        Print its top 15 rows for your chosen movie, and the number of rows and distinct
        movies it returned over the whole set. Families you could use, none of them
        preferred: distinct users who applied the tag; a rarity weight, the count times how
        few movies carry the tag; a damped version of either; something of your own. Whatever
        you choose, `WRITEUP.md` gets what you chose, what you rejected, and why.

    == (4) cleaning ==
        Whatever cleaning your `score()` does, and its size: how many raw tag strings went
        in, how many distinct tags came out, and the five mergers that absorbed the most
        applications. If you clean nothing, print that and say why in `WRITEUP.md`.
        Merging `Sci-Fi`, `sci-fi` and `scifi` is a decision, and so is not merging them.

    == (5) scores.csv ==
        `scores.csv` in the repo root, columns `movieId,tag,score`, holding a score for every
        movie and tag the judge will be asked about. That is two sets put together:

            every movie and tag in `judge/movies.csv`, which has one row per movie and a
            `tags` column of tags joined by `|`;
            plus, for each of the ten movies in your "My ten movies" slot, every tag from
            `judge/vocabulary.txt` that appears on it, matched after stripping and
            lowercasing, which is the same rule `judge/movies.csv` used.

        The second set matters because the judge adds your ten movies to its list, and
        `agreement.py` compares exactly what the two files share: a tag you never scored is
        dropped without a number. Print how many were asked for and how many you wrote.

    == (6) the four rankings ==
        For each of the ten movies in your "My ten movies" slot, four rankings of the same tags,
        printed one after another and never in one table:

            the counts: the ten most-used tags, by how many times each was applied;
            your own order, from the `WRITEUP.md` slot you filled before seeing any data;
            the judge's order, from `judge/ratings_movies.csv`;
            your `score()`'s order.

        Print each list under its own heading, best first. `results_viewer.py` builds the same
        four lists as a page you can read. Which tag is the artifact, and what the
        disagreements mean, is your paragraph in `WRITEUP.md`.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import re

from load_data import REPO, load_all

MY_MOVIE = 1258   # The Shining (1980), the student's step 1 movie
MIN_USES = 10     # the student's cutoff: tags applied fewer times than this, in total, score 0
JUDGE = REPO / "judge"


def tag_key(tag):
    """The student's rule for what counts as one tag: case, spaces at either end, spaces
    inside, and punctuation are all format, so all of them are dropped. Only letters and
    digits are left."""
    return re.sub(r"[\W_]+", "", tag.lower())


def score(tags_df, ratings_df, movies_df):
    """The student's score: times the tag was applied to this movie, divided by times it was
    applied to any movie, for tags applied at least MIN_USES times in total; 0 otherwise.
    Tags are compared by tag_key()."""
    keyed = tags_df.assign(key=tags_df["tag"].map(tag_key))
    keyed = keyed[keyed["key"] != ""]
    here = keyed.groupby(["movieId", "key"]).size().rename("here").reset_index()
    total = keyed.groupby("key").size().rename("total")
    out = here.join(total, on="key")
    out["score"] = (out["here"] / out["total"]).where(out["total"] >= MIN_USES, 0.0)
    return out.rename(columns={"key": "tag"})[["movieId", "tag", "score"]]


def my_ten():
    """movieIds in the "My ten movies" slot of WRITEUP.md, read the way judge/judge.py reads it."""
    slot = (REPO / "WRITEUP.md").read_text(encoding="utf-8").split("**My ten movies")[-1]
    return [int(n) for n in re.findall(r"^\s*(\d+)", slot.split("\n**")[0], re.M)]


def part2_tags(ratings, tags, movies, links):
    print("== (1) the obvious answer ==")
    title = movies.set_index("movieId").loc[MY_MOVIE, "title"]
    mine = tags[tags.movieId == MY_MOVIE]
    print(f"{title}: {(ratings.movieId == MY_MOVIE).sum():,} ratings, "
          f"{len(mine):,} tag applications, {mine.tag.nunique():,} distinct raw tag strings")
    print("Raw tag strings, exactly as typed: `Cult classic` and `cult classic` are two rows here.")
    counts = mine.groupby("tag").size().rename("applications").reset_index()
    counts = counts.sort_values(["applications", "tag"], ascending=[False, True])
    print(counts.to_string(index=False))

    print("== (2) up close ==")
    my_ratings = ratings[ratings.movieId == MY_MOVIE]
    when_figure(my_ratings, mine, title)

    print("-- who added each tag --")
    print("The movie's 10 heaviest taggers: their tag applications on it, the share of its")
    print(f"{len(mine):,} applications that is, and how many distinct raw tag strings they used.")
    who = mine.groupby("userId").agg(applications=("tag", "size"), distinct_tags=("tag", "nunique"))
    who["share"] = (who.applications / len(mine)).map("{:.1%}".format)
    who = who.sort_values(["applications", "distinct_tags"], ascending=False)
    print(f"{len(who):,} distinct users tagged it.")
    print(who.head(10)[["applications", "share", "distinct_tags"]].to_string())

    print("-- how the taggers rated it --")
    print("For each of the 10 most-applied raw tag strings: how many users applied it, how many of")
    print("them rated the movie, their mean rating, and the mean rating of every other rater.")
    stars = my_ratings.set_index("userId")["rating"]
    rows = []
    for tag in counts.tag.head(10):
        users = set(mine.loc[mine.tag == tag, "userId"])
        rated = stars[stars.index.isin(users)]
        rest = stars[~stars.index.isin(users)]
        rows.append({"tag": tag, "users": len(users), "users_who_rated": len(rated),
                     "their_mean": round(rated.mean(), 2), "everyone_else_mean": round(rest.mean(), 2),
                     "everyone_else_n": len(rest)})
    print(pd.DataFrame(rows).to_string(index=False))

    print("== (3) my definition ==")
    scored = score(tags, ratings, movies)
    print(f"{len(scored):,} movie-tag rows over {scored.movieId.nunique():,} movies; "
          f"{(scored.score > 0).sum():,} of them score above 0")
    print(f"top 15 for {title} (tags shown as their merged key):")
    top = scored[scored.movieId == MY_MOVIE].sort_values(["score", "tag"], ascending=[False, True]).head(15)
    print(top[["tag", "score"]].to_string(index=False, float_format="{:.4f}".format))

    print("== (4) cleaning ==")
    keys = tags["tag"].map(tag_key)
    print(f"raw tag strings in: {tags.tag.nunique():,}; distinct tags out: {keys[keys != ''].nunique():,}")
    dropped = (keys == "").sum()
    print(f"tag applications whose text is only spaces or punctuation, dropped: {dropped:,}")
    spellings = tags.assign(key=keys).groupby(["key", "tag"]).size().rename("n").reset_index()
    spellings = spellings[spellings.key != ""].sort_values(["key", "n"], ascending=[True, False])
    groups = spellings.groupby("key").agg(spellings=("tag", "size"), applications=("n", "sum"),
                                          most_common=("tag", "first"), most_common_n=("n", "first"))
    groups["absorbed"] = groups.applications - groups.most_common_n
    print("the five mergers that absorbed the most applications into their most common spelling:")
    for key, g in groups.sort_values("absorbed", ascending=False).head(5).iterrows():
        forms = spellings[spellings.key == key]
        print(f"  {key!r}: {g.spellings} spellings, {g.applications:,} applications, "
              f"{g.absorbed:,} not in the most common spelling")
        print("    " + ", ".join(f"{t!r} {n:,}" for t, n in zip(forms.tag.head(6), forms.n.head(6)))
              + (" ..." if len(forms) > 6 else ""))

    print("== (5) scores.csv ==")
    asked = pd.read_csv(JUDGE / "movies.csv", keep_default_na=False)
    asked = asked.assign(tag=asked["tags"].str.split("|")).explode("tag")[["id", "tag"]]
    asked = asked.rename(columns={"id": "movieId"})
    ten = my_ten()
    words = {t.strip() for t in (JUDGE / "vocabulary.txt").read_text().splitlines() if t.strip()}
    stripped = tags.assign(tag=tags["tag"].str.strip().str.lower())
    extra = stripped[stripped.movieId.isin(ten) & stripped.tag.isin(words)][["movieId", "tag"]].drop_duplicates()
    asked = pd.concat([asked, extra]).drop_duplicates()
    asked["key"] = asked["tag"].map(tag_key)
    out = asked.merge(scored.rename(columns={"tag": "key"}), on=["movieId", "key"], how="left")
    missing = out.score.isna().sum()
    out = out.dropna(subset=["score"])[["movieId", "tag", "score"]].sort_values(["movieId", "tag"])
    out.to_csv(REPO / "scores.csv", index=False)
    print(f"movies from the \"My ten movies\" slot: {len(ten)}")
    print(f"movie-tag pairs asked for: {len(asked):,}; written to scores.csv: {len(out):,}; "
          f"with no score: {missing:,}")

    print("== (6) the four rankings ==")


def per_month(df):
    """Rows per calendar month, from unix-second timestamps."""
    month = pd.to_datetime(df["timestamp"], unit="s").dt.to_period("M")
    return month.value_counts().sort_index()


def when_figure(my_ratings, my_tags, title):
    """figures/part2_when.png: ratings per month above, tag applications per month below."""
    r, t = per_month(my_ratings), per_month(my_tags)
    months = pd.period_range(min(r.index.min(), t.index.min()), max(r.index.max(), t.index.max()), freq="M")
    r, t = r.reindex(months, fill_value=0), t.reindex(months, fill_value=0)
    x = months.to_timestamp()

    print("ratings and tag applications per year:")
    yearly = pd.DataFrame({"ratings": r.groupby(months.year).sum(), "tag applications": t.groupby(months.year).sum()})
    yearly.index.name = "year"
    print(yearly.to_string())

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    for ax, series, color, label in [(top, r, "#2a78d6", "ratings per month"),
                                     (bottom, t, "#eb6834", "tag applications per month")]:
        ax.plot(x, series.values, color=color, linewidth=1.5)
        ax.set_ylabel(label)
        ax.grid(axis="y", color="#e5e5e2", linewidth=0.8)
        ax.spines[["top", "right"]].set_visible(False)
    bottom.set_xlabel("month")
    fig.suptitle(f"When did the ratings and the tags on {title} arrive?")
    fig.tight_layout()
    out = REPO / "figures" / "part2_when.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    ratings, tags, movies, links = load_all()
    part2_tags(ratings, tags, movies, links)
