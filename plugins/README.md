# GenMassAnalyzer

## Introduction

This README mainly explains how the jet categorization algorithm in GenMassAnalyzer.cc works for the SVJ tchannel analysis at GEN level.

## Jet Categorization Algorithm

Looking at only events with at least one jet, we looped through all the gen particles in the event. In the description below, I will often refer to the "particle list" as the list of all the particles in the particle decay tree (similar to what you see in https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCandidateModules#ParticleListDrawer_Utility).

1. Going through the particle list, the function `lastDarkGQ` identifies the last copies of dark hadrons in the particle list. For each dark hadron, the function also finds the last visible descendants and save them in the vector `lastD`.

2. The function `firstDark` identifies and groups particles that are the immediate daughters of the first dark particles in the particle list. These immediate daughters often correspond to the final state particles in the tree level diagram. For example, in a direct production diagram, there are two dark quarks in the final state. In that case, `firstDark` will identify these two dark quarks. With `firstDark`, we get the following groups of particles:

* `fdMPart`: dark mediators that are immediate daughters of the first dark particles
* `fdQPart`: dark quarks that are immediate daughters of the first dark particles.
* `fdGPart`: dark gluons that are immediate daughters of the first dark particles.
* `fdQPartFM`: dark quarks that are daughters of the dark mediators from fdMPart.
* `fSMqPart`: SM quarks that are daughters of the dark mediators from fdMPart.

These groups of particles help us determine where the `lastD` particles found in step 1 could have come from. I will sometimes refer to the particles in the list above as "first particles".

3. We also group stable dark particles in a list called `stableD`, but we are not using this list in any part of the code now.

4. Looping through all the jets in an event, requiring that each jet satisfies pT > 100, we assign a number (`jCatLabel`) to each jet. `jCatLabel` will tell us what the jet contains. This number is based on a base-2 system. The function `checkDark` will add 1 to `jCatLabel` if any of the jet's constituents is found in `lastD`. The function `isfj` adds 2, 4, 8, and 16 to `jCatLabel` if the jet contains particles from fdQPart, fdGPart, fdQPartFM, and fSMqPart respectively. In this context, "contain" means the particle is within deltaR < 0.8 of the jet. For example, if a jet contains contituents from `lastD`, a first dark quark from the mediator (`fdQPartFM`), and a first SM quark from the mediator (`fSMqPart`), then its `jCatLabel=1+8+16=25`.

## Pseudocode for Each Function

### lastDarkGQ

1. While looping through all the particles in the event, check and see if the particle's PDG ID matches the given dark particle ID (in this case, we are only using the dark hadron ID) and the particle is the last copy in the particle list.
2. If the particle is a dark hadron and it is the last copy, then we use `lastDau` to get all the last descendants of this dark hadron.

### lastDau

1. Loop through the daughters of the last dark hadrons.
2. If a daughter doesn't have any more daughters, we save the daughter in a vector called `lastD`.
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

1. Looping through all the AK8 jets with pT > 100 in the event, we check and see if any of the jet constituents are found in `lastD`.
2. If yes, then add 1 to `jCatLabel`, a number that reflects the kinds of particles a jet contains.

### darkPtFract

1. For each dark jet in the event, loop though the daughters and see if the daughters appear in the vector `lastD` (see functions `lastDarkGQ` and `lastDau`).
2. If the daughters appear in `lastD`, their 4 vectors are added together. The pT of the resultant 4 vector is considered the dark pT of the jet.
3. Dividing the dark pT by the pT of the jet, we get the dark pT fraction of the jet. Note that stable dark hadrons are not included in this calculation.

### isfj

1. Looping through the jets, we see if the first SM/dark particles from `fdQPart`, `fdGPart`, `fdQPartFM`, and `fSMqPart` are found within the deltaR < 0.8 of the jets.
2. Depending on what particles are found within the jet, we add different numbers to `jCatLabel`. The list below shows which number to add for which particles:
* `fdQPart`     : 2
* `fdGPart`     : 4
* `fdQPartFM`   : 8
* `fSMqPart`    : 16
