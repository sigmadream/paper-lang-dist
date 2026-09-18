import Data.Bits (popCount)
import System.IO

main :: IO ()
main = do
    n <- readLn :: IO Int
    let counts = map popCount [0..n]
    putStrLn $ unwords $ map show counts