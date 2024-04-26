# HAB_Spring_2024
Software for two High Altitude Ballon (HAB) payloads.  

There were two payloads, one collecting data for a database. 


## Control
The control payload was wirtten in C++. 

We needed this payload to measure temperature, humidity, pressure, altitude, gas resistance. 
All of this data was sotred on an sd card, and will be added to a 5-year database. 



## Research 
This payload was written in CircuitPyhton. 

This payoad measured accleraton on all axis, environmental data, C02, and battery information. 

This software differs from the control payload because it stores data in the buil in FLASh and SD card. 
This allows us to have a backup system in case of catastrophic failures. 

