# print scripts depending on how much it takes for the welcome, that may get its own file

def welcome():
    return """
 ------------------------------------------------------------

  #    # ###  ###   ####   ###    ###    ##    #     #  ####
  #    #  #   #  #  #     #   #  #   #  #  #   ##   ##  #
  #    #  #   #  #  ###   #   #  #      ####   # # # #  ###
   #  #   #   #  #  #     #   #  #  ##  #  #   #  #  #  #
    ##   ###  ###   ####   ###    ###   #  #   #     #  ####


   ###     ##   #####   ##     ###     ##    ###    ####
   #  #   #  #    #    #  #    #  #   #  #  #       #
   #  #   ####    #    ####    ###    ####   ###    ###
   #  #   #  #    #    #  #    #  #   #  #      #   #
   ###    #  #    #    #  #    ###    #  #   ###    #### 

 ------------------------------------------------------------
"""
def greeting():
    return """
  Hello and welcome to the video game recommendation 
  engine! Choose a genre from the categories of 
 'Action' 'Adventure' 'Casual' 'Sports' or 'Strategy'
  The engine will list 5 games from that category 
  ranked by their user score (MetaCritic)!
          """

def line_break():
    return """
 ------------------------------------------------------------
           """
def double_line_break():
    return """
 ------------------------------------------------------------
 ------------------------------------------------------------
           """

def goodbye_message():
    return """
 ------------------------------------------------------------
  Thanks for using my recommendation engine!
 ------------------------------------------------------------
"""

# test
# print(welcome())
# print(greeting())
# print(line_break())



