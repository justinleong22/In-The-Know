# In The Know - Treehacks 2024

## Motivation
Growing up in Parkland, Florida, one of our hackers experienced firsthand the effects of the Marjory Stoneman Douglas school shooting. Surveys have shown that over 60% of Americans worry that they or a loved one will die in a mass shooting (Brennan 2017). The most harrowing reality of school shootings is the lack of real-time information––students and faculty cannot make informed decisions without knowing where the active shooter is. 

## What It Does
In The Know flips the narrative on school shootings by providing critical data of the shooter’s location to students and faculty on the front lines. In The Know predicts location of active shooter in real-time to allow students and faculty to make more informed decisions during critical situations. Using an intuitive and streamlined UI, users are only a single button-press away from calling 911 in case of emergencies, facilitating faster response.

During the event of an emergency, all phones begin recording from every student in the school. After an anomaly is detected in the audio, the data is sent to our proprietary algorithm, updating the shooter location on the easy-to-read map on your screen.

A single point representing shooter location is displayed on an intuitive, easy-to-use map, giving the user information where they are relative to the shooter. With this information, it allows them to make a decision of the best course of action, filling the gap in knowledge during this critical event.

## How We Built It
Our app is built with React Native on the frontend, with a FastAPI RESTful API with an Uvicorn ASGI server implementation. We designed an end-to-end data acquisition, processing, and inference framework powered by mathematical modeling and spatial audio features.

After an emergency is triggered, the app’s frontend enters anomaly-detection mode, listening for gunshots in real-time. After a statistically significant anomaly is detected using local maxima and neighborhood region analysis, we forward anomalous audio clips to the backend, marking the first step in our data pipeline.

This is how we detect the shooter’s location: our model first segments students in different spatial groups, then considers the inputted audio data from each individual phone. We account for real life situations where phones may be in different conditions such as in pockets, backpacks, out in the open, or with loud background noise. Then, our model filters through this noisy data to detect anomalies, and identifies audio samples with the highest signals. We then generate a probability density function using a spatial mathematical approach to pinpoint the location of the shooter.  We’ve experimented with different weightings and scaling factors, and generated over 250 simulations to optimize our model. 

## Challenges
In our workflow, it was challenging to ensure that asynchronous functions were called at proper moments and data was received correctly. Another barrier we experienced is a lack of data on gunshot audio; in particular, an ideal scenario involves multi-perspective data from random points within a ~300 meter radius of a gunshot. We decided to simulate realistic data, pulling from mathematical insights on sound decay rates with respect to relative distance, while accounting for background noise and phone placement. Finally, we encountered errors when integrating the predictive model into the backend infrastructure.

## Accomplishments
We engineered a real-time data tracking system to identify the location of a live shooter with extreme precision (radius of error consistently less than 3-5 meters relative to a ~300 meter long school). We optimized the model with over 250 simulated events, and created algorithm for audio anomaly detection and distance calculation with signal processing

## What we learned
Throughout the course of this project, we learned to navigate constraints, such as limited data sourcing and computational resources for signal processing, and develop a system capable of effectively responding to reported incidents. We sharpened our research and experimentation skills, reinforcing important functionalities such as data privacy, algorithm accuracy, and noticing along the way the many interdisciplinary connections in software. Finally, our findings motivated a deep societal connection, underscoring the necessity of ethical considerations and ongoing refinement to In The Know in future use cases.

## Whats next
We’ll onboard schools in the Parkland, Florida area from March to June 2024. This will help us establish and strengthen partnerships with select schools at a premium rate. We hope to provide protection and safety to communities scarred from the Stoneman Douglas massacre. Afterwards, we intend to scale and expand to other districts. With our local schools and expanded ones, we’ll continue to build a network of protection against gun violence. Finally, we hope to establish government partnerships and create national programs to help maximize impact.

## Ethics
Every student deserves the right to a safe education. In the United States, gun violence has made this nearly impossible, with more than 360,000 students having experienced gun violence at school since Columbine (Cox et al. 2024). In The Know is designed to return power to students and teachers, helping them finally feel safe again at school. 

One of our hackers, having grown up in Parkland, has directly felt the negative impact and intergenerational trauma that gun violence can cause, reverberating across communities. We believe that safety should always come first in the face of an active shooter situation, even before incredibly important principles like privacy. We prioritized creating a user experience that would help save the most lives, which used advanced computational analysis based off of audio recordings to triangulate the location of the active shooter. 

We did not take this decision lightly, and considered many ethical concerns throughout development.

Ethical considerations that we evaluated include:
Privacy Concerns. Recording audio from student phones, even if they have given prior consent, can infringe on student privacy. We evaluated the potential benefit of finding the active shooter’s location to outweigh privacy concerns in emergencies. As such, recordings will only begin during a confirmed emergency/active shooter risk. There are also likely legal risks in specific states or localities, based on recording laws. Before our public release, we will ensure compliance with local laws based on user/school location.

Ensuring Informed Consent. Students may not fully realize that the app will record all audio. We want to ensure that students fully understand the data they agree to give during an emergency, and that students have the option to refuse to provide audio data without fear of punishment. We believe that due to the potential benefit of lives saved, most students would agree to provide data during school shooting emergencies.

Although the current app includes a pop-up upon installation that asks for access to the user’s phone microphone, students may click through this notification without reading. In the future, we would consider creating clear recording consent forms for students. 

Data Security. As we handle large amounts of sensitive and private information, data security is a major priority. We do not store any audio files, and will never EVER sell ANY user information for ANY reason. We think that as the majority of our users would be children, this is extremely unethical and would go against our core ethical priorities. We will do our utmost to prevent ANY human from EVER listening to audio data taken from the app. Emergencies should not be abused for profit. 

Bias and Discrimination. Many mainstream narratives assume that white people are most impacted by school shootings. Although the deadliest school shooting perpetrators were mostly white (creating the misperception that school shootings mostly harm white children), children of color are the most likely to be targeted and negatively impacted by gun violence.  (“School Shooting Toll…” 2023). We recognize the disproportionate impact that re-activating intergenerational trauma causes to the most marginalized groups in the United States. In the face of rampant racism (seen in police brutality and discrimination), we hope that In The Know provides meaningful information that helps communities of color survive in a bigoted and violent world.  
 
We also evaluated potential risks from deploying our app, negatively impacting students and faculty. These included:
Inaccurate Information about Shooter Movements. Ethically, the worst case scenario is providing inaccurate information to students. If students make choices using this inaccurate information, they could face great harm from wrong decisions (such as running when the shooter is nearby). As such, accuracy is the highest priority of our models. We generated over 250+ computational simulations at Marjory Stoneman Douglas High School, and we’re able to successfully predict shooter movements. This is fantastic news!
In the future, we want to scale this through a larger number of schools onboarded. 

Government or School Administration Misuse. Government surveillance agencies could attempt to misuse the app to gain information on students. School administrators may also be tempted to try to abuse the app to always listen to student conversations. However, we have put clear safeguards in our app to minimize misuse. To begin, as data is not stored, bad actors wouldn’t be able to infringe upon student privacy for no reason. No human will listen to any audio data taken from our app. Furthermore, organizations that frequently misuse the app will no longer have access to administrative privileges. 

False alarms. These can cause panic, emotional harm, and harm mental health of students through creating fear. Some students may also misuse the app for “pranks”, and misclicks may occur. In addition to laws preventing false 911 calls or prank emergencies, we think students should be given the benefit of the doubt. Further, trying to curtail the ability to report emergencies would be unethical, and the risks of reacting to a non-emergency are smaller than the risks of not reacting to an actual emergency. We recognize the undue stress false emergencies could present, which is why we shall do our best to ensure only real emergencies are reported.

After evaluating the ethical considerations and different risks across many stakeholders, In The Know can mitigate risks while maximizing benefits. 

To students, knowing the location of the active shooter is a life-and-death situation. Let’s help save lives together.

## Bibliography
Brennan, W. (2017, January) Bulletproofing America. The Atlantic. https://www.theatlantic.com/magazine/archive/2017/01/bulletproofing/508754/ 
NCJA. (2023, February 14). School shooting toll rises rapidly, with major impact on minorities. NCJA. https://www.ncja.org/crimeandjusticenews/school-shooting-toll-rises-rapidly-with-major-impact-on-minorities 
There have been 394 school shootings since Columbine - Washington Post. (2024). https://www.washingtonpost.com/education/interactive/school-shootings-database/ 