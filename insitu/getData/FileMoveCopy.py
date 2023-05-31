#%%
import shutil
import os

def search_subdirectories(directory):
    try:
        # 디렉토리 내의 모든 파일과 디렉토리를 조회
        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry) # 현재 entry의 절대 경로 생성
            if os.path.isdir(entry_path): # 디렉토리인 경우
                print(f"디렉토리: {entry_path}")
                search_subdirectories(entry_path) # 재귀적으로 하위 디렉토리 탐색
            else: # 파일인 경우
                print(f"파일: {entry_path}")
    except Exception as e:
        print(f"디렉토리 탐색 중 에러가 발생하였습니다: {e}")

def explore_directory(dir_path, depth=0, max_depth=3):
    """
    지정된 디렉토리를 탐색하여 하위 디렉토리까지 깊이 설정에 따라 탐색하는 함수

    Args:
        dir_path (str): 탐색을 시작할 디렉토리 경로
        depth (int): 현재 탐색 중인 디렉토리의 깊이 (기본값: 0)
        max_depth (int): 최대 탐색 깊이 (기본값: 3)

    Returns:
        None
    """
    if depth > max_depth:
        return

    # 현재 디렉토리 출력
    print(f"[Depth {depth}] {dir_path}")

    # 현재 디렉토리의 하위 디렉토리 탐색
    for entry in os.listdir(dir_path):
        entry_path = os.path.join(dir_path, entry)
        if os.path.isdir(entry_path):
            explore_directory(entry_path, depth + 1, max_depth)


# 파일 이동
def move_file(src_path, dst_path):
    try:
        shutil.move(src_path, dst_path)
        print(f"{src_path}을(를) {dst_path}로 이동하였습니다.")
    except Exception as e:
        print(f"파일 이동 중 에러가 발생하였습니다: {e}")

# 파일 복사
def copy_file(src_path, dst_path):
    try:
        shutil.copy(src_path, dst_path)
        print(f"{src_path}을(를) {dst_path}로 복사하였습니다.")
    except Exception as e:
        print(f"파일 복사 중 에러가 발생하였습니다: {e}")

#%%
# src_root = r"\\10.108.0.221\\realtime_g2gs\\"
src_root_2021 = r"\\10.108.0.221\\g2gs\\" #2021
src_root_2022 = r"\\10.108.0.221\\realtime_g2gs\\" #2022
dst_root = "D:\\Data\\GK2_GC2\\"
yy = [2021, 2022]
mm = ['02', '05', '08', '11']
var = ['Chl', 'CDOM', 'TSS', 'IOP']
level = 'LA_L2'
version = 'V1.0.0'
time = '031530'
slot = 'S007'
# endstr = 'S007_Chl.nc' #Chl, CDOM, TSS, IOP

#%%
for y in yy:
    y = str(y)
    for m in mm:
        
        if y == '2021':
            src_path0 = src_root_2021+y+"\\"+m+"\\"
        else:
            src_path0 = src_root_2022+y+"\\"+m+"\\"
        
        flist0 = os.listdir(src_path0)
        flist0.pop()
        
        for f in flist0:
            src_path1 = src_path0 + f + "\\" + level + "\\" + version
            flist1 = os.listdir(src_path1)
            flist_time = [file for file in flist1 if time in file]
        
            try: 
                src_path2 = src_path1 + "\\" + str(flist_time[0])
                flist2 = os.listdir(src_path2)
        
                for v in var: 
                    endstr = slot + '_' + v + '.nc'
                    fname = [file for file in flist2 if file.endswith(endstr)]
                    src_path = src_path2 + '\\' + str(fname[0])
                    dst_path = dst_root +y+"\\"+m+"\\"+v+"\\"

                    if not os.path.exists(dst_path):
                        os.makedirs(dst_path)
                        
                    copy_file(src_path, dst_path)
                    print(fname[0])
        
            except : IndexError
# %%
