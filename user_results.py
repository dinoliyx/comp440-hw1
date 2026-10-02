"""User viewer, Part 3.

Builds one self-contained HTML page about a person: every movie they rated with their stars,
and the five most-used tags on each of those movies. Tags are counted by the student's Part 2
rule, `tag_key()`, so `Comedy` and `comedy` are one tag.

    uv run python user_results.py            # writes user_results.html
    uv run python user_results.py --text     # the same content as plain text

The movie table covers the student, userId 999999, read from the "My 20 ratings" slot. Below
it, for every person in judge/users.csv: their description, and each tag the judge rated with
its score(user, tag) and the judge's rating, highest score first.
"""

import argparse
import html
from pathlib import Path

import pandas as pd

from load_data import load_movies, load_ratings, load_tags
from part2_tags import tag_key
from part3_users import ME, add_me, read_my_ratings, score

REPO = Path(__file__).resolve().parent

USERS = [ME]     # who the page covers
TAGS_SHOWN = 5   # how many tags to show per movie, most-used first

CSS = """body { font-family: Helvetica, Arial, sans-serif; margin: 20px; }
table { border-collapse: collapse; margin-bottom: 12px; }
th, td { border: 1px solid #999999; padding: 4px 8px; text-align: left; vertical-align: top; }
ul { margin: 0; padding-left: 18px; }"""


def build(users=USERS):
    """One dict per user: their rated movies, stars and each movie's top tags."""
    ratings = add_me(load_ratings(), read_my_ratings()[0])
    tags = load_tags()
    titles = load_movies().set_index("movieId")["title"]
    keyed = tags.assign(tag=tags["tag"].map(tag_key))
    keyed = keyed[keyed["tag"] != ""]
    counts = keyed.groupby(["movieId", "tag"]).size().rename("n").reset_index()
    # Most-used first; ties broken alphabetically so the five are reproducible.
    counts = counts.sort_values(["movieId", "n", "tag"], ascending=[True, False, True])
    top = counts.groupby("movieId").head(TAGS_SHOWN)
    top = top.groupby("movieId").apply(lambda g: list(zip(g["tag"], g["n"])), include_groups=False)

    out = []
    for user in users:
        rated = ratings[ratings["userId"] == user]
        # Highest stars first, then title, so the page reads from favourite down.
        rated = rated.assign(title=rated["movieId"].map(titles))
        rated = rated.sort_values(["rating", "title"], ascending=[False, True])
        rows = [(row.title, row.rating, top.get(row.movieId, [])) for row in rated.itertuples()]
        out.append({"user": user, "rows": rows})
    return out, ratings, tags, load_movies()


def judged(ratings, tags, movies):
    """One dict per person in judge/users.csv: description, and (tag, score, judge rating) rows."""
    people = pd.read_csv(REPO / "judge" / "users.csv", keep_default_na=False)
    verdicts = pd.read_csv(REPO / "judge" / "ratings_users.csv", keep_default_na=False)
    scored = score(ratings, tags, movies, users=list(people["id"]))
    scored = scored.set_index(["userId", "tag"])["score"]
    out = []
    for person in people.itertuples():
        rows = []
        for v in verdicts[verdicts["id"] == person.id].itertuples():
            rows.append((v.tag, scored.get((person.id, tag_key(v.tag)), float("nan")), int(v.rating)))
        rows.sort(key=lambda r: (-r[1], r[0]))
        out.append({"user": person.id, "description": person.description, "rows": rows})
    return out


def tags_cell(pairs):
    return ", ".join("%s (%d)" % (t, n) for t, n in pairs) or "no tags"


def tags_list_html(pairs):
    if not pairs:
        return "no tags"
    return "<ul>%s</ul>" % "".join("<li>%s (%d)</li>" % (html.escape(t), n) for t, n in pairs)


def render(people, judged_people):
    body = ["<h1>User viewer</h1>",
            "<p>Each movie the person rated, their stars, and the %d most-used tags on it "
            "(merged by the Part 2 rule; count in brackets).</p>" % TAGS_SHOWN]
    for p in people:
        body.append("<h2>userId %d: %d ratings</h2>" % (p["user"], len(p["rows"])))
        head = "<tr><th>Movie</th><th>Stars</th><th>Top %d tags</th></tr>" % TAGS_SHOWN
        rows = "".join("<tr><td>%s</td><td>%.1f</td><td>%s</td></tr>"
                       % (html.escape(t), r, tags_list_html(tg)) for t, r, tg in p["rows"])
        body.append("<table>%s%s</table>" % (head, rows))
    body.append("<h1>The judge on people</h1>")
    body.append("<p>Every person in judge/users.csv: the tags the judge rated, highest "
                "score(user, tag) first, with the judge's rating from 1 to 5.</p>")
    for p in judged_people:
        body.append("<h2>userId %d</h2><p>%s</p>" % (p["user"], html.escape(p["description"])))
        head = "<tr><th>Tag</th><th>score(user, tag)</th><th>Judge rating</th></tr>"
        rows = "".join("<tr><td>%s</td><td>%.4f</td><td>%d</td></tr>" % (html.escape(t), sc, j)
                       for t, sc, j in p["rows"])
        body.append("<table>%s%s</table>" % (head, rows))
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            "<title>User viewer</title>\n<style>\n%s\n</style>\n</head>\n<body>\n%s\n"
            "</body>\n</html>\n" % (CSS, "\n".join(body)))


def render_text(people, judged_people):
    out = []
    for p in people:
        out.append("userId %d: %d ratings" % (p["user"], len(p["rows"])))
        for t, r, tg in p["rows"]:
            out.append("  %.1f  %s" % (r, t))
            out += ["         - %s (%d)" % pair for pair in tg] or ["         - no tags"]
    out.append("\nThe judge on people: tag, score(user, tag), judge rating")
    for p in judged_people:
        out.append("userId %d: %s" % (p["user"], p["description"]))
        out += ["  %-28s %8.4f  %d" % row for row in p["rows"]]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="A page about a person's ratings and tags.")
    parser.add_argument("--out", default=str(REPO / "user_results.html"))
    parser.add_argument("--text", action="store_true")
    args = parser.parse_args()
    people, ratings, tags, movies = build()
    judged_people = judged(ratings, tags, movies)
    if args.text:
        print(render_text(people, judged_people))
        return
    Path(args.out).write_text(render(people, judged_people), encoding="utf-8")
    print("wrote %s" % args.out)


if __name__ == "__main__":
    main()
