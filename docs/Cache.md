# Caching
---
For our database, we decided to use PostgreSQL. We used the database to store new ingredients that hadn’t been previously 
entered. This allows us to store ingredients to share with users in the future. Storing the ingredients allows us to show and 
access those same ingredients much faster than making a number of API calls. For each user, we plan to store their “pantry” 
(their current ingredients), as well as the user’s favorited recipes. This allows the user to remember what they’ve cooked. 
This is particularly helpful if the users often buy the same things, they can find recipes that they’ve previously made, and 
liked, with the ingredients in their pantry. 
