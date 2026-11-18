import qualified Data.ByteString.Builder as B
import qualified Data.ByteString.Lazy as BL

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (x:_) -> do
            let n = read x :: Int
                cnt = ((2 :: Integer) ^ n) - 1
                out = B.integerDec cnt <> B.char8 '\n' <> buildMoves n 1 2 3
            BL.hPut stdout (B.toLazyByteString out)

buildMoves :: Int -> Int -> Int -> Int -> B.Builder
buildMoves 0 _ _ _ = mempty
buildMoves n s m e =
    buildMoves (n - 1) s e m <>
    B.intDec s <> B.char8 ' ' <> B.intDec e <> B.char8 '\n' <>
    buildMoves (n - 1) m s e