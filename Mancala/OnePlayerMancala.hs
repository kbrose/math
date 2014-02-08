module Main where

import MancalaBoard
import MancalaAI
import System.IO 
import Data.Char

{- this is from last week's lab -}
gameOver :: MancalaBoard -> Bool
gameOver m = or (map ((all (==0)) . (playerSide m)) allPlayers)

welcomeUser :: IO()
welcomeUser = do 
    putStr "\n***********************************************\n"
    putStr "Hello and welcome to Digicala(TM)\n"
    putStr "To move, please type the number corresponding\n"
    putStr "to the pit you would like to select for moving,\n"
    putStr "then press Enter.  Please input 1 if you would\n"
    putStr "like to go first, input 2 if you prefer second.\n"
    putStr "***********************************************\n\n"
    hFlush stdout

sayGoodbye :: IO()
sayGoodbye = do
    putStr "Thanks for playing, please come back soon!\n"

showMove :: MancalaBoard -> Int -> IO()
showMove board move = do
    putStr ((show (getCurPlayer board)) ++ " moved " ++ (show move) ++ "\n")

playGame :: MancalaBoard -> Player -> IO()
playGame board aiPlayer = do
    if getCurPlayer board == aiPlayer then do
        let move = MancalaAI.minimax board aiPlayer 6 True
        let newBoard = MancalaBoard.move board move
        if gameOver newBoard then
            endGame newBoard
        else do
            showMove board move
            putStr (show newBoard)
            playGame newBoard aiPlayer
    else do
        move' <- getLine
        if not (all isDigit move') then do -- not given integer
            putStr "Please input an integer.\n"
            playGame board aiPlayer
        else do-- given integer
            let move = read move' :: Int 
            if (move `elem` allowedMoves board) then do -- is valid move
                let newBoard = MancalaBoard.move board move
                if gameOver newBoard then
                    endGame newBoard
                else do
                    showMove board move
                    putStr (show newBoard)
                    playGame newBoard aiPlayer
            else do-- not a valid move
                putStr ("Please input an integer from the list " ++ show (allowedMoves board) ++ "\n")
                playGame board aiPlayer

endGame :: MancalaBoard -> IO()
endGame board = do
    putStr (show board)
    putStr (show (whoWins board) ++ " is(are) the winner(s)!  Congrats!\n")

main :: IO()
main = do
    welcomeUser
    turn <- getLine
    let aiPlayer = MancalaBoard.allPlayers !! ((read turn :: Int) `mod` 2)
    putStr (show initial)
    playGame initial aiPlayer
    sayGoodbye


