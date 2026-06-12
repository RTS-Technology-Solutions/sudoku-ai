# Soduku AI Project
*by Pat Snyder*
*Created: 2026-06-11*

This project implements a series of solvers for the game Sudoku. 


## Model Analytics Project Readme:

*Breaking the Boundaries of the "Black Box"*

### Overview

A machine learning project designed to strip away the "magic" of neural networks by treating model weights not as a mysterious unknown, but as observable, temporal numbers with defined impacts. 

Using a custom-built Sudoku solver as the canvas, this project maps internal matrix multiplications directly back to human-comprehensible concepts. By translating raw data into clear visual metaphors, we trace "the idea" that led to "the decision," mirroring the complete transparency of chess engine bitboards.

#### Phase 1: Architectural Coverage
- Layer 1 (The Lens Stack): Implements a Mixed Convolutional (Inception-style) Layer using 6 parallel, rule-agnostic geometric filter shapes (2 x 2, 3 x 3, 4 x 4, 2 x 6, 1 x 5, 5 x 1) with 16 variations each, yielding 96 total feature channels.
- Layer 2 (The Synthesizer): Compresses the 96 raw perspectives down to 32 combined channels, forcing the network to synthesize micro-patterns into high-level structural concepts.

#### Phase 2: Analytics & Visualizing the Machine
- Weight Auditing: Extracting raw floating-point matrices post-training to isolate and identify "dead" vs. highly weighted channels.
- Feature Map Snaps: Exporting 9 x 9 grayscale visual snapshots of Layer 1 and Layer 2 to explicitly show what the model "sees" and "prioritizes" mid-decision.
- The Metaphor Layer: Translating mathematical matrices into strategic narratives to bridge the gap between computer bytes and human understanding.

#### Phase 3: Feedback & Tuning
- Iterative Refinement: Using insights from the analytics phase to adjust architecture, training data, and hyperparameters in a transparent, feedback-driven loop.
- Consider regularization techniques such as nn.Dropout2d to encourage the model to learn more robust, generalizable features rather than overfitting to specific patterns in the training data.
- Implement model training continuation and checkpointing to allow for longer training runs and the ability to resume training from previous models.


### Project Updates:
- **2026-06-11**: Initial project setup with data generation and one-hot encoding scripts. Basic CNN architecture defined.
- **2026-06-12**: Training loop implemented with live loss plotting and early stopping.
- **2026-06-12**: Initial training runs completed with preliminary results. Observed inverse training loss in early epochs indicating low initial intelligence but rapid learning. Identified crossover at epoch 8 indicating validation loss improvement, but sharpness of crossover suggests mild overfitting. Lastly, volatile validation loss in later epochs suggests a learning rate that is too high, causing the optimizer to take too large of steps.
- **2026-06-12**: Implemented model checkpointing to save epoch checkpoints and allow for training continuation. Added regularization techniques such as nn.Dropout2d to encourage more robust feature learning.  Introduced a learning rate scheduler to monitor validation loss and detect the volatile bouncing pattern that was observed (optim.lr_scheduler.ReduceLROnPlateau, shrink learning rate from 0.001 to 0.0001).