from setuptools import setup, find_packages

setup(
    name="ProtectedEmailSender",
    version="1.0.0",
    description="🔐 Protected Email Sender Tool by DARKBOSS1BD",
    author="DARKBOSS1BD",
    packages=find_packages(),
    install_requires=[
        "secure-smtplib",
    ],
    entry_points={
        'console_scripts': [
            'protected-email-sender=protected_email_sender:main',
        ],
    },
    python_requires='>=3.6',
)