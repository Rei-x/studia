BLACK = "B"
WHITE = "W"
EMPTY = "_"

# Scores for terminal states
WIN_SCORE = 100000
LOSS_SCORE = -100000

# Global counter for visited nodes - This is tricky with modules.
# It's better if algorithms.py manages this internally or if find_best_move returns it.
# For now, we'll keep it here and import, but it's a point for potential further refinement.
# The testing script version of algorithms will handle node counting return values better.
visited_nodes_count = 0
