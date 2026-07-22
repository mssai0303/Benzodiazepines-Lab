====================================================================
  BENZODIAZEPINE LAB  --  read this first
  A pyramidal cell model in the NEURON simulator
====================================================================

Hi! In this lab you'll model how a benzodiazepine drug (like Valium or
Xanax) changes the firing of a brain cell. Don't worry if you've never
coded before -- you only need to change ONE number and run the model.

There is a full step-by-step guide in this folder called
"Benzodiazepine_Student_Guide.pdf" -- open that for the detailed
explanation of everything. This text file is just the quick start.


THE BIG IDEA
------------------------------------------------------------
A benzodiazepine strengthens the brain's natural "brakes" (GABA_A
inhibition). Stronger brakes = the cell fires fewer times. That's the
whole experiment: make the inhibition stronger and watch the spiking
go down.


WHAT YOU'LL CHANGE
------------------------------------------------------------
Open main.py and find this line near the top:

    myTauValue = 10

That number is how long each inhibitory (braking) signal lasts.
Raising it = adding the benzodiazepine. That's the assignment.


HOW TO RUN IT  (do these in order)
------------------------------------------------------------
FIRST TIME? See INSTALL.txt for full setup (installing NEURON into
your RISE Anaconda environment with requirements.txt). Quick version:

1. Install NEURON (with Python) if you don't have it:  neuron.yale.edu
   Or, in your RISE Anaconda environment:  pip install -r requirements.txt
   Open the model folder in a NEURON/Python terminal or in Spyder.

2. Compile the ion channels ONE time. In a terminal, from this folder:
       nrnivmodl            (on Windows use:  mknrndll)
   You only do this once. It reads all the .mod files.

3. Run the model:
       python main.py       (or press the green Run button in Spyder)
   Plots and data are saved into the Results folder.

4. Do the experiment:
   - Run once with myTauValue = 10 (control). Note the number of spikes.
   - Change it to 40, save, run again. Note the spikes.
   - Change it to 100, save, run again. Note the spikes.
   - What happens to the spiking as the number goes up? Write it down.


WHAT TO TURN IN
------------------------------------------------------------
Upload these two files to Blackboard:
    - main.py         (with your changed myTauValue)
    - cellClasses.py  (you don't edit this one -- just include it)
Plus whatever your instructor asked for (a short write-up and/or your
result plot from the Results folder).


IF NOTHING RUNS / TROUBLESHOOTING
------------------------------------------------------------
* "nrnivmodl won't finish / errors on a .mod file" -- make sure you ran
  it from inside this folder, and that NEURON is installed correctly.

* "The cell never spikes" -- check that near the top of main.py you have
  addSynInputs = 2 and injectionLevel = 0.4 . If it still won't fire,
  raise injectionLevel a little (e.g. 0.5).

* "Changing the number does nothing" -- make sure you SAVED main.py
  before running it.

Read the .docx guide for the full explanation. Good luck!
====================================================================
