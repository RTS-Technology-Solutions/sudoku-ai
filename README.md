# Soduku AI Project

This project implements a series of solvers for the game Sudoku. 


## Model Analytics Project Readme:

*Breaking the Boundaries of the Black Box*

### Overview

A machine learning project designed to strip away the "magic" of neural networks by treating model weights not as a black box, but as observable, temporal numbers. 

Using a custom-built Sudoku solver as the canvas, this project maps internal matrix multiplications directly back to human-comprehensible concepts. By translating raw data into clear visual metaphors, we trace "the idea" that led to "the decision," mirroring the complete transparency of chess engine bitboards.

#### Phase 1: Architectural Coverage
- Layer 1 (The Lens Stack): Implements a Mixed Convolutional (Inception-style) Layer using 6 parallel, rule-agnostic geometric filter shapes (2 x 2, 3 x 3, 4 x 4, 2 x 6, 1 x 5, 5 x 1) with 16 variations each, yielding 96 total feature channels.
- Layer 2 (The Synthesizer): Compresses the 96 raw perspectives down to 32 combined channels, forcing the network to synthesize micro-patterns into high-level structural concepts.

#### Phase 2: Analytics & Visualizing the Machine
- Weight Auditing: Extracting raw floating-point matrices post-training to isolate and identify "dead" vs. highly weighted channels.
- Feature Map Snaps: Exporting 9 x 9 grayscale visual snapshots of Layer 1 and Layer 2 to explicitly show what the model "sees" and "prioritizes" mid-decision.
- The Metaphor Layer: Translating mathematical matrices into strategic narratives to bridge the gap between computer bytes and human understanding.

