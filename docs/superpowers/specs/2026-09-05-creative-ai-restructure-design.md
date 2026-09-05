# Creative AI textbook restructure: design

Date: 2026-09-05
Status: approved in discussion, awaiting spec review

## 1. Purpose

Rework the *Creative AI* open textbook so that it

- stands on its own as a 12-week bachelor course open to all UiO faculties, taught in 45-minute blocks: one 45-minute lecture and a 90-minute lab (two blocks) each week;
- is complementary to *Sensing Sound and Music* (MUS2640) without depending on it, since many but not all students will arrive from that course;
- adopts the writing style, chapter template, tooling, and standalone web apps of *Sensing Sound and Music*;
- is visibly research-led, building on RITMO, the fourMs Lab, and the MishMash Centre for AI and Creativity while covering the wider state of the art;
- absorbs the changes agreed on 2026-09-05: split multimodal from agentic AI, add a robotic AI week, move ethics early, keep 3D and XR as its own week, add a tips-and-tricks page and a glossary, reorder the lab tracks to Explore, Reflect, Create, and move the Synthetic Gallery to the exam period.

## 2. Constraints

- 12 teaching weeks, each with three 45-minute blocks: a 45-minute lecture and a 90-minute lab. The Synthetic Gallery showcase is held in the exam period, outside the 12 weeks.
- No programming prerequisite. Code appears only in collapsible "Dig deeper" notes and in optional exercises.
- Open education: CC-BY-4.0, source on GitHub, open tools preferred, paid tools named with an open alternative.
- Everything must build with `myst build --html --execute`. Executed code cells must run offline in CI in under a minute each and need no GPU, API key, or network access. Heavy or paid code stays as non-executed fenced listings.
- Web apps are single-file, client-side, send no data anywhere, and work offline.

## 3. The spine: five layers

*Sensing Sound and Music* has four levels of description and every chapter says which level it works at. *Creative AI* gets an equivalent spine of five layers. Each chapter opens with one paragraph naming its layer(s).

| Layer | What it covers | Question it answers |
| --- | --- | --- |
| **Data** | Training corpora, provenance, consent, bias, labour | What went in? |
| **Model** | Architectures, training, sampling, conditioning, capabilities and limits | What can it do, and why? |
| **Interface** | Prompts, briefs, controls, tools, agents, bodies | How do you steer it? |
| **Practice** | Workflows, craft, iteration, documentation, collaboration | How do you make good work with it? |
| **Culture** | Authorship, aesthetics, law, economy, environment, futures | What changes when it enters the world? |

The three course concepts stay as they are: **intentionality**, **aesthetic control**, **ethical authorship**. The five paradoxes of co-creation (Salma et al. 2025) move from the generative-AI chapter into the ethics chapter, where they frame the human role.

## 4. Course schedule

| Week | File | Chapter | Layer | Lecture (45 min) | Lab (90 min) | Milestone |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `introduction.ipynb` | What is Creative AI? | culture | History from Dada to diffusion; definitions; the five layers; RITMO, fourMs, MishMash context | First generations in one text and one image tool; start the practice log | A1 starts |
| 2 | `how-it-works.ipynb` | How generative AI works | data, model | Data, models, training, inference; distributions, sampling, conditioning; model families | Model card reading; same prompt three samplers; training-loop and sampler apps | A1 due |
| 3 | `co-creation-and-ethics.ipynb` | Co-creation, authorship, and ethics | culture | Five paradoxes; craftsperson to creative director; copyright, bias, labour, energy, authenticity; three futures as foresight | Debate; audit one tool; draft a one-page AI policy | Ethics essay starts |
| 4 | `language.ipynb` | Language | interface | LLMs, tokens, context, in-context learning, failure modes | Hallucination hunt; two-model comparison; prompt library | A2 starts |
| 5 | `images.ipynb` | Images | model, interface | Diffusion, control signals, editing, series consistency | Controlled one-variable experiment; image-to-image; a finished series | A2 due |
| 6 | `sound.ipynb` | Sound and music | practice | Speech, voice, music, sound design; from analysis to generation; consent | Transcribe and re-voice with consent; a 30-second piece | A3 starts |
| 7 | `video.ipynb` | Video | model | The time axis; consistency; image-to-video; lip-sync; deepfakes; world models | Storyboard to three shots with provenance card | Ethics essay due |
| 8 | `spatial.ipynb` | 3D, XR, and games | practice | Capture (splats), generation (meshes, textures), worlds, VR/AR/XR pipelines, game assets | Capture a splat or generate an asset and place it in a scene or headset | A3 due |
| 9 | `code.ipynb` | Creative coding | practice | Assistants, reading code, p5.js, tiny AI-powered web tools | Mouse-reactive sketch with an assistant; read code you did not write | Proposal starts |
| 10 | `multimodal.ipynb` | Multimodal AI | model | Shared representations; models that see, hear, and speak; show, don't tell | Multimodal critique of your own work in progress; cross-modal translation | Proposal due |
| 11 | `agents.ipynb` | Agentic AI | interface | Loops, tools, briefs, supervision, cost, safety | Design a pipeline; run a small agent on one slice; agent-loop app | — |
| 12 | `body.ipynb` | AI with a body, and what stays human | practice, culture | Embodiment and 4E cognition; action-sound mappings; musicking robots; what stays human | Rhythm-bot session; map a sensor or camera to a generator; project rehearsal | Final project due end of week |
| exam period | — | The Synthetic Gallery | — | — | Public showcase, 5 min + 5 min per project | Gallery |

Five extra pages sit outside the weekly rhythm: `intro.ipynb` (course overview), `tips-and-tricks.ipynb`, `glossary.md`, `tools.md`, and `gallery.md` (template and archive for the showcase).

Files to delete: `foundations.ipynb`, `generative-ai.ipynb`, `ai-language.ipynb`, `ai-images.ipynb`, `ai-sound.ipynb`, `ai-video.ipynb`, `ai-code.ipynb`, `ai-3d-games.ipynb`, `multimodal-agents.ipynb`, `ethics.ipynb`, `futures.ipynb`. Their content is redistributed as described in section 7; nothing good is thrown away.

## 5. Lab structure: Explore, Reflect, Create

Every lab runs in the same order, and every chapter's lab section uses the same three subheadings.

1. **Explore (about 30 min).** Controlled experiments with the week's tool: vary one thing, compare two tools, break something on purpose. This is where the model surprises you.
2. **Reflect (about 15 min).** A structured pair or plenary discussion, not a writing block. It ends with each student stating one intention for what they will make. This is where you decide.
3. **Create (about 45 min).** Make the artefact you stand behind, and carry it over into the portfolio at home. This is where you exert your will.
4. **Log (at home).** The three-paragraph weekly entry, Explore / Reflect / Create, closes the loop as the retrospective.

The order maps onto the two process-memo questions, surprise and will, with reflection between them. The cycle diagram in the overview is redrawn as Explore → Reflect → Create → Log → Explore. Weeks 3 and 12 bend the timings (ethics is reflect-heavy; week 12 reserves time for project rehearsal) but keep the order.

The acronym changes from REC to ERC everywhere: overview, diagram, chapter subheadings, log template, assessment table.

## 6. Chapter template

Adopted from *Sensing Sound and Music*, with the lab section kept from *Creative AI*.

1. **Front matter**: title `"N. Chapter title"`, subtitle, description.
2. **Opening paragraph** naming the layer(s) the chapter works at and linking back to the spine.
3. **Prose sections** (`##` and `###`), written as explanation rather than tool documentation. Inline `{admonition} Question` boxes and short `{exercise}` blocks where a two-minute try-it helps.
4. **Dig deeper** collapsible notes (`:::{note} Dig deeper: ...`) for optional technical depth, equations, and code listings. These replace the scattered "optional code track" blocks.
5. **Research spotlight** admonition (`:::{admonition} Research spotlight` with class `spotlight`): one RITMO, fourMs, or MishMash project per chapter, described in a paragraph with a link and a citation, plus one sentence on how a student could connect to it.
6. **If you took MUS2640** note in chapters that overlap with *Sensing Sound and Music* (weeks 2, 6, 10, 12): one paragraph saying what is assumed known there and linking to the relevant chapter.
7. **This week's lab: Explore, Reflect, Create** with timings as in section 5.
8. **A critical look: ...** A popular claim about Creative AI checked against evidence in four moves: the claim, the evidence, the method, the limits.
9. **Chapter summary** admonition (class `tip`), one paragraph.
10. **Questions** admonition (class `question`), five questions.
11. **Further reading** (`:::{seealso} Further reading`), three to six items, every one with a DOI or URL.
12. **Explore interactively** (`:::{tip} Explore interactively`), links to the chapter's web apps.

Figures move to `book/figures/<chapter>/` with one folder per chapter, as in the other book. Cover art stays in `book/figures/cover/`.

## 7. Chapter briefs

Each brief lists layer, key concepts, research spotlight, critical look, lab sketch, apps, and what is carried over from the current draft. Word budgets are for prose excluding the lab, and are targets, not limits.

### 1. What is Creative AI? (culture, about 3 000 words)

- Concepts: creativity (Boden's P/H and combinational/exploratory/transformational), AI, the working definition of Creative AI, the two historical strands, the three course concepts, the five layers.
- Spotlight: MishMash Centre for AI and Creativity, its seven work packages, and how the course's three tracks map onto them.
- Critical look: *Did an AI win the Colorado State Fair?* The 2022 Théâtre D'opéra Spatial case as claim, evidence, method, limits.
- Lab: as now, in ERC order. Explore first generations; Reflect on the student's own one-sentence definition; Create the first flyer or diptych and the first log entry.
- Apps: none specific; the tools page.
- Carried over: almost everything from the current `introduction.ipynb`, plus the "reading a claim" checklist from the overview.

### 2. How generative AI works (data, model, about 4 000 words)

- Concepts: data, model, parameters, training, inference, loss, generalisation, bias as a data property; classification versus generation; distributions and sampling; temperature, top-k, guidance, steps, seeds; conditioning; the four model families; foundation models and adaptation; what generative models cannot do.
- Spotlight: the AMBIENT project as an example of what a dataset of human bodily entrainment looks like, and why models need data of that kind.
- Critical look: *Is a language model just autocomplete?* Claim, evidence from in-context learning and scaling results, method, limits.
- MUS2640 note: artificial neural networks are introduced in *The brain*, and model families in *Machine listening*.
- Lab: Explore a model card and run the same prompt through three sampler settings; Reflect on distribution versus boundary; Create a captioned triptych with an artist's statement.
- Apps: **Training loop playground**, **Next-token sampler**, **Forward diffusion explorer**.
- Carried over: `foundations.ipynb` and `generative-ai.ipynb` merged; the five paradoxes move to chapter 3; the numpy training loop becomes an executed code cell with a figure.

### 3. Co-creation, authorship, and ethics (culture, about 4 000 words)

- Concepts: executors versus collaborators; the five paradoxes; craftsperson to creative director; the four questions (who benefits, who is harmed, proportionality, consent); copyright and training data; bias and representation; labour; sustainability; authenticity and the public sphere; *Death of the Artist or Birth of the Curator?*; three futures as a foresight exercise; the personal toolkit.
- Spotlight: MishMash's work on human agency in co-creative systems and on gender equity in technology-mediated creative fields.
- Critical look: *Does one image cost a bottle of water?* Energy and water claims for inference, checked against published estimates and their assumptions.
- Lab: Explore by auditing one tool with the four questions; Reflect through the structured debate; Create a one-page AI policy. The ethics essay is set here and due in week 7.
- Apps: **Inference energy estimator**, **Provenance inspector**.
- Carried over: `ethics.ipynb` in full, the paradoxes section from `generative-ai.ipynb`, the three futures from `futures.ipynb`.

### 4. Language (interface, about 3 500 words)

- Concepts: next-token prediction, tokens, context versus memory, in-context learning, prompt patterns, the prompt template, failure modes (hallucination, sycophancy, verbosity, drift, arithmetic, cutoff), open versus closed models, how to write with an LLM, Norwegian and low-resource languages.
- Spotlight: the NB AI Lab's Norwegian language models and the NorwAI collaboration, as the national context for what "open" means.
- Critical look: *Do AI-text detectors work?* Claim, evidence from evaluation studies, method, limits including false positives for non-native writers.
- Lab: Explore the hallucination hunt and two-model comparison; Reflect on where the model helps and hinders the student's writing; Create the prompt library.
- Apps: **Tokeniser explorer**, **Word-vector explorer**; stretch: **Small language model in the browser**.
- Carried over: `ai-language.ipynb` with the API listing moved to a Dig deeper note.

### 5. Images (model, interface, about 3 500 words)

- Concepts: diffusion in pictures, latent diffusion, flow matching, the vocabulary of knobs, prompting for images, negative prompts, reference images and control signals, editing instead of generating, where models struggle, consistency across a series.
- Spotlight: motiongrams and video visualisation from the Musical Gestures Toolbox as a different kind of picture-making from data, and what it means to generate images that are true.
- Critical look: *Does an image model copy its training images?* Memorisation studies, extraction attacks, and what "copy" means.
- Lab: Explore one-variable grids and image-to-image at three strengths; Reflect on what the model averages away; Create a series, poster, or diptych with an honest caption.
- Apps: **Forward diffusion explorer** (shared with chapter 2), **Seed and guidance grid viewer** for laying out and captioning a controlled experiment.
- Carried over: `ai-images.ipynb` with the diffusers listing in a Dig deeper note.

### 6. Sound and music (practice, about 4 000 words)

- Concepts: three families (speech, music, sound design); representations (spectrogram, neural codec); where machine listening ends and generation begins; text-to-speech and cloning; music generation and its long-range problem; stems and separation; sound design as the workhorse; consent and voice.
- Spotlight: RITMO's MusicLab and the self-playing guitars as sites where generation meets bodies in a room; RAVE and the IRCAM lineage as the research-grade open tool.
- Critical look: *Can listeners tell AI music from human music?* Listening studies, their stimuli, and their limits.
- MUS2640 note: spectrograms, machine listening, MIR, and the generative-music section are in *Machine listening*; this chapter starts where that one ends.
- Lab: Explore transcription and re-voicing with consent; Reflect on what gives a synthetic voice away; Create a 30-second piece with a consent and provenance note.
- Apps: **Markov melody generator**; link to the *Sensing Sound and Music* live spectrogram rather than duplicate it.
- Carried over: `ai-sound.ipynb`.

### 7. Video (model, about 3 000 words)

- Concepts: why video is hard (cost, consistency, physics); three model strategies; what current systems do and do not do; video prompting; the production workflow; lip-sync and avatars; deepfakes and labelling; world models as the frontier between video and simulation.
- Spotlight: video analysis of musicians' motion in the fourMs Lab as the mirror image of video generation: extracting motion rather than fabricating it.
- Critical look: *Will AI video replace film crews?* Claims from industry, evidence from what has shipped, method, limits.
- Lab: Explore image-to-video with three variations and end-frame conditioning; Reflect in pair critique; Create three shots with a provenance card.
- Apps: **Frame-consistency inspector**, which loads a short clip and shows frame differences over time so students can see where coherence breaks.
- Carried over: `ai-video.ipynb`.

### 8. 3D, XR, and games (practice, about 3 500 words)

- Concepts: capture (NeRFs, Gaussian splats, photogrammetry); generation (text-to-3D, textures, materials); virtual, augmented, and extended reality as the medium where spatial AI is experienced; presence, embodiment, and scale; AI in design tools; the indie game pipeline; where 3D AI struggles.
- Spotlight: RITMO's use of VR and motion capture for studying bodies in concert, and the fourMs Lab infrastructure.
- Critical look: *Does VR make you feel present?* Presence research, its measures, and what AI-generated environments change.
- Lab: Explore by breaking a capture tool with reflective, thin, and dynamic subjects; Reflect on where design judgement sits when variations are free; Create a splat, an asset in a scene, or a small XR scene viewed in a headset or on a phone.
- Apps: **Splat viewer** that loads a small bundled Gaussian splat in the browser; no generation.
- Carried over: `ai-3d-games.ipynb` with an added XR section.

### 9. Creative coding (practice, about 3 000 words)

- Concepts: assistant patterns (complete, chat, inline, agentic); reading before writing; p5.js worked example; how to talk to a coding assistant; generating assets for code; a tiny AI-powered web tool; deskilling and supervision.
- Spotlight: the Musical Gestures Toolbox for Python as an open research codebase students can read, run, and extend with an assistant.
- Critical look: *Does AI make beginners better programmers?* Evidence from classroom studies, method, limits.
- Lab: Explore two assistants on the same p5.js feature; Reflect by explaining back the longest generated function; Create the mouse-reactive sketch.
- Apps: none new; the p5.js web editor is the app.
- Carried over: `ai-code.ipynb`.

### 10. Multimodal AI (model, about 2 500 words)

- Concepts: shared representations; encoders and a common transformer; what changes when a model can look at your sketch, hear your clip, and speak back; multimodal prompting as show, don't tell; multimodal critique; cross-modal translation as a creative method; limits and grounding failures.
- Spotlight: multimodal research at RITMO, where sound, motion, physiology, and video are recorded together, and what a model trained on such data could and could not learn.
- Critical look: *Does a model "see"?* Vision-language evaluation, adversarial examples, and what perception means here.
- MUS2640 note: multimodality and cross-modal correspondences in *Tuning in* and *Vision*.
- Lab: Explore three increasingly specific questions about a photograph; Reflect on where design knowledge ends and pattern-matching begins; Create a cross-modal translation of the student's own project material.
- Apps: **Cross-modal sketchpad**, which maps a drawn line to sound parameters and a sound to a line, as a hands-on illustration of shared representations without a model.
- Carried over: the multimodal half of `multimodal-agents.ipynb`.

### 11. Agentic AI (interface, about 3 000 words)

- Concepts: the minimal agent (tools, loop, stop); executors to collaborators; coding, research, and production agents; a creative pipeline as an agent; what agents are not (cost, failure rates, permissions); supervision and cheap-to-verify tasks; briefs as the new interface.
- Spotlight: agent-based and swarm approaches in RITMO's rhythm research, including the Dr. Squiggles swarm, as agents that act in time rather than in text.
- Critical look: *Can agents complete real creative tasks?* Benchmark evidence on long-horizon tasks, method, limits.
- Lab: Explore by giving a small agent one bounded task and reading its trace; Reflect on which steps to delegate; Create the pipeline diagram with verification and human-in-the-loop checkpoints, and run one slice.
- Apps: **Agent loop simulator**, a toy environment where students step through plan, act, observe with a scripted agent.
- Carried over: the agent half of `multimodal-agents.ipynb`.

### 12. AI with a body, and what stays human (practice, culture, about 3 500 words)

- Concepts: embodied and 4E cognition; the action-perception loop; movement, motion, action, gesture; action-sound couplings versus mappings; musicking robots and machine musicianship; sensors and actuators as interface; inverse and indirect mappings in embodied AI; robots in performance and care; what stays human; closing the loop back to week 1.
- Spotlight: Dr. Squiggles, ZRob, and the self-playing guitars, with the 2026 paper on inverse and indirect mappings in embodied AI and Vear's musicking-robots framework.
- Critical look: *Can a robot musician be creative?* The Lovelace objection, the musicking-robots literature, method, limits.
- MUS2640 note: 4E cognition, motion terminology, motion capture, and the Musical Gestures Toolbox are in *The body*; the action-perception loop is in *Tuning in*.
- Lab: Explore the rhythm-bot and a sensor-to-generator mapping; Reflect on which parts of the student's own work should stay embodied; Create a short project rehearsal with peer feedback, and finish the final entry of the log with the week-1 definition beside it.
- Apps: **Rhythm-bot**, a browser cousin of Dr. Squiggles that tracks the student's taps and plays along; **Sensor-to-sound mapper**, which maps phone or laptop sensors to a simple generator.
- Carried over: the "what stays human" and "reading the next decade" sections from `futures.ipynb`; the closing question about the week-1 definition.

### Overview page (`intro.ipynb`)

Rewritten to the *Sensing Sound and Music* pattern: introduction, learning outcomes, schedule table, extra pages, pedagogical strategy (a course for everyone at UiO; active learning; studio labs; research-based and research-led with RITMO, fourMs, MishMash; reading claims about AI; open education; guest lecturers), ERC lab structure with diagram, assessment, tools (link to the tools page), curriculum, learn more cards (MUS2640, MUS2850, and IN3050 Introduction to Artificial Intelligence and Machine Learning). The gallery description moves to `gallery.md`.

### Tips and tricks (`tips-and-tricks.ipynb`)

Sections: prompt craft that transfers across tools; keeping a decisions and prompt log; writing about AI-made work (describe before you interpret; name the tool, model, version, date, and seed); citing models, datasets, and generated material; figures and captions for generated images; privacy and accounts at UiO; running models locally; preparing the portfolio and the gallery presentation; study technique for a flipped course.

### Glossary (`glossary.md`)

MyST `{glossary}` block, roughly 120 terms, each a one- or two-sentence reminder. Terms are those set in bold at first use in the chapters.

### Tools (`tools.md`)

The categorised tool lists from the current overview, with the turnover warning, one open alternative per category, and the course's own web apps listed first.

### Gallery (`gallery.md`)

The Synthetic Gallery: format, requirements, delivery list, examples of strong projects, the page template, consent options, and the archive of past cohorts.

## 8. Web apps

Conventions, copied from `sensingsoundandmusic/book/apps/`:

- One folder per app under `book/apps/<name>/` with a single `index.html`; vendored libraries live beside it and keep their licences.
- Same CSS variables and light/dark palette as the *Sensing Sound and Music* apps, system font, max width 780 px, keyboard operable, `aria-pressed` on toggles.
- One intro paragraph at the top saying what the app shows and that nothing leaves the browser.
- Copied to `_build/html/apps/` by the deploy workflow and the local verify script, and listed in `book/apps/README.md`.
- No API keys, no network calls after load. Bundled data (vocabularies, vectors, sample clips, a small splat) is capped at a few megabytes per app and listed with its licence.

First batch, in build order:

1. Training loop playground (week 2)
2. Next-token sampler (week 2)
3. Tokeniser explorer (week 4)
4. Forward diffusion explorer (weeks 2 and 5)
5. Inference energy estimator (week 3)
6. Provenance inspector (week 3)
7. Word-vector explorer (week 4)
8. Markov melody generator (week 6)
9. Agent loop simulator (week 11)
10. Rhythm-bot (week 12)

Second batch, after the chapters are in place: seed-and-guidance grid viewer, frame-consistency inspector, splat viewer, cross-modal sketchpad, sensor-to-sound mapper, small language model in the browser. Bring-your-own-key apps are out of scope for now.

## 9. Assessment

Unchanged in weight and philosophy. Milestones move as in the schedule: A1 due week 2, A2 due week 5, ethics essay due week 7, A3 due week 8, proposal due week 10, final project due end of week 12, Synthetic Gallery in the exam period. The weekly log keeps three paragraphs, now in the order Explore, Reflect, Create. The process memo keeps the two questions, surprise and will.

## 10. Relationship to Sensing Sound and Music

- Creative AI is standalone: every concept it needs is taught in its own pages.
- Four chapters carry an "If you took MUS2640" note (weeks 2, 6, 10, 12) linking to *The brain*, *Machine listening*, *Tuning in*, *Vision*, and *The body*.
- The sound chapter starts at the analysis-to-generation turn where *Machine listening* ends, and links to the live spectrogram app there rather than rebuilding it.
- The body chapter uses the movement, motion, action, gesture terminology from *Sound Actions* and *The body* without re-deriving it.
- The overview's "reading a claim" checklist is the same claim, evidence, method, limits checklist as in the other book, applied to model cards, benchmarks, and company announcements.
- The learn-more cards point both ways: MUS2640 lists Creative AI, and Creative AI lists MUS2640 and MUS2850.

## 11. Repository and infrastructure

- Add `linkcheck.yml` and `accessibility.yml` workflows, copied from the other repository and adjusted for this one.
- Extend `deploy.yml` and `scripts/verify-book-build.sh` to copy `book/apps` into the built site.
- Move figures into per-chapter folders and update all figure paths.
- Add `book/templates/practice-log.md` and `book/templates/gallery-page.md`.
- Update `myst.yml` table of contents to the new files and extra pages.
- Extend `references.bib` with, at minimum: Vear 2021 on musicking robots; the 2026 Frontiers paper on inverse and indirect mappings in embodied AI; the Oxford Handbook of 4E Cognition; Jensenius 2022 *Sound Actions*; the Dr. Squiggles and ZRob publications; the Gaussian splatting paper is already present; presence research for XR; AI-text detector evaluations; image memorisation studies; energy and water estimates for inference. Every entry gets a DOI or URL.
- Keep code as fenced listings except for light, offline numpy and matplotlib cells that produce figures, which become executed cells as in the other book. No cell may need a GPU, key, or network.
- Update `README.md` to describe the new structure, the apps, and the CI checks.

## 12. Writing style

Follow *Sensing Sound and Music*:

- Explanatory prose in the second person, British spelling with -ise, short paragraphs, one idea per paragraph.
- Describe before you interpret; hedge claims and cite them; prefer "what the evidence shows" to "what everyone knows".
- Product names only on the tools page and in Dig deeper notes; chapters talk about categories.
- Every non-obvious claim about capability carries a year, since the field moves.
- Bold for a term at first definition only; those terms go into the glossary.
- Admonition classes: `question`, `tip`, `note` with "Dig deeper" or "Going deeper" prefixes, `important` for definitions and learning outcomes, `spotlight` for research spotlights, `seealso` for further reading.
- Cite with `[@Key]` as the current draft does; MyST resolves both styles.

## 13. Out of scope

- Beamer lecture decks (the other book has experimental decks; consider after the chapters are stable).
- Norwegian translation.
- Any app that needs an API key or a server.
- The physical logistics of the gallery, headsets, sensors, or robots; the chapters describe activities and name what is available to borrow.

## 14. Implementation order

1. Infrastructure: workflows, verify script, apps copy, figure folders, TOC, templates.
2. Overview, tools, gallery, tips-and-tricks pages, glossary skeleton.
3. Chapters in week order, each with its research spotlight, critical look, summary, questions, further reading, and references.
4. First-batch apps alongside the chapters that use them.
5. Glossary fill-in from bolded terms, cross-link pass, link check, accessibility check, full executed build.
