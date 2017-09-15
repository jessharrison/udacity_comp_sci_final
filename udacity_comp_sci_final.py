
# coding: utf-8

# # Gamer's Network

# In[1]:

from collections import defaultdict


# In[2]:

# Example string input. Use it to test your code.
example_input="John is connected to Bryant, Debra, Walter.John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.Bryant is connected to Olive, Ollie, Freda, Mercedes.Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.Mercedes is connected to Walter, Robin, Bryant.Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.Olive is connected to John, Ollie.Olive likes to play The Legend of Corgi, Starfleet Commander.Debra is connected to Walter, Levi, Jennie, Robin.Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.Walter is connected to John, Levi, Bryant.Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.Levi is connected to Ollie, John, Walter.Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.Ollie is connected to Mercedes, Freda, Bryant.Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.Jennie is connected to Levi, John, Freda, Robin.Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.Robin is connected to Ollie.Robin likes to play Call of Arms, Dwarves and Swords.Freda is connected to Olive, John, Debra.Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."


# def parse_sentences(input_string):
#     previous = example_input.find('.')
#     sentence_list = [example_input[:previous+1]]
#     while previous != -1:
#         current = example_input.find('.', previous + 1)
#         if current != -1:
#             sentence_list.append(example_input[previous+1:current+1])
#         previous = current
#     return sentence_list

# network_info = parse_sentences(example_input)

# In[3]:

from enum import IntEnum

class category(IntEnum):
    friends = 0
    games = 1


# In[4]:

def create_data_structure(input_string):
    network_info = example_input.strip().split('.')
    

    keywords = [' is connected to ',' likes to play ']
    result = []
    for word in keywords:
        for sentence in network_info:
            if sentence.find(word) != -1:
                name = sentence[:sentence.find(word)]
                friend = sentence[(sentence.find(word) + len(word)):]
                current = (name, (friend))
                result.append(current)
    
    network_conn = []
    
    for i in result:
        network_conn.append([i[0],i[1].strip().split(', ')])
    
    network = defaultdict(list)
    for k, v in network_conn:
        network[k].append(v)
    return network


# In[5]:

create_data_structure(example_input)


# In[6]:

network = create_data_structure(example_input)
# each entry in the dictionary is structured as follows:
# name (key): [[friends (as list)], [games played (as list)]]


# In[7]:

print network['Freda']


# In[8]:

# when kernel is cleared and rerun, the length (from initial paragraph input) should read 11.
# it will read 12+ because of later additions to the dict.
len(network)


# In[9]:

print network['John'][1]


# In[10]:

def get_connections(network, user):
    if user in network:
        return network[user][category.friends]
    else:
        return None


# In[11]:

get_connections(network, 'John')


# In[12]:

def get_games_liked(network,user):
    if user in network:
        return network[user][category.games]
    else:
        return None


# In[13]:

get_games_liked(network, 'John')


# In[14]:

def add_connection(network, user_A, user_B):
    if user_A and user_B in network:
        if user_B in network[user_A][category.friends]:
            return
        else:
            network[user_A][category.friends].append(user_B)
    else:
        return False
    
    return network


# In[15]:

add_connection(network, 'John', 'Robin')


# In[16]:

def add_new_user(network, user, games):
    if user not in network:
        network[user] = [[], [games]]
    return network


# In[17]:

add_new_user(network, 'Lola', 'Ninja Hamsters')


# In[18]:

add_connection(network, 'Robin', 'Lola')

 get_secondary_connections(network, user): 
#   Finds all the secondary connections (i.e. connections of connections) of a 
#   given user.
# 
# Arguments: 
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return: 
#   A list containing the secondary connections (connections of connections).
#   - If the user is not in the network, return None.
#   - If a user has no primary connections to begin with, return an empty list.
# 
# NOTE: 
#   It is OK if a user's list of secondary connections includes the user 
#   himself/herself. It is also OK if the list contains a user's primary 
#   connection that is a secondary connection as well.
# In[19]:

def get_secondary_connections(network, user):
    result = set()
    ## safety check to see if friend is in the data structure
    if user not in network:
        return None
    
    ##enumerate through user's friends
    for i in network[user][category.friends]:
        ## check if user's friends exist in network
        if i in network:
            secondary_connects = set(network[i][category.friends])
            result = result.union(secondary_connects)
    return list(result)


# In[20]:

##test for true
print get_secondary_connections(network, "Robin")
print get_secondary_connections(network, "Ollie")


# In[21]:

## test for false
get_secondary_connections(network, 'Joel')


# In[22]:

# count_common_connections(network, user_A, user_B): 
#   Finds the number of people that user_A and user_B have in common.
#  
# Arguments: 
#   network: the gamer network data structure
#   user_A:  a string containing the name of user_A
#   user_B:  a string containing the name of user_B
#
# Return: 
#   The number of connections in common (as an integer).
#   - If user_A or user_B is not in network, return False.

# counts common secondary connections, not just common initial connections

def count_common_connections(network, user_A, user_B):
    if user_A and user_B in network:
        user_A_connections = get_secondary_connections(network, user_A)
        user_B_connections = get_secondary_connections(network, user_B)

        common = list(set(user_A_connections).intersection(set(user_B_connections)))
        return len(common)
    else:
        return False


# In[23]:

count_common_connections(network, 'Robin', 'John')


# In[24]:

def find_most_well_connected(network):
    test_list = []
    for i in network:
        test_list.append((i,get_secondary_connections(network, i)))
    
    longest = 0
    result = None
    for entry in test_list:
        if len(entry[1]) > longest:
            longest = len(entry[1])
            result = entry[0]
            
            ## ADD SECTION TO TEST FOR MULTIPLE LONGEST LISTS ##
#         elif len(network[person][category.friends]) == longest:
#             result += person
    return result


# In[25]:

find_most_well_connected(network)


# In[26]:

# Make-Your-Own-Procedure (MYOP)
# ----------------------------------------------------------------------------- 
# Your MYOP should either perform some manipulation of your network data 
# structure (like add_new_user) or it should perform some valuable analysis of 
# your network (like path_to_friend). Don't forget to comment your MYOP. You 
# may give this procedure any name you want.

def find_game_players(network, game):
    """this procedure takes a network, as a dictionary of lists, and the name of a game,
    as a string, and returns a list of players who like the game."""
    result = set()
    
    for person in network: #iterate throught the people in the network
        if game in network[person][category.games]: # check if the game is in their liked list
            result.add(person) # add them to the set
    
    if len(result) > 0:
        return list(result) # if the set is not empty, return the list of players
    else:
        return None # if the game is not in the network or no one likes it, return None


# In[27]:

find_game_players(network, 'The Legend of Corgi')


# In[ ]:




# In[109]:

def find_path(network, user_A, user_B, checked = None):
    ## check that users are in network
    if user_A and user_B not in network:
        print "These are not the droids you are looking for."
        return None
    
    ## check for a direct connection:
    if user_B in network[user_A][category.friends]:
        print "we found you!"
        return [user_A, user_B]
    
    ## start recursion to hunt for links
    
# 😳 THIS IS WHERE I GET CONFUSED

    # start keeping track of whose networks you've looked in already
    if checked == None:
        checked = [user_A]
    
    for friend in network[user_A]:
        #determine in the person (and thus their network) has been checked
        if friend not in checked:
            # add them to the checked list
            checked.append(friend)
            # check their connections
            find_path(network, friend, user_B)
        
    
        


# In[110]:

find_path(network, 'John', 'Olive')


# In[101]:

# # find_path_to_friend(network, user_A, user_B): 
# #   Finds a connections path from user_A to user_B. It has to be an existing 
# #   path but it DOES NOT have to be the shortest path.
# #   
# # Arguments:
# #   network: The network you created with create_data_structure. 
# #   user_A:  String holding the starting username ("Abe")
# #   user_B:  String holding the ending username ("Zed")
# # 
# # Return:
# #   A list showing the path from user_A to user_B.
# #   - If such a path does not exist, return None.
# #   - If user_A or user_B is not in network, return None.
# #
# # Sample output:
# #   >>> print find_path_to_friend(network, "Abe", "Zed")
# #   >>> ['Abe', 'Gel', 'Sam', 'Zed']
# #   This implies that Abe is connected with Gel, who is connected with Sam, 
# #   who is connected with Zed.
# # 
# # NOTE:
# #   You must solve this problem using recursion!
# # 
# # Hints: 
# # - Be careful how you handle connection loops, for example, A is connected to B. 
# #   B is connected to C. C is connected to B. Make sure your code terminates in 
# #   that case.
# # - If you are comfortable with default parameters, you might consider using one 
# #   in this procedure to keep track of nodes already visited in your search. You 
# #   may safely add default parameters since all calls used in the grading script 
# #   will only include the arguments network, user_A, and user_B.

def find_path_to_friend(network, user_A, user_B, checked=None):
    ## test for both users out of network
    if user_A and user_B not in network:
        print "not here!"
        return None
    
    ## found in network
    if user_B in network[user_A][category.friends]:
        return [user_A, user_B]
    
    ## start the checked library
    if checked = None:
        check = [user_A]
        path = []
        for friend in network[user_A][category.friends]:
            path += find_path_to_friend(network, user_A, user_B, users_searched)
        path = path + find_path_to_friend()
        return path
    return None


# In[25]:

def paths(network, user_A, user_B, checked=None):
    print "calling function..."
    if user_A not in network and user_B not in network:
        return None
    
    if user_B in network[user_A][category.friends]:
        return [user_A, user_B]
    
    if checked == None:
        checked = [user_A]
    
    for person in network[user_A][category.friends]:
        if person not in checked:
            checked.append(person)
            path = paths(network, person, user_B, checked)
            
            if path:
                return [user_A] + path
    return None



# In[26]:

print paths(network, 'John', 'Levi')


# In[27]:

def find_all_paths(network, start, search):
    paths = []
    result = []
    
    depth = len(network)
    
    for iteration in range(0, depth):
        for i in network[start][category.friends]:
            if i == search:
                result = [start, i]
                if result not in paths:
                    paths.append(result)
            else:
                for person in network[i][category.friends]:
                    if person == search:
                        result = [start, i, person]
                        if result not in paths:
                            paths.append(result)
                    else:
                        for friend in network[i][category.friends]:
                            if friend == search:
                                result = [start, i, person, friend]
                                if result not in paths:
                                    paths.append(result)
    return paths


# In[86]:

find_all_paths('John', 'Levi')


# In[29]:

def find_shortest_path(network, start, search):
    paths = find_all_paths(network, start, search)
    lengths = {}
    for path in paths:
        lengths[(len(path))] = path
    return lengths[min(lengths.keys())]


# In[30]:

find_shortest_path(paths)


# In[ ]:




# In[ ]:




# In[ ]:



