from setuptools import setup,find_packages

setup(
    name='tiktik',
    version='0.4',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
    "console_scripts": [
        "tiktik_kokul=tiktik.main:kokul",
        "tiktik_appleornotnaive=tiktik.main:appleornotnaive",
        "tiktik_appleornotcandi=tiktik.main:appleornotcandi",
        "tiktik_candsunnyorrain=tiktik.main:candsunnyorrain",
        "tiktik_carpreferencesfinds=tiktik.main:carpreferencesfinds",
        "tiktik_dbscan=tiktik.main:dbscan",
        "tiktik_diabetes_logistic=tiktik.main:diabetes_logistic",
        "tiktik_enjoysportfinds=tiktik.main:enjoysportfinds",
        "tiktik_finds=tiktik.main:finds",
        "tiktik_heirarchialclust=tiktik.main:heirarchialclust",
        "tiktik_heirarkmeansexam=tiktik.main:heirarkmeansexam",
        "tiktik_diabeteshmm=tiktik.main:diabeteshmm",
        "tiktik_hmmrainy=tiktik.main:hmmrainy",
        "tiktik_id3=tiktik.main:id3",
        "tiktik_kmeanscluster=tiktik.main:kmeanscluster",
        "tiktik_knniris=tiktik.main:knniris",
        "tiktik_naiveposorneg=tiktik.main:naiveposorneg",
        "tiktik_naivetsampletext=tiktik.main:naivetsampletext",
        "tiktik_orangeorapple=tiktik.main:orangeorapple",
        "tiktik_naivespamornot=tiktik.main:naivespamornot",
        "tiktik_svmiris=tiktik.main:svmiris",
        "tiktik_backwardimage=tiktik.main:backwardimage",
    ],
},

)