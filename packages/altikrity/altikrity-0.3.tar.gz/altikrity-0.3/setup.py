from setuptools import setup, find_packages

setup(
    name='altikrity',  # اسم المكتبة
    version='0.3',  # الإصدار
    packages=find_packages(),  # حزمة المكتبة
    install_requires=[  # المتطلبات
        'zlib',  # إذا كنت تستخدم مكتبات أخرى، أضفها هنا
    ],
    author='Abdullah',  # اسم المؤلف
    author_email='abdullah.alttikrity@gmail.com',  # البريد الإلكتروني
    description='A powerful encryption library with multi-layer encryption techniques.',  # وصف المكتبة
    long_description=open('README.md').read(),  # وصف مفصل من ملف README
    long_description_content_type='text/markdown',
    classifiers=[  # تصنيف المكتبة
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # الحد الأدنى للإصدار المدعوم من بايثون
)
