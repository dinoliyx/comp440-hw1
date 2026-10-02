# HW1 writeup

**Name:** Dino Li
**Date:** 2026-09-28

Every placeholder below gets your answer, told to Claude or typed in here yourself. Every number
you give comes from a script in this repo; say which one. Claude may format tables and figures
here; the words are yours.

## Part 0. Predictions

Give these to Claude before any analysis runs. One sentence each, plus one sentence on why you
think so.

**(1) A movie you know well, and what its three most-used tags will be:** Sing, I think the three most-used tags will be family, music, animated.

**(1) Why you think so:** Because it is an animated movie, and it's a family-oriented musical movie.

**(2) Out of every 100 people who rated movies here, how many ever added a tag?** 46

**(2) Why you think so:** I feel like it's common to tag when rating because the features are kind of designed to be integrated now.

**(3) Can one person's tags take over a movie's tag list? Yes or no:** No

**(3) Why you think so:** If there's a lot of people tagging it, I think the tag that appears more would take over the list.

## Part 1. Whose data is this?

Code: `part1_data.py`.

**My rule for cutting 32 million ratings to 5 million** (written before reading `data/make_compact.py`)**:** Randomly. I would eliminate every discrete value of ratings at a same proportion.

**One rule I considered and rejected, and why:** I considered to eliminate ratings randomly but then I realize that is maybe unfair to the users because I want to keep the cutting down fair by saving the same ratio of ratings.

**One interesting thing from `data/README.md`:** The way they filter users to the subset is interesting to me because I didn't really think about it when I was making my own rule. Their method of only keeping users who has tagged at least 20 movies is useful because we can gather more information on learning their tagging preference. They also subset a sample of movies first and keeps the user who has at least 20 ratings on those movies.

**How the script's rule differs from mine, and what each keeps that the other drops:** My method only thinks about kicking out the ratings but their rule first filter movies then users who has eligible amount of ratings and finally the ratings. My method is more computational easy but their method is more rigorous and keeps more information from the original data set. My method drops users who might rated a lot of movies by the random selection and keeps some of the users who only rated one movie. Their method dropped users who doesn't have 20 ratings but mine will keep them.

**First check. Which of Claude's numbers, the different route you took, and whether it matched** (one good target: 6 tags are the literal text `NA`, which pandas drops unless told not to)**:** 85.8. I would sort them as the amount of unique tags per user, then rank it from high to low. Numerator is the total amount of tags those 1402 users and divided by the total amount of tags. It doesn't match.

**Second check. Which of Claude's numbers, the different route you took, and whether it matched:** I tried a different module to check for the "NA" tag and it matched with claude's method.

## Part 2. What tags best describe a movie?

Code: `part2_tags.py`.

**My movie, and why I picked it:** The Shining (1980), because it's a classic I think and I'm interested to see how people tag and rate it.

**Its most misleading tag in the count-ordered list, and why it misleads:** Nudity, because I can't recall any plots with nudity in the movie and that's not what the movie trying to convey. Also I might've watched not the original version.

**What I learned about how MovieLens collects ratings and tags, from rating and tagging my movie myself (about 100 words):** XXXX

### Up close

One sentence on the figure written before you saw it and one after. The two tables are where the
details below come from. Say which script made them.

**The figure, when the tags and the ratings arrived. What I expected:** Mostly early since it's an old movie.
**The figure, what it shows:** I'm surprised that no one tag this movie until 2006 but the figure shows the amount of ratings and tags every year.

**Two interesting details I learned up close that the counts did not show:** 1. People who tagged Stanley Kubrick rated, on average, higher than the ones who tagged Stephen King. I would thought the opposite. 2. People who tagged also just rate the movie higher in general compare to ones who didn't tagged.

**Anything up close that contradicted something I had already written down. Which one, what the data showed, and what you now think. Or "nothing yet":** Yeah my prediction for the rank of the tag for Shining was that cult film would probably be on top because its such a classic cult movie but it actually sit at the bottom of the list.

### My definition

**My `score(movie, tag)`** (one or two sentences, precise enough that a classmate could code it)**:** score(movie, tag) is the number of times the tag was applied to this movie divided by the number of times it was applied to any movie, computed only for tags applied at least 10 times across all movies. Tags applied fewer than 10 times in total get a score of 0.

**One definition I considered and rejected, and why:** One definition I had was that only counting the frequency a tag applied to the movie because that would imply how much people resonate with the same tag but I think the score should be more rigorous than that, it should have some limit to filter out for some tags that's random.

**Which tags I merged as the same tag, which I kept apart, and why:** I kept the tags that has the same word but some alternations as the same tag, for example if there's lower/capitalized case or inner spaces because to me they are conveying the same information just in different format. I just keep every word apart because I want them to have different information and weight on the movie so it's good to have a diverse range of tag.

**Why my definition, in about 150 words. Name one thing it gains and one thing it loses:**

XXXX

### The judge

The two slots below are read by scripts, so write them as bare lines: one item to a line, the
movieId first, no bullets and no numbering. A movie line looks like `296, Pulp Fiction (1994)`.
An order line looks like `296: nonlinear, hit men, dark comedy, ...`, the tags best first.

**My ten movies:**

1258, Shining, The (1980)
59784, Kung Fu Panda (2008)
4144, In the Mood For Love (Fa yeung nin wa) (2000)
152081, Zootopia (2016)
168492, Call Me by Your Name (2017)
122912, Avengers: Infinity War - Part I (2018)
95510, Amazing Spider-Man, The (2012)
1721, Titanic (1997)
54001, Harry Potter and the Order of the Phoenix (2007)
2459, Texas Chainsaw Massacre, The (1974)

**My own order of the ten most-used tags, written before looking at any data: my movie from step 1, then my nine others from step 4:**

1258: cult film, psychological, Stephen King, suspense, dreamlike, visually appealing, atmospheric, Stanley Kubrick, Jack Nicholson, disturbing
59784: Kung Fu, funny, animation, animals, anti-hero, pixar, Jack Black, underdog, comedy, martial arts
4144: Wong Kar Wai, atmospheric, elegant, visually stunning, moody, melancholy, melancholic, stylized, music, loneliness
152081: friendship, funny, tolerance, cute, social commentary, visually stunning, xenophobia, racism, attention to detail, creative
168492: gay, gay romance, romance, Timothée Chalamet, lgbt, atmospheric, sensual, coming of age, Armie Hammer, italy
122912: superhero, Marvel, MCU, comic book, Robert Downey Jr., Thanos, time travel, emotional, Guardians of the Galaxy, cliffhanger
95510: action, Spider-Man, Marvel, superhero, Andrew Garfield, Emma Stone, comic book, nerds kicking butt, Martin Sheen, special effects
1721: romance, drama, historical, disaster, Leonardo DiCaprio, true story, love story, Kate Winslet, atmospheric, bittersweet
54001: harry potter, fantasy, magic, wizards, based on a book, Gary Oldman, magic school, fantasy world, Emma Watson, Daniel Radcliffe
2459: horror, dark, atmospheric, grim, tense, disturbing, gruesome, slasher, grindhouse, cannibalism

**One criterion I considered for the judge and rejected, and why** (the one I used is in `judge/criterion.md`)**:** XXXX

**Agreement. The number `agreement.py` gives for your `score()`, for popularity and for your own order, and which of the three came closest to the judge:** XXXX

**How the judge skill is built: the files it is made of and what each one does (about 150 words):**

XXXX

**What happens when I run `/judge`, from the first check to the CSV (about 150 words):**

XXXX

**Why a skill: what a skill like this gives you that a script or a prompt alone does not, and where you would use one next (about 100 words):**

XXXX

### The viewer and the disagreements

**One thing `movie_results.html` showed me that was useful, and one thing about it that got in my way:** XXXX

Then three improvements. For each: what the page would not let you see, what you had Claude
change, and what the changed page shows that the first draft did not.

**Improvement 1:** XXXX

**Improvement 2:** XXXX

**Improvement 3:** XXXX

Then the three disagreements. A disagreement is a movie and a tag where your `score()` and the
judge are furthest apart. For each: the movie and the tag, where your `score()` put it and where
the judge put it, and what you think accounts for the gap.

**Disagreement 1:** XXXX

**Disagreement 2:** XXXX

**Disagreement 3:** XXXX

**One other high-level pattern in the results, and what you think is behind it:** XXXX

## Predictions revisited

**Which of my three predictions were wrong, and what I make of each miss:** XXXX

## Part 3. What tags best describe a user?

Code: `part3_users.py`.

The slot below is read by a script, so write it as bare lines: one rating to a line, no bullets
and no numbering, the movieId first and the rating last, as in `296, Pulp Fiction (1994), 4.5`.

**My 20 ratings:**

XXXX

**My `score(user, tag)`, in a sentence, and why I started there (about 100 words):**

XXXX

**What my score says about me: my top ten tags, and whether they describe my taste (about 100 words):**

XXXX

**What my user viewer shows and why I chose that (about 100 words):**

XXXX

**What I put in the description column for a person, and why (about 150 words):**

XXXX

**My criterion for people: what it asks the judge to do that the movie criterion did not (about 60 words):**

XXXX

**The user-tag pairs I chose to judge, how many, and why those (about 100 words):**

XXXX

**Improvement 1: what I changed in the scoring function, what the judge and the viewer showed before and after (about 150 words):**

XXXX

**Improvement 2: the same (about 150 words):**

XXXX

## Part 4. Working with Claude

Give these to Claude the way you gave it the rest. Graded on the catch and the candor, not on
making Claude look good or bad.

**A moment where Claude was wrong or overconfident, how you caught it, and where it
happened. Name the part and the step, so the moment can be found:** XXXX

**One call where you overrode Claude, and why:** XXXX

**What you would hand to Claude sooner next time:** XXXX

**Did Claude name the misleading tag in Part 2 step 1 before you did? What happened:** XXXX

**The figure. Would asking Claude "what does this show?" have produced your sentence, and what
would have been missing from it:** XXXX

**Hours spent:** XXXX

**Anyone who helped you, or "no one":** XXXX
