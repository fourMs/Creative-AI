# Glossary

This page collects the technical vocabulary of the book in one place, as a lookup list for revision and for writing your reflections. Every term is explained in context in the chapters, so treat these short definitions as reminders rather than as first introductions.

```{glossary}
Agent
: A system given a goal that chooses its own steps, calling tools in a loop of plan, act, and observe until a stopping condition is met.

Anarchive
: A computational memory that holds no fixed documents but continuously reorganises cultural traces into new generative forms, a term proposed by Pierre Cassou-Noguès and Gwenola Wagon. Chapter 3 uses it for the latent space of a trained model, where provenance is unstable and meaning is relational rather than documentary.

Audio–video and auditory–visual
: Audio and video name data, the recorded, transmitted, or generated signal; auditory and visual name perception and processing, whether in a person or in a machine. A film is an audio–video artefact, and watching it is auditory–visual. The book keeps the two apart rather than folding them into a single word that means both.

Cellular automaton
: A grid of cells whose states update together at each step according to a rule that looks only at each cell's neighbours. Simple rules can produce elaborate patterns, as in Conway's Game of Life.

Conditioning
: Any input besides noise that steers what a generative model produces, such as a text prompt, a reference image, a mask, or a control signal.

Diffusion model
: A generative model trained to remove noise step by step, so that it can turn pure noise into a coherent image, sound, or video.

Evolutionary algorithm (genetic algorithm)
: A search method that keeps a population of candidate solutions, scores them, and repeatedly makes a new population by copying the better ones with small random changes and recombinations.

Fitness function
: The score an evolutionary algorithm optimises, saying how good a candidate is. When a person supplies the score by choosing favourites instead, the search becomes interactive evolution.

Foundation model
: A very large model trained once on broad data and then adapted to many tasks by prompting or fine-tuning.

Hallucination
: A fluent, confident output that is false, a direct consequence of training a model to produce plausible rather than true text.

Inference
: Using a trained model to produce an output from an input; the parameters do not change.

Interactive evolution
: An evolutionary loop in which a person, rather than a written fitness function, selects which candidates survive; used to breed images, shapes, and sounds by eye.

L-system
: A rewriting grammar that repeatedly replaces symbols in a string according to a small set of rules, then reads the result as drawing instructions. It is a common way to generate branching forms such as plants.

Large language model (LLM)
: A transformer trained to predict the next token in text, on which chat, coding, and reasoning behaviours are built.

Modality
: In this book, a kind of data a model takes in or puts out: text, image, audio, video, 3D geometry, motion data. Psychology uses the same word for a sense, and where this book means perception it says sensory modality, or names the sense as auditory, visual, or tactile.

Multimodal and multisensory
: Multimodal describes models and data that combine several kinds of data, such as text with images or audio with video. People are multisensory rather than multimodal, since they combine senses rather than data types. Cross-modal correspondences, the reliable matches people make across the senses, keep their established name.

Procedural generation
: Building content such as terrain, levels, textures, or music from an algorithm and a seed rather than authoring every element by hand.

Prompt
: The text (and sometimes images or audio) given to a model to condition its output; the main interface of current generative tools.

Quantum machine learning
: A research area proposing to run parts of a learning or sampling algorithm on quantum hardware. As of 2026 it has shown no demonstrated advantage for training or running generative models.

Rule-based system
: A generative or reasoning system whose behaviour is written out by hand as explicit rules, grammars, or constraints rather than learned from data.

Token
: The unit a language model reads and writes, usually a word piece; Norwegian text uses more tokens than the same text in English.

Training
: Repeatedly adjusting a model's parameters to reduce a loss measured on batches of data.
```
