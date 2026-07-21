# Benzodiazepines Lab

A short computational lab for students: model how a **benzodiazepine** drug
(like Valium or Xanax) changes the firing of a brain cell, using the
[NEURON](https://neuron.yale.edu) simulator.

You do **not** need any coding experience. You'll change **one number** and
run the model to see the drug's effect.

## The idea in one sentence

Benzodiazepines don't switch neurons off — they turn **up the volume on the
brain's brakes** (GABA_A inhibition). So a firing pyramidal cell gets braked
harder and fires **less**.

## How to get this lab

Click the green **Code** button (top right) → **Download ZIP** → unzip it on
your computer. Then open the folder.

## Start here (in this order)

1. **`INSTALL.txt`** — one-time setup: installing NEURON into your RISE
   Anaconda environment (with `requirements.txt`), and how to run the model.
2. **`READ_ME_FIRST.txt`** — the quick-start summary.
3. **`Benzodiazepine_Student_Guide.pdf`** — the full step-by-step guide: the
   biology, the code explained line by line, and the assignment.

## The assignment (short version)

1. Install NEURON (see `INSTALL.txt`), then compile the channels once:
   `nrnivmodl` (Windows: `mknrndll`).
2. In `main.py`, find `myTauValue = 10`. Run the model and note how many
   times the cell spikes.
3. Increase `myTauValue` (try `40`, then `100`) to model the drug. Run again
   each time and see the spiking go down.
4. Write up what you observed, and submit `main.py` and `cellClasses.py`.

## What to submit

- `main.py` (with your changed `myTauValue`)
- `cellClasses.py` (unchanged)
- A short write-up + your result plot from the `Results` folder

---

*Model based on Bahl A, Stemmler MB, Herz AV, Roth A (2012), "Automated
optimization of a reduced layer 5 pyramidal cell model based on experimental
data," J Neurosci Methods 210:22–34 (ModelDB #146026), converted to
NEURON + Python. Adapted into a teaching lab on benzodiazepine effects.*
