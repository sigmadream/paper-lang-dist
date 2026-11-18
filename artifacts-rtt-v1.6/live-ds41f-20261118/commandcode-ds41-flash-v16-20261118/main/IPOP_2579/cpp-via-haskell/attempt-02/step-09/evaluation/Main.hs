module Main where

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Integer]
    case nums of
        [] -> return ()
        (n0:_) -> do
            let n = fromIntegral n0 :: Int
                xs = take n (drop 1 nums)
            if n == 0
                then putStrLn "0"
                else if n == 1
                    then putStrLn (show (head xs))
                    else do
                        let s = 0 : take n xs
                            dp = [0, s !! 1, s !! 1 + s !! 2] ++
                                 [ max (dp !! (i - 2)) (dp !! (i - 3) + s !! (i - 1)) + s !! i
                                 | i <- [3..n] ]
                        putStrLn (show (dp !! n))