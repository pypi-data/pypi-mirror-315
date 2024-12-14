from setuptools import setup, find_packages

setup(
    name="wodnjspackage",  # PyPI에 등록될 패키지 이름 (고유해야 함)
    version="0.3.0",  # 패키지 버전
    description="A sample Python package",  # 간단한 설명
    long_description=open("README.md").read(),  # PyPI에 표시될 상세 설명
    long_description_content_type="text/markdown",
    author="Your Name",  # 작성자 이름
    author_email="your_email@example.com",  # 작성자 이메일
    url="https://github.com/yourusername/my_package",  # 프로젝트 URL
    packages=find_packages(),  # 패키지 목록 자동 탐색 필수!!
    python_requires=">=3.6",  # 지원하는 Python 버전
)
