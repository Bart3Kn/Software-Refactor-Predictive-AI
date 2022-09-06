# Software-Refactor-Predictive-AI
My master's research project carried out alongside my professor, Mahir Arzozky.



The research project aims to interpret Java projects to look for Classes and look at the dependencies between them through the usage of referencing and class usage.
It will then usage the reference data to create a multiple dependency graph (MDG) that is stored as a matrix (n by n size) with n being the number of classes with the project.

This allows me to form an 'image' of the project architecture and use it for analysis throught a Convolutional Neural Network to look for patterns and trends.
This can be used to look for refactor location within the code.

To train a model on where refactoring should occur, time series of a large scale project can be used to identify where locations of refactors should occur or how classes should be split up based on code smells.
