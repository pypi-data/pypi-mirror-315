# data file to store graph lists and handle auto loading
from graph import Graph, Vertex

def load_data():
    data = {
            "Action": [("Space Marine 2", 8.1), ("Call of Duty Black Ops 6", 6.7), ("Street Fighter 6", 7.5), ("Grand Theft Auto V", 8.5), ("Cyberpunk2077", 8.0)],
            "Adventure": [("Elden Ring", 8.2), ("Final Fantasy XVI", 8.4), ("Remnant II", 7.2), ("Destiny 2", 7.6), ("Elder Scrolls Online", 5.7)],
            "Casual": [("Balatro", 8.2), ("Cities Skylines II", 4.0), ("Stardew Valley", 8.8), ("Marvel Snap", 6.6), ("Sims 4", 4.3)],
            "Sports": [("EA FC 25", 2.4), ("NBA 2K25", 5.8), ("Forza Horizon 5", 8.2), ("Forza Motorsport", 7.0), ("WWE 2K24", 6.6)],
            "Strategy": [("Civilization VI", 7.2), ("DOTA 2", 6.5), ("Stellaris", 8.0), ("Yu Gi Oh Master Duel", 6.0), ("Age of Empires IV", 7.8)],
            } 

    blurb = {
            "Space Marine 2": "\n The sequel of the legendary license space marine,\n by the creators of the best-seller world war z (15m players)\n",
            "Call of Duty Black Ops 6": "\n Black Ops 6 features fast, responsive movement on PC,\n allowing players to swiftly navigate the map in search of\n their next target and objective.\n",
            "Street Fighter 6": "\n Street Fighter 6 offers a highly evolved combat\n system with three control types - Classic, Modern and Dynamic\n",
            "Grand Theft Auto V": "\n Experience entertainment blockbusters,\n Grand Theft Auto V and GTA Online.\n",
            "Cyberpunk2077": "\n Magnificent, confident and loaded with content\n that other games do not offer.\n",
            "Elden Ring": "\n 2022 Game of the Year\n",
            "Final Fantasy XVI": "\n An epic dark fantasy world where the fate of the\n land is decided by the mighty Eikons and the Dominants who wield them.\n",
            "Remnant II": "\n Remnant 2 iterates on the original to phenomenal effect.\n",
            "Destiny 2": "\n Destiny 2 takes place in a fictional universe where you will\n assume the role of a Guardian, a protector of Earth's last city.\n",
            "Elder Scrolls Online": "\n Go anywhere, do anything, and play your way\n in The Elder Scrolls Online, the award-winning online\n RPG set in the Elder Scrolls universe.\n",
            "Balatro": "\n Balatro is one of the most addictive games of the past few years\n",
            "Cities Skylines II": "\n Cities: Skylines II is still a long way from perfect.\n",
            "Stardew Valley": "\n Stardew Valley is a highly praised farming simulation game\n",
            "Marvel Snap": "\n Marvel Snap is a fast-paced mobile collectible card\n game that features strategic gameplay\n",
            "Sims 4": "\n Regardless of environmental aesthetic, the series has\n always been functionally and fundamentally Californian.\n",
            "EA FC 25": "\n The new Rush mode is a fast and often high-scoring spectacle.\n",
            "NBA 2K25": "\n NBA 2K25 has been praised for its improved gameplay and\n realistic player movements, making it one of the best entries in the series.\n",
            "Forza Horizon 5": "\n Forza Horizon 5 is widely praised as the best entry in the series.\n",
            "Forza Motorsport": "\n Forza Motorsport has been praised for its improved\n handling and realistic driving experience.\n",
            "WWE 2K24": "\n WWE 2K24 has been praised for its improved gameplay mechanics,\n better visuals, and a variety of match types.\n",
            "Civilization VI": "\n Civilization VI is a turn-based strategy game that allows\n players to build and expand their empires throughout history.\n",
            "DOTA 2": "\n This is a dizzyingly deep competitive team strategy game whose\n core design benefits from fifteen years of unbroken refinement.\n",
            "Stellaris": "\n Stellaris is a grand strategy game that starts strong with\n engaging exploration and empire-building but struggles in the mid-game\n",
            "Yu Gi Oh Master Duel": "\n It's complicated, but hasn't lost the basic\n appeal of any card game: the agony and ecstasy at the intersection of skill and luck.\n",
            "Age of Empires IV": "\n Age of Empires IV has received mixed reviews,\n with some praising its nostalgic gameplay and stunning visuals, while others\n criticize it for lacking depth and innovation\n",
            }
    # I limited the graph to 5 titles in 5 genres to keep it from getting too large
    graph = Graph()
    for genre, games in data.items():
        genre_vertex = Vertex(genre)
        graph.add_vertex(genre_vertex)
        for game_name, rating in games:
            game_vertex = Vertex(game_name, rating)
            game_vertex.blurb = blurb.get(game_name, "No blurb available")
            graph.add_vertex(game_vertex)
            graph.add_edge(genre_vertex, game_vertex)
    return graph

def get_blurb(graph, game_name):
    vertex = graph.get_vertex(game_name)
    return vertex.blurb if vertex else "Game not found"
