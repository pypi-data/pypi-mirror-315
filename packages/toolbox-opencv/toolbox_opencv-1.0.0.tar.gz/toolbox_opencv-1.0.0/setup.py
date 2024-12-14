from setuptools import setup, find_packages

setup(
    name='toolbox_opencv',              # Tên gói
    version='1.0.0',                # Phiên bản
    packages=find_packages(),       # Tìm và đóng gói các module
    install_requires=[              # Các thư viện cần thiết
        'numpy',
        'opencv-python'
    ],
    entry_points={                  # Tùy chọn chạy file chính
        'console_scripts': [
            'my_project = my_project.main:main',  # Lệnh terminal
        ]
    }
)