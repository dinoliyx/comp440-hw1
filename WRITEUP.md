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

**What I learned about how MovieLens collects ratings and tags, from rating and tagging my movie myself (about 100 words):** They show you a prediction of your rating and shows wht the average ratings are for the movie. I also like that they show all the counts for the tags for the movie because you can just hit the plus button to add, its like checking a list.

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

I choose this definition because I want it to compare the frequency of tags applied to one movie with all movies. I think this way we can figure out how this tag fits this specific movie compared to other movies. And the 10 tags cutoff avoid the problem of if there's a random tag that only applied once then it won't have the highest score just because of that. I gain specificity which tells me if tags are concentrated in one movie or not. For example, Stephen King for the Shining would score high because its one of his most successful movie. However this ratio can overlook accurate tags that are also popular. For example, horror is a perfect tag for the Shining but since this tag has been applied too many times on other movies too so it loses the weight on the Shining.

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

**One criterion I considered for the judge and rejected, and why** (the one I used is in `judge/criterion.md`)**:** I considered having the criterion that a tag that best describe a movie should be the one that most people would agree to. But I realize that would just be the rank of counts of tags which is already existing in the file.

**Agreement. The number `agreement.py` gives for your `score()`, for popularity and for your own order, and which of the three came closest to the judge:** score() 2.45, popularity 2.85, your own order 3.50, all out of 5. My own rule came closest to the judge but also it wan't fair because my own rule only rated 10 movies and the other methods looks at all movies, so it was an easier task for me.

**How the judge skill is built: the files it is made of and what each one does (about 150 words):**

Skill.md reads judge/readme.md and do what it says. system.md tells claude to rate how well the tags are applied to the movies. criterion is the rule I decided on what a tag best describes a movie. Claude will read it and judge the tags base on my rule. judge.py evaluates a set of 110 movies against my criterion and generate ratings and retry missing tags before saving the final results to ratings_movies.csv. Readme provides instructions for me to understand how the judge operates. movies.csv is the subset of movies with their id and descriptions and tags. vocabulary is the subset that holds the tags the judge is allowed to rate.

**What happens when I run `/judge`, from the first check to the CSV (about 150 words):**

when you run judge, the process begins with pre-execution checks that verifies the items files exist and validate the rule or criterion I chose. Once that's done, it reads the elements of the items file alongside my ten movies and outputs a status message indicating which rule was loaded and what information it is about to request. Next, it moves into execution by launching an individual claude session for each movie. It processes and reads all the returned answers, automatically reprompting any sessions that returned incomplete or short response to make sure we have the full data. Lastly, it writes the collected results to the csv output and print out a summary.

**Why a skill: what a skill like this gives you that a script or a prompt alone does not, and where you would use one next (about 100 words):**

A skill gives you flexibility that you don't need to remember complex terminal commands, or file paths. And I also don't need to evaluate the movies one by one or organize the output myself. It saves a lot of labors from me doing repeating tasks. I would like to use skill like it in my project when I know what I want to do with each item but have to do it one by one. It's a great tool to avoid a lot of manual labors.

### The viewer and the disagreements

**One thing `movie_results.html` showed me that was useful, and one thing about it that got in my way:** Useful, I see how the list of tags are compared across different methods. Got in my way, the page shows all the tags on the movie, making it such a long page.

Then three improvements. For each: what the page would not let you see, what you had Claude
change, and what the changed page shows that the first draft did not.

**Improvement 1:** The page was hard to read because of the long list of all tags on movies, I change it to a table with tags and counts and that makes the page more neat.

**Improvement 2:** The page was showing the list from the four methods one by one, which makes it hard to look at to compare so I ask Claude to put them in the same row. Now they are easy to look at and compare.

**Improvement 3:** It was hard for me to notice the best tag from the list so I ask claude to highlight the tag that remain in top 5 across four list. Now you can easily spot the tag that is in top 5 from every list.

Then the three disagreements. A disagreement is a movie and a tag where your `score()` and the
judge are furthest apart. For each: the movie and the tag, where your `score()` put it and where
the judge put it, and what you think accounts for the gap.

**Disagreement 1:** For the shining, the judge put the tag stanley kubrick it 38 and score() put it 2. stanley kubrick is the filmmaker of the shining, it doesn't really capture any information about the movie but form my definition, score() yeild hihgher score for tags that applied to the movie that's unique. I think this gives stanley kubrick a super high score but it's not the best tag for the shining.

**Disagreement 2:** For KungFu Panda, the score() put the tag action 15th rank and the judge put it the 1st place. The gap is because score() adds penalty to the tag that's popular for example action is a very common tag so although it suits kungfu panda very well, score() give it a lower score compare to other tags.

**Disagreement 3:** For In the Mood for Love, the judge put the tag cinematography the second in the rank whereas score() put it teh 24th. score() ranks "cinematography" low because it's applied to so many movies that this film's share of its uses is small, while the judge ranks it high because the film is so widely known for its cinematography.

**One other high-level pattern in the results, and what you think is behind it:** oh, I saw that tags that are highlighted are at most 2 in every movie, across the four list. I think it's because the order are determined very differently.

## Predictions revisited

**Which of my three predictions were wrong, and what I make of each miss:** Prediction 2: people actually tag movies way more than I thought. Prediction 3: I still dont think one person's tags can take over a movie's list because the user tagged the most is still on ly 35, which is not a lot compare to the total amount of tags a movie could have form the data set. I guess one user's tags can make a difference if they have 99% of the tags for a movie, but that's still some extreme case in my consideration. Prediction 1: I'm pretty much right about this one except fun but funny was going to be my fourth tag (a later thought).

## Part 3. What tags best describe a user?

Code: `part3_users.py`.

The slot below is read by a script, so write it as bare lines: one rating to a line, no bullets
and no numbering, the movieId first and the rating last, as in `296, Pulp Fiction (1994), 4.5`.

**My 20 ratings:**

446, Farewell My Concubine (Ba wang bie ji) (1993), 5.0
1721, Titanic (1997), 4.0
152081, Zootopia (2016), 4.0
167036, Sing (2016), 5.0
164909, La La Land (2016), 4.5
2959, Fight Club (1999), 4.0
2571, Matrix, The (1999), 4.5
5618, Spirited Away (Sen to Chihiro no kamikakushi) (2001), 5.0
593, Silence of the Lambs, The (1991), 4.5
202439, Parasite (2019), 3.5
177765, Coco (2017), 5.0
95510, Amazing Spider-Man, The (2012), 5.0
254726, Dune (2021), 3.5
1200, Aliens (1986), 4.0
1203, 12 Angry Men (1957), 5.0
47099, Pursuit of Happyness, The (2006), 4.5
134853, Inside Out (2015), 4.0
50872, Ratatouille (2007), 4.0
1387, Jaws (1975), 3.5
4447, Legally Blonde (2001), 5.0

**My `score(user, tag)`, in a sentence, and why I started there (about 100 words):**

My score is calculated by taking my rating distance per movie relative to average user ratings, weighing it by each tag's score from part 2 and summing those weighted distances across all my rated movies. I started with this rule because it directly isolates my unique taste over general consensus while leveraging our existing tag specificity scores to give more weight on the descriptive ones.

**What my score says about me: my top ten tags, and whether they describe my taste (about 100 words):**

No they don't, I don't understand some of the tags here like diadelosmuertos and doortothedifferentworld. I feel like they are not very related to the movies I rated. Although I can see how pink and lawschool comes from legally blonde which I rated 5.

My top ten, from `uv run python part3_users.py`, first version of `score(user, tag)`:

| tag | score |
| --- | --- |
| pink | 1.2562 |
| ordinary | 1.0279 |
| wasntfunny | 1.0279 |
| diadelosmuertos | 0.9398 |
| gaystereotypes | 0.8206 |
| doortothedifferentworld | 0.7885 |
| cinemascope | 0.7686 |
| lawschool | 0.7537 |
| notasgoodastheoriginal | 0.7248 |
| spanglish | 0.7196 |

**What my user viewer shows and why I chose that (about 100 words):**

I showed the user the 20 movies they rated with the top 5 tags that's applied to them on the side in a table. Because I think it gives the user an intuitive context for how their ratings connected to specific themes.

**What I put in the description column for a person, and why (about 150 words):**

their group like which selection group they belong to and how closely their movie ratings align with mine. And their favorite high-rated movies along with the general genre they watch the most. It gives the judge context on where the user sits in the 10-person sample and how closely are they matching with my taste. It also provides concrete titles so the judge can evaluate whether chosen tags match the core themes or not.

**My criterion for people: what it asks the judge to do that the movie criterion did not (about 60 words):**

The movie criterion asks the judge to evaluate how well tags describe a single movie's overall plot and style. And the people criterion asks the judge to evaluate how well tags capture a person's broader taste profile

**The user-tag pairs I chose to judge, how many, and why those (about 100 words):**

It should include me plus a sample of other users from the dataset. I picked other users by selecting a diverse mix of rating, some with high rating overlap with me, some with contrasting tastes, and a few randomly sampled users. So the judge has a good baseline to evaluate taste profiles across different type of users. the number is 10 tags per user. Include each user's top 10 highest-scoring tags after filtering through vocab.txt so every tag is evaluated by the judge is a valid and closely reflective.

**Improvement 1: what I changed in the scoring function, what the judge and the viewer showed before and after (about 150 words):**

the judge gave low scores to tags like miyazaki and anthony hopkins because those creators don't appear in the top 3 fav movies. since the judge only sees the text descriptions, any tag that doesn't match those 3 movies gets marked down, even if the tag score was high. It now only receives tags tied directly to those 3 movies, resulting in relevant tags and higher judge ratings

**Improvement 2: the same (about 150 words):**

Change score to weight candidate tags by multiplying each movie's score by the user's explicit movie ratings and distance and weight, keeping only tags from their top 3 movies. it makes the rank list much cleaner and easier to read. Irrelevant creator tags are gone. Judge's ratings also improved because it now give top scores to the most defining elements of your profile instead of 1. The highest scoring tags also align with the judge's top rank

## Part 4. Working with Claude

Give these to Claude the way you gave it the rest. Graded on the catch and the candor, not on
making Claude look good or bad.

**A moment where Claude was wrong or overconfident, how you caught it, and where it
happened. Name the part and the step, so the moment can be found:** when I was working with the viewer claude mistaken my command of highlighting and making the table, I caught it by checking the tables myself because it's visually reflective. part 2 viewer when asking for improvement

**One call where you overrode Claude, and why:** One moment that I overrode Claude is when it change the order of answering to the slot in part 2 when I'm building the viewer, I just found it confusing and did it in my own order.

**What you would hand to Claude sooner next time:** when I'm trying to come up with the formula for scores of tags that describe a user. I should've ask claude to print out the conditions and elements I have and connect them with visual output so I can see what's there to manipulate.

**Did Claude name the misleading tag in Part 2 step 1 before you did? What happened:** well I dont think claude name it before I did.

**The figure. Would asking Claude "what does this show?" have produced your sentence, and what
would have been missing from it:** I think that will be very helpful to summarize the figures for me

**Hours spent:** 6~8 hours

**Anyone who helped you, or "no one":** no one
