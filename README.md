# Abstract

## Executive Summary:
•	Alexa interacts with Intel Edison to check if someone is standing on the door, clicks the image and emails it to the sender in addition to providing the identity of the visitor via self-implemented facial recognition algorithm. 
•	Alexa emails the picture to the resident so as to confirm its result
•	Alexa also reports the crimes statistics at the granularity of the street level so as to make the user aware of the reported crimes. 

## Problem Scenario:

Knock knock
Who’there ?
</Exactly>

That’s exactly the problem statement. In order to build a better world, we need to hack out the information about the identity of the person standing in front of your door - is that person your friend, stranger or a named criminal? 

## Proposed Solution:
There would be a CCTV camera installed outside the door for live streaming. The resident will ask Alexa to check who’s at the door. Alexa will in turn push the request to our server which will do the background check on the visitor in real-time using our self-devised facial recognition software. Finally, Alexa will reply back to the resident with the identity of the visitor. An email notification would also be triggered to the resident with the image and the identity of the visitor.

Moreover, do you also want to know about the most dangerous streets according to the crime rate, wells, Alexa knows that too! When the resident asks Alexa for the crime rate with a specific zip code, Alexa would reply with the names of the most dangerous streets with the total number of crimes that has occurred on the streets in the last 24 hours. Moreover, Alexa would also inform the resident about the total number of different crimes like shooting, Robbery, Vandalism and any other kind of crime that has occurred at the granularity of street name.


## Target Audience:
Residents with disability
Neighborhood with high crime rate 
People who are a lot lot lazy !
People who really like to own cool stuff


## Flow diagram of the project:

![alt tag](https://github.com/VimanyuAgg/Knock-Knock-Hackster/blob/master/FlowDiagram_KnockKnock.png)




## Implementation:
A server is running on Intel Edison which is interfaced with a webcam to provide live streaming. When the resident asks Alexa to the check who’s at the door, Alexa posts a request to our web server that clicks a snapshot of the person outside that runs face analysis on the captured image using Google Vision API. It, then runs the generated JSON against our database of the images using out face recognition algorithm to know who the visitor is. 
We have used the Spot Crime API to process the total number of crimes in the top three most dangerous streets with the highest crime rate in the last 24 hours.

## Email Snapshots
Real time emails with pictures and description of the visitor shared with the resident.
