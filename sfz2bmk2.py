class Instrument:
    def __init__(self):
        self.samples = []

        self.vels = set()
        self.minVel = Attrib2Sample()
        self.maxVel = Attrib2Sample(False)

        self.pitchs = set()
        self.minPitch = Attrib2Sample()
        self.maxPitch = Attrib2Sample(False)

    def __str__(self):
        result = "Instrument:"
        for s in self.samples:
            result += "\n" + str(s)
        return result

    def getAllSamples(self):
        return self.samples

    def getSample(self, pitch, velocity):
        temp = self.minVel.get(velocity)
        #print "vmin:", len(temp)
        #for s in temp:
        #   print "name:", s.getName()
        result = temp


        temp = self.maxVel.get(velocity)
        #print "vmax:", len(temp)
        #for s in temp:
        #   print "name:", s.getName()
        result = result.intersection(temp)

        temp = self.minPitch.get(pitch)
        #print "pmin:", len(temp)
        #for s in temp:
        #   print "name:", s.getName()
        result = result.intersection(temp)

        temp = self.maxPitch.get(pitch)
        #print "pmax:", len(temp)
        #for s in temp:
        #   print "name:", s.getName()
        result = result.intersection(temp)
        return result

    def addSample(self, sample, pitchRange, velRange):
        self.samples.append(sample)
        self.vels.add(velRange)
        self.pitchs.add(pitchRange)

        self.minVel.add(sample, velRange[0])
        self.maxVel.add(sample, velRange[1])

        self.minPitch.add(sample, pitchRange[0])
        self.maxPitch.add(sample, pitchRange[1])

def testInstrument2Sample():
    instrument = Instrument()
    instrument.addSample(Sample("sample1.wav"), (0,100), (0,50))
    instrument.addSample(Sample("sample2.wav"), (10,110), (40,100))
    instrument.addSample(Sample("sample3.wav"), (50,120), (0,100))


    print "Get 1"
    i1 = instrument.getSample(1,0)
    print "Get 2"
    i2 = instrument.getSample(100,25)
    print "Get 3"
    i3 = instrument.getSample(115,55)
    print "Get 4"
    i4 = instrument.getSample(105,25)

    print len(i1)
    for s in i1:
        print s.getName()
    print len(i2)
    for s in i2:
        print s.getName()
    print len(i3)
    for s in i3:
        print s.getName()
    print len(i4)
    for s in i4:
        print s.getName()

class Attrib2Sample:
    def __init__(self, min = True):
        self.attributes = []
        if min:
            self.predicate = lambda x,y: x <= y
        else:
            self.predicate = lambda x,y: x >= y


    def add(self, sample, value):
        self.attributes.append( (value, sample) )

    def get(self, value):
        result = set()

        for att in self.attributes:
            if self.predicate(att[0], value):
                result.add(att[1])

        return result


def testAttrib2Sample():
    sample1 = Sample()
    sample2 = Sample()
    att = Attrib2Sample()
    att.add(sample1, 11)
    att.add(sample2, 35)

    print len(att.get(20))
    for a in att.get(20):
        print "result"
        print a

class Sample:
    def __init__(self, name = "none.wav"):
        self.name = name
        self.path = name
        
        self.nsamples = 0

        self.basekey = 0
        self.finetune = 0

        self.minkey = 0
        self.maxkey = 127
        self.minvel = 0
        self.maxvel = 127

        self.volume = 0
        self.pan = 0

        self.loopType = 0
        self.loopStart = 0
        self.loopEnd = 0

        self.attack = 0
        self.decay = 0
        self.sustain = 0
        self.release = 0

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


# ----------------------------------------------------
# BMK reading and writing

# Public ---------------

#def read_bmk2(filename):
#    import xml.etree.ElementTree as ET
#    tree = ET.parse(file)
#
#    return tree

def write_bmk2(instrument, filename):
    samples = instrument.getAllSamples()

    import xml.etree.ElementTree as ET
    #<BM2 BPM="120.00000000" FileType="4" MemorySize="618344" ProductType="BMKS" SigDen="4" SigNum="4" VersionMajor="2" VersionMinor="5" VersionRevision="6">
    bm2Tag = ET.Element('BM2')
    bm2Tag.set("BMP","120.0")
    bm2Tag.set("FileType","4")
    bm2Tag.set("MemorySize","618344")
    bm2Tag.set("ProductType","BMKS")
    bm2Tag.set("SigDen", "4")
    bm2Tag.set("SigNum", "4")
    bm2Tag.set("VersionMajor", "2")
    bm2Tag.set("VersionMinor", "5")
    bm2Tag.set("VersionRevision", "6")

    #<KeyboardSampler DisplayName="multi" Name="inst" Order="0" Polyphony="5" PolyphonyMode="0" PresetPath="bmuser:/testMulti/multi/multi.bmk2">
    keyboardSamplerTag = ET.SubElement(bm2Tag, 'KeyboardSampler')
    keyboardSamplerTag.set("DisplayName", "multi")
    keyboardSamplerTag.set("Name", "inst")
    keyboardSamplerTag.set("Order", "0")
    keyboardSamplerTag.set("Polyphony", "5")
    keyboardSamplerTag.set("PolyphonyMode", "0")
    keyboardSamplerTag.set("PresetPath", "bmuser:/testMulti/multi/multi.bmk2")

    #<LinearAHDSR AHDSRAmount="1.00000000" AHDSRInvert="false" AttackAmplitude="0.00000000" AttackTime="0.00000000" DecayAmplitude="1.00000000" DecayTime="0.00000000" HoldTime="0.00000000" KillAfterRelease="true" ModDestScaleParamID="0" ModEnabled="true" ModFollowVoices="true" ModScaleRatio="0.00000000" ModUseKeyAsScale="false" ModUseVelocityAsScale="false" Name="ahdsr0" Order="0" ReleaseTime="0.50000000" SustainAmplitude="1.00000000" _AttackTime="73" _DecayTime="74" _ReleaseTime="76" _SustainAmplitude="75"/>
    LinearAHDSRTag1 = ET.SubElement(keyboardSamplerTag, 'LinearAHDSR')
    LinearAHDSRTag1.set("AHDSRAmount", "1.00000000")
    LinearAHDSRTag1.set("AHDSRInvert", "false")
    LinearAHDSRTag1.set("AttackAmplitude", "0.00000000")
    LinearAHDSRTag1.set("AttackTime", "0.00000000")
    LinearAHDSRTag1.set("DecayAmplitude", "1.00000000")
    LinearAHDSRTag1.set("DecayTime", "0.00000000")
    LinearAHDSRTag1.set("HoldTime", "0.00000000")
    LinearAHDSRTag1.set("KillAfterRelease", "true")
    LinearAHDSRTag1.set("ModDestScaleParamID", "0")
    LinearAHDSRTag1.set("ModEnabled", "true")
    LinearAHDSRTag1.set("ModFollowVoices", "true")
    LinearAHDSRTag1.set("ModScaleRatio", "0.00000000")
    LinearAHDSRTag1.set("ModUseKeyAsScale", "false")
    LinearAHDSRTag1.set("ModUseVelocityAsScale", "false")
    LinearAHDSRTag1.set("Name", "ahdsr0")
    LinearAHDSRTag1.set("Order", "0")
    LinearAHDSRTag1.set("ReleaseTime", "0.50000000")
    LinearAHDSRTag1.set("SustainAmplitude", "1.00000000")
    LinearAHDSRTag1.set("_AttackTime", "73")
    LinearAHDSRTag1.set("_DecayTime", "74")
    LinearAHDSRTag1.set("_ReleaseTime", "76")
    LinearAHDSRTag1.set("_SustainAmplitude", "75")

    #<LinearAHDSR AHDSRAmount="1.00000000" AHDSRInvert="false" AttackAmplitude="0.00000000" AttackTime="3.00000000" DecayAmplitude="1.00000000" DecayTime="3.00000000" HoldTime="0.00000000" KillAfterRelease="false" ModDestScaleParamID="0" ModEnabled="false" ModFollowVoices="true" ModScaleRatio="0.00000000" ModUseKeyAsScale="false" ModUseVelocityAsScale="false" Name="ahdsr1" Order="0" ReleaseTime="3.00000000" SustainAmplitude="1.00000000" _AttackTime="77" _DecayTime="78" _ReleaseTime="80" _SustainAmplitude="79"/>
    LinearAHDSRTag2 = ET.SubElement(keyboardSamplerTag, 'LinearAHDSR')
    LinearAHDSRTag2.set("AHDSRAmount", "1.00000000")
    LinearAHDSRTag2.set("AHDSRInvert", "false")
    LinearAHDSRTag2.set("AttackAmplitude", "0.00000000")
    LinearAHDSRTag2.set("AttackTime", "3.00000000")
    LinearAHDSRTag2.set("DecayAmplitude", "1.00000000")
    LinearAHDSRTag2.set("DecayTime", "3.00000000")
    LinearAHDSRTag2.set("HoldTime", "0.00000000")
    LinearAHDSRTag2.set("KillAfterRelease", "false")
    LinearAHDSRTag2.set("ModDestScaleParamID", "0")
    LinearAHDSRTag2.set("ModEnabled", "false")
    LinearAHDSRTag2.set("ModFollowVoices", "true")
    LinearAHDSRTag2.set("ModScaleRatio", "0.00000000")
    LinearAHDSRTag2.set("ModUseKeyAsScale", "false")
    LinearAHDSRTag2.set("ModUseVelocityAsScale", "false")
    LinearAHDSRTag2.set("Name", "ahdsr1")
    LinearAHDSRTag2.set("Order", "0")
    LinearAHDSRTag2.set("ReleaseTime", "3.00000000")
    LinearAHDSRTag2.set("SustainAmplitude", "1.00000000")
    LinearAHDSRTag2.set("_AttackTime", "77")
    LinearAHDSRTag2.set("_DecayTime", "78")
    LinearAHDSRTag2.set("_ReleaseTime", "80")
    LinearAHDSRTag2.set("_SustainAmplitude", "79")

    #<SimpleFilter DisplayName="FILTER" InsertEffectBypass="true" InsertEffectVoiceProcessing="true" Name="filter" Order="0" ProcessorOutputBusName="Render" SFilterCutoffFrequency="3000.00000000" SFilterFilteringMode="0" SFilterKeyFreqAmount="0.00000000" SFilterResonance="0.25000000" _SFilterCutoffFrequency="70" _SFilterKeyFreqAmount="72" _SFilterResonance="71"/>
    SimpleFilterTag = ET.SubElement(keyboardSamplerTag, 'SimpleFilter')
    SimpleFilterTag.set("DisplayName", "FILTER")
    SimpleFilterTag.set("InsertEffectBypass", "true")
    SimpleFilterTag.set("InsertEffectVoiceProcessing", "true")
    SimpleFilterTag.set("Name", "filter")
    SimpleFilterTag.set("Order", "0")
    SimpleFilterTag.set("ProcessorOutputBusName", "Render")
    SimpleFilterTag.set("SFilterCutoffFrequency", "3000.00000000")
    SimpleFilterTag.set("SFilterFilteringMode", "0")
    SimpleFilterTag.set("SFilterKeyFreqAmount", "0.00000000")
    SimpleFilterTag.set("SFilterResonance", "0.25000000")
    SimpleFilterTag.set("_SFilterCutoffFrequency", "70")
    SimpleFilterTag.set("_SFilterKeyFreqAmount", "72")
    SimpleFilterTag.set("_SFilterResonance", "71")

    sampleId = -1
    layerManager = Bmk2LayerManager(instrument)
    for sample in samples:
        sampleId = sampleId + 1
        #<Keygroup KeygroupBaseKey="63" KeygroupExclusiveGroup="0" KeygroupHighKey="35" KeygroupHighVelocity="100" KeygroupLayer="0" KeygroupLoopToggleMode="false" KeygroupLoopToggleSync="9" KeygroupLowKey="0" KeygroupLowVelocity="0" KeygroupMute="false" KeygroupOneShot="false" KeygroupPan="0.00000000" KeygroupPolyphony="0" KeygroupVolume="1.00000000" Name="kg0" Order="0" ProcessorOutputBusName="IN" ProcessorOutputBusPath="../../">
        KeygroupTag = ET.SubElement(keyboardSamplerTag, 'Keygroup')
        KeygroupTag.set("KeygroupBaseKey", str(sample.basekey))
        KeygroupTag.set("KeygroupExclusiveGroup", "0")
        KeygroupTag.set("KeygroupHighKey", str(sample.maxkey))
        KeygroupTag.set("KeygroupHighVelocity", str(sample.maxvel))
        #find layer for sample
        layerId = layerManager.getLayerId(sample)

        KeygroupTag.set("KeygroupLayer", str(layerId))
        KeygroupTag.set("KeygroupLoopToggleMode", "false")
        KeygroupTag.set("KeygroupLoopToggleSync", "9")
        KeygroupTag.set("KeygroupLowKey", str(sample.minkey))
        KeygroupTag.set("KeygroupLowVelocity", str(sample.minvel))
        KeygroupTag.set("KeygroupMute", "false")
        KeygroupTag.set("KeygroupOneShot", "false")
        KeygroupTag.set("KeygroupPolyphony", "0")
        KeygroupTag.set("KeygroupPan", str(sample.pan))

        # volume dst = (-inf, 6] ; orig = dB
        from math import pow
        volume = pow(10.0, (float(sample.volume)/20.0) )
        KeygroupTag.set("KeygroupVolume", str(volume))
        KeygroupTag.set("Name", "kg"+str(sampleId))
        KeygroupTag.set("Order", "0")
        KeygroupTag.set("ProcessorOutputBusName", "IN")
        KeygroupTag.set("ProcessorOutputBusPath", "../../")
        
        #<ModulationConnection ConnectionDestinationParamID="KeygroupVolume" ConnectionSourceModulationPath="../../ahdsr0" Name="ahdsr0con" Order="0"/>
        ModulationConnectionTag1 = ET.SubElement(KeygroupTag, 'ModulationConnection')
        ModulationConnectionTag1.set("ConnectionDestinationParamID", "KeygroupVolume")
        ModulationConnectionTag1.set("ConnectionSourceModulationPath", "../../ahdsr0")
        ModulationConnectionTag1.set("Name", "ahdsr0con")
        ModulationConnectionTag1.set("Order", "0")

        #<ModulationConnection ConnectionDestinationObjectPath="../../filter" ConnectionDestinationParamID="SFilterCutoffFrequency" ConnectionSourceModulationPath="../../ahdsr1" Name="ahdsr1con" Order="0"/>
        ModulationConnectionTag2 = ET.SubElement(KeygroupTag, 'ModulationConnection')
        ModulationConnectionTag2.set("ConnectionDestinationObjectPath", "../../filter")
        ModulationConnectionTag2.set("ConnectionDestinationParamID", "SFilterCutoffFrequency")
        ModulationConnectionTag2.set("ConnectionSourceModulationPath", "../../ahdsr1")
        ModulationConnectionTag2.set("Name", "ahdsr1con")
        ModulationConnectionTag2.set("Order", "0")

        #<ModulationConnection ConnectionDestinationParamID="KeygroupVolume" ConnectionSourceModulationPath="../../lfo0" Name="lfo0con" Order="0"/>
        ModulationConnectionTag3 = ET.SubElement(KeygroupTag, 'ModulationConnection')
        ModulationConnectionTag3.set("ConnectionDestinationParamID", "KeygroupVolume")
        ModulationConnectionTag3.set("ConnectionSourceModulationPath", "../../lfo0")
        ModulationConnectionTag3.set("Name", "lfo0con")
        ModulationConnectionTag3.set("Order", "0")

        #<ModulationConnection ConnectionDestinationObjectPath="../../filter" ConnectionDestinationParamID="SFilterResonance" ConnectionSourceModulationPath="../../lfo1" Name="lfo1con" Order="0"/>
        ModulationConnectionTag4 = ET.SubElement(KeygroupTag, 'ModulationConnection')
        ModulationConnectionTag4.set("ConnectionDestinationObjectPath", "../../filter")
        ModulationConnectionTag4.set("ConnectionDestinationParamID", "SFilterResonance")
        ModulationConnectionTag4.set("ConnectionSourceModulationPath", "../../lfo1")
        ModulationConnectionTag4.set("Name", "lfo1con")
        ModulationConnectionTag4.set("Order", "0")

        #<SampleRenderer LoopEnd="21566" LoopStart="0" LoopType="0" Name="renderer" Order="0" RendererPitch="1.00000000" Reverse="false" SampleEnd="21566" SampleID="0" SamplePath="multi_samples/s2.wav" SampleStart="0" Streaming="false" Stretch="1.00000000" UseSampleInfo="true" Warp="false">
        SampleRendererTag = ET.SubElement(KeygroupTag, 'SampleRenderer')
        SampleRendererTag.set("LoopEnd", str(sample.loopEnd))
        SampleRendererTag.set("LoopStart", str(sample.loopStart))
        SampleRendererTag.set("LoopType", str(sample.loopType))
        SampleRendererTag.set("Name", "renderer")
        SampleRendererTag.set("Order", "0")
        SampleRendererTag.set("RendererPitch", "1.00000000")
        SampleRendererTag.set("Reverse", "false")
        SampleRendererTag.set("SampleEnd", str(sample.nsamples))
        SampleRendererTag.set("SampleID", "0")
        SampleRendererTag.set("SamplePath", sample.path)
        SampleRendererTag.set("SampleStart", "0")
        SampleRendererTag.set("Streaming", "false")
        SampleRendererTag.set("Stretch", "1.00000000")
        SampleRendererTag.set("UseSampleInfo", "true")
        SampleRendererTag.set("Warp", "false")

        #<PitchModulation ModDestScaleParamID="0" ModEnabled="true" ModFollowVoices="false" ModScaleRatio="0.00000000" ModUseKeyAsScale="false" ModUseVelocityAsScale="false" Name="pitchmod" Order="0" PitchModTune="0.00000000" PitchModeFineTune="0.00000000"/>
        PitchModulationTag = ET.SubElement(SampleRendererTag, 'PitchModulation')
        PitchModulationTag.set("ModDestScaleParamID", "0")
        PitchModulationTag.set("ModEnabled", "true")
        PitchModulationTag.set("ModFollowVoices", "false")
        PitchModulationTag.set("ModScaleRatio", "0.00000000")
        PitchModulationTag.set("ModUseKeyAsScale", "false")
        PitchModulationTag.set("ModUseVelocityAsScale", "false")
        PitchModulationTag.set("Name", "pitchmod")
        PitchModulationTag.set("Order", "0")
        PitchModulationTag.set("PitchModTune", "0.00000000")
        PitchModulationTag.set("PitchModeFineTune", "0.00000000")

        #<ModulationConnection ConnectionDestinationParamID="RendererPitch" ConnectionSourceModulationPath="../pitchmod" Name="pitchmodconnection" Order="0"/>
        SampleRendererModulationConnectionTag1 = ET.SubElement(SampleRendererTag, 'ModulationConnection')
        SampleRendererModulationConnectionTag1.set("ConnectionDestinationParamID", "RendererPitch")
        SampleRendererModulationConnectionTag1.set("ConnectionSourceModulationPath", "../pitchmod")
        SampleRendererModulationConnectionTag1.set("Name", "pitchmodconnection")
        SampleRendererModulationConnectionTag1.set("Order", "0")

        #<ModulationConnection ConnectionDestinationParamID="RendererPitch" ConnectionSourceModulationPath="../../../portamento" Name="portamentoconnection" Order="0"/>
        SampleRendererModulationConnectionTag2 = ET.SubElement(SampleRendererTag, 'ModulationConnection')
        SampleRendererModulationConnectionTag2.set("ConnectionDestinationParamID", "RendererPitch")
        SampleRendererModulationConnectionTag2.set("ConnectionSourceModulationPath", "../../../portamento")
        SampleRendererModulationConnectionTag2.set("Name", "portamentoconnection")
        SampleRendererModulationConnectionTag2.set("Order", "0")


    
    #<Layer LayerID="0" LayerName="LAYER 1" Name="layer0" Order="0"/>
    #<Layer LayerID="1" LayerName="LAYER 2" Name="layer1" Order="0"/>
    #...
    for id in range(layerManager.numLayers):
        LayerTag = ET.SubElement(keyboardSamplerTag, 'Layer')
        LayerTag.set("LayerID",str(id))
        LayerTag.set("LayerName","LAYER "+str(id))
        LayerTag.set("Name","layer"+str(id))
        LayerTag.set("Order","0")
    
    #<LFO LFOAmpOrigin="0.20000000" LFOAmplitude="0.80000001" LFORate="0.05000000" LFOSyncRate="33" LFOType="0" ModDestScaleParamID="0" ModEnabled="false" ModFollowVoices="true" ModScaleRatio="0.00000000" ModUseKeyAsScale="false" ModUseVelocityAsScale="false" Name="lfo0" Order="0" _LFOAmpOrigin="82" _LFOAmplitude="81" _LFORate="83"/>
    LFOTag1 = ET.SubElement(keyboardSamplerTag, 'LFO')
    LFOTag1.set("LFOAmpOrigin", "0.20000000")
    LFOTag1.set("LFOAmplitude", "0.80000001")
    LFOTag1.set("LFORate", "0.05000000")
    LFOTag1.set("LFOSyncRate", "33")
    LFOTag1.set("LFOType", "0")
    LFOTag1.set("ModDestScaleParamID", "0")
    LFOTag1.set("ModEnabled", "false")
    LFOTag1.set("ModFollowVoices", "true")
    LFOTag1.set("ModScaleRatio", "0.00000000")
    LFOTag1.set("ModUseKeyAsScale", "false")
    LFOTag1.set("ModUseVelocityAsScale", "false")
    LFOTag1.set("Name", "lfo0")
    LFOTag1.set("Order", "0")
    LFOTag1.set("_LFOAmpOrigin", "82")
    LFOTag1.set("_LFOAmplitude", "81")
    LFOTag1.set("_LFORate", "83")

    #<LFO LFOAmpOrigin="0.50000000" LFOAmplitude="0.50000000" LFORate="0.00200000" LFOSyncRate="33" LFOType="3" ModDestScaleParamID="0" ModEnabled="false" ModFollowVoices="true" ModScaleRatio="0.00000000" ModUseKeyAsScale="false" ModUseVelocityAsScale="false" Name="lfo1" Order="0" _LFOAmpOrigin="85" _LFOAmplitude="84" _LFORate="86"/>
    LFOTag2 = ET.SubElement(keyboardSamplerTag, 'LFO')
    LFOTag2.set("LFOAmpOrigin", "0.20000000")
    LFOTag2.set("LFOAmplitude", "0.80000001")
    LFOTag2.set("LFORate", "0.05000000")
    LFOTag2.set("LFOSyncRate", "33")
    LFOTag2.set("LFOType", "3")
    LFOTag2.set("ModDestScaleParamID", "0")
    LFOTag2.set("ModEnabled", "false")
    LFOTag2.set("ModFollowVoices", "true")
    LFOTag2.set("ModScaleRatio", "0.00000000")
    LFOTag2.set("ModUseKeyAsScale", "false")
    LFOTag2.set("ModUseVelocityAsScale", "false")
    LFOTag2.set("Name", "lfo1")
    LFOTag2.set("Order", "0")
    LFOTag2.set("_LFOAmpOrigin", "82")
    LFOTag2.set("_LFOAmplitude", "81")
    LFOTag2.set("_LFORate", "83")
    #<Portamento ModDestScaleParamID="0" ModEnabled="true" ModFollowVoices="true" ModScaleRatio="0.00000000" ModUseKeyAsScale="false" ModUseVelocityAsScale="false" Name="portamento" Order="0" PortamentoGlideTime="0.00000000" _PortamentoGlideTime="5"/>
    PortamentoTag = ET.SubElement(keyboardSamplerTag, 'Portamento')
    PortamentoTag.set("ModDestScaleParamID", "0")
    PortamentoTag.set("ModEnabled", "true")
    PortamentoTag.set("ModFollowVoices", "true")
    PortamentoTag.set("ModScaleRatio", "0.00000000")
    PortamentoTag.set("ModUseKeyAsScale", "false")
    PortamentoTag.set("ModUseVelocityAsScale", "false")
    PortamentoTag.set("Name", "portamento")
    PortamentoTag.set("Order", "0")
    PortamentoTag.set("PortamentoGlideTime", "0.00000000")
    PortamentoTag.set("_PortamentoGlideTime", "5")

    from xml.etree.ElementTree import ElementTree
    tree = ElementTree()
    tree._setroot(bm2Tag)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

class Bmk2LayerManager:
    def __init__(self,instrument):
        self.numLayers = len(instrument.vels)
        self.instrument = instrument
        self.layers = {}
        self.nextId = 0
        self.InitLayers()

    def InitLayers(self):
        layers = list(self.instrument.vels)
        layers.sort(key=lambda item: item[0])
        for layer in layers:
            self.layers[layer] = [(self.nextId,set())]
            self.nextId = self.nextId + 1

    def overlap(self,keyGroup, setOfKeys):
        for keyOccuped in setOfKeys:
            print "searching in :",keyOccuped
            if keyGroup[0] <= keyOccuped[1] and keyGroup[1] >= keyOccuped[0]:
                return True

        return False

    def getLayerId(self, sample):
        availableGroups = self.layers[(sample.minvel, sample.maxvel)]
        keyGroup = (sample.minkey, sample.maxkey)
        for possibleGroup in availableGroups:
            occupiedKeysInGroup = possibleGroup[1]
            if not self.overlap(keyGroup, occupiedKeysInGroup):
                occupiedKeysInGroup.add(keyGroup)
                return possibleGroup[0] # id for the group

        # create new Group
        newSet = set()
        newSet.add(keyGroup)
        newGroup = (self.nextId,newSet)
        print "newGroupd:",newGroup
        self.nextId = self.nextId + 1
        availableGroups.append(newGroup)
        
        return newGroup[0] # id for the group

def TestWrite_bmk2():
    instrument = Instrument()
    s1 = Sample("Sample1.wav")
    s2 = Sample("Sample2.wav")
    s3 = Sample("Sample3.wav")
    instrument.addSample(s1, (0,100), (0,127))
    instrument.addSample(s2, (0,100), (0,127))
    instrument.addSample(s3, (0,100), (0,127))

    write_bmk2(instrument, "output.xml")


# Internal -------------

# elem.tag -> tag name
# elem.attrib -> tag attributes
# for x in elem: -> iterate subelements
# elem[0], elem[1] -> access children
def root(tree):
    return tree.getroot()


# ----------------------------------------------------
# SFZ reading and writing
def read_sfz(filename):
    with open(filename) as f:
        content = f.readlines()

        # groups = (data{}, regions[])
        # regions = data{}
        groups = []
        current = None
        currentGroup = None
        for line in NextLine(content):
            if line == "<region>":
                print "reading region..."
                assert currentGroup != None
                current = dict()
                currentGroup[1].append(current)
            elif line == "<group>":
                print "reading group..."
                current = dict()
                currentGroup = (current, [])
                groups.append(currentGroup)
            else:
                keyValuePair = line.split("=")
                current[keyValuePair[0]] = keyValuePair[1]

        instrument = GetInstrumentFromSFZ(groups)
        print instrument

        return instrument
# private----------------
def NextLine(content):
    for line in content:
        line = line.strip()
        if line.startswith("//") or len(line) == 0:
            continue

        # hack around sample containing spaces
        if line.startswith("sample"):
            yield line
            continue

        # hack around lokey, hikey and lovel, hivel  
        # being in the same line separated by space
        line = line.split(" ")
        for l in line:
            yield l

def GetInstrumentFromSFZ(groups):
    instrument = Instrument()
    for g in groups:
        sampleTemplate = readSampleInfo(g[0], Sample())

        for r in g[1]:
            sample = readSampleInfo(r, sampleTemplate)
            
            pitchRange = (sample.minkey, sample.maxkey)
            velRange = (sample.minvel, sample.maxvel)
            instrument.addSample(sample, pitchRange, velRange)

    return instrument

def readSampleInfo(info, template):
    sample = Sample(template.name)
    sample.name      = info.get("sample"           , template.name)
    sample.path      = info.get("sample"           , template.path)
    sample.nsamples  = info.get("end"              , template.nsamples)
    sample.basekey   = info.get("pitch_keycenter"  , template.basekey)
    sample.finetune  = info.get("tune"             , template.finetune)
    sample.minkey    = info.get("lokey"            , template.minkey)
    sample.maxkey    = info.get("hikey"            , template.maxkey)
    sample.minvel    = info.get("lovel"            , template.minvel)
    sample.maxvel    = info.get("hivel"            , template.maxvel)
    sample.volume    = info.get("volume"           , template.volume)
    sample.pan       = info.get("pan"              , template.pan)
    sample.loopStart = info.get("loop_start"       , template.loopStart)
    sample.attack    = info.get("pitcheg_attack"   , template.attack)
    sample.decay     = info.get("pitcheg_decay"    , template.decay)
    sample.sustain   = info.get("pitcheg_sustain"  , template.sustain)
    sample.release   = info.get("pitcheg_release"  , template.release)

    #adjust range to [-1, 1] for [-100, 100]
    sample.pan = float(sample.pan) / 100.0
    assert(sample.pan <= 1.0 and sample.pan >= -1.0)

    sample.loopEnd   = info.get("loop_end"         , sample.nsamples)
    sample.loopType  = GetLoopMode(info)
    return sample

def GetLoopMode(region):
    result = 0
    stringResult = region.get("loop_mode", "none")
    # switch with str to number

    return result

def ConvertFile(filename):
    instrument = read_sfz(filename)
    write_bmk2(instrument, filename + ".bmk2")
