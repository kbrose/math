module MancalaAI (minimax) where

import MancalaBoard

-- simple hueristic, returns how many stones are in store
hueristic :: MancalaBoard -> Player -> Int
hueristic board player = (playerHuer board player) - (playerHuer board (nextPlayer player)) where
    playerHuer b p = numCaptured b p + sum (playerSide b p) + (isMyTurn b p)
    isMyTurn b p = if (getCurPlayer b) == p then 1 else 0

-- implementation taken from psuedocode on Wikipedia
minimax :: MancalaBoard -> Player -> Int -> Bool -> Int
minimax board aiPlayer 0 _ = hueristic board aiPlayer
minimax board aiPlayer depth True = snd (maximum heuristics) where
    heuristics = [(minimaxUtil (move board m), m) | m <- (allowedMoves board)]
    minimaxUtil b = minimax b aiPlayer (depth - 1) False
minimax board aiPlayer depth False = snd (minimum heuristics) where
    heuristics = [(minimaxUtil (move board m), m) | m <- (allowedMoves board)]
    minimaxUtil b = minimax b aiPlayer (depth - 1) True


