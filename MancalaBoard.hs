module MancalaBoard (MancalaBoard, Player, initial, getCurPlayer,
            getBoardData, numCaptured, move, allowedMoves, isAllowedMove,
            gameOver, winners) where

import Data.List as List -- for List.elemIndex
import Data.Maybe as Maybe -- for List.elemIndex

{-
 - The stones on a Mancala board are simply recorded as a list of Ints.  The
 -  Ints come in the following order:
 - 1. The boardSize pits belonging to PlayerA
 - 2. The store belonging to PlayerA
 - 3. The boardSize pits belonging to PlayerB
 - 4. The store belonging to PlayerB
 -}

data MancalaBoard = MancalaBoardImpl [Int] Player
    deriving (Eq)
             
data Player = PlayerA | PlayerB deriving (Eq, Show)

---- Functions/constants for Player ----

allPlayers = [PlayerA, PlayerB]
numPlayers = length allPlayers


playerNum :: Player -> Int
playerNum p = fromJust $ List.elemIndex p allPlayers


playerWithNum :: Int -> Player
playerWithNum i = allPlayers !! i


nextPlayer :: Player -> Player
{- Find the player whose turn is next -}
nextPlayer p = playerWithNum $ ((playerNum p) + 1) `mod` numPlayers


---- Functions/constants for MancalaBoard ----

{- number of pits on each side -}
boardSize = 6
{- number of stones in each pit -}
startStones = 4

{- the initial mancala board -}
initial :: MancalaBoard
initial = MancalaBoardImpl (concat $ take numPlayers (repeat boardSide)) PlayerA
                        -- One side of board                pit at end
    where boardSide = take boardSize (repeat startStones) ++ [0]
          

{- return the index of the first pit belonging to a player -}
indexForFirstPit :: Player -> Int
indexForFirstPit p = (playerNum p) * (boardSize + 1)


{- return the index of the store for that player -}
indexForPlayerStore :: Player -> Int
indexForPlayerStore p = boardSize + (indexForFirstPit p)


{- return the indices for the pits (without the store) for a player -}
indicesForPlayerSide :: Player -> [Int]
indicesForPlayerSide p = [firstPit .. lastPit] where
    firstPit = indexForFirstPit p
    lastPit = firstPit + boardSize - 1


---- Retrieve information about Mancala Board
{- return the player who has the current turn -}
getCurPlayer :: MancalaBoard -> Player
getCurPlayer (MancalaBoardImpl _ p) = p

testGetCurPlayer :: Bool
testGetCurPlayer = (getCurPlayer initial == PlayerA) && 
                   (getCurPlayer (MancalaBoardImpl [1] PlayerB) == PlayerB)


{- return the list of all pits in the board -}
getBoardData :: MancalaBoard -> [Int]
getBoardData (MancalaBoardImpl ps _) = ps

testGetBoardData :: Bool
testGetBoardData = (getBoardData initial == [4,4,4,4,4,4,0,4,4,4,4,4,4,0]) &&
                   (getBoardData (MancalaBoardImpl [1,2,3,4,0,4,3,2,1,0] PlayerA) == [1,2,3,4,0,4,3,2,1,0])


{- return the side of the board for a specified player, including the store at
 - the end -}
playerSide :: MancalaBoard -> Player -> [Int]
playerSide (MancalaBoardImpl ps _) p = take (boardSize + 1) $ drop (indexForFirstPit p)  ps

testPlayerSide :: Bool
testPlayerSide = (playerSide initial PlayerA == [4,4,4,4,4,4,0]) && 
                 (playerSide (MancalaBoardImpl [1,2,3,4,5,6,0,6,5,4,3,2,1,0] PlayerA) PlayerB == [6,5,4,3,2,1,0])

{- return the number of pieces in specified index -}
numInIndex :: MancalaBoard -> Int -> Int
numInIndex (MancalaBoardImpl ps _) i = ps !! i

-- I don't think this is technically accessible to outer world 
-- since it is not described in the module statement, but here's a test anyway
testNumInIndex :: Bool
testNumInIndex = (numInIndex initial 0 == 4) && (numInIndex initial 6 == 0) &&
                 (numInIndex (MancalaBoardImpl [0,1,2,3,4,5,6] PlayerA) 3 == 3)

{- return the number of captured pieces in specified player's store -}
numCaptured :: MancalaBoard -> Player -> Int
numCaptured m p = numInIndex m (indexForPlayerStore p)

testNumCaptured :: Bool
testNumCaptured = (numCaptured initial PlayerA == 0) && 
                  (numCaptured (MancalaBoardImpl [1,2,3,4,5,6,100,6,5,4,3,2,1,50] PlayerA) PlayerB == 50)


{- allowedMoves returns a list of valid moves for the current player:
 - ie. the indices of pits which belong to that player, and which contain one
 - or more pieces -}
-- NOTE: the skeleton code had two underscores, but the above
--       paragraph suggests only one argument, I am working under
--       that assumption.
allowedMoves :: MancalaBoard -> [Int]
allowedMoves m = [i | i <- (indicesForPlayerSide (getCurPlayer m)), numInIndex m i > 0]

testAllowedMoves :: Bool
testAllowedMoves = (allowedMoves initial == [0,1,2,3,4,5]) && 
                   (allowedMoves (MancalaBoardImpl [1,2,3,4,5,6,0,0,1,0,3,0,5,0] PlayerB) == [1+7,3+7,5+7]) -- +7 to account for PlayerA offset


{- check that a move is valid for the current player -}
isAllowedMove :: MancalaBoard -> Int -> Bool
isAllowedMove m move = move `elem` (allowedMoves m) 

testIsAllowedMove :: Bool
testIsAllowedMove = and [isAllowedMove initial i | i <- [0..5]] && 
                    not (isAllowedMove (MancalaBoardImpl [1,2,3,4,5,6,0,0,1,2,3,4,5,0] PlayerB) 0) &&
                    not (isAllowedMove initial 6) -- test out of bounds

{- We number the pits from 0 to 13 (2 players, 6 pits each and 1 store each)
 - This function takes a board and applies the move where the player selects
 - the numbered pit, giving back an updated board after the move -}
move :: MancalaBoard -> Int -> MancalaBoard
move m@(MancalaBoardImpl ps p) move = if not $ isAllowedMove m move then -- invalid move
                  m
              else updated where -- valid move, return current board
                  updated = MancalaBoardImpl updatedPits nextP
                  otherP = nextPlayer p -- assumes only 2 players unfortunately
                  l = length ps
                  nextP = if (numInIndex m move) + move `mod` l == indexForPlayerStore p
                               then p
                               else otherP
                  
                  replaceElt xs i x = beginning ++ (x : ending) where
                      beginning = take i xs
                      ending = drop (i+1) xs
                  
                  updatedPits = update (replaceElt ps move 0) (move + 1) (numInIndex m move) 
                  -- I realize that it would have been neater to have the modular
                  -- arithmetic at the recursive calls, but for the life of me
                  -- I could not get that to function correctly, so here's the
                  -- complement of that solution.
                  update xs _ 0 = xs
                  update xs i n =  if (i `mod` l) == indexForPlayerStore otherP then 
                      update xs (i + 1) n
                      else update (replaceElt xs (i `mod` l) ((xs!!(i `mod` l))+1)) (i+1) (n-1)
                  
testMove :: Bool
testMove = (move initial 2 == (MancalaBoardImpl [4,4,0,5,5,5,1,4,4,4,4,4,4,0] PlayerA)) && -- test turn stays same
           (move initial 7 == initial) && -- test out of bounds
           (move test2 12 == test2Result) where -- test wrapping around
               test2 = MancalaBoardImpl [0,1,2,3,4,5,0,7,8,9,10,11,8,13] PlayerB
               test2Result = MancalaBoardImpl [1,2,3,4,5,6,0,8,8,9,10,11,0,14] PlayerA


{- gameOver checks to see if the game is over (i.e. if one player's side of the
 - board is all empty -}
gameOver :: MancalaBoard -> Bool
gameOver m = or (map ((all (==0)) . init . (playerSide m)) allPlayers)

testGameOver :: Bool
testGameOver = not (gameOver initial) &&
               gameOver (MancalaBoardImpl [0,0,0,0,0,0,1,1,1,1,1,1,1,1] PlayerA) &&
               gameOver (MancalaBoardImpl [1,1,1,1,1,1,1,0,0,0,0,0,0,1] PlayerB)

{- winner returns a list of players who have the top score: there will only be 
 - one in the list if there is a clear winner, and none if it is a draw -}
winners :: MancalaBoard -> [Player]
winners m = filter ((==maxx) . (numCaptured m)) allPlayers where
    maxx = maximum (map (numCaptured m) allPlayers)

testWinners :: Bool
testWinners = winners initial == [PlayerA, PlayerB] &&
              winners (MancalaBoardImpl [1,2,3,4,5,6,7,8,9,10,11,12,13,14] PlayerA) == [PlayerB] &&
              winners (MancalaBoardImpl [14,13,12,11,10,9,8,7,6,5,4,3,2,1] PlayerA) == [PlayerA]

testAll :: Bool
testAll = testGetCurPlayer && testGetBoardData &&
          testPlayerSide && testNumInIndex &&
          testNumCaptured && testIsAllowedMove &&
          testMove && testGameOver && testWinners

---- show
instance Show MancalaBoard where
    show (MancalaBoardImpl boardData player) =
            (show player) ++ "'s turn\n" ++ 
            (show (take (boardSize + 1) (reverse boardData))) ++ "    B side\n" ++ 
            "  " ++ (show (take (boardSize + 1) boardData)) ++ "  A side"
            

