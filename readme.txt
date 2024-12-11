# Author: Daniel Glauber
# File: readme.txt

Project 2:
To run program run the command: python3 sga.py [-h] [-g] [-G] [settings file].
To run bisection you need to set bisection to 1 in the settings file.
To turn bisection off need to set bisection to 0 in the settings file.
I added the settings bisectionThreshold, bisectionStartingPopulation, bisectionMaxGeneration.
These setting control how bisection is run.
The following settings are ignored when running bisection: terminateOnFailure, failuresBeforeTermination.
The setting populationSizeN is controlled by my bisection function.
The same debugging options are available when running bisection.
Bisection will work with both fitness functions.

Project 1:
I added additional settings terminateOnFailure and failuresBeforeTermination.
The setting terminateOnFailure allows the user to turn off the termination failsafe mode.
By default terminateOnFailure is set to 1, which means the termination failsafe is on.
To turn off the termination failsafe set terminateOnFailure to 0.
The setting failuresBeforeTermination allows the user to change failures can occur before the program terminates.
By default failuresBeforeTermination is set to 0, which means the program will terminate after the first failure.
To allow multiple failures before termination you can set failuresBeforeTermination to an integer greater than 0.
If failuresBeforeTermination is set to 1, then 1 failure is allowed before the program terminates.
If the default settings file is not found the program will create the file gasettings.dat, which contains the default settings.
If the user's custom settings file is missing a setting or if a setting's value is formatted incorrectly, the user will be asked if they want to continue running the program using the default settings value for the missing setting. 

Conclusions from Experiments:
The only crossover operator that was not able to complete all the test string sizes was uniform.
It was only able to complete a string size of 24, but that was with the probApplyCrossover setting set to 0.2.
All other crossover operators were run with a probApplyCrossover setting of 0.6.
When running one-point crossover, I found that it was the best operator for running string size of 24.
For both string sizes of 48 and 100, one-point crossover took longer and ended up with larger values for max n and min n than two-point crossover.
Two-point crossover was the clear winner for string sizes larger than 24.

Results from Experiments:
uniform
24: probApplyCrossover 0.2
Final Max N = 80
Final Min N = 75
Final Threshold = 0.06666666666666667
Execution time: 0.9867539405822754 seconds

one-point
24: 
Final Max N = 70
Final Min N = 65
Final Threshold = 0.07692307692307693
Execution time: 0.5745749473571777 seconds

48:
Final Max N = 340
Final Min N = 320
Final Threshold = 0.0625
Execution time: 10.89070987701416 seconds

100:
Final Max N = 1520
Final Min N = 1440
Final Threshold = 0.05555555555555555
Execution time: 109.2048990726471 seconds

two-point
24:
Final Max N = 130
Final Min N = 120
Final Threshold = 0.08333333333333333
Execution time: 0.959205150604248 seconds

48:
Final Max N = 160
Final Min N = 150
Final Threshold = 0.06666666666666667
Execution time: 3.8417489528656006 seconds

100:
Final Max N = 1360
Final Min N = 1280
Final Threshold = 0.0625
Execution time: 87.42322182655334 seconds
