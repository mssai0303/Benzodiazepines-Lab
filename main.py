# -*- coding: utf-8 -*-
# =====================================================================
#  BENZODIAZEPINE LAB  --  main.py   (this is the file you RUN)
# ---------------------------------------------------------------------
#  HOW TO READ THIS FILE (for first-time coders):
#    * Any line that starts with a #  is a COMMENT. Comments are notes
#      for humans. The computer ignores them completely. They are here
#      to explain what each real line of code is doing and WHY.
#    * Everything else is CODE -- the actual instructions the computer
#      follows, one line at a time, from top to bottom.
#    * A "variable" (like  myTauValue = 10 ) is just a labeled box that
#      stores a value so we can use it later.
#
#  WHAT THIS PROGRAM DOES:
#    It builds one realistic brain cell (a pyramidal cell), gives it
#    some input so it fires, adds inhibition (the brakes), and lets you
#    make a "benzodiazepine" by strengthening that inhibition. Then it
#    saves plots and a list of spike times.
#
#  Original model: Bahl et al. 2012, converted to Python.
# =====================================================================


# =====================================================================
# STEP 1:  Load the tools we need ("importing")
# ---------------------------------------------------------------------
#  "import" means: go get some code someone else already wrote, so we
#  can use it here instead of writing it ourselves.
# =====================================================================

from neuron import h        # 'h' is the doorway into the NEURON simulator.
                            # Every NEURON command we use starts with  h.
                            # (Think of h as the remote control for NEURON.)

import simrun               # 'simrun' is a helper FILE in this folder
                            # (simrun.py). It knows how to run the
                            # simulation and draw the result plots, so we
                            # don't have to write that part ourselves.

h.load_file("stdrun.hoc")   # Loads NEURON's standard "run" commands
                            # (the ones that let us start a simulation).
                            # Without this line, NEURON can't run.

h.load_file("nrngui.hoc")   # Loads extra NEURON tools/menus. Safe to keep.


# =====================================================================
# STEP 2:  Set the parameters (the knobs you are allowed to turn)
# ---------------------------------------------------------------------
#  Each line below stores a setting in a variable. Changing these
#  numbers changes how the experiment behaves.
# =====================================================================

h.celsius = 37              # Body temperature in Celsius. Ion channels
                            # behave differently at different temps, so
                            # we set it to 37 C (a warm mammal). Leave it.

sltype = "/"               # The slash used in file paths. "/" works on
                            # Mac/Linux. (Just used to build a filename.)

simname = "testcell"       # A name for this run. The result files will
                            # start with this name so runs don't clash.

plotflag = 1                # Controls the plots:
                            #   0 = don't show plots
                            #   1 = show plots  (use this while working)
                            #   2 = show AND save picture files

batchflag = 1               # Whether this is part of a big batch of runs.
                            # Leave it at 1; not important for this lab.

fstem = "Results" + sltype + simname   # Builds the start of the output
                            # file path, e.g. "Results/testcell".
                            # The + here glues text pieces together.

print("simname = " + simname + ", fstem = " + fstem)  # print(...) shows
                            # text in the output window so you can see
                            # what's happening while the program runs.


# -------------------------------------------------------------------
#  >>> THIS IS THE SETTING YOU CHANGE FOR THE ASSIGNMENT <<<
#
#  myTauValue is the DECAY TIME (in milliseconds) of the GABA_A
#  inhibitory synapses onto the cell -- basically, how LONG each
#  "braking" signal lasts.
#
#  A benzodiazepine makes GABA_A inhibition stronger and longer,
#  so to model the drug you INCREASE this number.
#
#  What to do:
#    1) Leave it at 10 (the control), run the model, note how many
#       times the cell spikes.
#    2) Increase it (try 40, then 100), run again each time, and see
#       what happens to the number of spikes.
#    3) Describe what you found. (You can open cellClasses.py and
#       search for "myTauValue" to see exactly which synapse it sets.)
# -------------------------------------------------------------------
myTauValue = 10             # 10 = control (no drug). Raise it = the drug.


mytstop = 800               # How long to simulate, in milliseconds.
                            # (800 ms = 0.8 seconds of brain activity.)

addSynInputs = 2            # What kind of input the cell gets:
                            #   0 = current injection only
                            #   1 = synaptic inputs only
                            #   2 = BOTH  <-- we use this so the cell
                            #                fires nicely AND has GABA_A
                            #                inhibition for the drug to act on.

# These 3 apply only when addSynInputs is 0 or 2 (i.e. when we inject current):
injectionLevel = 0.4        # How hard we push the cell, in nA (the "gas").
injectionDuration = 500     # How long the push lasts, in ms.
injectionStart = 100        # When the push begins, in ms.

stimPeriod = 125            # Milliseconds between input spikes from the
                            # artificial "partner" cells. 125 ms = 8 per
                            # second (an 8 Hz rhythm).


# =====================================================================
# STEP 3:  Decide how many "partner" cells send signals to our cell
# ---------------------------------------------------------------------
#  An  if / else  makes a choice: IF the condition is true, do the first
#  block; otherwise (else) do the second block.
# =====================================================================

if addSynInputs > 0:              # If we asked for synaptic input...
    numExcCells = 2               # ...use 2 excitatory (gas) input cells,
    numInhDendCells = 2           #    2 inhibitory cells onto the dendrites,
    numInhSomaCells = 1           #    and 1 inhibitory cell onto the soma.
else:                             # Otherwise (current injection only)...
    numExcCells = 0               # ...use no input cells at all.
    numInhDendCells = 0
    numInhSomaCells = 0

ntot = numExcCells + numInhDendCells + numInhSomaCells   # total input cells


# =====================================================================
# STEP 4:  Build the cell and its input cells
# =====================================================================

import define_stimcells      # Another helper file (define_stimcells.py)
                             # that knows how to make the artificial
                             # input cells.
import cellClasses           # The file (cellClasses.py) that defines our
                             # pyramidal cell and its synapses.

# Make the artificial input cells. This helper hands back several lists.
# (A "list" is just a container that holds several things.)
excStimcell_list, inhDendStimcell_list, inhSomaStimcell_list, cells = define_stimcells.make_stim_cells(numExcCells, numInhDendCells, numInhSomaCells, stimPeriod)

# Build the actual pyramidal cell. Notice we hand it myTauValue here --
# THIS is how your assignment setting reaches the cell's GABA_A synapses.
model_cell = cellClasses.reduced_cell_model(myTau=myTauValue)

# Attach the input-cell lists to the cell so it knows who talks to it.
model_cell.excStimcell_list = excStimcell_list
model_cell.inhDendStimcell_list = inhDendStimcell_list
model_cell.inhSomaStimcell_list = inhSomaStimcell_list

# Give the cell its exact "electrical personality" using a preset.
# (init_model1 is one of several presets in the init_models_with_ca folder.)
from init_models_with_ca import init_model1
model_cell = init_model1.setEphysParams(model_cell)   # apply the preset
model_cell.recalculate_passive_properties()           # finish the setup...
model_cell.recalculate_channel_densities()            # ...math NEURON needs

cells.append(model_cell)     # .append(...) adds our finished cell to the
                             # 'cells' list (put it in the box of all cells).


# =====================================================================
# STEP 5:  Wire the input cells to the synapses on our cell
# ---------------------------------------------------------------------
#  A "for loop" repeats the same steps for each item in a list.
#  "for r in range(N):" means "do this once for r = 0, 1, 2, ... up to N".
#  We use loops so we don't copy-paste the same connection code many times.
# =====================================================================

nclist = []                  # An empty list. We'll store each connection
                             # here as we make it. [] means "empty list".

print("excStimcell_list length = ", len(model_cell.excStimcell_list),
      " and preExcDend_list length = ", len(model_cell.preExcDend_list))
                             # len(...) tells us how many items a list has.

# ---- Connect the EXCITATORY (gas) inputs to the excitatory synapses ----
for r in range(len(model_cell.excStimcell_list)):      # for each input cell
    for j in range(len(model_cell.preExcDend_list)):   # for each synapse
        syn = model_cell.preExcDend_list[j]            # pick that synapse
        nc = model_cell.excStimcell_list[r].connect2target(syn)  # wire them
        nclist.append(nc)                              # remember the wire
        nc.delay = 3                                   # ms delay along the wire
        nc.weight[0] = model_cell.excitatory_syn_weight  # how strong it is
        print("adding exc syn from ", r, " to Excitatory synapse #", j)

# ---- Connect the INHIBITORY (brake) inputs onto the DENDRITES ----
for r in range(len(model_cell.inhDendStimcell_list)):
    for j in range(len(model_cell.preInhDend_list)):
        syn = model_cell.preInhDend_list[j]            # a GABA_A synapse
        nc = model_cell.inhDendStimcell_list[r].connect2target(syn)
        nclist.append(nc)
        nc.delay = 3
        nc.weight[0] = model_cell.inhDend_syn_weight   # inhibitory strength
        print("adding inhdend syn ", r, " to inhibitory dendritic synapse #", j)

# ---- Connect the INHIBITORY (brake) inputs onto the SOMA (cell body) ----
for r in range(len(model_cell.inhSomaStimcell_list)):
    for j in range(len(model_cell.preInhSoma_list)):
        syn = model_cell.preInhSoma_list[j]            # a GABA_A synapse
        nc = model_cell.inhSomaStimcell_list[r].connect2target(syn)
        nclist.append(nc)
        nc.delay = 3
        nc.weight[0] = model_cell.inhSoma_syn_weight   # inhibitory strength
        print("adding inhsoma syn from ", r, " to inhibitory somatic synapse #", j)


# =====================================================================
# STEP 6:  Inject a steady current to make the cell fire
# ---------------------------------------------------------------------
#  Only runs if addSynInputs is NOT 1 (i.e. 0 or 2). "!=" means "not equal".
# =====================================================================

if addSynInputs != 1:
    stimobj = h.IClamp(model_cell.soma(0.5))   # an electrode in the middle
                                               # of the soma. soma(0.5) = the
                                               # halfway point of the soma.
    stimobj.delay = injectionStart             # when the current turns on
    stimobj.dur = injectionDuration            # how long it stays on
    stimobj.amp = injectionLevel               # how strong it is (nA)


# =====================================================================
# STEP 7:  Run the simulation and record what happens
# =====================================================================

# Set up "recording vectors" -- containers that save the voltage over time
# at the soma and dendrites, plus the times the cell spiked.
soma_v_vec, dend_v_vec, tuft_v_vec, t_vec, spike_times = simrun.set_recording_vectors(model_cell, nclist)

simrun.simulate(tstop=mytstop)   # <-- THIS actually runs the simulation.


# =====================================================================
# STEP 8:  Save the results to files, then draw the plots
# ---------------------------------------------------------------------
#  "with open(...) as f:" opens a file so we can write into it, and closes
#  it automatically when we're done. \t means a TAB, \n means a NEW LINE.
# =====================================================================

# Save the spike times to a file (one spike per line).
with open("{}_spikes.dat".format(fstem), 'w') as f:
    f.write("{}\t{}\n".format("time", "cell"))     # header row
    i = 1
    for spk in spike_times:                        # for each spike time...
        f.write("{:.2f}\t{}\n".format(spk, i))     # ...write it to the file

# Save the voltage over time to a file (soma, apical, tuft).
with open("{}_voltages.dat".format(fstem), 'w') as f:
    f.write("{}\t{}\t{}\t{}\n".format("time", "soma_v", "apical_v", "tuft_v"))
    for i, v in enumerate(soma_v_vec):             # go through every time step
        f.write("{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\n".format(i*h.dt, v, dend_v_vec[i], tuft_v_vec[i]))

# Draw the plots (voltage trace and spike raster). This is in simrun.py.
simrun.show_output(soma_v_vec, dend_v_vec, tuft_v_vec, t_vec, spike_times, plotflag, fstem)

# ---- THE END. Count the spikes in the plot / in Results/testcell_spikes.dat,
# ----          then change myTauValue near the top and run again! ----
