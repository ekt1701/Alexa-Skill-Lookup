# Alexa-Skill-Lookup

Updated on Aug 21,2016

The skill has been updated, now you can ask Alexa to search for skills by name, author. You can get the description or invocation for a skill. You can find out when the csv was last updated and the number of skills listed. In addition you can hear the name of the Alexa skills released on a certain day. You can say today, yesterday, last Thursday, July 15, 2016 and so on.

Finally when you ask Alexa to "tell me" about a skill, you will get the author, description, ratings, number of reviews, released date and invocation.

The configuration is Runtime: Python 2.7, Handler: lambda_function.lambda_handler, Existing Role: lambda_basic_execution.  The code is entered in-line. You will need to create a Custom Slot with the name ANSWERS and add a number of random words and phrases in the Value section.

The source of the data is https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv

