# Benzodiazepines Lab

This is a short lab I put together for the RISE course. You'll use a computer
model of a real brain cell to see what a benzodiazepine (a calming drug like
Valium or Xanax) does to how that cell fires.

No coding experience needed. For the actual assignment you only change one
number and run the model.

## What's going on, briefly

Benzodiazepines don't shut neurons off. They make the brain's own "brakes"
(a kind of inhibition called GABA_A) work harder. So a cell that was firing
away gets held back more, and it fires less. That's the whole thing you're
going to show.

## Getting the files

Hit the green **Code** button up top, choose **Download ZIP**, and unzip it
somewhere on your computer. Open that folder and you're ready.

## Where to start

Open these, roughly in this order:

- `INSTALL.txt` first. It walks you through the one-time setup (getting NEURON
  working in your RISE Anaconda environment) and how to run the model.
- `READ_ME_FIRST.txt` if you just want the quick version.
- `Benzodiazepine_Student_Guide.pdf` is the full guide. It explains the
  biology, walks through the code line by line, and lays out the assignment.
  If you get stuck or confused, this is the file to read.

## The assignment

1. Get NEURON installed (`INSTALL.txt` shows you how), then compile the parts
   of the model once by running `nrnivmodl` (on Windows it's `mknrndll`).
2. Open `main.py` and find the line `myTauValue = 10`. Run the model and count
   how many times the cell fires (spikes).
3. That `10` is the "no drug" setting. Bump it up to `40`, run it again, then
   try `100`. Each time, notice what happens to the number of spikes.
4. Write up what you saw and why you think it happened.

## What to hand in

- Your `main.py` (with whatever you changed `myTauValue` to)
- `cellClasses.py` (you don't touch this one, just include it)
- A short write-up plus one of the result plots from the `Results` folder

If something won't run, check the troubleshooting notes at the bottom of
`INSTALL.txt` before you panic. And feel free to ask me.

---

The underlying cell model isn't mine. It comes from Bahl, Stemmler, Herz &
Roth (2012), "Automated optimization of a reduced layer 5 pyramidal cell model
based on experimental data," *J Neurosci Methods* 210:22-34 (ModelDB #146026),
converted to NEURON + Python. I adapted it into this benzodiazepine lab for
class.
