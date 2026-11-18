module Main (main) where

import Data.IORef
import qualified Data.Text.IO as TIO
import qualified Data.Text as T
import qualified Data.Text.Builder as TB
import Data.List (foldl')

hanoi :: Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s e = [(s, e)]
hanoi k s e = hanoi (m - 1) s e ++ [(s, e)] ++ hanoi (m - 1) e s
  where m = 1 :: Int

main :: IO ()
main = do
    n <- readLn :: IO Int
    let moves = go n 1 3 2
        go :: Int -> Int -> Int -> Int -> [(Int, Int)]
        go 1 s e _ = [(s, e)]
        go k s e m = go (k - 1) s m e ++ [(s, e)] ++ go (k - 1) m e s
    let count = length moves
    let b = TB.decimal count <> TB.singleton '\n' <>
            mconcat [ TB.decimal a <> TB.singleton ' ' <> TB.decimal c <> TB.singleton '\n'
                    | (a, c) <- moves ]
    TIO.putStr (TB.toLazyText b)