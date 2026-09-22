"""Manually curated specifications and public examples checked on 2026-09-16."""

# ID, repository slug, function, category, interface, Korean summary, constraints,
# independent oracle methods, public example argument lists.
ROWS = [
 (1,'two_sum','twoSum','배열·해시','vector_target','합이 target인 서로 다른 두 원소의 0-based 인덱스를 찾는다. 유일한 인덱스 쌍이 존재한다.',
  '2<=N<=10000; 원소와 target은 -10^9..10^9; 정답 쌍은 유일하다.',('해시 보완값 탐색','모든 인덱스 쌍 검사'),
  [[[2,7,11,15],9],[[3,2,4],6],[[3,3],6]]),
 (121,'best_time_to_buy_and_sell_stock','maxProfit','배열·최적화','vector','먼저 하루에 매수하고 이후 하루에 매도할 때 최대 이익을 구한다. 거래하지 않을 때 이익은 0이다.',
  '1<=N<=100000; 0<=가격<=10000.',('최저 매수가 순회','모든 매수·매도 쌍 검사'),[[[7,1,5,3,6,4]],[[7,6,4,3,1]]]),
 (217,'contains_duplicate','containsDuplicate','배열·해시','vector','배열에 같은 값이 두 번 이상 등장하면 1, 아니면 0을 출력한다.',
  '1<=N<=100000; 원소는 -10^9..10^9.',('집합 크기 비교','정렬 후 인접 값 검사'),[[[1,2,3,1]],[[1,2,3,4]],[[1,1,1,3,3,4,3,2,4,2]]]),
 (53,'maximum_subarray','maxSubArray','동적 계획법','vector','비어 있지 않은 연속 부분배열의 합 중 최댓값을 구한다.',
  '1<=N<=100000; 원소는 -10000..10000.',('Kadane DP','모든 연속 구간 합 검사'),[[[-2,1,-3,4,-1,2,1,-5,4]],[[1]],[[5,4,-1,7,8]]]),
 (704,'binary_search','search','이분탐색','vector_target','오름차순 배열에서 target의 0-based 인덱스를 출력하고 없으면 -1을 출력한다.',
  '1<=N<=10000; -10000<원소,target<10000; 원소는 서로 다르고 오름차순이다. 요구 시간 O(log N).',('이분탐색','직접 선형 검색'),
  [[[-1,0,3,5,9,12],9],[[-1,0,3,5,9,12],2]]),
 (35,'search_insert_position','searchInsert','이분탐색','vector_target','정렬 배열에서 target의 위치 또는 정렬을 유지할 삽입 위치를 0-based로 출력한다.',
  '1<=N<=10000; 원소,target은 -10000..10000; 배열은 중복 없이 오름차순이다. 요구 시간 O(log N).',('lower-bound 이분탐색','target보다 작은 원소 개수'),
  [[[1,3,5,6],5],[[1,3,5,6],2],[[1,3,5,6],7]]),
 (283,'move_zeroes','moveZeroes','배열·재배치','vector','0이 아닌 원소의 상대 순서를 유지하면서 모든 0을 뒤로 옮긴 배열을 출력한다.',
  '1<=N<=10000; 원소는 signed 32-bit 정수. 원래 함수는 in-place 수정이며 반환값 대신 수정된 배열을 평가한다.',('두 포인터 in-place 이동','0 제외 목록과 0 개수 결합'),
  [[[0,1,0,3,12]],[[0]]]),
 (242,'valid_anagram','isAnagram','문자열','strings','두 소문자 문자열의 문자별 개수가 모두 같으면 1, 아니면 0을 출력한다.',
  '각 문자열 길이 1..50000; 영문 소문자.',('문자 빈도표','문자 정렬 비교'),[['anagram','nagaram'],['rat','car']]),
 (387,'first_unique_character_in_a_string','firstUniqChar','문자열','string','한 번만 등장하는 첫 문자의 0-based 인덱스를 출력하고 없으면 -1을 출력한다.',
  '문자열 길이 1..100000; 영문 소문자.',('빈도표와 첫 위치','각 위치의 다른 위치 전수 대조'),[['leetcode'],['loveleetcode'],['aabb']]),
 (3,'longest_substring_without_repeating_characters','lengthOfLongestSubstring','문자열·슬라이딩 윈도','string','문자가 중복되지 않는 연속 부분문자열의 최대 길이를 구한다. 빈 문자열의 답은 0이다.',
  '길이 0..100000; 영문자, 숫자, 기호, 공백. 이 묶음은 인쇄 가능한 ASCII를 사용한다.',('최근 등장 위치 기반 윈도','모든 부분문자열의 고유 문자 검사'),
  [['abcabcbb'],['bbbbb'],['pwwkew']]),
 (139,'word_break','wordBreak','동적 계획법·문자열','words','문자열을 사전 단어들의 연결로 만들 수 있으면 1을 출력한다. 같은 단어를 여러 번 쓸 수 있다.',
  '문자열 길이 1..300; 사전 크기 1..1000; 단어 길이 1..20; 모두 소문자이며 사전 단어는 중복되지 않는다.',('접두사 DP','모든 분할 위치 완전탐색'),
  [['leetcode',['leet','code']],['applepenapple',['apple','pen']],['catsandog',['cats','dog','sand','and','cat']]]),
 (518,'coin_change_ii','change','동적 계획법·수치','coins','동전을 무제한 사용해 amount를 만드는 조합 수를 구한다. 동전 순서는 구별하지 않는다.',
  'amount는 0..5000; 동전 종류 1..300; 서로 다른 액면가 1..5000; 답은 signed 32-bit 범위.',('동전별 조합 DP','액면가별 사용 개수 전수 탐색'),
  [[5,[1,2,5]],[3,[2]],[10,[10]]]),
 (62,'unique_paths','uniquePaths','동적 계획법·격자','dimensions','M×N 격자의 좌상단에서 우하단까지 오른쪽 또는 아래로만 이동하는 경로 수를 구한다.',
  '1<=M,N<=100; 최종 답은 2×10^9 이하.',('격자 DP','이동 순서 이항계수'),[[3,7],[3,2]]),
 (63,'unique_paths_ii','uniquePathsWithObstacles','동적 계획법·격자','matrix','0은 통과 가능, 1은 장애물이다. 좌상단에서 우하단까지 오른쪽·아래로만 이동하는 경로 수를 구한다.',
  '1<=M,N<=100; 원소 0 또는 1; 답은 2×10^9 이하.',('격자 DP','모든 합법 경로 재귀 탐색'),
  [[[[0,0,0],[0,1,0],[0,0,0]]],[[[0,1],[0,0]]]]),
 (64,'minimum_path_sum','minPathSum','동적 계획법·격자','matrix','오른쪽·아래로만 이동할 때 좌상단에서 우하단까지 방문한 칸의 값의 합을 최소화한다.',
  '1<=M,N<=200; 칸 값 0..200.',('최소 누적합 DP','모든 이동 경로 재귀 탐색'),
  [[[[1,3,1],[1,5,1],[4,2,1]]],[[[1,2,3],[4,5,6]]]]),
 (739,'daily_temperatures','dailyTemperatures','스택','vector','각 날짜에서 더 높은 기온이 처음 나타날 때까지 일수를 출력한다. 없으면 0이다.',
  '날짜 수 1..100000; 기온 30..100.',('단조 스택','각 날짜의 미래 직접 탐색'),
  [[[73,74,75,71,69,72,76,73]],[[30,40,50,60]],[[30,60,90]]]),
 (496,'next_greater_element_i','nextGreaterElement','스택','vectors','nums1의 각 원소가 nums2에서 처음 만나는 오른쪽의 더 큰 값을 출력한다. 없으면 -1이다.',
  '1<=N1<=N2<=1000; 값 0..10000; 각 배열은 중복이 없고 nums1은 nums2의 부분집합이다.',('단조 스택 사전','질의별 오른쪽 직접 탐색'),
  [[[4,1,2],[1,3,4,2]],[[2,4],[1,2,3,4]]]),
 (547,'number_of_provinces','findCircleNum','그래프','adjacency','대칭 인접행렬로 주어진 무방향 그래프의 연결 성분 수를 구한다.',
  '정점 수 1..200; 행렬 값 0/1, 대칭, 대각선은 1.',('DFS 연결 성분','서로소 집합 병합'),
  [[[[1,1,0],[1,1,0],[0,0,1]]],[[[1,0,0],[0,1,0],[0,0,1]]]]),
 (207,'course_schedule','canFinish','그래프','edges','선수과목 관계 [a,b]는 b를 먼저 이수해야 a를 들을 수 있다는 뜻이다. 모든 과목을 이수할 수 있으면 1이다.',
  '과목 수 1..2000; 관계 수 0..5000; 과목 번호 0..N-1; 관계 쌍 중복 없음.',('Kahn 위상 정렬','모든 정점 순서의 선수 관계 검사'),
  [[2,[[1,0]]],[2,[[1,0],[0,1]]]]),
 (338,'counting_bits','countBits','비트·수치','scalar','0부터 N까지 각 정수의 이진 표현에서 1의 개수를 순서대로 출력한다.',
  '0<=N<=100000. 기준 구현은 내장 popcount를 사용하지 않는다.',('절반 값 기반 DP','각 수를 2로 나누며 나머지 합산'),[[2],[5]]),
 (912,'sort_an_array','sortArray','정렬','vector','정수 배열을 오름차순으로 정렬해 출력한다.',
  '1<=N<=50000; 원소 -50000..50000. 원 명세의 요구는 내장 정렬 없이 O(N log N).',('병합 정렬','최소 원소 반복 추출'),[[[5,2,3,1]],[[5,1,1,2,0,0]]]),
]

CATALOG = {row[0]: dict(zip(('id','slug','function','category','interface','summary','constraints','oracle_methods','public_examples'),row)) for row in ROWS}

SECOND_ORACLES = {
 1:'값·인덱스 정렬 후 양끝 포인터 탐색',
 121:'소형 매매 쌍 전수 검사 / 대형 역방향 최고 매도가 순회',
 53:'소형 구간 전수 검사 / 대형 누적합과 최소 접두합',
 387:'소형 위치 전수 대조 / 대형 문자별 첫·마지막 위치 비교',
 3:'소형 부분문자열 전수 검사 / 대형 집합 기반 가변 구간',
 139:'메모이제이션 분할 위치 탐색',
 518:'메모이제이션 액면가별 개수 탐색 / 최대공약수 도달 불가 증명',
 63:'메모이제이션을 사용한 도착점 기준 재귀 경로 계산',
 64:'메모이제이션을 사용한 도착점 기준 재귀 비용 계산',
 739:'소형 미래 직접 탐색 / 대형 기온별 다음 위치 역방향 순회',
 207:'소형 정점 순열 전수 검사 / 대형 색상 상태 반복 DFS',
 912:'소형 최소값 반복 추출 / 대형 정수 빈도 계수 정렬',
}
for _pid,_method in SECOND_ORACLES.items():
    CATALOG[_pid]['oracle_methods']=(CATALOG[_pid]['oracle_methods'][0],_method)

FORMATS = {
 'vector':'첫 줄 N, 다음 줄 N개 정수.',
 'vector_target':'첫 줄 N target, 다음 줄 N개 정수.',
 'strings':'첫 줄 s, 다음 줄 t. 각 줄은 문자열 하나다.',
 'string':'첫 줄 전체가 문자열이다. 공백도 문자로 보존하며 LC_0003은 빈 줄을 허용한다.',
 'words':'첫 줄 s, 둘째 줄 사전 크기 K, 이후 K줄에 단어 하나씩.',
 'coins':'첫 줄 amount K, 다음 줄 K개의 서로 다른 동전 액면가.',
 'dimensions':'첫 줄 M N.',
 'matrix':'첫 줄 M N, 이후 M줄에 N개 정수.',
 'vectors':'첫 줄 N1 N2, 둘째 줄 nums1, 셋째 줄 nums2.',
 'adjacency':'첫 줄 N, 이후 N줄에 N개의 0/1 정수.',
 'edges':'첫 줄 과목 수 N과 관계 수 E, 이후 E줄에 a b.',
 'scalar':'첫 줄 정수 N.',
}


def encode(pid,args):
    kind=CATALOG[pid]['interface']; vec=lambda a:' '.join(map(str,a))
    if kind=='vector':lines=[str(len(args[0])),vec(args[0])]
    elif kind=='vector_target':lines=[f'{len(args[0])} {args[1]}',vec(args[0])]
    elif kind=='strings':lines=args
    elif kind=='string':lines=[args[0]]
    elif kind=='words':lines=[args[0],str(len(args[1])),*args[1]]
    elif kind=='coins':lines=[f'{args[0]} {len(args[1])}',vec(args[1])]
    elif kind=='dimensions':lines=[vec(args)]
    elif kind=='matrix':lines=[f'{len(args[0])} {len(args[0][0])}',*map(vec,args[0])]
    elif kind=='vectors':lines=[f'{len(args[0])} {len(args[1])}',vec(args[0]),vec(args[1])]
    elif kind=='adjacency':lines=[str(len(args[0])),*map(vec,args[0])]
    elif kind=='edges':lines=[f'{args[0]} {len(args[1])}',*map(vec,args[1])]
    elif kind=='scalar':lines=[str(args[0])]
    else:raise ValueError(kind)
    return '\n'.join(lines)+'\n'


def decode(pid,text):
    kind=CATALOG[pid]['interface']
    if kind=='string':return [text.removesuffix('\n').removesuffix('\r')]
    if kind=='strings':return text.splitlines()
    if kind=='words':
        lines=text.splitlines();assert len(lines)==int(lines[1])+2
        return [lines[0],lines[2:]]
    t=list(map(int,text.split()))
    if kind=='vector':assert len(t)==1+t[0];return [t[1:]]
    if kind=='vector_target':assert len(t)==2+t[0];return [t[2:],t[1]]
    if kind=='coins':assert len(t)==2+t[1];return [t[0],t[2:]]
    if kind=='dimensions':assert len(t)==2;return t
    if kind in ('matrix','adjacency'):
        m,n,start=(t[0],t[1],2) if kind=='matrix' else (t[0],t[0],1)
        assert len(t)==start+m*n
        return [[t[i:i+n] for i in range(start,len(t),n)]]
    if kind=='vectors':assert len(t)==2+t[0]+t[1];return [t[2:2+t[0]],t[2+t[0]:]]
    if kind=='edges':assert len(t)==2+2*t[1];return [t[0],[t[i:i+2] for i in range(2,len(t),2)]]
    if kind=='scalar':assert len(t)==1;return t
    raise ValueError(kind)


def output(value):
    if isinstance(value,bool):return str(int(value))+'\n'
    if isinstance(value,list):return ' '.join(map(str,value))+'\n'
    return str(value)+'\n'
