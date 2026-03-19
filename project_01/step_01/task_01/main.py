import os

# 상수 설정 (PEP 8: 대문자 사용, = 앞뒤 공백)
LOG_FILE = 'mission_computer_main.log'
ERROR_FILE = 'error.log'
KEYWORDS = ['ERROR', 'FAIL', 'CRITICAL', 'unstable', 'explosion', 'warning']


def analyze_logs():
    """로그 파일을 분석하고 결과를 출력 및 저장한다."""
    print('Hello Mars')
    print('-' * 20)

    lines = []
    error_lines = []

    # 1. 파일 읽기 및 예외 처리
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f: 
            for line in f:
                clean_line = line.strip()
                if not clean_line:
                    continue
                
                # 전체 내용 출력
                print(clean_line)
                lines.append(clean_line)

                # 문제 로그 감지 (보너스 과제 준비)
                for key in KEYWORDS:
                    if key in clean_line:
                        error_lines.append(clean_line)
                        break
    except FileNotFoundError:
        print(f"'{LOG_FILE}' 파일을 찾을 수 없습니다.")
        return
    except Exception as e:
        print(f'오류 발생: {e}')
        return

    # 2. 시간 역순 출력 (보너스 과제)
    print('\n[시간 역순 정렬 결과]')
    print('-' * 20)
    # 로그 형식이 고정되어 있으므로 문자열 기반 역순 정렬 가능
    reversed_lines = sorted(lines, reverse=True)
    for line in reversed_lines:
        print(line)

    # 3. 문제 로그 파일 저장 (보너스 과제)
    if error_lines:
        try:
            with open(ERROR_FILE, 'w', encoding='utf-8') as f:
                for line in error_lines:
                    f.write(line + '\n')
            print(f'\n[알림] 문제가 발견되어 {ERROR_FILE}에 저장되었습니다.')
        except Exception as e:
            print(f'파일 저장 중 오류 발생: {e}')


if __name__ == '__main__':
    analyze_logs()



# 키워드 검색시, 대소문자 관련 처리 필요
# 'r' , 'rb' 차이 확인
# 'r'  : 텍스트 파일을 읽을 때 사용
# 'rb' : 바이너리 파일을 읽을 때 사용
# 라이브러리 없이 파일의 크기 확인 seek(), tell() 사용
# chunk 단위로 끊을 때, 로그의 중간에서 끊길 수 있는 문제 관련 처리
