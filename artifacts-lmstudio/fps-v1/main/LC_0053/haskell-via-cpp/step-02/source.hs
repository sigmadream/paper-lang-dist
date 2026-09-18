import System.IO

main :: IO ()
main = do
    hSetBuffering stdin LineBuffering
    hSetBuffering stdout NoBuffering
    n <- readLn :: IO Int
    nums <- replicateM n (readLn :: IO Int)
    let bestSoFar = go 0 0 nums
    print bestSoFar
  where
    go endingHere bestSoFar [] = bestSoFar
    go endingHere bestSoFar (x:xs) =
        let newEndingHere = max x (endingHere + x)
            newBestSoFar = max bestSoFar newEndingHere
        in go newEndingHere newBestSoFar xs