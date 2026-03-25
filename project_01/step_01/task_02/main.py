def print_table(header, data_list):
    """데이터 리스트를 깔끔한 표 형식으로 출력하는 공통 함수"""
    if not data_list:
        return

    # 모든 행(헤더 포함)을 조사하여 컬럼별 최대 너비 계산
    col_widths = []
    for i in range(len(header)):
        max_w = len(header[i])
        for item in data_list:
            if len(str(item[1][i])) > max_w:
                max_w = len(str(item[1][i]))
        col_widths.append(max_w + 2)

    # 한 줄 출력용 내부 함수
    def print_row(row):
        formatted = ''
        for i, val in enumerate(row):
            formatted += f'{str(val):<{col_widths[i]}}| '
        print(formatted.rstrip('| '))

    # 표 상단 출력
    print_row(header)
    print('-' * (sum(col_widths) + len(col_widths) * 2))
    for item in data_list:
        print_row(item[1])

def save_to_binary(file_path, header, data_list):
    """모든 컬럼 데이터를 이진 규격으로 저장 (메모장에서 깨짐)"""
    try:
        with open(file_path, 'wb') as f:
            # 헤더 정보도 나중에 복원하기 위해 저장
            header_str = '\t'.join(header)
            h_bytes = header_str.encode('utf-8')
            f.write(len(h_bytes).to_bytes(4, byteorder='big')) # 헤더 길이(4바이트)
            f.write(h_bytes)

            for item in data_list:
                # 전체 컬럼 데이터를 탭으로 묶음
                row_str = '\t'.join(item[1])
                r_bytes = row_str.encode('utf-8')
                # 데이터의 길이를 먼저 쓰고(4바이트), 내용을 씀
                f.write(len(r_bytes).to_bytes(4, byteorder='big'))
                f.write(r_bytes)
        print(f"\n[보안] 진짜 이진 파일 저장 완료: {file_path}")
    except Exception as e:
        print(f"[오류] 저장 실패: {e}")

def read_and_print_binary(file_path):
    """길이 정보를 바탕으로 이진 데이터를 완벽히 복원"""
    print(f'\n--- [이진 파일({file_path}) 정밀 복원 결과] ---')
    try:
        with open(file_path, 'rb') as f:
            # 1. 헤더 복원
            h_len_bytes = f.read(4)
            if not h_len_bytes: return
            h_len = int.from_bytes(h_len_bytes, byteorder='big')
            header = f.read(h_len).decode('utf-8').split('\t')

            # 2. 데이터 복원
            binary_data = []
            while True:
                len_bytes = f.read(4) # 데이터 길이 4바이트 읽기
                if not len_bytes: break
                
                d_len = int.from_bytes(len_bytes, byteorder='big')
                row_content = f.read(d_len).decode('utf-8')
                parts = row_content.split('\t')
                
                # 원본 구조 [정렬값, [전체컬럼]] 유지
                binary_data.append([0, parts]) 
        
        # 앞서 만든 표 출력 함수 재사용
        print_table(header, binary_data)
    except Exception as e:
        print(f"[오류] 복원 실패: {e}")
        
def process_inventory():
    file_name = 'Mars_Base_Inventory_List.csv'
    danger_file = 'Mars_Base_Inventory_danger.csv'
    binary_file = 'Mars_Base_Inventory_List.bin'
    
    all_data = []

    try:
        # 1. 원본 파일 로드
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            if not lines: return
            header = [h.strip() for h in lines[0].split(',')]

        # 2. 사용자 컬럼 선택 및 데이터 분석
        print(f'탐지된 컬럼: {header}')
        target_col = input('인화성 지수 기준이 될 컬럼명을 입력하세요: ').strip()
        if target_col not in header:
            print('해당 컬럼을 찾을 수 없습니다.')
            return
        flam_idx = header.index(target_col)

        for line in lines[1:]:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) == len(header):
                try:
                    val = float(parts[flam_idx])
                except ValueError:
                    val = -1.0
                all_data.append([val, parts])

        # 3. 전체 데이터 출력 (원본 상태)
        print('\n[1단계] 원본 데이터 전체 출력')
        print_table(header, all_data)

        # 4. 정렬 및 위험 물질 필터링
        all_data.sort(key=lambda x: x[0], reverse=True)
        danger_list = [item for item in all_data if item[0] >= 0.7]

        print('\n[2단계] 인화성 순 정렬 및 위험 물질(0.7 이상) 추출')
        if danger_list:
            print_table(header, danger_list)
            # CSV 저장
            with open(danger_file, 'w', encoding='utf-8') as f:
                f.write(','.join(header) + '\n')
                for item in danger_list:
                    f.write(','.join(item[1]) + '\n')
            print(f'\n[시스템] 위험 물질 목록 저장 완료: {danger_file}')
        else:
            print('위험 등급의 물질이 없습니다.')

        # 5. 이진 파일 저장 및 출력 분리 실행
        save_to_binary(binary_file, header, all_data)
        read_and_print_binary(binary_file)

    except FileNotFoundError:
        print(f"'{file_name}' 파일이 존재하지 않습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == '__main__':
    process_inventory()