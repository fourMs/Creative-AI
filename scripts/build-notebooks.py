#!/usr/bin/env python3
"""Generate the chapter Jupyter notebooks for the Creative AI textbook.

This is a one-shot scaffolding script. It writes each chapter as an .ipynb
file containing only Markdown cells separated by ``\\n\\n---\\n\\n`` in the
source strings below. After the initial scaffolding, you can edit the
notebooks directly with Jupyter, VS Code, or any text editor.

Run from the repo root:

    python scripts/build-notebooks.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"


def make_notebook(markdown_blocks: List[str]) -> dict:
    """Build a minimal nbformat 4.5 notebook with markdown cells only."""
    cells = []
    for block in markdown_blocks:
        text = block.strip("\n")
        if not text:
            continue
        cells.append(
            {
                "cell_type": "markdown",
                "metadata": {"language": "markdown"},
                "source": text,
            }
        )
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook(filename: str, blocks: List[str]) -> None:
    nb = make_notebook(blocks)
    out = BOOK / filename
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


def split_blocks(text: str) -> List[str]:
    """Split a chapter source string into cells on standalone '---' lines."""
    text = text.strip("\n")
    parts = re.split(r"\n-{3,}\n", text)
    return [p.strip("\n") for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# Chapter sources
# ---------------------------------------------------------------------------

INTRO = r"""---
title: Creative AI
subtitle: An open textbook for a bachelor course at the University of Oslo
authors:
  - name: Alexander Refsum Jensenius (ed.)
    affiliation:
      - University of Oslo
description: "An open undergraduate textbook on Creative AI. The book accompanies a 12-week course open to students from all faculties at the University of Oslo."
---

---

![Creative AI book cover](figures/cover/creative-ai-cover.svg)

---

## Welcome

You are reading the open textbook for **Creative AI**, a bachelor-level course at the University of Oslo (UiO). The course is open to students from *all* faculties, regardless of prior experience with programming, machine learning, or any particular art form. The book is also written for self-study and as a public resource for anyone curious about creative uses of AI.

The aim of the course is twofold:

1. To give you a working *understanding* of how today's generative AI systems are built and why they behave the way they do.
2. To give you *hands-on experience* using these systems for creative work, alongside the critical vocabulary needed to discuss their cultural, ethical, and environmental consequences.

Three concepts thread through every week: **intentionality**, **aesthetic control**, and **ethical authorship**. The interesting question is not *can the model do this*, but *what do you want, how do you guide the system there, and on whose terms*.

---

## Course at a glance

| Field | Value |
| --- | --- |
| Course title | Creative AI |
| Level | Bachelor — open to students from all UiO faculties |
| Credits | 10 ECTS (suggested) |
| Duration | 12 teaching weeks |
| Format per week | 1 h lecture + 2 h practice-based lab |
| Workload | ≈ 6 hours of self-study and project work per week |
| Prerequisites | None. Basic digital literacy assumed; no programming required. |
| Language | English (with discussion in Norwegian as needed) |
| Teaching team | Coordinator + invited guest lecturers from across UiO faculties |

---

## Course description (for the course catalogue)

Artificial intelligence has moved from a back-office technology into a tool that shapes everyday creative work: writing, drawing, photography, music, video, design, code, journalism, scholarship, and teaching. **Creative AI** introduces students from across the University of Oslo to the concepts, tools, and ethics of working creatively with contemporary AI systems.

The course assumes no prior programming or specialised art background. Through a combination of short lectures and weekly hands-on labs, students learn how today's text, image, sound, video, and multimodal models work; how to direct and refine their outputs; how to integrate them responsibly into their own discipline; and how to reflect critically on the cultural, legal, environmental, and political stakes of the technology.

Students leave the course with a small portfolio of creative AI artefacts, a documented prompt and decisions log, and a final project presented at a public end-of-semester *Synthetic Gallery* showcase at UiO.

---

## Learning outcomes

Following the standard UiO three-tier format:

:::{important} Knowledge
Having completed the course, students will:

- explain core ideas behind contemporary generative AI in plain language — including neural networks, large language models, diffusion models, multimodal and agentic systems — and be able to describe what they cannot do;
- identify typical use cases and limitations of generative AI across text, image, sound, video, code, 3D, and design;
- describe the key ethical, legal, social, and environmental questions raised by Creative AI: bias, hallucination, consent, copyright, labour, energy, authorship, and authenticity.
:::

:::{important} Skills
Students will be able to:

- use a range of accessible AI tools to produce text, images, sound, video, code, and design artefacts;
- design effective prompts, workflows, and iteration loops to direct AI systems toward specific creative goals;
- critically evaluate AI-generated content for quality, bias, factual reliability, and appropriateness;
- document their creative process — tools, prompts, decisions, edits — transparently and reproducibly;
- collaborate in small groups to design and deliver a creative AI project.
:::

:::{important} General competence
Students will:

- discuss opportunities and risks of Creative AI in their own discipline with both technical and critical literacy;
- reflect on how AI reshapes notions of creativity, originality, and authorship — and on what stays human;
- make informed, responsible choices about using AI tools in study, professional, and civic contexts.
:::

---

## Recommended background

- No programming experience required.
- Basic digital literacy (web browsing, document editors, file management) is assumed.
- Curiosity from any discipline is more important than any specific prior knowledge.

Students who already program will find an optional **"code track"** in each weekly chapter (clearly marked) — typically a short Python notebook that opens the hood on the same idea explored in the no-code lab.

---

## Modes of teaching and learning

Each weekly cycle follows the same shape:

1. **Before class** — read the week's chapter (≈ 1 hour). The textbook is meant to be read *before* the lecture, not in place of it.
2. **Lecture (1 h)** — short talk, demos, class discussion. Many lectures feature a guest from another UiO faculty or research centre (RITMO, IFI, IMV, Department of Media and Communication, KHiO, etc.).
3. **Practice (2 h)** — guided hands-on lab. You will work alone or in pairs with real AI tools, produce a small artefact (a paragraph, an image, a sound, a sketch, a short video, or some code), and discuss results with peers.
4. **Self-study (≈ 6 h)** — reading, follow-on experimentation, work on assignments and the final project.

In **week 0** (the week before teaching starts) all students complete a short **AI-literacy onboarding module**: account setup for the term's tools, a privacy briefing, and the [AI at UiO](https://www.uio.no/english/services/ai/) guidelines for student use of AI.

---

## Course schedule

The 12-week schedule below maps lectures, practice labs, and assignment milestones. Practice sessions deliberately mix modes: some weeks you will use commercial tools in the browser; other weeks you will write a few lines of Python in a notebook on your laptop or in [UiO Educloud](https://www.uio.no/english/services/it/research/platforms/edu-research/).

| Week | Chapter | Lecture (1 h, theory) | Practice (2 h, hands-on) | Milestone |
| ---: | --- | --- | --- | --- |
| 1 | [What is Creative AI?](introduction.ipynb) | From Dadaism to diffusion — a brief history; defining creativity, AI, and Creative AI | First experiments with one text tool and one image tool; start the practice log | **A1** starts: AI-augmented self-introduction |
| 2 | [Foundations of AI](foundations.ipynb) | Data, models, training, inference; bias from data | Inspect a public model card; optional 10-line training loop | A1 due |
| 3 | [Generative AI](generative-ai.ipynb) | Probability, sampling, conditioning, prompts | Same prompt, three samplers; controlled image experiments | — |
| 4 | [AI and language](ai-language.ipynb) | Large language models; in-context learning; hallucination | Prompt library for your discipline; hallucination hunt | **A2** starts: AI-assisted text in your field |
| 5 | [AI and images](ai-images.ipynb) | Diffusion models; controllability; image-to-image | Four-image series with a controlled variable; image-to-image | A2 due |
| 6 | [AI and sound](ai-sound.ipynb) | Speech, music, sound design; consent and voice | Transcribe and remix a clip; build a 30-second piece | **A3** starts: multimodal mini-piece |
| 7 | [AI and video](ai-video.ipynb) | Time, motion, consistency; lip-sync; deepfakes | Storyboard and produce a 10-second clip; critique | A3 due |
| 8 | [Creative coding with AI](ai-code.ipynb) | Pair programming with an LLM; generative graphics | p5.js sketch with an AI assistant; read code you did not write | — |
| 9 | [AI for 3D, design, and games](ai-3d-games.ipynb) | NeRFs / Gaussian splats; generative pipelines for game and design | Gaussian splat capture or text-to-3D asset in a scene | **Final-project proposal** starts |
| 10 | [Multimodal and agentic AI](multimodal-agents.ipynb) | When models see, hear, and act; briefs as the new interface | Design (on paper) a multi-step AI pipeline for a creative task | Proposal due |
| 11 | [Ethics and politics of Creative AI](ethics.ipynb) | Copyright, bias, labour, energy, authorship | Class debate; ethical audit of one tool | **Ethics essay** (Pass/Fail) due |
| 12 | [Futures and final projects](futures.ipynb) | Three futures of Creative AI; what stays human | *The Synthetic Gallery* — public showcase of final projects | **Final project** due |

:::{tip} Reading the chapters
Each chapter is roughly the length of one short lecture's worth of reading. Every chapter follows the same six-section shape: *Why this matters → Concepts → Examples → Practice → Reflection prompts → Going further*. The Practice section is what you will do in the 2-hour lab that week.
:::

---

## Pedagogical strategy

### A course for everyone at UiO

Creative AI is *not* a specialist course in computer science, art, or media. It is designed as a **general education** course: students arrive from law, medicine, musicology, design, theology, mathematics, dentistry, education, literature, biology, and many other places. That diversity is the point. The classroom is itself a small interdisciplinary laboratory where lawyers and artists, medics and historians can ask hard questions of the same AI tool and watch each other's answers.

We assume **no programming background**, but each weekly lab provides an optional *code track* for students who want to look under the hood. Where we use code, it is in Python notebooks that you can run in your browser without installing anything.

### Active learning and a flipped classroom

This course is built around [active learning](https://en.wikipedia.org/wiki/Active_learning) and a [flipped classroom](https://en.wikipedia.org/wiki/Flipped_classroom) model: the chapter is read *before* the lecture; the lecture is the place to argue, demo, and answer the questions you bring in; the lab is where you make things.

### Studio-based labs and process over polish

The labs are run **studio-style**: short briefs, fast iteration, peer feedback, instructor and TA on hand. The assessment philosophy follows from this — we grade *process*, *reflection*, and *deliberate decisions* over technical perfection. Risk-taking, honesty about failure, and originality are explicitly rewarded.

### Guest lecturers from across UiO

Where possible, each week's lecture features a guest from a UiO department or research centre whose work intersects with the week's theme: e.g., RITMO for sound and music, IFI for the machine-learning weeks, IMK for the ethics and media weeks, KHiO and architecture for design weeks, the Law Faculty for the copyright discussions, NB AI Lab and the National Library for language and audio in Norwegian.

### Research-based and research-led

This is a *research-based* course: the content rests on current research from machine learning, human–computer interaction, media studies, the humanities, and the arts. It is also *research-led*: the teachers are themselves working on Creative AI projects, and parts of the course (in particular the final-project showcase) feed into ongoing research at UiO and partner centres.

### A note on AI tools used to write this book

This textbook is itself an example of AI-supported authorship. Drafts of every chapter have been written collaboratively with large language models, then revised, fact-checked, and re-organised by human editors. Where AI tools have produced figures or examples, we say so. We treat the book as a living document — please open an issue or a pull request on the [GitHub repository](https://github.com/fourMs/Creative-AI) when you spot errors or omissions.

---

## Tools we will use

Across the semester you will meet many tools. The list below is not exhaustive, and any of it may change as the field moves. The point is to *learn the categories*, so that you can evaluate the next tool that appears.

<details>
<summary>Text and dialogue</summary>

- [ChatGPT](https://chatgpt.com/), [Claude](https://claude.ai/), [Gemini](https://gemini.google.com/), [Mistral Le Chat](https://chat.mistral.ai/) — commercial chat assistants
- [LM Studio](https://lmstudio.ai/), [Ollama](https://ollama.com/) — running open-weight models locally on your laptop
- [Sudowrite](https://www.sudowrite.com/), [NotebookLM](https://notebooklm.google.com/) — writing-focused tools

</details>

<details>
<summary>Images</summary>

- [Midjourney](https://www.midjourney.com/), [DALL·E](https://openai.com/index/dall-e-3/), [Adobe Firefly](https://www.adobe.com/products/firefly.html), [Ideogram](https://ideogram.ai/) — commercial text-to-image
- [Stable Diffusion](https://stability.ai/) (with [ComfyUI](https://www.comfy.org/) or [InvokeAI](https://invoke.com/)) — open-weight image models
- [Krea](https://www.krea.ai/), [Recraft](https://www.recraft.ai/) — design-oriented tools

</details>

<details>
<summary>Sound and music</summary>

- [Suno](https://suno.com/), [Udio](https://www.udio.com/) — text-to-song
- [ElevenLabs](https://elevenlabs.io/), [Resemble](https://www.resemble.ai/) — voice generation and cloning
- [Riffusion](https://riffusion.com/), [Stable Audio](https://stability.ai/stable-audio) — sound and music generation
- [Magenta](https://magenta.tensorflow.org/), [RAVE](https://github.com/acids-ircam/RAVE) — research-grade open tools

</details>

<details>
<summary>Video and animation</summary>

- [Runway](https://runwayml.com/), [Pika](https://pika.art/), [Luma Dream Machine](https://lumalabs.ai/dream-machine), [OpenAI Sora](https://openai.com/sora) — text- and image-to-video
- [Kaiber](https://kaiber.ai/) — stylised animation

</details>

<details>
<summary>Code and creative coding</summary>

- [Cursor](https://cursor.com/), [GitHub Copilot](https://github.com/features/copilot), [Claude Code](https://www.anthropic.com/claude-code) — AI-assisted development environments
- [p5.js](https://p5js.org/), [Processing](https://processing.org/) — creative coding host languages
- [Hugging Face Spaces](https://huggingface.co/spaces) — running models in the browser

</details>

<details>
<summary>3D, design, and games</summary>

- [Luma AI](https://lumalabs.ai/), [Polycam](https://poly.cam/) — Gaussian splats and 3D capture
- [Meshy](https://www.meshy.ai/), [Tripo3D](https://www.tripo3d.ai/) — text/image to 3D mesh
- [Scenario](https://www.scenario.com/), [Layer](https://www.layer.ai/) — game-art pipelines

</details>

:::{warning} Tool turnover
Specific products listed above will appear, merge, and disappear during the semester. Treat the list as a starting point, not a syllabus. In every practice session we will use whatever currently works well enough for the task at hand.
:::

---

## Open Education and Open Research

The textbook follows the principles of [Open Education](https://en.wikipedia.org/wiki/Open_education) and [Open Research](https://en.wikipedia.org/wiki/Open_research): the material is openly licensed (CC-BY-4.0), the source is on GitHub, and we point to open tools and datasets where possible. Where a tool requires a paid account, we say so and try to offer an open alternative.

This is also a political stance. Creative AI is being built and deployed mainly by a handful of large companies. Treating the *study* of Creative AI as an open, collaborative project is one small way to push back.

---

## Assessment

There is no traditional written exam. The expectation is that you can talk and write coherently about what you made, with what tools, and why. Assessment is *portfolio-based* and is structured as a ladder of increasingly ambitious deliverables:

| Component | Weight | Mode | What it is |
| --- | ---: | --- | --- |
| Weekly practice log | 10 % | Pass / Fail | A short entry each week: brief, tools used, prompts, what you noticed, one open question. Submitted via the LMS. |
| **A1** — AI-augmented self-introduction | 5 % | Graded | 1 page of text + 1 image + ½ page reflection. Due in week 2. |
| **A2** — AI-assisted text in your discipline | 10 % | Graded | 800–1 200 words in a chosen genre (academic, creative, or popular science) + a 1–2 page reflection documenting prompts and edits. Due in week 5. |
| **A3** — Multimodal mini-piece | 10 % | Graded | A 3–5 page (or slide) cross-modal piece combining text and at least one other modality, with reflection. Due in week 7. |
| Mid-term **ethics essay** | 10 % | Pass / Fail | 1-page argumentative essay on a topic of the student's choice (recommended: *"Death of the Artist or Birth of the Curator?"*, *"Should AI-generated work be copyright-eligible?"*, *"Where should AI stay out of my discipline?"*). Due in week 11. |
| Final-project **proposal** | 5 % | Pass / Fail | 1–2 page proposal + feasibility sketch. Due in week 10. |
| **Final project** + reflection | 50 % | Graded | A creative AI artefact in any medium, presented at the *Synthetic Gallery* showcase in week 12, plus a 1 500–2 500-word reflective essay and the full prompt log. Solo or groups of 2–3. |

### Process memo

Each graded assignment is submitted with a short **process memo** answering, at minimum, two prompts that we will use all semester (adapted from the practice-based tradition at RITMO and from earlier creative-AI courses):

1. **Surprise.** Where did the AI surprise you — pleasantly or unpleasantly — and what did that teach you about the tool?
2. **Will.** Where did you exert your own creative *will* over the output — through prompt, edit, refusal, selection, or composition?

These two questions are the centre of gravity of the course. If you can answer them honestly across all your work, you will pass.

### The final project — "The Synthetic Gallery"

The final project is presented at a **public mini-exhibition** in week 12 (the *Synthetic Gallery*), open to other UiO students and staff. The exhibition lives both physically (in a UiO common space) and online (as a static gallery on the course's GitHub Pages site). Selected projects, with consent, are kept in the public gallery for future cohorts.

Final-project requirements:

- Any medium — text, image series, short film, song / EP, podcast episode, interactive sketch, small game, redesign of a real organisation's brand, critical essay, teaching resource, etc.
- The work must use **at least two different AI modalities** (e.g., text + image, image + video, audio + code) — this is the technical bar.
- Solo or groups of 2–3.
- Documented with a full prompt-and-decisions log and a 1 500–2 500-word reflection.

:::{tip} Academic integrity and AI
You are *allowed and encouraged* to use AI tools in this course. You must, however, **declare** which tools you used and *how*. A simple, honest log of prompts and decisions is enough. Hiding AI use is treated as academic dishonesty; using AI thoughtfully and transparently is treated as a course goal.
:::

---

## How to read this book

The chapters are roughly linear, but they are also self-contained. If you are a complete beginner, read in order. If you already have some background, you can skim chapters 2–3 and jump into the application chapters that interest you (text, image, sound, video, code).

Every chapter follows the same six-section shape:

1. **Why this matters** — a short framing.
2. **Concepts** — the ideas you should be able to explain after reading.
3. **Examples** — concrete cases, screenshots, code snippets.
4. **Practice** — what you will do in the 2-hour lab session.
5. **Reflection prompts** — questions for your weekly log.
6. **Going further** — readings, tools, links.

Let's begin.
"""


CH1 = r"""---
title: "1. What is Creative AI?"
subtitle: "Setting the scene for the course"
description: "An introduction to the field of Creative AI: what we mean by creativity, what we mean by AI, and why their meeting in 2022–2026 is reshaping cultural production."
---

---

## Why this matters

In the autumn of 2022, a sentence typed into a web form could produce a photographic-looking image of a place that does not exist. A few months later, a paragraph could be drafted by a model that had read most of the open web. By 2024 we had short videos from text, songs from text, and code from text. By 2026 these tools are everywhere — in editors, in browsers, in phones — and the question is no longer *whether* they can produce something but *what we should do with them*.

This week we ask: **what is Creative AI**, and why is it now suddenly the subject of an undergraduate course at UiO?

```{admonition} Question
:class: question
Before reading further, write a one-sentence definition of *Creative AI* in your own words. Keep it; we will return to it at the end of week 12.
```

---

## Three slippery words

Each of the three words in *Creative AI* hides a long argument.

### Creativity

[Creativity](https://en.wikipedia.org/wiki/Creativity) is one of the oldest contested concepts in the humanities. A common working definition is that something is creative when it is *novel* and *valuable* in some context. The cognitive scientist Margaret Boden distinguishes between two senses [@Boden2004]:

- **P-creativity** ("psychological"): novel *to the person who produced it*.
- **H-creativity** ("historical"): novel *to humanity*.

A child's first drawing of a face is P-creative; the invention of perspective in early Renaissance painting is H-creative.

Boden also distinguishes three *kinds* of creativity:

- **Combinational** — putting familiar ideas together in unfamiliar ways (collage, mash-up).
- **Exploratory** — moving around inside an existing conceptual space and discovering its corners.
- **Transformational** — changing the conceptual space itself, so that ideas previously impossible become thinkable.

We will return to this triple repeatedly. Generative AI is excellent at the first two and ambiguous about the third.

### Artificial intelligence

"AI" is even older as a label (the [Dartmouth workshop](https://en.wikipedia.org/wiki/Dartmouth_workshop) coined the phrase in 1956) and even harder to pin down. A pragmatic working definition is:

> *Artificial intelligence* is the study and construction of systems that perform tasks we would otherwise consider to require human cognition.

That definition is deliberately slippery: as soon as a task becomes routine (chess, OCR, spam filtering, speech-to-text), it tends to lose its "AI" status. Russell and Norvig describe four canonical framings: systems that think like humans, act like humans, think rationally, or act rationally [@Russell2021].

For our purposes, the AI in *Creative AI* almost always refers to **machine-learned**, often **generative**, systems based on **neural networks** trained on large datasets. We unpack each of those words in chapters [2](foundations.ipynb) and [3](generative-ai.ipynb).

### Creative AI

Putting the two together, we can define the field of study as follows:

:::{important} Working definition
**Creative AI** is the use of machine-learned generative systems — for text, image, sound, video, code, 3D, or any other expressive medium — as tools, materials, or collaborators in cultural and design work. As a field of study, it asks both *how these systems work* and *what changes when they enter the practices of writing, art, music, design, journalism, and education.*
:::

Notice three things about this definition:

1. It is **medium-agnostic**. We are not building yet another course on "AI for music" or "AI for writing". The whole point of this generation of models is that the same architectures move between media.
2. It treats AI **as a material**, not only as a topic. We will use these tools, not just read about them.
3. It includes **both the technical and the cultural side**. Without the technical side, we cannot evaluate claims about what AI can or cannot do. Without the cultural side, we cannot evaluate what it should or should not be doing.

---

## A short, opinionated history — *from Dadaism to diffusion*

The history of Creative AI is older than it looks, and it has two intertwined strands. One strand is the *technology* — rule-based programs, neural networks, transformers, diffusion. The other is the *art-historical* lineage of practices that *welcomed chance, machines, systems, and procedures into the studio* long before any of this technology existed. Without that second strand, the first looks like it appeared from nowhere in 2022.

```{figure} figures/timeline.svg
:alt: A simplified timeline of creative AI milestones from 1957 to today
:align: center
A simplified timeline of creative AI milestones from 1957 to the mid-2020s.
```

### The art-historical strand

- **1910s — Dadaism.** Tristan Tzara writes a poem by drawing words out of a hat. The point is precisely that *chance* is allowed into the work, and that the artist's role becomes setting the conditions rather than choosing every word.
- **1950s–60s — Concrete music, serialism, and Fluxus.** Composers like Iannis Xenakis use stochastic processes to compose pieces; the Fluxus group treats *instructions* as the artwork ("Drip Music", "Composition 1960 #7").
- **1960s–70s — Generative art.** Vera Molnar, Manfred Mohr, and Frieder Nake produce drawings *with* algorithms and plotters; Sol LeWitt writes "Sentences on Conceptual Art" — *"the idea becomes a machine that makes the art"*.
- **1990s–2010s — Algorithmic art and creative coding.** Casey Reas and Ben Fry release Processing; *generative art* becomes a stable category and the lineage that today flows directly into AI-augmented creative coding (chapter [8](ai-code.ipynb)).

The shift to generative AI is therefore not a break with art history — it is the latest entry in a long tradition of artists *delegating* parts of the work to systems, procedures, and machines. What changes is *how much* gets delegated, *how powerful* the systems are, and *who* owns them.

### The technical strand

- **1957 — Illiac Suite.** Lejaren Hiller and Leonard Isaacson compose what is often cited as the first piece of music generated by a computer, using rules and pseudo-random choices.
- **1973–present — AARON.** The artist Harold Cohen develops AARON, a rule-based system that draws and later paints autonomously [@McCorduck1991].
- **1980s — Markov models and expert systems** are used in music composition (David Cope), in story generation (TALE-SPIN, MINSTREL), and in design.
- **2014 — Generative Adversarial Networks (GANs).** Goodfellow and colleagues introduce a new way to train generators by pitting them against discriminators [@Goodfellow2014GAN]. This kicks off the first wave of "neural" creative AI.
- **2015 — DeepDream.** Google researchers turn an image classifier inside out and produce hallucinated, dog-eyed pictures that go viral. For the first time, a wide public *sees* what a neural network "thinks".
- **2017 — Transformer architecture.** Vaswani et al. publish "Attention Is All You Need" [@Vaswani2017]; within a few years it becomes the dominant architecture for language, image, audio, and code models.
- **2020 — Diffusion models** mature [@Ho2020Diffusion], and large language models pass the threshold where they become useful for general writing [@Brown2020GPT3].
- **2022 — The generative turn.** *Stable Diffusion* (open-weight), *DALL·E 2*, *Midjourney*, and *ChatGPT* all land within a few months. Generative AI moves from research labs into the hands of millions of users.
- **2023 onwards — Multimodality and scale.** Models now handle text, image, audio, and video together, run on phones, and are integrated into operating systems, browsers, and creative software.

Two patterns are worth pulling out of this list. First, **the medium-specific waves are converging**: by 2024 the same model family powers writing, drawing, coding, and speaking. Second, **public visibility lags research by years**: every "sudden" public moment (2015 DeepDream, 2022 ChatGPT) sits on top of a decade of slower academic and industrial work.

### Three concepts that thread through the course

Out of these two strands, three concepts run through every remaining chapter:

- **Intentionality.** Why are *you* making this? A model can produce a thousand variations cheaply. The interesting question is which of them you *meant*.
- **Aesthetic control.** How precisely can you steer the system toward the artefact you actually want? Most of the technical content of this course — prompts, conditioning, sampling, editing, reference images, LoRAs, agents — is in service of this single question.
- **Ethical authorship.** Who is the author when a model trained on millions of other people's work assists you? What do you owe them, your audience, and yourself in how you describe the work?

We will return to these three words repeatedly. They will also appear, almost verbatim, in your process memos.

---

## What is *not* Creative AI

To sharpen the working definition above, here are a few things this course is **not** about:

- **AI in general.** We will not survey self-driving cars, medical diagnosis, or fraud detection.
- **The mathematics of deep learning.** A few equations help and we will show them, but you do not need to derive backpropagation to pass the course.
- **AGI/ASI predictions.** Speculation about super-intelligence is a fine pub conversation but not a useful basis for a 12-week practical course in 2026.

We will, however, take seriously:

- **Critical perspectives** from the humanities and social sciences on what these systems do to labour, copyright, attention, education, and the environment [@Crawford2021Atlas; @Bender2021Parrots; @ONeil2016].
- **Hands-on use** of the systems, so that the criticism is grounded in experience.

---

## Practice (2 h)

In the practice session this week you will run **two small experiments** and start a personal *practice log* that you will keep all semester.

1. **Pick one text tool and one image tool** from the lists in the [introduction](intro.ipynb). Make a free account if needed.
2. **Same brief, two media.** Write a single short brief (1–2 sentences) for a small creative task. For example: *"A flyer for a student concert at Chateau Neuf featuring a jazz trio."* Use the text tool to draft the flyer text; use the image tool to draft a visual.
3. **Vary one thing.** Re-run each generation with **one** parameter changed (a different style, a different tone, a longer or shorter prompt). Save both versions.
4. **Write a log entry** with these sections:
   - Brief used.
   - Tools used (with version, if shown).
   - Two prompts, exact wording.
   - One sentence on what you got, one sentence on what you expected, one sentence on the gap.
5. **Tell us a story.** In the last 30 minutes of class, pair up and present each other's experiments to a third student. We will then collect surprises on the board.

:::{tip} Save your prompts
Throughout this course, save every prompt you write. It will become the most valuable artefact in your project portfolio at week 12.
:::

---

## Reflection prompts

For your weekly log, choose one prompt and write 150–300 words:

1. Compare your one-sentence definition of *Creative AI* (from the start of this chapter) with the working definition we ended up with. What did you leave out? What did you include that we did not?
2. Pick one item from the short history above and look it up. What was the historical context (technical, cultural, economic)? Is there a similar context for the 2022 generative turn?
3. In your discipline, what counted as "creative work" five years ago? Which parts of it are most affected by generative AI today?

---

## Going further

- Margaret Boden, *The Creative Mind: Myths and Mechanisms* [@Boden2004]
- Lev Manovich, *AI Aesthetics* [@Manovich2018] — short and accessible
- Kate Crawford, *Atlas of AI* [@Crawford2021Atlas] — for the political side
- The [AI Index Report](https://aiindex.stanford.edu/) (Stanford HAI) — annual snapshot of the field

Open tools you can install this week:

- [Ollama](https://ollama.com/) — open-weight chat models on your laptop
- [Stable Diffusion in the browser](https://huggingface.co/spaces) — many free Spaces

```{admonition} Question
:class: question
By the end of the week, can you finish this sentence in three different ways?

*"Creative AI is to writing what \\_\\_\\_ is to \\_\\_\\_."*
```
"""


CH2 = r"""---
title: "2. Foundations of AI"
subtitle: "Data, models, training, and inference"
description: "A non-mathematical introduction to how today's AI models actually learn from data, why they look like they do, and what that means for using them in creative work."
---

---

## Why this matters

If we are going to use generative AI seriously, we need a *mental model* of how it works. Not the equations — we can leave those to the specialists — but the cast of characters: **data**, **models**, **training**, **inference**, **parameters**, **loss**, **generalisation**, **bias**. With those words in place, the rest of the course makes sense.

By the end of this chapter you should be able to explain, in plain language and over coffee, what happens when somebody says "we trained a model on a billion images and now we are using it to generate logos".

---

## A toy starting point: learning from examples

Imagine you want to teach a computer to tell **cats** from **dogs** in photographs. You have two strategies:

1. **Write rules by hand.** "If the ears are pointy and the snout is narrow…" — this is the *symbolic* AI of the mid-20th century. It works for small problems and breaks for anything visual at the level of the real world.
2. **Show it many examples** of cats and dogs labelled as such, and let it *learn the rule itself*. This is **machine learning** (ML).

```{figure} figures/ml-pipeline.svg
:alt: A simple diagram showing data flowing into a model with parameters, producing a prediction, with a loss feedback loop into the parameters.
:align: center
A simple machine-learning pipeline: **data** flows into a **model** with **parameters**; the model produces a **prediction**; a **loss** measures how wrong the prediction is and is used to update the parameters.
```

The diagram above is essentially the whole field. The specifics — what the data looks like, what shape the model takes, how the loss is measured — change wildly between applications. But the loop is always the same.

---

## The cast of characters

### Data

Data is the **fuel**. Every AI model you will use in this course was trained on a dataset:

- **Images** — public photography (e.g. [LAION-5B](https://laion.ai/) collections), licensed stock libraries, scraped web galleries.
- **Text** — books, Wikipedia, Common Crawl scrapes of the open web, scientific papers, code repositories.
- **Audio** — music libraries, podcasts, speech corpora, YouTube transcripts.
- **Video** — public video platforms, licensed footage libraries, motion-capture archives.

```{admonition} Question
:class: question
Pick a tool you have used and try to find a public statement about *which dataset* it was trained on. How precise is the answer?
```

The quality, *content*, and *consent* of training data shape the model in deep ways. We will return to this in chapter [11](ethics.ipynb).

### Models

A **model** is a function with **parameters**. In modern AI, this function is a *neural network* — a layered chain of multiplications, additions, and non-linear "squashing" operations. The parameters are the numbers (often billions of them) that determine exactly which input produces which output.

You do not need to know the inner workings to use a model, just as you do not need to know how a violin is made to play one. But two facts matter:

1. **The function is differentiable.** This means we can compute, for each parameter, *which direction would make the prediction slightly better*. That is what makes training possible.
2. **The function is huge.** Modern models have between a few hundred million and a few trillion parameters. The model file alone can be tens of gigabytes.

### Training

**Training** is the process of repeatedly:

1. taking a batch of examples from the dataset,
2. making predictions with the current parameters,
3. measuring the **loss** (how wrong the predictions were),
4. nudging the parameters in the direction that reduces the loss.

This loop runs **billions of times** for a large model. It typically takes days or weeks on hundreds of high-end GPUs and consumes enormous amounts of electricity. Strubell et al. estimated the carbon cost of training a large NLP model already in 2019; the numbers have grown since [@Strubell2019Energy].

The result of training is a **trained model**: the network plus its specific set of parameter values.

### Inference

**Inference** is what happens when you *use* a trained model. You feed it an input (a prompt, an image, an audio clip), and it produces an output. Inference is far cheaper than training — a few cents instead of a few million dollars — but at the scale of hundreds of millions of users it still adds up.

When you type into ChatGPT, you are *running inference* on a previously trained model. The model's parameters do not change.

```{important}
Most of the AI you use day to day is doing **inference**, not training. The model already exists; you are just asking it questions.
```

### Generalisation

We want a model that does well on **new** examples it has never seen. This is **generalisation**. The opposite is **overfitting** — the model has memorised the training examples and does poorly on anything else.

Generalisation is the reason a face-recognition model can recognise a face it never saw during training. It is also the reason a language model can write a paragraph about a topic that did not exist in its training set. (And, as we will see, the reason such a paragraph can be subtly wrong.)

### Bias

Models inherit the **biases of their data**. If a dataset over-represents English-speaking, Western, web-published, well-photographed material, the model will be best at exactly that material. This is not a bug; it is a property of how machine learning works [@Bender2021Parrots; @Crawford2021Atlas]. We will return to bias as an ethical and practical question in chapter [11](ethics.ipynb), but it is also relevant to everyday creative use.

---

## A very short tour of neural networks

A **neural network** is a stack of *layers*. Each layer takes a list of numbers, multiplies them by another list of numbers (the parameters), adds, and passes the result through a simple non-linear function. Stacked many times, this becomes flexible enough to model very complex patterns [@Goodfellow2016].

A few common families you will hear about:

- **Convolutional neural networks (CNNs)** — used for images for most of the 2010s.
- **Recurrent neural networks (RNNs)** — used for sequences (text, audio) until around 2018.
- **Transformers** — the dominant architecture today [@Vaswani2017]. Powers most chat models, image models, and the new generation of audio and video models.
- **Diffusion models** — a *training procedure* layered on top of a neural network, particularly successful for images [@Ho2020Diffusion]. See chapter [5](ai-images.ipynb).

The specific architecture matters for performance, but the cast of characters above stays the same.

---

## Foundation models and fine-tuning

Most state-of-the-art creative AI tools today are **foundation models**: very large models trained once, then *adapted* to many tasks. Adaptation can take several forms:

- **Prompting** — putting the right text in front of the model at inference time. No retraining needed.
- **Fine-tuning** — taking a foundation model and continuing to train it briefly on a smaller, more focused dataset. Costs vary from a few dollars (LoRA on a personal GPU) to millions (full fine-tunes of large models).
- **RLHF / RLAIF** — reinforcement learning from human or AI feedback. Used to align chat models to be helpful and polite.
- **Distillation** — training a smaller "student" model to mimic a larger "teacher".

For most of this course, you will be **prompting** existing foundation models. In chapter [4](ai-language.ipynb) we look at what prompting really is.

---

## Practice (2 h)

This practice session is in two parts. The first is in-browser; the second is optional code.

### Part 1 — Inspecting a model (60 min)

1. Visit [Hugging Face](https://huggingface.co/) and search for **`stable-diffusion`**.
2. Pick one *model card* and read it from top to bottom. Find:
   - Which **dataset** was the model trained on?
   - How many **parameters** does the model have?
   - What is the **licence**?
   - What are the **known limitations**?
3. Write down three things from the card that you did not know before, and one thing you did not understand.

### Part 2 — A 10-line training loop (60 min, optional code track)

This is for students who want to feel a training loop in their fingers. It is *not* required.

We will train a tiny model to fit a curve. Open a notebook and run:

```python
import numpy as np

rng = np.random.default_rng(0)
x = rng.uniform(-1, 1, size=200)
y = 2 * x + 0.5 + rng.normal(0, 0.1, size=200)

# parameters
w, b = 0.0, 0.0
lr = 0.05

for step in range(200):
    pred = w * x + b
    loss = ((pred - y) ** 2).mean()
    grad_w = ((pred - y) * x).mean() * 2
    grad_b = (pred - y).mean() * 2
    w -= lr * grad_w
    b -= lr * grad_b

print(f"w = {w:.3f}, b = {b:.3f}, loss = {loss:.4f}")
```

You should get $w \approx 2$ and $b \approx 0.5$. That is a model with two parameters, trained from scratch, in 12 lines. Every "AI" you will use this semester is the same loop scaled up by a factor of ten billion.

---

## Reflection prompts

1. List three categories of work in your discipline where AI models are *plausibly* useful, and three where you suspect they are not. What is the difference?
2. The training data of large models is mostly English, mostly Western, and mostly from the open web. How might that show up in a model's outputs for your discipline or your native language?
3. Strubell et al. estimated training a large NLP model could emit as much CO₂ as five cars over their lifetimes [@Strubell2019Energy]. How does that change (or not) how you feel about using these tools?

---

## Going further

- Goodfellow, Bengio, Courville — *Deep Learning* [@Goodfellow2016], free at <https://www.deeplearningbook.org/>
- 3Blue1Brown's [Neural Networks](https://www.3blue1brown.com/topics/neural-networks) series on YouTube — best visual explanation of backpropagation
- The [Hugging Face course](https://huggingface.co/learn) — free, code-first, beginner-friendly
- Crawford, *Atlas of AI* [@Crawford2021Atlas], chapter 1, on what is *in* the data
"""


CH3 = r"""---
title: "3. Generative AI"
subtitle: "Probability, sampling, conditioning, and prompts"
description: "From classifying to generating: what changes when an AI model outputs something new instead of labelling something existing, and why that single change reorganised the field after 2020."
---

---

## Why this matters

For most of its history, machine learning was used to **classify** things: is this email spam, is this image a cat, does this MRI scan show a tumour? Generative AI flips the question around: instead of *labelling* an existing thing, the model **produces a new thing**.

This change is small in mathematics and enormous in practice. It is also the change that took machine learning from a back-office technology into something people use in the foreground, every day. This chapter introduces the vocabulary you will need for the rest of the book.

---

## From classifying to generating

Suppose we have a dataset of pictures of cats. A *classifier* learns a function

> "given an image, output 1 if it is a cat, 0 otherwise."

A *generator* learns a different function

> "produce an image that looks like the cats you have seen."

The classifier learns about a *boundary* (cat / not-cat). The generator learns about a *distribution* (the space of plausible cat pictures). The distribution is much harder to learn — but once you have it, you can sample from it and get pictures that did not exist before.

```{important}
Generative AI = **learn a distribution** of training examples, then **sample** from it.
```

This is the single mental shift behind everything in this book.

---

## Probability without tears

You do not need formal probability for this course, but two ideas help.

### Distributions

A **distribution** is a way of saying *how likely* each possible thing is. For example, the heights of UiO students form a distribution: 1.70 m is more likely than 2.20 m. A generative image model implicitly learns a distribution over images. A generative language model learns a distribution over sequences of words.

The catch: the space of all possible images is unimaginably large. A single $512 \times 512$ colour image has 786 432 numbers in it. The set of *plausible* images is a vanishingly thin slice of that vast space. Learning to navigate that slice is what diffusion models, GANs, and transformers do.

### Sampling

To **sample** is to draw a single concrete thing from a distribution. Every time you press "generate" in an image tool, the model is **sampling** from the distribution it learned. Press the button twice and you get two different samples — usually similar in style, never identical.

Samplers have parameters:

- **Temperature** (text and audio models) — high temperature flattens the distribution, making the output more varied and weird. Low temperature sharpens it, making the output safer and more predictable.
- **Top-k / top-p** (text models) — restrict the model to the top *k* or top *p*% of next-token candidates. Stops it from sampling extremely rare nonsense.
- **CFG / guidance scale** (image and video models) — strengthens the influence of the conditioning prompt. Too high and the result becomes oversaturated and rigid; too low and it ignores the prompt.
- **Steps** (diffusion models) — how many denoising steps to take. More steps generally means sharper output, up to a point.

The same prompt with different sampler settings can produce dramatically different results. This is one of the most useful things to internalise this semester.

---

## Conditioning: telling the model what you want

If a generator just samples from its full distribution, you get something randomly cat-shaped. Useful, but not creative *work*. The technical word for steering the generator is **conditioning**.

Conditioning is anything that goes into the model *in addition to noise* to bias what it produces.

- A **text prompt** is the most common form of conditioning.
- A **reference image** can also condition the generation ("make it look like this").
- A **mask** can condition where to change ("only edit this part of the picture").
- A **control signal** like a pose skeleton, edge map, or depth map can condition shape and composition (this is what tools like *ControlNet* do, see chapter [5](ai-images.ipynb)).
- An **audio waveform** or a **piece of MIDI** can condition a music model.
- A **previous frame** can condition the next frame in a video model.

Once you start looking, you will see conditioning everywhere. The user interface of every generative tool is essentially a *conditioning console*.

```{figure} figures/conditioning.svg
:alt: Diagram showing different conditioning inputs (text, image, mask, control) feeding into a single generative model.
:align: center
Multiple ways to condition a single generative model. The model itself is shared; the inputs change.
```

---

## Prompts as the new interface

For a generation of users who have never seen a command line, **prompts** are the new interface. A prompt is just text, but writing a good one is now its own small craft.

A few principles that hold across most chat and image tools:

- **Be specific** about subject, style, context, and constraints.
- **Show, don't only tell** — quote a sentence, paste an example, attach an image.
- **Iterate** — generation is cheap. Treat the first output as a draft.
- **Constrain the form**, not only the content — "in three sentences", "as a bulleted list", "as a poster in 1:2 ratio".
- **Inspect failures** — when the output is wrong, write down *how* it is wrong. That is often more informative than your initial prompt.

We dedicate chapter [4](ai-language.ipynb) to prompts for language models. For now, the take-away is that the prompt **is the interface**, and that interface is *text*. (Even when it includes images, you usually still describe what to do in words.)

---

## A taxonomy of generative models

You will hear many architecture names in the wild. The four big families are:

- **GANs (Generative Adversarial Networks)** [@Goodfellow2014GAN] — train two networks against each other: a *generator* tries to produce realistic samples, a *discriminator* tries to tell them apart from real data. Dominant for images 2014–2020, now mostly retired.
- **Autoregressive models** — predict the next token given the previous ones. Powers all chat models (next word) and many audio and image models. Underlying maths: factorise the joint distribution as a product of conditionals.
- **Diffusion models** [@Ho2020Diffusion; @Rombach2022LatentDiffusion] — learn to *denoise*. Starting from random noise, the model iteratively removes a bit of noise to reveal a coherent image, audio, or video. Dominant for high-quality images, video, and (increasingly) audio.
- **Flow matching / rectified flows** [@Esser2024SD3] — close cousin of diffusion models with simpler training. Powers some of the latest image and video models.

You do not need to memorise this. But when a tool brags about being "GAN-based" or "diffusion-based" or "flow-based", you should be able to nod and understand roughly what that implies.

---

## What generative models *cannot* do

A short list, useful to keep in mind:

1. **They do not know what is true.** A text model can produce a perfectly written paragraph that is factually wrong. An image model can produce a person with six fingers. We will return to this throughout the course.
2. **They generalise from training data, not from causal understanding.** They have no model of physics, no model of social cause, no model of why things happen.
3. **They are not deterministic at default settings.** Same prompt, different output.
4. **They cannot remember you across sessions** unless they are explicitly designed to (with retrieval, memory, or fine-tuning).
5. **They are bounded by their training cutoff.** Anything newer than the cutoff is invisible to them unless they can search the web or read uploaded files.

---

## Practice (2 h)

### Same prompt, three samplers

1. Pick one image tool you have access to.
2. Write a prompt that has a *clear style and subject* — for example, *"a watercolour illustration of a fox reading a book in a library, soft lighting, warm tones"*.
3. Generate the image with three different settings:
   - default,
   - low CFG / guidance scale (or low temperature),
   - high CFG / guidance scale (or high temperature).
4. Paste the three results side by side and describe in two sentences each what changed.

### Conditioning beyond text

1. Generate an image you like.
2. Use the same tool's **image-to-image** mode (or *style reference*) to generate a *variation* with the same overall composition.
3. Write down how strict the conditioning was — what is preserved, what changes?

### Optional code track: sampling from a tiny language model

Open a notebook. Install the `transformers` library if it is not already installed and try:

```python
from transformers import pipeline
gen = pipeline("text-generation", model="gpt2")
for t in [0.2, 0.7, 1.2]:
    out = gen("Once upon a time in Oslo,", max_new_tokens=40, temperature=t, do_sample=True)
    print(f"--- t={t} ---")
    print(out[0]["generated_text"])
```

GPT-2 is small and quaint by 2026 standards but illustrates the temperature knob nicely.

---

## Reflection prompts

1. Describe in plain language the difference between *learning a distribution* and *learning a boundary*. Why does that matter for creative work?
2. Tools like Midjourney expose only a few sampler parameters; tools like ComfyUI expose dozens. Whom does each design serve?
3. The same model, same prompt, two clicks: two different images. Is this a feature or a bug for your use case?

---

## Going further

- Lilian Weng, [What are diffusion models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) — a careful, illustrated technical introduction
- Andrej Karpathy, [The unreasonable effectiveness of recurrent neural networks](https://karpathy.github.io/2015/05/21/rnn-effectiveness/) — old but a beautifully written introduction to "next-token" generation
- [Hugging Face — diffusers documentation](https://huggingface.co/docs/diffusers/index)
"""


CH4 = r"""---
title: "4. AI and language"
subtitle: "Writing, dialogue, and large language models"
description: "How large language models actually work, how prompting works in practice, and how to use them as a writing and thinking tool — including their failure modes."
---

---

## Why this matters

Of all the generative tools we will meet, **large language models (LLMs)** are the ones most students already use every day. They draft emails, summarise readings, fix code, explain concepts, brainstorm, translate, and *help you cheat on assignments*. (We will talk about that last one.)

This chapter is about what is actually happening when you type into ChatGPT, Claude, Gemini, Mistral, or a local model. It is also about how to **use them well** as a tool for writing and thinking — and how to spot when they are quietly making things up.

---

## What is a language model?

A language model is a system trained to **predict the next word** (technically: the next **token**) given the previous words. That is it.

Given the input "*The capital of Norway is*", the model assigns a probability to every possible next token. The probability of "Oslo" should be high; the probability of "purple" should be low.

To **generate** text, the model samples the next token, appends it to the input, and repeats:

> The capital of Norway is ☐ → Oslo
> The capital of Norway is Oslo ☐ → .
> The capital of Norway is Oslo. ☐ → It

This is the same loop whether the model has 1 million parameters or 1 trillion. Modern LLMs are scaled-up versions of GPT-style models from 2018–2020 [@Brown2020GPT3], built on the *transformer* architecture [@Vaswani2017].

```{important}
A language model is a **next-token predictor**. Everything else — chatting, coding, reasoning, refusing to answer — is built on top of that single trick.
```

### Tokens, not words

The model does not see words; it sees **tokens**. A token is usually a piece of a word — common words become one token, rare words become several. "Oslo" might be one token; "Jensenius" might be three. You can play with this in the [OpenAI tokenizer](https://platform.openai.com/tokenizer) or [tiktokenizer](https://tiktokenizer.vercel.app/).

Why does this matter?

- **Cost.** Most commercial models bill per token. Long prompts and long answers cost more.
- **Context length.** Each model has a maximum number of tokens it can attend to at once (its **context window**). Outside that window, information is invisible to it.
- **Languages.** Non-English languages often tokenise less efficiently. Norwegian text typically uses more tokens than equivalent English, so it costs more and fits into less context.

### Context, not memory

LLMs have **no persistent memory** between conversations unless a system is built around them to provide it. What they have is a **context window**: a buffer holding the conversation so far (system instructions + user messages + model responses). Anything outside that buffer simply does not exist for the model.

This is why "remember that we are writing a fantasy novel" works inside a chat (it stays in context) but does not transfer to a new chat (the buffer is gone). Tools that *appear* to remember (custom GPTs, ChatGPT memory) achieve this by quietly pasting relevant snippets back into the context.

---

## In-context learning, or "prompting"

A striking discovery in 2020 [@Brown2020GPT3] was that you can teach an LLM new behaviour just by **showing it examples in the prompt** — no retraining. This is called **in-context learning**.

```text
Translate to Norwegian.

EN: The library is open.
NO: Biblioteket er åpent.

EN: Where is the train station?
NO: ☐
```

The model uses the pattern in the prompt to fill in the next answer. This is why **prompting** is now a real skill: you are programming the model with examples, not with code.

Three useful patterns:

- **Zero-shot** — just ask. Works for common tasks the model has seen a lot of.
- **Few-shot** — give 2–6 examples of input/output before your real request.
- **Chain-of-thought** — ask the model to *think step by step* before answering. Often improves reasoning, sometimes at the cost of length.

### A practical prompt template

For non-trivial tasks, this skeleton works well:

```text
ROLE: You are a [role with relevant expertise].

TASK: [What you want done, in one sentence.]

CONSTRAINTS:
- [Length, style, format]
- [What to avoid]
- [Audience]

CONTEXT:
[Any background the model needs.]

OUTPUT:
[The exact shape you want, with placeholders or an example.]
```

This is *not* magic. It is the same template you would write for a freelancer.

---

## The failure modes you need to recognise

LLMs fail in characteristic ways. You will see all of these by week 6.

### Hallucination

The model generates a confident, fluent statement that is **false**. It might invent a paper title, a court case, a quote, or a study. This is not a bug to be patched — it is a direct consequence of the next-token training objective, which rewards plausibility over truth [@Bender2021Parrots].

Mitigations:

- **Ask for sources** and check them. (Beware: the model can also hallucinate sources.)
- **Restrict the task** to the model's strengths (e.g., rewriting, summarising provided text).
- **Provide grounding** — paste the article and ask the model to answer from *it*, not from its weights.

### Sycophancy

The model agrees with you, even when you are wrong. Tell it that 2 + 2 = 5 and confidently insist, and it will often capitulate. This is a side effect of training procedures that reward "helpful" answers.

Mitigations:

- **Don't lead the witness.** Ask "is the following correct?" rather than "I think X is correct, right?"
- **Ask for counterarguments** explicitly.

### Verbosity

The model produces three paragraphs where one sentence is needed. Solution: ask for fewer words. Specify the exact format. Models obey length instructions reasonably well in 2026.

### Style drift

A long generation drifts in tone or style. Solution: regenerate from a fresh prompt every few hundred words.

### Inability to count, sort, multiply

LLMs are not calculators. They will confidently get 17 × 23 wrong. Modern chat products fix this by giving the model access to a code interpreter. If you are doing anything numeric, **make sure the model is running code**, not just generating prose.

### Out-of-date knowledge

Models have a training cutoff. They do not know what happened yesterday unless they have web search. Always check the cutoff if recency matters.

---

## Open vs closed models

You will work with two kinds of LLM this semester:

- **Closed/commercial** — OpenAI, Anthropic, Google, Mistral (some). You access them via a website or API. The weights are not public. They tend to be the most capable.
- **Open-weight** — Llama, Mistral (some), Gemma, Qwen, DeepSeek, etc. You can download the weights and run them yourself, on a laptop or a server. They lag the frontier by 6–18 months but are closing the gap.

Pragmatic guidance:

- For **rapid, high-quality drafts**, use a frontier closed model.
- For **research, reproducibility, sensitive data, or learning**, prefer an open-weight model you can run locally (e.g., via [Ollama](https://ollama.com/) or [LM Studio](https://lmstudio.ai/)).
- For **production**, weigh privacy, cost, latency, and quality.

---

## How to write with an LLM

A working pattern that holds up across disciplines:

1. **Think first.** Make a bullet outline yourself. Do *not* ask the model to brainstorm from scratch — that path leads to bland, average prose.
2. **Use the model to argue with the outline.** "What is missing? What is wrong? What audience would object?"
3. **Draft yourself.** Write a rough version of each section.
4. **Use the model to edit.** "Make this paragraph half as long. Make this sentence clearer. Suggest three alternative openings."
5. **Verify everything claimed as fact** against an original source.
6. **Track your prompts.** Keep them in a file alongside your draft.

You should treat the LLM as a **fast, slightly drunk colleague** — useful, opinionated, sometimes wrong, never to be trusted on anything that matters without a check.

---

## Practice (2 h)

### Prompt library

1. **Pick three writing tasks** from your discipline (a paragraph, an explanation, a critique, a translation, a summary…).
2. For each, build a prompt using the **ROLE / TASK / CONSTRAINTS / CONTEXT / OUTPUT** template above.
3. Run each prompt in two different LLMs (e.g., one commercial, one open-weight via Ollama). Save the outputs.
4. **Compare**: where do the models differ? Which one made which mistakes?

### Hallucination hunt

1. Ask an LLM for **five academic references** on a niche topic in your field (something obscure enough that it might bluff).
2. Try to find each reference. How many actually exist? How many are partially real (real authors, wrong title; real title, wrong year)?
3. Write a short note (200 words) on what you found.

### Optional code track

Use the `openai`, `anthropic`, or `ollama` Python package to call a model from a notebook. Try:

```python
from openai import OpenAI
client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You answer in one sentence."},
        {"role": "user", "content": "What is the etymology of the word 'fjord'?"},
    ],
)
print(resp.choices[0].message.content)
```

(Replace the API key and model name with whatever your institution gives you. UiO has its own [generative AI service](https://www.uio.no/english/services/ai/) for staff and students.)

---

## Reflection prompts

1. How would you tell, in five seconds, that a paragraph in front of you was written by an LLM? Test your heuristic on three short paragraphs (a mix of your own, a model's, and a colleague's) and see how often you are right.
2. The 2024 EU AI Act [@EUAIAct] introduces transparency requirements for "synthetic content". What would meaningful labelling look like for an essay drafted with an LLM?
3. Where, in your own writing process, is the LLM most useful? Where is it actively in the way?

---

## Going further

- Vaswani et al., *Attention Is All You Need* [@Vaswani2017] — the founding paper of the transformer
- Stephen Wolfram, [What is ChatGPT Doing... and Why Does It Work?](https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/) — best intuitive explanation of LLMs
- Hugging Face's [LLM course](https://huggingface.co/learn/llm-course/) — free and code-first
- Bender et al., *On the Dangers of Stochastic Parrots* [@Bender2021Parrots] — the critical take you have to read
- The [UiO AI service guidelines](https://www.uio.no/english/services/ai/) [@UiOAI]
"""


CH5 = r"""---
title: "5. AI and images"
subtitle: "Diffusion models and the new picture-making"
description: "How text-to-image models work, how to control them, and how to fit them into a real image-making practice."
---

---

## Why this matters

Image is the medium where Creative AI announced itself loudest. In 2022, when *Stable Diffusion*, *DALL·E 2*, and *Midjourney* arrived within a few months of each other, they changed picture-making faster than any tool since the smartphone camera. Designers, illustrators, journalists, lawyers, and the rest of us are still working out what that means.

This chapter introduces the technology underneath text-to-image models, the practical vocabulary of using them, and the editorial questions they raise.

---

## How diffusion works (in pictures)

Modern image models are **diffusion models** [@Ho2020Diffusion; @Rombach2022LatentDiffusion]. The idea is simpler than it looks.

```{figure} figures/diffusion.svg
:alt: A simple diagram showing forward diffusion adding noise to an image step by step, and reverse diffusion removing it to recover an image.
:align: center
Forward diffusion (top): start from a real image and progressively add noise. Reverse diffusion (bottom): start from pure noise and let a neural network remove it step by step, conditioned on a text prompt.
```

The training procedure has two halves:

1. **Forward.** Take a real image. Add a tiny bit of noise. Add a tiny bit more. Repeat many times until the image is pure static.
2. **Reverse.** Train a neural network to *undo* one step of noise at a time. Given a noisy image and how noisy it is, predict what was added.

Once trained, you can run the reverse half *from scratch*: start with pure noise, denoise step by step, and a coherent image emerges. With **conditioning** (chapter [3](generative-ai.ipynb)), you can steer that emergence — most commonly with a text prompt, embedded by a model like CLIP [@Radford2021CLIP] and injected at every step.

A few practical consequences:

- The model can be reused for **image-to-image** by starting from a *partially noisy* version of an existing image. Less noise = more faithfulness to the input.
- The model can be reused for **inpainting** by only denoising the masked region.
- The model can be reused for **outpainting** by treating the canvas extension as a masked region.
- The number of **steps** trades quality for time. Many modern models can produce good results in 4–8 steps using distilled samplers.

Latent diffusion [@Rombach2022LatentDiffusion] adds a key efficiency trick: the diffusion does not happen in pixel space (millions of numbers per image) but in a compressed *latent* space (thousands of numbers). This is why models can run on a consumer laptop.

The most recent generation of image models (e.g. SD3, FLUX) uses **flow matching** or **rectified flows** rather than vanilla diffusion [@Esser2024SD3]. The intuition stays the same.

---

## The vocabulary of text-to-image

When you use a text-to-image tool you will meet a small set of knobs.

- **Prompt** — what you want.
- **Negative prompt** — what you *don't* want. Often more powerful than people expect.
- **Aspect ratio** — 1:1, 16:9, 9:16, 2:3, 3:2. Some compositions look fine in landscape and break in square.
- **CFG scale / guidance** — how strictly the model should obey the prompt. 5–9 is typical. Higher = more literal but oversaturated; lower = looser and more varied.
- **Steps** — number of denoising steps. 20–50 is typical for high quality; 4–8 for fast distilled models.
- **Seed** — the random seed for the noise. Same prompt + same seed = same image (within one model). Useful for iterating with a controlled variable.
- **Sampler / scheduler** — the algorithm that performs the denoising (Euler, DPM++, etc.). Affects style and convergence.
- **Style / reference image** — an extra conditioning input.

A simple discipline: **change one knob at a time**. If you change the prompt *and* the seed *and* the CFG, you cannot tell what caused the change in output.

---

## Prompting for images

Image prompts are *not* the same as language prompts. A working pattern is:

```text
[Subject] | [composition] | [style] | [medium] | [lighting] | [mood] | [extra refs]
```

A worked example:

```text
A wooden rowing boat moored at a fjord pier, viewed from a low angle,
black-and-white film photograph, soft early morning light, 50 mm,
nostalgic, in the style of late 20th-century Scandinavian photography
```

Some practical tips:

- **Be concrete about the subject** before you reach for style. "A car" is vague; "a 1972 Volvo Amazon parked in front of a yellow wooden house" is something the model can grip.
- **Style words matter.** Material ("oil painting", "pen drawing"), medium ("photograph", "render"), and period ("1970s", "Renaissance") all do work.
- **Avoid contradictions.** "Photo-realistic illustration in watercolour" tells the model to choose between three things it cannot do at once.
- **Iterate on what is wrong**, not on the whole prompt. If the lighting is off, change only the lighting words.

### Negative prompts

For models that support them, negative prompts are where you stop the failure modes you keep seeing: `blurry, extra fingers, watermark, low quality, deformed face`. Treat the negative prompt as a curated list, not a brain dump.

### Reference images and ControlNet

If words run out, **show**. Most modern tools accept:

- a **style reference** — make it look like this,
- a **structural reference** — match this composition,
- a **pose reference** — use this pose,
- a **depth or edge map** — preserve this geometry.

The open-source community calls these *ControlNets* and stacks them freely; commercial products call them *style reference* or *character reference*.

This is where image generation stops being a slot machine and starts being a controllable creative tool.

---

## Editing instead of generating

A common, often more useful workflow is **image editing**:

- **Inpainting**: mask a region, replace it with something else. "Replace the bottle in his hand with a coffee cup."
- **Outpainting**: extend the canvas. "Add another metre of beach to the left."
- **Variation**: same subject, slightly different.
- **Upscaling**: increase resolution while sharpening detail.
- **Removing/adding** specific objects with a single click.

You will get further with editing than with pure prompting for most professional jobs.

---

## Where image models still struggle

- **Hands, feet, text in pictures, jewellery, complicated logos.**
- **Faithful portraits of specific people** — generally restricted by the major commercial tools.
- **Multi-step composition.** "A man holds a cat with one hand and points at a sign that says 'Open' with the other" is at the edge of what current models can compose reliably.
- **Symbolic content.** Tools struggle to put accurate text into images. (Improving — but not solved.)
- **Diagrams and infographics.** Image models can mimic the *look* of an infographic but rarely produce accurate data.
- **Consistency across a series.** Two pictures of "the same character" tend to drift. Solutions: character reference images, LoRA fine-tunes, image-to-image with seed locking.

---

## Practice (2 h)

### A controlled experiment

1. Write **one base prompt** with a clear subject, composition, and style.
2. Generate the image four times, each time changing **exactly one variable**:
   - same prompt, same seed, four different aspect ratios;
   - same prompt, same seed, four different CFG values (3, 6, 9, 12);
   - same prompt, four different seeds;
   - prompt unchanged except for the lighting words.
3. Lay out the four grids in a single image (Canva, Figma, an empty markdown cell — anything). Caption each.
4. Pick the *one* knob that mattered most for your subject. Write a short note on why.

### Image-to-image

1. Take a photograph (or screenshot) you have rights to.
2. Run it through an **image-to-image** pipeline with three different *denoise strengths* (0.3, 0.5, 0.8).
3. Note where you sit on the *fidelity ↔ freedom* axis.

### Optional code track

If you have a Hugging Face account, the [`diffusers` library](https://huggingface.co/docs/diffusers/index) lets you generate images locally:

```python
import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float16,
).to("cuda")  # or "mps" on Mac, or "cpu"

img = pipe("a wooden rowing boat at sunrise on a fjord, watercolour",
           num_inference_steps=4, guidance_scale=1.0).images[0]
img.save("boat.png")
```

---

## Reflection prompts

1. Compare an AI-generated image of "a typical Norwegian street" with a real photograph. What is the model *averaging away*?
2. What changes when image-making moves from "ten minutes for a sketch" to "ten seconds for a finished-looking picture"? Who benefits, who loses?
3. Pick a single image you generated this week. Write a 100-word caption that *honestly* describes how it was made — the tool, the prompt, the iterations, the edits.

---

## Going further

- Rombach et al., *Latent Diffusion Models* [@Rombach2022LatentDiffusion] — the founding paper of Stable Diffusion
- Esser et al., *Scaling Rectified Flow Transformers* [@Esser2024SD3] — the SD3 paper
- The [Hugging Face Diffusers documentation](https://huggingface.co/docs/diffusers/index)
- Lev Manovich, *AI Aesthetics* [@Manovich2018] — short essays on what AI image-making *looks like*
- For the legal side: cases from [Andersen v. Stability AI](https://en.wikipedia.org/wiki/Andersen_v._Stability_AI) and the [Getty Images v. Stability AI](https://en.wikipedia.org/wiki/Getty_Images_v._Stability_AI) suits
"""


CH6 = r"""---
title: "6. AI and sound"
subtitle: "Speech, music, and sound design with generative audio models"
description: "From text-to-speech to text-to-song: how generative audio models work, what they can already do, and how they fit into a sound-making practice."
---

---

## Why this matters

Sound used to be the laggard medium for generative AI. Images and text arrived in 2022; high-quality audio took another year or two to catch up. By 2024 we had usable text-to-music systems and convincing voice cloning; by 2026 these are everywhere from podcast workflows to film production to *Eurovision*. This week we look at what these systems can actually do, and where they still fail.

The audio chapter is also where the question of **consent** becomes most personal: voices are tied to bodies, and audio cloning of a real person can be used to harm.

---

## Three quick families of audio AI

You will meet at least three quite different things under the umbrella of "AI and sound":

1. **Text-to-speech (TTS) and voice cloning.** Synthetic voices reading text. Quality has been transformed by neural vocoders and now by transformer-based systems. Tools: ElevenLabs, Resemble, OpenAI TTS, Microsoft VALL-E, Norwegian-language efforts like [the National Library's NB-Whisper](https://huggingface.co/NbAiLab/nb-whisper-large) on the recognition side.
2. **Music generation.** Systems that produce full pieces of music from text prompts. Tools: Suno, Udio, Stable Audio, MusicLM in research form [@Agostinelli2023MusicLM].
3. **Sound effects and design.** Generative SFX for film/game pipelines: footsteps on different surfaces, ambient atmospheres, Foley.

Underneath all of them sit the same core ideas as image generation: a model trained on huge amounts of audio learns to predict, and at inference time produces, audio that resembles its training distribution.

```{figure} figures/spectrogram.svg
:alt: A schematic spectrogram with frequency on the y-axis and time on the x-axis.
:align: center
A spectrogram represents sound as an image (time on x, frequency on y). Many audio models treat sound generation as image generation on a spectrogram.
```

---

## How models represent sound

Computers store sound as a sequence of numbers — typically 44 100 or 48 000 of them per second per channel. That is a lot. Generating sound directly *sample by sample* (as the first WaveNet model did in 2016) was beautiful but slow.

Modern audio models almost always work on a **compressed representation**:

- A **spectrogram** — a 2D image of the sound (time × frequency). Treat it as an image, diffuse over it, then convert back to audio with a *vocoder*.
- A **discrete code** from a *neural audio codec* (like EnCodec, SoundStream, DAC). The model produces a short sequence of codes; the codec decodes them back to audio.

Both approaches make the problem 50–100× smaller than working on raw samples. This is why your laptop can now produce a song in seconds.

The architectural backbone is again usually a **transformer** [@Vaswani2017], adapted to handle the very long sequences that audio implies. Diffusion models on spectrograms or codec tokens are common [@Agostinelli2023MusicLM].

---

## Text-to-speech and voice cloning

A modern TTS system takes:

- A piece of **text** (or phonemes), and
- a **speaker embedding** describing the desired voice, possibly extracted from a short reference recording (5–30 seconds is often enough),

and produces a waveform.

What works well in 2026:

- **Convincing prosody** in English and most major European languages, including Norwegian (with the right model).
- **Cloning a specific voice** from a short reference. *Worryingly well.*
- **Emotion and style control** via prompts ("sad, slow"), tags, or a reference clip.
- **Multilingual speakers** — one voice speaking many languages without re-recording.

What still struggles:

- **Long context coherence** — a 20-minute audiobook can drift in tone.
- **Sung speech / song-speech mixes** in TTS engines (separate music systems do better).
- **Code-switching mid-sentence**, especially with code or technical terms.
- **Low-resource languages** — Sami, Faroese, many African and Asian languages still get poor results.

### A note on consent

You can clone a voice in two minutes from a YouTube clip. This is a fact, not a recommendation. **Cloning a real person's voice without their consent is harmful and, increasingly, illegal** — for fraud, for harassment, for impersonation. Treat voice cloning as you would treat using somebody's face: with explicit permission, attribution where appropriate, and a clear use case.

The EU AI Act [@EUAIAct] places certain forms of deepfake audio in the higher-risk categories with transparency obligations.

---

## Music generation

Music generation is harder than speech because:

- The structure is **longer-range** — verses, choruses, build-ups, drops.
- The judgement is **aesthetic** — wrong notes are not "wrong" in the same way as wrong words.
- The **training data is contested** — music is heavily copyrighted; using it for training has triggered lawsuits.

Despite all that, by 2026 tools like *Suno* and *Udio* will reliably produce 2–3 minute songs from a paragraph of prompt. Stems can often be separated for further editing in a DAW.

Useful prompt elements for music models:

- **Genre and era**: "1970s funk", "Norwegian black metal", "modern indie folk".
- **Instrumentation**: "fingerpicked acoustic guitar, brushed snare, double bass".
- **Tempo and feel**: "BPM 110, swung eighths, intimate, late night".
- **Lyrics**, when supported, in their own field with `[Verse]`/`[Chorus]` tags.

What still fails:

- **Specific quotation of existing pieces.** Asking for "in the style of Taylor Swift" raises legal and ethical alarms and is often blocked.
- **Coherent lyrics** in languages other than English. Norwegian-language music output is improving but uneven.
- **Structural sophistication** beyond pop forms — fugues, multi-section classical works, free-jazz dialogues.

---

## Sound design and Foley

Beyond speech and music sits a quieter category: **sound design**. Models that produce 5–15 seconds of "rain on a tin roof", "wooden cart on cobblestones", or "alien ambience" are reshaping film, game, and podcast workflows. Tools include [ElevenLabs sound effects](https://elevenlabs.io/sound-effects), Stable Audio, AudioGen, and various open-source efforts.

This category is *the* unsung workhorse: less spectacular than song generation, less morally fraught than voice cloning, often the most immediately useful in production.

---

## Where sound AI fits in a real workflow

Three observations:

1. **AI is rarely the whole pipeline.** Generated audio gets imported into a DAW (Reaper, Ableton, Logic, Reason). It is layered, EQ-ed, mixed, and sometimes re-recorded.
2. **Stem separation has improved dramatically.** Tools like [Demucs](https://github.com/facebookresearch/demucs) and commercial offerings let you split a song into vocals, drums, bass, and other. This makes AI generation useful even when you cannot get clean stems out of it.
3. **Speech-to-text is the silent revolution.** OpenAI's Whisper [and its Norwegian variant](https://huggingface.co/NbAiLab/nb-whisper-large) made transcription nearly free. Researchers, journalists, and podcasters use it daily. We will use it in the practice session.

---

## Practice (2 h)

### Part 1 — Transcribe and remix a short clip (60 min)

1. Record (or pick) a 30–60 second voice clip with your permission to use.
2. Transcribe it with [Whisper](https://huggingface.co/openai/whisper-large-v3) (via the web, via a local install, or via a service).
3. Generate a **new voice** reading the same text in a TTS tool.
4. Compare the two side by side. What did the AI catch? What did it miss? What does the synthetic voice add or remove?

### Part 2 — Build a 30-second piece (60 min)

1. Pick a small brief: "background music for a UiO research lab promo video, 30 seconds".
2. Generate a song in a music tool. Iterate prompts until you have something usable.
3. Generate a separate ambient sound effect bed.
4. Mix the two (any DAW; even Audacity works).
5. Document: tools, prompts, edits, time taken.

### Optional code track

Install `openai-whisper` or `nb-whisper` locally:

```bash
pip install openai-whisper
whisper my-clip.mp3 --model small --language Norwegian
```

For audio generation, the [`audiocraft`](https://github.com/facebookresearch/audiocraft) library by Meta lets you run MusicGen locally on a moderate GPU.

---

## Reflection prompts

1. Voice cloning is now essentially a free service. What changes for journalism? For political ads? For your own digital footprint?
2. Listen carefully to a generated 30-second clip. What gives it away? What does *not* give it away? Are you sure?
3. Music generation models were trained on existing music. Imagine you are a working musician — how do you feel about that? Imagine you are a film composer working on a small project — how does that change your answer?

---

## Going further

- Engel et al., *Neural Audio Synthesis of Musical Notes with WaveNet Autoencoders* [@Engel2017NSynth] — early but influential paper from Google's Magenta team
- Agostinelli et al., *MusicLM: Generating Music From Text* [@Agostinelli2023MusicLM] — research paper from Google
- Holly Herndon, the [Spawning Coalition](https://spawning.ai/), and the wider movement around **opting voices and likeness out** of training datasets
- The [NB-Whisper](https://huggingface.co/NbAiLab/nb-whisper-large) project at the National Library of Norway — a great example of a low-resource-language AI effort
"""


CH7 = r"""---
title: "7. AI and video"
subtitle: "Text-to-video, image-to-video, and the time problem"
description: "Why video took longer to arrive in generative AI than images, what current systems can do, and how they fit into a real production pipeline."
---

---

## Why this matters

Image, text, and audio are all easier than **video**. A video is just a sequence of frames, but generating a sequence of frames that are *consistent over time* — same character, same lighting, same physics — is dramatically harder than generating any single frame.

By 2024 the first credible text-to-video systems arrived (Sora, Veo, Runway Gen-3, Kling, Pika, Luma). By 2026 they are good enough to do short cinematic clips, ad inserts, music videos, and B-roll for documentary work. They are still not good enough for sustained narrative film. This chapter looks at what is possible now and what is just over the horizon.

---

## Why video is hard

Three problems compound:

1. **Cost.** A 5-second clip at 30 fps is 150 frames. Even at compressed latent resolution, that is 100× the inference cost of a single image.
2. **Consistency.** Each frame must be coherent with the previous one — same character, same scene, same lighting. This requires the model to "remember" what it just drew.
3. **Physics.** Cloth has to fall, water has to flow, hands have to grip. Image models can fake plausible physics in one frame; video models have to fake *trajectories*.

```{figure} figures/video.svg
:alt: A schematic showing a stack of video frames over a time axis, with arrows showing temporal consistency requirements.
:align: center
The hard part of video is not the frames; it is the time axis between them.
```

Modern video models use one of three strategies:

- **Frame-by-frame with attention across frames.** Each frame "sees" the others through cross-attention.
- **3D diffusion** (space × space × time). Treat the whole clip as a single tensor; diffuse all at once. Conceptually clean, computationally expensive.
- **Two-stage**: first generate keyframes, then *interpolate* the frames in between using a separate, lighter model.

By 2026 the best public systems use combinations of all three.

---

## What current video models can do

In 2026, off-the-shelf tools (Sora, Runway, Veo, Kling, Pika, Luma) reliably produce:

- **5–15 second clips** at 720p or 1080p.
- **Photorealistic or stylised** output based on prompts.
- **Camera motion control** — orbit, dolly, push, pull, hand-held.
- **Image-to-video** — take a still and animate it.
- **Keyframe-to-keyframe** — first frame + last frame → in-between motion.
- **Lip-sync** — drive a static face image with an audio file.
- **Style transfer** across an existing clip.

They struggle with:

- **Longer clips.** Coherence falls off rapidly past 10–20 seconds.
- **Specific people and IPs.** Most commercial tools refuse explicit requests for real people, brands, or copyrighted characters.
- **Crowds and complex interactions.** Two people having a conversation is at the edge of reliable.
- **Hands, text, and small details.** Same as image models, but in motion.
- **Reading printed text** on signs and screens within a clip.

---

## The vocabulary of video prompting

Video prompts are richer than image prompts because they include motion. A working template:

```text
[Subject + key features],
[scene / setting],
[camera angle and movement],
[lighting and time of day],
[style],
[motion within the scene]
```

Worked example:

```text
A young woman walking quickly along the riverbank in Oslo,
autumn leaves on the ground, river to the left,
medium-wide shot from a hand-held camera following her from behind,
overcast late-afternoon light,
documentary style,
she pulls a beanie out of her pocket and puts it on as she walks
```

Useful concepts:

- **Camera moves**: *dolly in*, *truck left*, *crane up*, *orbit*, *push in*, *static*.
- **Motion**: do not assume "looking sad" → "starts to cry". Spell out the motion in time.
- **Cuts**: most current systems generate a single shot. For multi-shot sequences you stitch in a video editor.
- **Aspect ratio**: 16:9 for landscape work; 9:16 for vertical (TikTok / Reels / Shorts).

---

## Workflow: where video AI actually fits

A realistic production workflow in 2026:

1. **Storyboard** in image-AI (chapter [5](ai-images.ipynb)) until you have a frame you like for each shot.
2. **Animate** each frame with image-to-video, possibly with end-frame conditioning.
3. **Stitch** the shots in a video editor (DaVinci Resolve is free; CapCut, Premiere, Final Cut work too).
4. **Add audio** — voice (chapter [6](ai-sound.ipynb)), music (chapter [6](ai-sound.ipynb)), Foley, ambience.
5. **Colour-grade and finish** in the same editor.

The pieces of this pipeline that are most transformed by AI are the *first* and the *second*. The traditional editorial work (pacing, sound design, colour) remains very human.

```{tip}
Plan the **last frame** at the same time as the first. End-frame conditioning is often what separates "magic clip" from "useful clip".
```

---

## Lip-sync and avatars

A specific genre of video AI worth flagging: **talking heads**. Tools like HeyGen, Synthesia, D-ID, and many others let you upload (or pick from a stock library) a photograph or short clip of a person and drive it with a TTS voice. The output is a video of "that" person reading any text.

This is widely used for:

- corporate training videos,
- product explainers,
- multilingual versions of recorded talks,
- localised marketing.

It is also a perfect tool for political and personal manipulation. As with voice cloning (chapter [6](ai-sound.ipynb)): **explicit consent and clear labelling are non-negotiable**.

---

## A short word on cost and access

Video generation is still the most computationally expensive medium per second of output. As of 2026:

- A 5-second 720p clip uses roughly the same compute as 100 image generations.
- Most consumer tools price video in **credits**; one clip costs 5–20 credits depending on length and quality.
- Free tiers are very limited; the cheaper paid plans (around USD/EUR 10–20 per month) tend to be the right starting point for a course.

If your laptop has 16 GB of RAM and no dedicated GPU, do video work in a hosted tool. Local video generation is for workstations with serious GPUs.

---

## Practice (2 h)

### A 10-second clip from a single image

1. Generate a strong **still image** (chapter [5](ai-images.ipynb)) of a clear subject in a clear scene.
2. In a video tool of your choice, run **image-to-video** with a short motion prompt — e.g., "*the subject turns their head slowly to the right while the camera pushes in*".
3. Generate three variations. Pick the best.
4. Optional: generate an **end-frame** and re-run with both first and last frame conditioned.

### A 30-second mini-piece

1. Storyboard **three shots** of a small idea — for example, "a tourist arriving in Oslo at sunrise".
2. Generate each shot (3–5 seconds each).
3. Add an ambient soundtrack from chapter [6](ai-sound.ipynb).
4. Edit the three shots together in a video editor.
5. Watch it twice. Write down what works, what does not, and what you would re-do.

### Critique

Pair up with another student. Each of you watches the other's 30-second piece silently, then writes:

- One thing the AI clearly produced well.
- One thing that gives it away as AI.
- One thing that would be the next step.

---

## Reflection prompts

1. What kinds of moving-image work are easiest for current video AI? Which kinds remain stubbornly out of reach?
2. Watch one AI-generated short film online (search for "AI short film 2026"). Pause every two seconds. Where does coherence break down? Where does it hold?
3. Imagine a journalist using AI video for a news report. List three legitimate uses and three uses that would constitute serious misuse. What is the difference?

---

## Going further

- [The Runway research blog](https://runwayml.com/research) — readable updates on video model development
- [OpenAI Sora system card](https://openai.com/sora) — useful for understanding what one major company commits to and refuses
- *Tracking Generative Video* (Stanford HAI) — annual surveys of capabilities and limits
- For ethics: documentation around the [EU AI Act's deepfake provisions](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) [@EUAIAct]
"""


CH8 = r"""---
title: "8. Creative coding with AI"
subtitle: "Pair programming and generative graphics"
description: "How AI changes programming — both as a tool for learning to code, and as a medium for creative work in code itself."
---

---

## Why this matters

Programming is the discipline that AI has changed first and fastest. Even students with no programming background can now write working code by describing what they want in plain English. For *creative* coding — graphics, sound, generative art, interactive installations — the change is doubled: the model helps you write the code *and* generates the content.

This chapter is for everyone, programmers or not. We use programming as a creative medium and as a way to understand what is going on inside the tools we have been using.

---

## AI coding assistants in 2026

By 2026 most professional development is done with an AI assistant in the editor. The dominant patterns are:

- **Tab-complete** — the assistant suggests the next line or block as you type. Originated with GitHub Copilot in 2021.
- **Chat in the editor** — a sidebar that can see your code and respond in plain language. Tools: [Cursor](https://cursor.com/), [Windsurf](https://windsurf.com/), VS Code with Copilot Chat.
- **Inline edit** — select code, press a shortcut, describe the change.
- **Agentic** — describe a task, the assistant plans, edits multiple files, runs the code, fixes errors, and reports back. Tools: [Claude Code](https://www.anthropic.com/claude-code), [Codex CLI](https://github.com/openai/codex), Cursor's agent mode.

For a beginner the most useful pattern is **chat in the editor** with **explain**, **fix**, and **refactor** commands. You write a draft (or paste an example), the assistant explains, you ask for changes, you iterate.

```{important}
The assistant is fastest when you can read code. You do not need to write it from scratch.
```

We teach you to **read** code more than to **write** it. Reading is what lets you supervise an AI.

---

## A worked example: p5.js + an assistant

[p5.js](https://p5js.org/) is a JavaScript library descended from Processing, designed for visual sketches. You can use it directly in your browser at the [p5.js Web Editor](https://editor.p5js.org/) without installing anything.

A canonical "hello world" sketch:

```javascript
function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(20);
  noStroke();
  fill(255);
  circle(mouseX, mouseY, 40);
}
```

A useful prompt to an AI assistant, even if you have never seen JavaScript before:

> "Modify this p5.js sketch so that instead of a single circle, twenty circles follow the mouse with a trailing delay, and their colour cycles through hues over time."

A solid assistant will produce something like:

```javascript
let circles = [];
const N = 20;

function setup() {
  createCanvas(400, 400);
  colorMode(HSB, 360, 100, 100, 1);
  for (let i = 0; i < N; i++) circles.push({ x: 200, y: 200 });
}

function draw() {
  background(20);
  noStroke();
  for (let i = N - 1; i > 0; i--) {
    circles[i].x = circles[i - 1].x;
    circles[i].y = circles[i - 1].y;
  }
  circles[0].x = mouseX;
  circles[0].y = mouseY;

  for (let i = 0; i < N; i++) {
    fill((frameCount + i * 18) % 360, 70, 90);
    circle(circles[i].x, circles[i].y, 40 - i * 1.5);
  }
}
```

Run it; play with it; ask the assistant to "make the trail spring instead of linear", "add a glow effect", "double the number of circles", "make it react to audio input". The whole loop is *show me, tweak, repeat*.

---

## How to talk to a coding assistant

Some habits that pay off:

- **Tell it what kind of code you want.** "Vanilla JavaScript, no frameworks." "Python with `numpy`." "p5.js running in the browser." Without that, the assistant defaults to whatever was most common in its training data.
- **Show it the smallest possible failing example.** Don't paste the whole project.
- **Ask for explanations.** "Explain this function line by line as if I have never seen JavaScript."
- **Ask for tests.** "Write three small tests for this function." Helps catch the mistakes the assistant cannot see.
- **Re-anchor often.** Long conversations drift. Start a new chat for a new task.
- **Verify by running the code.** The model is wrong more often in code than in prose — but it is also instantly checkable.

---

## Generative graphics, sound, and interactivity

Beyond *writing* code, AI can also *generate* the assets that code uses:

- **Sprites and characters** for a game (chapter [9](ai-3d-games.ipynb)).
- **Backgrounds and skies** for an interactive piece.
- **Sound effects** for buttons and events (chapter [6](ai-sound.ipynb)).
- **Voices** for NPCs and tutorials.

A common pipeline:

1. Sketch the idea on paper.
2. Generate placeholder assets with image and audio tools.
3. Wire them together in code with an AI assistant.
4. Iterate on each piece.

This is the modern equivalent of cardboard-prototyping a board game — fast, scrappy, generative.

---

## Building a tiny AI-powered web tool

By chapter 8 you should be able to build something like:

- a web page where the user types a sentence and a generated image appears,
- a sketch that listens to the microphone and reacts in colour,
- a button that produces an AI-generated story riff,
- a small dashboard that classifies your selected files into categories using a local model.

A clean stack for prototyping in 2026:

- **Frontend**: HTML + a single JavaScript file, often using [Vite](https://vitejs.dev/) or [Bun](https://bun.com/).
- **Model calls**: either browser-side using transformers.js or [WebLLM](https://webllm.mlc.ai/), or backend-side via an API call.
- **Hosting**: [Vercel](https://vercel.com/), [Netlify](https://www.netlify.com/), [Hugging Face Spaces](https://huggingface.co/spaces).

All of this can be assembled with an AI assistant in an afternoon.

---

## Practice (2 h)

### Build a sketch with an AI assistant

1. Open the [p5.js Web Editor](https://editor.p5js.org/).
2. With your AI assistant of choice, build a **mouse-reactive sketch** that meets at least two of:
   - colour changes with position or speed,
   - shapes leave trails or echoes,
   - sound plays on click,
   - the canvas is responsive to window size.
3. Iterate at least three times: ask for changes, run, ask for more.
4. Save the sketch publicly and put the link in your weekly log.

### Read code you did not write

Take the assistant's longest function and **explain it back** in your own words — in your log, line by line. (Use the assistant to check your explanation.) This habit is the most important coding skill in 2026.

### Optional advanced track: a generative pipeline

Combine:

- an image model (chapter [5](ai-images.ipynb)),
- an audio model (chapter [6](ai-sound.ipynb)),
- a tiny script that wires them together.

For example: generate four images of "*a forest in different seasons*" and a 20-second ambient track for each. Display all four with their soundscapes on a simple HTML page.

---

## Reflection prompts

1. The assistant suggested a function. You ran it. It worked. Five minutes later you cannot remember what it does. What does that mean for your skill, and for the long-term reliability of your project?
2. What are three things a coding assistant is *worse* at than a beginner? (Hint: novelty, debugging across abstraction, judging which library to use.)
3. Find one bug the assistant introduced in your sketch. How would you have found it without the assistant?

---

## Going further

- [The p5.js learning materials](https://p5js.org/learn/) — beautifully designed, free
- Daniel Shiffman's [The Nature of Code](https://natureofcode.com/) — free book on generative graphics
- [Cursor's docs](https://cursor.com/docs) and Claude Code's [getting-started guide](https://docs.anthropic.com/claude-code) for AI-assisted programming
- Casey Reas et al., [*A Brief History of Generative Music*](https://github.com/CodingTrain) lectures (YouTube)
- [Hugging Face Spaces](https://huggingface.co/spaces) — to see what one-page AI demos look like
"""


CH9 = r"""---
title: "9. AI for 3D, design, and games"
subtitle: "Generative pipelines for spatial and interactive media"
description: "A working tour of generative AI in 3D capture, mesh generation, character design, UI/UX, and game pipelines."
---

---

## Why this matters

The first wave of generative AI was 2D: text, images, audio. The second wave is **spatial**: 3D meshes, point clouds, Gaussian splats, full scenes, characters, animations, levels, interfaces. Spatial creative work — game design, product design, architecture, museum exhibits, AR/VR — is being transformed at the same pace text was transformed in 2022.

This week we look at where AI fits into 3D and design pipelines, and what its strengths and weaknesses are when shape and space — not just colour and word — are the medium.

---

## Three kinds of "3D AI"

You will meet three quite different things:

### 1. 3D capture from real scenes

The classic problem: take a few photos or a video of an object or a place; produce a digital 3D model.

- **NeRFs (Neural Radiance Fields)** — train a small neural network on multi-view photos to render any new view. Pioneered in 2020.
- **Gaussian splats (3D Gaussian Splatting)** — a 2023 technique that represents scenes as millions of tiny 3D Gaussians. Renders fast, looks photorealistic. Now the dominant *capture* technology.
- **Photogrammetry + AI denoising** — a more traditional pipeline, accelerated and improved by AI.

Tools: [Luma AI](https://lumalabs.ai/), [Polycam](https://poly.cam/), [Postshot](https://www.jawset.com/), [Scaniverse](https://scaniverse.com/).

What works well in 2026: outdoor scenes, statues, rooms, products. What does not: reflective surfaces, hair, dynamic scenes, transparent objects.

### 2. Generative 3D from scratch

Text-to-3D and image-to-3D pipelines. Tools: [Meshy](https://www.meshy.ai/), [Tripo3D](https://www.tripo3d.ai/), [Rodin](https://hyper3d.ai/), and many research models on Hugging Face.

What works well: cartoonish objects, props, mid-poly assets for games. What does not: clean topology (game-ready quad meshes), rigged characters, large coherent scenes.

### 3. Generative texture and material AI

Even when the *geometry* is hand-made, AI can produce:

- **Textures** — diffuse, normal, roughness maps from a text prompt or photo.
- **PBR materials** — for game engines.
- **Lighting and HDRIs** — environment maps for realistic rendering.

Tools: [Polycam Textures](https://poly.cam/textures), [Substance 3D](https://www.adobe.com/products/substance3d.html) (with AI features), [Layer](https://www.layer.ai/) for game art.

---

## AI in design (2D and UX)

Outside of game and 3D contexts, "design" is now an AI-saturated discipline:

- **Layout drafts** — Figma's AI features, [Galileo](https://www.usegalileo.ai/), Recraft.
- **Icon generation** — described in words, produced in vector.
- **UI text** — microcopy, error messages, onboarding flows.
- **Brand boards** — Midjourney moodboards, Recraft brand kits.
- **Photo retouching** — Photoshop's generative fill is now a standard tool.

The shift is from "AI generates a finished asset" to "AI is in every menu". A design student in 2026 should expect every tool in their stack — Figma, Adobe Suite, Sketch, Canva — to have AI built in. The interesting questions are no longer about *whether* to use AI but about *which decisions to keep human*.

---

## AI in game development

Game development is a useful microcosm because it touches all of the above plus interactive behaviour.

A modern indie pipeline in 2026 might use:

- **Concept art** — generated with image models (chapter [5](ai-images.ipynb)).
- **2D sprites and tilesets** — generated and refined with [Scenario](https://www.scenario.com/) or similar.
- **3D assets** — generated meshes, hand-retopologised, textured with AI material tools.
- **Voice acting** — synthetic, often with permission to use a specific voice actor's clone.
- **Background music and ambient stems** — generated.
- **Sound effects** — generated.
- **Procedural levels** — sometimes AI-assisted, more often classical procedural generation with AI tweaks.
- **In-game NPC dialogue** — increasingly powered by small local LLMs.
- **Playtesting** — automated, with AI agents exploring builds.
- **Localisation** — LLM-translated, human-reviewed.

You can ship a real, polished game in 2026 with two people and a year of work. The bottleneck has shifted from production to *taste*.

---

## Where 3D AI still struggles

- **Clean topology.** Generated meshes are almost always "potato-mesh" — fine for distant props, useless for animated characters without manual retopology.
- **Multi-object scenes.** A single object: easy. A whole room with proper relationships: hard.
- **Articulated motion.** Rigged characters animating well are not yet a solved problem.
- **Editability.** Once generated, a 3D model is harder to *edit precisely* than a 2D image. Stretching a leg, tweaking a curve, fixing an intersection — these are still mostly manual.

The trajectory is clear, but the gap to professional-grade 3D production is wider than the gap to professional-grade 2D was in 2022.

---

## Practice (2 h)

### Path A — Gaussian splatting (no code)

1. Take 50–100 photos of an object (a plant, a sculpture, a piece of furniture) from many angles.
2. Upload to [Luma AI](https://lumalabs.ai/) or [Polycam](https://poly.cam/) and let it process the splat.
3. Explore the resulting scene. Take screenshots from three angles.
4. Identify three failures of the capture and explain what caused them.

### Path B — Text-to-3D + scene

1. Generate a 3D asset in [Meshy](https://www.meshy.ai/) or similar.
2. Import into [Blender](https://www.blender.org/) (free).
3. Place it in a small scene with one light and one camera.
4. Render a single still. Document the steps.

### Path C — Game asset pipeline (advanced)

1. Generate four matching 2D sprites for a tiny game character (idle, walk, jump, action).
2. Generate one tileset for a small environment.
3. Generate one music loop and three sound effects.
4. (Optional) Combine in a small playable scene using [Phaser](https://phaser.io/) or [PICO-8](https://www.lexaloffle.com/pico-8.php) with help from an AI coding assistant (chapter [8](ai-code.ipynb)).

---

## Reflection prompts

1. What does it mean to "design" a thing when the AI can generate 100 variations in 60 seconds? Where does design judgement now sit?
2. A small game studio with five people in 2018 made one game in two years. The same studio with five people in 2026 can make six games in two years. What changes culturally?
3. Which parts of 3D / design work do you most *want* to stay human, and why?

---

## Going further

- [Inria's official Gaussian Splatting page](https://inria.hal.science/hal-04261469) — the original 2023 paper
- [Polycam Academy](https://poly.cam/academy) — quick, video-based introductions to 3D capture
- The [Blender + AI](https://www.blender.org/) ecosystem — many add-ons combining traditional modelling with AI
- *AI Animation Studio*, IDEO and Anthropic case studies on AI in studio practice
"""


CH10 = r"""---
title: "10. Multimodal and agentic AI"
subtitle: "When models see, hear, and act"
description: "How AI moves from single-medium tools to systems that combine text, image, sound, and action — and what that means for creative pipelines."
---

---

## Why this matters

For most of this book we have looked at AI as a system that takes a prompt and produces an artefact. By 2026 a quieter revolution has been changing what AI *is*:

- **Multimodal models** see images and hear sound as easily as they read text.
- **Agentic systems** chain models together, take actions in the world, and complete multi-step tasks autonomously.

These two ideas, taken together, mean that the creative AI of the late 2020s looks less like a slot machine and more like a **collaborator that can read your screen, look at your sketch, listen to your voice memo, write code, and pay for an API**.

This week we look at the architecture and the ethics of that shift.

---

## Multimodal models

Until around 2023, generative AI tools were medium-specific: ChatGPT did text, Midjourney did images, MusicLM did music. Modern models are increasingly **multimodal**: a single architecture handles many media in and many media out.

```{figure} figures/multimodal.svg
:alt: A diagram showing several modalities (text, image, audio) flowing into a shared model and out again as new modalities.
:align: center
A schematic of a multimodal model: many modalities in, many modalities out, with a single shared "thinking" space in the middle.
```

The technical recipe is roughly:

1. **Encode** each modality (text, image, audio) into a sequence of vectors using a small modality-specific encoder.
2. **Pass them through a shared transformer** [@Vaswani2017] that does not care which modality they came from.
3. **Decode** to whichever modality is wanted on the way out.

Concrete consequences for creative work:

- **You can paste an image and ask a question about it.** Useful for design critique, architecture review, art history.
- **You can hand the model a screenshot and ask it to fix the UI.**
- **You can play it a 30-second clip and ask for the genre, tempo, and emotional tone.**
- **You can talk to it like a phone call** — Voice Mode in major chat products.
- **You can give it a sketch and ask for a polished version**, or a polished image and ask for a structural sketch.

This unlocks a different kind of prompt: **show, don't tell**. The most useful prompt is often *"here is what I am working with — here is what I want — please help."*

---

## Agentic AI

An **AI agent** is a system that is given a goal and decides for itself which steps to take. The minimum architecture is:

1. An LLM with **tools** it can call — web search, code execution, file system, browser, APIs.
2. A **loop**: the model takes a step, observes the result, plans the next step, repeats.
3. A **stopping criterion**: the goal is met, the user intervenes, or a budget is exhausted.

Agents have existed in research since the 1970s. The current generation works because the underlying LLMs are good enough to plan and to recover from errors. By 2026, agentic tools include [Anthropic's Claude Code](https://www.anthropic.com/claude-code), [OpenAI's Operator](https://openai.com/index/introducing-operator/), [Cursor's agent mode](https://cursor.com/), and many specialised ones for sales, support, research, and creative pipelines.

For creative work, the most useful agents are:

- **Coding agents** — implement a small feature across multiple files (chapter [8](ai-code.ipynb)).
- **Research agents** — plan a literature search, summarise the findings, draft a memo.
- **Production agents** — wire together image, audio, and video tools into a single pipeline.

The hardest part is **supervision**: agents can do enormous amounts of work, much of it wrong. The discipline is to give an agent narrow, *cheap-to-verify* tasks.

---

## A creative pipeline as an agent

Imagine you want to produce a 60-second animated short film. The agent's plan might look like:

1. **Story generation.** Ask an LLM for three story outlines on the brief. Pick one.
2. **Storyboard.** Generate 12 storyboard panels with an image model (chapter [5](ai-images.ipynb)).
3. **Animation.** For each storyboard panel, run image-to-video with motion prompts (chapter [7](ai-video.ipynb)).
4. **Voice-over.** Generate the voice-over with TTS (chapter [6](ai-sound.ipynb)).
5. **Music.** Generate the score with a music model (chapter [6](ai-sound.ipynb)).
6. **SFX.** Generate Foley and ambience.
7. **Assembly.** Open a video editor, place the clips, sync the voice-over, mix the audio.
8. **Render.** Export the final film.

Each step is doable by a separate, focused tool. Stitching them together used to be a producer's job; in 2026 that producer is increasingly an agent.

This is *not* the same as "AI replaces a film crew". It is more like "an apprentice now does the wiring while the director directs."

---

## What agents are not

- **They are not magical.** Most fail at multi-step tasks more than 50% of the time without careful supervision.
- **They are not cheap at scale.** A single agent run on a non-trivial task can cost USD/EUR 1–10 in API fees. Multiplied by users, this adds up.
- **They are not safe by default.** An agent with a browser can pay for things, send messages, sign up to services. Read the permissions before you press go.
- **They do not have opinions.** They have outputs. Pretending otherwise is a category error.

---

## Where this is going

By the late 2020s, the centre of gravity of generative AI is moving from "produce one artefact from one prompt" to "complete one task using many tools over time." That is a much bigger change than it first appears, because it changes who is doing the *work* (still you, but as a director) and where the *value* sits (in the brief, the supervision, and the taste).

For students this means a single piece of practical advice: **become very good at writing briefs**. A brief is a precise, ambitious, well-bounded request. Models cannot read your mind; agents cannot guess what you really want. Whoever can write a great brief, in 2026, can ship work that used to require a team.

---

## Practice (2 h)

### Try a multimodal conversation

1. Take a photograph of something messy or interesting in your daily life — your desk, a Tupperware drawer, a chord diagram from a music book.
2. Upload it to a multimodal chat model. Ask it three increasingly specific questions about the image.
3. Pivot: ask it to *redesign* what is in the image (a tidied desk, a different kind of chord). Note where its design knowledge ends and its general pattern-matching begins.

### Design an agent on paper

You will not implement an agent today. Instead, **design one**.

1. Pick a small creative goal you care about (a website portfolio, a podcast episode, a comic page, a recipe book).
2. List **every single step** an agent would take to complete it.
3. For each step, write down: which model, what input, what output, how you would verify the output, and what would happen if it failed.
4. Stop. Look at the diagram. Which steps are you happy to delegate, and which would you keep manual?

### Optional code track

Use the OpenAI [Agents SDK](https://platform.openai.com/docs/agents) or LangGraph to build a tiny three-step agent: search for a paper, summarise it, write a one-sentence headline. Don't expect magic — expect a useful sketch.

---

## Reflection prompts

1. In your discipline, what is a *brief*? Who writes it now, and who would write it if AI did the rest of the work?
2. Imagine an agent that watches all your work and proactively suggests "next steps" in the background. Is that a tool or a colleague? Should you pay it?
3. The most successful agents in 2026 are also the ones with the most permissions (browsers, payment, code execution). What is the price of that?

---

## Going further

- Anthropic's [Claude Code](https://www.anthropic.com/claude-code) documentation — readable, opinionated take on coding agents
- OpenAI's [Operator](https://openai.com/index/introducing-operator/) demos
- Andrej Karpathy, *Software 2.0 / 3.0* talks on YouTube — programming-with-prompts as a paradigm shift
- The [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) and [BabyAGI](https://github.com/yoheinakajima/babyagi) historical projects — for a sense of where this all started in 2023
"""


CH11 = r"""---
title: "11. Ethics and politics of Creative AI"
subtitle: "Copyright, bias, labour, sustainability, and consent"
description: "A working ethics curriculum for Creative AI: where the harms come from, how to think about them concretely, and what you can do as a student, creator, and citizen."
---

---

## Why this matters

It would be easy to spend an entire course on the wonders of Creative AI without ever asking the harder question: **at whose cost?** This chapter is the place where we ask it directly, with examples grounded in the tools you have been using all semester.

The aim is not to make you cynical or paralysed. It is to give you the vocabulary, the cases, and a small toolkit of personal decisions, so that when an AI tool lands on your work or in your inbox, you can think *clearly* about it instead of in slogans.

---

## A simple frame: harm, benefit, and to whom

For every Creative AI system, four questions get you most of the way to a useful ethical position:

1. **Who benefits?** (Users? The company? Specific groups? Society at large?)
2. **Who is harmed, or could be?** (Workers in the training data? Users? Bystanders? The planet?)
3. **Is the benefit *proportional* to the harm?**
4. **Are the harms *consented to* by those bearing them?**

You will see versions of these four questions in every serious AI ethics framework, from the [Belmont Report](https://en.wikipedia.org/wiki/Belmont_Report) to the EU AI Act [@EUAIAct] to UNESCO's *Recommendation on the Ethics of AI*.

Now we apply them across five concrete topics.

---

## Topic 1 — Copyright, consent, and training data

The biggest open legal question in 2026 is **whether training a model on copyrighted material is fair use**. Different jurisdictions have given different answers, and many cases are still being litigated.

The factual situation:

- Most foundation models were trained on **massive web-scraped datasets** that include copyrighted text, images, music, and code, without explicit permission from the authors.
- Companies argue this is **fair use / fair dealing / "text and data mining" exception**.
- Authors, artists, photographers, musicians, and game studios argue it is **mass infringement**.
- The legal landscape: in the EU, there is a [text-and-data-mining exception with an opt-out](https://eur-lex.europa.eu/eli/dir/2019/790) (the [DSM Directive](https://en.wikipedia.org/wiki/Directive_on_Copyright_in_the_Digital_Single_Market)). In the US, ongoing cases (e.g., [Andersen v. Stability AI](https://en.wikipedia.org/wiki/Andersen_v._Stability_AI), [NYT v. OpenAI](https://en.wikipedia.org/wiki/The_New_York_Times_Company_v._Microsoft_Corporation,_OpenAI,_Inc.,_OpenAI_LP_et_al.)) will set the doctrine for the next decade.

What you can do:

- **Honour opt-outs.** If you train or fine-tune, respect `robots.txt`, `ai.txt`, and platform-level opt-outs.
- **Use licensed data** for commercial or sensitive work where possible. Adobe Firefly, Getty AI, and a growing number of music-AI startups train on licensed corpora.
- **Be honest about provenance** in your own outputs.

```{admonition} Question
:class: question
Should training data be opt-in (you must agree before your work is used) or opt-out (your work is used unless you object)? What changes for individual artists vs. institutions like libraries and universities?
```

---

## Topic 2 — Bias and representation

Models inherit the distribution of their training data. If the data over-represents English, Western, urban, web-published, well-photographed, predominantly male material, the model will reflect that — sometimes obviously, sometimes invisibly.

Concrete examples:

- Ask an image model for "a CEO" without further qualifiers. Count the proportion of men.
- Ask a chat model for "a typical Norwegian breakfast". How often does it list things actually eaten in Norway?
- Ask a code model to write a sorting function. In which programming language does it default?
- Ask a music model for "a wedding song". From which culture?

These are *legible* biases. There are also subtler ones: stereotyped associations, missing dialects, accents that get mis-transcribed, faces that are not detected, languages that produce strictly worse output.

Bender et al.'s "Stochastic Parrots" paper [@Bender2021Parrots] is the canonical critical text on this. Crawford [@Crawford2021Atlas] situates the question within wider structural inequalities.

What you can do:

- **Audit your outputs** for representation, especially in work that will be public.
- **Use refined prompts and reference images** when generating people.
- **Document failures** when you see them. Many companies fix flagged biases in the next training cycle.
- **Choose tools that report bias evaluations** — increasingly common in 2026.

---

## Topic 3 — Labour

Generative AI sits on a foundation of human labour that is rarely visible:

- **Data labellers** — millions of workers, often in low-wage countries, label images, rank model outputs, and write fine-tuning examples. They make the model behave; they also bear the psychological cost of moderating violent and abusive material [@BroussardArt].
- **Artists whose work was used for training** — often without consent, payment, or attribution.
- **Voice actors** asked to record samples that are later cloned to do work they would have been paid to do.
- **Creative professionals** whose markets are reshaped by tools trained on their previous work.

This is not unique to AI — every wave of automation reorganises labour. But the speed and the source of the training data make it sharper than past waves.

What you can do:

- **Pay for tools** that pay their labellers fairly and license their data.
- **Credit and pay human collaborators** when you publish AI-assisted work.
- **Push your employer or institution** to adopt AI policies that protect contractors and workers.
- **Read your contracts.** Many platforms now insert clauses about training on user content.

---

## Topic 4 — Sustainability

Training a large model uses **a lot of electricity, water, and rare materials**. Inference (everyday use) uses less per query but vastly more in aggregate. Strubell et al. [@Strubell2019Energy] put this on the map in 2019 with their NLP-focused estimates; more recent estimates have widened the scope to include water for data-centre cooling and the embodied carbon of GPUs.

In 2026:

- Major data centres in the Nordics, including some in Norway, are being built specifically for AI workloads. This is partly *because of* our cheap clean electricity — a mixed blessing.
- A single image generation can use roughly the energy of a smartphone charge for inference; training a frontier model uses on the order of a small town's electricity for a year.
- Reasoning-mode "thinking" models multiply inference compute by 10×–100× per query.

What you can do:

- **Use smaller, distilled models** for routine tasks. Most jobs do not need the frontier.
- **Batch your work.** Iterate locally before paying for the big cloud run.
- **Choose tools that publish their compute usage** and their energy mix.
- **Ask, in policy debates, whether the marginal benefit is worth the marginal energy.**

---

## Topic 5 — Authorship, authenticity, and the public sphere

Generative AI strains the basic categories of cultural life:

- **Authorship.** If a song is written 70% by Suno and 30% by you, who is the author? Spotify, the courts, and your conscience may give different answers.
- **Authenticity.** A photograph of "the prime minister at a demonstration" is no longer evidence. Audio of "a friend asking for money" is no longer evidence. The default assumption of *recorded media as truth* is over [@EUAIAct].
- **The public sphere.** Social platforms in 2026 are full of AI-generated content competing for human attention. Some of it is benign; some of it floods elections and public debate with low-quality, plausible-sounding noise.
- **Education.** Submitting AI-written essays as your own is academic dishonesty — but a generation of students has grown up with these tools, and the policies are still catching up.

What you can do:

- **Label.** When you publish AI-assisted work, say so. C2PA-style metadata is emerging as a standard.
- **Verify.** When you receive a striking video, audio, or quote, check the provenance before sharing.
- **Resist over-claiming, in both directions.** AI is not creating the apocalypse, and it is not just a fancy autocomplete.

---

## A small personal toolkit

Three habits worth committing to as a creator in 2026:

1. **Keep a decisions log.** Every project: which tools, which prompts, which edits, which versions you kept and why. This protects you legally and is honest.
2. **Treat a model like a freelancer.** Ask for credentials, check the work, give credit, do not assume good faith on copyright.
3. **Refuse cheerfully.** It is fine — and increasingly important — to say *"I am not using AI for this part."* Not as ideology; as craft.

---

## *Death of the Artist or Birth of the Curator?*

A useful — and deliberately provocative — framing for the cultural argument: in 1967, Roland Barthes wrote *The Death of the Author* and shifted authority from the writer onto the reader. In the AI era, a parallel debate has opened up: does generative AI dissolve the *artist* into the model and the dataset, or does it elevate a new figure — the *curator* who selects, prompts, edits, refuses, and stands behind the work?

Both readings are partly true, and they are usefully in tension. The argument matters because it shapes:

- **what we call authorship** (and what we put in copyright registers);
- **what we credit** (and how we pay people whose labour entered the dataset);
- **what we ask of students and professionals** when we say *"do this with AI"*;
- **what the public will accept** as a published creative artefact.

This week's ethics essay (see below) is your chance to take a real position on this tension — or on a different one — and defend it.

---

## Practice (2 h)

### Audit one tool

Pick a Creative AI tool you have used this semester. Spend the first hour of the practice session writing a short **ethical audit** of it, using the four questions from the top of this chapter. Cover:

- **Provenance** of training data (what the company says publicly).
- **Bias** — try a small probing set (e.g., 10 prompts that touch gender, geography, language).
- **Labour** — what do you know about the labellers and moderators?
- **Sustainability** — does the company publish anything?
- **Authorship and labelling** — does the tool offer C2PA or watermarking?

Aim for 600–1 000 words. This is also the seed material for your ethics essay.

### Group debate

In the second hour: two teams of 3–4 students each. Each team randomly draws a position:

- "Training generative models on copyrighted material is acceptable as fair use."
- "Training generative models on copyrighted material is not acceptable without per-rights-holder consent."

You will defend the position you drew, regardless of your prior view. (This is a deliberate exercise — being able to make the strongest case for a view you disagree with is the most useful skill in ethics.)

### Mid-term ethics essay (1 page, Pass / Fail) — due this week

Choose **one** of the following prompts and write a tight, well-argued one-page essay (≈ 600 words) with at least three references:

- *Death of the Artist or Birth of the Curator?* — Take a clear position on what generative AI does to authorship.
- *Should AI-generated work be eligible for copyright protection?* — Argue one side, with worked counter-arguments.
- *Where should AI stay out of my discipline, and why?* — Pick your field and draw a defensible line.
- *Whose voice, whose face?* — The ethics of voice and likeness cloning in the age of consent.
- A topic of your own, proposed in your weekly log by the end of week 9.

Submit through the LMS. The essay is graded Pass / Fail (10 % of the course); a Fail can be revised once.

---

## Reflection prompts

1. Pick a Creative AI use you find uncomfortable. Write 300 words on why. Then write 200 words steelmanning the other side.
2. The EU AI Act [@EUAIAct] requires labelling of AI-generated content "interacting with humans". How would you implement that for your own work?
3. Your future job will be done partly with AI. What conditions would have to hold for you to feel that this is good for you and good for others?
4. Re-read the *Death of the Artist or Birth of the Curator?* framing above. Where does it map onto a specific project you have worked on this semester?

---

## Going further

- Bender et al., *On the Dangers of Stochastic Parrots* [@Bender2021Parrots]
- Crawford, *Atlas of AI* [@Crawford2021Atlas] — the most readable structural critique
- O'Neil, *Weapons of Math Destruction* [@ONeil2016]
- Broussard, *Artificial Unintelligence* [@BroussardArt]
- UNESCO, *Recommendation on the Ethics of AI* (2021)
- The [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) text and summaries [@EUAIAct]
- The [Spawning Coalition](https://spawning.ai/) — for opt-out tools and arguments
"""


CH12 = r"""---
title: "12. Futures and final projects"
subtitle: "What comes next, and what you will make"
description: "Closing the semester: where Creative AI is heading, how to think about uncertain futures, and how to present a small final project."
---

---

## Why this matters

We have spent eleven weeks looking at what Creative AI *is*. We close the semester by looking at what it might *become*, what you will make, and what to do with all the work and prompts and decisions you have accumulated.

This is the lightest reading of the semester. The 2 hours of practice this week are spent presenting your final project to the class.

---

## Three futures, none of which is the future

It is worth being honest: no one knows where this is going. The most accurate prediction in 2022 about 2026 was made by very few people. Prediction in 2026 about 2030 will be at least as hard.

Still, three "futures" sketches are useful, not because any of them will come true, but because they map out the *space* of where we might end up. (This kind of "scenarios" exercise comes from [strategic foresight](https://en.wikipedia.org/wiki/Futures_studies) and is widely used in policy-making.)

### Future A — "AI as electricity"

Generative AI fades into the background, the way the internet did in the 2000s and the cloud did in the 2010s. Every tool has AI features; nobody talks about them as *AI* features any more. The technology becomes infrastructure. The interesting work moves up the stack to design, story, taste, and ethics.

Creators in this future spend less time on production craft (which is automated) and more on **direction, curation, and editorial judgement**. Smaller studios produce work that used to require larger teams. New genres emerge from the cheapness of iteration.

### Future B — "AI as collaborator"

Generative AI stays in the foreground as a distinct *kind* of collaborator. Tools have personalities, opinions, and styles. Studios hire specific AI characters the same way they hire specific actors. Reputation systems emerge for both human and AI contributors. The legal and labour frameworks accommodate this hybrid mode.

Creators learn a new craft: *casting*. You know which model has which sensibility, which can do which kind of work, which to pair with which human collaborator. The line between *making* and *directing* becomes more obviously continuous.

### Future C — "AI as flood"

Generative AI scales beyond human capacity to attend to or evaluate its output. Most online content is AI-generated; most of it is mediocre and most of it is competing for attention. Search degrades, social platforms degrade, public discourse degrades. Human-made and human-curated work commands a premium in the same way handmade goods do today.

Creators in this future organise into **trust networks**, where provenance, slowness, and verifiable authenticity are the value proposition. Institutions like libraries, universities, and public broadcasters become more important, not less.

These three futures are not exclusive. Bits of all three are visible already in 2026. The point of the exercise is not to bet on one; it is to ask, in each, *what does your discipline look like?*

---

## What stays human

Whatever the future, some things stay human longer than others. A non-exhaustive list of things that current and near-future AI cannot do well:

- **Sit in a room with another person and read their face for ten minutes.** Therapists, teachers, social workers, nurses, mentors.
- **Live performance** that depends on the audience being in the same physical space.
- **Long, situated, embodied research** — fieldwork, ethnography, clinical care.
- **Care for the very young, the very old, the very sick.**
- **Take moral responsibility** for a piece of work or a decision.
- **Be liable in a court.**

These are not "AI-proof" categories in the sense that AI cannot affect them — it can and will — but they are categories where the centre of gravity stays human for at least the medium term.

Your final project does not need to be in any of these categories. But it is worth thinking, this week, about which parts of your own work and life sit closest to them.

---

## Reading the next decade

A few habits that help, regardless of what happens:

- **Read primary sources.** A model card, a research paper, an EU regulation — these are easier to read than the takes about them, and they are more reliable.
- **Watch benchmarks fall.** [Papers with Code](https://paperswithcode.com/), Stanford's AI Index, and Epoch AI track capabilities over time. Look at the trend, not the snapshot.
- **Build small things.** A weekend project tells you more than a year of essays.
- **Talk to people in other disciplines.** Lawyers, doctors, librarians, designers, teachers — they each see a different face of the same technology.
- **Stay sceptical of both extremes.** Both "AI changes nothing" and "AI changes everything" are *almost always* wrong.

---

## Final projects — *The Synthetic Gallery*

The remaining 2 hours of class are spent on the **final project showcase**, which we call *The Synthetic Gallery*. The project counts for 50% of the course grade and is the central artefact of your semester. The Synthetic Gallery is a public mini-exhibition open to other UiO students, staff, and invited guests — held both in a physical room at UiO and as a static gallery on the course's GitHub Pages site.

### What a project can look like

Anything that meaningfully uses Creative AI for a creative purpose:

- a short story or chapter,
- a poster series,
- a 30–90 second short film,
- a song or short EP,
- a small interactive web piece,
- a game prototype,
- a podcast episode,
- a redesign of a real organisation's brand,
- a curated exhibition of generated work,
- a written critical essay using AI as a tool for the work *and* as the object of study,
- a teaching resource for a younger sibling.

Solo or in groups of 2–3. The project should be ambitious enough to be hard, and small enough to finish.

### Technical requirements

- The work must use **at least two different AI modalities** — for example text + image, image + video, audio + code, 3D + text. This is the technical bar of the course.
- All prompts, generations, and decisions must be **logged** and submitted with the work.
- The work and reflection must explicitly **acknowledge** which AI tools were used, with versions or dates.

### What you must deliver

1. **The work itself** — file, link, video, deck, or performance.
2. **A reflection** (1 500–2 500 words) covering:
   - The brief and the audience.
   - The tools used, with versions.
   - A timeline of decisions, including the moments where the AI *surprised* you and the moments where you exerted your *will*.
   - One ethical question you ran into and how you resolved it.
   - What you would do differently.
3. **A 5-minute presentation** at the Synthetic Gallery in week 12, with a 5-minute Q&A.
4. **A gallery page** — a single HTML/markdown page (template provided) for the public online gallery, with consent options for inclusion in future cohorts' material.
5. **Your full prompt log** (the file you have been keeping all semester). Yes, this matters.

### What "good" looks like

Examples of strong projects from prior offerings:

- *A 40-second AI-generated music video for an original song the student wrote*, with stems generated by Suno and re-recorded vocals on top, and a hand-edited storyboard in Runway. The reflection compared early Bob Dylan music videos with the new affordances of cheap motion.
- *A redesign of the visual identity for a Norwegian charity*, using Midjourney for moodboards, Recraft for vector marks, and Figma for the final system. The reflection walked the reader through every prompt and editorial decision.
- *A short interactive piece in p5.js* where the user types a memory and a generated soundscape plays back. The reflection focused on what the AI got wrong, and why those errors became part of the piece.

What makes these projects strong is not the polish but the **fit between brief, tool, and reflection**. A modest project with a clear, honest brief beats a flashy project with no spine.

### Process memo — once more, with feeling

When you submit, your reflection must answer the two questions we have used all semester:

1. **Where did the AI surprise you?**
2. **Where did you exert your own creative will?**

These will be the first things the audience at the Synthetic Gallery asks you in the Q&A. Be ready.

---

## Closing

When this course was designed in 2026, the field was moving so fast that two of the tools listed in chapter 1 had merged and one had been bought before the syllabus was approved. By the time you read this in your future career, every tool name will have changed.

What will not have changed is the structure of the questions:

- How do these systems work?
- How do I use them well?
- Who benefits, who is harmed, and what does *my* practice owe them?

You leave this course with a small toolkit, a personal log of decisions, and one finished project. Take all three with you.

```{admonition} Question
:class: question
Look back at the one-sentence definition of *Creative AI* you wrote in week 1. Do you still agree with it? What would you write today?
```

---

## Practice (2 h) — Project presentations

The structure for the final session:

- 5 minutes per project + 5 minutes of Q&A.
- Audience is the rest of the class plus invited guests from elsewhere at UiO.
- Bring your laptop. Test the AV during the break.
- Submit your reflection and prompt log by the start of the session.

---

## Going further

After the course:

- The [Stanford AI Index](https://aiindex.stanford.edu/) — the best single-volume snapshot of the field, published yearly.
- The [Distill](https://distill.pub/) archive and [Lilian Weng's blog](https://lilianweng.github.io/) — the best long-form technical writing on machine learning ideas, free.
- [Hugging Face](https://huggingface.co/) — the closest thing the open AI world has to a town square. Follow people there, not on Twitter.
- The next iteration of this course. The textbook is open and updated yearly. Issues, pull requests, and corrections welcome at <https://github.com/fourMs/Creative-AI>.

Thank you for spending the semester here. Make things.
"""


CHAPTERS = [
    ("intro.ipynb", INTRO),
    ("introduction.ipynb", CH1),
    ("foundations.ipynb", CH2),
    ("generative-ai.ipynb", CH3),
    ("ai-language.ipynb", CH4),
    ("ai-images.ipynb", CH5),
    ("ai-sound.ipynb", CH6),
    ("ai-video.ipynb", CH7),
    ("ai-code.ipynb", CH8),
    ("ai-3d-games.ipynb", CH9),
    ("multimodal-agents.ipynb", CH10),
    ("ethics.ipynb", CH11),
    ("futures.ipynb", CH12),
]


def main() -> None:
    BOOK.mkdir(parents=True, exist_ok=True)
    for filename, source in CHAPTERS:
        write_notebook(filename, split_blocks(source))


if __name__ == "__main__":
    main()
