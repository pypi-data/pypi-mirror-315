from setuptools import setup, find_packages

setup(
    name='altikrity',  # اسم المكتبة
    version='0.5',  # الإصدار
    packages=find_packages(),  # حزمة المكتبة
    install_requires=[  # المتطلبات
        # لا حاجة لإضافة zlib هنا، لأنها مضمنة في بايثون
    ],
    author='Abdullah',  # اسم المؤلف
    author_email='abdullah.alttikrity@gmail.com',  # البريد الإلكتروني
    description='A powerful encryption library with multi-layer encryption techniques.',  # وصف المكتبة
    long_description="This is a powerful encryption library with multi-layer encryption techniques.",
    long_description_content_type='text/markdown',
    classifiers=[  # تصنيف المكتبة
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # الحد الأدنى للإصدار المدعوم من بايثون
)
