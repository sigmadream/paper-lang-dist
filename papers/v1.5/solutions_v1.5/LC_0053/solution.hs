import Data.List (foldl')

kadane :: [Integer] -> Integer
kadane [] = 0
kadane (x:xs) = snd $ foldl' step (x, x) xs
  where
    step (cur, best) v =
        let newCur = max v (cur + v)
            newBest = max best newCur
        in (newCur, newBest)

main :: IO ()
main = do
    content <- getContents
    case words content of
        [] -> return ()
        (_:rest) -> do
            let nums = map read rest :: [Integer]
            print (kadane nums)
