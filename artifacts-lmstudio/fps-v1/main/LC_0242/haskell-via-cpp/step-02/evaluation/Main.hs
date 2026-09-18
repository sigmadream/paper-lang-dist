import Data.Map (Map, empty, insertWith, fromListWith, toList)
import qualified Data.Map as Map

main :: IO ()
main = do
    s <- getLine
    t <- getLine
    let freq_s = fromListWith (+) [(c, 1) | c <- s]
        freq_t = fromListWith (+) [(c, 1) | c <- t]
    if freq_s == freq_t then putStrLn "1" else putStrLn "0"