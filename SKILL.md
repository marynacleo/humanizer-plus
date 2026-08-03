---
name: humanizer-plus
description: "Strip AI-writing tells from any text in English, French or Russian, then verify the result with a mechanical detector before it is published. Use before publishing or sending anything outward: web pages, articles, social posts, client and administrative letters, ad copy, lead magnets, interface strings. Also for auditing text that is already live, and for judging whether someone else's draft is slop. Do not use on code, on working chat, or on internal notes."
allowed-tools: Read Edit Write Glob Grep Bash
license: MIT
metadata:
  version: "1.0.0"
---

# Humanizer plus

Built on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
by way of [blader/humanizer](https://github.com/blader/humanizer) v2.9.1 (MIT). The upstream skill,
unchanged and with a before/after example for each of its 33 patterns, is kept in
`reference/upstream-humanizer-2.9.1.md`. Open it whenever a case is arguable.

This file is the working checklist plus the layer that upstream does not have: French and Russian
tells, publisher typography rules, and a detector that checks the finished text instead of trusting
that the rewrite went well.

## What the skill does

1. Find the patterns listed below.
2. **Keep the information, drop the shape.** Every claim in the source survives. Depth does not have
   to be even: compress the dull parts, slow down where a person would, merge and split paragraphs
   freely.
3. **Never invent a fact.** No name, number, date, quote or citation that is not in the source or
   supplied by the author. A vague claim becomes a specific one only when the specific comes from
   the source. If a sentence needs a real detail that does not exist, ask for it or write the plain
   version without it. A fabricated fact is a defect even when it reads better than the vague
   original.
4. **Keep the author's voice.** If a writing sample is provided, the sample outranks every style
   rule here except the typography rules the publisher has made absolute.

### Voice is half the work

Scrubbing the patterns is only half of it. Smooth, opinion-free, faceless prose gives itself away as
readily as slop does. Judgement, hesitation, uneven rhythm and a real aside are signs of a person, and
they may be added. Facts may not. For reference, legal and technical text the neutral register is the
human one, so no opinions go in there.

## The patterns (33, numbered as upstream)

**Content**
1. Inflated significance: stands as, serves as, testament, pivotal, key moment, underscores its importance, evolving landscape, marking a shift, deeply rooted.
2. Inflated notability: independent coverage, leading expert, active social media presence, a list of outlets with no context.
3. Fake depth on "-ing": highlighting, ensuring, reflecting, showcasing, fostering, contributing to. FR: "soulignant", "témoignant de". RU: «подчёркивая», «отражая».
4. Advertising register: boasts, vibrant, rich (figurative), nestled, in the heart of, breathtaking, must-visit, stunning, renowned. For travel and lifestyle brands this is also a tone-of-voice breach.
5. Vague attribution: experts argue, observers have cited, industry reports, some critics say. Name the real source or cut the claim. Never decorate it.
6. Formulaic "Challenges and Future Prospects" and "Despite these challenges" sections.

**Language**
7. AI vocabulary: delve, crucial, pivotal, key, enhance, foster, garner, highlight, interplay, intricate, landscape, showcase, tapestry, testament, underscore, vibrant, valuable, align with, additionally.
8. Copula avoidance: serves as, stands as, represents, boasts, features, offers, where "is" or "has" is the honest verb.
9. Negative parallelism: not only... but also, it is not just X it is Y, and clipped tailing negations ("no guessing").
10. Rule of three: ideas forced into triplets to look complete.
11. Elegant variation: protagonist, main character, central figure, hero, all for the same person.
12. False ranges: "from X to Y" where X and Y are not on one scale.
13. Passive voice and subjectless fragments: "the results are preserved automatically", "no config file needed".

**Style**
14. **Em and en dashes: cut them all.** The publisher rule here is absolute, including interface strings, and it has no "the author's sample uses them" exception. Replace, in order of preference: full stop, comma, colon, brackets, restructure. Catch spaced ` — ` and ` -- ` too.
15. Mechanical bold inside a paragraph.
16. Inline-header lists: "- **Heading:** one sentence".
17. Title Case in headings.
18. Emoji on headings and bullets.
19. Curly quotes where straight ones belong. Exception: French guillemets with non-breaking spaces are correct French, not a tell.
20. Chat residue: "I hope this helps", "Of course!", "Would you like me to expand on this?".
21. Knowledge-cutoff disclaimers and speculative gap-filling: "as of my last update", "not publicly available, suggesting a low profile", "likely grew up in".
22. Sycophancy: "Great question!", "You are absolutely right".

**Padding**
23. Filler: in order to, due to the fact that, at this point in time, it is important to note that the data shows.
24. Excessive hedging: could potentially possibly be argued.
25. Generic upbeat endings. Finish on the last concrete fact instead.
26. Uniform hyphenated pairs: high-quality, data-driven, real-time. Keep the hyphen in attributive position, drop it after the noun.
27. False authority: the real question is, at its core, what really matters, fundamentally.
28. Announcing instead of doing: let's dive in, here is what you need to know, without further ado.
29. A heading followed by a line that only restates the heading.
30. Diff-anchored writing: describing what changed rather than what the thing is. Changelogs and migration guides are the exception.
31. Manufactured punchlines and staccato drama: a run of short fragments engineered to land.
32. Aphorism formulas: X is the language of Y, X becomes a trap, the architecture of trust.
33. Fake-candid openers: "Honestly?", "Look,", "Here's the thing", used as a theatrical pause before an ordinary point.

## The added layer

### French

Tells that the English list does not cover:

- Openers and connectors: "dans un monde où", "à l'ère du numérique", "force est de constater",
  "il est important de noter que", "plongeons dans", "décryptons", "en conclusion", and
  "n'hésitez pas à" closing every paragraph.
- Empty adjectives: riche, véritable, incontournable, unique en son genre, au cœur de, and
  sur-mesure when it does not describe an actual service.
- Symmetric constructions: "non seulement... mais aussi", and triplets of adjectives.
- Heavy nominalisation: "la mise en place de la réalisation de" where a verb belongs.
- **Not tells:** guillemets with non-breaking spaces, the typographic apostrophe, the space before
  `: ; ! ?`, and the formal politeness formulas an administrative letter requires. Do not relax a
  letter to the prefecture in the name of sounding human.

### Russian

- Openers and padding: «в современном мире», «стоит отметить, что», «играет ключевую роль»,
  «широкий спектр», «уникальное сочетание», «в заключение», «таким образом».
- Bureaucratese and verbal nouns: «осуществление проведения работ по».
- Same symmetric patterns as English: «не только... но и», triplets, Title Case headings.

### Publisher rules that outrank upstream

Configured per project. These are the defaults shipped here:

- **No em or en dashes anywhere public**, interface strings included. Upstream is softer and allows
  them when the author's sample uses them.
- **No full stop at the end of a heading, title, slogan or call to action.** Upstream does not
  know this rule.
- **One spelling standard** across the project, chosen deliberately.
- **No tool names** (Claude, Codex, ChatGPT, AI) in public code or copy, unless the subject really
  is AI visibility.
- **No invented credentials, statistics, insurance cover, years of experience or client counts.**
  A special case of the no-invented-facts rule, kept separate because this is where a model lies
  most often and most expensively.

### Where it sits in a pipeline

- Skills that write (brand copy, articles, posts, commercial pages) run first. Humanizer runs **last**,
  on the finished text.
- Language and register skills (formal French, for example) run before it, and humanizer must not
  break the politeness formulas they put in.
- The pre-deploy check calls the detector over the built pages.
- Print and PDF review stays a separate step: this skill reads text, a human reads the final export.

## The detector

```bash
python scripts/ai_tells.py <file or folder> [--lang en|fr|ru|auto] [--all] [--internal] [--json]
```

Zero dependencies, read-only, nothing leaves the machine.

- `--all` also prints soft hits. By default only hard hits are shown.
- `--internal` for working notes: typography (dashes, heading full stops, Title Case, curly quotes)
  drops to soft. Never use it on public text.
- Code, frontmatter, links, HTML markup and quoted text are skipped. In HTML it reads the visible
  text plus `alt`, `title` and meta `content`, because those are public too.
- Exit code is 1 when hard hits exist, so it can gate a deploy.

The detector does not decide anything. It shows where to look and reports tell density per 1000
words. The loop is: run it on the draft, rewrite by hand against the patterns above, run it on the
final, then read the final aloud, because a script cannot hear rhythm.

## False positives, and what to leave alone

A clean human writer trips half of these patterns without any AI involvement. Not tells on their
own: flawless grammar, mixed casual and formal register, dry prose, academic vocabulary, a greeting
or sign-off, one "however", curly quotes by themselves (Word, Google Docs and most CMSes insert
them), one short emphatic sentence, "honestly" mid-sentence, missing citations, tidy formatting.
Quotations, titles, proper names and examples where a phrase is being discussed rather than used are
never rewritten. Look for clusters, not single hits.

**Signs of a person, to be protected:** a specific detail that would be hard to fabricate, mixed
feelings left unresolved, references tied to a particular year and subculture, a choice the writer
can defend, real variation in sentence length, genuine asides and self-corrections.

## Invocation modes

- **Pasted text (default):** draft, then a short list of what still reads as AI, then the final.
- **File:** read it, run the loop internally, rewrite the file in place, report a short summary.
  Prose only: code, frontmatter, data, link targets and CMS block comments stay untouched.
- **Embedded:** another task is using this as one step. Return the final text only.
- **Live page:** edits follow the project's own safe write path, and the page is checked after.
  This skill grants no permission to write to production.

## Process

1. Read the input and mark every hit.
2. Write a draft: reads aloud, varied sentence length, plain constructions, right register.
3. Ask two questions. What still sounds like AI here? Does the rewrite contain any fact, name,
   number, date or citation that was not in the source?
4. Produce the final: answer both, remove every dash, check headings for a stray full stop.
