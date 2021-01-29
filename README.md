# Summoner GUI
Uses the Riot API for League of Legends to obtain match history data. The program is able to review all match histories that the API has (everything in the past two years) and display a summary of the results. The program is limited by the rate limit from the API. The algorithm for updating the API is nondestructive, so a theoretically unlimited amount of data is able to be stored. 

To avoid excessive lag, only 10 matches are displayed at a time. To scroll, either use the arrow keys, or use drag around the screen with your mouse. Pressing "Home" or "End" on the keyboard will scroll to either the beginning or the end of the match history. 
![pic5](https://github.com/jrchen312/onePercentLeagueImprovement/blob/main/images/summonerGUI2.png)

A sorting algorithm sorts the data by the user's parameters. Clicking on each of the headers will sort the data by the parameter stated on the headers. 
![pic0](https://github.com/jrchen312/onePercentLeagueImprovement/blob/main/images/summonerGUI1.png)

Pressing the "Escape" button will return the user back to the search page. 

# Champions GUI
Uses the Riot API (DataDragon) to obtain data about all the champions from League of Legends. 
Parses through API data to obtain information about the skills that all of the champions have. The app also obtains champion splash screens and icon images from the API. 

### Instructions
In the Dist folder, there is an executable file. Open "championGUI.exe" to run the champion GUI program. 

To use the app, type a champion name into the search bar on the home page. 
![pic1](https://github.com/jrchen312/onePercentLeagueImprovement/blob/main/images/championgui1.png)

To begin the search, press "Enter" on the keyboard. 
![pic2](https://github.com/jrchen312/onePercentLeagueImprovement/blob/main/images/championgui2.png)

Click on the five different ability icons to look at the information related to each ability.
![pic3](https://github.com/jrchen312/onePercentLeagueImprovement/blob/main/images/championgui3.png)

In each ability page, press the champion icon to return to the previous page. 
![pic4](https://github.com/jrchen312/onePercentLeagueImprovement/blob/main/images/championgui4.png)

# onePercentLeagueImprovement
Application dedicated to obtaining stats of a LoL summoner and analyzing the areas to improve in.
This is WIP.
