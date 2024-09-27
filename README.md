# joker-synergy-visualisation
Spider diagram of all jokers that synergise very well with each other, using scraped text from Balatro Wiki 

# How it worked

## Scraping

The ``scraper.py`` script recursively goes through every joker listed on the Balatro Wiki's central joker page https://balatrogame.fandom.com/wiki/Category:Jokers 
but it ignores sections of text under "Anti-synergies"

It uses wikitext and when a Joker is mentioned, it links to that joker with ``{J|Joker_Name}`` (or something similar i cant remember)

Then the ``collation3.py`` script puts it all into a txt file, with each line containing the Joker name and then the jokers it synergizes with

Example:

```
Lucky Cat: Jokers: Baseball Card, Bloodstone, Cartomancer, Certificate, Dusk, Glass Joker, Golden Ticket, Hack, Hanging Chad, Oops! All 6s, Red Card, Sock and Buskin, Steel Joker, Stone Joker
Seance: Jokers: Arrowhead, Bloodstone, Blueprint, Brainstorm, Crazy Joker, Credit Card, DNA, Driver's License, Drunkard, Erosion, Fibonacci, Four Fingers, Hit the Road, Hologram, Joker Stencil, Juggler, Merry Andy, Onyx Agate, Perkeo, Scholar, Shortcut, Smeared Joker, The Family, Troubadour, Vampire, Wee Joker
Oops! All 6s: Jokers: 8 Ball, Baseball Card, Bloodstone, Business Card, Canio, Cavendish, Glass Joker, Gros Michel, Hallucination, Hanging Chad, Lucky Cat, Lusty Joker, Reserved Parking, Sock and Buskin, Space Joker
Canio: Jokers: Business Card, Cavendish, Chicot, Erosion, Glass Joker, Hologram, Oops! All 6s, Pareidolia, Perkeo, Trading Card, Triboulet, Yorick
To Do List: Jokers: Blueprint, Brainstorm
```

In the Balatro Wiki, sometimes it'll say a joker synergizes with another joker, but on the second joker's wiki page, it won't mention the synergy there.

Therefore, the script also ensures that if a Joker is found to have synergy with another one, then it is included in both lists.

### chip jokers fix.py
although it ignored anti-synergies sections, the jokers that boost chips for a specific hand (ie, Crafty Joker, Sly Joker, Wily Joker) were included in each others lists because the wiki mentions them as a piece of trivia and also links to them too (without actually having synergy with them)

so that script is just to remove any of the hand specific chip jokers from each other's lists


# Visualisation

``app.py`` is the backend that just fetches from the final txt file ``corrected_joker_synergies.txt``

``index.html`` is responsible for displaying the interactive visualisation using the ``D3.js`` library

it also includes logic for scaling the size of each node (joker) based on how many connections it has, like Blueprint (which has the most i think) is ideally the biggest sized nodes. Also has colours

The graph has pan and zoom features and should ideally fit to screen but I have had issues with that

the joker synergy data is fetched from a server endpoint ``(/synergies/all)`` and is processed into graph format and rendered dynamically

## Controls

The graph has pan and zoom

It includes prefix based filtering so that it hides nodes that dont match the text in the input box

You can click on a node to see what connections it has, and press ``ESC`` to view the whole diagram again

You can drag nodes around (this does not readjust the graph - it did at first but it would always be erratic and laggy)



### known issues

Misprint and Driver's License are connected by a "No synergies" because that's how it is in the text file. obviously something went wrong with the collation part for misprint and drivers' license

Drivers' License do have connections with other jokers as well.



There are 150 jokers in Balatro (the wiki page says 151, but that is incorrect) and the amount of nodes displayed is 152. One of them is ``No synergies`` but I have no idea what the other one is yet


# Final Result

![](https://i.imgur.com/s9BGZ1Q.png)
