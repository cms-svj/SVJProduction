# GenMassAnalyzer

## Introduction

This README mainly explains how the jet categorization algorithm in GenMassAnalyzer.cc works for the SVJ tchannel analysis at GEN level.

## Jet Categorization Algorithm

Looking at only events with at least one jet, we looped through all the gen particles in the event. In the description below, I will often refer to the "particle list" as the list of all the particles in the particle decay tree (similar to what you see in https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCandidateModules#ParticleListDrawer_Utility).

1. The function `lastDarkGQ` identifies and groups the last copies of dark gluons, dark quarks, and dark hadrons separately. These groups are called dQPart, dGPart, and dHPart respectively. `lastDarkGQ` also stores the last descendants of the last dark hadrons in a vector called lastD. lastD is used in the calculation of the dark pT of each jet.

2. The function `firstDark` then identifies and groups particles that are the immediate daughters of the first dark particles in the particle list. These immediate daughters often correspond to the final state particles in the tree level diagram. For example, in a direct production diagram, there are two dark quarks in the final state. In that case, `firstDark` will identify these two dark quarks. With `firstDark`, we get the following groups of particles:

* fdMPart: dark mediators that are immediate daughters of the first dark particles
* fdQPartFM : dark quarks that are daughters of the dark mediators from fdMPart.
* fSMqPart: SM quarks that are daughters of the dark mediators from fdMPart.
* fdQPart: dark quarks that are immediate daughters of the first dark particles.
* fdGPart: dark gluons that are immediate daughters of the first dark particles.

These groups of particles help us determine where the particles found in step 1 come from. I will sometimes refer to the particles in the list above as "first particles".

3. We also group stable dark particles in a list called stableD, but we are not using this list in any part of the code now.

4. In this step, we loop through the jets in the event, and we only look at AK8 jets with pT > 200. If we find any last dark particles from dQPart or dGPart (see step 1) within delta R of 0.8 of the jet, the jet is classified as a dark jet, otherwise it is classified as an SM jet. If the jet is a dark jet, we also keep track of the last dark particles that are found within its radius in the list dPartTrack. All this is done using the function `checkDark`.

5. Then we calculate the dark pT fraction over the jet's pT for all the dark jets in the event using the function `darkPtFract`. We store the daughters of the jets that appear in the lastD vector from step 1. We add the 4-vectors of all these daughters and call the resultant pT the dark pT of the jet. dJPts is the vector that stores the dark pT fractions of all the dark jets in the event. This implies that the stable dark particles are not included in the calculation.

6. It is possible for the last dark particles in dQPart or dGPart from step 1 to appear within the radius of more than one jet. In that case, we need to decide which jets these particles "really" belong to. We first sort all the dark jets in the event using the `sort_permutation` and `sortByDPt` functions. If a last dark particle appears in two dark jets, only the dark jet with the higher dark pT fraction "really" owns that particle. After deciding which jets these last dark particles "really" belong to, it is possible for us to end up having a dark jet that doesn't "really" contain any last dark particles. That dark jet is then reclassified as an SM jet. This reclassification is done using the `reclassToSM` function.

7. So far we only have two categories of jets: dark and SM jets. We can further classify each category by finding out where the jets' constituents come from. This is where we use the list from step 2.

8. The SM jets can be classified as

* SMM: if particles from fSMqPart are found within the jet.
* SM: if none of the particles from fSMqPart are found within the jet.

9. The dark jet can be further classified into 12 categories. The function `isfj` first labels the dark jets based on which particles from the groups in step 2 are found within the radii of the dark jets. For example, a dark jet is labeled "dq" if we find a particle from fdQPart within the dark jet. It is possible for a dark jet to have multiple labels at this point, because it is possible to find more than one kind of "first particles" in the radius of the jet. Depending on what labels a dark jet contain, the function `DarkClass` then puts these jets in the following sets:

* G_         : first dark gluons.
* QM_        : first dark quarks from the mediators.
* Q_         : first dark quarks not from the mediators.
* QM_Q       : first dark quarks from and not from the mediators.
* QM_G       : first dark quarks from the mediator and dark gluons.
* Q_G        : first dark quarks not from the mediator and dark gluons.
* G_SM       : first SM quarks from the mediators and dark gluons.
* QM_SM      : first dark and SM quarks both from the mediators.
* Q_SM       : first dark quarks not from the mediator and SM quarks from the mediators.
* LD_lowDF  : no first particles found; dark pT fraction < 0.7.
* LD_highDF : no first particles found; dark pT fraction > 0.7.
* LD_SM     : no first dark particles found, but does have SM quarks from mediators.

These categories are mutually exclusive. For example, even though a QM_Q jet contains first dark quarks from the mediators, it doesn't show up in the QM_ jet category.

## Pseudocode for Each Function

### lastDarkGQ

1. While looping through all the particles in the event, check and see if the particle's PDG ID is dark and the particle is the last copy in the particle list.
2. If yes, we save the particle's TLorentzVector and index in vectors dPartList and dPartList_label respectively.
3. If the PDG ID is a dark hadron ID, we use the function `lastDau` on the particle.

### lastDau

1. Loop through the daughters of the last dark hadrons.
2. If a daughter doesn't have any more daughters, we save the daughter in a vector called lastD.
3. Otherwise, if the daughter has other daughters, we would use this function `lastDau` on the daughter. The idea is that a daughter that doesn't have any more daughters is a last descendant, and lastDau wants a vector of all the last descendants from the dark hadrons. Note that the stable dark hadrons are not included in the vector.

### firstDark

1. While looping through all the particles, check and see if the particles have the PDG IDs of dark quarks, dark gluons or dark mediators.
2. If the particle is dark, we look at that particle's first mother.
3. If the first mother is dark, we look at its first mother. We repeat this process until we get a non-dark first mother. The idea is that the mother(s) of the first dark particles must have come directly from SM particles.
4. If the first mother of the particle is not dark, the particle's daughters are considered the first dark mediators, quarks, or gluons. fdMPart, fdQPart, and fdGPart are vectors that store the first dark mediators, quarks and gluons respectively.
5. We use the function `medDecay` on the first dark mediators to get the first daughters of the first dark mediators. These daughters are useful for telling us whether a dark jet comes from a mediator.
6. This algorithm actually double counts the first dark particles, so we use the function `remove` to make sure that we only have unique items in the vectors fdMPart, fdQPart, and fdGPart.

### medDecay

1. Looping through the daughters of the first dark mediators, see if the daughters have the dark mediator IDs.
2. If the daughters are still dark mediators, loop through their daughters and perform the same check. Repeat this until we get the daughters that are not dark mediators. The idea is that, the dark mediators produced on shell may not decay "immediately" in the particle list. They may remain as dark mediators for a while before they decay to other particles.
3. If the daughters are not the dark mediators, store the TLorentzVectors of the daughters to the vectors fdQPartFM, fdGPartFM, and fSMqPart, if the daughters are dark quarks, dark gluons, and SM particles respectively. From the samples tested so far, fdGPartFM is actually empty, so this vector actually wasn't used in the script. There is no dark gluon that came immediately from a dark mediator.
4. There is a double counting problem similar to the one described for `firstDark`. So we need to use the `remove` function on fdQPartFM, fdGPartFM, and fSMqPart as well.

### checkDark

1. Looping through all the AK8 jets with pT > 200 in the event, we check and see if the particles from dQPart and dGPart are found within a deltaR < 0.8 of the jets.
2. If those last dark particles are found within an AK8 jet, that AK8 jet is considered a dark jet and inserted in the vector dJets.
3. Otherwise, the jet is considered an SM jet and inserted in the vector SMJets.

### darkPtFract

1. For each dark jet in the event, loop though the daughters and see if the daughters appear in the vector lastD (see functions lastDarkGQ and lastDau).
2. If the daughters appear in lastD, their 4 vectors are added together. The pT of the resultant 4 vector is considered the dark pT of the jet.
3. Dividing the dark pT by the pT of the jet, we get the dark pT fraction of the jet. Note that stable dark hadrons are not included in this calculation.

### sort_permutation and sortByDPt

1. sort_permutation looks at the dark pT fractions of the dark jets in the event and sorts them in descending order.
2. sort_permutation returns a vector of indices that corresponding to the sorted order.
3. sortByDPt loops through the vector dJets (as well as the vector dPartTrack) and sort the jets according to the order given by sort_permutation in step 2.

### reclassToSM

1. dPartTrack is a vector that contains sets of integers. These integers are the indices of the particles when we are looping over all the particles in the event. In each event, we not only record the dark jets in dJets, but we also record the particles from dQPart and dGPart that are found within the dark jets in dPartTrack. The first entry in dPartTrack is a set of last dark particles (from dQPart and dGPart) that are found in the first dark jet, the second entry is a set of last dark particles found in the second dark jet etc.
2. Looping through dPartTrack, we compare two sets of last dark particles at a time to see if there is any overlap. The dark particles that appear in both sets are stored in a vector called comval. After that, those particles in comval are removed from the set corresponding to lower dark Pt fraction (this is just the set with the larger loop index, since dPartTrack was sorted by dark pT fraction).
3. After erasing overlapping dark particles, we loop through dPartTrack again and record the indices of the empty sets (empty after removing overlapping dark particles).
4. The jets in dJets whose indices correspond to the indices of the empty sets from step 3 are deleted from dJets and inserted into SMJets.

### isfj

1. Looping through the dark jets in dJets, we see if the first/dark particles from fdQPart, fdGPart, fdQPartFM, fSMqPart, and lastDPL (dQPart + dGPart) are found within the deltaR < 0.8 of the jets.
2. We attach different labels to each dark jet depending on what first/last dark particles are found. For example, "dq" is a label for finding particles from fdQPart in the jet. A jet may have multiple labels. The list below shows the labels and their corresponding lists of first particles:

* "dq"   : fdQPart, first dark quarks not from mediator.
* "dg"   : fdGPart, first dark gluons not from mediator.
* "dqm"  : fdQPartFM, first dark quarks from mediators.
* "SMqm" : fSMqPart, first SM quarks from mediators.
* "lD"   : lastDPL, last dark quarks and gluons not from mediators. All the dark jets have this label.

3. This information is stored in a vector called dJetswL. This vector is a vector of a class named dJetsLab. A dJetsLab object has two components: a jet and a set of labels that indicate the origin of the last dark particles.

### DarkClass

1. Looping dJetswL, which contains the dark jets and their corresponding sets of labels, we see which jet category a jet belongs to based its set of labels.
2. For each jet category, we have two sets of labels: labels that should be present and labels that should not be present. For example, G_ is the jet category that stands for dark gluon jets that did not come from mediators. A G_ jet therefore should only contain {"dg","lD"} in its labels and none of the other labels. The list below shows the different sets of labels for different jet categories.

* G_    : {"dg","lD"}
* QM_   : {"dqm","lD"}
* Q_    : {"dq","lD"}
* QM_Q  : {"dqm","dq","lD"}
* QM_G  : {"dqm","dg","lD"}
* Q_G   : {"dq","dg","lD"}
* G_SM  : {"dg","SMqm","lD"}
* QM_SM : {"dqm","SMqm","lD"}
* Q_SM  : {"dq","SMqm","lD"}
* LD    : {"lD"}
* LD_SM : {"lD","SMqm"}

3. In the case of jets that contain only the "lD" label, we split the jets into the LD_lowDF and LD_highDF categories if the dark pT fractions of the jets are < 0.7 and > 0.7 respectively.
