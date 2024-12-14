import subprocess

def solve_flag_problem():
    command = ["/flag"]

    try:
        # 프로그램 실행
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 프로그램의 출력 (문제 읽기)
        problem = process.stdout.readline().strip()
        print(f"Problem: {problem}")

        # 문제에서 숫자 추출 후 계산
        numbers = [int(num) for num in problem.split() if num.isdigit()]
        result = numbers[0] * numbers[1] + numbers[2]
        print(f"Calculated Result: {result}")

        # 결과를 프로그램에 입력으로 전달
        process.stdin.write(f"{result}\n")
        process.stdin.flush()

        # 최종 출력 읽기
        output = process.stdout.read().strip()
        print(f"Program Output: {output}")
        
        return output
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    solve_flag_problem()