# Glossary

This page collects the technical vocabulary of the book in one place, as a lookup list for revision and for writing your reflections. Every term is explained in context in the chapters, so treat these short definitions as reminders rather than as first introductions.

```{glossary}
Agent
: A system given a goal that chooses its own steps, calling tools in a loop of plan, act, and observe until a stopping condition is met.

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
