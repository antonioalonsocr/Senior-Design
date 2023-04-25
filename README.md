# Senior-Design
The ```raspberry_pi_python``` folder holds all the files in the Raspberry Pi Pico.
Special attention can be paid to ```/raspberry_pi_python/main.py``` as this is the main script that facilitates the communication between the Rasperry Pi Pico, two MAX17330s (by Analog Devices, Inc.), and the LCD.<br><br>

### Python Libraries
Within the ```/raspberry_pi_python/libraries``` directory, you can locate the Python libraries that we created and use in ```main.py```. Here 
- ```chipClasses.py``` contains class definitions for our I2C functions in communication with the MAX17330 integrated chip (IC). Some functions include accessing the I2C slave device and its internal registers to reading battery percentage and current through the MAX17330 and converting the read value to an approrpiate resolution.
- ```gpio_LCD.py``` contains LCD GPIO function definitions specific to our LCD model, the FocusLCDs 40x2 (182x33.5) LCD, C402ALBSBSW6WN33XAA.
- ```LCD_prints.py``` contains functions useful for printing to our LCD, e.g., a dynamic character animation that scales to the battery's state of charge (battery percentage).<br><br>

### Reports and Documents
Within the ```/raspberry_pi_python/reports_and_documents``` directory, you can locate all of our reports, relevant documents, and diagrams from the Fall 2022 and Spring 2023 semesters for our senior design project.