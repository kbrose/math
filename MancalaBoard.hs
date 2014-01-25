module MancalaBoard (MancalaBoard, Player, initial, getCurPlayer, getBoardData, numCaptured, move, allowedMoves, allowedMovesFor, whoWins, allPlayers, argmaxes, playerSide, playerScore, nextPlayer) where

import Data.List -- for List.elemIndex
import Data.Maybe -- for List.elemIndex

-- The stones on a Mancala board are simply recorded as a list of Ints.  The Ints come in the following order:
-- 1. The boardSize pits belonging to PlayerA
-- 2. The store belonging to PlayerA
-- 3. The boardSize pits belonging to PlayerB
-- 4. The store belonging to PlayerB

data MancalaBoard = MancalaBoardImpl [Int] Player

data Player = PlayerA | PlayerB deriving (Eq, Show)

---- Functions/constants for Player ----

allPlayers = [PlayerA, PlayerB]
numPlayers = length allPlayers

playerNum :: Player -> Int
playerNum p = fromJust $ Data.List.elemIndex p allPlayers

playerWithNum :: Int -> Player
playerWithNum i = allPlayers !! i

nextPlayer :: Player -> Player
nextPlayer p = playerWithNum $ ((playerNum p) + 1) `mod` numPlayers

---- Functions/constants for MancalaBoard ----

initial :: MancalaBoard

---- getters
getCurPlayer :: MancalaBoard -> Player
getBoardData :: MancalaBoard -> [Int]
playerSide :: MancalaBoard -> Player -> [Int]

numCaptured :: MancalaBoard -> Player -> Int

---- more complex functions
move :: MancalaBoard -> Int -> MancalaBoard 
allowedMoves :: MancalaBoard -> [Int]
allowedMovesFor :: MancalaBoard -> Player -> [Int]
whoWins :: MancalaBoard -> [Player] -- if the list has more than one Player, it's a tie.

---- show
---- Show method due to Alex Stephens.
instance Show MancalaBoard where
    show (MancalaBoardImpl boardData player) =
      "                       PlayerB's Side\n\n"++
      "                12   11   10    9    8    7\n"++
      "          ____ ____ ____ ____ ____ ____ ____ ____\n"++
      "         |    |    |    |    |    |    |    |    |\n"++
      "         |    | "
           ++(doubleDigit$boardData!!12)++
      " | "++(doubleDigit$boardData!!11)++
      " | "++(doubleDigit$boardData!!10)++
      " | "++(doubleDigit$boardData!!9)++
      " | "++(doubleDigit$boardData!!8)++
      " | "++(doubleDigit$boardData!!7)++        " |    |\n"++
      "PlayerB's| "++(doubleDigit$boardData!!13)++
      " |____|____|____|____|____|____| "++(doubleDigit$boardData!!6)++
      " |PlayerA's\n"++
      "   Pit   |    |    |    |    |    |    |    |    |   Pit\n"++
      "         |    | "
           ++(doubleDigit$boardData!!0)++
      " | "++(doubleDigit$boardData!!1)++
      " | "++(doubleDigit$boardData!!2)++
      " | "++(doubleDigit$boardData!!3)++
      " | "++(doubleDigit$boardData!!4)++
      " | "++(doubleDigit$boardData!!5)++        " |    |\n"++
      "         |____|____|____|____|____|____|____|____|\n\n"++
      "                 0    1    2    3    4    5\n\n"++
      "                       PlayerA's Side\n\n"++
      (show player)++", it is your turn.\n" where
        doubleDigit x= case elem x [0..9] of
                         True->"0"++show x
                         False->show x

---- some internal helpers ----
boardSize = 6
startStones = 4

indexForPlayerStore :: Player -> Int
indexForPlayerStore player = (playerNum player) * (boardSize + 1) + boardSize

indicesForPlayerSide :: Player -> [Int]
indicesForPlayerSide player = [bottom .. top] where
    bottom = (playerNum player) * (boardSize + 1)
    top = bottom + boardSize - 1

-- assumes vals is not empty
-- argmax f vals returns the value(s) in vals which maximize(s) the function f.  
argmaxes :: (Eq a, Ord b) => (a -> b) -> [a] -> [a]
argmaxes f vals = nub $ foldl (doArgMax f) [(vals !! 0)] vals where
   doArgMax :: (Ord b) => (a -> b) -> [a] -> a -> [a]
   doArgMax f (curArgMax:cams) val | f val > f curArgMax = [val]
                                   | f val == f curArgMax = (val : (curArgMax : cams))
                                   | otherwise = (curArgMax : cams)

initialPlayerSetup = (take (fromIntegral boardSize) (repeat (fromIntegral startStones))) ++ [0]
---- end internal helpers ----

initial = MancalaBoardImpl (concat $ take numPlayers (repeat (take boardSize (repeat startStones) ++ [0]))) PlayerA

getCurPlayer (MancalaBoardImpl _ p) = p

getBoardData (MancalaBoardImpl boardData _) = boardData

playerSide (MancalaBoardImpl boardData _) player = [boardData !! i | i <- indicesForPlayerSide player]

numCaptured (MancalaBoardImpl boardData _) player = boardData !! (indexForPlayerStore player)

allowedMovesFor (MancalaBoardImpl boardData _) player = [i | i <- indicesForPlayerSide player, (boardData !! i) /= 0]

allowedMoves mancala = allowedMovesFor mancala (getCurPlayer mancala)

whoWins mancala = argmaxes (playerScore mancala) allPlayers

playerScore :: MancalaBoard -> Player -> Int    
playerScore mancala p = numCaptured mancala p + sum (playerSide mancala p)

-- assumes the move i is legal -- it's up to the user of MancalaBoard to check this first!!
move mancala i = MancalaBoardImpl newBoardData newPlayer where
                     boardData = getBoardData mancala
                     curPlayer = getCurPlayer mancala
                     curPlayerStoreIndex = indexForPlayerStore curPlayer
                     otherPlayerStoreIndex = indexForPlayerStore (nextPlayer curPlayer)
                     numStones = boardData !! i

                     midBoardData = fst $ pickupStones boardData i
                     newBoardData = placeStones midBoardData numStones ((i + 1) `mod` (length boardData)) otherPlayerStoreIndex
                     newPlayer = if (i + numStones == curPlayerStoreIndex) then curPlayer else (nextPlayer curPlayer)

---- internal helpers for move
pickupStones :: [Int] -> Int -> ([Int], Int)
pickupStones boardData 0 = ((0 : (tail boardData)), head boardData)
pickupStones boardData i = (((head boardData) : (fst rec)), snd rec) where rec = pickupStones (tail boardData) (i-1)

placeStones :: [Int] -> Int -> Int -> Int -> [Int]
placeStones boardData 0 _ _ = boardData
placeStones boardData numStones i exclIndex | i == exclIndex = placeStones boardData numStones ((i + 1) `mod` (length boardData)) exclIndex
                                            | otherwise = placeStones (listIncr boardData i) (numStones - 1) ((i + 1) `mod` (length boardData)) exclIndex

-- listIncr vals idx returns a new list with (vals !! idx) incremented by 1
listIncr :: [Int] -> Int -> [Int]
listIncr vals i | i > length vals = listIncr vals (i `mod` length vals)
                | i == 0 = ((head vals + 1) : (tail vals))
                | otherwise = (head vals) : (listIncr (tail vals) (i-1))