# =====================================================================
#  cellClasses.py  --  defines the cells used in the lab
# ---------------------------------------------------------------------
#  You do NOT need to change anything in this file for the assignment.
#  But it's worth reading the parts marked "IMPORTANT" -- especially the
#  GABA_A synapse section, because that is where your myTauValue setting
#  from main.py actually gets used.
#
#  WHAT IS A "CLASS"? (for first-time coders)
#  A class is like a blueprint or a cookie-cutter. It describes how to
#  build one kind of thing. From one class you can stamp out ("create")
#  as many copies as you want, each with its own settings. Here we have
#  two blueprints:
#    * stimcell           = a simple artificial cell that just fires
#                           spikes to feed input to our real cell.
#    * reduced_cell_model = the realistic pyramidal cell we study.
#
#  A "def" inside a class is a METHOD -- a mini-instruction-list that
#  belongs to that blueprint (for example, "build the shape", "add the
#  channels", "add the synapses").
#  The word "self" just means "this particular cell" -- so self.V is
#  "this cell's voltage", self.soma is "this cell's soma", etc.
# =====================================================================

from neuron import h        # 'h' = the doorway into the NEURON simulator
import math                 # Python's math tools (we use math.sqrt, math.exp)
  
class stimcell():
    def __init__(self):
        self.is_art=1
        self.noiseFromRandom=0
        self.gid=[]
        self.x=0
        self.y=0
        self.z=0

        pp = h.MyNetStim(.5)
        pp.interval = 1000/8 # Gives an 8 Hz rhythm with an interval of 125 ms
        pp.number = 1e9
        pp.noise = 0 # 0 = no noise, same interval every time. 1 = maximum noise, variable interval with poisson mean of 125 ms                
        pp.start = 0
        self.pp = pp

    def is_art(self):
        return 1

    def setnoiseFromRandom(self,ranstream):
        self.noiseFromRandom(ranstream)
    
    def connect2target(self, target, thresh=-10):
        nc = h.NetCon(self.pp, target)
        nc.threshold = thresh
        
        #self.spike_times = []
        #vecrecs = []
        #vecrecs.append(h.Vector())
        #nc.record(vecrecs[0])
        #self.nclist.append(nc)
        #self.spike_times.append(vecrecs[0])

        return nc
        
    def position(self,xp,yp,zp):
        self.x = xp
        self.y = yp
        self.z = zp    
        xpos = xp
        ypos = yp
        zpos = zp    
        #self.pp.position(xpos, ypos, zpos)
        
class reduced_cell_model():
    # __init__ runs automatically when a cell is created in main.py.
    # It's a to-do list: build the shape, then add channels & synapses.
    # 'myTau' is the value main.py passed in (your assignment setting).
    def __init__(self, myTau=0.5):
        self.soma = None
        self.x = 0; self.y = 0; self.z = 0
        self.create_sections()      # make the parts of the cell
        self.build_topology()       # connect those parts together
        self.build_subsets()        # group the parts into handy lists
        self.define_geometry()      # set their sizes
        self.define_biophysics()    # add the ion channels
        self.addSynapses(myTau)     # add the synapses  <-- uses myTau

    # Create the 7 parts (Sections) of the neuron.
    # A Section is one straight piece of the cell (like one branch of a tree).
    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)        # cell body (where spikes happen)
        self.basal = h.Section(name='basal', cell=self)      # lower dendrites
        self.apical = h.Section(name='apical', cell=self)    # the long dendrite going up
        self.tuft = h.Section(name='tuft', cell=self)        # the bushy top
        self.hillock = h.Section(name='hillock', cell=self)  # base of the axon
        self.iseg = h.Section(name='iseg', cell=self)        # start of the axon
        self.axon = h.Section(name='axon', cell=self)        # the output cable

    # Connect the parts end-to-end to build the cell's shape.
    # ".connect(soma(1))" means "attach me to the far end (1) of the soma".
    def    build_topology(self):
        self.basal.connect(self.soma(0.5))     # basal hangs off the middle of soma
        self.apical.connect(self.soma(1))      # apical rises from the top of soma
        self.tuft.connect(self.apical(1))      # tuft sits on top of apical
        self.hillock.connect(self.soma(0))     # hillock at the bottom of soma
        self.iseg.connect(self.hillock(1))     # iseg after hillock
        self.axon.connect(self.iseg(1))        # axon after iseg


    def recalculate_geometry(self):
        self.soma.diam = self.soma.L =  math.sqrt(self.soma_area/self.PI)
        self.basal.diam = self.basal_area/self.PI/self.basal.L    
        self.apical.diam = self.diam_apical    
        self.tuft.diam = self.tuft_area/self.PI/self.tuft.L

    def define_geometry(self):
        self.soma_area = 1682.96028429
        self.basal_area = 7060.90626796
        self.apicalshaftoblique_area = 9312.38528764
        self.tuft_area = 9434.24861189
        self.PI  = 3.1415926535897932384

        # Set spatial resolution of sections
        self.soma.nseg = 1
        self.basal.nseg = 1
        self.apical.nseg = 5
        self.tuft.nseg = 2
        self.hillock.nseg = 5
        self.iseg.nseg = 5
        self.axon.nseg = 1

        # Set dimensions of the sections
        self.basal.L     = 257   
        self.apical.L = 500
        self.tuft.L = 499
        self.hillock.L = 20
        self.axon.L = 500
        self.iseg.L = 25
        self.axon.diam = 1.5
        
        self.iseg.diam = 1.75
        self.hillock.diam = 2.75
        # for seg in self.iseg:
        #     seg.diam = 2.0 - seg.x*.5
            
        # for seg in self.hillock:
        #     seg.diam = 3.5 - seg.x*1.5
            
        #self.iseg.diam=1.8 #(0:1) = 2.0:1.5
        #self.hillock.diam=2.8 #(0:1) = 3.5:2.0

        self.diam_apical = self.apicalshaftoblique_area/self.PI/self.apical.L
        self.recalculate_geometry()
        
    def build_subsets(self):
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

    def recalculate_passive_properties(self):
        for sec in self.axosomatic_list:
            sec.g_pas = 1./self.Rm_axosomatic
            
        for sec in self.apicaltree_list:
            sec.g_pas = self.soma.g_pas*self.spinefactor 
            sec.cm = self.soma.cm*self.spinefactor

    def recalculate_channel_densities(self):        
        # See Keren et al. 2009        
        h.distance(sec=self.soma)
        
        for sec in self.apicaltree_list:
            based = h.distance(self.soma(0),sec(0))
            for seg in sec:
                seg.gbar_kfast = self.soma(0.5).gbar_kfast * math.exp(-(seg.x*sec.L+based)/self.decay_kfast)
                seg.gbar_kslow = self.soma(0.5).gbar_kslow * math.exp(-(seg.x*sec.L+based)/self.decay_kslow)

        d = h.distance(self.soma(0),self.tuft(0))
        if d>0:
            mih = self.tuft.gbar_ih/d
            mnat = (self.tuft.gbar_nat-self.soma(0.5).gbar_nat)/d
        else:
            mih = self.tuft.gbar_ih/self.apical.L
            mnat = (self.tuft.gbar_nat-self.soma(0.5).gbar_nat)/self.apical.L
            
        based = h.distance(self.soma(0),self.apical(0))
        for seg in self.apical.allseg():
            seg.gbar_nat = mnat*(seg.x*self.apical.L+based) + self.soma(0.5).gbar_nat
            seg.gbar_ih = mih*(seg.x*self.apical.L+based)

    # -----------------------------------------------------------------
    #  define_biophysics: inserts the ion channels that make the cell
    #  electrically alive (sodium, potassium, calcium, etc. -- these come
    #  from the .mod files). Different parts get different channels, which
    #  is what gives this cell its realistic behavior.
    #
    #  ADVANCED: you do NOT need to read or change the details below for
    #  this lab. Just know that "sec.insert('nat')" adds the sodium
    #  channel, "sec.insert('kfast')" adds a potassium channel, and so on.
    # -----------------------------------------------------------------
    def define_biophysics(self):
        self.Rm_axosomatic = 15000
        self.spinefactor = 2.0

        self.decay_kfast = 50.0
        self.decay_kslow = 50.0

        self.soma.Ra =  82
        self.basal.Ra = 734 
        self.tuft.Ra = 527

        Ra_apical = 261
        self.apical.Ra =  Ra_apical

        self.hillock.Ra = self.soma.Ra
        self.axon.Ra = self.soma.Ra
        self.iseg.Ra = self.soma.Ra

        for sec in self.all: # 'all' defined in build_subsets
            sec.insert('pas')
            sec.cm = 1.0
            sec.g_pas = 1./15000
            sec.e_pas = -70
        
        for sec in self.ih_list:
            sec.insert('ih')
            for seg in sec:
                seg.ehd_ih = -47

        for sec in self.nat_list:
            sec.insert('nat')
            sec.ena = 55
            sec.vshift_nat = 10

        for sec in self.kfast_list:
            sec.insert('kfast')
            sec.ek = -80

        for sec in self.kslow_list:
            sec.insert('kslow')
            sec.ek = -80

        self.soma.insert('nap')
        self.soma.insert('km')

        self.tuft.insert('cad')
        self.tuft.insert('sca')
        self.tuft.insert('kca')
        self.tuft.eca = 140
        h.ion_style("ca_ion",0,1,0,0,0)

        self.recalculate_passive_properties()
        self.recalculate_channel_densities()
        #self.tuft.gbar_sca = 3.67649485*10 # TODO what is this


    ######################/

    #Define Section lists
    def build_subsets(self):
        """Build subset lists. For now we define 'all'."""
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

        # morphological section lists
        self.axon_list = []
        self.axosomatic_list = []
        self.apicalshaftoblique_list = []
        self.apicaltree_list = []
        self.tuft_list = []
        self.soma_list = []
        self.basal_list = []

        self.axon_list.append(self.hillock)
        self.axon_list.append(self.iseg)
        self.axon_list.append(self.axon)

        self.axosomatic_list.append(self.soma)
        self.axosomatic_list.append(self.basal)
        self.axosomatic_list.append(self.hillock)
        self.axosomatic_list.append(self.iseg)
        self.axosomatic_list.append(self.axon)

        self.apicalshaftoblique_list.append(self.apical)

        self.apicaltree_list.append(self.apical)
        self.apicaltree_list.append(self.tuft)

        self.tuft_list.append(self.tuft)

        self.soma_list.append(self.soma)

        self.basal_list.append(self.basal)

    # Create lists of cell parts that contain each ion channel type
        self.nat_list = []
        self.kslow_list = []
        self.kfast_list = []
        self.ih_list = []

        self.ih_list.append(self.basal)
        self.ih_list.append(self.apical)
        self.ih_list.append(self.tuft)
        
        self.excsyn_list = []
        self.inhdendsyn_list = []
        self.inhsomasyn_list = []

        self.excsyn_list.append(self.basal)
        self.excsyn_list.append(self.apical)
        self.excsyn_list.append(self.tuft)

        self.inhdendsyn_list.append(self.basal)
        self.inhdendsyn_list.append(self.apical)

        self.inhsomasyn_list.append(self.soma)

        self.nat_list.append(self.soma)
        self.nat_list.append(self.hillock)
        self.nat_list.append(self.iseg)
        self.nat_list.append(self.apical)
        self.nat_list.append(self.tuft)

        self.kfast_list.append(self.soma)
        self.kfast_list.append(self.apical)
        self.kfast_list.append(self.tuft)

        self.kslow_list.append(self.soma)
        self.kslow_list.append(self.apical)
        self.kslow_list.append(self.tuft)

    def recordData(self):
        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)

    def addSynapses(self, myTauValue):
        # ===========================================================
        #  IMPORTANT  --  THIS IS THE HEART OF THE ASSIGNMENT
        # -----------------------------------------------------------
        #  This method builds the synapses (the connection points where
        #  input reaches the cell). It receives 'myTauValue' straight
        #  from main.py -- so the number you set there arrives HERE.
        #
        #  Each synapse has three key settings:
        #     tau1 = how fast it turns ON  (rise time, ms)
        #     tau2 = how long it LASTS      (decay time, ms)  <-- the drug knob
        #     e    = the voltage it pulls toward (reversal potential, mV):
        #            e = -75  -> pulls voltage DOWN = INHIBITORY (a brake)
        #            e =  0   -> pulls voltage UP   = EXCITATORY (the gas)
        #
        #  We make three groups of synapses below:
        #     1) GABA_A (inhibitory) on the soma
        #     2) GABA_A (inhibitory) on the dendrites
        #     3) AMPA  (excitatory) on the dendrites
        # ===========================================================

        # These empty lists [] will hold the synapses we create.
        self.preInhSoma_list = []    # inhibitory synapses on the cell body
        self.preInhDend_list = []    # inhibitory synapses on the dendrites
        self.preExcDend_list = []    # excitatory synapses on the dendrites

        s=0
        self.recInhSomaCurrent = []
        for sec in self.inhsomasyn_list:
            syn_ = h.MyExp2Syn(sec(0.5))         # make a synapse (from my_exp2syn.mod)
            self.preInhSoma_list.append(syn_)    # GABA_A synapse on the cell body
            syn_.tau1 = 0.5                      # rise time (ms) -- fixed
            syn_.tau2 = myTauValue               # <== DECAY time = your drug knob!
            syn_.e = -75                         # -75 mV -> this synapse is a BRAKE (inhibitory)


            self.recInhSomaCurrent.append(h.Vector())    
            self.recInhSomaCurrent[s].record(self.preInhSoma_list[s]._ref_i)

            #sprint(cmdstr,"objref recInhSomaCurrent%d", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recInhSomaCurrent%d = new Vector()", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recInhSomaCurrent%d.record(&preInhSoma_list.object(%d).i)", s, s)
            #{execute(cmdstr)}
            s = s + 1

        totInhSoma = s

        s = 0
        self.recInhDendCurrent = []
        for sec in self.inhdendsyn_list:
            syn_ = h.MyExp2Syn(sec(0.5))
            self.preInhDend_list.append(syn_)    # GABA_A synapse on the dendrites
            syn_.tau1 = 0.5                      # rise time (ms) -- fixed
            syn_.tau2 = myTauValue               # <== DECAY time = your drug knob (again)!
            syn_.e = -75                         # -75 mV -> inhibitory (a BRAKE)
            self.recInhDendCurrent.append(h.Vector())        
            self.recInhDendCurrent[s].record(self.preInhDend_list[s]._ref_i)

            #sprint(cmdstr,"recInhDendCurrent%d = new Vector()", s)
            #sprint(cmdstr,"recInhDendCurrent%d.record(&preInhDend_list.object(%d).i)", s, s)
            s = s + 1

        totInhDend = s

        s = 0
        self.recExcCurrent = []
        for sec in self.excsyn_list:
            syn_ = h.MyExp2Syn(sec(0.5))
            self.preExcDend_list.append(syn_)    # AMPA synapse = EXCITATORY (the gas)
            syn_.tau1 = 1                        # rise time (ms)
            syn_.tau2 = 5                        # decay time (ms) -- note: the drug does NOT touch this one
            syn_.e = 0                           # 0 mV -> pulls voltage UP = excitatory
            self.recExcCurrent.append(h.Vector())
            self.recExcCurrent[s].record(self.preExcDend_list[s]._ref_i)

            #sprint(cmdstr,"objref recExcCurrent%d", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recExcCurrent%d = new Vector()", s)
            #{execute(cmdstr)}
            #sprint(cmdstr,"recExcCurrent%d.record(&preExcDend_list.object(%d).i)", s, s)
            #{execute(cmdstr)}
            s = s + 1

        self.totExc = s

        # Synaptic conductances (max)
        # ---- How STRONG each synapse is (its peak size) ----
        # (For this lab you change the DECAY time (myTauValue) above, not these.
        #  But these are also GABA_A knobs -- raising the two inhibitory ones
        #  is another way to strengthen the brakes.)
        self.excitatory_syn_weight = 0.005   # strength of the excitatory (gas) synapses
        self.inhDend_syn_weight = 0.015      # strength of inhibitory synapses on the dendrites
        self.inhSoma_syn_weight = 0.03       # strength of inhibitory synapses on the soma