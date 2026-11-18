import Control.Monad (forM_, when)
import Data.Array.ST (newArray, readArray, writeArray, runSTUArray)
import Data.Array.Unboxed (UArray, (!))

main :: IO ()
main = do
    input <- getContents
    case (map read (words input) :: [Int]) of
        (m:n:_) -> putStr (unlines (map show (primeList m n)))
        _ -> return ()

primeList :: Int -> Int -> [Int]
primeList m n = [i | i <- [max 2 m .. n], isPrime ! i]
  where
    isPrime :: UArray Int Bool
    isPrime = runSTUArray $ do
        arr <- newArray (0, n) True
        when (n >= 0) $ writeArray arr 0 False
        when (n >= 1) $ writeArray arr 1 False
        let loop i
              | i * i > n = return arr
              | otherwise = do
                  p <- readArray arr i
                  when p $ forM_ [i * i, i * i + i .. n] $ \j ->
                      writeArray arr j False
                  loop (i + 1)
        loop 2