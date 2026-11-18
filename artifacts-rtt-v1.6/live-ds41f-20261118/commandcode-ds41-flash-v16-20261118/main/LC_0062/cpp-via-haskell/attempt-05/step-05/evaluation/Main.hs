module Main where

main :: IO ()
main = do
    input <- getContents
    let vals = map read (words input) :: [Integer]
    case vals of
        (m:n:_) -> do
            let len = fromIntegral n :: Int
                row0 = replicate len 1
                steps = fromIntegral (m - 1) :: Int
                row = (!! steps) $ iterate (\r -> scanl1 (+) r) row0
            print (last row)
        _ -> return ()