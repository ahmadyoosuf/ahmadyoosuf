"""77 MINUTES: the film as data. Single source of truth for build.py.

Wording is the user's fixed SCRIPT, character for character, except two
deliberate typographic changes (DECISIONS D023): narration apostrophes are set as
’ and the brother's quote marks as ‘ ’. Discord quotes keep their straight
apostrophes.

A card has one or more parts. Each part is revealed after the previous one
(sentence by sentence) and they flow into one paragraph unless `block` is set,
in which case the part starts on its own line (dates, Tamil, subtitle).

Fields per part:
  text    exact text
  face    fraunces | italic | mono | tamil
  size    px (cards 64, mono 60, title/end 72, subtitle/final 60)
  reveal  ink (soft ink, word wave) | type (character strikes) | words (word by word) | cut
  accent  list of substrings set in #C8902E (night/black grounds only, D018)
  pause   seconds of stillness after this part before the next part starts
  block   start this part on its own line
"""

P = 0.0  # readability alias for "no pause"


def part(text, face="fraunces", size=64, reveal="ink", accent=(), pause=P, block=False, **kw):
    d = dict(text=text, face=face, size=size, reveal=reveal, accent=list(accent), pause=pause, block=block)
    d.update(kw)
    return d


def card(cid, *parts, exit="dissolve", extra=None, air=None, note="", script=None, **kw):
    d = dict(id=cid, parts=list(parts), exit=exit, extra=extra, air=air, note=note, script=script)
    d.update(kw)
    return d


# ---------------------------------------------------------------- section 0
LETTER = "I took 77 minutes for writing this message to you (#hardwork\U0001F605). Period."

OPEN_A = dict(
    id="s0a", name="Cold open (A: two voices)", ground="black", extra=0.15, air=0.3,
    cards=[
        card("s0a-letter",
             part(LETTER, face="mono", size=60, reveal="type", accent=["77 minutes"], schedule="coldopen",
                  caret=True),
             lead=0.17, note="The 2022 letter's last line, typed in under three seconds.",
             script="The letter's last line typed character by character"),
        card("s0a-2022",
             part("In 2022, it took me 77 minutes to write one message to a Harvard professor.",
                  accent=["77 minutes"]),
             script="In 2022, it took me 77 minutes to write one message to a Harvard professor."),
        card("s0a-proud", part("I was proud of that."), exit="cut", extra=0.45, air=0.4,
             script="I was proud of that."),
        card("s0a-title", part("77 MINUTES", face="mono", size=72, reveal="type", cps=14.0, tracking=0.12,
                               heavy=True),
             extra=0.4, air=0.0, script="Title: 77 MINUTES"),
    ],
)

OPEN_B = dict(
    id="s0b", name="Cold open (B: one sitting)", ground="black", extra=0.15, air=0.0,
    cards=[
        card("s0b-letter",
             part(LETTER, face="mono", size=60, reveal="type", accent=["77 minutes"], schedule="coldopen",
                  caret=True),
             exit="cut", air=0.0, return_after=True, lead=0.17,
             script="The letter's last line typed character by character"),
        card("s0b-2022",
             part("In 2022, it took me 77 minutes to write one message to a Harvard professor.",
                  face="mono", size=60, reveal="type", cps=21.0, accent=["77 minutes"], caret=True),
             exit="cut", air=0.0, return_after=True,
             script="In 2022, it took me 77 minutes to write one message to a Harvard professor."),
        card("s0b-proud",
             part("I was proud of that.", face="mono", size=60, reveal="type", cps=9.0, caret=True),
             exit="cut", extra=0.55, air=0.0, return_after=True, script="I was proud of that."),
        card("s0b-title", part("77 MINUTES", face="mono", size=72, reveal="type", cps=4.0, tracking=0.12,
                               heavy=True, caret=True),
             extra=0.4, air=0.0, script="Title: 77 MINUTES"),
    ],
)

# ---------------------------------------------------------------- section 1
LIBRARY = dict(
    id="s1", name="The library", ground="night", extra=0.1, air=0.2, lead=0.6,
    footage="Old book spines on wooden shelves at night, warm lamp (still with 3% drift), 5-6 s per shot",
    cards=[
        card("s1-ahmad",
             part("I’m Ahmad.", pause=0.3),
             part("I’m from Adirampattinam, a small town on the Tamil Nadu coast."),
             script="I'm Ahmad. I'm from Adirampattinam, a small town on the Tamil Nadu coast."),
        card("s1-family",
             part("My family are scholars of Islam.", pause=0.35),
             part("Most of us stop formal school around class ten or twelve."),
             script="My family are scholars of Islam. Most of us stop formal school around class ten or twelve. "
                    "(split 1/2: line exceeds two lines, D026)"),
        card("s1-first", part("I’m the first of us to go to college."), extra=0.45,
             script="I'm the first of us to go to college. (split 2/2)"),
        card("s1-father",
             part("My father studied until the third grade.", pause=0.4),
             part("He owned more than two thousand books."),
             script="My father studied until the third grade. He owned more than two thousand books."),
        card("s1-world",
             part("Between nine and fifteen, before I had a phone, that library was how I left my world."),
             script="Between nine and fifteen, before I had a phone, that library was how I left my world."),
        card("s1-dream", part("It’s also where I got a dream far too big for the boy reading it."),
             script="It's also where I got a dream far too big for the boy reading it."),
        card("s1-reason",
             part("From seventh grade to tenth, I came first in all eighteen exams I wrote.", pause=0.6),
             part("He was the reason."),
             extra=0.6, air=0.0,
             script="From seventh grade to tenth, I came first in all eighteen exams I wrote. He was the reason."),
    ],
)

# ---------------------------------------------------------------- section 2
NINE = dict(
    id="s2", name="Nine months", ground="paper", extra=0.15, air=0.3, lead=0.6,
    footage="Monsoon sky over the coast, no people, no wreckage (still, 2% drift), 7-9 s per shot",
    cards=[
        card("s2-oct",
             part("October 2018.", face="mono", size=60, reveal="type", cps=11.0, block=True, pause=0.35, paper=True),
             part("My maternal grandmother.", block=True),
             script="October 2018. My maternal grandmother."),
        card("s2-gaja",
             part("15 November 2018.", face="mono", size=60, reveal="type", cps=11.0, block=True, pause=0.35,
                  paper=True),
             part("Cyclone Gaja.", block=True),
             script="15 November 2018. Cyclone Gaja. (split 1/2: date line + the sentence exceed two lines, D026)", wind="rise"),
        card("s2-roof", part("The roof of our house landed on the next street."),
             script="The roof of our house landed on the next street.", wind="peak"),
        card("s2-dec",
             part("December 2018.", face="mono", size=60, reveal="type", cps=11.0, block=True, pause=0.35, paper=True),
             part("My paternal grandmother.", block=True, pause=0.45),
             part("Forty-five days after the first."),
             script="December 2018. My paternal grandmother. Forty-five days after the first.", wind="fall"),
        card("s2-july", part("1 July 2019.", face="mono", size=60, reveal="type", cps=7.0, paper=True),
             extra=1.0, air=0.6, script="1 July 2019."),
        card("s2-woke", part("I woke up at five thirty, prayed, and put on my school uniform."),
             script="I woke up at five thirty, prayed, and put on my school uniform."),
        card("s2-knock", part("Around seven, my brother knocked on my door."),
             script="Around seven, my brother knocked on my door.", knock=True),
        card("s2-over", part("‘Everything is over. Change your dress.’", face="italic"), extra=0.8,
             script="'Everything is over. Change your dress.'"),
        card("s2-fortythree", part("My father was forty-three."), exit="cut", extra=1.0, air=0.0,
             script="My father was forty-three.", black_after=2.0),
        card("s2-school",
             part("In my last year of school I spent two of the final four months sick in bed.", pause=0.6),
             part("I finished with seventy-five percent."),
             extra=0.6, air=0.0,
             script="In my last year of school I spent two of the final four months sick in bed. "
                    "I finished with seventy-five percent."),
    ],
)

# ---------------------------------------------------------------- section 3
ALONE = dict(
    id="s3", name="Alone", ground="night", extra=0.1, air=0.2, lead=1.0,
    footage="Old laptop keyboard close-up in lamp light, no screen content (still, 3% drift), 5 s per shot",
    cards=[
        card("s3-applied",
             part("So I applied to Harvard, MIT, Princeton and Yale by myself.", pause=0.45),
             part("No counsellor.", pause=0.25),
             part("No SAT.", pause=0.25),
             part("No mentor."),
             script="So I applied to Harvard, MIT, Princeton and Yale by myself. No counsellor. No SAT. No mentor."),
        card("s3-slow",
             part("I'm not a fast writer.", face="italic", pause=0.35),
             part("It took nearly half an hour to write the above statement.", face="italic", accent=["half an hour"]),
             extra=0.35, script="I'm not a fast writer. It took nearly half an hour to write the above statement."),
        card("s3-stranger",
             part("A stranger reviewed my essay once.", pause=0.45),
             part("It was brutal, and it was the most useful thing anyone had told me."),
             script="A stranger reviewed my essay once. It was brutal, and it was the most useful thing anyone had told me."),
        card("s3-again1",
             part("When I asked again:", pause=0.35),
             part("no i'm busy", face="italic"),
             exit="cut", script="When I asked again: no i'm busy"),
        card("s3-again2",
             part("And again:", pause=0.3),
             part("No I'm busy", face="italic"),
             exit="cut", script="And again: No I'm busy"),
        card("s3-ok", part("Ok\U0001F622", face="italic"), extra=0.4, script="Ok😢"),
        card("s3-rejections", part("The rejection letters came."), extra=0.3, script="The rejection letters came."),
        card("s3-hundred",
             part("Later, a hundred companies rejected more than four hundred of my applications."),
             script="Later, a hundred companies rejected more than four hundred of my applications."),
        card("s3-laptop", part("I wrote most of them on a laptop made in 2010."), air=0.0,
             script="I wrote most of them on a laptop made in 2010."),
    ],
)

# ---------------------------------------------------------------- section 4 (accelerates)
WELL_SAID = dict(
    id="s4", name="Well said", ground="night", accelerate=True, extra=(0.25, 0.0), air=(0.3, 0.0), lead=0.3,
    footage="Notebook pages turning fast (2-3 s per shot, shrinking), then none: the gourd is the only visual",
    cards=[
        card("s4-did-well",
             part("The thing I did well was write about the person I was going to become."),
             script="The thing I did well was write about the person I was going to become."),
        card("s4-notes", part("For three years I filled notes with plans, rules and resolutions."),
             script="For three years I filled notes with plans, rules and resolutions."),
        card("s4-journal-1",
             part("27 August 2023", face="mono", size=60, reveal="type", cps=12.0, block=True, pause=0.35),
             part("Well said and well thought is better than well done", face="italic", reveal="words", block=True,
                  accent=["well done"], words_from=0.40, words_to=0.30),
             script="the 27 August 2023 journal line, revealed word by word (split 1/2, D026)"),
        card("s4-journal-2",
             part("according to my intuition which seems ridiculous but does not hinder me from practicing that "
                  "terrible idea.", face="italic", reveal="words", words_from=0.28, words_to=0.16),
             script="(journal line, split 2/2)"),
        card("s4-eighteen",
             part("I wrote that at eighteen.", pause=0.35),
             part("Then I kept doing it."),
             exit="cut", script="I wrote that at eighteen. Then I kept doing it."),
        card("s4-saying", part("There’s an old Tamil saying."), exit="cut", air=0.0,
             script="There's an old Tamil saying."),
        card("s4-gourd",
             part("ஏட்டுச் சுரைக்காய் கறிக்கு உதவாது", face="tamil", size=64, block=True, pause=0.25),
             part("A gourd drawn on paper won’t cook a curry.", face="italic", size=60, block=True),
             ground="paper", gourd=True, exit="cut", extra=0.0, air=0.0, lead=0.45,
             script="ஏட்டுச் சுரைக்காய் கறிக்கு உதவாது / A gourd drawn on paper won't cook a curry."),
        card("s4-notes-gourd", part("Every one of those notes was a gourd on paper."), ground="paper",
             extra=0.5, air=0.0, script="Every one of those notes was a gourd on paper."),
    ],
)

# ---------------------------------------------------------------- section 5 (decelerates)
WELL_DONE = dict(
    id="s5", name="Well done", ground="night", extra=0.3, air=0.4, lead=0.9,
    footage="Captured product footage only: vaakku.org, statement2xl.com, ayyayo.ai (blocked in v1, D011)",
    cards=[
        card("s5-cooking", part("So, slowly, I started cooking.", accent=["cooking"]), extra=0.85,
             script="So, slowly, I started cooking."),
        card("s5-vaakku-url", part("vaakku.org", size=72), capture="vaakku.org", extra=0.2,
             script="(over vaakku.org: domain card stands in for the blocked capture, D013)"),
        card("s5-vaakku", part("A Tamil voice system that called voters, for district election officials."),
             capture="vaakku.org",
             script="A Tamil voice system that called voters, for district election officials."),
        card("s5-s2xl-url", part("statement2xl.com", size=72), capture="statement2xl.com", extra=0.2,
             script="(over statement2xl.com: domain card, D013)"),
        card("s5-s2xl", part("An engine that turns bank statements into spreadsheets."), capture="statement2xl.com",
             script="An engine that turns bank statements into spreadsheets."),
        card("s5-name",
             part("And a name.", pause=0.5),
             part("In Tamil, ayyayo is what you say when something goes wrong."),
             capture="ayyayo.ai",
             script="And a name. In Tamil, ayyayo is what you say when something goes wrong."),
        card("s5-photos", part("I first used it for an agent that found lost photos."), capture="ayyayo.ai",
             air=0.0, script="I first used it for an agent that found lost photos."),
    ],
)

# ---------------------------------------------------------------- section 6
SAY_IT = dict(
    id="s6", name="Just say it", ground="night", extra=0.15, air=0.25, lead=0.6,
    footage="Captured ayyayo.app footage only (blocked in v1, D011)",
    cards=[
        card("s6-think",
             part("Most children in Tamil Nadu think in Tamil.", pause=0.5),
             part("Most code is written in English."),
             capture="ayyayo.app",
             script="Most children in Tamil Nadu think in Tamil. Most code is written in English."),
        card("s6-like-me", part("And a lot of them, like me, aren’t fast writers."), capture="ayyayo.app",
             script="And a lot of them, like me, aren't fast writers."),
        card("s6-say",
             part("So with ayyayo, they don’t write.", pause=0.6),
             part("They say it.", accent=["They say it."]),
             capture="ayyayo.app", extra=0.8, air=0.0,
             script="So with ayyayo, they don't write. They say it."),
    ],
)

# ---------------------------------------------------------------- section 7
ASK = dict(
    id="s7", name="The ask", ground="paper", extra=0.15, air=0.3, lead=0.7,
    footage="Paper only (as scripted)",
    cards=[
        card("s7-still", part("I’m still not a fast writer."), extra=0.6, script="I'm still not a fast writer."),
        card("s7-anymore",
             part("I don’t need to be anymore.", pause=0.6),
             part("Neither do they."),
             extra=0.6, script="I don't need to be anymore. Neither do they."),
        card("s7-chennai", part("I’m putting ayyayo into classrooms in Chennai."),
             script="I'm putting ayyayo into classrooms in Chennai. (split 1/2, D026)"),
        card("s7-dms",
             part("If you run a school, teach children, or want to build this with me, my DMs are open."),
             extra=0.8, script="If you run a school, teach children, or want to build this with me, my DMs are open. "
                               "(split 2/2)"),
        card("s7-end", part("ayyayo. just say it.", size=72), extra=1.0, air=0.6,
             script="End card: ayyayo. just say it."),
        card("s7-credits",
             part("Music and sound made for this film. Piano samples: Salamander Grand Piano V3 by Alexander Holm, "
                  "CC BY 3.0.", size=60),
             extra=0.0, air=0.6, credits=True,
             script="(end credits: attributions, as the brief requires)"),
        card("s7-father", part("For my father, who studied until the third grade.", size=60), extra=1.5, air=0.0,
             final=True, script="Final small card: For my father, who studied until the third grade."),
    ],
)

SECTIONS = [LIBRARY, NINE, ALONE, WELL_SAID, WELL_DONE, SAY_IT, ASK]
OPENS = {"A": OPEN_A, "B": OPEN_B}
