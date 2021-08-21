# 2021 Fantasy Football Draft Tool #

As the 2021 NFL season approaches, plenty of people are preparing for their Fantasy Football leagues. Everyone wants to be a winner. If only it were that easy to know who exactly you should add to your team.

A huge part of being successful in your league, is picking the right players and you need to have as much information about the players and their stats to make the most informed decision.

We've leveraged the [SportsDataIO Fantasy API](https://sportsdata.io/company "SportsDataIO Fantasy API")to pull the most recent projections about all the players you may be hoping to add to your team. 

For the scope of this project we chose to focus on standard scoring leagues, without a flex position (1QB, 2RB, 2WR, 1TE, 1DEF, 1K) although there is data about PPR average draft positions in our sortable table. Data about Dynasty, IDP, or auction leagues will have to wait for another assignment.

The primary feature is a tool that ranks all players by position, sorted by Average Draft Position. 

We then took that data and visualized it in order to confirm or deny some of the long understood truths/myths about fantasy football drafts. RB is the most important position, K and DEF are worthless, QB score the most points, but you can only start one (two RBs and WRs). While most of what we would expect to see held true, there are definitley some interesting trends to be aware of for this year.

This project utilized [DataTables](https://datatables.net/ "DataTables") to aid in the interactivity of the tables being created off of our API data. DataTables is a plug-in for the jQuery Javascript library. It is a highly flexible tool, built upon the foundations of progressive enhancement, that adds all of these advanced features to any HTML table.

Please follow this link to our website: [2021 Fantasy Football Drafting](https://fantasyfootballstats.herokuapp.com/ "2021 Fantasy Football Drafting")

Good luck in your upcoming 2021 Fantasy Leagues! Hope we helped you make informed decisions!