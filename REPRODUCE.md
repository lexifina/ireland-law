# How this repository was made

This file records where every part of this repository comes from, how it was built, how it was checked, what was done
by hand, and what an AI model did and did not do. The build writes it, so it describes the build that made this
commit.

## Short version

```sh
git clone https://github.com/lexifina/ireland-law && cd ireland-law
pip install pymupdf
GITLAW_PUBLIC_REBUILD=1 python -X utf8 tools/build.py --offline --repo ../rebuilt --today 2026-10-28
git -C ../rebuilt rev-parse main        # the same hash as this repository's main
python -X utf8 tools/check_repo.py --repo ../rebuilt
python -X utf8 tools/test_repo.py --repo ../rebuilt
```

`tools/build.py` needs Python 3.12 or later with PyMuPDF (`pymupdf`), and git. It reads the retrieved files of the
Revised Acts site (the alphabetical list and the revision PDFs, each kept under the name `cache_path()` gives its URL)
and writes this repository into `--repo`. How the files were retrieved is not part of this record. With the same PDFs
and the same `--today` it gives the same commits with the same hashes. `GITLAW_PUBLIC_REBUILD=1` skips Lexifina's own
publish check, which is not part of this record. `data/versions.json` lists every revision with the sha256 of
its PDF; the Commission replaces revisions as it updates them, and then the hashes change too.

## Sources

All legal text, and all dates and amending laws, come from the **Revised Acts** of the Law Reform Commission of
Ireland (https://revisedacts.lawreform.ie). Nothing was typed in, summarised or rewritten. The build read the
alphabetical list (`/revacts/alpha`, which links each act's current and previous revisions as PDFs, with the day each
was listed) and 2566 revision PDFs:

| Act | Number | Folder | Revisions | Updated to | Files today |
| --- | --- | --- | ---: | --- | ---: |
| Public Bodies Corrupt Practices Act 1889 | 1889 c. 69 | `public-bodies-corrupt-practices-act-1889/` | 1 | 2018-07-30 to 2018-07-30 | 11 |
| Sale of Goods Act 1893 | 1893 c. 71 | `sale-of-goods-act-1893/` | 4 | 2016-06-30 to 2025-10-10 | 67 |
| Merchant Shipping Act 1894 | 1894 c. 60 | `merchant-shipping-act-1894/` | 4 | 2021-04-28 to 2025-07-29 | 768 |
| Prevention of Corruption Act 1906 | 1906 c. 34 | `prevention-of-corruption-act-1906/` | 1 | 2018-07-30 to 2018-07-30 | 5 |
| Probation Of Offenders Act 1907 | 1907 c. 17 | `probation-of-offenders-act-1907/` | 1 | 2026-02-24 to 2026-02-24 | 12 |
| Punishment Of Incest Act 1908 | 1908 c. 45 | `punishment-of-incest-act-1908/` | 1 | 2023-02-24 to 2023-02-24 | 9 |
| Prevention of Corruption Act 1916 | 1916 c. 64 | `prevention-of-corruption-act-1916/` | 1 | 2018-07-30 to 2018-07-30 | 5 |
| Roads Act 1920 | 1920 c. 72 | `roads-act-1920/` | 2 | 2024-02-01 to 2025-03-27 | 23 |
| Ministers and Secretaries Act 1924 | No. 16 of 1924 | `ministers-and-secretaries-act-1924/` | 1 | 2025-02-21 to 2025-02-21 | 22 |
| Firearms Act 1925 | No. 17 of 1925 | `firearms-act-1925/` | 6 | 2018-05-25 to 2026-09-01 | 61 |
| Wireless Telegraphy Act 1926 | No. 45 of 1926 | `wireless-telegraphy-act-1926/` | 7 | 2024-07-29 to 2026-03-11 | 26 |
| Electricity (Supply) Act 1927 | No. 27 of 1927 | `electricity-supply-act-1927/` | 1 | 2024-07-23 to 2024-07-23 | 117 |
| Legitimacy Act 1931 | No. 13 of 1931 | `legitimacy-act-1931/` | 2 | 2016-01-01 to 2019-05-28 | 14 |
| Road Transport Act 1933 | No. 8 of 1933 | `road-transport-act-1933/` | 2 | 2016-06-30 to 2019-05-28 | 75 |
| Foreshore Act 1933 | No. 12 of 1933 | `foreshore-act-1933/` | 6 | 2017-07-26 to 2024-05-14 | 52 |
| Road Transport Act 1934 | No. 17 of 1934 | `road-transport-act-1934/` | 2 | 2016-06-30 to 2019-05-28 | 16 |
| Road Transport Act 1935 | No. 23 of 1935 | `road-transport-act-1935/` | 2 | 2016-06-30 to 2019-05-28 | 10 |
| Ministerial and Parliamentary Offices Act 1938 | No. 38 of 1938 | `ministerial-and-parliamentary-offices-act-1938/` | 1 | 2025-11-06 to 2025-11-06 | 62 |
| Offences Against the State Act 1939 | No. 13 of 1939 | `offences-against-the-state-act-1939/` | 1 | 2025-10-01 to 2025-10-01 | 71 |
| Tourist Traffic Act 1939 | No. 24 of 1939 | `tourist-traffic-act-1939/` | 4 | 2016-08-31 to 2025-06-01 | 58 |
| Ministers and Secretaries (Amendment) Act 1939 | No. 36 of 1939 | `ministers-and-secretaries-amendment-act-1939/` | 4 | 2025-04-01 to 2026-03-01 | 15 |
| Enforcement of Court Orders Act 1940 | No. 23 of 1940 | `enforcement-of-court-orders-act-1940/` | 3 | 2021-04-27 to 2026-07-01 | 12 |
| Central Bank Act 1942 | No. 22 of 1942 | `central-bank-act-1942/` | 26 | 2019-01-29 to 2026-08-01 | 303 |
| Arterial Drainage Act 1945 | No. 3 of 1945 | `arterial-drainage-act-1945/` | 1 | 2026-05-20 to 2026-05-20 | 83 |
| Industrial Relations Act 1946 | No. 26 of 1946 | `industrial-relations-act-1946/` | 15 | 2018-12-19 to 2025-12-18 | 96 |
| Health Act 1947 | No. 28 of 1947 | `health-act-1947/` | 41 | 2020-04-08 to 2026-05-14 | 157 |
| Tourist Traffic Act 1952 | No. 15 of 1952 | `tourist-traffic-act-1952/` | 3 | 2016-12-28 to 2020-10-18 | 56 |
| Finance (Excise Duties) (Vehicles) Act 1952 | No. 24 of 1952 | `finance-excise-duties-vehicles-act-1952/` | 2 | 2024-03-27 to 2026-06-01 | 8 |
| Merchant Shipping (Safety Convention) Act 1952 | No. 29 of 1952 | `merchant-shipping-safety-convention-act-1952/` | 11 | 2021-05-20 to 2026-04-01 | 50 |
| Health Act 1953 | No. 26 of 1953 | `health-act-1953/` | 1 | 2026-02-03 to 2026-02-03 | 74 |
| Defence Act 1954 | No. 18 of 1954 | `defence-act-1954/` | 8 | 2017-04-07 to 2024-11-06 | 407 |
| State Property Act 1954 | No. 25 of 1954 | `state-property-act-1954/` | 1 | 2023-03-01 to 2023-03-01 | 41 |
| Tourist Traffic Act 1955 | No. 5 of 1955 | `tourist-traffic-act-1955/` | 3 | 2016-08-31 to 2020-09-16 | 17 |
| Transport (Miscellaneous Provisions) Act 1955 | No. 21 of 1955 | `transport-miscellaneous-provisions-act-1955/` | 2 | 2016-08-31 to 2019-05-28 | 6 |
| Gaming and Lotteries Act 1956 | No. 2 of 1956 | `gaming-and-lotteries-act-1956/` | 2 | 2021-11-10 to 2023-07-31 | 61 |
| Irish Nationality and Citizenship Act 1956 | No. 26 of 1956 | `irish-nationality-and-citizenship-act-1956/` | 6 | 2021-08-10 to 2026-06-12 | 44 |
| Civil Service Regulation Act 1956 | No. 46 of 1956 | `civil-service-regulation-act-1956/` | 2 | 2024-12-01 to 2026-07-15 | 29 |
| Married Women’s Status Act 1957 | No. 5 of 1957 | `married-women-s-status-act-1957/` | 1 | 2019-02-01 to 2019-02-01 | 22 |
| Statute of Limitations 1957 | No. 6 of 1957 | `statute-of-limitations-1957/` | 2 | 2018-06-09 to 2025-12-09 | 84 |
| Tourist Traffic Act 1957 | No. 27 of 1957 | `tourist-traffic-act-1957/` | 3 | 2016-08-31 to 2020-09-16 | 12 |
| Greyhound Industry Act 1958 | No. 12 of 1958 | `greyhound-industry-act-1958/` | 4 | 2022-03-01 to 2026-02-05 | 64 |
| Transport Act 1958 | No. 19 of 1958 | `transport-act-1958/` | 2 | 2016-08-31 to 2019-05-28 | 32 |
| Fisheries (Consolidation) Act 1959 | No. 14 of 1959 | `fisheries-consolidation-act-1959/` | 1 | 2025-04-16 to 2025-04-16 | 352 |
| Defence (Amendment) (No. 2) Act 1960 | No. 44 of 1960 | `defence-amendment-no-2-act-1960/` | 3 | 2016-06-30 to 2022-04-04 | 9 |
| Road Traffic Act 1961 | No. 24 of 1961 | `road-traffic-act-1961/` | 28 | 2019-01-21 to 2026-09-04 | 156 |
| Health (Corporate Bodies) Act 1961 | No. 27 of 1961 | `health-corporate-bodies-act-1961/` | 1 | 2026-01-01 to 2026-01-01 | 12 |
| Courts (Supplemental Provisions) Act 1961 | No. 39 of 1961 | `courts-supplemental-provisions-act-1961/` | 1 | 2026-06-23 to 2026-06-23 | 88 |
| Civil Liability Act 1961 | No. 41 of 1961 | `civil-liability-act-1961/` | 3 | 2018-10-01 to 2023-07-31 | 81 |
| Coroners Act 1962 | No. 9 of 1962 | `coroners-act-1962/` | 5 | 2020-06-15 to 2025-04-02 | 96 |
| Official Secrets Act 1963 | No. 1 of 1963 | `official-secrets-act-1963/` | 1 | 2021-04-15 to 2021-04-15 | 19 |
| Firearms Act 1964 | No. 1 of 1964 | `firearms-act-1964/` | 3 | 2016-01-01 to 2021-12-27 | 33 |
| Guardianship of Infants Act 1964 | No. 7 of 1964 | `guardianship-of-infants-act-1964/` | 6 | 2019-01-01 to 2026-07-21 | 64 |
| Registration of Title Act 1964 | No. 16 of 1964 | `registration-of-title-act-1964/` | 4 | 2018-04-04 to 2023-07-17 | 130 |
| Civil Liability (Amendment) Act 1964 | No. 17 of 1964 | `civil-liability-amendment-act-1964/` | 2 | 2017-04-13 to 2020-05-21 | 9 |
| Extradition Act 1965 | No. 17 of 1965 | `extradition-act-1965/` | 8 | 2019-02-01 to 2026-08-10 | 68 |
| Succession Act 1965 | No. 27 of 1965 | `succession-act-1965/` | 4 | 2017-11-02 to 2023-11-01 | 143 |
| Tourist Traffic Act 1966 | No. 3 of 1966 | `tourist-traffic-act-1966/` | 2 | 2016-08-31 to 2020-09-16 | 8 |
| Housing Act 1966 | No. 21 of 1966 | `housing-act-1966/` | 5 | 2017-07-01 to 2024-01-01 | 126 |
| Industrial Training Act 1967 | No. 5 of 1967 | `industrial-training-act-1967/` | 18 | 2018-09-12 to 2026-07-15 | 52 |
| Diplomatic Relations and Immunities Act 1967 | No. 8 of 1967 | `diplomatic-relations-and-immunities-act-1967/` | 2 | 2025-07-15 to 2026-04-28 | 60 |
| Criminal Procedure Act 1967 | No. 12 of 1967 | `criminal-procedure-act-1967/` | 3 | 2017-11-27 to 2022-02-28 | 57 |
| Redundancy Payments Act 1967 | No. 21 of 1967 | `redundancy-payments-act-1967/` | 12 | 2016-08-01 to 2023-07-03 | 65 |
| Firearms (Proofing) Act 1968 | No. 20 of 1968 | `firearms-proofing-act-1968/` | 2 | 2016-01-01 to 2019-05-28 | 15 |
| Road Traffic Act 1968 | No. 25 of 1968 | `road-traffic-act-1968/` | 5 | 2018-11-05 to 2025-03-01 | 70 |
| Industrial Relations Act 1969 | No. 14 of 1969 | `industrial-relations-act-1969/` | 2 | 2019-01-01 to 2021-07-29 | 27 |
| Health Act 1970 | No. 1 of 1970 | `health-act-1970/` | 14 | 2020-02-17 to 2025-06-01 | 117 |
| Tourist Traffic Act 1970 | No. 16 of 1970 | `tourist-traffic-act-1970/` | 3 | 2016-08-31 to 2020-09-16 | 8 |
| Local Government Services (Corporate Bodies) Act 1971 | No. 6 of 1971 | `local-government-services-corporate-bodies-act-1971/` | 2 | 2019-02-18 to 2022-03-31 | 10 |
| Road Transport Act 1971 | No. 8 of 1971 | `road-transport-act-1971/` | 2 | 2016-06-30 to 2019-05-28 | 14 |
| Firearms Act 1971 | No. 13 of 1971 | `firearms-act-1971/` | 2 | 2016-01-01 to 2019-05-28 | 8 |
| Redundancy Payments Act 1971 | No. 20 of 1971 | `redundancy-payments-act-1971/` | 2 | 2019-02-01 to 2020-10-14 | 22 |
| Central Bank Act 1971 | No. 24 of 1971 | `central-bank-act-1971/` | 3 | 2025-01-01 to 2026-07-10 | 102 |
| Employment Agency Act 1971 | No. 27 of 1971 | `employment-agency-act-1971/` | 2 | 2016-06-30 to 2019-09-01 | 16 |
| National College of Art and Design Act 1971 | No. 28 of 1971 | `national-college-of-art-and-design-act-1971/` | 1 | 2022-11-10 to 2022-11-10 | 41 |
| European Communities Act 1972 | No. 27 of 1972 | `european-communities-act-1972/` | 2 | 2017-04-13 to 2020-08-26 | 8 |
| Minimum Notice and Terms of Employment Act 1973 | No. 4 of 1973 | `minimum-notice-and-terms-of-employment-act-1973/` | 2 | 2017-09-01 to 2020-10-14 | 22 |
| Air Navigation and Transport Act 1973 | No. 29 of 1973 | `air-navigation-and-transport-act-1973/` | 2 | 2019-08-01 to 2023-05-01 | 23 |
| Law Reform Commission Act 1975 | No. 3 of 1975 | `law-reform-commission-act-1975/` | 2 | 2015-11-30 to 2019-03-05 | 16 |
| Air Navigation and Transport Act 1975 | No. 9 of 1975 | `air-navigation-and-transport-act-1975/` | 2 | 2020-09-17 to 2022-12-07 | 11 |
| Local Authorities (Traffic Wardens) Act 1975 | No. 14 of 1975 | `local-authorities-traffic-wardens-act-1975/` | 3 | 2018-03-01 to 2023-01-01 | 11 |
| Juries Act 1976 | No. 4 of 1976 | `juries-act-1976/` | 1 | 2026-02-03 to 2026-02-03 | 42 |
| Family Law (Maintenance of Spouses and Children) Act 1976 | No. 11 of 1976 | `family-law-maintenance-of-spouses-and-children-act-1976/` | 4 | 2016-01-18 to 2020-05-04 | 39 |
| Industrial Relations Act 1976 | No. 15 of 1976 | `industrial-relations-act-1976/` | 2 | 2019-01-01 to 2020-02-01 | 13 |
| Family Home Protection Act 1976 | No. 27 of 1976 | `family-home-protection-act-1976/` | 2 | 2019-01-01 to 2023-06-22 | 17 |
| Gas Act 1976 | No. 30 of 1976 | `gas-act-1976/` | 2 | 2023-01-01 to 2024-06-01 | 75 |
| Criminal Law Act 1976 | No. 32 of 1976 | `criminal-law-act-1976/` | 1 | 2026-07-23 to 2026-07-23 | 17 |
| Wildlife Act 1976 | No. 39 of 1976 | `wildlife-act-1976/` | 9 | 2018-12-20 to 2024-05-16 | 87 |
| Local Government (Water Pollution) Act 1977 | No. 1 of 1977 | `local-government-water-pollution-act-1977/` | 2 | 2021-10-14 to 2024-08-28 | 38 |
| Protection of Employment Act 1977 | No. 7 of 1977 | `protection-of-employment-act-1977/` | 3 | 2018-01-18 to 2024-07-01 | 26 |
| Unfair Dismissals Act 1977 | No. 10 of 1977 | `unfair-dismissals-act-1977/` | 6 | 2017-09-01 to 2023-07-03 | 28 |
| Misuse of Drugs Act 1977 | No. 12 of 1977 | `misuse-of-drugs-act-1977/` | 19 | 2018-05-25 to 2026-07-29 | 48 |
| Ministers and Secretaries (Amendment) (No. 2) Act 1977 | No. 28 of 1977 | `ministers-and-secretaries-amendment-no-2-act-1977/` | 7 | 2025-02-21 to 2026-07-29 | 8 |
| Road Transport Act 1978 | No. 8 of 1978 | `road-transport-act-1978/` | 2 | 2016-06-30 to 2019-03-17 | 12 |
| Redundancy Payments Act 1979 | No. 7 of 1979 | `redundancy-payments-act-1979/` | 1 | 2019-02-01 to 2019-02-01 | 21 |
| Housing (Miscellaneous Provisions) Act 1979 | No. 27 of 1979 | `housing-miscellaneous-provisions-act-1979/` | 8 | 2018-09-12 to 2024-12-01 | 26 |
| Landlord and Tenant (Amendment) Act 1980 | No. 10 of 1980 | `landlord-and-tenant-amendment-act-1980/` | 1 | 2019-09-20 to 2019-09-20 | 90 |
| Packaged Goods (Quantity Control) Act 1980 | No. 11 of 1980 | `packaged-goods-quantity-control-act-1980/` | 1 | 2026-07-07 to 2026-07-07 | 21 |
| Sale of Goods and Supply of Services Act 1980 | No. 16 of 1980 | `sale-of-goods-and-supply-of-services-act-1980/` | 3 | 2017-05-16 to 2022-11-29 | 60 |
| Ombudsman Act 1980 | No. 26 of 1980 | `ombudsman-act-1980/` | 1 | 2025-04-02 to 2025-04-02 | 19 |
| Criminal Law (Rape) Act 1981 | No. 10 of 1981 | `criminal-law-rape-act-1981/` | 2 | 2021-05-01 to 2024-08-31 | 15 |
| Family Law Act 1981 | No. 22 of 1981 | `family-law-act-1981/` | 2 | 2016-06-30 to 2019-05-28 | 12 |
| Transport (Tour Operators and Travel Agents) Act 1982 | No. 3 of 1982 | `transport-tour-operators-and-travel-agents-act-1982/` | 2 | 2022-03-30 to 2022-12-09 | 29 |
| Courts-Martial Appeals Act 1983 | No. 19 of 1983 | `courts-martial-appeals-act-1983/` | 3 | 2017-04-07 to 2022-07-06 | 44 |
| Criminal Justice (Community Service) Act 1983 | No. 23 of 1983 | `criminal-justice-community-service-act-1983/` | 1 | 2026-10-01 to 2026-10-01 | 17 |
| Tourist Traffic Act 1983 | No. 31 of 1983 | `tourist-traffic-act-1983/` | 3 | 2016-08-31 to 2020-09-16 | 14 |
| Road Traffic (Amendment) Act 1984 | No. 16 of 1984 | `road-traffic-amendment-act-1984/` | 2 | 2016-04-29 to 2019-05-28 | 8 |
| Protection of Employees (Employers Insolvency) Act 1984 | No. 21 of 1984 | `protection-of-employees-employers-insolvency-act-1984/` | 6 | 2015-10-01 to 2026-06-08 | 29 |
| Criminal Justice Act 1984 | No. 22 of 1984 | `criminal-justice-act-1984/` | 6 | 2017-08-28 to 2025-04-02 | 49 |
| Dentists Act 1985 | No. 9 of 1985 | `dentists-act-1985/` | 2 | 2024-08-06 to 2025-05-06 | 85 |
| Industrial Development Act 1986 | No. 9 of 1986 | `industrial-development-act-1986/` | 2 | 2019-02-01 to 2020-01-07 | 52 |
| National Archives Act 1986 | No. 11 of 1986 | `national-archives-act-1986/` | 2 | 2025-09-16 to 2025-12-01 | 28 |
| Road Transport Act 1986 | No. 16 of 1986 | `road-transport-act-1986/` | 3 | 2016-06-30 to 2020-12-22 | 24 |
| Domicile and Recognition of Foreign Divorces Act 1986 | No. 24 of 1986 | `domicile-and-recognition-of-foreign-divorces-act-1986/` | 3 | 2016-01-01 to 2022-08-01 | 7 |
| Control of Dogs Act 1986 | No. 32 of 1986 | `control-of-dogs-act-1986/` | 5 | 2018-01-31 to 2025-06-09 | 39 |
| Air Pollution Act 1987 | No. 6 of 1987 | `air-pollution-act-1987/` | 5 | 2022-09-27 to 2025-08-01 | 74 |
| Defence (Amendment) Act 1987 | No. 8 of 1987 | `defence-amendment-act-1987/` | 2 | 2016-06-30 to 2019-05-28 | 18 |
| Labour Services Act 1987 | No. 15 of 1987 | `labour-services-act-1987/` | 1 | 2013-06-05 to 2013-06-05 | 41 |
| Status of Children Act 1987 | No. 26 of 1987 | `status-of-children-act-1987/` | 3 | 2016-01-18 to 2020-05-04 | 51 |
| Science and Technology Act 1987 | No. 30 of 1987 | `science-and-technology-act-1987/` | 1 | 2019-02-01 to 2019-02-01 | 30 |
| Data Protection Act 1988 | No. 25 of 1988 | `data-protection-act-1988/` | 5 | 2018-05-25 to 2025-11-10 | 47 |
| Bankruptcy Act 1988 | No. 27 of 1988 | `bankruptcy-act-1988/` | 3 | 2018-10-01 to 2026-02-01 | 166 |
| Housing Act 1988 | No. 28 of 1988 | `housing-act-1988/` | 3 | 2018-01-31 to 2024-05-16 | 33 |
| Judicial Separation and Family Law Reform Act 1989 | No. 6 of 1989 | `judicial-separation-and-family-law-reform-act-1989/` | 3 | 2019-01-01 to 2022-08-01 | 48 |
| Building Control Act 1990 | No. 3 of 1990 | `building-control-act-1990/` | 9 | 2018-12-17 to 2026-07-27 | 36 |
| Firearms and Offensive Weapons Act 1990 | No. 12 of 1990 | `firearms-and-offensive-weapons-act-1990/` | 3 | 2018-05-25 to 2024-09-30 | 31 |
| Derelict Sites Act 1990 | No. 14 of 1990 | `derelict-sites-act-1990/` | 6 | 2018-12-19 to 2025-12-11 | 34 |
| Industrial Relations Act 1990 | No. 19 of 1990 | `industrial-relations-act-1990/` | 6 | 2017-12-20 to 2026-06-29 | 64 |
| Health (Nursing Homes) Act 1990 | No. 23 of 1990 | `health-nursing-homes-act-1990/` | 1 | 2025-07-23 to 2025-07-23 | 29 |
| Criminal Law (Rape) (Amendment) Act 1990 | No. 32 of 1990 | `criminal-law-rape-amendment-act-1990/` | 1 | 2022-02-15 to 2022-02-15 | 24 |
| Child Abduction and Enforcement of Custody Orders Act 1991 | No. 6 of 1991 | `child-abduction-and-enforcement-of-custody-orders-act-1991/` | 3 | 2017-04-07 to 2022-08-01 | 47 |
| Child Care Act 1991 | No. 17 of 1991 | `child-care-act-1991/` | 13 | 2019-01-01 to 2026-07-21 | 164 |
| Statute of Limitations (Amendment) Act 1991 | No. 18 of 1991 | `statute-of-limitations-amendment-act-1991/` | 3 | 2016-06-30 to 2023-09-27 | 10 |
| Payment of Wages Act 1991 | No. 25 of 1991 | `payment-of-wages-act-1991/` | 3 | 2017-09-01 to 2022-12-01 | 22 |
| Sea Pollution Act 1991 | No. 27 of 1991 | `sea-pollution-act-1991/` | 6 | 2017-09-01 to 2025-09-16 | 51 |
| Liability for Defective Products Act 1991 | No. 28 of 1991 | `liability-for-defective-products-act-1991/` | 2 | 2016-06-30 to 2019-05-28 | 16 |
| Criminal Damage Act 1991 | No. 31 of 1991 | `criminal-damage-act-1991/` | 2 | 2019-01-01 to 2024-12-31 | 18 |
| Merchant Shipping Act 1992 | No. 2 of 1992 | `merchant-shipping-act-1992/` | 3 | 2021-09-07 to 2025-06-01 | 40 |
| Environmental Protection Agency Act 1992 | No. 7 of 1992 | `environmental-protection-agency-act-1992/` | 7 | 2020-09-30 to 2026-05-08 | 156 |
| Criminal Evidence Act 1992 | No. 12 of 1992 | `criminal-evidence-act-1992/` | 5 | 2019-01-01 to 2024-09-02 | 37 |
| Regional Technical Colleges Act 1992 | No. 16 of 1992 | `regional-technical-colleges-act-1992/` | 3 | 2018-04-24 to 2022-11-10 | 40 |
| Foreshore (Amendment) Act 1992 | No. 17 of 1992 | `foreshore-amendment-act-1992/` | 4 | 2017-04-13 to 2024-05-14 | 12 |
| Housing (Miscellaneous Provisions) Act 1992 | No. 18 of 1992 | `housing-miscellaneous-provisions-act-1992/` | 7 | 2018-09-12 to 2026-04-01 | 43 |
| Criminal Justice Act 1993 | No. 6 of 1993 | `criminal-justice-act-1993/` | 2 | 2022-01-01 to 2023-08-01 | 17 |
| Comptroller and Auditor General (Amendment) Act 1993 | No. 8 of 1993 | `comptroller-and-auditor-general-amendment-act-1993/` | 1 | 2025-12-10 to 2025-12-10 | 32 |
| Interception of Postal Packets and Telecommunications Messages (Regulation) Act 1993 | No. 10 of 1993 | `interception-of-postal-packets-and-telecommunications-messages-regulation-act-1993/` | 1 | 2025-04-02 to 2025-04-02 | 17 |
| Roads Act 1993 | No. 14 of 1993 | `roads-act-1993/` | 12 | 2018-10-16 to 2026-05-13 | 111 |
| Criminal Law (Sexual Offences) Act 1993 | No. 20 of 1993 | `criminal-law-sexual-offences-act-1993/` | 3 | 2017-06-30 to 2022-12-22 | 18 |
| Irish Aviation Authority Act 1993 | No. 29 of 1993 | `irish-aviation-authority-act-1993/` | 8 | 2020-05-29 to 2025-08-07 | 106 |
| Criminal Procedure Act 1993 | No. 40 of 1993 | `criminal-procedure-act-1993/` | 2 | 2020-02-17 to 2023-08-01 | 16 |
| Criminal Justice (Public Order) Act 1994 | No. 2 of 1994 | `criminal-justice-public-order-act-1994/` | 4 | 2017-08-14 to 2024-12-31 | 47 |
| Terms of Employment (Information) Act 1994 | No. 5 of 1994 | `terms-of-employment-information-act-1994/` | 4 | 2017-09-01 to 2022-12-16 | 26 |
| Road Traffic Act 1994 | No. 7 of 1994 | `road-traffic-act-1994/` | 13 | 2018-12-22 to 2026-09-02 | 53 |
| Irish Nationality and Citizenship Act 1994 | No. 9 of 1994 | `irish-nationality-and-citizenship-act-1994/` | 1 | 2021-09-01 to 2021-09-01 | 4 |
| Referendum Act 1994 | No. 12 of 1994 | `referendum-act-1994/` | 1 | 2025-10-01 to 2025-10-01 | 62 |
| Criminal Justice Act 1994 | No. 15 of 1994 | `criminal-justice-act-1994/` | 1 | 2026-07-31 to 2026-07-31 | 85 |
| Health Insurance Act 1994 | No. 16 of 1994 | `health-insurance-act-1994/` | 10 | 2022-09-29 to 2026-04-01 | 73 |
| Irish Horseracing Industry 1994 | No. 18 of 1994 | `irish-horseracing-industry-1994/` | 2 | 2023-10-31 to 2026-02-05 | 91 |
| Investment Limited Partnerships Act 1994 | No. 24 of 1994 | `investment-limited-partnerships-act-1994/` | 1 | 2022-12-07 to 2022-12-07 | 77 |
| Maintenance Act 1994 | No. 28 of 1994 | `maintenance-act-1994/` | 2 | 2016-06-30 to 2019-05-28 | 28 |
| Maternity Protection Act 1994 | No. 34 of 1994 | `maternity-protection-act-1994/` | 7 | 2017-12-23 to 2024-11-20 | 54 |
| Adoptive Leave Act 1995 | No. 2 of 1995 | `adoptive-leave-act-1995/` | 6 | 2016-08-01 to 2023-07-03 | 51 |
| Occupiers' Liability Act 1995 | No. 10 of 1995 | `occupiers-liability-act-1995/` | 1 | 2024-07-23 to 2024-07-23 | 11 |
| Tourist Traffic Act 1995 | No. 13 of 1995 | `tourist-traffic-act-1995/` | 3 | 2016-08-31 to 2020-09-16 | 12 |
| Package Holidays and Travel Trade Act 1995 | No. 17 of 1995 | `package-holidays-and-travel-trade-act-1995/` | 2 | 2021-05-26 to 2022-11-29 | 48 |
| Casual Trading Act 1995 | No. 19 of 1995 | `casual-trading-act-1995/` | 1 | 2022-12-15 to 2022-12-15 | 21 |
| Ethics in Public Office Act 1995 | No. 22 of 1995 | `ethics-in-public-office-act-1995/` | 3 | 2018-11-21 to 2026-01-01 | 41 |
| Consumer Credit Act 1995 | No. 24 of 1995 | `consumer-credit-act-1995/` | 4 | 2018-05-25 to 2026-02-05 | 217 |
| Family Law Act 1995 | No. 26 of 1995 | `family-law-act-1995/` | 2 | 2019-01-01 to 2022-08-01 | 58 |
| Irish Medicines Board Act 1995 | No. 29 of 1995 | `irish-medicines-board-act-1995/` | 9 | 2023-09-14 to 2026-06-30 | 51 |
| Civil Legal Aid Act 1995 | No. 32 of 1995 | `civil-legal-aid-act-1995/` | 3 | 2025-06-19 to 2026-06-24 | 48 |
| Domestic Violence Act 1996 | No. 1 of 1996 | `domestic-violence-act-1996/` | 1 | 2016-06-30 to 2016-06-30 | 28 |
| Waste Management Act 1996 | No. 10 of 1996 | `waste-management-act-1996/` | 17 | 2018-04-12 to 2026-05-08 | 120 |
| Dumping at Sea Act 1996 | No. 14 of 1996 | `dumping-at-sea-act-1996/` | 5 | 2016-07-22 to 2025-08-01 | 20 |
| Protection of Young Persons (Employment) Act 1996 | No. 16 of 1996 | `protection-of-young-persons-employment-act-1996/` | 3 | 2018-06-30 to 2022-07-27 | 32 |
| Refugee Act 1996 | No. 17 of 1996 | `refugee-act-1996/` | 1 | 2015-04-20 to 2015-04-20 | 41 |
| Transnational Information and Consultation of Employees Act 1996 | No. 20 of 1996 | `transnational-information-and-consultation-of-employees-act-1996/` | 1 | 2018-01-18 to 2018-01-18 | 31 |
| Metrology Act 1996 | No. 27 of 1996 | `metrology-act-1996/` | 2 | 2026-02-24 to 2026-07-07 | 38 |
| National Standards Authority of Ireland Act 1996 | No. 28 of 1996 | `national-standards-authority-of-ireland-act-1996/` | 2 | 2026-07-07 to 2026-07-22 | 41 |
| Criminal Justice (Drug Trafficking) Act 1996 | No. 29 of 1996 | `criminal-justice-drug-trafficking-act-1996/` | 1 | 2025-08-01 to 2025-08-01 | 13 |
| Proceeds of Crime Act 1996 | No. 30 of 1996 | `proceeds-of-crime-act-1996/` | 2 | 2018-07-30 to 2021-07-28 | 25 |
| Criminal Assets Bureau Act 1996 | No. 31 of 1996 | `criminal-assets-bureau-act-1996/` | 3 | 2016-06-30 to 2023-04-10 | 30 |
| Family Law (Divorce) Act 1996 | No. 33 of 1996 | `family-law-divorce-act-1996/` | 3 | 2019-01-01 to 2022-08-01 | 54 |
| Telecommunications (Miscellaneous Provisions) Act 1996 | No. 34 of 1996 | `telecommunications-miscellaneous-provisions-act-1996/` | 3 | 2016-06-29 to 2025-06-01 | 21 |
| Sexual Offences (Jurisdiction) Act 1996 | No. 38 of 1996 | `sexual-offences-jurisdiction-act-1996/` | 2 | 2024-01-01 to 2024-08-31 | 13 |
| Health Insurance Act, 1994 (Registration) Regulations 1996 | S.I. No. 80 of 1996 | `health-insurance-act-1994-registration-regulations-1996/` | 1 | 2024-07-01 to 2024-07-01 | 8 |
| Health Insurance Act, 1994 (Minimum Benefit) Regulations 1996 | S.I. No. 83 of 1996 | `health-insurance-act-1994-minimum-benefit-regulations-1996/` | 1 | 2024-07-01 to 2024-07-01 | 16 |
| Social Welfare (Social Welfare Tribunal) Regulations 1996 | S.I. No. 262 of 1996 | `social-welfare-social-welfare-tribunal-regulations-1996/` | 1 | 2023-05-04 to 2023-05-04 | 22 |
| Social Welfare (Consolidated Contributions and Insurability) Regulations 1996 | S.I. No. 312 of 1996 | `social-welfare-consolidated-contributions-and-insurability-regulations-1996/` | 4 | 2021-11-19 to 2026-01-01 | 130 |
| European Parliament Elections Act 1997 | No. 2 of 1997 | `european-parliament-elections-act-1997/` | 1 | 2025-10-01 to 2025-10-01 | 34 |
| Central Bank Act 1997 | No. 8 of 1997 | `central-bank-act-1997/` | 5 | 2021-06-01 to 2026-08-01 | 126 |
| Litter Pollution Act 1997 | No. 12 of 1997 | `litter-pollution-act-1997/` | 5 | 2022-04-27 to 2026-05-08 | 40 |
| Freedom of Information Act 1997 | No. 13 of 1997 | `freedom-of-information-act-1997/` | 1 | 2014-03-18 to 2014-03-18 | 52 |
| Criminal Law Act 1997 | No. 14 of 1997 | `criminal-law-act-1997/` | 3 | 2016-06-30 to 2021-12-31 | 21 |
| Credit Union Act 1997 | No. 15 of 1997 | `credit-union-act-1997/` | 9 | 2018-09-21 to 2025-09-30 | 241 |
| Bail Act 1997 | No. 16 of 1997 | `bail-act-1997/` | 8 | 2019-01-01 to 2026-06-12 | 24 |
| Organisation of Working Time Act 1997 | No. 20 of 1997 | `organisation-of-working-time-act-1997/` | 7 | 2017-09-01 to 2025-01-20 | 49 |
| Housing (Miscellaneous Provisions) Act 1997 | No. 21 of 1997 | `housing-miscellaneous-provisions-act-1997/` | 3 | 2018-09-12 to 2024-10-17 | 28 |
| Fisheries (Amendment) Act 1997 | No. 23 of 1997 | `fisheries-amendment-act-1997/` | 4 | 2018-07-04 to 2025-02-03 | 94 |
| Universities Act 1997 | No. 24 of 1997 | `universities-act-1997/` | 3 | 2022-11-15 to 2024-02-21 | 69 |
| Non-Fatal Offences Against the Person Act 1997 | No. 26 of 1997 | `non-fatal-offences-against-the-person-act-1997/` | 6 | 2017-05-17 to 2024-12-31 | 46 |
| Road Traffic (Traffic and Parking) Regulations 1997 | S.I. No. 182 of 1997 | `road-traffic-traffic-and-parking-regulations-1997/` | 3 | 2024-05-20 to 2026-05-13 | 66 |
| Building Control Regulations 1997 | S.I. No. 496 of 1997 | `building-control-regulations-1997/` | 6 | 2020-04-03 to 2026-07-27 | 59 |
| Building Regulations 1997 | S.I. No. 497 of 1997 | `building-regulations-1997/` | 1 | 2026-02-19 to 2026-02-19 | 19 |
| Employment Equality Act 1998 | No. 21 of 1998 | `employment-equality-act-1998/` | 9 | 2018-07-18 to 2025-05-31 | 117 |
| Child Trafficking and Pornography Act 1998 | No. 22 of 1998 | `child-trafficking-and-pornography-act-1998/` | 2 | 2017-06-30 to 2020-05-21 | 17 |
| Parental Leave Act 1998 | No. 30 of 1998 | `parental-leave-act-1998/` | 6 | 2016-01-18 to 2024-03-06 | 42 |
| Housing (Traveller Accommodation) Act 1998 | No. 33 of 1998 | `housing-traveller-accommodation-act-1998/` | 2 | 2018-09-12 to 2024-05-16 | 37 |
| Industrial Development (Enterprise Ireland) Act 1998 | No. 34 of 1998 | `industrial-development-enterprise-ireland-act-1998/` | 2 | 2019-02-01 to 2020-01-07 | 58 |
| Protections for Persons Reporting Child Abuse Act 1998 | No. 49 of 1998 | `protections-for-persons-reporting-child-abuse-act-1998/` | 2 | 2015-10-01 to 2019-02-01 | 8 |
| Education Act 1998 | No. 51 of 1998 | `education-act-1998/` | 6 | 2018-10-03 to 2023-12-12 | 80 |
| Fisheries and Foreshore (Amendment) Act 1998 | No. 54 of 1998 | `fisheries-and-foreshore-amendment-act-1998/` | 1 | 2019-01-01 to 2019-01-01 | 8 |
| Social Welfare (Rent Allowance) Regulations 1998 | S.I. No. 188 of 1998 | `social-welfare-rent-allowance-regulations-1998/` | 1 | 2026-01-21 to 2026-01-21 | 24 |
| Road Transport Act 1999 | No. 15 of 1999 | `road-transport-act-1999/` | 2 | 2016-06-30 to 2019-05-28 | 27 |
| Sea Pollution (Amendment) Act 1999 | No. 18 of 1999 | `sea-pollution-amendment-act-1999/` | 2 | 2019-01-01 to 2021-11-22 | 20 |
| Immigration Act 1999 | No. 22 of 1999 | `immigration-act-1999/` | 2 | 2023-07-31 to 2026-06-12 | 17 |
| Electricity Regulation Act 1999 | No. 23 of 1999 | `electricity-regulation-act-1999/` | 17 | 2018-12-31 to 2025-12-31 | 171 |
| Comhairle Act 2000 | No. 1 of 2000 | `comhairle-act-2000/` | 1 | 2019-02-01 to 2019-02-01 | 43 |
| National Minimum Wage Act 2000 | No. 5 of 2000 | `national-minimum-wage-act-2000/` | 11 | 2019-01-01 to 2026-01-01 | 59 |
| Equal Status Act 2000 | No. 8 of 2000 | `equal-status-act-2000/` | 4 | 2018-10-03 to 2021-07-29 | 55 |
| Firearms (Firearm Certificates For Non-Residents) Act 2000 | No. 20 of 2000 | `firearms-firearm-certificates-for-non-residents-act-2000/` | 3 | 2016-01-01 to 2022-05-04 | 9 |
| Education (Welfare) Act 2000 | No. 22 of 2000 | `education-welfare-act-2000/` | 2 | 2023-04-05 to 2025-02-19 | 43 |
| Electronic Commerce Act 2000 | No. 27 of 2000 | `electronic-commerce-act-2000/` | 1 | 2025-06-01 to 2025-06-01 | 37 |
| Copyright and Related Rights Act 2000 | No. 28 of 2000 | `copyright-and-related-rights-act-2000/` | 1 | 2026-09-09 to 2026-09-09 | 422 |
| Illegal Immigrants (Trafficking) Act 2000 | No. 29 of 2000 | `illegal-immigrants-trafficking-act-2000/` | 2 | 2024-05-14 to 2026-06-12 | 14 |
| Planning and Development Act 2000 | No. 30 of 2000 | `planning-and-development-act-2000/` | 33 | 2019-01-01 to 2026-08-12 | 538 |
| Protection of Children (Hague Convention) Act 2000 | No. 37 of 2000 | `protection-of-children-hague-convention-act-2000/` | 4 | 2016-01-18 to 2022-08-01 | 21 |
| Wildlife (Amendment) Act 2000 | No. 38 of 2000 | `wildlife-amendment-act-2000/` | 1 | 2024-06-01 to 2024-06-01 | 90 |
| National Treasury Management Agency (Amendment) Act 2000 | No. 39 of 2000 | `national-treasury-management-agency-amendment-act-2000/` | 7 | 2020-08-01 to 2025-11-26 | 39 |
| National Training Fund Act 2000 | No. 41 of 2000 | `national-training-fund-act-2000/` | 4 | 2019-01-01 to 2026-01-19 | 13 |
| Aviation Regulation Act 2001 | No. 1 of 2001 | `aviation-regulation-act-2001/` | 7 | 2019-03-11 to 2023-05-01 | 59 |
| Teaching Council Act 2001 | No. 8 of 2001 | `teaching-council-act-2001/` | 8 | 2016-11-08 to 2026-02-09 | 74 |
| Industrial Relations (Amendment) Act 2001 | No. 11 of 2001 | `industrial-relations-amendment-act-2001/` | 2 | 2019-01-01 to 2020-02-01 | 19 |
| Valuation Act 2001 | No. 13 of 2001 | `valuation-act-2001/` | 17 | 2018-11-09 to 2024-10-18 | 92 |
| Health Insurance (Amendment) Act 2001 | No. 17 of 2001 | `health-insurance-amendment-act-2001/` | 1 | 2023-03-21 to 2023-03-21 | 16 |
| Sex Offenders Act 2001 | No. 18 of 2001 | `sex-offenders-act-2001/` | 2 | 2022-01-01 to 2023-11-13 | 62 |
| Carer's Leave Act 2001 | No. 19 of 2001 | `carer-s-leave-act-2001/` | 2 | 2018-09-04 to 2020-10-14 | 35 |
| Children Act 2001 | No. 24 of 2001 | `children-act-2001/` | 6 | 2017-11-27 to 2026-08-10 | 302 |
| Mental Health Act 2001 | No. 25 of 2001 | `mental-health-act-2001/` | 5 | 2019-01-01 to 2026-06-23 | 80 |
| Prevention of Corruption (Amendment) Act 2001 | No. 27 of 2001 | `prevention-of-corruption-amendment-act-2001/` | 1 | 2018-07-30 to 2018-07-30 | 17 |
| Agriculture Appeals Act 2001 | No. 29 of 2001 | `agriculture-appeals-act-2001/` | 2 | 2025-07-17 to 2025-11-27 | 32 |
| Standards in Public Office Act 2001 | No. 31 of 2001 | `standards-in-public-office-act-2001/` | 4 | 2017-04-13 to 2025-01-01 | 32 |
| Local Government Act 2001 | No. 37 of 2001 | `local-government-act-2001/` | 13 | 2018-12-26 to 2025-12-31 | 329 |
| Youth Work Act 2001 | No. 42 of 2001 | `youth-work-act-2001/` | 3 | 2017-05-16 to 2025-05-01 | 39 |
| Protection of Employees (Part-Time Work) Act 2001 | No. 45 of 2001 | `protection-of-employees-part-time-work-act-2001/` | 2 | 2017-09-01 to 2020-10-14 | 23 |
| Criminal Justice (Theft and Fraud Offences) Act 2001 | No. 50 of 2001 | `criminal-justice-theft-and-fraud-offences-act-2001/` | 6 | 2018-07-30 to 2026-08-10 | 79 |
| Transport (Railway Infrastructure) Act 2001 | No. 55 of 2001 | `transport-railway-infrastructure-act-2001/` | 1 | 2026-06-03 to 2026-06-03 | 96 |
| Sustainable Energy Act 2002 | No. 2 of 2002 | `sustainable-energy-act-2002/` | 1 | 2024-05-01 to 2024-05-01 | 35 |
| Public Health (Tobacco) Act 2002 | No. 6 of 2002 | `public-health-tobacco-act-2002/` | 4 | 2024-09-23 to 2026-07-20 | 60 |
| Housing (Miscellaneous Provisions) Act 2002 | No. 9 of 2002 | `housing-miscellaneous-provisions-act-2002/` | 1 | 2018-09-12 to 2018-09-12 | 28 |
| Gas (Interim) (Regulation) Act 2002 | No. 10 of 2002 | `gas-interim-regulation-act-2002/` | 2 | 2023-06-06 to 2024-06-01 | 32 |
| Road Traffic Act 2002 | No. 12 of 2002 | `road-traffic-act-2002/` | 3 | 2018-10-26 to 2025-03-31 | 30 |
| Competition Act 2002 | No. 14 of 2002 | `competition-act-2002/` | 6 | 2019-01-01 to 2026-07-01 | 147 |
| Courts and Court Officers Act 2002 | No. 15 of 2002 | `courts-and-court-officers-act-2002/` | 1 | 2026-10-01 to 2026-10-01 | 49 |
| Communications Regulation Act 2002 | No. 20 of 2002 | `communications-regulation-act-2002/` | 9 | 2017-03-21 to 2026-07-31 | 108 |
| Ombudsman for Children Act 2002 | No. 22 of 2002 | `ombudsman-for-children-act-2002/` | 1 | 2018-12-26 to 2018-12-26 | 24 |
| Unclaimed Life Assurance Policies Act 2003 | No. 2 of 2003 | `unclaimed-life-assurance-policies-act-2003/` | 1 | 2021-10-30 to 2021-10-30 | 30 |
| Social Welfare (Miscellaneous Provisions) Act 2003 | No. 4 of 2003 | `social-welfare-miscellaneous-provisions-act-2003/` | 1 | 2024-07-01 to 2024-07-01 | 26 |
| Employment Permits Act 2003 | No. 7 of 2003 | `employment-permits-act-2003/` | 2 | 2018-06-30 to 2024-09-02 | 10 |
| National Tourism Development Authority Act 2003 | No. 10 of 2003 | `national-tourism-development-authority-act-2003/` | 4 | 2017-09-26 to 2025-06-01 | 45 |
| Central Bank and Financial Services Authority of Ireland Act 2003 | No. 12 of 2003 | `central-bank-and-financial-services-authority-of-ireland-act-2003/` | 1 | 2025-05-20 to 2025-05-20 | 40 |
| Licensing of Indoor Events Act 2003 | No. 15 of 2003 | `licensing-of-indoor-events-act-2003/` | 1 | 2021-09-28 to 2021-09-28 | 35 |
| Criminal Justice (Public Order) Act 2003 | No. 16 of 2003 | `criminal-justice-public-order-act-2003/` | 1 | 2024-12-31 to 2024-12-31 | 11 |
| Criminal Justice (Illicit Traffic by Sea) Act 2003 | No. 18 of 2003 | `criminal-justice-illicit-traffic-by-sea-act-2003/` | 2 | 2021-01-01 to 2021-11-22 | 31 |
| European Convention on Human Rights Act 2003 | No. 20 of 2003 | `european-convention-on-human-rights-act-2003/` | 1 | 2020-10-14 to 2020-10-14 | 17 |
| Fisheries (Amendment) Act 2003 | No. 21 of 2003 | `fisheries-amendment-act-2003/` | 1 | 2024-05-14 to 2024-05-14 | 37 |
| Digital Hub Development Agency Act 2003 | No. 23 of 2003 | `digital-hub-development-agency-act-2003/` | 3 | 2021-09-28 to 2025-06-01 | 47 |
| Immigration Act 2003 | No. 26 of 2003 | `immigration-act-2003/` | 4 | 2017-05-17 to 2026-06-12 | 14 |
| Protection of Employees (Fixed-Term Work) Act 2003 | No. 29 of 2003 | `protection-of-employees-fixed-term-work-act-2003/` | 3 | 2017-09-01 to 2022-12-16 | 21 |
| Industrial Development (Science Foundation Ireland) Act 2003 | No. 30 of 2003 | `industrial-development-science-foundation-ireland-act-2003/` | 2 | 2021-09-15 to 2024-08-01 | 40 |
| Intoxicating Liquor Act 2003 | No. 31 of 2003 | `intoxicating-liquor-act-2003/` | 4 | 2023-12-08 to 2025-12-17 | 26 |
| Official Languages Act 2003 | No. 32 of 2003 | `official-languages-act-2003/` | 8 | 2022-02-28 to 2026-07-15 | 61 |
| Minister for Community, Rural and Gaeltacht Affairs (Powers and Functions) Act 2003 | No. 39 of 2003 | `minister-for-community-rural-and-gaeltacht-affairs-powers-and-functions-act-2003/` | 1 | 2025-05-20 to 2025-05-20 | 7 |
| European Arrest Warrant Act 2003 | No. 45 of 2003 | `european-arrest-warrant-act-2003/` | 6 | 2019-12-12 to 2024-07-23 | 65 |
| Personal Injuries Assessment Board Act 2003 | No. 46 of 2003 | `personal-injuries-assessment-board-act-2003/` | 10 | 2018-05-25 to 2025-12-01 | 102 |
| Immigration Act 2004 | No. 1 of 2004 | `immigration-act-2004/` | 18 | 2018-01-31 to 2026-06-15 | 28 |
| Civil Registration Act 2004 | No. 3 of 2004 | `civil-registration-act-2004/` | 13 | 2019-01-01 to 2025-12-31 | 134 |
| Industrial Relations (Miscellaneous Provisions) Act 2004 | No. 4 of 2004 | `industrial-relations-miscellaneous-provisions-act-2004/` | 2 | 2019-01-01 to 2020-02-01 | 18 |
| Public Service Superannuation (Miscellaneous Provisions) Act 2004 | No. 7 of 2004 | `public-service-superannuation-miscellaneous-provisions-act-2004/` | 5 | 2018-03-07 to 2025-04-02 | 22 |
| Aer Lingus Act 2004 | No. 10 of 2004 | `aer-lingus-act-2004/` | 1 | 2020-10-01 to 2020-10-01 | 16 |
| Air Navigation and Transport (International Conventions) Act 2004 | No. 11 of 2004 | `air-navigation-and-transport-international-conventions-act-2004/` | 1 | 2020-10-01 to 2020-10-01 | 18 |
| Private Security Services Act 2004 | No. 12 of 2004 | `private-security-services-act-2004/` | 9 | 2018-09-01 to 2025-10-31 | 57 |
| Electoral (Amendment) Act 2004 | No. 15 of 2004 | `electoral-amendment-act-2004/` | 2 | 2020-07-08 to 2024-03-31 | 41 |
| Criminal Justice (Joint Investigation Teams) Act 2004 | No. 20 of 2004 | `criminal-justice-joint-investigation-teams-act-2004/` | 2 | 2020-06-27 to 2023-11-01 | 19 |
| Commissions of Investigation Act 2004 | No. 23 of 2004 | `commissions-of-investigation-act-2004/` | 3 | 2018-05-25 to 2025-07-22 | 52 |
| Residential Tenancies Act 2004 | No. 27 of 2004 | `residential-tenancies-act-2004/` | 27 | 2018-07-23 to 2026-09-25 | 273 |
| Maritime Security Act 2004 | No. 29 of 2004 | `maritime-security-act-2004/` | 3 | 2020-10-14 to 2021-11-22 | 17 |
| Education for Persons with Special Educational Needs Act 2004 | No. 30 of 2004 | `education-for-persons-with-special-educational-needs-act-2004/` | 4 | 2017-10-02 to 2023-03-01 | 56 |
| Civil Liability and Courts Act 2004 | No. 31 of 2004 | `civil-liability-and-courts-act-2004/` | 4 | 2019-01-28 to 2024-09-02 | 65 |
| State Airports Act 2004 | No. 32 of 2004 | `state-airports-act-2004/` | 1 | 2021-08-25 to 2021-08-25 | 31 |
| Public Service Management (Recruitment and Appointments) Act 2004 | No. 33 of 2004 | `public-service-management-recruitment-and-appointments-act-2004/` | 3 | 2019-09-10 to 2023-09-04 | 78 |
| Ombudsman (Defence Forces) Act 2004 | No. 36 of 2004 | `ombudsman-defence-forces-act-2004/` | 4 | 2017-05-16 to 2024-07-17 | 20 |
| Health Act 2004 | No. 42 of 2004 | `health-act-2004/` | 2 | 2021-08-04 to 2023-03-01 | 162 |
| Road Traffic Act 2004 | No. 44 of 2004 | `road-traffic-act-2004/` | 6 | 2017-06-01 to 2025-02-07 | 44 |
| Proceeds of Crime (Amendment) Act 2005 | No. 1 of 2005 | `proceeds-of-crime-amendment-act-2005/` | 1 | 2018-07-30 to 2018-07-30 | 24 |
| Criminal Justice (Terrorist Offences) Act 2005 | No. 2 of 2005 | `criminal-justice-terrorist-offences-act-2005/` | 37 | 2018-12-20 to 2026-07-08 | 97 |
| Social Welfare and Pensions Act 2005 | No. 4 of 2005 | `social-welfare-and-pensions-act-2005/` | 2 | 2017-04-12 to 2023-01-09 | 45 |
| Sea Pollution (Hazardous Substances) (Compensation) Act 2005 | No. 9 of 2005 | `sea-pollution-hazardous-substances-compensation-act-2005/` | 2 | 2019-01-01 to 2021-11-22 | 32 |
| Safety, Health and Welfare at Work Act 2005 | No. 10 of 2005 | `safety-health-and-welfare-at-work-act-2005/` | 12 | 2018-07-12 to 2026-04-09 | 108 |
| Maritime Safety Act 2005 | No. 11 of 2005 | `maritime-safety-act-2005/` | 7 | 2016-12-01 to 2025-07-29 | 62 |
| Investment Funds, Companies and Miscellaneous Provisions Act 2005 | No. 12 of 2005 | `investment-funds-companies-and-miscellaneous-provisions-act-2005/` | 4 | 2016-10-13 to 2021-03-01 | 110 |
| Disability Act 2005 | No. 14 of 2005 | `disability-act-2005/` | 6 | 2018-05-25 to 2025-04-02 | 60 |
| International Interests in Mobile Equipment (Cape Town Convention) Act 2005 | No. 15 of 2005 | `international-interests-in-mobile-equipment-cape-town-convention-act-2005/` | 3 | 2017-05-02 to 2023-01-09 | 19 |
| Commission to Inquire into Child Abuse (Amendment) Act 2005 | No. 17 of 2005 | `commission-to-inquire-into-child-abuse-amendment-act-2005/` | 2 | 2016-12-15 to 2019-05-28 | 37 |
| Civil Service Regulation (Amendment) Act 2005 | No. 18 of 2005 | `civil-service-regulation-amendment-act-2005/` | 2 | 2017-03-31 to 2020-05-29 | 35 |
| Garda Síochána Act 2005 | No. 20 of 2005 | `garda-s-och-na-act-2005/` | 11 | 2018-02-06 to 2024-09-03 | 177 |
| Grangegorman Development Agency Act 2005 | No. 21 of 2005 | `grangegorman-development-agency-act-2005/` | 3 | 2016-10-26 to 2020-10-21 | 48 |
| Veterinary Practice Act 2005 | No. 22 of 2005 | `veterinary-practice-act-2005/` | 5 | 2017-06-27 to 2026-01-01 | 151 |
| Social Welfare Consolidation Act 2005 | No. 26 of 2005 | `social-welfare-consolidation-act-2005/` | 2 | 2026-01-21 to 2026-10-01 | 549 |
| Health and Social Care Professionals Act 2005 | No. 27 of 2005 | `health-and-social-care-professionals-act-2005/` | 25 | 2019-01-30 to 2026-05-28 | 131 |
| Transfer of Execution of Sentences Act 2005 | No. 28 of 2005 | `transfer-of-execution-of-sentences-act-2005/` | 3 | 2017-04-07 to 2023-05-03 | 21 |
| Railway Safety Act 2005 | No. 31 of 2005 | `railway-safety-act-2005/` | 10 | 2018-05-25 to 2026-07-01 | 154 |
| Development Banks Act 2005 | No. 34 of 2005 | `development-banks-act-2005/` | 3 | 2017-03-15 to 2023-01-09 | 11 |
| Social Welfare Law Reform and Pensions Act 2006 | No. 5 of 2006 | `social-welfare-law-reform-and-pensions-act-2006/` | 1 | 2018-01-01 to 2018-01-01 | 58 |
| Sea-Fisheries and Maritime Jurisdiction Act 2006 | No. 8 of 2006 | `sea-fisheries-and-maritime-jurisdiction-act-2006/` | 23 | 2018-10-24 to 2025-12-19 | 131 |
| Employees (Provision of Information and Consultation) Act 2006 | No. 9 of 2006 | `employees-provision-of-information-and-consultation-act-2006/` | 2 | 2015-10-01 to 2019-02-01 | 26 |
| Criminal Law (Insanity) Act 2006 | No. 11 of 2006 | `criminal-law-insanity-act-2006/` | 3 | 2017-04-13 to 2023-11-01 | 32 |
| Registration of Deeds and Title Act 2006 | No. 12 of 2006 | `registration-of-deeds-and-title-act-2006/` | 5 | 2018-01-01 to 2023-07-31 | 80 |
| Parental Leave (Amendment) Act 2006 | No. 13 of 2006 | `parental-leave-amendment-act-2006/` | 2 | 2016-06-30 to 2019-07-19 | 14 |
| Road Safety Authority Act 2006 | No. 14 of 2006 | `road-safety-authority-act-2006/` | 2 | 2015-09-30 to 2019-02-01 | 41 |
| Criminal Law (Sexual Offences) Act 2006 | No. 15 of 2006 | `criminal-law-sexual-offences-act-2006/` | 4 | 2017-03-27 to 2024-08-31 | 12 |
| Employment Permits Act 2006 | No. 16 of 2006 | `employment-permits-act-2006/` | 15 | 2018-12-13 to 2024-09-02 | 57 |
| Health (Repayment Scheme) Act 2006 | No. 17 of 2006 | `health-repayment-scheme-act-2006/` | 1 | 2018-05-25 to 2018-05-25 | 24 |
| NATIONAL SPORTS CAMPUS DEVELOPMENT AUTHORITY ACT 2006 | No. 19 of 2006 | `national-sports-campus-development-authority-act-2006/` | 1 | 2014-10-14 to 2014-10-14 | 42 |
| Defence (Amendment) Act 2006 | No. 20 of 2006 | `defence-amendment-act-2006/` | 1 | 2022-04-04 to 2022-04-04 | 17 |
| National Economic and Social Development Office Act 2006 | No. 21 of 2006 | `national-economic-and-social-development-office-act-2006/` | 3 | 2017-05-16 to 2023-01-09 | 43 |
| Road Traffic Act 2006 | No. 23 of 2006 | `road-traffic-act-2006/` | 8 | 2018-07-19 to 2026-07-01 | 24 |
| Criminal Justice Act 2006 | No. 26 of 2006 | `criminal-justice-act-2006/` | 7 | 2017-04-07 to 2026-08-10 | 208 |
| Road Traffic and Transport Act 2006 | No. 28 of 2006 | `road-traffic-and-transport-act-2006/` | 3 | 2018-10-04 to 2025-11-10 | 4 |
| Sea Pollution (Miscellaneous Provisions) Act 2006 | No. 29 of 2006 | `sea-pollution-miscellaneous-provisions-act-2006/` | 2 | 2017-04-13 to 2021-11-22 | 40 |
| International Criminal Court Act 2006 | No. 30 of 2006 | `international-criminal-court-act-2006/` | 3 | 2017-04-07 to 2026-09-01 | 74 |
| Electoral (Amendment) Act 2006 | No. 33 of 2006 | `electoral-amendment-act-2006/` | 3 | 2018-05-25 to 2024-05-16 | 21 |
| Energy (Miscellaneous Provisions) Act 2006 | No. 40 of 2006 | `energy-miscellaneous-provisions-act-2006/` | 2 | 2017-07-26 to 2023-01-09 | 32 |
| Investment Funds, Companies and Miscellaneous Provisions Act 2006 | No. 41 of 2006 | `investment-funds-companies-and-miscellaneous-provisions-act-2006/` | 1 | 2019-01-01 to 2019-01-01 | 36 |
| Local Government (Business Improvement Districts) Act 2006 | No. 42 of 2006 | `local-government-business-improvement-districts-act-2006/` | 3 | 2017-04-13 to 2023-01-09 | 10 |
| Criminal Law (Sexual Offences) (Amendment) Act 2007 | No. 6 of 2007 | `criminal-law-sexual-offences-amendment-act-2007/` | 1 | 2024-08-31 to 2024-08-31 | 8 |
| National Oil Reserves Agency Act 2007 | No. 7 of 2007 | `national-oil-reserves-agency-act-2007/` | 14 | 2018-05-30 to 2026-08-28 | 107 |
| Social Welfare and Pensions Act 2007 | No. 8 of 2007 | `social-welfare-and-pensions-act-2007/` | 2 | 2017-07-26 to 2023-01-09 | 43 |
| Education (Miscellaneous Provisions) Act 2007 | No. 9 of 2007 | `education-miscellaneous-provisions-act-2007/` | 2 | 2017-04-13 to 2021-06-24 | 10 |
| Prisons Act 2007 | No. 10 of 2007 | `prisons-act-2007/` | 3 | 2018-11-30 to 2023-08-01 | 44 |
| Carbon Fund Act 2007 | No. 12 of 2007 | `carbon-fund-act-2007/` | 2 | 2016-07-22 to 2019-05-28 | 11 |
| Consumer Protection Act 2007 | No. 19 of 2007 | `consumer-protection-act-2007/` | 15 | 2018-12-03 to 2025-11-24 | 132 |
| Pharmacy Act 2007 | No. 20 of 2007 | `pharmacy-act-2007/` | 15 | 2018-05-25 to 2026-06-30 | 90 |
| Building Control Act 2007 | No. 21 of 2007 | `building-control-act-2007/` | 4 | 2018-07-03 to 2022-08-29 | 77 |
| Communications Regulation (Amendment) Act 2007 | No. 22 of 2007 | `communications-regulation-amendment-act-2007/` | 3 | 2016-06-23 to 2025-06-01 | 36 |
| Health Act 2007 | No. 23 of 2007 | `health-act-2007/` | 7 | 2019-01-08 to 2025-03-31 | 122 |
| Medical Practitioners Act 2007 | No. 25 of 2007 | `medical-practitioners-act-2007/` | 10 | 2018-12-26 to 2026-07-29 | 154 |
| Child Care (Amendment) Act 2007 | No. 26 of 2007 | `child-care-amendment-act-2007/` | 2 | 2017-04-13 to 2020-05-21 | 23 |
| Protection of Employment (Exceptional Collective Redundancies and Related Matters) Act 2007 | No. 27 of 2007 | `protection-of-employment-exceptional-collective-redundancies-and-related-matters-act-2007/` | 2 | 2017-09-01 to 2020-10-14 | 28 |
| Criminal Justice Act 2007 | No. 29 of 2007 | `criminal-justice-act-2007/` | 8 | 2017-06-28 to 2025-04-02 | 64 |
| Water Services Act 2007 | No. 30 of 2007 | `water-services-act-2007/` | 4 | 2018-10-22 to 2025-12-31 | 138 |
| Community, Rural and Gaeltacht Affairs (Miscellaneous Provisions) Act 2007 | No. 32 of 2007 | `community-rural-and-gaeltacht-affairs-miscellaneous-provisions-act-2007/` | 3 | 2018-01-01 to 2025-06-01 | 12 |
| Roads Act 2007 | No. 34 of 2007 | `roads-act-2007/` | 1 | 2019-01-01 to 2019-01-01 | 16 |
| Markets in Financial Instruments and Miscellaneous Provisions Act 2007 | No. 37 of 2007 | `markets-in-financial-instruments-and-miscellaneous-provisions-act-2007/` | 1 | 2018-10-29 to 2018-10-29 | 27 |
| Social Welfare (Consolidated Occupational Injuries) Regulations 2007 | S.I. No. 102 of 2007 | `social-welfare-consolidated-occupational-injuries-regulations-2007/` | 3 | 2023-01-06 to 2026-01-06 | 83 |
| European Communities (Access to Information on the Environment) Regulations 2007 | S.I. No. 133 of 2007 | `european-communities-access-to-information-on-the-environment-regulations-2007/` | 1 | 2022-11-01 to 2022-11-01 | 17 |
| Social Welfare (Consolidated Claims, Payments and Control) Regulations 2007 | S.I. No. 142 of 2007 | `social-welfare-consolidated-claims-payments-and-control-regulations-2007/` | 3 | 2023-05-04 to 2026-01-21 | 416 |
| Prison Rules 2007 | S.I. No. 252 of 2007 | `prison-rules-2007/` | 1 | 2024-01-01 to 2024-01-01 | 129 |
| Safety, Health and Welfare at Work (General Application) Regulations 2007 | S.I. No. 299 of 2007 | `safety-health-and-welfare-at-work-general-application-regulations-2007/` | 2 | 2018-04-30 to 2023-05-24 | 188 |
| Social Welfare (Consolidated Supplementary Welfare Allowance) Regulations 2007 | S.I. No. 412 of 2007 | `social-welfare-consolidated-supplementary-welfare-allowance-regulations-2007/` | 3 | 2023-03-24 to 2026-01-21 | 54 |
| Social Welfare and Pensions Act 2008 | No. 2 of 2008 | `social-welfare-and-pensions-act-2008/` | 2 | 2017-07-26 to 2023-01-09 | 34 |
| Passports Act 2008 | No. 4 of 2008 | `passports-act-2008/` | 1 | 2018-05-25 to 2018-05-25 | 29 |
| Criminal Justice (Mutual Assistance) Act 2008 | No. 7 of 2008 | `criminal-justice-mutual-assistance-act-2008/` | 10 | 2018-08-17 to 2025-05-20 | 205 |
| Criminal Law (Human Trafficking) Act 2008 | No. 8 of 2008 | `criminal-law-human-trafficking-act-2008/` | 3 | 2017-03-27 to 2022-12-22 | 17 |
| Electricity Regulation (Amendment) (Eirgrid) Act 2008 | No. 11 of 2008 | `electricity-regulation-amendment-eirgrid-act-2008/` | 1 | 2022-07-12 to 2022-07-12 | 11 |
| Chemicals Act 2008 | No. 13 of 2008 | `chemicals-act-2008/` | 4 | 2018-05-25 to 2024-12-17 | 38 |
| Civil Law (Miscellaneous Provisions) Act 2008 | No. 14 of 2008 | `civil-law-miscellaneous-provisions-act-2008/` | 1 | 2020-08-21 to 2020-08-21 | 85 |
| Dublin Transport Authority Act 2008 | No. 15 of 2008 | `dublin-transport-authority-act-2008/` | 5 | 2018-10-22 to 2023-07-17 | 123 |
| Intoxicating Liquor Act 2008 | No. 17 of 2008 | `intoxicating-liquor-act-2008/` | 1 | 2022-05-04 to 2022-05-04 | 25 |
| Credit Institutions (Financial Support) Act 2008 | No. 18 of 2008 | `credit-institutions-financial-support-act-2008/` | 3 | 2017-04-07 to 2025-12-16 | 10 |
| Cluster Munitions And Anti-Personnel Mines Act 2008 | No. 20 of 2008 | `cluster-munitions-and-anti-personnel-mines-act-2008/` | 2 | 2017-04-07 to 2020-05-21 | 22 |
| Anglo Irish Bank Corporation Act 2009 | No. 1 of 2009 | `anglo-irish-bank-corporation-act-2009/` | 2 | 2016-06-23 to 2019-02-08 | 41 |
| Electoral (Amendment) Act 2009 | No. 4 of 2009 | `electoral-amendment-act-2009/` | 3 | 2017-04-07 to 2023-01-09 | 22 |
| Financial Emergency Measures in the Public Interest Act 2009 | No. 5 of 2009 | `financial-emergency-measures-in-the-public-interest-act-2009/` | 1 | 2018-01-01 to 2018-01-01 | 21 |
| Charities Act 2009 | No. 6 of 2009 | `charities-act-2009/` | 4 | 2018-07-04 to 2026-04-22 | 115 |
| Investment of the National Pensions Reserve Fund and Miscellaneous Provisions Act 2009 | No. 7 of 2009 | `investment-of-the-national-pensions-reserve-fund-and-miscellaneous-provisions-act-2009/` | 3 | 2016-08-31 to 2021-12-31 | 14 |
| Electoral (Amendment) (No. 2) Act 2009 | No. 9 of 2009 | `electoral-amendment-no-2-act-2009/` | 3 | 2017-04-07 to 2023-01-09 | 11 |
| Social Welfare and Pensions Act 2009 | No. 10 of 2009 | `social-welfare-and-pensions-act-2009/` | 2 | 2017-07-26 to 2023-01-09 | 24 |
| Financial Services (Deposit Guarantee Scheme) Act 2009 | No. 13 of 2009 | `financial-services-deposit-guarantee-scheme-act-2009/` | 1 | 2019-01-01 to 2019-01-01 | 21 |
| Nursing Homes Support Scheme Act 2009 | No. 15 of 2009 | `nursing-homes-support-scheme-act-2009/` | 10 | 2019-01-01 to 2026-03-13 | 76 |
| Aviation (Preclearance) Act 2009 | No. 16 of 2009 | `aviation-preclearance-act-2009/` | 2 | 2016-06-23 to 2019-05-28 | 23 |
| Broadcasting Act 2009 | No. 18 of 2009 | `broadcasting-act-2009/` | 15 | 2017-10-25 to 2026-06-12 | 315 |
| Criminal Justice (Surveillance) Act 2009 | No. 19 of 2009 | `criminal-justice-surveillance-act-2009/` | 5 | 2017-02-06 to 2025-04-02 | 20 |
| Housing (Miscellaneous Provisions) Act 2009 | No. 22 of 2009 | `housing-miscellaneous-provisions-act-2009/` | 8 | 2018-09-12 to 2025-12-31 | 106 |
| Land And Conveyancing Law Reform Act 2009 | No. 27 of 2009 | `land-and-conveyancing-law-reform-act-2009/` | 6 | 2016-06-30 to 2025-12-31 | 137 |
| Criminal Justice (Miscellaneous Provisions) Act 2009 | No. 28 of 2009 | `criminal-justice-miscellaneous-provisions-act-2009/` | 2 | 2018-05-25 to 2020-05-01 | 53 |
| Local Government (Charges) Act 2009 | No. 30 of 2009 | `local-government-charges-act-2009/` | 3 | 2017-04-07 to 2023-01-09 | 19 |
| Defamation Act 2009 | No. 31 of 2009 | `defamation-act-2009/` | 4 | 2020-01-17 to 2026-03-01 | 64 |
| National Asset Management Agency Act 2009 | No. 34 of 2009 | `national-asset-management-agency-act-2009/` | 4 | 2018-05-25 to 2026-08-01 | 245 |
| Courts and Court Officers Act 2009 | No. 36 of 2009 | `courts-and-court-officers-act-2009/` | 2 | 2017-04-07 to 2020-05-21 | 27 |
| Public Transport Regulation Act 2009 | No. 37 of 2009 | `public-transport-regulation-act-2009/` | 1 | 2018-10-22 to 2018-10-22 | 49 |
| Financial Emergency Measures in the Public Interest (No. 2) Act 2009 | No. 41 of 2009 | `financial-emergency-measures-in-the-public-interest-no-2-act-2009/` | 3 | 2018-01-01 to 2023-01-01 | 17 |
| Companies (Miscellaneous Provisions) Act 2009 | No. 45 of 2009 | `companies-miscellaneous-provisions-act-2009/` | 1 | 2019-01-01 to 2019-01-01 | 6 |
| Health Insurance Act 1994 (Information Returns) Regulations 2009 | S.I. No. 294 of 2009 | `health-insurance-act-1994-information-returns-regulations-2009/` | 1 | 2024-07-01 to 2024-07-01 | 9 |
| Arbitration Act 2010 | No. 1 of 2010 | `arbitration-act-2010/` | 2 | 2022-11-29 to 2023-07-05 | 40 |
| Communications Regulation (Premium Rate Services and Electronic Communications Infrastructure) Act 2010 | No. 2 of 2010 | `communications-regulation-premium-rate-services-and-electronic-communications-infrastructure-act-2010/` | 3 | 2017-04-07 to 2025-06-01 | 23 |
| Petroleum (Exploration and Extraction) Safety Act 2010 | No. 4 of 2010 | `petroleum-exploration-and-extraction-safety-act-2010/` | 3 | 2017-05-16 to 2023-01-09 | 5 |
| Criminal Justice (Money Laundering and Terrorist Financing) Act 2010 | No. 6 of 2010 | `criminal-justice-money-laundering-and-terrorist-financing-act-2010/` | 10 | 2018-11-26 to 2025-08-01 | 198 |
| Euro Area Loan Facility Act 2010 | No. 7 of 2010 | `euro-area-loan-facility-act-2010/` | 2 | 2016-06-30 to 2019-05-28 | 8 |
| Fines Act 2010 | No. 8 of 2010 | `fines-act-2010/` | 2 | 2016-01-11 to 2019-05-28 | 23 |
| Inland Fisheries Act 2010 | No. 10 of 2010 | `inland-fisheries-act-2010/` | 9 | 2019-01-01 to 2026-04-03 | 91 |
| Energy (Biofuel Obligation and Miscellaneous Provisions) Act 2010 | No. 11 of 2010 | `energy-biofuel-obligation-and-miscellaneous-provisions-act-2010/` | 2 | 2016-06-30 to 2019-09-01 | 29 |
| European Financial Stability Facility Act 2010 | No. 16 of 2010 | `european-financial-stability-facility-act-2010/` | 2 | 2016-06-30 to 2019-05-28 | 10 |
| Wildlife (Amendment) Act 2010 | No. 19 of 2010 | `wildlife-amendment-act-2010/` | 1 | 2018-07-18 to 2018-07-18 | 10 |
| Adoption Act 2010 | No. 21 of 2010 | `adoption-act-2010/` | 5 | 2018-02-01 to 2023-07-03 | 189 |
| Criminal Justice (Psychoactive Substances) Act 2010 | No. 22 of 2010 | `criminal-justice-psychoactive-substances-act-2010/` | 1 | 2023-12-22 to 2023-12-22 | 27 |
| Central Bank Reform Act 2010 | No. 23 of 2010 | `central-bank-reform-act-2010/` | 7 | 2018-07-01 to 2026-02-10 | 85 |
| Civil Partnership and Certain Rights and Obligations of Cohabitants Act 2010 | No. 24 of 2010 | `civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010/` | 5 | 2019-01-01 to 2024-11-13 | 221 |
| Road Traffic Act 2010 | No. 25 of 2010 | `road-traffic-act-2010/` | 10 | 2018-10-26 to 2026-01-01 | 99 |
| Criminal Procedure Act 2010 | No. 27 of 2010 | `criminal-procedure-act-2010/` | 4 | 2018-07-30 to 2024-12-31 | 40 |
| Social Welfare (Miscellaneous Provisions) Act 2010 | No. 28 of 2010 | `social-welfare-miscellaneous-provisions-act-2010/` | 1 | 2018-01-01 to 2018-01-01 | 36 |
| Dog Breeding Establishments Act 2010 | No. 29 of 2010 | `dog-breeding-establishments-act-2010/` | 3 | 2017-07-27 to 2025-08-01 | 27 |
| Planning and Development (Amendment) Act 2010 | No. 30 of 2010 | `planning-and-development-amendment-act-2010/` | 1 | 2019-01-25 to 2019-01-25 | 85 |
| Value-Added Tax Consolidation Act 2010 | No. 31 of 2010 | `value-added-tax-consolidation-act-2010/` | 15 | 2019-01-01 to 2026-08-01 | 174 |
| Credit Institutions (Stabilisation) Act 2010 | No. 36 of 2010 | `credit-institutions-stabilisation-act-2010/` | 4 | 2018-04-23 to 2025-07-14 | 87 |
| Social Welfare and Pensions Act 2010 | No. 37 of 2010 | `social-welfare-and-pensions-act-2010/` | 2 | 2017-07-26 to 2023-01-09 | 49 |
| Financial Emergency Measures in the Public Interest Act 2010 | No. 38 of 2010 | `financial-emergency-measures-in-the-public-interest-act-2010/` | 3 | 2018-01-01 to 2023-01-01 | 20 |
| Multi-Unit Developments Act 2011 | No. 2 of 2011 | `multi-unit-developments-act-2011/` | 2 | 2016-11-30 to 2019-05-28 | 38 |
| Communications (Retention of Data) Act 2011 | No. 3 of 2011 | `communications-retention-of-data-act-2011/` | 4 | 2018-05-25 to 2025-04-02 | 40 |
| Student Support Act 2011 | No. 4 of 2011 | `student-support-act-2011/` | 19 | 2019-01-01 to 2026-03-18 | 35 |
| Social Welfare and Pensions Act 2011 | No. 9 of 2011 | `social-welfare-and-pensions-act-2011/` | 1 | 2020-12-22 to 2020-12-22 | 44 |
| Ministers and Secretaries (Amendment) Act 2011 | No. 10 of 2011 | `ministers-and-secretaries-amendment-act-2011/` | 8 | 2018-09-28 to 2026-07-13 | 107 |
| Biological Weapons Act 2011 | No. 13 of 2011 | `biological-weapons-act-2011/` | 2 | 2014-12-28 to 2019-05-28 | 16 |
| Child Care (Amendment) Act 2011 | No. 19 of 2011 | `child-care-amendment-act-2011/` | 2 | 2018-01-01 to 2026-06-23 | 50 |
| Environment (Miscellaneous Provisions) Act 2011 | No. 20 of 2011 | `environment-miscellaneous-provisions-act-2011/` | 3 | 2018-07-19 to 2026-05-08 | 52 |
| Communications Regulation (Postal Services) Act 2011 | No. 21 of 2011 | `communications-regulation-postal-services-act-2011/` | 3 | 2019-01-01 to 2025-06-01 | 83 |
| Criminal Justice Act 2011 | No. 22 of 2011 | `criminal-justice-act-2011/` | 3 | 2018-07-30 to 2023-11-01 | 25 |
| Civil Law (Miscellaneous Provisions) Act 2011 | No. 23 of 2011 | `civil-law-miscellaneous-provisions-act-2011/` | 2 | 2017-04-07 to 2020-05-21 | 68 |
| European Financial Stability Facility and Euro Area Loan Facility (Amendment) Act 2011 | No. 25 of 2011 | `european-financial-stability-facility-and-euro-area-loan-facility-amendment-act-2011/` | 2 | 2016-06-30 to 2019-05-28 | 8 |
| Central Bank and Credit Institutions (Resolution) Act 2011 | No. 27 of 2011 | `central-bank-and-credit-institutions-resolution-act-2011/` | 7 | 2018-09-27 to 2025-09-30 | 116 |
| Welfare of Greyhounds Act 2011 | No. 29 of 2011 | `welfare-of-greyhounds-act-2011/` | 4 | 2016-06-08 to 2025-04-02 | 30 |
| Road Transport Act 2011 | No. 31 of 2011 | `road-transport-act-2011/` | 5 | 2015-11-01 to 2025-11-10 | 25 |
| Local Government (Household Charge) Act 2011 | No. 36 of 2011 | `local-government-household-charge-act-2011/` | 3 | 2017-05-16 to 2023-01-09 | 21 |
| Property Services (Regulation) Act 2011 | No. 40 of 2011 | `property-services-regulation-act-2011/` | 10 | 2018-05-25 to 2026-06-17 | 110 |
| Nurses and Midwives Act 2011 | No. 41 of 2011 | `nurses-and-midwives-act-2011/` | 7 | 2018-12-26 to 2025-05-06 | 120 |
| Energy (Miscellaneous Provisions) Act 2012 | No. 3 of 2012 | `energy-miscellaneous-provisions-act-2012/` | 1 | 2019-01-01 to 2019-01-01 | 23 |
| Criminal Justice (Female Genital Mutilation) Act 2012 | No. 11 of 2012 | `criminal-justice-female-genital-mutilation-act-2012/` | 3 | 2017-11-27 to 2024-08-31 | 17 |
| Protection of Employees (Temporary Agency Work) Act 2012 | No. 13 of 2012 | `protection-of-employees-temporary-agency-work-act-2012/` | 2 | 2017-09-01 to 2020-10-14 | 28 |
| Road Safety Authority (Commercial Vehicle Roadworthiness) Act 2012 | No. 16 of 2012 | `road-safety-authority-commercial-vehicle-roadworthiness-act-2012/` | 9 | 2018-05-20 to 2025-01-01 | 58 |
| European Stability Mechanism Act 2012 | No. 20 of 2012 | `european-stability-mechanism-act-2012/` | 2 | 2017-04-13 to 2021-12-09 | 12 |
| Criminal Justice (Withholding of Information on Offences against Children and Vulnerable Persons) Act 2012 | No. 24 of 2012 | `criminal-justice-withholding-of-information-on-offences-against-children-and-vulnerable-persons-act-2012/` | 5 | 2017-03-27 to 2025-05-30 | 15 |
| Credit Guarantee Act 2012 | No. 26 of 2012 | `credit-guarantee-act-2012/` | 5 | 2017-03-03 to 2022-12-08 | 15 |
| Qualifications and Quality Assurance (Education and Training) Act 2012 | No. 28 of 2012 | `qualifications-and-quality-assurance-education-and-training-act-2012/` | 7 | 2018-04-24 to 2026-01-01 | 106 |
| European Arrest Warrant (Application to Third Countries and Amendment) and Extradition (Amendment) Act 2012 | No. 30 of 2012 | `european-arrest-warrant-application-to-third-countries-and-amendment-and-extradition-amendment-act-2012/` | 1 | 2021-03-30 to 2021-03-30 | 36 |
| Microenterprise Loan Fund Act 2012 | No. 31 of 2012 | `microenterprise-loan-fund-act-2012/` | 3 | 2020-04-28 to 2024-08-28 | 24 |
| Residential Institutions Statutory Fund Act 2012 | No. 35 of 2012 | `residential-institutions-statutory-fund-act-2012/` | 4 | 2017-09-01 to 2024-07-17 | 46 |
| Public Service Pensions (Single Scheme and Other Provisions) Act 2012 | No. 37 of 2012 | `public-service-pensions-single-scheme-and-other-provisions-act-2012/` | 8 | 2017-01-27 to 2024-08-19 | 76 |
| Fiscal Responsibility Act 2012 | No. 39 of 2012 | `fiscal-responsibility-act-2012/` | 2 | 2017-04-13 to 2020-12-16 | 13 |
| Credit Union and Co-operation with Overseas Regulators Act 2012 | No. 40 of 2012 | `credit-union-and-co-operation-with-overseas-regulators-act-2012/` | 8 | 2018-10-22 to 2025-09-30 | 76 |
| Personal Insolvency Act 2012 | No. 44 of 2012 | `personal-insolvency-act-2012/` | 7 | 2018-05-25 to 2026-03-16 | 217 |
| National Vetting Bureau (Children and Vulnerable Persons) Act 2012 | No. 47 of 2012 | `national-vetting-bureau-children-and-vulnerable-persons-act-2012/` | 5 | 2019-01-01 to 2026-06-23 | 37 |
| Civil Defence Act 2012 | No. 51 of 2012 | `civil-defence-act-2012/` | 3 | 2017-04-07 to 2023-07-18 | 19 |
| Finance (Local Property Tax) Act 2012 | No. 52 of 2012 | `finance-local-property-tax-act-2012/` | 9 | 2018-12-03 to 2026-05-07 | 180 |
| Europol Act 2012 | No. 53 of 2012 | `europol-act-2012/` | 2 | 2018-05-25 to 2025-04-02 | 23 |
| Irish Bank Resolution Corporation Act 2013 | No. 2 of 2013 | `irish-bank-resolution-corporation-act-2013/` | 3 | 2016-08-01 to 2026-08-01 | 31 |
| Water Services Act 2013 | No. 6 of 2013 | `water-services-act-2013/` | 2 | 2018-05-25 to 2023-01-01 | 42 |
| Health (Alteration of Criteria for Eligibility) Act 2013 | No. 10 of 2013 | `health-alteration-of-criteria-for-eligibility-act-2013/` | 1 | 2018-05-25 to 2018-05-25 | 9 |
| Education and Training Boards Act 2013 | No. 11 of 2013 | `education-and-training-boards-act-2013/` | 4 | 2018-04-24 to 2025-05-01 | 80 |
| Health (Pricing and Supply of Medical Goods) Act 2013 | No. 14 of 2013 | `health-pricing-and-supply-of-medical-goods-act-2013/` | 4 | 2019-01-01 to 2025-06-01 | 40 |
| Animal Health and Welfare Act 2013 | No. 15 of 2013 | `animal-health-and-welfare-act-2013/` | 23 | 2019-01-01 to 2026-05-05 | 96 |
| Financial Emergency Measures in the Public Interest Act 2013 | No. 18 of 2013 | `financial-emergency-measures-in-the-public-interest-act-2013/` | 2 | 2016-07-18 to 2019-09-01 | 14 |
| Criminal Justice Act 2013 | No. 19 of 2013 | `criminal-justice-act-2013/` | 1 | 2018-11-26 to 2018-11-26 | 29 |
| Social Welfare and Pensions (Miscellaneous Provisions) Act 2013 | No. 20 of 2013 | `social-welfare-and-pensions-miscellaneous-provisions-act-2013/` | 1 | 2018-01-01 to 2018-01-01 | 34 |
| Health Service Executive (Governance) Act 2013 | No. 23 of 2013 | `health-service-executive-governance-act-2013/` | 1 | 2019-06-28 to 2019-06-28 | 24 |
| Further Education and Training Act 2013 | No. 25 of 2013 | `further-education-and-training-act-2013/` | 19 | 2018-09-12 to 2026-07-15 | 53 |
| Central Bank (Supervision and Enforcement) Act 2013 | No. 26 of 2013 | `central-bank-supervision-and-enforcement-act-2013/` | 12 | 2019-01-28 to 2026-07-07 | 104 |
| Land and Conveyancing Law Reform Act 2013 | No. 30 of 2013 | `land-and-conveyancing-law-reform-act-2013/` | 1 | 2019-08-01 to 2019-08-01 | 7 |
| Houses of the Oireachtas (Inquiries, Privileges and Procedures) Act 2013 | No. 33 of 2013 | `houses-of-the-oireachtas-inquiries-privileges-and-procedures-act-2013/` | 4 | 2017-05-16 to 2025-04-02 | 135 |
| Taxi Regulation Act 2013 | No. 37 of 2013 | `taxi-regulation-act-2013/` | 10 | 2018-02-01 to 2026-04-01 | 80 |
| Gas Regulation Act 2013 | No. 39 of 2013 | `gas-regulation-act-2013/` | 1 | 2024-06-01 to 2024-06-01 | 54 |
| Child and Family Agency Act 2013 | No. 40 of 2013 | `child-and-family-agency-act-2013/` | 6 | 2018-06-30 to 2025-11-26 | 101 |
| Credit Reporting Act 2013 | No. 45 of 2013 | `credit-reporting-act-2013/` | 3 | 2018-10-29 to 2026-08-01 | 36 |
| Companies (Miscellaneous Provisions) Act 2013 | No. 46 of 2013 | `companies-miscellaneous-provisions-act-2013/` | 1 | 2019-01-01 to 2019-01-01 | 12 |
| Water Services (No. 2) Act 2013 | No. 50 of 2013 | `water-services-no-2-act-2013/` | 11 | 2018-12-31 to 2025-12-31 | 50 |
| Local Government Reform Act 2014 | No. 1 of 2014 | `local-government-reform-act-2014/` | 4 | 2017-11-10 to 2024-05-16 | 86 |
| Road Traffic Act 2014 | No. 3 of 2014 | `road-traffic-act-2014/` | 5 | 2017-04-13 to 2024-10-01 | 27 |
| Criminal Justice (Forensic Evidence and DNA Database System) Act 2014 | No. 11 of 2014 | `criminal-justice-forensic-evidence-and-dna-database-system-act-2014/` | 7 | 2021-07-30 to 2026-09-01 | 177 |
| Industrial Development (Forfás Dissolution) Act 2014 | No. 13 of 2014 | `industrial-development-forf-s-dissolution-act-2014/` | 1 | 2024-08-01 to 2024-08-01 | 44 |
| Protected Disclosures Act 2014 | No. 14 of 2014 | `protected-disclosures-act-2014/` | 8 | 2018-06-09 to 2026-06-08 | 52 |
| Health Identifiers Act 2014 | No. 15 of 2014 | `health-identifiers-act-2014/` | 2 | 2018-05-25 to 2022-03-31 | 42 |
| Social Welfare and Pensions Act 2014 | No. 16 of 2014 | `social-welfare-and-pensions-act-2014/` | 1 | 2018-01-01 to 2018-01-01 | 27 |
| Housing (Miscellaneous Provisions) Act 2014 | No. 21 of 2014 | `housing-miscellaneous-provisions-act-2014/` | 4 | 2022-01-04 to 2024-05-16 | 59 |
| Strategic Banking Corporation of Ireland Act 2014 | No. 22 of 2014 | `strategic-banking-corporation-of-ireland-act-2014/` | 1 | 2020-07-20 to 2020-07-20 | 24 |
| National Treasury Management Agency (Amendment) Act 2014 | No. 23 of 2014 | `national-treasury-management-agency-amendment-act-2014/` | 18 | 2018-12-17 to 2026-09-22 | 94 |
| Irish Human Rights and Equality Commission Act 2014 | No. 25 of 2014 | `irish-human-rights-and-equality-commission-act-2014/` | 4 | 2020-10-14 to 2025-05-01 | 61 |
| Employment Permits (Amendment) Act 2014 | No. 26 of 2014 | `employment-permits-amendment-act-2014/` | 1 | 2022-07-22 to 2022-07-22 | 40 |
| Competition and Consumer Protection Act 2014 | No. 29 of 2014 | `competition-and-consumer-protection-act-2014/` | 5 | 2022-11-29 to 2026-07-31 | 113 |
| Freedom of Information Act 2014 | No. 30 of 2014 | `freedom-of-information-act-2014/` | 9 | 2018-12-26 to 2026-07-31 | 61 |
| Forestry Act 2014 | No. 31 of 2014 | `forestry-act-2014/` | 5 | 2017-11-09 to 2023-10-13 | 39 |
| European Stability Mechanism (Amendment) Act 2014 | No. 32 of 2014 | `european-stability-mechanism-amendment-act-2014/` | 1 | 2021-12-09 to 2021-12-09 | 8 |
| Civil Registration (Amendment) Act 2014 | No. 34 of 2014 | `civil-registration-amendment-act-2014/` | 4 | 2016-07-11 to 2025-12-10 | 37 |
| Companies Act 2014 | No. 38 of 2014 | `companies-act-2014/` | 21 | 2018-12-19 to 2025-07-15 | 1862 |
| Water Services Act 2014 | No. 44 of 2014 | `water-services-act-2014/` | 3 | 2018-01-01 to 2024-06-01 | 22 |
| Health Insurance Act 1994 (Determination of Relevant Increase under section 7A and Provision of Information under section 7B) Regulations 2014 | S.I. No. 312 of 2014 | `health-insurance-act-1994-determination-of-relevant-increase-under-section-7a-and-provision-of-information-under-section-7b-regulations-2014/` | 1 | 2024-07-01 to 2024-07-01 | 8 |
| Irish Collective Asset-Management Vehicles Act 2015 | No. 2 of 2015 | `irish-collective-asset-management-vehicles-act-2015/` | 4 | 2018-09-21 to 2022-07-06 | 203 |
| Public Health (Standardised Packaging of Tobacco) Act 2015 | No. 4 of 2015 | `public-health-standardised-packaging-of-tobacco-act-2015/` | 3 | 2017-09-30 to 2023-01-09 | 24 |
| Regulation of Lobbying Act 2015 | No. 5 of 2015 | `regulation-of-lobbying-act-2015/` | 7 | 2018-05-25 to 2025-12-31 | 36 |
| Redress for Women Resident in Certain Institutions Act 2015 | No. 8 of 2015 | `redress-for-women-resident-in-certain-institutions-act-2015/` | 2 | 2019-08-02 to 2020-10-14 | 8 |
| Children and Family Relationships Act 2015 | No. 9 of 2015 | `children-and-family-relationships-act-2015/` | 5 | 2017-10-19 to 2026-04-20 | 182 |
| Vehicle Clamping Act 2015 | No. 13 of 2015 | `vehicle-clamping-act-2015/` | 3 | 2017-10-01 to 2025-10-01 | 38 |
| Sport Ireland Act 2015 | No. 15 of 2015 | `sport-ireland-act-2015/` | 2 | 2018-05-25 to 2020-09-16 | 48 |
| Workplace Relations Act 2015 | No. 16 of 2015 | `workplace-relations-act-2015/` | 12 | 2017-09-01 to 2026-06-29 | 95 |
| Customs Act 2015 | No. 18 of 2015 | `customs-act-2015/` | 5 | 2018-05-25 to 2025-08-01 | 57 |
| Gender Recognition Act 2015 | No. 25 of 2015 | `gender-recognition-act-2015/` | 1 | 2019-01-01 to 2019-01-01 | 39 |
| Industrial Relations (Amendment) Act 2015 | No. 27 of 2015 | `industrial-relations-amendment-act-2015/` | 6 | 2018-03-06 to 2025-08-01 | 47 |
| Environment (Miscellaneous Provisions) Act 2015 | No. 29 of 2015 | `environment-miscellaneous-provisions-act-2015/` | 1 | 2024-07-31 to 2024-07-31 | 52 |
| Urban Regeneration and Housing Act 2015 | No. 33 of 2015 | `urban-regeneration-and-housing-act-2015/` | 5 | 2018-11-01 to 2026-08-12 | 38 |
| Children First Act 2015 | No. 36 of 2015 | `children-first-act-2015/` | 4 | 2018-06-30 to 2026-06-23 | 32 |
| Residential Tenancies (Amendment) Act 2015 | No. 42 of 2015 | `residential-tenancies-amendment-act-2015/` | 2 | 2019-05-31 to 2023-03-15 | 89 |
| National Cultural Institutions (National Concert Hall) Act 2015 | No. 44 of 2015 | `national-cultural-institutions-national-concert-hall-act-2015/` | 1 | 2023-02-28 to 2023-02-28 | 40 |
| Climate Action and Low Carbon Development Act 2015 | No. 46 of 2015 | `climate-action-and-low-carbon-development-act-2015/` | 2 | 2021-10-12 to 2026-07-27 | 24 |
| PRISONS ACT 2015 | No. 57 of 2015 | `prisons-act-2015/` | 1 | 2026-06-12 to 2026-06-12 | 26 |
| Finance (Tax Appeals) Act 2015 | No. 59 of 2015 | `finance-tax-appeals-act-2015/` | 3 | 2020-10-01 to 2023-12-18 | 53 |
| Assisted Decision-Making (Capacity) Act 2015 | No. 64 of 2015 | `assisted-decision-making-capacity-act-2015/` | 6 | 2019-01-01 to 2026-03-31 | 166 |
| Legal Services Regulation Act 2015 | No. 65 of 2015 | `legal-services-regulation-act-2015/` | 10 | 2018-12-29 to 2026-07-27 | 231 |
| International Protection Act 2015 | No. 66 of 2015 | `international-protection-act-2015/` | 13 | 2018-06-30 to 2026-06-18 | 92 |
| Credit Guarantee (Amendment) Act 2016 | No. 1 of 2016 | `credit-guarantee-amendment-act-2016/` | 2 | 2020-08-11 to 2022-12-08 | 21 |
| Horse Racing Ireland Act 2016 | No. 2 of 2016 | `horse-racing-ireland-act-2016/` | 1 | 2023-07-11 to 2023-07-11 | 22 |
| Criminal Justice (Spent Convictions and Certain Disclosures) Act 2016 | No. 4 of 2016 | `criminal-justice-spent-convictions-and-certain-disclosures-act-2016/` | 3 | 2018-05-25 to 2025-04-02 | 32 |
| Paternity Leave and Benefit Act 2016 | No. 11 of 2016 | `paternity-leave-and-benefit-act-2016/` | 2 | 2021-04-01 to 2022-07-01 | 38 |
| Planning and Development (Housing) and Residential Tenancies Act 2016 | No. 17 of 2016 | `planning-and-development-housing-and-residential-tenancies-act-2016/` | 7 | 2019-01-01 to 2025-12-31 | 52 |
| Road Traffic Act 2016 | No. 21 of 2016 | `road-traffic-act-2016/` | 3 | 2018-12-22 to 2024-11-21 | 45 |
| Criminal Law (Sexual Offences) Act 2017 | No. 2 of 2017 | `criminal-law-sexual-offences-act-2017/` | 5 | 2018-05-30 to 2024-08-31 | 60 |
| Criminal Justice (Offences Relating to Information Systems) Act 2017 | No. 11 of 2017 | `criminal-justice-offences-relating-to-information-systems-act-2017/` | 1 | 2025-04-02 to 2025-04-02 | 16 |
| Financial Services and Pensions Ombudsman Act 2017 | No. 22 of 2017 | `financial-services-and-pensions-ombudsman-act-2017/` | 11 | 2018-10-29 to 2026-03-06 | 79 |
| National Shared Services Office Act 2017 | No. 26 of 2017 | `national-shared-services-office-act-2017/` | 3 | 2018-07-18 to 2025-04-02 | 38 |
| Mediation Act 2017 | No. 27 of 2017 | `mediation-act-2017/` | 1 | 2019-01-01 to 2019-01-01 | 28 |
| Criminal Justice (Victims of Crime) Act 2017 | No. 28 of 2017 | `criminal-justice-victims-of-crime-act-2017/` | 7 | 2019-01-01 to 2025-04-02 | 38 |
| Water Services Act 2017 | No. 29 of 2017 | `water-services-act-2017/` | 2 | 2023-04-28 to 2024-06-01 | 63 |
| Public Service Pay and Pensions Act 2017 | No. 34 of 2017 | `public-service-pay-and-pensions-act-2017/` | 11 | 2020-10-14 to 2026-01-31 | 46 |
| Protection of Cultural Property in the event of Armed Conflict (Hague Convention) Act 2017 | No. 36 of 2017 | `protection-of-cultural-property-in-the-event-of-armed-conflict-hague-convention-act-2017/` | 1 | 2021-03-30 to 2021-03-30 | 14 |
| Technological Universities Act 2018 | No. 3 of 2018 | `technological-universities-act-2018/` | 2 | 2022-11-10 to 2023-11-01 | 111 |
| Vehicle Registration Data (Automated Searching and Exchange) Act 2018 | No. 5 of 2018 | `vehicle-registration-data-automated-searching-and-exchange-act-2018/` | 1 | 2026-06-15 to 2026-06-15 | 12 |
| Domestic Violence Act 2018 | No. 6 of 2018 | `domestic-violence-act-2018/` | 3 | 2021-02-10 to 2024-09-02 | 57 |
| Data Protection Act 2018 | No. 7 of 2018 | `data-protection-act-2018/` | 17 | 2018-12-26 to 2026-07-16 | 238 |
| Criminal Justice (Corruption Offences) Act 2018 | No. 9 of 2018 | `criminal-justice-corruption-offences-act-2018/` | 3 | 2023-11-01 to 2025-06-18 | 37 |
| Childcare Support Act 2018 | No. 11 of 2018 | `childcare-support-act-2018/` | 6 | 2020-12-31 to 2026-08-31 | 34 |
| Planning and Development (Amendment) Act 2018 | No. 16 of 2018 | `planning-and-development-amendment-act-2018/` | 5 | 2018-10-22 to 2023-07-17 | 81 |
| Home Building Finance Ireland Act 2018 | No. 28 of 2018 | `home-building-finance-ireland-act-2018/` | 1 | 2026-08-01 to 2026-08-01 | 40 |
| European Investment Fund Agreement Act 2018 | No. 32 of 2018 | `european-investment-fund-agreement-act-2018/` | 1 | 2020-07-20 to 2020-07-20 | 6 |
| Central Bank (National Claims Information Database) Act 2018 | No. 42 of 2018 | `central-bank-national-claims-information-database-act-2018/` | 1 | 2022-07-08 to 2022-07-08 | 16 |
| Local Government Act 2019 | No. 1 of 2019 | `local-government-act-2019/` | 1 | 2024-05-16 to 2024-05-16 | 49 |
| Data Sharing and Governance Act 2019 | No. 5 of 2019 | `data-sharing-and-governance-act-2019/` | 3 | 2023-06-26 to 2024-06-01 | 77 |
| Criminal Law (Extraterritorial Jurisdiction) Act 2019 | No. 6 of 2019 | `criminal-law-extraterritorial-jurisdiction-act-2019/` | 2 | 2023-11-01 to 2024-12-31 | 7 |
| Withdrawal of the United Kingdom from the European Union (Consequential Provisions) Act 2019 | No. 8 of 2019 | `withdrawal-of-the-united-kingdom-from-the-european-union-consequential-provisions-act-2019/` | 1 | 2020-01-31 to 2020-01-31 | 99 |
| Aircraft Noise (Dublin Airport) Regulation Act 2019 | No. 12 of 2019 | `aircraft-noise-dublin-airport-regulation-act-2019/` | 1 | 2026-07-27 to 2026-07-27 | 32 |
| Residential Tenancies (Amendment) Act 2019 | No. 14 of 2019 | `residential-tenancies-amendment-act-2019/` | 4 | 2019-07-15 to 2024-10-18 | 39 |
| Criminal Justice (Mutual Recognition of Probation Judgments and Decisions) Act 2019 | No. 20 of 2019 | `criminal-justice-mutual-recognition-of-probation-judgments-and-decisions-act-2019/` | 1 | 2023-05-03 to 2023-05-03 | 33 |
| Local Government Rates and Other Matters Act 2019 | No. 24 of 2019 | `local-government-rates-and-other-matters-act-2019/` | 3 | 2024-01-01 to 2025-12-31 | 31 |
| Criminal Justice (International Co-operation) Act 2019 | No. 27 of 2019 | `criminal-justice-international-co-operation-act-2019/` | 1 | 2025-04-02 to 2025-04-02 | 11 |
| Parole Act 2019 | No. 28 of 2019 | `parole-act-2019/` | 3 | 2021-12-27 to 2023-11-01 | 42 |
| CervicalCheck Tribunal Act 2019 | No. 31 of 2019 | `cervicalcheck-tribunal-act-2019/` | 2 | 2022-05-23 to 2026-01-30 | 41 |
| Judicial Council Act 2019 | No. 33 of 2019 | `judicial-council-act-2019/` | 7 | 2020-10-25 to 2025-06-23 | 104 |
| Parent’s Leave and Benefit Act 2019 | No. 35 of 2019 | `parent-s-leave-and-benefit-act-2019/` | 3 | 2021-04-01 to 2024-08-01 | 39 |
| Family Law Act 2019 | No. 37 of 2019 | `family-law-act-2019/` | 1 | 2020-12-17 to 2020-12-17 | 8 |
| Housing (Regulation of Approved Housing Bodies) Act 2019 | No. 47 of 2019 | `housing-regulation-of-approved-housing-bodies-act-2019/` | 3 | 2022-07-06 to 2024-11-18 | 73 |
| Criminal Records (Exchange of Information) Act 2019 | No. 51 of 2019 | `criminal-records-exchange-of-information-act-2019/` | 1 | 2025-04-02 to 2025-04-02 | 20 |
| Consumer Insurance Contracts Act 2019 | No. 53 of 2019 | `consumer-insurance-contracts-act-2019/` | 2 | 2023-01-01 to 2026-05-12 | 30 |
| Health (Preservation and Protection and other Emergency Measures in the Public Interest) Act 2020 | No. 1 of 2020 | `health-preservation-and-protection-and-other-emergency-measures-in-the-public-interest-act-2020/` | 3 | 2021-07-01 to 2022-06-21 | 12 |
| Emergency Measures in the Public Interest (Covid-19) Act 2020 | No. 2 of 2020 | `emergency-measures-in-the-public-interest-covid-19-act-2020/` | 5 | 2020-08-01 to 2024-11-12 | 36 |
| Residential Tenancies and Valuation Act 2020 | No. 7 of 2020 | `residential-tenancies-and-valuation-act-2020/` | 1 | 2022-07-24 to 2022-07-24 | 15 |
| Civil Law and Criminal Law (Miscellaneous Provisions) Act 2020 | No. 13 of 2020 | `civil-law-and-criminal-law-miscellaneous-provisions-act-2020/` | 3 | 2023-07-31 to 2026-02-09 | 34 |
| Criminal Justice (Enforcement Powers) (Covid-19) Act 2020 | No. 14 of 2020 | `criminal-justice-enforcement-powers-covid-19-act-2020/` | 2 | 2021-07-03 to 2022-02-10 | 18 |
| Regulated Professions (Health and Social Care) (Amendment) Act 2020 | No. 16 of 2020 | `regulated-professions-health-and-social-care-amendment-act-2020/` | 3 | 2023-06-06 to 2025-09-05 | 186 |
| Residential Tenancies Act 2020 | No. 17 of 2020 | `residential-tenancies-act-2020/` | 2 | 2021-03-30 to 2022-10-29 | 6 |
| Health (Amendment) Act 2020 | No. 19 of 2020 | `health-amendment-act-2020/` | 3 | 2021-06-10 to 2022-02-10 | 7 |
| Criminal Justice (Mutual Recognition of Decisions on Supervision Measures) Act 2020 | No. 21 of 2020 | `criminal-justice-mutual-recognition-of-decisions-on-supervision-measures-act-2020/` | 1 | 2023-05-03 to 2023-05-03 | 39 |
| Planning and Development, and Residential Tenancies, Act 2020 | No. 27 of 2020 | `planning-and-development-and-residential-tenancies-act-2020/` | 2 | 2021-03-30 to 2021-07-09 | 17 |
| Loan Guarantee Schemes Agreements (Strategic Banking Corporation of Ireland) Act 2021 | No. 9 of 2021 | `loan-guarantee-schemes-agreements-strategic-banking-corporation-of-ireland-act-2021/` | 1 | 2022-12-08 to 2022-12-08 | 6 |
| Planning and Development, Heritage and Broadcasting (Amendment) Act 2021 | No. 11 of 2021 | `planning-and-development-heritage-and-broadcasting-amendment-act-2021/` | 1 | 2025-06-18 to 2025-06-18 | 18 |
| Health (Amendment) (No. 2) Act 2021 | No. 24 of 2021 | `health-amendment-no-2-act-2021/` | 1 | 2022-01-10 to 2022-01-10 | 8 |
| Affordable Housing Act 2021 | No. 25 of 2021 | `affordable-housing-act-2021/` | 7 | 2022-07-28 to 2025-07-02 | 53 |
| Land Development Agency Act 2021 | No. 26 of 2021 | `land-development-agency-act-2021/` | 4 | 2024-06-01 to 2025-12-31 | 86 |
| Criminal Justice (Smuggling of Persons) Act 2021 | No. 42 of 2021 | `criminal-justice-smuggling-of-persons-act-2021/` | 1 | 2026-06-12 to 2026-06-12 | 30 |
| Companies (Corporate Enforcement Authority) Act 2021 | No. 48 of 2021 | `companies-corporate-enforcement-authority-act-2021/` | 2 | 2022-07-07 to 2023-06-11 | 39 |
| Maritime Area Planning Act 2021 | No. 50 of 2021 | `maritime-area-planning-act-2021/` | 9 | 2022-10-01 to 2026-07-23 | 214 |
| Garda Síochána (Functions and Operational Areas) Act 2022 | No. 7 of 2022 | `garda-s-och-na-functions-and-operational-areas-act-2022/` | 2 | 2023-07-31 to 2024-02-07 | 36 |
| Birth Information and Tracing Act 2022 | No. 14 of 2022 | `birth-information-and-tracing-act-2022/` | 1 | 2023-07-20 to 2023-07-20 | 75 |
| Civil Law (Miscellaneous Provisions) Act 2022 | No. 19 of 2022 | `civil-law-miscellaneous-provisions-act-2022/` | 2 | 2026-03-30 to 2026-06-12 | 63 |
| Circular Economy and Miscellaneous Provisions Act 2022 | No. 26 of 2022 | `circular-economy-and-miscellaneous-provisions-act-2022/` | 1 | 2026-05-08 to 2026-05-08 | 45 |
| Remediation of Dwellings Damaged by the Use of Defective Concrete Blocks Act 2022 | No. 28 of 2022 | `remediation-of-dwellings-damaged-by-the-use-of-defective-concrete-blocks-act-2022/` | 3 | 2026-02-25 to 2026-07-08 | 65 |
| Planning and Development, Maritime and Valuation (Amendment) Act 2022 | No. 29 of 2022 | `planning-and-development-maritime-and-valuation-amendment-act-2022/` | 3 | 2022-12-01 to 2024-05-16 | 78 |
| Electoral Reform Act 2022 | No. 30 of 2022 | `electoral-reform-act-2022/` | 3 | 2024-03-31 to 2025-10-10 | 208 |
| Higher Education Authority Act 2022 | No. 31 of 2022 | `higher-education-authority-act-2022/` | 1 | 2024-08-01 to 2024-08-01 | 150 |
| Garda Síochána (Compensation) Act 2022 | No. 33 of 2022 | `garda-s-och-na-compensation-act-2022/` | 1 | 2025-04-02 to 2025-04-02 | 36 |
| Air Navigation and Transport Act 2022 | No. 40 of 2022 | `air-navigation-and-transport-act-2022/` | 1 | 2023-07-20 to 2023-07-20 | 122 |
| Online Safety and Media Regulation Act 2022 | No. 41 of 2022 | `online-safety-and-media-regulation-act-2022/` | 1 | 2024-02-17 to 2024-02-17 | 81 |
| Planning and Development and Foreshore (Amendment) Act 2022 | No. 47 of 2022 | `planning-and-development-and-foreshore-amendment-act-2022/` | 1 | 2025-06-18 to 2025-06-18 | 22 |
| Water Environment (Abstractions and Associated Impoundments) Act 2022 | No. 48 of 2022 | `water-environment-abstractions-and-associated-impoundments-act-2022/` | 2 | 2025-06-18 to 2025-12-31 | 118 |
| Criminal Justice (Mutual Recognition of Custodial Sentences) Act 2023 | No. 3 of 2023 | `criminal-justice-mutual-recognition-of-custodial-sentences-act-2023/` | 1 | 2024-07-23 to 2024-07-23 | 88 |
| Patient Safety (Notifiable Incidents and Open Disclosure) Act 2023 | No. 10 of 2023 | `patient-safety-notifiable-incidents-and-open-disclosure-act-2023/` | 1 | 2024-10-01 to 2024-10-01 | 86 |
| Mother and Baby Institutions Payment Scheme Act 2023 | No. 20 of 2023 | `mother-and-baby-institutions-payment-scheme-act-2023/` | 1 | 2025-10-15 to 2025-10-15 | 59 |
| Wildlife (Amendment) Act 2023 | No. 25 of 2023 | `wildlife-amendment-act-2023/` | 2 | 2023-11-17 to 2024-06-01 | 8 |
| Historic and Archaeological Heritage and Miscellaneous Provisions Act 2023 | No. 26 of 2023 | `historic-and-archaeological-heritage-and-miscellaneous-provisions-act-2023/` | 1 | 2025-12-31 to 2025-12-31 | 290 |
| Garda Síochána (Recording Devices) Act 2023 | No. 32 of 2023 | `garda-s-och-na-recording-devices-act-2023/` | 3 | 2024-05-15 to 2026-07-01 | 51 |
| Judicial Appointments Commission Act 2023 | No. 33 of 2023 | `judicial-appointments-commission-act-2023/` | 2 | 2024-10-17 to 2025-01-01 | 71 |
| Public Health (Tobacco Products and Nicotine Inhaling Products) Act 2023 | No. 35 of 2023 | `public-health-tobacco-products-and-nicotine-inhaling-products-act-2023/` | 1 | 2026-02-02 to 2026-02-02 | 53 |
| Digital Services Act 2024 | No. 2 of 2024 | `digital-services-act-2024/` | 3 | 2024-09-02 to 2026-01-01 | 88 |
| Local Government (Mayor of Limerick) and Miscellaneous Provisions Act 2024 | No. 7 of 2024 | `local-government-mayor-of-limerick-and-miscellaneous-provisions-act-2024/` | 2 | 2025-06-18 to 2025-12-31 | 74 |
| Employment Permits Act 2024 | No. 17 of 2024 | `employment-permits-act-2024/` | 1 | 2026-06-12 to 2026-06-12 | 81 |
| Automatic Enrolment Retirement Savings System Act 2024 | No. 20 of 2024 | `automatic-enrolment-retirement-savings-system-act-2024/` | 2 | 2026-01-01 to 2026-06-01 | 142 |
| Criminal Law (Sexual Offences and Human Trafficking) Act 2024 | No. 28 of 2024 | `criminal-law-sexual-offences-and-human-trafficking-act-2024/` | 1 | 2026-08-10 to 2026-08-10 | 42 |
| Planning and Development Act 2024 | No. 34 of 2024 | `planning-and-development-act-2024/` | 5 | 2025-08-01 to 2026-05-18 | 645 |
| Gambling Regulation Act 2024 | No. 35 of 2024 | `gambling-regulation-act-2024/` | 4 | 2026-01-30 to 2026-07-06 | 275 |
| Automatic Enrolment Retirement Savings System Regulations 2025 | S.I. No. 637 of 2025 | `automatic-enrolment-retirement-savings-system-regulations-2025/` | 1 | 2026-01-01 to 2026-01-01 | 42 |

Left out: the Revised Acts in the list that the builder cannot read back exactly (`left_out.json` next to the builder,
which is part of the build's input, or a revision PDF the reader cannot read). Their text is not in this repository.

| Act | ELI | Why |
| --- | --- | --- |
| Electricity Regulation Act 1999 (Public Service Obligations) Order 2002 | `2002/si/217` | the Commission's layout of this Order runs its schedule headings into the long title ('SCHEDULE 1' over 'Part 1.' entries set like a contents) and carries numbered paragraphs ('1. Peat powered generating stations') with margin headings inside the schedules, so the schedules cannot be told from the articles |
| Merchant Shipping Act 2010 | `2010/act/14` | the revision updated to 2025-03-05 prints the heading of s.41 in the text column as 'Offences (>Chapter 3).' (a stray '>'), while its contents give 'Offences (Chapter 3).': the publisher's text, which the word check cannot match to the contents title |

The data was retrieved on 2026-10-28. The electronic Irish Statute Book (irishstatutebook.ie) has the acts as
enacted only, not revised text or past versions. Reuse terms: see LICENSE (not settled for the Revised Acts; the repository is
private).

## The build, step by step

1. `python -X utf8 scripts/ireland-law/build.py` in Lexifina's own repository wrote this repository from the
   retrieved files. `tools/build.py` here is the same file (git blob `c96be0e3195df02c7e1eb817caa3c2c1c52fe876`), with `tools/reproduce.py`, which
   writes this file, `tools/check_repo.py` and `tools/test_repo.py`. Every later build ran with `--offline`.
2. `python -X utf8 scripts/ireland-law/check_repo.py` read every revision of each act back from this repository with
   `tools/on_date.py`, on the day it is updated to, and compared it file by file with the text the builder reads from
   that PDF; then it compared the whole act, in order, with the PDF's body text read with a different PyMuPDF
   extraction (span text, not the builder's character positions) and without the builder's paragraph, heading and
   layout rules: character by character with white space removed (some PDFs hold no space glyphs), headings left out on
   both sides, schedules as the letters and digits they contain. Result: `2513 revisions checked (261602 files), 0 mismatches; 2513 revisions in order against the PDF text (87150698 words), 0 mismatches`.
3. `python -X utf8 scripts/ireland-law/test_repo.py --record` ran the functional smoke test (6 of 6 passed):
   - pass: blame names a law: protected-disclosures-act-2014/section-5.md lines by act-2014-14@irishstatutebook.invalid, act-2022-27@irishstatutebook.invalid, si-2023-375@irishstatutebook.invalid
   - pass: text before and after an amendment: protected-disclosures-act-2014/section-5.md 2022-12-31 != 2023-01-01; data-protection-act-2018/section-12.md 2026-06-11 != 2026-06-12
   - pass: log --follow in date order: protected-disclosures-act-2014/section-5.md 3 commits; protected-disclosures-act-2014/section-10.md 3 commits; data-protection-act-2018/section-117A.md 4 commits
   - pass: tags resolve, In-force on every commit: 3799 tags resolve; all 3548 commits carry In-force
   - pass: only the documentation commit is by Lexifina: only the documentation commit fa523a4798 is by Lexifina; 988 distinct authors
   - pass: README commands run: 10 README commands ran and printed output
4. `python -X utf8 scripts/ireland-law/build.py --offline --verify-rebuild` built the repository a second time from
   the same retrieved files into a temporary folder and compared the hashes. A second build from the same retrieved files into an empty folder gave the same history: the last law commit was `972d9b6eacc383703729b6455c8b779c260ad775` in both, and every one of the 3547 law commits and 3799 tags had the same hash.
5. The build was run once more to write these results into this file, and the final `main` was rebuilt again and
   compared hash for hash.

It ran with Python 3.12.10, PyMuPDF 2.0 and git version 2.46.0.windows.1 on Windows 11.

## How the text and the commits are derived

- **Revisions.** Each PDF says "Updated to <day>"; that day is the revision's day. Two listings updated to the same day
  are one revision (the later listing, unless the later one was printed without its annotations and the earlier
  with them: then the annotated one, `preferred_to_unannotated_listing` in `data/versions.json`). Revisions are
  ordered by that day.
- **Text.** PyMuPDF's character positions give the words (a space where the gap between two letters exceeds a
  threshold, or where the PDF has a space glyph). Running heads, page numbers, footnotes (below 8pt), footnote
  reference numbers (below 7pt) and the annotation notes (8–9pt) are taken out of the body; the notes are kept for
  the commit messages. The text starts at the long title and ends at "About this Revised Act". A section starts at a bold
  number ("12. "); its heading is the title the table of contents gives it. Annotation marks `F12[ ... ]` are removed.
  A word broken at a line end is joined with or without its hyphen as the act's other revisions write it.
- **One layout.** The PDFs of different years break the same words differently. So that a change of layout is not a
  change of law: a paragraph starting with a small letter runs on from the one before; a definition run on after
  another ("...; ‘data’ means ...") starts its own paragraph; consecutive part and chapter headings are joined and
  split again before each PART/CHAPTER; spaces inside quotation marks are dropped. Differences that remain, where no
  word changed, are commits labelled `Kind: editorial (layout)`: firearms-firearm-certificates-for-non-residents-act-2000 2018-05-25 (section-3, section-8), family-law-maintenance-of-spouses-and-children-act-1976 2019-01-01 (section-9), environment-miscellaneous-provisions-act-2011 2019-01-31 (section-41), protection-of-employees-employers-insolvency-act-1984 2019-02-01 (section-12), employees-provision-of-information-and-consultation-act-2006 2019-02-01 (section-10, section-14, section-15), road-safety-authority-act-2006 2019-02-01 (section-1, section-4, section-5, section-8, section-9, section-15, section-17, section-18, section-19, section-20, section-22, section-23, section-24, section-25, section-26, section-28, section-29, section-32, section-33), anglo-irish-bank-corporation-act-2009 2019-02-08 (long-title, section-21, section-25), valuation-act-2001 2019-02-20 (section-56), workplace-relations-act-2015 2019-03-04 (schedule-7), planning-and-development-act-2000 2019-03-10 (section-1A, section-2, section-37, section-214), housing-act-1988 2019-03-12 (section-5, section-9, section-11, section-15, section-18, section-20, section-24, section-27, schedule-1), dublin-transport-authority-act-2008 2019-03-17 (section-95), companies-act-2014 2019-03-29 (section-633, section-1000, section-1002, section-1173, section-1230, section-1283, section-1387, section-1388, section-1428), personal-injuries-assessment-board-act-2003 2019-04-03 (section-18, section-51A, section-68), planning-and-development-amendment-act-2018 2019-04-03 (section-4), education-and-training-boards-act-2013 2019-04-04 (long-title, section-4, section-9, section-14, section-17, section-23, section-30, section-31, section-33, section-34, section-44, section-45, section-58, section-69, section-73, schedule-3), communications-regulation-postal-services-act-2011 2019-04-10 (long-title, section-6, section-19, section-30, section-35, section-36, section-38, section-52, section-54, section-60), immigration-act-2003 2019-04-12 (section-4), local-government-act-2001 2019-04-16 (section-191), criminal-justice-terrorist-offences-act-2005 2019-04-18 (section-56), ministers-and-secretaries-amendment-act-2011 2019-04-18 (schedule-2), finance-local-property-tax-act-2012 2019-04-18 (section-17), criminal-justice-mutual-assistance-act-2008 2019-04-29 (section-76), housing-act-1966 2019-05-01 (section-56, section-84, schedule-1), companies-act-2014 2019-05-01 (section-360, section-1502, section-1503), railway-safety-act-2005 2019-05-07 (section-14), chemicals-act-2008 2019-05-10 (long-title, section-26), civil-registration-act-2004 2019-05-23 (section-19A, schedule-2, schedule-3), children-and-family-relationships-act-2015 2019-05-23 (section-135), sale-of-goods-act-1893 2019-05-28 (section-2, section-52, section-58), road-transport-act-1933 2019-05-28 (section-33, section-74), transport-act-1958 2019-05-28 (section-3, schedule-1), sale-of-goods-and-supply-of-services-act-1980 2019-05-28 (section-10, section-22, section-44, section-46), road-traffic-amendment-act-1984 2019-05-28 (section-3), defence-amendment-act-1987 2019-05-28 (section-2, section-3, section-5), liability-for-defective-products-act-1991 2019-05-28 (section-1, schedule-1), maintenance-act-1994 2019-05-28 (long-title), telecommunications-miscellaneous-provisions-act-1996 2019-05-28 (schedule-2, schedule-3), commission-to-inquire-into-child-abuse-amendment-act-2005 2019-05-28 (section-18), carbon-fund-act-2007 2019-05-28 (section-1, section-2, section-3, section-7), aviation-preclearance-act-2009 2019-05-28 (long-title, schedule-1), euro-area-loan-facility-act-2010 2019-05-28 (long-title, section-1, schedule-2), fines-act-2010 2019-05-28 (section-4, section-10, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20, section-21, section-22), european-financial-stability-facility-act-2010 2019-05-28 (schedule-1), multi-unit-developments-act-2011 2019-05-28 (section-22, schedule-1, schedule-2), european-financial-stability-facility-and-euro-area-loan-facility-amendment-act-2011 2019-05-28 (long-title, schedule-1, schedule-2, schedule-3, schedule-4), welfare-of-greyhounds-act-2011 2019-05-28 (section-1, section-27), irish-bank-resolution-corporation-act-2013 2019-05-28 (section-6, section-9, section-18), animal-health-and-welfare-act-2013 2019-05-28 (section-24, schedule-4), road-traffic-act-1961 2019-05-30 (section-26), residential-tenancies-act-2004 2019-06-04 (section-65, section-111, section-189, section-197), criminal-justice-terrorist-offences-act-2005 2019-06-20 (section-51, section-56), roads-act-1993 2019-06-24 (section-81), fisheries-amendment-act-1997 2019-06-25 (section-61), misuse-of-drugs-act-1977 2019-06-26 (section-15C, section-35), children-first-act-2015 2019-06-28 (long-title), planning-and-development-act-2000 2019-07-01 (section-37, schedule-7), residential-tenancies-act-2004 2019-07-01 (section-111), dublin-transport-authority-act-2008 2019-07-01 (section-2, section-32, section-58), planning-and-development-act-2000 2019-07-15 (section-1A, section-2, section-214), parental-leave-amendment-act-2006 2019-07-19 (section-2, section-3), central-bank-act-1942 2019-07-21 (section-33Y, section-33AA), extradition-act-1965 2019-07-22 (section-23, section-44), companies-act-2014 2019-07-22 (section-1387, section-1388, section-1413, section-1429, section-1502, section-1503), central-bank-supervision-and-enforcement-act-2013 2019-07-23 (long-title, section-73, section-80, section-81), wildlife-act-1976 2019-08-01 (section-65), firearms-act-1925 2019-09-01 (section-3), personal-injuries-assessment-board-act-2003 2019-09-01 (section-62, section-68), land-and-conveyancing-law-reform-act-2009 2019-09-01 (section-74), energy-biofuel-obligation-and-miscellaneous-provisions-act-2010 2019-09-01 (section-1, section-3), financial-emergency-measures-in-the-public-interest-act-2013 2019-09-01 (section-5), data-protection-act-1988 2019-09-02 (section-1), criminal-law-sexual-offences-act-2017 2019-09-02 (section-14), waste-management-act-1996 2019-09-11 (section-22, section-39), teaching-council-act-2001 2019-09-11 (section-34), garda-s-och-na-act-2005 2019-09-16 (section-33, section-33D), sea-fisheries-and-maritime-jurisdiction-act-2006 2019-09-20 (section-28, section-31), criminal-justice-mutual-assistance-act-2008 2019-09-23 (section-76), residential-tenancies-act-2004 2019-09-26 (section-15, section-39, section-53, section-90, section-99, section-111, section-189, section-197), criminal-justice-terrorist-offences-act-2005 2019-09-28 (section-51), public-service-pensions-single-scheme-and-other-provisions-act-2012 2019-10-01 (section-16), civil-registration-act-2004 2019-10-06 (schedule-2, schedule-3), companies-act-2014 2019-10-07 (section-167), sea-fisheries-and-maritime-jurisdiction-act-2006 2019-10-23 (section-28, section-31), adoptive-leave-act-1995 2019-10-24 (section-7), planning-and-development-act-2000 2019-10-24 (section-1A, section-2), road-traffic-act-2010 2019-11-01 (section-57, section-65), workplace-relations-act-2015 2019-11-01 (schedule-2), credit-union-and-co-operation-with-overseas-regulators-act-2012 2019-11-07 (section-6, section-24, section-26, section-27), qualifications-and-quality-assurance-education-and-training-act-2012 2019-11-08 (section-8, section-29), road-traffic-act-2010 2019-11-12 (section-57, section-65, section-81), road-traffic-act-1961 2019-11-25 (section-101C), road-traffic-act-2016 2019-11-25 (section-8, section-34), civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010 2019-12-01 (section-187), industrial-relations-act-1946 2019-12-02 (section-35), defence-act-1954 2019-12-02 (section-210), consumer-protection-act-2007 2019-12-02 (schedule-9), legal-services-regulation-act-2015 2019-12-03 (section-52), criminal-justice-mutual-assistance-act-2008 2019-12-12 (section-12, section-22, schedule-8, schedule-9, schedule-10, schedule-13, schedule-14), misuse-of-drugs-act-1977 2019-12-17 (section-15C), garda-s-och-na-act-2005 2019-12-17 (long-title), central-bank-act-1942 2019-12-18 (section-2, section-20, section-33ANF, schedule-5, schedule-6, schedule-7), residential-tenancies-act-2004 2019-12-18 (section-111, section-197), electricity-regulation-act-1999 2019-12-31 (section-13MA, schedule-3, schedule-4), regional-technical-colleges-act-1992 2020-01-01 (long-title, section-15, schedule-1), road-traffic-act-1994 2020-01-01 (section-25), credit-union-act-1997 2020-01-01 (section-76I), value-added-tax-consolidation-act-2010 2020-01-01 (section-64, section-77, section-87, section-91D, section-95, section-108C, schedule-7, schedule-8), companies-act-2014 2020-01-01 (section-142, section-184, section-291, section-360, section-503, section-562, section-567, section-633, section-1181, section-1384, section-1503, schedule-3, schedule-4, schedule-5, schedule-6, schedule-7, schedule-9, schedule-10, schedule-11, schedule-12, schedule-13, schedule-14, schedule-15, schedule-16, schedule-17, schedule-18), industrial-development-act-1986 2020-01-07 (section-6), industrial-development-enterprise-ireland-act-1998 2020-01-07 (long-title, section-18, section-19, section-20, section-36, section-37, section-38, section-50, schedule-1), consumer-protection-act-2007 2020-01-30 (section-99, schedule-8, schedule-9), industrial-relations-act-1946 2020-02-01 (section-35, section-53, section-58), education-act-1998 2020-02-01 (long-title, section-32), industrial-relations-miscellaneous-provisions-act-2004 2020-02-01 (section-3), health-and-social-care-professionals-act-2005 2020-02-06 (section-38), planning-and-development-amendment-act-2018 2020-02-08 (section-4), control-of-dogs-act-1986 2020-03-01 (schedule-1), road-traffic-act-1961 2020-03-20 (section-26, section-101C), defence-act-1954 2020-03-27 (section-56, section-78, section-161, section-202, section-210, section-222, section-237, section-273, section-309, schedule-2), planning-and-development-act-2000 2020-03-27 (section-1A, section-2, section-20, section-37, section-175, section-214), civil-registration-act-2004 2020-03-27 (schedule-2, schedule-3), residential-tenancies-act-2004 2020-03-27 (section-25), pharmacy-act-2007 2020-03-27 (section-73), derelict-sites-act-1990 2020-03-29 (long-title), urban-regeneration-and-housing-act-2015 2020-03-29 (section-13, section-29), mental-health-act-2001 2020-03-30 (schedule-1), public-service-pensions-single-scheme-and-other-provisions-act-2012 2020-04-01 (section-1, section-5, section-11, section-16, section-44), waste-management-act-1996 2020-04-14 (section-22), ministers-and-secretaries-amendment-act-2011 2020-04-23 (schedule-2, schedule-3), criminal-law-insanity-act-2006 2020-04-24 (section-1, section-3, section-4, section-5, section-7, section-11, section-13, schedule-1, schedule-2), employment-permits-act-2006 2020-05-01 (section-20A), criminal-justice-miscellaneous-provisions-act-2009 2020-05-01 (section-40, section-43), guardianship-of-infants-act-1964 2020-05-04 (section-7), succession-act-1965 2020-05-04 (section-52, section-113A), status-of-children-act-1987 2020-05-04 (long-title, section-5, section-49), adoption-act-2010 2020-05-04 (section-24, section-33, section-84, section-110, section-147, section-151, section-159, section-162, schedule-2), civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010 2020-05-04 (long-title, section-3, section-67, section-101, section-109, section-120, section-121, section-126, section-128, section-140, section-173, section-176, section-182, section-186, section-192, section-194, section-195, section-196, section-201), children-and-family-relationships-act-2015 2020-05-05 (section-135), property-services-regulation-act-2011 2020-05-07 (section-36), child-care-act-1991 2020-05-12 (section-45B), sea-fisheries-and-maritime-jurisdiction-act-2006 2020-05-13 (section-28, section-31), taxi-regulation-act-2013 2020-05-13 (section-35), courts-martial-appeals-act-1983 2020-05-21 (section-23A), criminal-justice-act-1984 2020-05-21 (section-10, section-16), child-abduction-and-enforcement-of-custody-orders-act-1991 2020-05-21 (schedule-2), child-trafficking-and-pornography-act-1998 2020-05-21 (section-4A), children-act-2001 2020-05-21 (section-2, section-7, section-16, section-88, section-147, section-150, section-152, section-153, section-156A, section-156B, section-187, section-188, section-189, section-225, section-226, section-227, section-228, section-229, section-230, section-231, section-232, section-233, section-234, section-235, section-236, section-237, section-238, section-239, section-240, section-241, section-242, section-243, section-244), credit-institutions-financial-support-act-2008 2020-05-21 (section-6, section-7), cluster-munitions-and-anti-personnel-mines-act-2008 2020-05-21 (schedule-1, schedule-2), courts-and-court-officers-act-2009 2020-05-21 (section-13), communications-regulation-premium-rate-services-and-electronic-communications-infrastructure-act-2010 2020-05-21 (long-title, section-7, section-16, section-21), civil-law-miscellaneous-provisions-act-2011 2020-05-21 (section-1, section-48, section-54, section-56), civil-defence-act-2012 2020-05-21 (section-8), health-and-social-care-professionals-act-2005 2020-05-27 (section-38, section-44, section-67, section-69, section-70, section-95, schedule-3, schedule-4), civil-service-regulation-amendment-act-2005 2020-05-29 (long-title, section-16, schedule-1), criminal-justice-terrorist-offences-act-2005 2020-06-15 (section-56), central-bank-act-1942 2020-06-25 (section-2, section-5C, section-30, section-33ANF, section-50, section-57A, section-57BD, section-57CL, section-57CN, section-57CO, schedule-5, schedule-6, schedule-7), planning-and-development-act-2000 2020-06-30 (long-title, section-1A, section-2, section-5, section-11C, section-20, section-27A, section-37, section-37D, section-37L, section-60, section-146C, section-148, section-175, section-177P, section-177AE, section-182C, section-209, section-214, section-246), immigration-act-2004 2020-07-10 (section-19), consumer-protection-act-2007 2020-07-12 (section-2, section-6, section-15, section-23, section-24, section-25, section-27, section-29, section-39, section-47, section-54, section-60, section-63, section-71, section-76, section-93, section-101, section-102), health-act-1947 2020-07-13 (section-31A, section-65, section-87, schedule-1), residential-tenancies-act-2004 2020-07-20 (section-145, section-148L, section-182, section-188), road-traffic-act-1961 2020-07-29 (section-4, section-16, section-22, section-22A, section-22B, section-23, section-23A, section-24, section-26, section-29, section-39, section-40, section-44A, section-46, section-51A, section-52, section-53, section-55, section-58, section-61, section-69A, section-78A, section-78B, section-84, section-86, section-88, section-89, section-90, section-93, section-101C, section-108), valuation-act-2001 2020-08-01 (section-14, section-56, section-68, schedule-1), national-oil-reserves-agency-act-2007 2020-08-01 (long-title, section-38), criminal-justice-terrorist-offences-act-2005 2020-08-03 (section-22, section-61, section-62, section-63, section-64, section-65, section-66, section-67, schedule-1, schedule-3, schedule-4, schedule-5, schedule-7), redundancy-payments-act-1967 2020-08-04 (section-29, schedule-1), credit-guarantee-act-2012 2020-08-11 (section-5, section-6, section-7, section-8, section-9, section-10, section-12), coroners-act-1962 2020-08-21 (section-10, section-19, section-40, section-42, section-50, section-51, section-52, section-59, schedule-1), companies-act-2014 2020-08-21 (section-142, section-175, section-217, section-254, section-257, section-272, section-360, section-503, section-562, section-797, section-808, section-826, section-854, section-941A, section-964, section-1002, section-1055, section-1123, section-1129, section-1173, section-1230, section-1234, section-1280, section-1283, section-1366, section-1367, section-1387, section-1388, section-1389, section-1409, section-1413, section-1429, schedule-2, schedule-7, schedule-8, schedule-14, schedule-15, schedule-17, schedule-18), criminal-law-sexual-offences-act-1993 2020-08-26 (section-3, schedule-1), non-fatal-offences-against-the-person-act-1997 2020-08-26 (section-18, section-25), education-for-persons-with-special-educational-needs-act-2004 2020-08-26 (long-title), road-traffic-act-2004 2020-08-26 (section-13, section-15, section-18, section-19, section-20, section-22, section-27, section-28, section-33, section-36), international-interests-in-mobile-equipment-cape-town-convention-act-2005 2020-08-26 (schedule-1, schedule-2), development-banks-act-2005 2020-08-26 (long-title, schedule-1), criminal-law-sexual-offences-act-2006 2020-08-26 (section-4, section-7), national-economic-and-social-development-office-act-2006 2020-08-26 (section-2, section-7, section-8, section-10, section-11, section-13, section-14, section-15, section-16, section-17, section-18, section-20, section-22, section-26, section-30, section-35, section-42), local-government-business-improvement-districts-act-2006 2020-08-26 (long-title, section-4, section-5, section-7, section-8), criminal-justice-act-2007 2020-08-26 (section-1, section-12, schedule-2), criminal-law-human-trafficking-act-2008 2020-08-26 (long-title), electoral-amendment-act-2009 2020-08-26 (long-title), criminal-justice-surveillance-act-2009 2020-08-26 (section-1, section-3, section-7, section-8, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-18), local-government-charges-act-2009 2020-08-26 (section-3, section-5, section-6, section-9, section-14), petroleum-exploration-and-extraction-safety-act-2010 2020-08-26 (section-3), criminal-justice-female-genital-mutilation-act-2012 2020-08-26 (section-14), residential-institutions-statutory-fund-act-2012 2020-08-26 (long-title, section-37), houses-of-the-oireachtas-inquiries-privileges-and-procedures-act-2013 2020-08-26 (section-2, section-5, section-7, section-9, section-19, section-32, section-41, section-42, section-55, section-57, section-58, section-64, section-69, section-75, section-76, section-82, section-90, section-94, section-96, section-104, section-107, section-111, section-112, section-116, section-119, section-130, section-133, schedule-1), local-government-reform-act-2014 2020-08-26 (section-15, section-17, section-29, section-36, section-37, section-57, section-61, schedule-1, schedule-4), road-traffic-act-2014 2020-08-26 (section-10), public-health-standardised-packaging-of-tobacco-act-2015 2020-08-26 (long-title), waste-management-act-1996 2020-08-27 (section-10, section-39A, section-40, section-49, section-54, section-56A, section-73), financial-services-and-pensions-ombudsman-act-2017 2020-09-01 (schedule-1), central-bank-act-1942 2020-09-04 (section-6F, section-6G, section-6H, section-6I, section-7, section-8, section-12, section-13, section-14, section-16, section-17, section-26, section-27, section-29, section-30, section-31, section-33, section-33B, section-33C, section-33E, section-33F, section-33G, section-33H, section-33I, section-33J, section-33K, section-33M, section-33AJ, section-33AN, section-33ANA, section-33ANB, section-33AW, section-33AY, section-41, section-42, section-43, section-44, section-45, section-46, section-47, section-48, section-49, section-51, section-57, section-57A, section-57L, section-57Z, section-57BA, section-57BB, section-57BC, section-57BD, section-57BE, section-57BF, section-57BG, section-57BH, section-57BI, section-57BJ, section-57BK, section-57BL, section-57BM, section-57BN, section-57BO, section-57BP, section-57BQ, section-57BR, section-57BS, section-57BU, section-57BV, section-57BX, section-57BY, section-57BZ, section-57CC, section-57CD, section-57CE, section-57CF, section-57CG, section-57CH, section-57CI, section-57CK, section-57CM, section-57CN, section-57CP, section-57CQ, section-57CR, section-57CS, section-57CT, section-57CU, section-57CV, section-57CW, section-57CX, section-57CY, section-57CZ, section-57DA, section-57DB, section-57DC, section-57DD, section-57DE, section-57DF, section-57DG, section-57DH, section-58, section-59, section-60, section-61, section-63, section-64, section-66, section-67, schedule-2), civil-registration-act-2004 2020-09-04 (section-7, section-8A, section-13, section-23, section-28, section-30D, section-31, section-32, section-33, section-34, section-35, section-59B, section-59C, section-59E, section-59F, section-59G, section-59H, section-59I, schedule-2), wildlife-act-1976 2020-09-09 (section-2, section-44, section-61, section-68), roads-act-1993 2020-09-09 (section-2, section-17, section-51, section-51E, section-53, section-81, schedule-2), prisons-act-2007 2020-09-14 (section-20, section-32, section-35), european-arrest-warrant-act-2003 2020-09-15 (section-1, section-2, section-40, section-45, schedule-1), tourist-traffic-act-1957 2020-09-16 (section-7), tourist-traffic-act-1983 2020-09-16 (section-7), property-services-regulation-act-2011 2020-09-17 (long-title, section-1, section-2, section-7, section-18, section-30, section-31, section-34, section-35, section-36, section-41, section-43, section-48, section-62, section-64, section-65, section-74, section-83, section-84, section-85, section-98, section-101, schedule-3, schedule-4, schedule-5, schedule-6, schedule-7, schedule-8), health-act-1947 2020-09-21 (section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20, section-22, section-23, section-24, section-25, section-26, section-28, section-44, section-55, section-65, section-67, section-68, section-69, section-70, section-71, section-72, section-73, section-74, section-75, section-76, section-99, section-101, section-102, section-103, section-104), community-rural-and-gaeltacht-affairs-miscellaneous-provisions-act-2007 2020-09-23 (long-title), planning-and-development-act-2000 2020-09-24 (section-37J, section-42A, section-98, section-99, section-100, section-135, section-256, section-259, schedule-7), sea-fisheries-and-maritime-jurisdiction-act-2006 2020-09-24 (section-1, section-18, section-38, section-93, section-96, section-101, schedule-3), protected-disclosures-act-2014 2020-09-24 (schedule-4), residential-tenancies-act-2004 2020-09-29 (section-28, section-29, section-42, section-126), central-bank-and-credit-institutions-resolution-act-2011 2020-09-30 (section-10, section-20, section-42, section-49, section-66, section-69, section-74, section-82, section-89, section-110), road-traffic-act-1961 2020-10-01 (section-25, section-36, section-37, section-44, section-44A, section-45, section-46, section-49, section-50, section-51, section-83, section-86, section-89, section-90, section-101A, section-103, section-104, section-105, section-116, section-117, section-119, section-122), public-service-superannuation-miscellaneous-provisions-act-2004 2020-10-01 (long-title), road-traffic-act-2010 2020-10-01 (section-3, section-7, section-17, section-18, section-19, section-32, section-33, section-48, section-49, section-50, section-53, section-61, section-66, section-69, section-70, section-83, schedule-1), dog-breeding-establishments-act-2010 2020-10-01 (section-6), financial-emergency-measures-in-the-public-interest-act-2010 2020-10-01 (long-title, section-10), regulation-of-lobbying-act-2015 2020-10-01 (section-7), central-bank-reform-act-2010 2020-10-05 (long-title, section-14, section-15, section-16, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-62, section-63, section-64, section-66), forestry-act-2014 2020-10-07 (section-26), protection-of-employment-act-1977 2020-10-14 (section-11), unfair-dismissals-act-1977 2020-10-14 (section-2), protection-of-employees-employers-insolvency-act-1984 2020-10-14 (long-title, section-12), maternity-protection-act-1994 2020-10-14 (long-title, section-25), organisation-of-working-time-act-1997 2020-10-14 (section-2), employment-equality-act-1998 2020-10-14 (long-title, section-15, section-91), parental-leave-act-1998 2020-10-14 (long-title), national-minimum-wage-act-2000 2020-10-14 (long-title, section-21), equal-status-act-2000 2020-10-14 (section-17, section-18, section-25, section-41), carer-s-leave-act-2001 2020-10-14 (section-7), protection-of-employees-fixed-term-work-act-2003 2020-10-14 (section-14, section-15, section-16), disability-act-2005 2020-10-14 (long-title, section-43), protection-of-employment-exceptional-collective-redundancies-and-related-matters-act-2007 2020-10-14 (section-9), workplace-relations-act-2015 2020-10-14 (schedule-4), assisted-decision-making-capacity-act-2015 2020-10-14 (long-title, section-2, section-84, section-103), international-protection-act-2015 2020-10-14 (section-2, schedule-1), competition-act-2002 2020-10-15 (section-8, section-15E, section-23, section-25, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-39, section-40, section-41, section-42, section-43, section-44, section-45, section-46, section-47, section-47G, section-49), grangegorman-development-agency-act-2005 2020-10-21 (long-title), building-control-act-2007 2020-10-21 (section-5, section-58, section-61), qualifications-and-quality-assurance-education-and-training-act-2012 2020-10-21 (section-1, section-2, section-6, section-19, section-26, section-33, section-44, section-55, section-59, section-84), credit-union-and-co-operation-with-overseas-regulators-act-2012 2020-10-21 (section-26, section-27, section-39, section-57, section-65, section-69, schedule-1), further-education-and-training-act-2013 2020-10-21 (section-10, section-26, section-42), employment-permits-act-2006 2020-10-22 (section-1, section-3, section-7, section-10, section-15, section-16, section-20A, section-25, schedule-1, schedule-2), finance-local-property-tax-act-2012 2020-10-22 (section-2, section-26, section-41, section-62, section-63, section-65, section-73, section-78, section-80, section-81, section-90, section-91, section-96, section-99, section-103, section-114, section-129, section-133A, section-140, section-141, section-143, section-144, section-146, section-147), commissions-of-investigation-act-2004 2020-10-25 (section-19, section-40), freedom-of-information-act-2014 2020-10-27 (schedule-3, schedule-4), valuation-act-2001 2020-10-28 (section-56), nurses-and-midwives-act-2011 2020-10-28 (long-title, section-2, section-13, section-57, section-69, section-76), misuse-of-drugs-act-1977 2020-10-29 (section-10, schedule-1), health-act-1970 2020-11-01 (long-title, section-4, section-6, section-7, section-8, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20, section-21, section-22, section-24, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-41, section-42, section-67A, section-67D, section-69, section-73, section-78, section-80, section-83, schedule-1, schedule-4, schedule-5, schedule-6), electricity-regulation-act-1999 2020-11-02 (section-2, section-8A, section-9, section-9JD, section-10A, section-18, section-20, section-43, section-45, section-54, section-55, section-66), child-care-act-1991 2020-11-05 (section-10, section-44, section-45B, section-49, section-50, section-51, section-52, section-53, section-54, section-55, section-56, section-57, section-58), medical-practitioners-act-2007 2020-11-06 (section-2, section-17, section-35, section-44, section-46, section-72, section-75, section-86, section-89, section-96), road-traffic-act-2006 2020-11-09 (section-3, section-5, section-6, section-12, section-13, section-17, section-23), broadcasting-act-2009 2020-11-12 (section-2, section-9, section-26, section-27, section-28, section-38, section-43, section-50, section-52, section-62, section-74, section-77, section-94, section-140, section-141, section-145, section-154, section-156, section-166, section-176, section-179, section-182, section-185, schedule-1), civil-registration-act-2004 2020-11-20 (schedule-2, schedule-3), civil-registration-amendment-act-2014 2020-11-20 (section-6), data-protection-act-2018 2020-11-20 (schedule-1), road-traffic-act-1961 2020-11-30 (section-26), garda-s-och-na-act-2005 2020-12-08 (section-33A, section-33B, section-33C, section-33D, section-33G, section-33H, section-124), aviation-regulation-act-2001 2020-12-11 (section-2), fiscal-responsibility-act-2012 2020-12-16 (section-1, section-2, section-7), industrial-relations-act-1946 2020-12-18 (section-24, section-34, section-49), communications-regulation-act-2002 2020-12-18 (long-title, section-46A), legal-services-regulation-act-2015 2020-12-18 (section-121, section-157, section-189), animal-health-and-welfare-act-2013 2020-12-21 (section-2, section-9, section-15, section-52, section-55, section-58, section-74), road-transport-act-1986 2020-12-22 (section-6, section-8), credit-union-act-1997 2020-12-22 (section-76I, section-105, section-106), road-transport-act-2011 2020-12-22 (long-title), industrial-relations-act-1990 2020-12-23 (section-29, section-51, section-52, section-53, section-54, schedule-2, schedule-6), safety-health-and-welfare-at-work-act-2005 2020-12-23 (section-1, section-58, section-77), investment-funds-companies-and-miscellaneous-provisions-act-2005 2020-12-23 (section-22, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-39, section-40, section-41, section-42, section-43, section-44, section-45, section-46, section-47, section-48, section-49, section-50, section-51, section-52, section-53, section-54, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-62, section-63, section-64, section-65, section-66, section-67, section-68, section-69, section-70, section-71, section-72, section-73, section-74, section-87, schedule-1), road-traffic-act-2006 2020-12-23 (section-5, section-6, section-13, section-14, section-17, section-21), criminal-justice-money-laundering-and-terrorist-financing-act-2010 2020-12-28 (long-title, section-2, section-11, section-18, section-31, section-32, section-34, section-36, section-40, section-43, section-100, section-107, section-117, section-119), central-bank-act-1942 2020-12-29 (section-20), extradition-act-1965 2020-12-31 (section-7B, section-41, section-42, section-43, section-44, section-44B, section-44C, section-44D, section-45, section-46, section-47, section-48, section-49, section-50, section-51, section-52, section-53, section-54, section-55), protection-of-employees-employers-insolvency-act-1984 2020-12-31 (long-title, section-6, section-12), employment-permits-act-2006 2020-12-31 (section-20A), companies-act-2014 2020-12-31 (section-72, section-142, section-184, section-360, section-567, section-627, section-690A, section-804, section-905, section-964, section-1002, section-1110P, section-1173, section-1230, section-1234, section-1387, section-1388, section-1389, section-1503), customs-act-2015 2020-12-31 (schedule-1), electricity-regulation-act-1999 2021-01-01 (section-14B, section-40M, section-55, schedule-3, schedule-4), veterinary-practice-act-2005 2021-01-01 (section-96A, section-127), registration-of-deeds-and-title-act-2006 2021-01-01 (section-2, section-3, section-8, section-10, section-11, section-12, section-14, section-16, section-19, section-21, section-22, section-25, section-26, section-28, section-32, section-34, section-39, section-45, section-56, section-58, section-60, section-66, section-70, section-72, section-73, section-74), inland-fisheries-act-2010 2021-01-01 (long-title, section-4, section-8, section-26, section-77), value-added-tax-consolidation-act-2010 2021-01-01 (section-4, section-8, section-13, section-36, section-62A, section-64, section-87, schedule-4, schedule-7, schedule-8), personal-insolvency-act-2012 2021-01-01 (long-title, section-6, section-21A, section-27, section-31, section-34, section-35, section-36, section-41, section-49, section-54, section-55, section-57, section-62, section-64, section-72, section-77, section-91, section-95, section-99, section-101, section-102, section-107, section-108, section-109, section-114, section-128, section-129, section-139, section-157, section-164, section-166, section-176C, section-181, schedule-2), international-protection-act-2015 2021-01-01 (section-58, section-59), road-traffic-act-1961 2021-01-11 (section-3, section-26, section-101C), planning-and-development-act-2000 2021-01-15 (section-1A, section-2), roads-act-1993 2021-01-18 (section-53), immigration-act-2004 2021-01-28 (section-19), sea-fisheries-and-maritime-jurisdiction-act-2006 2021-01-28 (section-28, section-31), irish-collective-asset-management-vehicles-act-2015 2021-02-01 (section-34, section-77, section-107, section-117, section-189), child-care-act-1991 2021-02-03 (section-44), bail-act-1997 2021-02-10 (section-6), non-fatal-offences-against-the-person-act-1997 2021-02-10 (section-5, section-28), pharmacy-act-2007 2021-02-13 (section-10, section-21A, section-24A, section-25, section-64, section-65, section-75, section-77, schedule-1), national-treasury-management-agency-amendment-act-2014 2021-02-18 (schedule-1, schedule-2, schedule-4), criminal-justice-terrorist-offences-act-2005 2021-02-23 (section-56), investment-funds-companies-and-miscellaneous-provisions-act-2005 2021-03-01 (section-5, section-6, section-18B, section-18C, section-18D, section-18E, section-18F, section-18G, section-18H, section-18I, section-18J, section-18K, section-18L, section-18M, section-18N, section-18O, section-18P, section-18Q, section-18R, section-18S, section-18T, section-18U, section-87), companies-act-2014 2021-03-15 (section-1110P, section-1173, section-1230, section-1283, section-1387, section-1388, section-1389, section-1428A), foreshore-act-1933 2021-03-25 (section-13B, section-21B), european-arrest-warrant-act-2003 2021-03-30 (section-1), maritime-safety-act-2005 2021-03-30 (long-title, section-56, section-57, section-60), transfer-of-execution-of-sentences-act-2005 2021-03-30 (long-title), criminal-justice-act-2006 2021-03-30 (section-1, section-2, section-5, section-6, section-15, section-16, section-17, section-18, section-25, section-30, section-40, section-69, section-70, section-71, section-73, section-75, section-77, section-78, section-79, section-87, section-88, section-89, section-90, section-92, section-93, section-94, section-95, section-96, section-97, section-98, section-100, section-101, section-108, section-118, section-119, section-120, section-121, section-124, section-125, section-138, section-142, section-144, section-150, section-159, section-168, section-173, section-181, section-182, section-184, section-195), adoptive-leave-act-1995 2021-04-01 (section-11A, section-11B, section-11C, section-18, section-27, section-33), dumping-at-sea-act-1996 2021-04-01 (section-1, section-5A, schedule-1), child-and-family-agency-act-2013 2021-04-01 (long-title, section-14, section-63, schedule-2), children-and-family-relationships-act-2015 2021-04-01 (section-49, section-93, section-101, section-102, section-103, section-104, section-105, section-106, section-107, section-108, section-109, section-110, section-111, section-112, section-113, section-114, section-115, section-116, section-117, section-118, section-119, section-120, section-121, section-122, section-123, section-124, section-125, section-126, section-127, section-128, section-129, section-130, section-131, section-132, section-133, section-134), electricity-regulation-act-1999 2021-04-09 (section-9, section-13), criminal-justice-theft-and-fraud-offences-act-2001 2021-04-14 (section-22, section-43), road-traffic-act-1994 2021-04-15 (section-5, section-6, section-7, section-8, section-10, section-11, section-14, section-15, section-16, section-17, section-26, section-42), housing-miscellaneous-provisions-act-2009 2021-04-19 (long-title, section-1, section-2, section-6, section-32, section-33, section-43, section-46, section-47, section-62, section-64, section-69, section-70, section-74, section-75, section-83, section-87, section-91, section-92, section-94, section-98, section-99), credit-guarantee-act-2012 2021-04-22 (section-1, section-3, section-4, section-5, section-6, section-7, section-8, section-9, section-10, section-12), central-bank-act-1942 2021-04-23 (schedule-5, schedule-6, schedule-7), central-bank-supervision-and-enforcement-act-2013 2021-04-23 (section-37, section-49, section-64, section-73, schedule-5), personal-injuries-assessment-board-act-2003 2021-04-24 (long-title, section-4, section-17, section-38), civil-liability-and-courts-act-2004 2021-04-24 (long-title), judicial-council-act-2019 2021-04-24 (section-40, section-80), merchant-shipping-act-1894 2021-04-30 (section-2, section-4, section-39, section-55, section-59, section-63, section-68, section-89, section-93, section-127, section-211, section-239, section-259, section-268, section-285, section-287, section-291, section-295, section-301, section-303, section-314, section-376, section-390, section-427, section-446, section-492, section-535, section-547, section-586, section-599, section-652, section-723, section-731, section-739, section-742, schedule-19), planning-and-development-act-2000 2021-04-30 (section-11, section-31AL, section-37L, section-177AE, schedule-7), health-act-1970 2021-05-10 (section-59, section-67A, section-75D), valuation-act-2001 2021-05-17 (section-56), international-criminal-court-act-2006 2021-05-17 (long-title, section-2, section-4, section-6, section-7, section-8, section-9, section-11, section-12, section-13, section-15, section-19, section-20, section-21, section-22, section-24, section-25, section-26, section-27, section-29, section-31, section-32, section-33, section-34, section-37, section-38, section-40, section-41, section-42, section-44, section-45, section-50, section-51, section-52, section-53, section-54, section-55, section-56, section-59, section-61, section-63, schedule-1, schedule-2, schedule-3), protection-of-young-persons-employment-act-1996 2021-05-18 (schedule-2), companies-act-2014 2021-05-18 (section-72, section-142, section-184), railway-safety-act-2005 2021-05-19 (section-9A, section-10A, section-14, section-28A, section-45, section-50A, schedule-1, schedule-2), consumer-protection-act-2007 2021-05-20 (section-2, section-90), finance-local-property-tax-act-2012 2021-06-10 (section-2, section-20, section-72, section-129), road-traffic-act-1961 2021-06-24 (section-101C), wildlife-act-1976 2021-06-24 (section-2), education-miscellaneous-provisions-act-2007 2021-06-24 (long-title, section-7), medical-practitioners-act-2007 2021-06-24 (section-89), personal-insolvency-act-2012 2021-06-25 (section-176C), building-control-act-1990 2021-07-01 (section-6), building-control-regulations-1997 2021-07-01 (regulation-39, schedule-5), public-service-pay-and-pensions-act-2017 2021-07-01 (section-25), financial-emergency-measures-in-the-public-interest-no-2-act-2009 2021-07-05 (section-2A, section-2B, section-7, schedule-1), residential-tenancies-amendment-act-2019 2021-07-09 (section-22), road-traffic-act-1968 2021-07-13 (schedule-1), value-added-tax-consolidation-act-2010 2021-07-19 (section-8, section-35, section-62A, section-64, section-87, section-91, section-108A, schedule-3, schedule-7, schedule-8), health-and-social-care-professionals-act-2005 2021-07-21 (section-99), standards-in-public-office-act-2001 2021-07-22 (section-20, section-22, section-25), private-security-services-act-2004 2021-07-22 (schedule-3), ministers-and-secretaries-amendment-act-2011 2021-07-22 (section-22, section-23), finance-local-property-tax-act-2012 2021-07-22 (section-5, section-10B, section-17, section-72), customs-act-2015 2021-07-22 (section-2, section-12B), health-act-1947 2021-07-26 (section-31AA), criminal-justice-terrorist-offences-act-2005 2021-07-26 (section-56), proceeds-of-crime-act-1996 2021-07-28 (section-1, section-1A, section-1B, section-1C, section-4A, section-16A, section-16B, section-18), industrial-relations-act-1946 2021-07-29 (section-35), protection-of-employees-employers-insolvency-act-1984 2021-07-29 (section-6, section-12), workplace-relations-act-2015 2021-07-29 (section-12), criminal-law-sexual-offences-act-2017 2021-07-30 (section-38), criminal-justice-victims-of-crime-act-2017 2021-07-30 (section-12), pharmacy-act-2007 2021-08-01 (section-78), central-bank-act-1942 2021-08-03 (schedule-5, schedule-6, schedule-7), criminal-justice-theft-and-fraud-offences-act-2001 2021-08-03 (section-40), criminal-justice-act-2011 2021-08-03 (long-title, section-3, section-16, section-20, section-21), residential-tenancies-act-2004 2021-08-19 (section-47, section-48, section-198, schedule-3), valuation-act-2001 2021-09-01 (section-56, schedule-4), civil-liability-act-1961 2021-09-03 (section-29), housing-miscellaneous-provisions-act-1997 2021-09-03 (section-3A), local-government-act-2001 2021-09-03 (section-2, section-13A, section-22, section-22A, section-28, section-31, section-32, section-35, section-39, section-40, section-41, section-42, section-43, section-50, section-66A, section-66B, section-66C, section-72, section-77, section-79, section-81, section-92, section-93, section-94, section-95, section-100, section-101, section-103A, section-120, section-121, section-126A, section-126B, section-126C, section-126G, section-126K, section-126L, section-127, section-128A, section-128B, section-128C, section-128F, section-129, section-129A, section-129B, section-129C, section-129E, section-129J, section-129K, section-129L, section-129N, section-129P, section-133, section-134A, section-136, section-142, section-143, section-144, section-145, section-147, section-149, section-149A, section-158, section-185, section-186, section-188, section-189, section-191, section-192, section-195, section-196, section-197, section-198, section-211A, section-211B, section-211D, section-211E, section-211F, section-231, section-237A, schedule-2, schedule-4, schedule-10, schedule-13, schedule-14A), land-and-conveyancing-law-reform-act-2009 2021-09-03 (long-title, section-36, section-80, section-81, section-103, section-113, section-129, schedule-1, schedule-2), planning-and-development-act-2000 2021-09-09 (section-11, section-20), planning-and-development-housing-and-residential-tenancies-act-2016 2021-09-09 (section-7, section-18, section-34, schedule-1), credit-union-and-co-operation-with-overseas-regulators-act-2012 2021-09-21 (section-26, section-27, section-56, section-59, section-66, section-69), valuation-act-2001 2021-09-29 (section-56), employment-permits-act-2006 2021-10-27 (section-38), central-bank-act-1942 2021-11-03 (section-33ANF, schedule-4, schedule-5, schedule-6, schedule-7), railway-safety-act-2005 2021-11-10 (section-2), safety-health-and-welfare-at-work-act-2005 2021-11-20 (section-2, section-30, section-31, section-56A, section-56I, schedule-6, schedule-7), sea-pollution-act-1991 2021-11-22 (section-13, section-13A, section-13B, section-39A), dumping-at-sea-act-1996 2021-11-22 (section-6), sea-pollution-amendment-act-1999 2021-11-22 (section-8), electricity-regulation-act-1999 2021-11-22 (section-44, section-55), criminal-justice-theft-and-fraud-offences-act-2001 2021-11-22 (section-21, section-39, section-42B, schedule-1), criminal-justice-illicit-traffic-by-sea-act-2003 2021-11-22 (section-19), maritime-security-act-2004 2021-11-22 (schedule-1), sea-pollution-hazardous-substances-compensation-act-2005 2021-11-22 (schedule-1, schedule-2), sea-pollution-miscellaneous-provisions-act-2006 2021-11-22 (section-1, section-4, section-5, section-9, section-12, section-13, section-14, section-15, section-16, section-17, schedule-1), inland-fisheries-act-2010 2021-11-22 (section-77, schedule-4), customs-act-2015 2021-11-22 (section-12B), land-and-conveyancing-law-reform-act-2009 2021-11-30 (section-80, section-81, schedule-3), central-bank-supervision-and-enforcement-act-2013 2021-12-07 (section-73), fisheries-amendment-act-1997 2021-12-08 (section-67A, section-67B), health-and-social-care-professionals-act-2005 2021-12-08 (section-3, section-98, section-99), pharmacy-act-2007 2021-12-08 (section-2, section-23A, section-66, section-67, section-77, section-78, section-79), criminal-justice-act-2007 2021-12-08 (section-41, section-46), nursing-homes-support-scheme-act-2009 2021-12-09 (section-26, section-34, section-38), european-stability-mechanism-act-2012 2021-12-09 (long-title, section-8), central-bank-act-1942 2021-12-13 (section-20, section-33AN, section-33ANC, section-33ANG, schedule-4, schedule-5, schedule-6, schedule-7), criminal-evidence-act-1992 2021-12-15 (section-2, section-12, section-14C, section-19A, section-20, schedule-1), child-and-family-agency-act-2013 2021-12-15 (section-92), freedom-of-information-act-2014 2021-12-15 (schedule-1, schedule-3, schedule-4, schedule-5), companies-act-2014 2021-12-15 (section-27, section-72, section-117, section-142, section-174A, section-184, section-275, section-277, section-277A, section-280A, section-280B, section-280C, section-280D, section-280E, section-280F, section-280G, section-293, section-299, section-300, section-305, section-305A, section-306, section-324, section-360, section-363, section-364, section-503, section-534, section-567, section-633, section-804, section-900, section-905, section-930B, section-930C, section-931, section-931A, section-931B, section-933, section-933A, section-934, section-934E, section-935, section-936A, section-936B, section-942A, section-957A, section-957AA, section-957E, section-1002, section-1087D, section-1087E, section-1087F, section-1087G, section-1087H, section-1102A, section-1110C, section-1110D, section-1110F, section-1110K, section-1110M, section-1110N, section-1116A, section-1123, section-1129, section-1205, section-1230, section-1274, section-1283, section-1300, section-1361, section-1364, section-1365, section-1368, section-1400A, section-1401A, section-1428A, section-1448, section-1450, section-1451, section-1453, section-1458, section-1459, section-1460, section-1461, section-1472, section-1484, section-1485, section-1502, section-1515, section-1516, section-1522, section-1523, section-1526, section-1534, section-1551, section-1553, section-1561, section-1573, section-1577, schedule-2, schedule-3, schedule-18), registration-of-deeds-and-title-act-2006 2021-12-16 (section-3, section-32), planning-and-development-act-2000 2021-12-17 (section-3A, section-9A, section-37L, section-97, section-214), planning-and-development-housing-and-residential-tenancies-act-2016 2021-12-17 (section-25A), planning-and-development-amendment-act-2018 2021-12-17 (section-4, section-42, schedule-2, schedule-3, schedule-4), teaching-council-act-2001 2021-12-21 (section-2), registration-of-title-act-1964 2021-12-23 (section-3, section-4, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-17, section-27, section-28, section-33, section-99, section-101, section-104, section-109, section-110, section-111, section-112, section-113, section-114, section-123, schedule-1), foreshore-amendment-act-1992 2021-12-23 (section-1, section-5), firearms-act-1925 2021-12-27 (section-1, section-2), firearms-act-1964 2021-12-27 (section-2, section-10, section-12), misuse-of-drugs-act-1977 2021-12-27 (section-1, section-5, section-15A, section-15B, section-15C, section-24, section-26, section-28), firearms-and-offensive-weapons-act-1990 2021-12-27 (long-title, section-4, section-16A), criminal-justice-act-2007 2021-12-27 (section-26A, section-27, section-41, section-46, section-50), criminal-law-act-1997 2021-12-31 (section-7, section-8, schedule-3), investment-of-the-national-pensions-reserve-fund-and-miscellaneous-provisions-act-2009 2021-12-31 (long-title, section-9), credit-institutions-stabilisation-act-2010 2021-12-31 (long-title, section-1, section-28, section-77), road-safety-authority-commercial-vehicle-roadworthiness-act-2012 2021-12-31 (section-16, section-39, section-41, section-43, section-53), water-services-no-2-act-2013 2021-12-31 (section-2), national-treasury-management-agency-amendment-act-2014 2021-12-31 (section-8, section-49A), national-oil-reserves-agency-act-2007 2022-01-01 (section-2, section-8, section-14, section-15, section-16, section-18, section-21, section-30, section-34, section-36, section-38, section-44, section-44A, section-44B, section-44D, section-44E, section-44G, section-44I, section-44J, section-44K, section-44L, section-44N, section-44O, section-44P, section-44T, section-44W, section-50), inland-fisheries-act-2010 2022-01-01 (section-77), value-added-tax-consolidation-act-2010 2022-01-01 (section-62, section-64, section-77A, section-91A, section-92, section-95, section-96, section-108A, schedule-7, schedule-8), health-act-1970 2022-01-07 (section-59, section-75A), health-act-1947 2022-01-08 (section-31AA, section-31AL, section-31B, section-54), garda-s-och-na-act-2005 2022-01-11 (section-3A, section-3B, section-20, section-20A, section-28A, section-33, section-33A, section-33B, section-33C, section-33D, section-33G, section-33H, section-42, section-62S, section-81A, section-96), personal-insolvency-act-2012 2022-01-14 (section-2), criminal-justice-mutual-assistance-act-2008 2022-02-01 (section-8, section-9, section-12, section-22, section-55, section-60A, section-102, schedule-5A, schedule-5B, schedule-7B, schedule-8, schedule-9, schedule-10, schedule-13, schedule-14), road-traffic-act-2010 2022-02-01 (section-65), water-services-act-2014 2022-02-01 (section-3, section-5A), central-bank-act-1942 2022-02-03 (section-18A, section-33ANG, section-33AR), health-act-1947 2022-02-07 (section-31A), organisation-of-working-time-act-1997 2022-02-07 (section-2, section-8, section-18, section-23, section-26, section-29, section-30, section-31, section-38, section-41), merchant-shipping-safety-convention-act-1952 2022-02-08 (section-3, section-10, section-15, section-20), waste-management-act-1996 2022-02-09 (section-2, section-5, section-10, section-27B, section-40, section-42, section-49), electricity-regulation-act-1999 2022-02-15 (section-13, schedule-1A, schedule-3), housing-miscellaneous-provisions-act-1979 2022-02-24 (section-3, section-8, section-9, section-10, section-12, section-13, section-15, section-16, section-17, section-19, section-20), immigration-act-2004 2022-02-25 (section-11, section-17A), criminal-procedure-act-1967 2022-02-28 (section-5, section-6, section-7, section-8, section-9, section-10, section-11, section-12, section-14, section-15, section-16, section-17, section-18, section-24, section-27, section-30, section-33, section-37, schedule-1), criminal-justice-act-1984 2022-02-28 (section-3, section-4, section-5B, section-8A, section-8H, section-18, section-19, section-19A), criminal-procedure-act-2010 2022-02-28 (section-7, section-10, section-12, section-14, section-18, section-25), road-traffic-act-1961 2022-03-01 (section-3, section-22, section-29, section-35, section-36, section-42, section-56, section-65, section-78A, section-85, section-101B, section-101C, section-101D), health-act-1970 2022-03-01 (section-45A, section-51, section-58C, section-61A, section-62A, section-67A, section-67C, section-75A), merchant-shipping-act-1992 2022-03-01 (section-17), student-support-act-2011 2022-03-09 (section-2), medical-practitioners-act-2007 2022-03-14 (section-89, section-110), extradition-act-1965 2022-03-30 (section-3, section-10, section-27), local-government-services-corporate-bodies-act-1971 2022-03-31 (section-3), health-identifiers-act-2014 2022-03-31 (section-2, section-14), consumer-protection-act-2007 2022-04-01 (section-2, section-24D, section-24G, section-63A, section-66A, section-86A), defence-act-1954 2022-04-04 (section-2, section-56, section-62, section-78, section-105, section-142A, section-161, section-169A, section-179D, section-180, section-184C, section-184K, section-184LA, section-192, section-202, section-203, section-203B, section-209, section-210, section-211A, section-212A, section-213, section-215, section-216, section-217, section-218, section-219, section-220, section-223, section-224, section-225, section-227, section-228, section-240, section-240A, section-295, section-296, section-302, section-309, section-315, section-316), defence-amendment-no-2-act-1960 2022-04-04 (section-3, section-5, section-6), residential-tenancies-act-2004 2022-04-04 (section-4, section-32, section-35A, section-42, section-47, section-48, section-148R), central-bank-reform-act-2010 2022-04-04 (long-title, section-3, section-18, section-54, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-62, section-63, section-64, section-65, section-66), personal-injuries-assessment-board-act-2003 2022-04-11 (section-4, section-13, section-51A, section-79, section-86), health-act-2007 2022-04-12 (section-2, section-9, section-69, section-103), redundancy-payments-act-1967 2022-04-19 (section-1, section-2, section-12A, section-29, section-39A, schedule-1), child-care-act-1991 2022-04-27 (section-2, section-23A, section-23C, section-23D, section-23J, section-23N, section-23NL, section-23O, section-25, section-26, section-29, section-30, section-31, section-37, section-43A, section-45A, section-45B, section-45C, section-45D, section-58A, section-58C, section-59), irish-aviation-authority-act-1993 2022-05-01 (section-2, section-42, section-42A, section-45A, section-57B, section-69, section-72, section-74), firearms-act-1925 2022-05-04 (section-3D, section-14, section-27B), nurses-and-midwives-act-2011 2022-05-09 (section-2, section-52, section-52A, section-63A, section-68A, section-69, section-103A, section-108), personal-insolvency-act-2012 2022-05-10 (section-6, section-22, section-27, section-49B, section-49C, section-54A, section-115A, section-119, section-119A, section-136, section-159), wildlife-act-1976 2022-05-16 (section-39), consumer-credit-act-1995 2022-05-16 (long-title, section-8G, section-22, section-49, section-60, section-85, section-86, section-92, section-115, section-116, section-116A, section-142, section-149, section-149A, section-151B, section-153, schedule-1, schedule-3, schedule-4, schedule-5), central-bank-act-1997 2022-05-16 (section-14, section-24, section-44, section-67), financial-services-and-pensions-ombudsman-act-2017 2022-05-16 (section-63), employment-equality-act-1998 2022-05-31 (section-2, section-6, section-12, section-15, section-18, section-19, section-23, section-34, section-38, section-39, section-40, section-41, section-42, section-43, section-44, section-45, section-46, section-47, section-48, section-49, section-50, section-51, section-52, section-53, section-54, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-62, section-63, section-64, section-65, section-66, section-67, section-68, section-69, section-70, section-71, section-72, section-73, section-74, section-75, section-77, section-79, section-82, section-83, section-85A, section-91, section-92, section-101, section-106), medical-practitioners-act-2007 2022-06-01 (section-2, section-59, section-111), emergency-measures-in-the-public-interest-covid-19-act-2020 2022-06-02 (long-title, section-5, section-28), planning-and-development-act-2000 2022-06-23 (section-1A, section-10, section-11A, section-11B, section-11C, section-12, section-13, section-20, section-22A, section-24, section-31I, section-31K, section-31S, section-31T, section-31AH, section-31AV, section-31AW, section-34, section-34A, section-34C, section-35, section-37A, section-37B, section-37R, section-42B, section-49, section-50, section-50B, section-84, section-93, section-96B, section-97, section-143, section-146, section-146A, section-146B, section-146C, section-160, section-171, section-172, section-173C, section-176A, section-176C, section-177K, section-177R, section-177U, section-180, section-181, section-181A, section-181C, section-182A, section-182C, section-212, section-214, section-217, section-219, section-251A, section-254, section-255, section-261A, section-268A), criminal-justice-surveillance-act-2009 2022-06-29 (section-1, section-3, section-8, section-13, section-15), forestry-act-2014 2022-06-29 (section-8, section-30, section-31), veterinary-practice-act-2005 2022-07-01 (section-2, section-34, section-54A, section-54B, section-59A, section-76, section-78, section-91, section-95A, section-105, section-126, section-127, schedule-3), value-added-tax-consolidation-act-2010 2022-07-01 (section-2, section-16, section-32A, section-33, section-43A, section-53A, section-58, section-59, section-61, section-62, section-62A, section-64, section-77A, section-84, section-86A, section-91A, section-91B, section-91C, section-91D, section-91E, section-91I, section-91J, section-91K, section-108C, section-109A, section-116A, schedule-1, schedule-3), central-bank-supervision-and-enforcement-act-2013 2022-07-01 (section-7, section-59, section-81), paternity-leave-and-benefit-act-2016 2022-07-01 (section-15), parent-s-leave-and-benefit-act-2019 2022-07-01 (section-2, section-29), defence-act-1954 2022-07-06 (section-62, section-78, section-87, section-161, section-209, section-210, section-309, schedule-5), courts-martial-appeals-act-1983 2022-07-06 (section-3A, section-19B, section-23A, section-27, section-27A, section-28), irish-collective-asset-management-vehicles-act-2015 2022-07-06 (section-2A, section-32, section-37, section-38, section-75, section-116, section-117, section-148, section-149, section-150, section-153, section-189), data-protection-act-1988 2022-07-12 (section-1, section-2, section-2B, section-11, section-12A, section-24), finance-local-property-tax-act-2012 2022-07-18 (section-2A, section-10D, section-11, section-62, section-63, section-64, section-72, section-79, section-130, section-140, section-143, section-157), national-vetting-bureau-children-and-vulnerable-persons-act-2012 2022-07-19 (section-14A), criminal-justice-terrorist-offences-act-2005 2022-07-21 (section-4, section-4C, section-7, section-51, section-56, section-61, section-62, section-63, section-64, section-65, section-66, section-67), coroners-act-1962 2022-07-22 (section-2, section-11B, section-14, section-16A, section-18A, section-60), immigration-act-2004 2022-07-22 (section-12), valuation-act-2001 2022-07-24 (section-17, section-19, section-28, section-56, section-71, schedule-2, schedule-4, schedule-5), education-act-1998 2022-07-25 (section-24, section-32, section-53, section-60, section-62, section-63), residential-tenancies-act-2004 2022-07-26 (section-19A, section-19B, section-20, section-20A, section-22A, section-24A, section-24B, section-24BA, section-24C, section-25, section-33A, section-49, section-64A, section-66, section-95), organisation-of-working-time-act-1997 2022-07-27 (section-39), companies-act-2014 2022-07-27 (section-142, section-517, section-627, section-934, section-935A, section-935B, section-935D, section-936, section-1000, section-1002, section-1123, section-1129, section-1282, section-1283, section-1502), electricity-regulation-act-1999 2022-07-31 (section-44, section-55, schedule-3), guardianship-of-infants-act-1964 2022-08-01 (section-2, section-6, section-6E, section-6F, section-7, section-13, section-15, section-18D, section-19, section-20, section-21, section-23, section-31), judicial-separation-and-family-law-reform-act-1989 2022-08-01 (section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20, section-21, section-22, section-23, section-24, section-26, section-27, section-28, section-29, section-39, section-40), family-law-act-1995 2022-08-01 (section-2, section-12, section-15A, section-25, section-38, section-43), family-law-divorce-act-1996 2022-08-01 (section-2, section-17, section-31, section-32, section-33, section-34, section-35, section-36), dublin-transport-authority-act-2008 2022-08-01 (section-2, section-44, section-44A, section-56A, section-56C, section-56D, section-58, section-95), employment-permits-act-2006 2022-08-03 (section-1, section-1A, section-2, section-3D, section-7, section-10, section-14, section-38, schedule-1, schedule-2), building-control-act-2007 2022-08-29 (section-14), childcare-support-act-2018 2022-08-29 (section-1), central-bank-act-1942 2022-08-31 (section-2A, section-5, section-6B, section-6C, section-6E, section-6F, section-6K, section-18BA, section-18E, section-20, section-22, section-23, section-33, section-33A, section-33B, section-33C, section-33D, section-33E, section-33F, section-33G, section-33H, section-33I, section-33J, section-33K, section-33L, section-33M, section-33N, section-33O, section-33P, section-33Q, section-33R, section-33S, section-33SA, section-33T, section-33U, section-33V, section-33W, section-33AG, section-33AI, section-33AJ, section-33AN, section-33ANE, section-33AO, section-33AQ, section-57A, section-57C, section-57U, section-57AH, section-57AO, section-61B, section-61H, schedule-5, schedule-6, schedule-7), communications-regulation-act-2002 2022-09-06 (section-24B, section-30, section-39, section-45, section-46, section-46A, section-58A, section-58H), industrial-relations-act-1946 2022-09-15 (section-10, section-25, section-28, section-42A, section-58), animal-health-and-welfare-act-2013 2022-09-19 (section-11, schedule-4), central-bank-and-credit-institutions-resolution-act-2011 2022-09-20 (section-2, section-75, section-89, schedule-2), road-safety-authority-commercial-vehicle-roadworthiness-act-2012 2022-09-20 (section-53), credit-union-and-co-operation-with-overseas-regulators-act-2012 2022-09-20 (section-66, section-69), health-act-1970 2022-09-21 (section-45, section-52, section-58A, section-58C, section-59, section-75A, section-81), child-care-act-1991 2022-09-21 (section-23F, section-36), health-and-social-care-professionals-act-2005 2022-09-22 (section-44A), wildlife-act-1976 2022-10-03 (section-7, section-11, section-13, section-23A, section-29, section-36, section-53B, section-76), civil-registration-act-2004 2022-10-03 (section-8A, section-19B, section-23, section-23B, section-30A, section-30C, section-31, section-32, section-33, section-34, section-35, section-37, section-37A, section-44B, section-44C, section-44E, section-45, section-51, section-59A, section-59B, section-59E, section-59F, section-59G, section-59H, section-59I, section-66, schedule-1, schedule-3), judicial-council-act-2019 2022-10-03 (section-99, section-100), national-minimum-wage-act-2000 2022-10-06 (section-8, section-11, section-12, section-13, section-27, section-28, section-30, section-31, section-32, section-33), official-languages-act-2003 2022-10-10 (section-2), electoral-amendment-act-2006 2022-10-13 (section-1), national-oil-reserves-agency-act-2007 2022-10-18 (section-31A, section-34, section-37A, section-43A, section-44X, section-59A), greyhound-industry-act-1958 2022-10-19 (section-51), road-traffic-act-1961 2022-10-27 (section-12, section-18, section-26, section-62, section-95), road-traffic-act-1994 2022-10-27 (section-2, section-9, section-36B), road-traffic-act-2010 2022-10-27 (section-3, section-31, section-44, section-65, schedule-1), residential-tenancies-act-2020 2022-10-29 (section-4), air-pollution-act-1987 2022-10-31 (section-12A), environmental-protection-agency-act-1992 2022-10-31 (section-3, section-3A, section-4, section-5, section-52, section-58, section-59, section-63, section-81A, section-85, section-86A, section-86B, section-90, section-91, section-94, section-95, section-99D, section-99I, section-113, schedule-1), private-security-services-act-2004 2022-11-01 (section-2, section-37), nursing-homes-support-scheme-act-2009 2022-11-01 (section-14F, section-14G, section-14H, section-14K, section-14M, section-36, section-41, section-45B), industrial-training-act-1967 2022-11-10 (section-8, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-21, section-24, section-25), regional-technical-colleges-act-1992 2022-11-10 (section-21B, section-23A, schedule-1), qualifications-and-quality-assurance-education-and-training-act-2012 2022-11-10 (section-13, section-14A, section-19, section-43A), credit-institutions-stabilisation-act-2010 2022-11-17 (section-2, section-5A, section-9A, section-14, section-14A, section-22, section-29A, section-34A, section-37), sale-of-goods-act-1893 2022-11-29 (section-58), sale-of-goods-and-supply-of-services-act-1980 2022-11-29 (section-2, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-39, section-50), package-holidays-and-travel-trade-act-1995 2022-11-29 (section-2, section-19, section-22, section-24, schedule-3), consumer-credit-act-1995 2022-11-29 (schedule-1, schedule-3), consumer-protection-act-2007 2022-11-29 (section-6, section-7, section-8, section-8A, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20, section-21, section-22, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-39, section-40, schedule-9), housing-act-1966 2022-12-01 (section-8, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20, section-21, section-22, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-37, section-39, section-42, section-43, section-44, section-48, section-51, section-52, section-53, section-54, section-55, section-56, section-59, section-60, section-62, section-70, section-85, section-87, section-88, section-106, section-110, section-114), payment-of-wages-act-1991 2022-12-01 (section-8, section-9), central-bank-act-1942 2022-12-05 (section-33ANG, schedule-5, schedule-6, schedule-7, schedule-10), air-navigation-and-transport-act-1975 2022-12-07 (schedule-1), credit-guarantee-act-2012 2022-12-08 (section-5, section-8), houses-of-the-oireachtas-inquiries-privileges-and-procedures-act-2013 2022-12-10 (section-26), immigration-act-2004 2022-12-14 (section-9A, section-18), value-added-tax-consolidation-act-2010 2022-12-15 (section-16, section-64, section-81, section-91A, section-92, section-95, section-96, section-108C, schedule-4, schedule-7, schedule-8), finance-tax-appeals-act-2015 2022-12-15 (section-34, section-35, section-37, section-38, section-39, section-40, section-42, schedule-2), terms-of-employment-information-act-1994 2022-12-16 (section-6A, section-6B, section-6C, section-14), protection-of-employees-fixed-term-work-act-2003 2022-12-16 (section-2), employment-permits-act-2006 2022-12-16 (section-20A, section-37), irish-human-rights-and-equality-commission-act-2014 2022-12-17 (section-10, section-13, section-53, schedule-3), foreshore-act-1933 2022-12-20 (section-1B, section-1D, section-2, section-3A, section-3B, section-3C, section-6, section-13AA, section-13B, section-16A, section-18A), planning-and-development-act-2000 2022-12-20 (section-1A, section-31AL, section-34, section-37D, section-37E, section-37Q, schedule-4, schedule-7), maternity-protection-act-1994 2022-12-21 (section-16, section-32, section-33, section-33A, section-34, section-35, section-36, section-37), local-government-act-2001 2022-12-21 (section-22, section-49, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-62, section-70, section-79, section-84, section-89, section-90, section-91, section-185, section-186, section-187, section-231, schedule-8), criminal-law-sexual-offences-act-2006 2022-12-22 (section-1), animal-health-and-welfare-act-2013 2022-12-22 (section-11, schedule-4), electricity-regulation-act-1999 2022-12-31 (schedule-2, schedule-3), national-treasury-management-agency-amendment-act-2014 2022-12-31 (section-7, section-8, section-12, section-14, section-42A, schedule-4), health-act-1970 2023-01-01 (section-75A), health-insurance-act-1994 2023-01-01 (section-7F, schedule-4), social-welfare-consolidated-contributions-and-insurability-regulations-1996 2023-01-01 (regulation-3, regulation-6, regulation-20G, regulation-23, regulation-27A, regulation-28, regulation-29, regulation-30, regulation-34, regulation-49, regulation-55, regulation-63D, regulation-70, regulation-72B, regulation-72C, regulation-78, regulation-83A, regulation-94), public-service-superannuation-miscellaneous-provisions-act-2004 2023-01-01 (section-1, section-3A, schedule-2), public-service-management-recruitment-and-appointments-act-2004 2023-01-01 (section-2, section-28, section-57A, section-58A), housing-miscellaneous-provisions-act-2009 2023-01-01 (section-20, section-31, section-43), financial-emergency-measures-in-the-public-interest-no-2-act-2009 2023-01-01 (section-2A, section-5), inland-fisheries-act-2010 2023-01-01 (section-2), financial-emergency-measures-in-the-public-interest-act-2010 2023-01-01 (section-1, section-2, section-3, section-6B, section-10), ministers-and-secretaries-amendment-act-2011 2023-01-01 (section-16A, section-17, section-17A, section-21, schedule-2, schedule-3), water-services-act-2013 2023-01-01 (section-12), taxi-regulation-act-2013 2023-01-01 (section-2, section-29, section-35, section-74, section-78), water-services-no-2-act-2013 2023-01-01 (section-23A, section-32A, section-34A), protected-disclosures-act-2014 2023-01-01 (schedule-4), freedom-of-information-act-2014 2023-01-01 (section-2, section-11, section-15, section-23, section-24, section-28, section-35, section-37, schedule-3, schedule-4, schedule-5), companies-act-2014 2023-01-01 (section-2, section-140, section-142, section-212, section-213, section-214, section-215, section-237, section-238, section-274, section-290, section-311, section-360, section-405, section-406, section-496, section-517, section-543, section-567, section-627, section-695, section-714, section-715, section-746, section-747, section-797, section-957I, section-964, section-965, section-1002, section-1004, section-1110F, section-1110L, section-1122A, section-1159, section-1173, section-1230, section-1283, section-1305, section-1348, section-1366, section-1367, section-1387, section-1388, section-1389, section-1390, section-1463, section-1464, section-1493, section-1494, section-1502, section-1503, section-1567, section-1568, section-1572, section-1573, section-1577, schedule-2, schedule-3, schedule-4, schedule-5, schedule-7, schedule-8, schedule-10, schedule-12, schedule-14, schedule-15, schedule-16, schedule-17, schedule-18), workplace-relations-act-2015 2023-01-01 (section-2, section-3, section-28, section-31, section-84, schedule-2), ombudsman-defence-forces-act-2004 2023-01-09 (section-8), social-welfare-and-pensions-act-2005 2023-01-09 (section-1, section-6, section-15, schedule-1, schedule-2, schedule-3, schedule-4, schedule-5), development-banks-act-2005 2023-01-09 (section-4, section-6), national-economic-and-social-development-office-act-2006 2023-01-09 (section-2, section-7, section-8, section-10, section-11, section-13, section-14, section-15, section-16, section-17, section-18, section-22, section-26, section-30, section-35, section-42), energy-miscellaneous-provisions-act-2006 2023-01-09 (long-title, section-1, section-3, section-4, section-6, section-10, section-13, section-14, section-16, section-17, section-18, section-22, section-23, section-24, section-25, section-27, section-28, section-30), social-welfare-and-pensions-act-2007 2023-01-09 (section-1, section-9, section-25, schedule-1), social-welfare-and-pensions-act-2008 2023-01-09 (section-12, section-27, section-29, schedule-1, schedule-2), electoral-amendment-act-2009 2023-01-09 (section-1, section-6, section-7, section-8, section-9, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20), social-welfare-and-pensions-act-2009 2023-01-09 (long-title, section-12, section-13, section-15, section-22), local-government-charges-act-2009 2023-01-09 (section-2, section-8A, section-8B, section-10), petroleum-exploration-and-extraction-safety-act-2010 2023-01-09 (section-3), social-welfare-and-pensions-act-2010 2023-01-09 (section-1, section-11, section-26, section-29, section-42, section-45, schedule-2, schedule-3), local-government-household-charge-act-2011 2023-01-09 (section-13), vehicle-clamping-act-2015 2023-01-09 (section-6, section-7), planning-and-development-act-2000 2023-01-10 (section-97), central-bank-supervision-and-enforcement-act-2013 2023-01-23 (section-59, section-81), affordable-housing-act-2021 2023-01-27 (section-17), financial-services-and-pensions-ombudsman-act-2017 2023-02-01 (section-62, section-63, schedule-1), criminal-justice-money-laundering-and-terrorist-financing-act-2010 2023-02-02 (section-2, section-6, section-26, section-30A, section-30B, section-33A, section-34A, section-36A, section-38, section-38A, section-40B, section-40C, section-40D, section-54, section-57A, section-59, section-63A, section-63B, section-63C, section-63D, section-63E, section-84, section-101A, section-106A, section-106B, section-106C, section-106D, section-106E, section-106F, section-106G, section-106H, section-106I, section-106J, section-106K, section-106L, section-106M, section-106N, section-106O, section-106P, section-106Q, section-106R, section-106S, section-106T, section-106U, section-106V, section-106W, section-106X, section-106Y, section-106Z, section-106ZA, section-106ZB, section-106ZC, section-106ZD, section-107A, section-108A, section-108B, section-108C, section-108D, section-108E, section-108F, section-108G, section-108H, section-108I, section-109A, section-109B, section-109C, section-109D, section-109E, section-114A), public-service-pay-and-pensions-act-2017 2023-02-02 (section-25, section-28, section-29), criminal-justice-terrorist-offences-act-2005 2023-02-08 (section-51), sea-fisheries-and-maritime-jurisdiction-act-2006 2023-02-08 (section-6, section-17A, section-31), consumer-protection-act-2007 2023-02-09 (section-63A, section-63B, section-63C, section-63D, section-63E, section-86A, schedule-2, schedule-3, schedule-5, schedule-9), electricity-regulation-act-1999 2023-02-20 (section-9, section-9M, section-9O, section-13, section-13L, section-36, section-40H, schedule-2), registration-of-title-act-1964 2023-03-01 (section-104), housing-miscellaneous-provisions-act-1992 2023-03-01 (section-2, section-18), ethics-in-public-office-act-1995 2023-03-01 (section-21), standards-in-public-office-act-2001 2023-03-01 (section-1, section-22), education-for-persons-with-special-educational-needs-act-2004 2023-03-01 (long-title), health-act-2004 2023-03-01 (section-4, section-16Q, section-21E, section-26, section-40A, section-40HA, section-50, section-51, section-52, section-55A, section-55G, section-55H, section-55Q, section-81, schedule-5, schedule-6, schedule-7), local-government-act-2001 2023-03-08 (section-31, section-32, section-126D, section-128F, section-145, section-147, section-189, section-190, schedule-5, schedule-10), planning-and-development-act-2000 2023-03-10 (section-37D, section-37E, section-97, section-177AC, schedule-7), residential-tenancies-amendment-act-2015 2023-03-15 (section-4, section-36, section-60, section-63, section-64), valuation-act-2001 2023-03-24 (schedule-4), health-insurance-act-1994 2023-04-01 (section-2, section-2A, section-6A, section-7A, section-7B, section-7E, section-7F, section-12A, section-12B, section-13, section-17, section-18A, section-18F, section-18G), national-oil-reserves-agency-act-2007 2023-04-01 (section-37A, section-37B), adoption-act-2010 2023-04-04 (section-3, section-12, section-17, section-19, section-23, section-30, section-45, section-58A, section-63A, section-91A, section-91B, section-91C, section-91D, section-144, section-152A), criminal-justice-act-1984 2023-04-05 (section-4, section-8, section-8A, section-16), criminal-assets-bureau-act-1996 2023-04-10 (section-1, section-14, section-14C, section-23), personal-injuries-assessment-board-act-2003 2023-04-10 (long-title, section-18, section-62, section-68), garda-s-och-na-act-2005 2023-04-10 (section-16, section-33, section-96), health-act-1970 2023-04-17 (section-6, section-53, section-75A, section-81, schedule-5, schedule-6), environmental-protection-agency-act-1992 2023-04-18 (section-113), sea-pollution-act-1991 2023-04-19 (section-3), central-bank-act-1942 2023-04-20 (section-33V, section-33W, section-33AND, section-57A, section-57B, section-57C, section-57K, section-57L, section-57AD, section-57AI, section-57AJ, section-57AM, section-57AN, section-57AZ, section-57BB, section-57BH, section-57BO, section-57BW, section-57CJ, section-57CN, section-57CQ, section-57CV, section-57CW, section-57CZ, section-57DC, schedule-5, schedule-10), credit-union-act-1997 2023-04-26 (section-2, section-32, section-35, section-37E, section-45, section-46, section-48, section-56B, section-58, section-59, section-60, section-61, section-62, section-64, section-68, section-76B, section-76C, section-76D, section-76E, section-76G, section-76I, section-76J, section-76K, section-76L, section-78A, section-82A, section-83, section-85A, section-85B, section-93, section-129, section-134), mental-health-act-2001 2023-04-26 (section-9, section-15, section-25, section-71A), disability-act-2005 2023-04-26 (section-23, section-40, section-41), assisted-decision-making-capacity-act-2015 2023-04-26 (section-19, section-35, section-37, section-52), road-traffic-and-transport-act-2006 2023-04-27 (section-2), water-services-act-2007 2023-04-28 (section-5), industrial-relations-amendment-act-2015 2023-04-28 (section-24, section-28, section-29), irish-aviation-authority-act-1993 2023-05-01 (section-57B), aviation-regulation-act-2001 2023-05-01 (section-8A, section-8B, section-39A, section-45B), health-act-2007 2023-05-02 (section-1, section-103), children-act-2001 2023-05-03 (section-3, section-54, section-77, section-155, section-156A, section-156B, section-157, section-163, section-163A, section-184, section-187, section-188, section-189, section-215, section-218A, section-225, section-226, section-227, section-228, section-229, section-230, section-231, section-232, section-233, section-234, section-235, section-236, section-237, section-238, section-239, section-240, section-241, section-242, section-243, section-244), european-arrest-warrant-act-2003 2023-05-03 (section-12, section-21, section-22, section-23, section-31, section-45, schedule-1), criminal-justice-act-2007 2023-05-03 (section-27, section-41), criminal-justice-mutual-assistance-act-2008 2023-05-03 (section-51, section-51A, section-51B, section-51C, section-51D, section-51E, section-51F, section-51G, section-57A, section-60A, section-60B, section-60C, section-60D, section-60E, section-60F, section-60G, section-60H, section-60I, section-75A, section-76, section-78, section-79, section-79A, section-79B, section-79C, section-94, section-94A, section-94B, section-94C, section-94D, section-94E, section-95A, section-107, schedule-1, schedule-2, schedule-3, schedule-3A, schedule-5, schedule-6, schedule-7, schedule-7B, schedule-8, schedule-9, schedule-10, schedule-13, schedule-14), criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2023-05-03 (long-title, section-11, section-14, section-20, section-25, section-27, section-28, section-29, section-36, section-38, section-39, section-47, section-54, section-55, section-56, section-57, section-58, section-60, section-62, section-66, section-67, section-75, section-77, section-78, section-79, section-80, section-81, section-82, section-84, section-85, section-88, section-90, section-91, section-93, section-97, section-98, section-109, section-111, section-113, section-124, section-126, section-128, section-129, section-135, section-149, section-157, section-159, section-160, section-161, section-162, section-166, schedule-3, schedule-4), criminal-law-sexual-offences-act-2017 2023-05-03 (section-11, section-12, section-13, section-14, section-36), official-languages-act-2003 2023-05-05 (section-15, section-27), industrial-relations-act-1946 2023-05-11 (section-4, section-11, section-16, section-35, section-41, section-45A, section-45E, section-58, section-66, section-67, section-69, section-71, section-72), national-treasury-management-agency-amendment-act-2000 2023-05-11 (section-8A, section-8B), teaching-council-act-2001 2023-05-11 (section-24, section-41, section-42, section-43), criminal-justice-terrorist-offences-act-2005 2023-05-11 (schedule-5, schedule-6), maritime-area-planning-act-2021 2023-05-15 (section-4, section-171, schedule-9), road-safety-authority-commercial-vehicle-roadworthiness-act-2012 2023-05-16 (section-43, section-45), health-act-1947 2023-05-18 (section-2, section-9C, section-31A, section-31AB, section-31AF, section-31AG, section-31AH, section-31C, section-38A), safety-health-and-welfare-at-work-act-2005 2023-05-24 (section-1, section-28, section-29, section-56A, section-56B, section-56C, section-56D, section-56E, section-56F, section-56G, section-56H, section-56I), safety-health-and-welfare-at-work-general-application-regulations-2007 2023-05-24 (regulation-3, regulation-38, regulation-51, regulation-57, regulation-74, regulation-123, regulation-175, schedule-1, schedule-9, schedule-11, schedule-12), workplace-relations-act-2015 2023-05-24 (section-83, schedule-4, schedule-7), railway-safety-act-2005 2023-05-29 (long-title, section-10A, section-14, section-28A, section-38A, section-39A, section-39B, section-43A, section-43B, section-43C, section-46, section-46A, section-50A, section-52, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-61A, section-62, section-63, section-70), veterinary-practice-act-2005 2023-06-01 (section-43, section-80, section-96A, section-96B, section-126), nurses-and-midwives-act-2011 2023-06-01 (section-56A), animal-health-and-welfare-act-2013 2023-06-01 (section-36A, section-38A, section-71A, section-71B, section-71C, section-71D), communications-regulation-act-2002 2023-06-09 (section-11), companies-corporate-enforcement-authority-act-2021 2023-06-11 (section-10, schedule-2), sea-fisheries-and-maritime-jurisdiction-act-2006 2023-06-20 (section-26A, section-28, section-31), family-home-protection-act-1976 2023-06-22 (section-10), civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010 2023-06-22 (section-2, section-5A, section-52A, section-52B, section-67A, section-108A, section-109, section-109A, section-110, section-119, section-121, section-129, section-131A, section-141A, section-141B, section-173, section-187, section-196, section-196A), residential-tenancies-act-2004 2023-06-28 (section-3B, section-20, section-24A, section-66, section-77, section-148S, section-148T, section-148X, section-148Y), waste-management-act-1996 2023-07-01 (section-3, section-4, section-10, section-15, section-27A, section-31A, section-34A, section-34B, section-34D, section-37A, section-42, section-72, schedule-2, schedule-3, schedule-4, schedule-6, schedule-7), litter-pollution-act-1997 2023-07-01 (section-28), redundancy-payments-act-1967 2023-07-03 (section-7, section-12A, section-26, section-28, section-32A, section-33, section-34, section-40, section-50, schedule-1), unfair-dismissals-act-1977 2023-07-03 (section-1, section-2A, section-8, section-8A, section-9, section-10), maternity-protection-act-1994 2023-07-03 (section-8, section-14, section-14B, section-15B, section-16B), adoptive-leave-act-1995 2023-07-03 (section-6A, section-27, section-28, section-33), organisation-of-working-time-act-1997 2023-07-03 (section-39), parental-leave-act-1998 2023-07-03 (section-7, section-15A, section-22A), national-minimum-wage-act-2000 2023-07-03 (section-2, section-10A, section-10B, section-10C, section-10D, section-10E, section-14, section-15, section-16, section-22, section-26, section-29, section-34), adoption-act-2010 2023-07-03 (section-61, section-84), irish-human-rights-and-equality-commission-act-2014 2023-07-03 (long-title, section-6, section-33, section-36, section-42, section-49), companies-act-2014 2023-07-04 (section-140, section-275, section-567, section-627, section-644, section-755, section-852, section-1002, section-1110I, section-1197, section-1230, section-1281, section-1328, section-1373, section-1388, section-1389, section-1428A, schedule-3, schedule-4, schedule-6, schedule-7, schedule-8), arbitration-act-2010 2023-07-05 (section-2, section-7), central-bank-act-1942 2023-07-10 (section-33ANG), pharmacy-act-2007 2023-07-10 (long-title, section-16, section-21B, section-21C, section-23A, section-24B, section-77), nursing-homes-support-scheme-act-2009 2023-07-11 (section-3, section-14A, section-14B, section-14C, section-14D, section-14E, section-14F, section-14G, section-14H, section-14I, section-14J, section-14K, section-14L, section-14M, section-14N, section-24A, section-27A, section-45A, section-47A, section-49, schedule-1), foreshore-act-1933 2023-07-17 (section-1AA, section-1B, section-1C, section-3AA, section-3BA, section-3CA, section-13AA, section-13B, section-16B, section-19, section-19A, section-19B, section-19C, section-20, section-21A, section-21B), registration-of-title-act-1964 2023-07-17 (section-9, section-18, section-98, section-123), foreshore-amendment-act-1992 2023-07-17 (section-7), dublin-transport-authority-act-2008 2023-07-17 (long-title, section-44A, section-95), planning-and-development-amendment-act-2018 2023-07-17 (long-title, section-4, schedule-1, schedule-3, schedule-4), health-and-social-care-professionals-act-2005 2023-07-18 (long-title, section-3, section-9, section-27A, section-28A, section-38, section-40A, section-44A, section-45A, section-68, section-78A, section-81A, section-98, section-99, section-100, schedule-2, schedule-3, schedule-4), civil-defence-act-2012 2023-07-18 (section-18), national-treasury-management-agency-amendment-act-2014 2023-07-18 (section-49), criminal-justice-act-2006 2023-07-19 (section-2, section-17, section-30, section-54, section-70, section-71, section-71A, section-71B, section-72, section-72A, section-73, section-74, section-75, section-78, section-79, section-92), merchant-shipping-safety-convention-act-1952 2023-07-20 (section-18), protected-disclosures-act-2014 2023-07-22 (schedule-4), planning-and-development-act-2000 2023-07-24 (section-1A, section-2), gaming-and-lotteries-act-1956 2023-07-31 (section-9A, section-19A, section-22A, section-26, section-26A, section-27, section-27A, section-27B), irish-nationality-and-citizenship-act-1956 2023-07-31 (section-6, section-6A, section-27), civil-liability-act-1961 2023-07-31 (section-6, section-11, section-49, section-49A, section-51A, section-51C, section-51M, section-51N, section-51O), guardianship-of-infants-act-1964 2023-07-31 (section-7), bankruptcy-act-1988 2023-07-31 (section-8, section-18, section-47, section-60A, section-60B, section-60C, section-60D, section-65A, section-83, section-84, section-85, section-85B, section-140A, section-140B, section-140C, section-140D, section-141, section-142), road-traffic-act-2002 2023-07-31 (section-1, section-8), civil-liability-and-courts-act-2004 2023-07-31 (section-17, section-22, section-32A, section-32B, section-32C, section-32D, section-39, section-53A), road-traffic-act-2014 2023-07-31 (section-10), international-protection-act-2015 2023-07-31 (section-50A, section-51A, section-51B, section-51C, section-72A), data-protection-act-2018 2023-07-31 (schedule-1), firearms-act-1925 2023-08-01 (section-1), criminal-procedure-act-1993 2023-08-01 (section-6, section-11), prisons-act-2007 2023-08-01 (section-33, section-34), affordable-housing-act-2021 2023-08-01 (section-12, section-17), employment-equality-act-1998 2023-08-09 (section-15), maritime-area-planning-act-2021 2023-08-14 (section-116, section-171), health-act-1947 2023-08-17 (section-55), local-government-reform-act-2014 2023-08-21 (long-title, section-1, section-15, section-17, section-19, section-36, section-37, section-44, section-58, section-63, schedule-4), teaching-council-act-2001 2023-08-23 (section-30, section-31A, section-33, section-33A, section-33B, section-34, section-42, section-43, section-43A, section-43B, section-43C, section-46A, section-46B, section-60), universities-act-1997 2023-08-30 (section-16, section-23A), roads-act-1993 2023-08-31 (section-15B, section-15C, section-24, section-43, section-50, section-51A, section-51B, section-51C, section-51D, section-51E, section-51F, section-51G, section-54A, section-56, section-64, section-64A, section-70, section-82, section-82A), residential-tenancies-act-2004 2023-08-31 (section-66), health-act-1970 2023-09-01 (section-45A, section-47A, section-48A, section-51, section-53B, section-55, section-58A, section-58C, section-58D, section-59A, section-61A, section-62A, section-67A, section-67B, section-67C, section-67D, section-67E, section-74A, section-75A, section-75B, section-75C, section-75D, section-81), child-care-act-1991 2023-09-01 (section-10, section-20, section-23A, section-23B, section-23C, section-23D, section-23E, section-23F, section-23G, section-23H, section-23I, section-23J, section-23K, section-23L, section-23M, section-23N, section-23NA, section-23NB, section-23NC, section-23ND, section-23NE, section-23NF, section-23NG, section-23NH, section-23NI, section-23NJ, section-23NK, section-23NL, section-23NM, section-23NN, section-23NO, section-23NP, section-45, section-45A, section-45B, section-45C, section-45D, section-49, section-50, section-51, section-52, section-53, section-54, section-55, section-56, section-57, section-58, section-58A, section-58C, section-58D, section-58E, section-58F, section-58G, section-58H, section-58J, section-58K, section-58L, section-72), waste-management-act-1996 2023-09-01 (section-10), industrial-relations-act-1946 2023-09-04 (section-53), public-service-management-recruitment-and-appointments-act-2004 2023-09-04 (section-57E), employment-permits-act-2006 2023-09-04 (section-1, section-1A, section-2, section-3, section-3A, section-3B, section-3C, section-3D, section-3E, section-3F, section-4, section-5, section-6, section-7, section-9, section-10A, section-11, section-12, section-13, section-14A, section-15, section-16, section-17, section-18, section-19, section-20, section-20A, section-20B, section-20C, section-20D, section-21, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-39, section-40, section-41), data-protection-act-1988 2023-09-07 (section-1), immigration-act-2004 2023-09-12 (section-9A, section-9B, section-14, section-17A), road-traffic-act-1968 2023-09-13 (section-18, section-19, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-38, section-43, section-44, section-45, section-46, section-47, section-48, section-49, section-50, section-51, section-52, section-60, section-64), road-traffic-act-2006 2023-09-13 (section-3, section-16), waste-management-act-1996 2023-09-22 (section-60, section-76A, section-77), property-services-regulation-act-2011 2023-09-26 (section-2), competition-act-2002 2023-09-27 (section-14, section-14A, section-15A, section-15B, section-15D, section-16, section-17, section-23, section-28A, section-28B, section-28C, section-28D, section-28E, section-28F, section-28G, section-28H, section-28I, section-28J, section-28K, section-28L, section-28M, section-28N, section-28O, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-37, section-38, section-39, section-40, section-41, section-43, section-44, section-45, section-46, section-47, section-47A, section-47C, section-47D, section-47F, section-47G), national-treasury-management-agency-amendment-act-2014 2023-09-27 (section-49), competition-and-consumer-protection-act-2014 2023-09-27 (section-29, section-47, section-81), merchant-shipping-safety-convention-act-1952 2023-10-09 (section-15), defence-act-1954 2023-10-13 (section-12, section-17A, section-309), irish-nationality-and-citizenship-act-1956 2023-10-16 (section-16A), chemicals-act-2008 2023-10-26 (section-14, section-16), succession-act-1965 2023-11-01 (section-3, section-60, section-113A), criminal-justice-public-order-act-1994 2023-11-01 (section-4A, section-5, section-8A, section-8B, section-19A, section-23B), bail-act-1997 2023-11-01 (section-1, section-1A, section-2, section-2A, section-4, section-5, section-6A, section-9, section-11A), non-fatal-offences-against-the-person-act-1997 2023-11-01 (section-18, section-24A, section-28), criminal-justice-theft-and-fraud-offences-act-2001 2023-11-01 (section-32, section-38, section-38A, section-40, section-42A, section-42B, section-45, section-54A, schedule-1), criminal-justice-terrorist-offences-act-2005 2023-11-01 (schedule-3, schedule-5), criminal-law-insanity-act-2006 2023-11-01 (section-1, section-3, section-4, section-5, section-7, section-8, section-11, section-13, section-13A, section-13B, section-13C, section-16, schedule-2), criminal-justice-act-2006 2023-11-01 (section-127, section-148), criminal-justice-act-2007 2023-11-01 (section-41), criminal-procedure-act-2010 2023-11-01 (section-2, section-12, section-23), criminal-justice-act-2011 2023-11-01 (section-3), criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2023-11-01 (schedule-2, schedule-3, schedule-4), health-and-social-care-professionals-act-2005 2023-11-02 (section-27A, section-28A, section-36A, section-36B, section-53A, section-66, section-81A, section-81B, section-81C, section-81D, section-81E, section-91A, section-91B, section-91C, section-91D, section-91E, section-91F, section-91G, section-91H, section-91I, section-91J, section-98, section-99), sex-offenders-act-2001 2023-11-13 (section-21), wildlife-act-1976 2023-11-23 (section-35, section-51, section-53), central-bank-supervision-and-enforcement-act-2013 2023-11-28 (section-3, schedule-3), criminal-evidence-act-1992 2023-11-30 (section-14A, section-14AA, section-14B, section-18, section-19A), garda-s-och-na-act-2005 2023-12-05 (section-102, section-102A), credit-union-and-co-operation-with-overseas-regulators-act-2012 2023-12-06 (section-69), education-act-1998 2023-12-12 (section-23, section-24, section-29A, section-29B, section-29C, section-29D, section-29E, section-29F, section-37A, section-53, section-60, section-61, section-62, section-63, section-64, section-65, section-66, section-68, section-69, section-70), personal-injuries-assessment-board-act-2003 2023-12-14 (section-51A, section-51C, section-55), finance-tax-appeals-act-2015 2023-12-18 (section-9, section-12, section-26), road-traffic-act-1961 2023-12-23 (section-24, section-35A, section-44B), central-bank-act-1942 2023-12-30 (section-33ANG, schedule-5), central-bank-act-1997 2023-12-30 (section-24, section-25, section-34FA, section-36F, section-67), foreshore-act-1933 2023-12-31 (section-1, section-6, section-7, section-8, section-9, section-17), electricity-regulation-act-1999 2023-12-31 (section-4, section-7, section-8A, section-8B, section-9, section-9A, section-9BA, section-9BB, section-9BC, section-9BD, section-9C, section-9D, section-9E, section-9EA, section-9F, section-9G, section-9H, section-9JA, section-9JB, section-9JC, section-9JD, section-9JE, section-9JF, section-9JG, section-9L, section-9M, section-9N, section-9O, section-13B, section-13C, section-13D, section-13E, section-13F, section-13G, section-13GA, section-13H, section-13J, section-13K, section-13KA, section-13KB, section-13KC, section-13L, section-13M, section-13N, section-13O, section-13OA, section-13P, section-13Q, section-13R, section-13S, section-13T, section-13U, section-13V, section-13W, section-13X, section-13Y, section-13Z, section-13AA, section-13AB, section-13AC, section-13AD, section-14A, section-14B, section-27, section-28, section-34A, section-34B, section-36A, section-40A, section-40C, section-40D, section-40E, section-40F, section-40G, section-40H, section-40I, section-40J, section-40K, section-40L, section-40M, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-62, section-63, section-64, section-65, section-66, schedule-2, schedule-3), planning-and-development-act-2000 2023-12-31 (section-20, section-32A, section-32C, section-32D, section-32E, section-32F, section-32G, section-34A, section-34B, section-34C, section-37A, section-37B, section-37C, section-37D, section-37E, section-37F, section-37H, section-37J, section-37K, section-37Q, section-37R, section-37S, section-38, section-41, section-42, section-42B, section-44A, section-50, section-50A, section-50B, section-105A, section-107A, section-112A, section-126A, section-126B, section-128, section-134A, section-143, section-146A, section-146B, section-146C, section-146CA, section-146D, section-164A, section-170A, section-171, section-172A, section-172B, section-172C, section-173A, section-173B, section-173C, section-173D, section-175, section-176, section-176A, section-176B, section-176C, section-177G, section-177H, section-177J, section-177P, section-177Q, section-177R, section-177S, section-177T, section-177U, section-177V, section-177W, section-177X, section-177Y, section-177AA, section-177AB, section-177AC, section-177AD, section-177AE, section-178, section-178A, section-179A, section-181, section-181B, section-181C, section-182C, section-182E), maritime-area-planning-act-2021 2023-12-31 (section-4, section-171), waste-management-act-1996 2024-01-01 (section-73A, schedule-7), valuation-act-2001 2024-01-01 (section-26A, section-26B, section-26C, section-26D, section-26E, section-26F, section-26G, section-29A, section-30, section-31, section-32, section-33, section-34, section-37, section-40, section-56A, section-56B, section-56C, section-56D, section-56E, section-67A, section-67B, section-68, section-70, section-71), local-government-act-2001 2024-01-01 (section-26A, section-145, schedule-4, schedule-13), national-oil-reserves-agency-act-2007 2024-01-01 (section-43A, section-44GA, section-44N, section-44O, section-44P, section-44T, section-44W, section-68, section-69, section-70), central-bank-reform-act-2010 2024-01-08 (schedule-2), employment-permits-act-2006 2024-01-17 (section-20A), industrial-relations-act-1946 2024-01-23 (section-41A), criminal-justice-terrorist-offences-act-2005 2024-01-23 (section-51), value-added-tax-consolidation-act-2010 2024-02-01 (section-13, section-23A, section-30, section-32A, section-35A, section-43A, section-53A, section-62A, section-64, section-77A, section-81, section-86A, section-91F, section-91G, section-91H, section-91I, section-91J, section-91K, section-95, section-108A, section-108B, section-108C, section-108D, section-109A, section-114A, section-114B, section-116A, section-118, schedule-4, schedule-7, schedule-8), irish-aviation-authority-act-1993 2024-02-08 (section-44, section-58), broadcasting-act-2009 2024-02-17 (section-2B), garda-s-och-na-act-2005 2024-02-20 (section-16), health-act-2007 2024-02-28 (section-41A, section-77A, section-99, section-103), criminal-justice-money-laundering-and-terrorist-financing-act-2010 2024-02-28 (section-26, section-36, section-39, section-40CA, section-54, section-57, section-59), misuse-of-drugs-act-1977 2024-02-29 (section-6), criminal-justice-terrorist-offences-act-2005 2024-02-29 (section-51), irish-medicines-board-act-1995 2024-03-01 (section-24), roads-act-1993 2024-03-06 (section-13), waste-management-act-1996 2024-03-06 (section-2, section-5, schedule-7), litter-pollution-act-1997 2024-03-06 (section-12), building-control-regulations-1997 2024-03-06 (regulation-5, regulation-11), parental-leave-act-1998 2024-03-06 (section-13AA), workplace-relations-act-2015 2024-03-06 (section-83, schedule-2, schedule-7), international-protection-act-2015 2024-03-12 (section-78), health-act-1947 2024-03-25 (section-55), building-control-act-1990 2024-03-26 (section-1, section-6, section-7A, section-7B, section-12), competition-and-consumer-protection-act-2014 2024-03-27 (section-37A, section-81), water-services-act-2007 2024-03-29 (section-5), financial-services-and-pensions-ombudsman-act-2017 2024-03-29 (section-63), litter-pollution-act-1997 2024-03-31 (section-30), local-government-act-2001 2024-03-31 (section-5, section-134, section-136, section-189, section-190, section-191, section-192, section-193, section-194, schedule-10, schedule-13), electoral-amendment-act-2004 2024-03-31 (section-8, section-12, section-20), affordable-housing-act-2021 2024-03-31 (section-12, section-26, section-33, section-44), health-insurance-act-1994 2024-04-01 (section-6B, section-7AB, section-7F, section-11A, section-11B, section-11D, section-11E, section-11F, section-11G, section-18A, section-18C, section-18D, section-18E, section-18F, section-18G, section-21, section-33A, section-33B), credit-union-act-1997 2024-04-08 (section-54), european-arrest-warrant-act-2003 2024-05-01 (section-3), broadcasting-act-2009 2024-05-01 (section-46O), national-treasury-management-agency-amendment-act-2014 2024-05-07 (section-48), personal-injuries-assessment-board-act-2003 2024-05-08 (section-18F, section-55, section-68), maritime-area-planning-act-2021 2024-05-14 (section-171), criminal-justice-surveillance-act-2009 2024-05-15 (section-10), coroners-act-1962 2024-05-16 (section-2A, section-13A, section-16A, section-16B, section-18A, section-18B, section-27, section-33, section-33A, section-33B, section-33C, section-33D, section-33E, section-38A, section-53A, section-54, section-60, section-61, section-62), wildlife-act-1976 2024-05-16 (long-title, section-53B, section-72, section-74, section-74A, schedule-5), housing-act-1988 2024-05-16 (section-5, section-9, section-13, section-17, section-20, section-24, section-27, schedule-1), housing-traveller-accommodation-act-1998 2024-05-16 (long-title, section-17, section-28), local-government-act-2001 2024-05-16 (section-5), local-government-reform-act-2014 2024-05-16 (section-12, section-15, section-36, section-44, schedule-4), housing-miscellaneous-provisions-act-2014 2024-05-16 (section-26, section-27, section-28, section-29, section-46, section-53, section-54), affordable-housing-act-2021 2024-05-16 (section-26, section-33, section-44), planning-and-development-maritime-and-valuation-amendment-act-2022 2024-05-16 (section-14), planning-and-development-act-2000 2024-05-17 (section-1, section-1A, section-3A, section-9A, section-11D, section-20A, section-20B, section-20C, section-21, section-22, section-22A, section-23, section-24, section-25, section-25A, section-26, section-27, section-27A, section-27B, section-27C, section-27D, section-31, section-31A, section-31B, section-31C, section-31D, section-31E, section-31FF, section-31GG, section-31H, section-31J, section-31K, section-31L, section-31M, section-31N, section-31O, section-31P, section-31Q, section-31R, section-31S, section-31T, section-31U, section-31V, section-31W, section-31X, section-31Y, section-31Z, section-31AA, section-31AB, section-31AC, section-31AD, section-31AE, section-31AF, section-31AG, section-31AH, section-31AI, section-31AJ, section-31AK, section-31AL, section-31AM, section-31AN, section-31AO, section-31AP, section-31AQ, section-31AR, section-31AS, section-31AT, section-31AU, section-31AV, section-31AW, section-31AX, section-37Q, section-144, section-215A, section-215B, section-215C, section-217A, section-217B, section-217C, section-219, section-243, section-247, section-251A, section-261A, section-268A, section-270A, section-278, section-279, section-279A, section-280, section-281, section-282, section-283, section-284, section-285, section-286, section-287, section-287A, section-287B, section-287C, section-288, section-289, section-290, section-291, section-292, section-293, section-294, section-295, section-296, section-297, section-298, section-299, section-300, section-301, section-302, section-303, section-304, section-305, section-306, section-307, section-308, section-309, section-310, section-311, section-312, section-313, section-314, section-315, section-316, section-317, section-318, section-319, section-320, section-321), road-traffic-act-1961 2024-05-20 (section-26), employment-equality-act-1998 2024-05-31 (section-20A), road-traffic-act-2010 2024-05-31 (section-11, section-13A, section-13B, section-17, section-18, section-19, section-44, section-48, section-49A, section-57, section-66, section-69, section-70), gas-act-1976 2024-06-01 (section-8A, section-16, section-16A), freedom-of-information-act-2014 2024-06-01 (section-27, schedule-3, schedule-4, schedule-5), local-government-act-2001 2024-06-14 (section-145), road-traffic-act-1961 2024-06-25 (section-26, section-36), maritime-safety-act-2005 2024-06-26 (section-60), animal-health-and-welfare-act-2013 2024-06-28 (section-11, schedule-4), official-languages-act-2003 2024-06-30 (section-4A, section-4B, section-10A, section-34, section-35), industrial-relations-act-1946 2024-07-01 (section-53), protection-of-employment-act-1977 2024-07-01 (section-6, section-11B), irish-aviation-authority-act-1993 2024-07-01 (section-58), waste-management-act-1996 2024-07-01 (section-2, section-5, section-22), companies-act-2014 2024-07-01 (section-142, section-567, section-998A, section-1002, section-1110I, section-1122A, section-1230, section-1281), international-protection-act-2015 2024-07-03 (section-78), companies-act-2014 2024-07-06 (section-212, section-567, section-627, section-644, section-755), local-government-rates-and-other-matters-act-2019 2024-07-10 (section-21), national-treasury-management-agency-amendment-act-2014 2024-07-30 (section-48), road-traffic-act-1961 2024-08-09 (section-24), immigration-act-2003 2024-08-12 (section-7), judicial-council-act-2019 2024-08-12 (section-33), local-government-water-pollution-act-1977 2024-08-28 (section-10), microenterprise-loan-fund-act-2012 2024-08-28 (section-2), defence-act-1954 2024-08-31 (section-56, section-62, section-87, section-178B, section-178C, section-178D, section-178E, section-178F, section-178G, section-179, section-179A, section-179B, section-179C, section-179D, section-179E, section-179F, section-184, section-184A, section-184B, section-184C, section-184D, section-184E, section-184F, section-184G, section-184H, section-184I, section-184J, section-184K, section-184L, section-184LA, section-184M, section-184N, section-184O, section-184P, section-187A, section-189, section-190, section-191, section-193, section-194, section-195, section-197, section-197A, section-198, section-199, section-203, section-203A, section-203B, section-203C, section-203D, section-205A, section-209, section-210, section-211, section-211A, section-212A, section-212B, section-213, section-213A, section-225, section-226, section-240A, section-240B), criminal-law-rape-act-1981 2024-08-31 (section-3), local-government-act-2001 2024-09-01 (section-145), qualifications-and-quality-assurance-education-and-training-act-2012 2024-09-01 (section-43A), criminal-evidence-act-1992 2024-09-02 (schedule-1), employment-permits-act-2003 2024-09-02 (section-3, section-3B, section-4), public-service-superannuation-miscellaneous-provisions-act-2004 2024-09-02 (section-3A), employment-permits-act-2006 2024-09-02 (section-1, section-1A, section-2, section-3, section-3A, section-3B, section-3C, section-3D, section-3E, section-3F, section-4, section-5, section-6, section-8, section-9, section-10A, section-11, section-12, section-13, section-14, section-14A, section-15, section-16, section-17, section-18, section-19, section-20, section-20A, section-20B, section-20C, section-20D, section-21, section-22, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-39, section-40, section-41), workplace-relations-act-2015 2024-09-02 (section-83, schedule-4, schedule-7), garda-s-och-na-act-2005 2024-09-03 (schedule-5), sea-fisheries-and-maritime-jurisdiction-act-2006 2024-09-10 (section-10, section-13), civil-registration-act-2004 2024-09-16 (section-2A, section-2B, section-8A, section-19B, section-23, section-23A, section-23B, section-27A, section-30A, section-30B, section-30C, section-30D, section-30E, section-30F, section-30G, section-30H, section-30I, section-30J, section-30K, section-30L, section-37A, section-42A, section-44A, section-44B, section-44C, section-44D, section-44E, section-44G, section-44H, section-54, section-58A, section-59IA, section-59J, section-59K, section-59L, section-61), environmental-protection-agency-act-1992 2024-09-19 (section-82, section-98A, schedule-2), nursing-homes-support-scheme-act-2009 2024-09-23 (section-21), planning-and-development-act-2000 2024-09-24 (section-1A, section-20, section-181), health-act-2007 2024-09-26 (section-103), central-bank-act-1942 2024-09-27 (section-33ANG), broadcasting-act-2009 2024-09-27 (section-2D, section-46O, section-122), credit-union-act-1997 2024-09-30 (section-3A, section-6A, section-14, section-23, section-27, section-27A, section-43, section-45, section-55A, section-56A, section-82A, section-182A), children-first-act-2015 2024-09-30 (long-title), financial-services-and-pensions-ombudsman-act-2017 2024-09-30 (section-63), childcare-support-act-2018 2024-09-30 (section-22, section-23), irish-aviation-authority-act-1993 2024-10-03 (section-39, section-42, section-63B), housing-miscellaneous-provisions-act-1997 2024-10-17 (section-1), electricity-regulation-act-1999 2024-10-18 (section-5, section-9R), residential-tenancies-act-2004 2024-10-18 (section-3A, section-3B, section-3C, section-19A, section-19B, section-19C, section-20A, section-22A, section-24BA, section-33A, section-35A, section-39A, section-64A, section-64B, section-76A, section-76B, section-125A, section-126, section-135A, section-135B, section-137A, section-144A, section-148A, section-148B, section-148C, section-148D, section-148E, section-148F, section-148G, section-148H, section-148I, section-148J, section-148K, section-148L, section-148M, section-148N, section-148O, section-148P, section-148Q, section-148R, section-148S, section-148T, section-148U, section-148V, section-148W, section-148X, section-148Y, section-148Z, section-148AA, section-148AB, section-148AC, section-148AD, section-148AE, section-148AF, section-148AG, section-177A, section-177B, section-180A), waste-management-act-1996 2024-10-22 (section-42), broadcasting-act-2009 2024-10-22 (section-2D, section-122, section-127), local-government-act-2001 2024-10-23 (section-183, section-211B, schedule-13), student-support-act-2011 2024-10-31 (section-14A), planning-and-development-act-2000 2024-11-01 (section-1A, section-20, section-177AC, section-181, section-261A), electoral-reform-act-2022 2024-11-01 (section-163, section-175), defence-act-1954 2024-11-06 (schedule-5), criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2024-11-06 (section-129, section-139, section-166), criminal-justice-mutual-assistance-act-2008 2024-11-07 (schedule-8, schedule-9, schedule-10), value-added-tax-consolidation-act-2010 2024-11-12 (section-62, section-62A, section-64, section-81, section-85, section-95, section-108C, schedule-7, schedule-8), land-and-conveyancing-law-reform-act-2009 2024-11-13 (schedule-3), civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010 2024-11-13 (section-16, section-26, section-73, section-101, section-150, section-159, section-194), consumer-protection-act-2007 2024-11-15 (section-7, section-8, section-8A, section-9, section-10, section-11, section-12, section-13, section-14, section-16, section-17, section-18, section-19, section-21, section-24A, section-24B, section-24C, section-24D, section-24E, section-24F, section-24G, section-28, section-30, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-40, section-44A, section-63A, section-63B, section-63C, section-63D, section-63E, section-66A, section-66B, section-74A, section-86A), affordable-housing-act-2021 2024-11-18 (section-26, section-33), maternity-protection-act-1994 2024-11-20 (long-title, section-8A, section-13A, section-21A, section-25, section-30A, section-41), employment-equality-act-1998 2024-11-20 (section-13, section-15, section-16), road-traffic-act-2016 2024-11-21 (section-8, section-11, section-13A, section-13B, section-34), health-act-1947 2024-11-25 (section-31A, section-31AA, section-31AB, section-31AC, section-31AD, section-31AE, section-31AF, section-31AG, section-31AH, section-31AI, section-31AJ, section-31AK, section-31AL, section-31B, section-31C, section-31D, section-38A, section-38B, section-38C, section-38D, section-38E, section-38F, section-38G, section-38H, section-38I, section-38J, section-38K, section-38L, section-38M, section-38N, section-38O, section-38P, section-38Q, section-38R, section-38S, section-38T, section-38U, section-38V, section-38W, section-38X, section-38Y, section-38Z), national-asset-management-agency-act-2009 2024-12-02 (section-4, section-11, section-201), companies-act-2014 2024-12-03 (section-142, section-184, section-627, section-725, section-852, section-918, section-964, section-998A, section-999, section-1002, section-1110I, section-1122A, section-1230, section-1281), credit-union-and-co-operation-with-overseas-regulators-act-2012 2024-12-05 (section-69), animal-health-and-welfare-act-2013 2024-12-06 (schedule-3, schedule-4), personal-injuries-assessment-board-act-2003 2024-12-12 (section-18F, section-38, section-68), consumer-protection-act-2007 2024-12-13 (schedule-9), sea-fisheries-and-maritime-jurisdiction-act-2006 2024-12-16 (section-28, section-31), health-act-1947 2024-12-17 (section-55), health-act-1970 2024-12-17 (section-75B), public-health-tobacco-act-2002 2024-12-17 (section-37), competition-and-consumer-protection-act-2014 2024-12-19 (section-81), electricity-regulation-act-1999 2024-12-31 (section-8, section-40D, schedule-3), criminal-justice-terrorist-offences-act-2005 2024-12-31 (schedule-3, schedule-4, schedule-5, schedule-7), criminal-justice-act-2006 2024-12-31 (section-15, section-71B, section-96), taxi-regulation-act-2013 2024-12-31 (section-34, section-35), criminal-justice-spent-convictions-and-certain-disclosures-act-2016 2024-12-31 (section-12), enforcement-of-court-orders-act-1940 2025-01-01 (section-6A, section-9), health-insurance-act-1994 2025-01-01 (section-7F), social-welfare-consolidated-contributions-and-insurability-regulations-1996 2025-01-01 (regulation-3, regulation-74, regulation-76), national-minimum-wage-act-2000 2025-01-01 (section-26, section-29), value-added-tax-consolidation-act-2010 2025-01-01 (section-62, section-64, section-81, section-85, section-108C, schedule-7, schedule-8), organisation-of-working-time-act-1997 2025-01-20 (section-18, section-18A, section-26, section-28, section-39), charities-act-2009 2025-01-27 (section-3, section-93, schedule-2), fisheries-amendment-act-1997 2025-02-03 (section-10), criminal-justice-terrorist-offences-act-2005 2025-02-06 (section-51), road-traffic-act-1961 2025-02-07 (section-54, section-64), broadcasting-act-2009 2025-02-08 (section-2D, section-28, section-46J, section-127, section-139ZI), central-bank-act-1942 2025-02-11 (section-33ANG, section-33ANH, schedule-5, schedule-6, schedule-7, schedule-10), health-act-2007 2025-02-14 (section-103), education-welfare-act-2000 2025-02-19 (section-2, section-9, section-11, section-13, section-14, section-15, section-19, section-25, section-26, section-31, section-32, section-33, section-34, section-35, section-36, section-37, section-38, section-39, section-41), central-bank-act-1942 2025-02-27 (section-33ANH), value-added-tax-consolidation-act-2010 2025-03-06 (section-86, section-92, section-108C), roads-act-1920 2025-03-27 (section-6, section-14, schedule-1, schedule-3), road-traffic-act-1961 2025-03-31 (section-64), air-pollution-act-1987 2025-03-31 (schedule-3), road-traffic-act-2002 2025-03-31 (section-1A, section-9, section-10, section-11, section-13, section-15, section-18, section-21), health-act-2007 2025-03-31 (section-69A, section-103, schedule-1), freedom-of-information-act-2014 2025-03-31 (schedule-3, schedule-4, schedule-5), criminal-justice-act-1984 2025-04-02 (section-28), children-act-2001 2025-04-02 (section-16), criminal-justice-mutual-assistance-act-2008 2025-04-02 (section-55), housing-miscellaneous-provisions-act-2009 2025-04-02 (section-67, section-68), criminal-justice-money-laundering-and-terrorist-financing-act-2010 2025-04-02 (section-7), europol-act-2012 2025-04-02 (section-1, schedule-1), houses-of-the-oireachtas-inquiries-privileges-and-procedures-act-2013 2025-04-02 (section-26), criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2025-04-02 (section-128, section-139, section-166), freedom-of-information-act-2014 2025-04-02 (schedule-3, schedule-4, schedule-5), criminal-justice-corruption-offences-act-2018 2025-04-02 (schedule-2), garda-s-och-na-recording-devices-act-2023 2025-04-02 (section-6), irish-nationality-and-citizenship-act-1956 2025-04-11 (section-15A, section-15B, section-15C, section-15D, section-15E, section-16A, section-28A, section-29A), intoxicating-liquor-act-2003 2025-04-15 (section-25), irish-human-rights-and-equality-commission-act-2014 2025-05-01 (section-10), medical-practitioners-act-2007 2025-05-06 (section-45, section-70, section-71, section-73, section-110, section-111), regulated-professions-health-and-social-care-amendment-act-2020 2025-05-06 (section-79, section-109, section-156, section-159, section-183), road-traffic-act-1961 2025-05-19 (section-26), merchant-shipping-act-1894 2025-06-01 (section-434, section-446, section-492, section-538, section-544, section-567, section-586, section-599), tourist-traffic-act-1939 2025-06-01 (section-2, section-4, section-5, section-6, section-7, section-8, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-21, section-22, section-23, section-25A, section-31, section-37B, section-37C, section-37D, section-41), merchant-shipping-safety-convention-act-1952 2025-06-01 (section-20), merchant-shipping-act-1992 2025-06-01 (section-17), telecommunications-miscellaneous-provisions-act-1996 2025-06-01 (section-2, section-3, section-4, section-5, section-6, section-10, section-11, section-14), communications-regulation-act-2002 2025-06-01 (long-title, section-9, section-12, section-46A, schedule-2), maritime-safety-act-2005 2025-06-01 (section-60), communications-regulation-amendment-act-2007 2025-06-01 (section-7, section-10, section-13, section-14, section-16, section-31), communications-regulation-premium-rate-services-and-electronic-communications-infrastructure-act-2010 2025-06-01 (section-16, section-21), communications-regulation-postal-services-act-2011 2025-06-01 (section-65A), urban-regeneration-and-housing-act-2015 2025-06-18 (section-29), planning-and-development-housing-and-residential-tenancies-act-2016 2025-06-18 (section-13, section-18, section-19, section-20, section-23, section-27, section-33, section-34, section-44, section-48), planning-and-development-act-2000 2025-06-19 (section-177AC), residential-tenancies-act-2004 2025-06-20 (long-title, section-17, section-28, section-32, section-41, section-66, section-137, section-145, section-148L, section-182, section-188, section-197, schedule-1, schedule-3), judicial-council-act-2019 2025-06-23 (section-33), social-welfare-consolidated-supplementary-welfare-allowance-regulations-2007 2025-06-24 (regulation-12), criminal-justice-terrorist-offences-act-2005 2025-06-27 (section-51), affordable-housing-act-2021 2025-07-02 (section-33), value-added-tax-consolidation-act-2010 2025-07-08 (section-64, section-81, section-92, section-92C, section-95, section-96, section-108C), railway-safety-act-2005 2025-07-11 (section-10A, section-28A), central-bank-act-1942 2025-07-15 (section-33AN, section-34), companies-act-2014 2025-07-15 (section-360, section-755, section-850, section-874, section-935, section-957I, section-964, section-998A, section-999, section-1002, section-1110I, section-1366, section-1367, section-1431, schedule-6, schedule-7), finance-local-property-tax-act-2012 2025-07-21 (section-8, section-10A, section-10B, section-11, section-15A, section-20, section-38, section-39A, section-47, section-50, section-72, section-74, section-75, section-129, section-142, section-149), merchant-shipping-safety-convention-act-1952 2025-07-29 (section-20), social-welfare-consolidated-occupational-injuries-regulations-2007 2025-07-29 (regulation-64, regulation-65, regulation-70, regulation-73, schedule-5), central-bank-act-1942 2025-08-01 (section-33ANG, section-34), environmental-protection-agency-act-1992 2025-08-01 (section-82A, section-82B, section-82C, section-82D, section-83, section-86B, section-87A, section-88A, section-88B, section-97A, section-97B, section-98A, section-99J, section-99K), criminal-justice-money-laundering-and-terrorist-financing-act-2010 2025-08-01 (section-110), dog-breeding-establishments-act-2010 2025-08-01 (section-2), property-services-regulation-act-2011 2025-08-01 (long-title, section-2, section-67, schedule-1, schedule-6, schedule-8), customs-act-2015 2025-08-01 (section-12A, section-41, section-44, section-51), planning-and-development-act-2000 2025-08-06 (section-32H, section-34B, section-34C, section-35, section-37, section-37A, section-37B, section-37H, section-37I, section-37L, section-37N, section-37O, section-42B, section-50B, section-146C, section-181, section-285, section-293, section-297, section-299, section-306), intoxicating-liquor-act-2003 2025-08-26 (section-25), medical-practitioners-act-2007 2025-09-05 (section-17, section-54A, section-88, schedule-2), regulated-professions-health-and-social-care-amendment-act-2020 2025-09-05 (section-58, section-79), social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-09-09 (regulation-27, regulation-35, regulation-52HB, regulation-58, regulation-63, regulation-178, regulation-191A, regulation-233D, schedule-10, schedule-16), central-bank-act-1971 2025-09-29 (section-53), vehicle-clamping-act-2015 2025-10-01 (section-2), planning-and-development-act-2000 2025-10-02 (section-35, section-37, section-246), maritime-area-planning-act-2021 2025-10-02 (section-4, section-44, section-171), planning-and-development-act-2024 2025-10-02 (section-76, section-87, section-155, section-193, section-262), road-traffic-traffic-and-parking-regulations-1997 2025-10-09 (regulation-5, regulation-27A, regulation-35), electoral-reform-act-2022 2025-10-10 (section-144, section-163, section-175), teaching-council-act-2001 2025-10-16 (section-34), sea-fisheries-and-maritime-jurisdiction-act-2006 2025-10-23 (section-28, section-31), private-security-services-act-2004 2025-10-31 (section-51), road-traffic-act-1961 2025-11-04 (section-36, schedule-1, schedule-2), planning-and-development-act-2000 2025-11-12 (section-261A), criminal-justice-terrorist-offences-act-2005 2025-11-17 (section-51), child-and-family-agency-act-2013 2025-11-26 (section-63, schedule-3), personal-injuries-assessment-board-act-2003 2025-12-01 (section-18F, section-38, section-68), health-and-social-care-professionals-act-2005 2025-12-01 (schedule-4), statute-of-limitations-1957 2025-12-09 (section-11A, section-49, section-74, section-76), sea-fisheries-and-maritime-jurisdiction-act-2006 2025-12-09 (long-title, section-28, section-38, section-41, section-97, section-100, section-101, schedule-2, schedule-3), civil-registration-act-2004 2025-12-10 (section-2, section-7, section-8, section-8A, section-9, section-11, section-13, section-19A, section-19B, section-23B, section-27, section-28, section-30, section-30B, section-30D, section-30G, section-30H, section-37A, section-39, section-41, section-44C, section-46, section-50, section-51, section-53, section-54, section-57, section-58, section-58A, section-59D, section-60, section-63, section-64, section-66, section-68, section-69, section-71, schedule-1, schedule-3), civil-registration-amendment-act-2014 2025-12-10 (section-1, section-5, section-7, section-8, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-20, section-21, section-22, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, section-35), industrial-training-act-1967 2025-12-11 (section-13), further-education-and-training-act-2013 2025-12-11 (long-title), planning-and-development-act-2024 2025-12-11 (section-87, section-90, section-95, section-99, section-116, section-120, section-148, section-155, section-302, section-304, section-311, section-506), animal-health-and-welfare-act-2013 2025-12-14 (section-11, section-58, schedule-1, schedule-2, schedule-3, schedule-4), irish-medicines-board-act-1995 2025-12-17 (schedule-1), intoxicating-liquor-act-2003 2025-12-17 (section-13, section-14, section-15, section-25), industrial-relations-act-1946 2025-12-18 (section-24, section-53, schedule-1), sea-fisheries-and-maritime-jurisdiction-act-2006 2025-12-19 (long-title, section-7, section-18, section-38, section-41, section-97, section-100, section-101, schedule-2, schedule-3), roads-act-1993 2025-12-31 (section-13, section-17, section-51E, schedule-1, schedule-2, schedule-3), electricity-regulation-act-1999 2025-12-31 (section-2, section-9, section-9D, section-9JD, section-10A, section-13D, section-18, section-20, section-34B, section-40D, section-43, section-44, section-45, section-54, schedule-2, schedule-3), planning-and-development-act-2000 2025-12-31 (section-2, section-5, section-20A, section-20B, section-20C, section-21, section-22, section-22A, section-23, section-24, section-25, section-25A, section-26, section-27, section-27A, section-27B, section-27C, section-27D, section-28, section-31A, section-31F, section-31FF, section-31G, section-31GG, section-31AM, section-31AN, section-31AO, section-31AQ, section-31AR, section-32I, section-34, section-34B, section-34C, section-34E, section-34F, section-34H, section-37, section-37A, section-37B, section-37CD, section-37D, section-37F, section-37I, section-37JA, section-37JB, section-37L, section-37M, section-37N, section-37R, section-37S, section-42, section-46, section-49, section-50A, section-50B, section-60, section-104, section-117, section-118, section-119, section-120, section-121, section-122, section-123, section-124, section-146B, section-146C, section-146CA, section-177P, section-181, section-182C, section-182D, section-184, section-205, section-209, section-231, section-246, section-251, section-254, section-258, section-261A, section-277, section-282, section-285, section-288, section-289, section-290, section-291, section-292, section-293, section-295A, section-295B, section-297, section-298, section-306, schedule-6, schedule-7, schedule-8), local-government-act-2001 2025-12-31 (section-22A, section-23, section-31, section-32, section-36, section-38, section-129M, section-133, section-143, section-158, section-180, section-183, section-211B, section-244, section-245, schedule-2, schedule-7, schedule-10, schedule-13), water-services-act-2007 2025-12-31 (section-41, section-107), housing-miscellaneous-provisions-act-2009 2025-12-31 (section-1, section-55, section-56, section-64, section-67, section-68, schedule-1), land-and-conveyancing-law-reform-act-2009 2025-12-31 (section-80, section-98, schedule-3), national-asset-management-agency-act-2009 2025-12-31 (long-title, section-32, section-33, section-91, section-166, section-213, section-240, schedule-2), urban-regeneration-and-housing-act-2015 2025-12-31 (section-29), local-government-rates-and-other-matters-act-2019 2025-12-31 (section-4, section-21, schedule-1), land-development-agency-act-2021 2025-12-31 (section-30, schedule-3), local-government-mayor-of-limerick-and-miscellaneous-provisions-act-2024 2025-12-31 (section-4, section-20, section-24, section-25, section-38, section-39, section-43, section-45, section-48, schedule-1, schedule-2, schedule-3), planning-and-development-act-2024 2025-12-31 (section-54), child-care-act-1991 2026-01-01 (section-2, section-23NJ, schedule-1), health-insurance-act-1994 2026-01-01 (section-2, section-7F, schedule-2, schedule-4, schedule-5), ethics-in-public-office-act-1995 2026-01-01 (schedule-2), social-welfare-consolidated-contributions-and-insurability-regulations-1996 2026-01-01 (regulation-6, regulation-20A, regulation-20C, regulation-20E, regulation-20G, regulation-23, regulation-58, regulation-71A, regulation-71B, regulation-72, regulation-72A, regulation-72C, regulation-77, regulation-89, regulation-92, regulation-94), national-minimum-wage-act-2000 2026-01-01 (long-title, section-21), safety-health-and-welfare-at-work-act-2005 2026-01-01 (long-title, section-1, section-4, schedule-1, schedule-2), veterinary-practice-act-2005 2026-01-01 (long-title, section-80, schedule-1, schedule-3, schedule-4), national-oil-reserves-agency-act-2007 2026-01-01 (section-45), broadcasting-act-2009 2026-01-01 (long-title, section-2, section-28, section-46K, section-54, section-77, section-139ZI), road-traffic-act-2010 2026-01-01 (section-54, section-84, schedule-1), value-added-tax-consolidation-act-2010 2026-01-01 (section-11, section-24, section-35, section-35A, section-75, section-77, section-81, section-85G, section-91B, section-95, section-108C, section-114B, schedule-2, schedule-4, schedule-7, schedule-8, schedule-9), qualifications-and-quality-assurance-education-and-training-act-2012 2026-01-01 (long-title, section-60, schedule-2), finance-local-property-tax-act-2012 2026-01-01 (section-72, section-77, section-141), workplace-relations-act-2015 2026-01-01 (section-27, schedule-4), digital-services-act-2024 2026-01-01 (section-35, section-38, section-41, section-61, section-67, section-72, section-75), social-welfare-consolidated-occupational-injuries-regulations-2007 2026-01-06 (regulation-21, regulation-50, regulation-64, regulation-72, regulation-73, schedule-2, schedule-5), misuse-of-drugs-act-1977 2026-01-14 (schedule-1), national-training-fund-act-2000 2026-01-19 (section-1, section-3, section-4, section-8, schedule-1), wireless-telegraphy-act-1926 2026-01-20 (long-title), social-welfare-consolidated-claims-payments-and-control-regulations-2007 2026-01-21 (regulation-16, regulation-27, regulation-28J, regulation-35, regulation-42, regulation-52I, regulation-52M, regulation-52MB, regulation-52MC, regulation-62A, regulation-63, regulation-83, regulation-90A, regulation-121A, regulation-124, regulation-130, regulation-136A, regulation-181, regulation-189, regulation-202, regulation-210, regulation-216, regulation-218, regulation-223D, regulation-233D, schedule-10, schedule-15, schedule-16), social-welfare-consolidated-supplementary-welfare-allowance-regulations-2007 2026-01-21 (regulation-12, schedule-1, schedule-4), industrial-relations-act-1990 2026-01-22 (schedule-2, schedule-6), further-education-and-training-act-2013 2026-01-28 (long-title), public-service-pay-and-pensions-act-2017 2026-01-31 (long-title, section-25), bankruptcy-act-1988 2026-02-01 (section-56, section-61, section-61B, section-140D, schedule-2), public-health-tobacco-act-2002 2026-02-02 (long-title), financial-services-and-pensions-ombudsman-act-2017 2026-02-03 (section-2, section-8, schedule-1), data-protection-act-2018 2026-02-04 (section-197, schedule-1, schedule-3), greyhound-industry-act-1958 2026-02-05 (schedule-1), irish-horseracing-industry-1994 2026-02-05 (long-title, section-50, section-71, schedule-1), consumer-credit-act-1995 2026-02-05 (long-title, section-5, section-32, section-49, section-60, section-73C, section-73D, section-86, section-153, schedule-1, schedule-3, schedule-6), teaching-council-act-2001 2026-02-09 (long-title, section-34), central-bank-act-1942 2026-02-10 (section-5C, section-33R, section-33ANH, section-50, section-57BW, section-57CJ, section-57CL, section-57CO), central-bank-reform-act-2010 2026-02-10 (long-title), immigration-act-2004 2026-02-16 (long-title), health-and-social-care-professionals-act-2005 2026-02-17 (schedule-1, schedule-2), criminal-justice-terrorist-offences-act-2005 2026-02-24 (long-title, section-22, section-43, section-49, section-51, schedule-1, schedule-3, schedule-4, schedule-5, schedule-7), ministers-and-secretaries-amendment-act-1939 2026-03-01 (schedule-1), health-insurance-act-1994 2026-03-01 (section-6A, section-7F, schedule-2, schedule-4, schedule-5), residential-tenancies-act-2004 2026-03-01 (long-title, section-66, section-197, schedule-1, schedule-3), defamation-act-2009 2026-03-01 (section-15, section-44), international-protection-act-2015 2026-03-02 (schedule-1, schedule-2), financial-services-and-pensions-ombudsman-act-2017 2026-03-06 (schedule-1), wireless-telegraphy-act-1926 2026-03-11 (long-title), nursing-homes-support-scheme-act-2009 2026-03-13 (section-1, section-4, section-5, section-14C, section-14F, section-14G, section-14L, section-14M, section-14N, section-15, section-16, section-20, section-21, section-24, section-24A, section-27, section-28, section-29, section-30, section-32, section-33, section-34, section-35, section-41, section-48), maritime-area-planning-act-2021 2026-03-13 (section-4, section-27, section-33, section-40, section-56, section-161, section-171, schedule-1, schedule-3, schedule-4, schedule-6), road-traffic-act-1961 2026-03-16 (section-36, schedule-1, schedule-2), personal-insolvency-act-2012 2026-03-16 (long-title, section-27, section-47, section-49, section-49A, section-49C, section-82, section-150, section-157, section-176C, schedule-2), criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2026-03-26 (section-77, section-81, section-128, section-129, section-166, schedule-1, schedule-3, schedule-4), assisted-decision-making-capacity-act-2015 2026-03-31 (section-15, section-30, section-47, section-52, section-76, section-84, section-87, section-103, section-143, schedule-1), merchant-shipping-safety-convention-act-1952 2026-04-01 (section-29), housing-miscellaneous-provisions-act-1992 2026-04-01 (long-title, section-20A, section-26), health-insurance-act-1994 2026-04-01 (long-title, section-6A, section-7F, section-33B, schedule-2), national-oil-reserves-agency-act-2007 2026-04-01 (long-title, section-44J, section-45), taxi-regulation-act-2013 2026-04-01 (section-29, section-34), road-traffic-act-1994 2026-04-03 (section-25, section-49), criminal-justice-terrorist-offences-act-2005 2026-04-03 (long-title, section-22, section-43, section-49, section-51, schedule-1, schedule-3, schedule-4, schedule-5, schedule-7), inland-fisheries-act-2010 2026-04-03 (section-72, schedule-1, schedule-4), planning-and-development-act-2000 2026-04-04 (long-title, section-1A, section-2, section-8, section-31AN, section-34, section-34B, section-34C, section-34F, section-34H, section-37, section-37CD, section-37D, section-37F, section-37I, section-37JA, section-37JB, section-37M, section-37R, section-37S, section-38, section-42, section-46, section-49, section-50A, section-50B, section-96, section-146B, section-146CA, section-182D, section-184, section-205, section-214, section-251, section-254, section-277, section-285, section-288, section-289, section-291, section-292, section-293, section-295A, section-295B, section-297, schedule-6, schedule-7, schedule-8), safety-health-and-welfare-at-work-act-2005 2026-04-09 (long-title, section-1, schedule-1, schedule-2), pharmacy-act-2007 2026-04-09 (schedule-1, schedule-4), data-protection-act-2018 2026-04-09 (section-125, section-167, section-197, schedule-1, schedule-3), central-bank-supervision-and-enforcement-act-2013 2026-04-10 (section-37, section-73, schedule-1), children-and-family-relationships-act-2015 2026-04-20 (section-49, section-93, section-99, section-135), charities-act-2009 2026-04-22 (long-title, schedule-2), further-education-and-training-act-2013 2026-04-23 (long-title), gambling-regulation-act-2024 2026-04-23 (section-75, schedule-3), diplomatic-relations-and-immunities-act-1967 2026-04-28 (schedule-1, schedule-2, schedule-3, schedule-4, schedule-5, schedule-6), animal-health-and-welfare-act-2013 2026-05-05 (schedule-1, schedule-2, schedule-3, schedule-4), finance-local-property-tax-act-2012 2026-05-07 (long-title, section-15, section-17, section-43, section-77), environmental-protection-agency-act-1992 2026-05-08 (section-4, section-21, section-52, section-82D, section-83, section-86A, section-87, section-97A, schedule-1, schedule-2), waste-management-act-1996 2026-05-08 (section-2, section-5, schedule-2, schedule-4, schedule-7), environment-miscellaneous-provisions-act-2011 2026-05-08 (section-41, section-48), legal-services-regulation-act-2015 2026-05-08 (section-9, section-34, section-121, section-139, section-147, section-189, section-219, schedule-2), road-traffic-act-1961 2026-05-13 (section-36), roads-act-1993 2026-05-13 (section-2, section-10A, schedule-1, schedule-2, schedule-3), road-traffic-traffic-and-parking-regulations-1997 2026-05-13 (schedule-2), health-act-1947 2026-05-14 (section-2, section-21, section-31B, section-55, section-87, schedule-1), planning-and-development-act-2024 2026-05-18 (section-54, section-82, section-116, section-238, section-294, section-360, section-474, section-506), planning-and-development-act-2000 2026-05-26 (section-38), health-and-social-care-professionals-act-2005 2026-05-28 (schedule-2, schedule-4), remediation-of-dwellings-damaged-by-the-use-of-defective-concrete-blocks-act-2022 2026-05-28 (section-46), national-treasury-management-agency-amendment-act-2014 2026-05-29 (section-8, section-9), finance-excise-duties-vehicles-act-1952 2026-06-01 (long-title), automatic-enrolment-retirement-savings-system-act-2024 2026-06-01 (section-113), protection-of-employees-employers-insolvency-act-1984 2026-06-08 (section-2), protected-disclosures-act-2014 2026-06-08 (schedule-4, schedule-6), irish-nationality-and-citizenship-act-1956 2026-06-12 (section-1, section-2, section-3, section-4, section-5, section-8, section-9, section-11, section-11A, section-12, section-13, section-14, section-15A, section-15B, section-15C, section-15D, section-15E, section-16, section-17, section-18, section-19, section-21, section-23, section-24, section-25, section-26, section-27, section-28, section-28A, section-29, section-29A, section-30), road-traffic-act-1961 2026-06-12 (section-26), civil-legal-aid-act-1995 2026-06-12 (section-11A, section-36A, section-36B, section-40), immigration-act-1999 2026-06-12 (section-11), immigration-act-2003 2026-06-12 (section-4, section-7), civil-law-miscellaneous-provisions-act-2022 2026-06-12 (section-47), immigration-act-2004 2026-06-15 (long-title), maritime-area-planning-act-2021 2026-06-16 (section-95, section-171), international-protection-act-2015 2026-06-18 (schedule-1, schedule-2), child-care-act-1991 2026-06-23 (section-2, section-23H, section-63, schedule-1), mental-health-act-2001 2026-06-23 (long-title, schedule-1), child-care-amendment-act-2011 2026-06-23 (section-10, section-15), national-vetting-bureau-children-and-vulnerable-persons-act-2012 2026-06-23 (long-title), civil-legal-aid-act-1995 2026-06-24 (section-1, section-11B), industrial-relations-act-1990 2026-06-29 (schedule-2), workplace-relations-act-2015 2026-06-29 (section-74, section-76, section-83, schedule-2, schedule-4), misuse-of-drugs-act-1977 2026-06-30 (long-title, section-10, section-32, schedule-1), irish-medicines-board-act-1995 2026-06-30 (schedule-1, schedule-2), competition-act-2002 2026-07-01 (long-title, section-15E, section-15AA, section-17, section-28G, section-46, section-47B), railway-safety-act-2005 2026-07-01 (long-title, section-134, schedule-1, schedule-2), road-traffic-act-2006 2026-07-01 (section-16, section-18), metrology-act-1996 2026-07-07 (long-title, section-1, section-2, section-3, section-4, section-5, section-6, section-7, section-8, section-9, section-10, section-11, section-12, section-13, section-14, section-15, section-16, section-17, section-18, section-19, section-20, section-21, section-22, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-31, section-32, section-33, section-34, schedule-1, schedule-3), central-bank-supervision-and-enforcement-act-2013 2026-07-07 (section-73), criminal-justice-terrorist-offences-act-2005 2026-07-08 (section-51, schedule-3, schedule-5), remediation-of-dwellings-damaged-by-the-use-of-defective-concrete-blocks-act-2022 2026-07-08 (section-22), central-bank-act-1971 2026-07-10 (section-30, section-31G, section-31H, section-31I, section-31Q, schedule-1), ministers-and-secretaries-amendment-act-2011 2026-07-13 (schedule-2, schedule-3), civil-service-regulation-act-1956 2026-07-15 (schedule-2), official-languages-act-2003 2026-07-15 (long-title, section-9E, section-18A, section-19B, section-19C, section-26, section-27, section-29, schedule-1), data-protection-act-2018 2026-07-16 (section-12, section-26A, section-117A), public-health-tobacco-act-2002 2026-07-20 (long-title), guardianship-of-infants-act-1964 2026-07-21 (section-6B, section-7, schedule-1), child-care-act-1991 2026-07-21 (section-2, section-23A, section-23C, section-23D, section-23J, section-23N, section-23NJ, section-23NL, section-23O, section-24, section-25, section-29, section-30, section-31, section-35A, section-35H, section-37, section-43A, section-45A, section-45B, section-45C, section-45D, section-58A, section-58C, section-58JA, section-58JB, section-58JC, section-58JD, section-58L, section-58M, section-59, section-63), maritime-area-planning-act-2021 2026-07-23 (section-95), building-control-act-1990 2026-07-27 (section-17A, section-17B, section-17C, section-23), building-control-regulations-1997 2026-07-27 (regulation-11, schedule-1, schedule-2, schedule-3, schedule-5, schedule-6), climate-action-and-low-carbon-development-act-2015 2026-07-27 (section-1), medical-practitioners-act-2007 2026-07-29 (long-title, section-2, section-17, section-88, schedule-2), communications-regulation-act-2002 2026-07-31 (long-title, section-12, section-39, schedule-2), competition-and-consumer-protection-act-2014 2026-07-31 (section-19, section-47, section-74, section-78, section-81, section-85, section-86, section-87), freedom-of-information-act-2014 2026-07-31 (section-10, section-27, schedule-3, schedule-4, schedule-5), central-bank-act-1942 2026-08-01 (section-2A, section-5, section-6B, section-6K, section-18A, section-18E, section-20, section-22, section-23, section-33W, section-33AG, section-33AI, section-33AJ, section-33AN, section-33ANC, section-33ANE, section-33ANG, section-33ANH, section-33ANI, section-33ANL, section-33AQ, section-33AW, section-33AXA, section-33AZA, section-33AZB, section-33BAA, section-33BE, section-57A, section-57C, section-57U, section-57AH, section-61B, section-61H), central-bank-act-1997 2026-08-01 (section-29A, section-34FA, section-34FB, section-36EA), national-asset-management-agency-act-2009 2026-08-01 (section-112, section-217, section-241), value-added-tax-consolidation-act-2010 2026-08-01 (section-2, section-17, section-28, section-32A, section-33, section-43A, section-53A, section-58, section-61, section-62, section-62A, section-65, section-77A, section-84, section-85A, section-86, section-86A, section-87, section-88, section-91A, section-91B, section-91C, section-91D, section-91E, section-91I, section-91J, section-91K, section-92, section-92A, section-92C, section-108, section-108C, section-108D, section-109A, section-114B, section-115, section-116, section-116A, schedule-1, schedule-2, schedule-3), irish-bank-resolution-corporation-act-2013 2026-08-01 (section-6, section-9, section-10, section-18, section-23), extradition-act-1965 2026-08-10 (section-20A, section-36A, schedule-1), children-act-2001 2026-08-10 (section-16, schedule-2), criminal-justice-theft-and-fraud-offences-act-2001 2026-08-10 (section-23, section-32, section-39, schedule-1), criminal-justice-act-2006 2026-08-10 (long-title, section-5, section-16, section-30, section-54, section-69, section-90, section-93, section-100, section-121, section-127, section-148, section-159, section-184), planning-and-development-act-2000 2026-08-12 (section-1A, section-2, section-37E, section-42, section-96, section-211, section-214), national-oil-reserves-agency-act-2007 2026-08-28 (section-44J), firearms-act-1925 2026-09-01 (section-1, section-3DA, section-10, section-10A, section-14, section-14A, section-20, section-27B), international-criminal-court-act-2006 2026-09-01 (long-title, section-1, section-3, section-5, section-7, section-10, section-11, section-13, section-14, section-15, section-16, section-17, section-18, section-20, section-21, section-23, section-24, section-25, section-26, section-27, section-28, section-29, section-30, section-32, section-33, section-34, section-35, section-36, section-39, section-40, section-41, section-42, section-43, section-44, section-45, section-46, section-47, section-48, section-49, section-54, section-55, section-56, section-57, section-58, section-59, section-60, section-61, section-64, section-65, section-66, schedule-1, schedule-2, schedule-3, schedule-4), criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2026-09-01 (section-1, section-3, section-9, section-12, section-14, section-16, section-17, section-20, section-22, section-24, section-25, section-26, section-27, section-29, section-32, section-41, section-42, section-44, section-46, section-48, section-62, section-72, section-76, section-78, section-79, section-81, section-82, section-84, section-85, section-86, section-87, section-89, section-90, section-91, section-109, section-114, section-115, section-123, section-126, section-129, section-132, section-133, section-134, section-135, section-139, section-143, section-144, section-155, section-156, section-166, section-168, section-170), national-treasury-management-agency-amendment-act-2014 2026-09-22 (long-title, section-8, section-9), residential-tenancies-act-2004 2026-09-25 (section-20B), social-welfare-consolidation-act-2005 2026-10-01 (section-17C, section-34A, section-109, section-115, section-239A, section-240).
- **Causes.** For each provision that changed between two revisions, the annotations attached to it in the newer one,
  and not present anywhere in the older one, name the law and the day ("Substituted (1.01.2023) by ... (27/2022)"). One
  law: the change is that law's commit, on that day. Where a note quotes an amendment made through another act ("as
  inserted (26.12.2018) by ..."), the dated law is the one credited. More than one law: credited to neither
  (`Candidate:`). No note attached, but a later revision attaches one dated in the interval: that law, with an
  `Evidence:` trailer. A day after the newer revision's own day: printed early, the publisher's, not credited. A day on
  or before the older revision's day: consolidated late, dated the day after the older revision, the stated day in
  `Stated-in-force:`.
- **Counts.** 604 first-revision commits, 1067 law commits (236 of them consolidated late),
  564 credited to neither of two laws, 51 printed early, 455
  unexplained, 1143 layout; 3799 tags; one documentation commit.

Labelled commits:

- transfer-of-execution-of-sentences-act-2005 2017-04-08: consolidated late (annotation gives 2017-04-07), section-10
- social-welfare-and-pensions-act-2005 2017-04-13: consolidated late (annotation gives 2005-12-01), section-2, section-3, section-4, section-5, section-7, section-8, section-9, section-10, section-11, section-12, section-13, section-14, section-16, section-17, section-18, section-19, section-20, section-21, section-22, section-23, section-24, section-25, section-26
- social-welfare-and-pensions-act-2007 2017-07-27: consolidated late (annotation gives 2008-03-07), section-35
- social-welfare-and-pensions-act-2008 2017-07-27: consolidated late (annotation gives 2014-07-17), section-5
- succession-act-1965 2017-11-03: consolidated late (annotation gives 1982-05-12), section-6
- succession-act-1965 2017-11-03: consolidated late (annotation gives 1988-06-14), section-27A, section-117
- succession-act-1965 2017-11-03: consolidated late (annotation gives 2009-12-01), section-53
- financial-emergency-measures-in-the-public-interest-no-2-act-2009 2018-01-02: consolidated late (annotation gives 2012-01-01), section-1
- regional-technical-colleges-act-1992 2018-04-25: consolidated late (annotation gives 2007-02-01), section-3
- regional-technical-colleges-act-1992 2018-04-25: candidates, section-13
- regional-technical-colleges-act-1992 2018-04-25: consolidated late (annotation gives 2018-04-24), section-13
- safety-health-and-welfare-at-work-general-application-regulations-2007 2018-05-01: consolidated late (annotation gives 2016-02-18), schedule-8
- consumer-credit-act-1995 2018-05-26: consolidated late (annotation gives 2003-05-01), section-4
- water-services-act-2013 2018-05-26: consolidated late (annotation gives 2015-11-23), section-16
- water-services-act-2013 2018-05-26: consolidated late (annotation gives 2014-01-01), section-27
- water-services-act-2007 2018-10-23: consolidated late (annotation gives 2013-03-29), section-6, section-7
- water-services-act-2007 2018-10-23: consolidated late (annotation gives 2018-06-11), section-75
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2018-11-27: consolidated late (annotation gives 2013-06-14), section-60
- industrial-relations-act-1969 2019-01-02: consolidated late (annotation gives 2015-10-01), section-13
- judicial-separation-and-family-law-reform-act-1989 2019-01-02: consolidated late (annotation gives 2017-01-11), section-31
- family-law-divorce-act-1996 2019-01-02: consolidated late (annotation gives 2017-01-11), section-38
- civil-registration-act-2004 2019-01-02: consolidated late (annotation gives 2018-12-31), section-7, section-9
- value-added-tax-consolidation-act-2010 2019-01-02: consolidated late (annotation gives 2014-01-01), section-62A
- value-added-tax-consolidation-act-2010 2019-01-02: consolidated late (annotation gives 2017-12-25), section-11
- value-added-tax-consolidation-act-2010 2019-01-02: consolidated late (annotation gives 2019-01-01), section-91A
- animal-health-and-welfare-act-2013 2019-01-02: consolidated late (annotation gives 2019-01-01), section-61
- civil-registration-act-2004 2019-01-02: candidates, section-2
- civil-registration-act-2004 2019-01-02: consolidated late (annotation gives 2015-11-16), section-2
- criminal-justice-act-2006 2019-01-12: consolidated late (annotation gives 2007-05-18), section-99
- planning-and-development-act-2000 2019-01-31: candidates, section-11
- employees-provision-of-information-and-consultation-act-2006 2019-02-01: unexplained, long-title
- terms-of-employment-information-act-1994 2019-03-04: candidates, section-3
- terms-of-employment-information-act-1994 2019-03-05: consolidated late (annotation gives 2019-03-04), section-1
- national-minimum-wage-act-2000 2019-03-05: consolidated late (annotation gives 2019-03-04), section-14
- national-minimum-wage-act-2000 2019-03-05: consolidated late (annotation gives 2019-03-04), section-15
- planning-and-development-act-2000 2019-03-10: unexplained, section-50
- planning-and-development-act-2000 2019-03-11: consolidated late (annotation gives 2019-01-01), section-246
- road-transport-act-1978 2019-03-17: unexplained, section-5
- companies-act-2014 2019-03-29: unexplained, section-999, section-1123, section-1129, section-1280, section-1282
- planning-and-development-act-2000 2019-04-03: candidates, section-11
- personal-injuries-assessment-board-act-2003 2019-04-03: candidates, section-50
- communications-regulation-postal-services-act-2011 2019-04-10: unexplained, schedule-4
- student-support-act-2011 2019-04-11: unexplained, section-14
- immigration-act-2003 2019-04-12: unexplained, section-7
- local-government-act-2001 2019-04-16: unexplained, section-188
- ministers-and-secretaries-amendment-act-2011 2019-04-18: candidates, section-17A
- criminal-justice-mutual-assistance-act-2008 2019-04-30: candidates, section-107
- criminal-justice-mutual-assistance-act-2008 2019-04-30: consolidated late (annotation gives 2018-05-25), section-107
- companies-act-2014 2019-05-01: unexplained, section-1428A, section-1431
- chemicals-act-2008 2019-05-10: candidates, section-2
- chemicals-act-2008 2019-05-11: consolidated late (annotation gives 2015-06-01), section-2
- firearms-act-1964 2019-05-16: consolidated late (annotation gives 2006-11-01), section-27
- firearms-act-1964 2019-05-16: candidates, section-26, section-27B
- firearms-act-1964 2019-05-16: consolidated late (annotation gives 2007-05-18), section-26, section-27B
- civil-registration-act-2004 2019-05-23: unexplained, section-67, schedule-1
- euro-area-loan-facility-act-2010 2019-05-28: unexplained, schedule-1
- residential-tenancies-act-2004 2019-06-04: unexplained, section-148S, section-148T, section-148U, section-148V, section-148W, section-148X, section-148Y, section-148Z, section-148AA, section-148AB, section-148AC, section-148AD, section-148AE, section-148AG, schedule-2, schedule-3
- central-bank-act-1942 2019-06-07: candidates, section-2
- roads-act-1993 2019-06-24: candidates, section-51
- roads-act-1993 2019-06-24: candidates, section-2
- planning-and-development-act-2000 2019-07-01: early, section-34A, section-34B, section-34C, section-37R, section-37S
- planning-and-development-act-2000 2019-07-01: unexplained, section-50
- central-bank-act-1942 2019-07-05: candidates, schedule-10
- communications-regulation-act-2002 2019-07-09: candidates, section-10
- residential-tenancies-act-2004 2019-07-15: candidates, section-3
- planning-and-development-act-2000 2019-07-16: candidates, section-11
- planning-and-development-act-2000 2019-07-16: consolidated late (annotation gives 2019-01-31), section-11
- parental-leave-act-1998 2019-07-19: candidates, section-2
- central-bank-act-1942 2019-07-21: candidates, section-2
- central-bank-act-1942 2019-07-21: candidates, section-33AK
- central-bank-act-1942 2019-07-21: candidates, section-33AN
- central-bank-act-1942 2019-07-21: unexplained, section-33ANC, section-33AR
- central-bank-act-1942 2019-07-22: consolidated late (annotation gives 2004-08-01), section-33AR
- central-bank-act-1942 2019-07-22: consolidated late (annotation gives 2018-01-03), section-33BC
- central-bank-act-1942 2019-07-22: consolidated late (annotation gives 2019-07-05), schedule-10
- companies-act-2014 2019-07-22: unexplained, section-1428A, section-1431
- national-treasury-management-agency-amendment-act-2014 2019-07-25: early, section-47A
- wildlife-act-1976 2019-08-01: candidates, section-2
- status-of-children-act-1987 2019-08-13: consolidated late (annotation gives 2016-01-18), section-35
- firearms-act-1925 2019-09-01: candidates, section-21
- firearms-act-1925 2019-09-01: candidates, section-2
- firearms-act-1925 2019-09-01: candidates, section-1, section-2A
- firearms-act-1925 2019-09-02: candidates, section-15
- firearms-act-1925 2019-09-02: consolidated late (annotation gives 2007-05-18), section-15
- garda-s-och-na-act-2005 2019-09-16: unexplained, section-22
- criminal-justice-mutual-assistance-act-2008 2019-09-24: consolidated late (annotation gives 2013-02-01), section-95
- health-and-social-care-professionals-act-2005 2019-09-28: consolidated late (annotation gives 2014-12-31), section-4
- civil-registration-act-2004 2019-10-06: candidates, section-2
- civil-registration-act-2004 2019-10-06: candidates, section-19A, section-23B
- civil-registration-act-2004 2019-10-06: early, schedule-1
- civil-registration-act-2004 2019-10-06: early, section-44F, section-44G, section-44H
- civil-registration-act-2004 2019-10-07: candidates, section-8
- civil-registration-act-2004 2019-10-07: consolidated late (annotation gives 2015-09-04), section-8
- criminal-procedure-act-1967 2019-10-08: consolidated late (annotation gives 2001-10-01), section-4Q
- adoptive-leave-act-1995 2019-10-24: early, section-6A
- unfair-dismissals-act-1977 2019-11-01: candidates, section-6
- maternity-protection-act-1994 2019-11-01: candidates, section-2
- adoptive-leave-act-1995 2019-11-01: candidates, section-2
- civil-registration-act-2004 2019-11-01: candidates, section-2
- qualifications-and-quality-assurance-education-and-training-act-2012 2019-11-08: unexplained, section-29A, section-29B, section-29C, section-55A, section-55B, section-55C, section-55D, section-55E, section-55F, section-55G, section-55H, section-55I, section-65A, section-66A
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2019-11-18: unexplained, section-24
- road-traffic-act-2016 2019-11-25: unexplained, section-38, section-39
- family-law-maintenance-of-spouses-and-children-act-1976 2019-11-26: candidates, section-5A
- family-law-maintenance-of-spouses-and-children-act-1976 2019-11-26: consolidated late (annotation gives 1990-11-29), section-5A
- family-law-maintenance-of-spouses-and-children-act-1976 2019-11-26: candidates, section-21A
- family-law-maintenance-of-spouses-and-children-act-1976 2019-11-26: consolidated late (annotation gives 2002-10-01), section-21A
- judicial-separation-and-family-law-reform-act-1989 2019-12-01: unexplained, long-title
- civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010 2019-12-02: consolidated late (annotation gives 2017-11-02), section-113
- industrial-relations-act-1946 2019-12-02: unexplained, section-34
- national-treasury-management-agency-amendment-act-2014 2019-12-03: consolidated late (annotation gives 2019-10-31), section-47A
- garda-s-och-na-act-2005 2019-12-17: unexplained, section-73, section-125
- central-bank-act-1942 2019-12-18: candidates, section-33AN
- central-bank-act-1942 2019-12-18: unexplained, section-33ANE
- central-bank-act-1942 2019-12-19: consolidated late (annotation gives 2014-01-27), schedule-2
- central-bank-act-1942 2019-12-19: consolidated late (annotation gives 2019-07-05), schedule-10
- value-added-tax-consolidation-act-2010 2019-12-22: candidates, section-59
- national-minimum-wage-act-2000 2019-12-24: unexplained, section-10D, section-16
- electricity-regulation-act-1999 2019-12-31: unexplained, section-14B
- road-traffic-act-1994 2020-01-01: candidates, section-41
- national-oil-reserves-agency-act-2007 2020-01-01: candidates, schedule-2, schedule-3
- value-added-tax-consolidation-act-2010 2020-01-01: candidates, schedule-3
- value-added-tax-consolidation-act-2010 2020-01-01: candidates, section-2
- value-added-tax-consolidation-act-2010 2020-01-01: candidates, schedule-2
- regional-technical-colleges-act-1992 2020-01-01: unexplained, section-3A
- value-added-tax-consolidation-act-2010 2020-01-01: unexplained, section-53A
- companies-act-2014 2020-01-01: unexplained, section-228, section-1384A
- regional-technical-colleges-act-1992 2020-01-02: consolidated late (annotation gives 2007-02-01), section-21C, section-21D
- value-added-tax-consolidation-act-2010 2020-01-02: consolidated late (annotation gives 2014-12-23), section-5
- value-added-tax-consolidation-act-2010 2020-01-02: consolidated late (annotation gives 2017-01-01), section-86
- companies-act-2014 2020-01-02: consolidated late (annotation gives 2019-12-18), section-1348, section-1349, section-1350, section-1351, section-1354, section-1357, section-1361, section-1363, section-1364, section-1551
- companies-act-2014 2020-01-02: consolidated late (annotation gives 2019-03-29), section-1328
- regional-technical-colleges-act-1992 2020-01-02: candidates, section-14
- regional-technical-colleges-act-1992 2020-01-02: consolidated late (annotation gives 2018-04-24), section-14
- value-added-tax-consolidation-act-2010 2020-01-02: candidates, section-116
- value-added-tax-consolidation-act-2010 2020-01-02: consolidated late (annotation gives 2017-12-25), section-116
- value-added-tax-consolidation-act-2010 2020-01-02: candidates, section-120
- value-added-tax-consolidation-act-2010 2020-01-02: consolidated late (annotation gives 2017-12-25), section-120
- value-added-tax-consolidation-act-2010 2020-01-02: candidates, section-2
- value-added-tax-consolidation-act-2010 2020-01-02: consolidated late (annotation gives 2017-12-25), section-2
- value-added-tax-consolidation-act-2010 2020-01-02: candidates, section-111
- value-added-tax-consolidation-act-2010 2020-01-02: consolidated late (annotation gives 2014-12-23), section-111
- industrial-development-act-1986 2020-01-07: unexplained, long-title
- education-act-1998 2020-01-15: consolidated late (annotation gives 2012-06-06), section-23
- central-bank-act-1942 2020-01-30: candidates, section-33AK
- central-bank-act-1942 2020-01-30: candidates, section-33AN
- consumer-protection-act-2007 2020-01-30: unexplained, schedule-2, schedule-3
- industrial-relations-act-1946 2020-02-01: unexplained, section-34, section-52, section-57
- health-and-social-care-professionals-act-2005 2020-02-06: unexplained, section-36B
- planning-and-development-act-2000 2020-02-08: candidates, section-4
- health-act-1970 2020-02-18: consolidated late (annotation gives 2017-04-14), section-59A
- health-act-1970 2020-02-18: candidates, section-53C
- health-act-1970 2020-02-18: consolidated late (annotation gives 2019-01-01), section-53C
- electricity-regulation-act-1999 2020-03-13: unexplained, section-43
- electricity-regulation-act-1999 2020-03-14: consolidated late (annotation gives 2014-02-07), section-13
- road-traffic-act-1961 2020-03-21: consolidated late (annotation gives 2013-01-12), section-21
- road-traffic-act-1961 2020-03-21: candidates, section-56
- road-traffic-act-1961 2020-03-21: consolidated late (annotation gives 2008-07-04), section-56
- planning-and-development-act-2000 2020-03-27: early, section-251A
- defence-act-1954 2020-03-27: unexplained, section-55, section-77
- mental-health-act-2001 2020-03-30: early, section-2A, section-17, section-18, section-28, section-48, section-49, section-58
- waste-management-act-1996 2020-04-15: consolidated late (annotation gives 2008-07-01), section-2
- succession-act-1965 2020-05-04: candidates, section-4A
- family-law-maintenance-of-spouses-and-children-act-1976 2020-05-04: candidates, section-8A
- maternity-protection-act-1994 2020-05-04: candidates, section-2
- maternity-protection-act-1994 2020-05-04: candidates, section-16, section-16B
- succession-act-1965 2020-05-04: unexplained, section-56
- adoption-act-2010 2020-05-04: unexplained, long-title
- civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010 2020-05-04: unexplained, schedule-1
- adoption-act-2010 2020-05-05: consolidated late (annotation gives 2017-10-19), section-18A
- children-act-2001 2020-05-21: unexplained, section-183, section-184, section-226A
- child-care-amendment-act-2007 2020-05-21: unexplained, section-4
- communications-regulation-premium-rate-services-and-electronic-communications-infrastructure-act-2010 2020-05-21: unexplained, section-8
- children-act-2001 2020-05-22: consolidated late (annotation gives 2017-12-31), section-7, section-8, section-10, section-13, section-71, section-267
- children-act-2001 2020-05-22: candidates, section-77
- children-act-2001 2020-05-22: consolidated late (annotation gives 2017-12-31), section-77
- children-act-2001 2020-05-22: candidates, section-3
- children-act-2001 2020-05-22: consolidated late (annotation gives 2017-12-31), section-3
- health-and-social-care-professionals-act-2005 2020-05-27: unexplained, section-96, section-97
- central-bank-act-1942 2020-06-25: unexplained, section-33ANE, section-33AR
- central-bank-act-1942 2020-06-26: consolidated late (annotation gives 2004-08-01), section-33AK
- planning-and-development-act-2000 2020-06-30: unexplained, section-112A, section-128, section-171, section-171A, section-177, section-177A, section-177N, section-177O, section-182E
- road-traffic-act-1961 2020-07-29: unexplained, section-20
- national-oil-reserves-agency-act-2007 2020-08-01: candidates, section-44I
- national-treasury-management-agency-amendment-act-2000 2020-08-02: consolidated late (annotation gives 2014-12-22), section-12, section-13, section-14, section-15
- emergency-measures-in-the-public-interest-covid-19-act-2020 2020-08-02: candidates, section-28
- emergency-measures-in-the-public-interest-covid-19-act-2020 2020-08-02: consolidated late (annotation gives 2020-08-01), section-28
- credit-guarantee-act-2012 2020-08-12: consolidated late (annotation gives 2020-08-11), section-4A
- health-act-1947 2020-08-15: unexplained, section-6
- companies-act-2014 2020-08-21: early, section-1110A, section-1110B, section-1110C, section-1110D
- companies-act-2014 2020-08-21: unexplained, section-296, section-297, section-298, section-349, section-350, section-351, section-353, section-354, section-916, section-917, section-935, section-935A, section-935B, section-935D, section-936, section-993, section-994, section-1101, section-1213, section-1214, section-1267A, section-1268, section-1280A, section-1282, section-1428A, section-1440, section-1441, section-1447, section-1448, section-1449
- local-government-reform-act-2014 2020-08-26: unexplained, section-69, section-70, schedule-2, schedule-3
- education-for-persons-with-special-educational-needs-act-2004 2020-08-27: consolidated late (annotation gives 2005-01-01), section-16, section-17
- electoral-amendment-act-2009 2020-08-27: consolidated late (annotation gives 2016-02-03), section-2, section-3, section-4, section-5, schedule-1
- waste-management-act-1996 2020-08-27: unexplained, schedule-5
- central-bank-act-1942 2020-09-04: unexplained, section-33AR
- civil-registration-act-2004 2020-09-04: unexplained, section-44E, section-44F
- civil-registration-act-2004 2020-09-05: consolidated late (annotation gives 2009-01-01), section-66
- roads-act-1993 2020-09-10: consolidated late (annotation gives 2007-01-31), section-51
- european-arrest-warrant-act-2003 2020-09-15: unexplained, section-10
- planning-and-development-act-2000 2020-09-24: unexplained, section-112A, section-128, section-177, section-177A, section-177N, section-177O, section-182E
- environmental-protection-agency-act-1992 2020-10-01: consolidated late (annotation gives 2019-01-25), section-82B
- financial-emergency-measures-in-the-public-interest-act-2010 2020-10-01: unexplained, section-2A
- redundancy-payments-act-1971 2020-10-14: unexplained, schedule-1
- protection-of-employees-employers-insolvency-act-1984 2020-10-14: unexplained, section-8A
- employment-equality-act-1998 2020-10-14: unexplained, section-14A
- parental-leave-act-1998 2020-10-14: unexplained, section-18, section-19, section-20, section-21, section-22
- national-minimum-wage-act-2000 2020-10-14: unexplained, section-15, section-16
- carer-s-leave-act-2001 2020-10-14: unexplained, section-18, section-19, section-20, section-21, section-22, section-23, section-24, section-25, section-31, section-32
- protection-of-employees-part-time-work-act-2001 2020-10-14: unexplained, long-title
- protection-of-employees-temporary-agency-work-act-2012 2020-10-14: unexplained, schedule-1
- protection-of-employees-employers-insolvency-act-1984 2020-10-15: consolidated late (annotation gives 1990-05-01), section-7
- adoptive-leave-act-1995 2020-10-15: consolidated late (annotation gives 2005-11-28), section-12
- adoptive-leave-act-1995 2020-10-15: candidates, section-9
- adoptive-leave-act-1995 2020-10-15: consolidated late (annotation gives 2016-08-01), section-9
- adoptive-leave-act-1995 2020-10-15: candidates, section-8, section-10
- adoptive-leave-act-1995 2020-10-15: consolidated late (annotation gives 2016-08-01), section-8, section-10
- competition-act-2002 2020-10-15: unexplained, section-47A
- competition-act-2002 2020-10-16: consolidated late (annotation gives 2012-07-03), section-14B
- national-training-fund-act-2000 2020-10-22: consolidated late (annotation gives 2013-10-26), section-7
- finance-local-property-tax-act-2012 2020-10-22: unexplained, section-12
- employment-permits-act-2006 2020-10-23: consolidated late (annotation gives 2014-09-30), section-10
- health-act-1947 2020-10-26: candidates, section-31A
- nurses-and-midwives-act-2011 2020-10-28: unexplained, section-51A, section-52A, section-52B, section-53A, section-56A, section-57A, section-63A, section-68A, section-103A, section-106A
- railway-safety-act-2005 2020-10-31: candidates, section-2
- health-act-1970 2020-11-01: candidates, section-45A
- health-act-1970 2020-11-01: candidates, section-59
- electricity-regulation-act-1999 2020-11-02: unexplained, section-9BB, section-13A, schedule-3
- medical-practitioners-act-2007 2020-11-06: unexplained, section-36A, section-36B, section-36C, section-36D, section-36E, section-36F, section-36G, section-36H, section-36I, section-36J, section-36K, section-36L, section-36M, section-36N, section-36O, section-36P, section-36Q, section-36R, section-38B, section-44A, section-44B, section-44C, section-54A, section-55A, section-56B, section-58A, section-59A, section-65A, section-70B, section-105A, section-105B, section-112
- civil-registration-act-2004 2020-11-20: candidates, section-44C
- civil-registration-act-2004 2020-11-20: unexplained, section-58, section-59I, schedule-1
- road-traffic-act-1961 2020-11-27: candidates, section-33
- road-traffic-act-1961 2020-11-27: candidates, section-3
- garda-s-och-na-act-2005 2020-12-08: unexplained, section-73, section-96, section-101, section-125
- credit-union-act-1997 2020-12-16: candidates, section-81
- value-added-tax-consolidation-act-2010 2020-12-19: candidates, section-115
- value-added-tax-consolidation-act-2010 2020-12-19: candidates, schedule-1
- value-added-tax-consolidation-act-2010 2020-12-19: candidates, section-46, section-114B
- credit-union-act-1997 2020-12-22: unexplained, section-180, section-181
- investment-funds-companies-and-miscellaneous-provisions-act-2005 2020-12-23: early, section-5, section-6, section-18, section-18B, section-18C, section-18D, section-18E, section-18F, section-18G, section-18H, section-18I, section-18J, section-18K, section-18L, section-18M, section-18N, section-18O, section-18P, section-18Q, section-18R, section-18S, section-18T, section-18U
- industrial-relations-act-1990 2020-12-23: unexplained, section-38, section-39
- investment-funds-companies-and-miscellaneous-provisions-act-2005 2020-12-23: unexplained, section-18A
- central-bank-act-1942 2020-12-28: candidates, section-2
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2020-12-28: candidates, section-24
- companies-act-2014 2020-12-28: candidates, section-1328
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2020-12-29: consolidated late (annotation gives 2014-03-03), section-84
- central-bank-act-1942 2020-12-29: candidates, section-33AK
- central-bank-act-1942 2020-12-29: candidates, section-33ANC
- central-bank-act-1942 2020-12-30: consolidated late (annotation gives 2019-07-05), schedule-10
- companies-act-2014 2020-12-31: early, section-1087A, section-1087B, section-1087C, section-1087D, section-1087E, section-1087F, section-1087G, section-1087H
- extradition-act-1965 2020-12-31: unexplained, section-3, section-14, section-23
- protection-of-employees-employers-insolvency-act-1984 2020-12-31: unexplained, section-1, section-4, section-8A
- defamation-act-2009 2020-12-31: unexplained, schedule-1
- companies-act-2014 2020-12-31: unexplained, section-999, section-1000, section-1101, section-1102, section-1110A, section-1110B, section-1110G, section-1110H, section-1110I, section-1110J, section-1110M, section-1110O, section-1123, section-1129, section-1430
- customs-act-2015 2020-12-31: unexplained, section-12A, section-12B, section-25
- companies-act-2014 2021-01-01: consolidated late (annotation gives 2017-06-09), section-1384A
- companies-act-2014 2021-01-01: consolidated late (annotation gives 2019-03-29), section-1328
- companies-act-2014 2021-01-01: consolidated late (annotation gives 2020-03-30), section-1110J
- electricity-regulation-act-1999 2021-01-01: candidates, section-9
- electricity-regulation-act-1999 2021-01-01: candidates, section-2
- value-added-tax-consolidation-act-2010 2021-01-01: candidates, schedule-3
- value-added-tax-consolidation-act-2010 2021-01-01: early, schedule-2
- electricity-regulation-act-1999 2021-01-01: unexplained, section-9BB, section-43
- veterinary-practice-act-2005 2021-01-01: unexplained, section-43, section-44
- health-and-social-care-professionals-act-2005 2021-01-01: unexplained, section-44A, section-45A, section-99, section-100
- value-added-tax-consolidation-act-2010 2021-01-01: unexplained, section-53, section-53A, section-56, section-58, schedule-9
- student-support-act-2011 2021-01-01: unexplained, section-2, section-7, section-8, section-14, section-14A
- international-protection-act-2015 2021-01-01: unexplained, section-2, section-19, section-21, section-50A, section-51A, section-51B, section-51C, section-72A
- value-added-tax-consolidation-act-2010 2021-01-02: candidates, section-111
- value-added-tax-consolidation-act-2010 2021-01-02: consolidated late (annotation gives 2014-12-23), section-111
- value-added-tax-consolidation-act-2010 2021-01-02: candidates, section-115
- value-added-tax-consolidation-act-2010 2021-01-02: consolidated late (annotation gives 2020-12-19), section-115
- value-added-tax-consolidation-act-2010 2021-01-02: candidates, section-2
- value-added-tax-consolidation-act-2010 2021-01-02: consolidated late (annotation gives 2020-12-19), section-2
- roads-act-1993 2021-01-19: consolidated late (annotation gives 2007-07-11), section-51
- immigration-act-2004 2021-01-28: unexplained, section-2, section-11
- emergency-measures-in-the-public-interest-covid-19-act-2020 2021-02-08: unexplained, section-2, section-3, section-8, section-24, section-25, section-32
- pharmacy-act-2007 2021-02-13: unexplained, section-21B, section-21C
- pharmacy-act-2007 2021-02-14: consolidated late (annotation gives 2018-05-25), section-67
- investment-funds-companies-and-miscellaneous-provisions-act-2005 2021-03-01: unexplained, section-18, section-18A
- sea-fisheries-and-maritime-jurisdiction-act-2006 2021-03-03: consolidated late (annotation gives 2007-05-09), section-17A
- companies-act-2014 2021-03-15: unexplained, section-1101, section-1102, section-1110A, section-1110B, section-1110G, section-1110H, section-1110I, section-1110M, section-1110O, section-1123, section-1129, section-1280A, section-1282, section-1430, section-1431
- planning-and-development-act-2000 2021-03-16: unexplained, section-146C
- health-and-social-care-professionals-act-2005 2021-03-24: unexplained, section-38
- foreshore-act-1933 2021-03-25: candidates, section-1
- foreshore-act-1933 2021-03-25: candidates, section-13A
- health-act-1947 2021-03-26: candidates, section-31A
- central-bank-act-1942 2021-03-29: candidates, section-2
- european-arrest-warrant-act-2003 2021-03-30: candidates, section-10
- adoptive-leave-act-1995 2021-04-01: candidates, section-2
- adoptive-leave-act-1995 2021-04-01: candidates, section-6
- emergency-measures-in-the-public-interest-covid-19-act-2020 2021-04-01: candidates, section-28B
- parental-leave-act-1998 2021-04-01: unexplained, section-7, section-16A, section-17
- children-and-family-relationships-act-2015 2021-04-01: unexplained, section-64
- adoptive-leave-act-1995 2021-04-02: consolidated late (annotation gives 2010-11-01), section-7
- dumping-at-sea-act-1996 2021-04-02: consolidated late (annotation gives 2010-02-15), section-5A
- criminal-justice-theft-and-fraud-offences-act-2001 2021-04-14: unexplained, section-44
- credit-union-act-1997 2021-04-20: unexplained, section-136
- central-bank-act-1942 2021-04-23: candidates, section-33AK
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2021-04-23: candidates, section-60
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2021-04-23: candidates, section-55
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2021-04-23: candidates, section-51
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2021-04-23: early, section-35
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2021-04-23: unexplained, section-8
- central-bank-act-1942 2021-04-24: consolidated late (annotation gives 2019-07-05), schedule-10
- judicial-council-act-2019 2021-04-24: unexplained, section-74
- planning-and-development-act-2000 2021-04-30: early, section-13, section-30, section-51, section-52, section-177X, section-177Y, section-177AB, section-177AC
- planning-and-development-act-2000 2021-04-30: early, section-9A, section-11D, section-12, section-27D, section-31AM, section-177R, section-177S, section-181, schedule-5
- merchant-shipping-act-1894 2021-04-30: unexplained, section-1, section-3, section-38, section-54, section-58, section-62, section-67, section-88, section-126, section-210, section-238, section-258, section-267, section-284, section-286, section-290, section-294, section-300, section-302, section-313, section-375, section-389, section-426, section-445, section-534, section-546, section-585, section-598, section-651, section-722, section-730, section-738, schedule-15, schedule-20
- planning-and-development-act-2000 2021-04-30: unexplained, section-42B, section-176, schedule-6
- children-act-2001 2021-05-07: unexplained, section-183, section-184
- health-act-1970 2021-05-10: unexplained, section-75B, section-75C
- consumer-protection-act-2007 2021-05-20: unexplained, schedule-4, schedule-9
- taxi-regulation-act-2013 2021-05-21: unexplained, section-35
- environmental-protection-agency-act-1992 2021-06-02: unexplained, section-3, section-83, section-86, section-87, section-90, schedule-1
- environmental-protection-agency-act-1992 2021-06-03: consolidated late (annotation gives 2013-04-23), section-82A, section-99J
- environmental-protection-agency-act-1992 2021-06-03: candidates, section-83
- environmental-protection-agency-act-1992 2021-06-03: consolidated late (annotation gives 2020-05-27), section-83
- finance-local-property-tax-act-2012 2021-06-10: unexplained, section-12
- road-traffic-act-1961 2021-06-25: consolidated late (annotation gives 2016-02-08), schedule-2
- personal-insolvency-act-2012 2021-06-25: unexplained, section-140A
- water-services-no-2-act-2013 2021-06-30: unexplained, section-34, section-34A
- value-added-tax-consolidation-act-2010 2021-07-01: candidates, section-116
- value-added-tax-consolidation-act-2010 2021-07-01: candidates, schedule-2
- value-added-tax-consolidation-act-2010 2021-07-01: candidates, section-34
- building-control-regulations-1997 2021-07-01: unexplained, regulation-20F, regulation-20G, schedule-6
- financial-emergency-measures-in-the-public-interest-no-2-act-2009 2021-07-05: unexplained, section-2, section-9A
- residential-tenancies-act-2004 2021-07-09: candidates, section-12
- value-added-tax-consolidation-act-2010 2021-07-19: candidates, section-46
- emergency-measures-in-the-public-interest-covid-19-act-2020 2021-07-19: unexplained, section-2, section-3, section-8, section-24, section-25
- value-added-tax-consolidation-act-2010 2021-07-20: candidates, schedule-1
- value-added-tax-consolidation-act-2010 2021-07-20: consolidated late (annotation gives 2014-01-01), schedule-1
- finance-local-property-tax-act-2012 2021-07-22: candidates, section-35
- finance-local-property-tax-act-2012 2021-07-23: consolidated late (annotation gives 2021-07-22), section-2, section-3, section-4, section-5, section-7, section-7A, section-10A, section-10B, section-14, section-15, section-17, section-19, section-20, section-34, section-35, section-47, section-59, section-131, section-132
- health-act-1947 2021-07-25: candidates, section-31A
- industrial-relations-act-1969 2021-07-29: candidates, section-4
- unfair-dismissals-act-1977 2021-07-29: candidates, section-8
- employment-equality-act-1998 2021-07-29: candidates, section-79
- equal-status-act-2000 2021-07-29: candidates, section-25
- workplace-relations-act-2015 2021-07-29: candidates, section-41
- employment-equality-act-1998 2021-07-29: early, section-20A, section-85B, section-85C
- industrial-relations-act-1946 2021-07-29: unexplained, section-34
- workplace-relations-act-2015 2021-07-29: unexplained, section-76
- unfair-dismissals-act-1977 2021-07-30: consolidated late (annotation gives 1993-10-01), section-6
- nurses-and-midwives-act-2011 2021-08-01: unexplained, section-71
- central-bank-act-1942 2021-08-03: candidates, schedule-2
- criminal-justice-theft-and-fraud-offences-act-2001 2021-08-03: candidates, section-39
- central-bank-act-1942 2021-08-03: unexplained, schedule-4
- criminal-justice-act-2011 2021-08-03: unexplained, section-7
- health-act-2004 2021-08-05: consolidated late (annotation gives 2010-07-03), section-40B, section-40F
- health-act-2004 2021-08-05: candidates, section-40D, section-40E
- health-act-2004 2021-08-05: consolidated late (annotation gives 2011-09-08), section-40D, section-40E
- residential-tenancies-act-2004 2021-08-19: unexplained, section-95, section-135
- local-government-act-2001 2021-09-03: unexplained, section-131A, schedule-12
- civil-liability-act-1961 2021-09-04: consolidated late (annotation gives 2018-10-01), section-51H, section-51I, section-51J, section-51K, section-51L
- planning-and-development-act-2000 2021-09-09: candidates, section-96
- planning-and-development-act-2000 2021-09-09: candidates, section-42
- planning-and-development-housing-and-residential-tenancies-act-2016 2021-09-09: unexplained, section-25A, section-26, section-31, section-38, section-46
- planning-and-development-act-2000 2021-09-10: consolidated late (annotation gives 2021-09-07), section-10
- taxi-regulation-act-2013 2021-09-20: unexplained, section-35
- central-bank-act-1942 2021-09-21: candidates, section-2
- central-bank-act-1942 2021-09-21: candidates, schedule-2
- nursing-homes-support-scheme-act-2009 2021-10-20: candidates, schedule-1
- nursing-homes-support-scheme-act-2009 2021-10-20: candidates, section-45
- central-bank-act-1942 2021-11-04: consolidated late (annotation gives 2019-07-05), schedule-10
- mental-health-act-2001 2021-11-10: candidates, section-2A
- wildlife-act-1976 2021-11-22: candidates, section-2
- dumping-at-sea-act-1996 2021-11-22: early, section-1
- criminal-justice-theft-and-fraud-offences-act-2001 2021-11-22: unexplained, section-3, section-40
- sea-fisheries-and-maritime-jurisdiction-act-2006 2021-11-22: unexplained, section-91, section-92, section-93, section-94, section-95, section-96, section-97, section-98, section-99, section-100, section-101, section-102, section-103, section-104
- sea-pollution-miscellaneous-provisions-act-2006 2021-11-22: unexplained, section-36
- criminal-justice-theft-and-fraud-offences-act-2001 2021-11-23: consolidated late (annotation gives 2021-08-03), section-36
- wildlife-act-1976 2021-11-23: candidates, section-72
- wildlife-act-1976 2021-11-23: consolidated late (annotation gives 2018-07-18), section-72
- criminal-justice-act-2007 2021-12-08: early, section-25
- fisheries-amendment-act-1997 2021-12-08: unexplained, section-48, section-60, section-61
- aviation-regulation-act-2001 2021-12-10: candidates, section-42
- aviation-regulation-act-2001 2021-12-10: consolidated late (annotation gives 2019-03-11), section-42
- aviation-regulation-act-2001 2021-12-10: candidates, section-2
- aviation-regulation-act-2001 2021-12-10: consolidated late (annotation gives 2019-03-11), section-2
- residential-tenancies-act-2004 2021-12-11: candidates, section-19
- central-bank-act-1942 2021-12-13: candidates, section-33AK
- central-bank-act-1942 2021-12-13: candidates, section-2
- central-bank-act-1942 2021-12-13: early, section-33BC
- central-bank-act-1942 2021-12-13: unexplained, section-33AR
- central-bank-act-1942 2021-12-14: consolidated late (annotation gives 2021-12-13), section-33BC
- child-and-family-agency-act-2013 2021-12-15: unexplained, section-53, section-54, schedule-2
- companies-act-2014 2021-12-15: unexplained, section-343, section-998A, section-1000, section-1087A, section-1087B, section-1099, section-1101, section-1110A, section-1110B, section-1110G, section-1110H, section-1110I, section-1110J, section-1110L, section-1110O, section-1110P, section-1267A, section-1280A, section-1282, section-1328, section-1329, section-1430, section-1431, section-1503, schedule-4, schedule-20
- freedom-of-information-act-2014 2021-12-16: consolidated late (annotation gives 2020-10-27), section-42
- companies-act-2014 2021-12-16: consolidated late (annotation gives 2018-05-25), section-957A
- companies-act-2014 2021-12-16: consolidated late (annotation gives 2020-03-30), section-1099, section-1110J, section-1110L
- planning-and-development-act-2000 2021-12-17: candidates, section-34
- planning-and-development-act-2000 2021-12-17: candidates, section-2
- planning-and-development-act-2000 2021-12-17: unexplained, section-96
- planning-and-development-amendment-act-2018 2021-12-17: unexplained, section-33, section-34
- value-added-tax-consolidation-act-2010 2021-12-21: candidates, section-101
- value-added-tax-consolidation-act-2010 2021-12-21: candidates, section-115
- value-added-tax-consolidation-act-2010 2021-12-21: candidates, section-116
- ministers-and-secretaries-amendment-act-2011 2021-12-21: candidates, section-101
- registration-of-title-act-1964 2021-12-23: unexplained, section-103
- foreshore-amendment-act-1992 2021-12-23: unexplained, section-1A
- firearms-act-1964 2021-12-27: candidates, section-27A
- firearms-and-offensive-weapons-act-1990 2021-12-27: candidates, section-12A
- credit-institutions-stabilisation-act-2010 2021-12-31: unexplained, section-76
- bail-act-1997 2022-01-01: consolidated late (annotation gives 2017-08-14), section-9A
- value-added-tax-consolidation-act-2010 2022-01-01: candidates, schedule-2
- value-added-tax-consolidation-act-2010 2022-01-01: unexplained, section-91C, section-91D, section-91H, section-91I, section-91J, section-91K
- credit-guarantee-act-2012 2022-01-01: unexplained, section-3, section-12
- criminal-justice-act-1993 2022-01-02: consolidated late (annotation gives 2006-08-01), section-2
- national-oil-reserves-agency-act-2007 2022-01-02: consolidated late (annotation gives 2016-11-30), section-44H
- value-added-tax-consolidation-act-2010 2022-01-02: candidates, schedule-2
- value-added-tax-consolidation-act-2010 2022-01-02: consolidated late (annotation gives 2020-12-19), schedule-2
- health-act-1970 2022-01-07: unexplained, section-75B
- health-act-1947 2022-01-08: early, section-2
- health-act-1947 2022-01-08: unexplained, section-38B, section-38C, section-38D, section-38E, section-38F, section-38G, section-38H, section-38I, section-38J, section-38K, section-38L, section-38M, section-38N, section-38O, section-38P, section-38Q, section-38R, section-38S, section-38T, section-38U, section-38V, section-38W, section-38X, section-38Y, section-38Z, section-42
- garda-s-och-na-act-2005 2022-01-11: unexplained, section-125
- road-traffic-act-2010 2022-02-01: unexplained, section-54
- housing-miscellaneous-provisions-act-2014 2022-02-01: unexplained, section-1, section-2
- water-services-act-2014 2022-02-01: unexplained, section-3A, section-3B
- central-bank-act-1942 2022-02-03: candidates, schedule-2
- central-bank-act-1942 2022-02-03: unexplained, schedule-4
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2022-02-03: unexplained, section-33A
- central-bank-act-1942 2022-02-04: consolidated late (annotation gives 2019-07-05), schedule-10
- central-bank-act-1942 2022-02-04: candidates, section-33AK
- central-bank-act-1942 2022-02-04: consolidated late (annotation gives 2013-08-01), section-33AK
- merchant-shipping-safety-convention-act-1952 2022-02-08: unexplained, section-19
- waste-management-act-1996 2022-02-10: consolidated late (annotation gives 2014-01-07), section-2
- electricity-regulation-act-1999 2022-02-15: candidates, section-9
- immigration-act-2004 2022-02-25: unexplained, section-2
- immigration-act-2004 2022-02-26: consolidated late (annotation gives 2016-03-10), section-4
- criminal-procedure-act-1967 2022-02-28: candidates, section-4E
- criminal-procedure-act-1967 2022-02-28: candidates, section-4A
- criminal-justice-act-1984 2022-02-28: candidates, section-21
- criminal-procedure-act-2010 2022-02-28: candidates, section-23
- criminal-procedure-act-1967 2022-02-28: unexplained, section-34
- road-traffic-act-1961 2022-03-01: unexplained, section-72, section-72A
- health-act-1970 2022-03-02: consolidated late (annotation gives 2005-01-01), section-83
- health-act-1970 2022-03-02: consolidated late (annotation gives 2011-01-04), section-75B
- road-traffic-act-1961 2022-03-02: candidates, section-38
- road-traffic-act-1961 2022-03-02: consolidated late (annotation gives 2015-06-22), section-38
- extradition-act-1965 2022-03-30: unexplained, section-44, section-44A
- public-service-pensions-single-scheme-and-other-provisions-act-2012 2022-04-01: consolidated late (annotation gives 2022-03-31), schedule-1
- consumer-protection-act-2007 2022-04-01: unexplained, schedule-9
- residential-tenancies-act-2004 2022-04-04: candidates, section-134
- defence-act-1954 2022-04-04: unexplained, section-12, section-13, section-124
- central-bank-reform-act-2010 2022-04-04: unexplained, schedule-1, schedule-2, schedule-3
- health-act-2007 2022-04-12: unexplained, section-73
- firearms-act-1925 2022-04-27: candidates, section-10
- firearms-act-1925 2022-04-27: candidates, section-1
- firearms-act-1925 2022-04-27: candidates, section-2A
- firearms-act-1925 2022-04-27: candidates, section-21
- irish-aviation-authority-act-1993 2022-05-02: consolidated late (annotation gives 2006-04-04), section-14, section-67
- irish-aviation-authority-act-1993 2022-05-02: consolidated late (annotation gives 2022-05-01), section-63C, section-63D, section-63F
- firearms-act-1925 2022-05-04: unexplained, section-24, section-25, section-25CA
- consumer-credit-act-1995 2022-05-16: candidates, section-2
- consumer-credit-act-1995 2022-05-16: candidates, section-3, section-9
- consumer-credit-act-1995 2022-05-16: candidates, section-12
- central-bank-act-1997 2022-05-16: candidates, section-28
- central-bank-act-1997 2022-05-16: candidates, section-34G
- wildlife-act-1976 2022-05-16: unexplained, section-29
- consumer-credit-act-1995 2022-05-16: unexplained, schedule-7, schedule-8
- central-bank-act-1997 2022-05-16: unexplained, section-36F
- financial-services-and-pensions-ombudsman-act-2017 2022-05-16: unexplained, section-45, section-52
- wildlife-act-1976 2022-05-17: consolidated late (annotation gives 2001-07-31), section-2
- employment-equality-act-1998 2022-05-31: unexplained, section-14A
- value-added-tax-consolidation-act-2010 2022-06-02: candidates, section-46
- emergency-measures-in-the-public-interest-covid-19-act-2020 2022-06-02: candidates, section-28C
- emergency-measures-in-the-public-interest-covid-19-act-2020 2022-06-02: candidates, section-28B
- emergency-measures-in-the-public-interest-covid-19-act-2020 2022-06-02: unexplained, section-2, section-3, section-8, section-24, section-25
- planning-and-development-act-2000 2022-06-23: unexplained, section-2, section-90, section-112A, section-128, section-177, section-177A, section-177N, section-177O, section-178A, section-182E, section-202, section-278, section-279, section-280, section-281, section-282, section-283, section-284, section-285, section-286, section-287, section-288, section-289, section-290, section-291, section-292, section-293, section-294, section-295, section-296, section-297, section-298, section-299, section-300, section-301, section-302, section-303, section-305, section-306, section-307, section-308, section-309, section-310, section-311, section-312, section-313, section-314, section-315, section-316, section-317, section-318, section-319, section-321, schedule-8, schedule-9
- forestry-act-2014 2022-06-29: early, section-22A, schedule-1
- forestry-act-2014 2022-06-29: unexplained, section-6, section-6A
- succession-act-1965 2022-06-30: candidates, section-4A
- veterinary-practice-act-2005 2022-07-01: unexplained, section-43, section-44
- paternity-leave-and-benefit-act-2016 2022-07-01: unexplained, section-1, section-2
- value-added-tax-consolidation-act-2010 2022-07-02: consolidated late (annotation gives 2019-12-22), section-108
- value-added-tax-consolidation-act-2010 2022-07-02: consolidated late (annotation gives 2021-12-21), section-116A
- value-added-tax-consolidation-act-2010 2022-07-02: candidates, section-115
- value-added-tax-consolidation-act-2010 2022-07-02: consolidated late (annotation gives 2017-01-01), section-115
- residential-tenancies-act-2004 2022-07-06: candidates, section-35
- companies-act-2014 2022-07-06: candidates, section-2
- defence-act-1954 2022-07-06: unexplained, section-77, section-86A, schedule-6, schedule-7, schedule-11
- courts-martial-appeals-act-1983 2022-07-06: unexplained, section-27B
- electricity-regulation-act-1999 2022-07-11: candidates, section-39
- housing-miscellaneous-provisions-act-2014 2022-07-11: unexplained, section-1, section-2
- data-protection-act-1988 2022-07-12: unexplained, section-9
- national-oil-reserves-agency-act-2007 2022-07-15: candidates, section-44I
- national-oil-reserves-agency-act-2007 2022-07-15: candidates, section-44G
- finance-local-property-tax-act-2012 2022-07-18: unexplained, section-38, section-61
- national-vetting-bureau-children-and-vulnerable-persons-act-2012 2022-07-20: consolidated late (annotation gives 2019-01-01), schedule-3
- planning-and-development-act-2000 2022-07-24: candidates, section-7
- education-act-1998 2022-07-25: candidates, section-67, section-68, section-69
- valuation-act-2001 2022-07-25: candidates, section-3
- valuation-act-2001 2022-07-25: consolidated late (annotation gives 2019-01-31), section-3
- education-for-persons-with-special-educational-needs-act-2004 2022-07-25: candidates, section-20
- education-act-1998 2022-07-25: unexplained, section-70
- data-protection-act-2018 2022-07-25: unexplained, section-117A
- residential-tenancies-act-2004 2022-07-26: unexplained, section-29, section-30, section-64B
- road-traffic-act-1961 2022-07-27: candidates, section-3
- companies-act-2014 2022-07-27: candidates, section-534
- companies-act-2014 2022-07-27: unexplained, section-343, section-888A, section-1087B, section-1110A, section-1110B, section-1110G, section-1110H, section-1110I, section-1110O, section-1110P, section-1448, section-1449, schedule-20, schedule-21
- organisation-of-working-time-act-1997 2022-07-28: consolidated late (annotation gives 2001-07-02), section-15, section-16
- sea-fisheries-and-maritime-jurisdiction-act-2006 2022-07-28: candidates, section-28
- electricity-regulation-act-1999 2022-07-31: candidates, section-2
- electricity-regulation-act-1999 2022-07-31: candidates, section-37
- electricity-regulation-act-1999 2022-07-31: candidates, section-14
- electricity-regulation-act-1999 2022-07-31: unexplained, section-66, schedule-1, schedule-1A
- dublin-transport-authority-act-2008 2022-08-01: unexplained, section-53, section-54
- environmental-protection-agency-act-1992 2022-08-24: candidates, section-87
- central-bank-act-1942 2022-08-28: candidates, section-2
- central-bank-act-1942 2022-08-28: candidates, schedule-2
- central-bank-act-1942 2022-08-28: candidates, section-33BC
- building-control-act-2007 2022-08-29: candidates, section-2
- central-bank-act-1942 2022-08-31: unexplained, section-33ANF, section-33ANG, section-33AR, section-33AS, section-57AE
- communications-regulation-act-2002 2022-09-06: early, section-39A, section-40A, section-40B
- communications-regulation-act-2002 2022-09-06: early, section-11A, section-31D
- communications-regulation-act-2002 2022-09-06: unexplained, section-2, section-10
- industrial-relations-act-1946 2022-09-15: unexplained, section-57
- animal-health-and-welfare-act-2013 2022-09-19: early, section-71A, section-71B, section-71C, section-71D, section-71E, section-71F, section-71G, section-71H, section-71I, section-71J, section-71K, section-71L, section-71M
- child-care-act-1991 2022-09-21: candidates, section-29
- health-act-1970 2022-09-21: unexplained, section-45A, section-46, section-63, section-64, section-84
- child-care-act-1991 2022-09-21: unexplained, section-2, section-24A, section-35A, section-35B, section-35C, section-35D, section-35E, section-35F, section-35G, section-35H, section-35I, section-35J, section-35K, section-35M, section-35N, section-35O, section-35P, section-35Q
- planning-and-development-act-2000 2022-10-01: candidates, section-35
- planning-and-development-act-2000 2022-10-01: candidates, section-156
- planning-and-development-act-2000 2022-10-01: candidates, section-12
- planning-and-development-act-2000 2022-10-01: candidates, section-31
- planning-and-development-act-2000 2022-10-01: candidates, section-4
- planning-and-development-act-2000 2022-10-01: candidates, section-31AM, section-144
- planning-and-development-act-2000 2022-10-01: candidates, section-177U, section-177AE
- civil-registration-act-2004 2022-10-03: candidates, section-13
- wildlife-act-1976 2022-10-03: unexplained, section-72
- civil-registration-act-2004 2022-10-03: unexplained, section-2, schedule-2
- judicial-council-act-2019 2022-10-03: unexplained, section-74
- wildlife-act-1976 2022-10-04: consolidated late (annotation gives 2001-07-31), section-2
- civil-registration-act-2004 2022-10-04: candidates, section-2
- civil-registration-act-2004 2022-10-04: consolidated late (annotation gives 2019-01-01), section-2
- national-minimum-wage-act-2000 2022-10-07: consolidated late (annotation gives 2001-07-02), section-8
- national-oil-reserves-agency-act-2007 2022-10-18: unexplained, section-2
- greyhound-industry-act-1958 2022-10-19: unexplained, section-45, section-47, section-50
- terms-of-employment-information-act-1994 2022-10-27: candidates, section-3
- road-traffic-act-1961 2022-10-27: unexplained, section-97
- road-traffic-act-2010 2022-10-27: unexplained, section-54
- road-traffic-act-2010 2022-10-28: consolidated late (annotation gives 2014-03-20), section-81, section-87
- road-traffic-act-2010 2022-10-28: consolidated late (annotation gives 2017-06-01), section-34
- environmental-protection-agency-act-1992 2022-10-31: unexplained, section-82, section-111
- nursing-homes-support-scheme-act-2009 2022-11-01: candidates, schedule-1
- regional-technical-colleges-act-1992 2022-11-10: candidates, section-7
- student-support-act-2011 2022-11-10: candidates, section-28
- industrial-training-act-1967 2022-11-10: unexplained, schedule-1, schedule-2
- consumer-credit-act-1995 2022-11-14: candidates, section-144
- consumer-credit-act-1995 2022-11-14: candidates, section-93
- credit-institutions-stabilisation-act-2010 2022-11-17: unexplained, section-64, section-65, schedule-1, schedule-2
- consumer-credit-act-1995 2022-11-29: candidates, section-2
- communications-regulation-act-2002 2022-11-29: candidates, section-39
- communications-regulation-act-2002 2022-11-29: candidates, section-10
- consumer-protection-act-2007 2022-11-29: candidates, section-55
- consumer-protection-act-2007 2022-11-29: candidates, section-90
- consumer-protection-act-2007 2022-11-29: candidates, section-2
- consumer-protection-act-2007 2022-11-29: candidates, schedule-4, schedule-5
- consumer-protection-act-2007 2022-11-29: candidates, section-67
- consumer-protection-act-2007 2022-11-29: candidates, section-85
- sale-of-goods-act-1893 2022-11-29: unexplained, long-title, section-2, schedule-1
- package-holidays-and-travel-trade-act-1995 2022-11-29: unexplained, section-20, schedule-4
- consumer-credit-act-1995 2022-11-29: unexplained, schedule-2
- consumer-protection-act-2007 2022-11-29: unexplained, section-74A
- consumer-credit-act-1995 2022-11-30: candidates, section-2
- consumer-credit-act-1995 2022-11-30: consolidated late (annotation gives 2022-11-29), section-2
- central-bank-act-1942 2022-12-05: candidates, schedule-2
- central-bank-act-1942 2022-12-05: candidates, section-33AK
- credit-guarantee-act-2012 2022-12-08: candidates, section-3
- animal-health-and-welfare-act-2013 2022-12-09: candidates, section-2
- animal-health-and-welfare-act-2013 2022-12-09: candidates, schedule-3
- value-added-tax-consolidation-act-2010 2022-12-15: candidates, section-59
- value-added-tax-consolidation-act-2010 2022-12-15: candidates, section-46
- value-added-tax-consolidation-act-2010 2022-12-15: candidates, section-65
- value-added-tax-consolidation-act-2010 2022-12-15: early, schedule-1
- value-added-tax-consolidation-act-2010 2022-12-15: early, schedule-3
- value-added-tax-consolidation-act-2010 2022-12-15: early, schedule-2
- value-added-tax-consolidation-act-2010 2022-12-15: early, section-86
- value-added-tax-consolidation-act-2010 2022-12-15: unexplained, section-91D, section-91H, section-91J
- terms-of-employment-information-act-1994 2022-12-16: unexplained, section-1, section-2, section-3A, section-4, section-5, section-5A, section-6D, section-6E, section-6F, section-6G, section-6H, section-6I, section-7
- employment-permits-act-2006 2022-12-16: unexplained, section-10
- irish-human-rights-and-equality-commission-act-2014 2022-12-17: unexplained, section-2
- planning-and-development-act-2000 2022-12-20: candidates, section-173A, section-181, section-181B
- foreshore-act-1933 2022-12-20: early, section-1E, section-13C
- planning-and-development-act-2000 2022-12-20: early, section-2
- planning-and-development-act-2000 2022-12-20: early, section-173D
- foreshore-act-1933 2022-12-20: unexplained, section-13A
- planning-and-development-act-2000 2022-12-20: unexplained, section-32H, section-32I, section-32J, section-32K, section-32L, section-37CC, section-37CD, section-37CE, section-105A, section-107A, section-179A, section-182F, section-182G, section-182H, section-247, schedule-6
- maternity-protection-act-1994 2022-12-21: early, section-30A
- aviation-regulation-act-2001 2022-12-22: candidates, section-33
- aviation-regulation-act-2001 2022-12-22: candidates, section-45A
- aviation-regulation-act-2001 2022-12-22: unexplained, section-7, section-10, section-17, section-27A, section-27B, section-33A, section-35, section-36, section-38, section-39A
- animal-health-and-welfare-act-2013 2022-12-22: unexplained, section-70, section-71M
- health-insurance-act-1994 2023-01-01: candidates, section-18F
- protected-disclosures-act-2014 2023-01-01: candidates, section-3
- workplace-relations-act-2015 2023-01-01: candidates, schedule-6
- workplace-relations-act-2015 2023-01-01: candidates, schedule-5
- workplace-relations-act-2015 2023-01-01: candidates, schedule-1
- health-insurance-act-1994 2023-01-01: early, section-6B
- health-act-1970 2023-01-01: unexplained, section-75B
- social-welfare-consolidated-contributions-and-insurability-regulations-1996 2023-01-01: unexplained, schedule-A
- financial-emergency-measures-in-the-public-interest-act-2010 2023-01-01: unexplained, section-2A
- water-services-act-2013 2023-01-01: unexplained, section-8, section-10, section-11, section-16A, section-18A, section-22
- taxi-regulation-act-2013 2023-01-01: unexplained, section-30
- companies-act-2014 2023-01-01: unexplained, section-115, section-343, section-987, section-1000, section-1087A, section-1110A, section-1110H, section-1110O, section-1123, section-1129, section-1282, section-1328, section-1329, section-1428A, section-1430
- workplace-relations-act-2015 2023-01-01: unexplained, section-76, schedule-7
- health-act-1970 2023-01-02: consolidated late (annotation gives 2009-01-01), section-45A
- health-act-1970 2023-01-02: consolidated late (annotation gives 2017-01-01), section-53C
- gas-act-1976 2023-01-02: consolidated late (annotation gives 2015-11-23), section-7C, section-21
- freedom-of-information-act-2014 2023-01-02: candidates, section-42
- freedom-of-information-act-2014 2023-01-02: consolidated late (annotation gives 2023-01-01), section-42
- international-interests-in-mobile-equipment-cape-town-convention-act-2005 2023-01-09: unexplained, schedule-2
- national-economic-and-social-development-office-act-2006 2023-01-09: unexplained, section-20
- energy-miscellaneous-provisions-act-2006 2023-01-09: unexplained, schedule-1
- social-welfare-and-pensions-act-2007 2023-01-09: unexplained, schedule-2, schedule-3
- local-government-charges-act-2009 2023-01-09: unexplained, section-15
- planning-and-development-act-2000 2023-01-10: candidates, section-104
- affordable-housing-act-2021 2023-01-27: unexplained, section-33
- financial-services-and-pensions-ombudsman-act-2017 2023-02-01: unexplained, section-45, section-46
- sea-fisheries-and-maritime-jurisdiction-act-2006 2023-02-08: unexplained, section-90, section-91, section-92, section-93, section-94, section-95, section-96, section-97, section-98, section-99, section-100, section-101, section-102, section-103, section-104
- electricity-regulation-act-1999 2023-02-20: unexplained, long-title, section-62
- national-oil-reserves-agency-act-2007 2023-02-28: candidates, section-43A
- national-oil-reserves-agency-act-2007 2023-02-28: candidates, section-44G
- national-oil-reserves-agency-act-2007 2023-02-28: candidates, section-2
- national-oil-reserves-agency-act-2007 2023-02-28: candidates, section-44D
- valuation-act-2001 2023-03-01: candidates, section-68
- valuation-act-2001 2023-03-01: candidates, section-53
- health-act-2004 2023-03-01: candidates, section-40C
- health-act-2004 2023-03-01: candidates, section-31
- health-act-2004 2023-03-01: candidates, section-10AA, section-35
- health-act-2007 2023-03-01: candidates, section-2
- health-act-2007 2023-03-01: candidates, section-100
- registration-of-title-act-1964 2023-03-01: unexplained, section-103
- health-act-2004 2023-03-01: unexplained, section-39
- digital-hub-development-agency-act-2003 2023-03-08: unexplained, schedule-1
- planning-and-development-act-2000 2023-03-10: unexplained, section-2, schedule-6
- official-languages-act-2003 2023-03-13: candidates, schedule-1
- broadcasting-act-2009 2023-03-15: candidates, section-106, section-127
- broadcasting-act-2009 2023-03-15: unexplained, section-18, section-46I, section-139ZZE, section-185, schedule-1, schedule-4
- residential-tenancies-amendment-act-2015 2023-03-15: unexplained, section-71, section-76
- private-security-services-act-2004 2023-03-31: candidates, section-2
- health-insurance-act-1994 2023-04-01: unexplained, section-6B, section-11G, section-12, schedule-4
- adoption-act-2010 2023-04-04: unexplained, section-18
- personal-injuries-assessment-board-act-2003 2023-04-10: candidates, section-4
- personal-injuries-assessment-board-act-2003 2023-04-10: candidates, section-54
- personal-injuries-assessment-board-act-2003 2023-04-10: candidates, section-73
- personal-injuries-assessment-board-act-2003 2023-04-10: unexplained, section-18A, section-18B, section-18C, section-18D, section-18E, section-18F
- personal-injuries-assessment-board-act-2003 2023-04-11: consolidated late (annotation gives 2023-04-10), section-21
- health-act-1970 2023-04-17: unexplained, section-46, section-63, section-64, section-75B, section-83, section-84
- environmental-protection-agency-act-1992 2023-04-18: unexplained, section-52, section-59, section-81A
- central-bank-act-1942 2023-04-19: candidates, section-33AX
- central-bank-act-1942 2023-04-19: candidates, section-33AK
- central-bank-act-1942 2023-04-19: candidates, section-33ANH, section-61G, schedule-2
- central-bank-act-1942 2023-04-19: candidates, section-2, section-33BA
- central-bank-act-1942 2023-04-19: candidates, section-33BC
- central-bank-act-1942 2023-04-20: unexplained, section-33AM, section-33BG, section-57AE
- central-bank-act-1942 2023-04-21: consolidated late (annotation gives 2014-11-04), section-33AK
- assisted-decision-making-capacity-act-2015 2023-04-26: candidates, section-2
- credit-union-act-1997 2023-04-26: unexplained, section-37F
- mental-health-act-2001 2023-04-26: unexplained, section-17, section-18, section-28, section-48, section-49, section-58
- assisted-decision-making-capacity-act-2015 2023-04-26: unexplained, long-title
- road-traffic-and-transport-act-2006 2023-04-27: unexplained, long-title, section-1
- water-services-act-2007 2023-04-28: candidates, section-16
- irish-aviation-authority-act-1993 2023-05-01: candidates, section-2
- value-added-tax-consolidation-act-2010 2023-05-01: candidates, schedule-2
- irish-aviation-authority-act-1993 2023-05-01: unexplained, section-69, section-74C, section-74D
- aviation-regulation-act-2001 2023-05-01: unexplained, section-27A
- health-act-2007 2023-05-02: early, section-41A, section-77A, section-101A
- health-act-2007 2023-05-02: unexplained, section-8, section-73
- transfer-of-execution-of-sentences-act-2005 2023-05-03: candidates, section-1, section-10
- criminal-justice-act-2007 2023-05-03: candidates, section-25
- criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2023-05-03: candidates, section-31
- criminal-law-sexual-offences-act-2017 2023-05-03: candidates, section-58
- children-act-2001 2023-05-03: unexplained, section-226A
- european-arrest-warrant-act-2003 2023-05-03: unexplained, section-2, section-20, section-45B
- criminal-justice-mutual-assistance-act-2008 2023-05-03: unexplained, section-2, schedule-5A, schedule-5B, schedule-7A
- criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2023-05-03: unexplained, section-1, section-2, section-86, section-87, section-127, section-167, section-168, schedule-2
- parole-act-2019 2023-05-03: unexplained, section-18, section-19
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2023-05-05: consolidated late (annotation gives 2023-01-01), regulation-56, regulation-136
- industrial-relations-act-1946 2023-05-11: unexplained, section-34, section-45B, section-45C, section-45D
- national-treasury-management-agency-amendment-act-2000 2023-05-11: unexplained, section-11A
- criminal-justice-terrorist-offences-act-2005 2023-05-11: unexplained, schedule-1, schedule-3
- maritime-area-planning-act-2021 2023-05-15: unexplained, schedule-1, schedule-12
- road-safety-authority-commercial-vehicle-roadworthiness-act-2012 2023-05-16: unexplained, section-3
- road-traffic-act-1961 2023-05-17: consolidated late (annotation gives 1970-10-26), section-60
- road-traffic-act-1961 2023-05-17: consolidated late (annotation gives 2006-07-21), section-23A
- road-traffic-act-1961 2023-05-17: consolidated late (annotation gives 2011-06-01), section-22B
- road-traffic-act-1961 2023-05-17: candidates, section-26
- road-traffic-act-1961 2023-05-17: consolidated late (annotation gives 2017-04-13), section-26
- workplace-relations-act-2015 2023-05-24: candidates, schedule-6
- workplace-relations-act-2015 2023-05-24: candidates, schedule-5
- safety-health-and-welfare-at-work-act-2005 2023-05-24: unexplained, section-54A, section-55
- safety-health-and-welfare-at-work-general-application-regulations-2007 2023-05-24: unexplained, schedule-15
- workplace-relations-act-2015 2023-05-24: unexplained, schedule-2
- workplace-relations-act-2015 2023-05-25: consolidated late (annotation gives 2023-01-01), schedule-5
- veterinary-practice-act-2005 2023-06-02: consolidated late (annotation gives 2012-07-18), section-44
- veterinary-practice-act-2005 2023-06-02: consolidated late (annotation gives 2016-03-09), section-43
- communications-regulation-act-2002 2023-06-09: candidates, section-13D
- communications-regulation-act-2002 2023-06-09: candidates, section-2
- communications-regulation-act-2002 2023-06-09: candidates, section-10
- communications-regulation-act-2002 2023-06-09: candidates, schedule-1
- communications-regulation-act-2002 2023-06-09: candidates, section-30
- communications-regulation-act-2002 2023-06-09: early, section-39
- sea-fisheries-and-maritime-jurisdiction-act-2006 2023-06-20: unexplained, section-15P
- communications-retention-of-data-act-2011 2023-06-26: candidates, section-10
- communications-retention-of-data-act-2011 2023-06-26: unexplained, section-7, section-7B, section-7D
- central-bank-reform-act-2010 2023-06-27: early, section-17A, section-53A, section-53B, section-53C, section-53D, section-53E, section-53F, section-53G, section-53H, section-53I
- waste-management-act-1996 2023-07-01: candidates, section-7
- waste-management-act-1996 2023-07-01: candidates, section-5
- waste-management-act-1996 2023-07-01: unexplained, section-14A, section-14B, section-14D, section-39, section-40
- litter-pollution-act-1997 2023-07-01: unexplained, section-23A, section-23C
- waste-management-act-1996 2023-07-02: consolidated late (annotation gives 2023-07-01), section-72
- redundancy-payments-act-1967 2023-07-03: candidates, schedule-3
- adoptive-leave-act-1995 2023-07-03: candidates, section-9
- adoptive-leave-act-1995 2023-07-03: candidates, section-19
- parental-leave-act-1998 2023-07-03: candidates, section-2
- unfair-dismissals-act-1977 2023-07-03: unexplained, section-2
- adoptive-leave-act-1995 2023-07-03: unexplained, section-34, section-35, section-36, section-37, section-38, section-39, section-40, section-41, section-45
- parental-leave-act-1998 2023-07-03: unexplained, section-13AA, section-13B, section-13C, section-13D, section-13E, section-13F, section-13G, section-13H, section-17, section-19, section-20, section-21A, section-22, section-23, section-24
- irish-human-rights-and-equality-commission-act-2014 2023-07-03: unexplained, section-2, schedule-3, schedule-4
- parental-leave-act-1998 2023-07-04: consolidated late (annotation gives 2023-07-03), section-14
- companies-act-2014 2023-07-04: unexplained, section-292, section-998A, section-1000, section-1348, section-1431
- arbitration-act-2010 2023-07-05: unexplained, section-5A
- central-bank-act-1942 2023-07-10: unexplained, section-33AM
- roads-act-1993 2023-07-17: candidates, section-13
- foreshore-amendment-act-1992 2023-07-17: unexplained, section-1A, section-5, section-6
- planning-and-development-amendment-act-2018 2023-07-17: unexplained, schedule-2
- health-and-social-care-professionals-act-2005 2023-07-18: unexplained, section-91B
- planning-and-development-act-2000 2023-07-25: consolidated late (annotation gives 2022-10-01), section-280, section-285, section-286, section-287
- road-traffic-act-1961 2023-07-31: candidates, section-95
- bankruptcy-act-1988 2023-07-31: candidates, section-56
- bankruptcy-act-1988 2023-07-31: candidates, section-3
- roads-act-1993 2023-07-31: candidates, section-19
- roads-act-1993 2023-07-31: candidates, section-2
- road-traffic-act-2002 2023-07-31: candidates, schedule-1
- road-traffic-act-2004 2023-07-31: candidates, section-9
- bankruptcy-act-1988 2023-07-31: unexplained, section-61A
- road-traffic-act-2002 2023-07-31: unexplained, section-21, section-22
- legal-services-regulation-act-2015 2023-07-31: unexplained, section-52, section-53
- international-protection-act-2015 2023-07-31: unexplained, section-2
- firearms-act-1925 2023-08-01: candidates, section-2
- firearms-act-1925 2023-08-01: candidates, section-4B
- road-traffic-act-2002 2023-08-01: candidates, schedule-1
- road-traffic-act-2002 2023-08-01: consolidated late (annotation gives 2023-07-31), schedule-1
- communications-retention-of-data-act-2011 2023-08-01: candidates, section-1, section-6, section-6D, section-6F, section-7A, section-7B, section-12G, section-12I
- affordable-housing-act-2021 2023-08-01: unexplained, section-33
- ministers-and-secretaries-amendment-act-2011 2023-08-02: early, section-101
- employment-equality-act-1998 2023-08-09: unexplained, section-14A
- maritime-area-planning-act-2021 2023-08-14: unexplained, section-4, schedule-12
- health-act-1947 2023-08-17: unexplained, section-54
- local-government-reform-act-2014 2023-08-21: unexplained, section-12, section-61, section-69, section-70, schedule-1, schedule-2, schedule-3
- roads-act-1993 2023-08-31: unexplained, section-77A
- child-care-act-1991 2023-09-02: candidates, section-29
- child-care-act-1991 2023-09-02: consolidated late (annotation gives 2022-09-21), section-29
- industrial-relations-act-1946 2023-09-04: unexplained, section-52
- forestry-act-2014 2023-09-06: candidates, section-2
- central-bank-act-1942 2023-09-07: consolidated late (annotation gives 2013-08-01), section-2
- data-protection-act-1988 2023-09-07: unexplained, section-9
- road-traffic-act-1968 2023-09-13: unexplained, section-18A, schedule-1, schedule-2
- waste-management-act-1996 2023-09-22: unexplained, section-34C, section-39, section-40
- competition-act-2002 2023-09-27: candidates, section-8
- competition-act-2002 2023-09-27: candidates, section-18, section-20
- communications-regulation-act-2002 2023-09-27: candidates, section-39
- statute-of-limitations-amendment-act-1991 2023-09-27: unexplained, section-5A
- value-added-tax-consolidation-act-2010 2023-10-11: candidates, section-46
- defence-act-1954 2023-10-14: consolidated late (annotation gives 2008-09-01), section-177A
- chemicals-act-2008 2023-10-26: candidates, section-8
- irish-horseracing-industry-1994 2023-11-01: consolidated late (annotation gives 2017-01-01), section-10
- irish-horseracing-industry-1994 2023-11-01: consolidated late (annotation gives 2016-03-09), section-48
- criminal-evidence-act-1992 2023-11-01: candidates, section-12
- criminal-justice-public-order-act-1994 2023-11-01: candidates, section-23A
- criminal-justice-public-order-act-1994 2023-11-01: candidates, section-19
- criminal-justice-public-order-act-1994 2023-11-01: candidates, section-24
- bail-act-1997 2023-11-01: candidates, schedule-1
- criminal-law-insanity-act-2006 2023-11-01: candidates, schedule-1
- criminal-justice-act-2007 2023-11-01: candidates, section-50
- succession-act-1965 2023-11-01: unexplained, section-51, section-53
- bail-act-1997 2023-11-01: unexplained, section-9B
- criminal-justice-theft-and-fraud-offences-act-2001 2023-11-01: unexplained, section-39
- technological-universities-act-2018 2023-11-01: unexplained, schedule-2
- valuation-act-2001 2023-11-06: candidates, section-56
- wildlife-act-1976 2023-11-24: consolidated late (annotation gives 2001-07-31), section-51
- central-bank-supervision-and-enforcement-act-2013 2023-11-28: unexplained, section-48, section-51, schedule-2, schedule-4
- criminal-evidence-act-1992 2023-12-01: consolidated late (annotation gives 2019-01-01), section-12
- criminal-justice-victims-of-crime-act-2017 2023-12-01: consolidated late (annotation gives 2019-01-01), section-2
- garda-s-och-na-act-2005 2023-12-05: unexplained, section-33D, section-33E
- education-act-1998 2023-12-12: unexplained, section-67
- personal-injuries-assessment-board-act-2003 2023-12-14: candidates, section-14
- personal-injuries-assessment-board-act-2003 2023-12-14: unexplained, section-18A
- planning-and-development-act-2000 2023-12-16: candidates, section-156
- planning-and-development-act-2000 2023-12-16: candidates, section-104
- value-added-tax-consolidation-act-2010 2023-12-18: candidates, section-120
- value-added-tax-consolidation-act-2010 2023-12-18: candidates, schedule-1
- road-traffic-act-1961 2023-12-23: candidates, section-78A
- road-traffic-act-1961 2023-12-23: unexplained, section-23C, section-23D, section-23E, section-34, section-36, section-100A
- road-traffic-act-1961 2023-12-24: consolidated late (annotation gives 1994-07-22), section-110
- road-traffic-act-1961 2023-12-24: consolidated late (annotation gives 2011-06-01), section-108
- road-traffic-act-1961 2023-12-24: candidates, section-47
- road-traffic-act-1961 2023-12-24: consolidated late (annotation gives 2011-06-01), section-47
- road-traffic-act-1961 2023-12-24: candidates, schedule-2
- road-traffic-act-1961 2023-12-24: consolidated late (annotation gives 2014-11-26), schedule-2
- central-bank-act-1942 2023-12-30: candidates, section-33AK
- central-bank-act-1942 2023-12-30: unexplained, section-33AM
- central-bank-act-1997 2023-12-30: unexplained, section-44, section-61, section-80
- planning-and-development-act-2000 2023-12-31: candidates, section-281
- maritime-area-planning-act-2021 2023-12-31: candidates, section-3
- electricity-regulation-act-1999 2023-12-31: unexplained, section-2
- planning-and-development-act-2000 2023-12-31: unexplained, section-182AA, section-278A, schedule-6
- value-added-tax-consolidation-act-2010 2024-01-01: candidates, schedule-3
- value-added-tax-consolidation-act-2010 2024-01-01: candidates, section-2
- value-added-tax-consolidation-act-2010 2024-01-01: candidates, schedule-2
- value-added-tax-consolidation-act-2010 2024-01-01: candidates, section-86
- valuation-act-2001 2024-01-01: unexplained, schedule-4
- local-government-act-2001 2024-01-01: unexplained, schedule-14A
- inland-fisheries-act-2010 2024-01-01: unexplained, section-77
- central-bank-reform-act-2010 2024-01-08: unexplained, section-17A, section-29, section-53A, section-53B, section-53C, section-53D, section-53E, section-53F, section-53G, section-53H, section-53I
- nursing-homes-support-scheme-act-2009 2024-02-01: candidates, schedule-1
- value-added-tax-consolidation-act-2010 2024-02-01: unexplained, section-85G, section-85H, section-91A, schedule-9
- disability-act-2005 2024-02-07: unexplained, section-32A
- broadcasting-act-2009 2024-02-17: unexplained, section-2C, section-2D, section-139ZG, section-185
- health-act-2007 2024-02-28: unexplained, section-8, section-12A
- criminal-justice-money-laundering-and-terrorist-financing-act-2010 2024-02-28: unexplained, section-38
- workplace-relations-act-2015 2024-03-06: candidates, section-41
- workplace-relations-act-2015 2024-03-06: candidates, schedule-6
- building-control-regulations-1997 2024-03-06: unexplained, regulation-8, regulation-8A
- parental-leave-act-1998 2024-03-06: unexplained, section-13B
- roads-act-1993 2024-03-07: consolidated late (annotation gives 2007-07-11), section-44
- roads-act-1993 2024-03-07: candidates, section-2
- roads-act-1993 2024-03-07: consolidated late (annotation gives 2023-07-31), section-2
- health-act-1947 2024-03-25: unexplained, section-54
- finance-excise-duties-vehicles-act-1952 2024-03-28: candidates, schedule-1
- finance-excise-duties-vehicles-act-1952 2024-03-28: consolidated late (annotation gives 2013-01-01), schedule-1
- water-services-act-2007 2024-03-30: consolidated late (annotation gives 2012-06-26), section-5
- litter-pollution-act-1997 2024-03-31: candidates, section-19
- local-government-act-2001 2024-03-31: early, section-182
- local-government-act-2001 2024-03-31: unexplained, section-137, schedule-14A
- credit-union-act-1997 2024-04-08: candidates, section-76
- credit-union-act-1997 2024-04-08: unexplained, section-51A, section-190, schedule-6
- credit-union-act-1997 2024-04-09: consolidated late (annotation gives 2003-05-01), section-76
- european-arrest-warrant-act-2003 2024-05-01: candidates, section-2
- european-arrest-warrant-act-2003 2024-05-01: candidates, section-15, section-16
- european-arrest-warrant-act-2003 2024-05-01: candidates, section-13, section-23
- european-arrest-warrant-act-2003 2024-05-02: consolidated late (annotation gives 2009-08-25), section-10
- national-treasury-management-agency-amendment-act-2014 2024-05-07: unexplained, section-49
- maritime-area-planning-act-2021 2024-05-13: candidates, section-6
- maritime-area-planning-act-2021 2024-05-14: early, section-29
- foreshore-act-1933 2024-05-14: unexplained, section-13A
- maritime-area-planning-act-2021 2024-05-14: unexplained, section-4
- criminal-justice-surveillance-act-2009 2024-05-15: early, section-2, section-3, section-4, section-5
- criminal-justice-surveillance-act-2009 2024-05-15: unexplained, section-7, section-8, section-11, section-12, section-13
- coroners-act-1962 2024-05-16: unexplained, section-33F, section-33G, section-33H, section-33I, section-33J, section-33K, section-33L, section-33M, section-33N, section-33O
- local-government-act-2001 2024-05-16: unexplained, section-129J
- local-government-reform-act-2014 2024-05-16: unexplained, section-32
- coroners-act-1962 2024-05-17: consolidated late (annotation gives 2019-09-16), section-27, section-36, section-43, section-47
- coroners-act-1962 2024-05-17: consolidated late (annotation gives 2020-01-16), section-33A, section-33E
- planning-and-development-act-2000 2024-05-17: unexplained, section-2
- road-traffic-act-1961 2024-05-20: candidates, section-3
- road-traffic-act-1961 2024-05-20: candidates, section-113
- road-traffic-act-1961 2024-05-20: candidates, section-20
- road-traffic-act-1961 2024-05-20: candidates, section-38
- roads-act-1993 2024-05-20: candidates, section-57
- road-traffic-act-1994 2024-05-20: candidates, section-35
- road-traffic-act-1994 2024-05-20: candidates, section-41
- road-traffic-act-2004 2024-05-20: early, section-7A
- road-traffic-act-1961 2024-05-20: unexplained, section-78A
- road-traffic-act-1961 2024-05-21: candidates, section-3
- road-traffic-act-1961 2024-05-21: consolidated late (annotation gives 2023-07-31), section-3
- education-and-training-boards-act-2013 2024-05-29: unexplained, schedule-6
- road-traffic-act-2010 2024-05-31: early, section-9
- road-traffic-act-2010 2024-05-31: early, section-10
- road-traffic-act-2010 2024-05-31: unexplained, section-3, section-6, section-16, section-54, section-65, section-74, section-82
- employment-equality-act-1998 2024-06-01: consolidated late (annotation gives 2004-07-18), section-17
- gas-act-1976 2024-06-01: candidates, section-8
- gas-act-1976 2024-06-01: candidates, section-2
- freedom-of-information-act-2014 2024-06-01: candidates, schedule-1
- regulation-of-lobbying-act-2015 2024-06-01: unexplained, section-22G
- protection-of-employment-act-1977 2024-07-01: candidates, section-11, section-13
- protection-of-employment-act-1977 2024-07-01: candidates, section-9, section-14
- protection-of-employment-act-1977 2024-07-01: candidates, section-12
- industrial-relations-act-1946 2024-07-01: unexplained, section-52
- companies-act-2014 2024-07-01: unexplained, section-1123
- companies-act-2014 2024-07-02: consolidated late (annotation gives 2018-09-21), section-935
- companies-act-2014 2024-07-06: candidates, section-906
- companies-act-2014 2024-07-06: unexplained, section-919, section-1585, section-1589, section-1602, section-1608, section-1626, section-1640, section-1642, schedule-21, schedule-22
- central-bank-act-1942 2024-07-09: consolidated late (annotation gives 2014-01-27), section-33AK
- residential-tenancies-act-2004 2024-07-19: unexplained, section-95, section-96
- national-treasury-management-agency-amendment-act-2014 2024-07-30: unexplained, section-40, section-45, section-47, section-47A, section-49A
- local-government-act-2001 2024-08-08: candidates, section-158
- civil-registration-act-2004 2024-08-12: candidates, section-73
- health-act-1970 2024-08-19: candidates, section-45A
- health-act-1970 2024-08-19: candidates, section-45
- planning-and-development-act-2000 2024-08-28: candidates, section-2
- defence-act-1954 2024-08-31: candidates, section-192
- criminal-law-rape-act-1981 2024-08-31: candidates, section-7
- criminal-law-rape-act-1981 2024-08-31: candidates, section-5
- criminal-law-rape-act-1981 2024-08-31: candidates, section-6
- defence-act-1954 2024-08-31: unexplained, section-55, section-61, section-86A, section-117A, section-248, section-258A, section-319, section-320, section-321, section-322, section-323, section-324, section-325, section-326, section-327, section-328, section-329, section-330, section-331, section-332, section-333, section-334, section-335, schedule-13
- criminal-law-sexual-offences-act-2006 2024-08-31: unexplained, section-3
- workplace-relations-act-2015 2024-09-02: candidates, schedule-6
- criminal-evidence-act-1992 2024-09-02: unexplained, section-1
- employment-permits-act-2003 2024-09-02: unexplained, section-1, section-2, section-2A, section-2B, section-2C, section-3A
- employment-permits-act-2006 2024-09-02: unexplained, section-10, schedule-1, schedule-2
- workplace-relations-act-2015 2024-09-02: unexplained, schedule-2
- civil-registration-act-2004 2024-09-16: candidates, section-2
- civil-registration-act-2004 2024-09-16: unexplained, section-30N, section-30O, section-30P, section-30Q, section-30R, section-30S, section-30T, section-41A, section-68A, schedule-2
- environmental-protection-agency-act-1992 2024-09-19: unexplained, section-89
- mental-health-act-2001 2024-09-23: candidates, section-48
- nursing-homes-support-scheme-act-2009 2024-09-24: consolidated late (annotation gives 2024-03-20), schedule-1
- health-act-2007 2024-09-26: candidates, section-73
- health-act-2007 2024-09-26: candidates, section-41
- health-act-2007 2024-09-26: unexplained, section-78A, section-78B
- broadcasting-act-2009 2024-09-27: candidates, section-21
- broadcasting-act-2009 2024-09-27: candidates, section-2, section-139ZG, section-139ZS, section-139ZW
- central-bank-act-1942 2024-09-27: unexplained, section-33AM
- broadcasting-act-2009 2024-09-27: unexplained, section-46K, section-46L, section-139ZF, schedule-3
- child-care-act-1991 2024-09-30: candidates, section-58D, section-58J
- child-care-act-1991 2024-09-30: candidates, section-58A
- child-care-act-1991 2024-09-30: candidates, section-2
- child-care-act-1991 2024-09-30: unexplained, section-58DA, section-58JA, section-58JB, section-58JC, section-58JD, section-58JE
- credit-union-act-1997 2024-09-30: unexplained, section-108
- social-welfare-consolidated-contributions-and-insurability-regulations-1996 2024-10-01: candidates, regulation-88
- control-of-dogs-act-1986 2024-10-01: unexplained, section-7, section-8
- value-added-tax-consolidation-act-2010 2024-10-02: candidates, section-46
- legal-services-regulation-act-2015 2024-10-17: early, section-154A, section-154B
- housing-miscellaneous-provisions-act-1997 2024-10-17: unexplained, section-2, section-3
- residential-tenancies-act-2004 2024-10-18: unexplained, section-114, section-114A
- broadcasting-act-2009 2024-10-22: unexplained, section-46J, section-46K
- local-government-act-2001 2024-10-23: unexplained, schedule-14A
- irish-medicines-board-act-1995 2024-10-31: early, section-32G, section-32H, section-32I
- planning-and-development-act-2000 2024-11-01: unexplained, section-2, section-7
- defence-act-1954 2024-11-06: candidates, section-2
- defence-act-1954 2024-11-06: candidates, section-161
- criminal-justice-mutual-assistance-act-2008 2024-11-06: candidates, section-2
- defence-act-1954 2024-11-06: unexplained, section-192, schedule-1, schedule-3, schedule-11
- criminal-justice-mutual-assistance-act-2008 2024-11-07: unexplained, section-94, section-94A
- central-bank-act-1942 2024-11-08: candidates, section-33AN
- central-bank-act-1942 2024-11-08: candidates, section-33AK
- value-added-tax-consolidation-act-2010 2024-11-12: candidates, section-114B
- value-added-tax-consolidation-act-2010 2024-11-12: candidates, section-115
- value-added-tax-consolidation-act-2010 2024-11-12: early, schedule-2
- value-added-tax-consolidation-act-2010 2024-11-13: candidates, section-46
- value-added-tax-consolidation-act-2010 2024-11-13: consolidated late (annotation gives 2020-12-19), section-46
- land-and-conveyancing-law-reform-act-2009 2024-11-13: unexplained, schedule-1, schedule-2
- civil-partnership-and-certain-rights-and-obligations-of-cohabitants-act-2010 2024-11-13: unexplained, section-110A, section-144, schedule-1
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2024-11-18: candidates, regulation-44
- maternity-protection-act-1994 2024-11-20: candidates, section-13
- maternity-protection-act-1994 2024-11-20: candidates, section-8, section-14A, section-14B
- employment-equality-act-1998 2024-11-20: unexplained, section-14A
- road-traffic-act-2016 2024-11-21: unexplained, section-13
- national-asset-management-agency-act-2009 2024-12-02: unexplained, schedule-3
- land-development-agency-act-2021 2024-12-02: unexplained, section-1
- companies-act-2014 2024-12-03: candidates, section-570, section-584, section-680
- companies-act-2014 2024-12-03: candidates, section-723
- companies-act-2014 2024-12-03: candidates, section-534
- companies-act-2014 2024-12-03: unexplained, section-1123
- animal-health-and-welfare-act-2013 2024-12-06: unexplained, schedule-1
- roads-act-1993 2024-12-10: early, section-51AB
- consumer-protection-act-2007 2024-12-13: unexplained, schedule-1, schedule-2, schedule-3, schedule-5
- chemicals-act-2008 2024-12-17: candidates, section-2
- health-act-1970 2024-12-17: early, section-67F
- health-act-1947 2024-12-17: unexplained, section-54
- public-health-tobacco-act-2002 2024-12-17: unexplained, section-43
- health-act-1947 2024-12-18: consolidated late (annotation gives 2006-06-08), section-54
- public-health-tobacco-act-2002 2024-12-18: consolidated late (annotation gives 2009-07-01), section-43
- competition-and-consumer-protection-act-2014 2024-12-19: unexplained, section-33
- bail-act-1997 2024-12-31: candidates, schedule-1
- electricity-regulation-act-1999 2025-01-01: consolidated late (annotation gives 2021-11-22), section-13A
- bail-act-1997 2025-01-01: candidates, schedule-1
- bail-act-1997 2025-01-01: consolidated late (annotation gives 2017-08-14), schedule-1
- electricity-regulation-act-1999 2025-01-01: candidates, section-13
- electricity-regulation-act-1999 2025-01-01: consolidated late (annotation gives 2017-04-28), section-13
- pharmacy-act-2007 2025-01-01: candidates, section-11
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-01-01: candidates, regulation-59
- value-added-tax-consolidation-act-2010 2025-01-01: candidates, schedule-3
- value-added-tax-consolidation-act-2010 2025-01-01: candidates, schedule-2
- value-added-tax-consolidation-act-2010 2025-01-01: candidates, section-87
- health-insurance-act-1994 2025-01-01: early, section-6A
- social-welfare-consolidated-contributions-and-insurability-regulations-1996 2025-01-01: early, regulation-58
- social-welfare-consolidated-contributions-and-insurability-regulations-1996 2025-01-01: early, regulation-86
- social-welfare-consolidated-contributions-and-insurability-regulations-1996 2025-01-01: early, regulation-49, regulation-63
- social-welfare-consolidated-contributions-and-insurability-regulations-1996 2025-01-01: unexplained, schedule-A
- standards-in-public-office-act-2001 2025-01-01: unexplained, schedule-1
- national-oil-reserves-agency-act-2007 2025-01-01: unexplained, section-44G
- inland-fisheries-act-2010 2025-01-01: unexplained, section-77
- regulation-of-lobbying-act-2015 2025-01-02: consolidated late (annotation gives 2024-01-01), section-5
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-01-03: candidates, schedule-2A, schedule-3A
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-01-03: candidates, schedule-8B
- organisation-of-working-time-act-1997 2025-01-20: candidates, section-3
- charities-act-2009 2025-01-27: candidates, section-2
- broadcasting-act-2009 2025-02-08: candidates, section-2
- central-bank-act-1942 2025-02-11: candidates, schedule-2
- central-bank-act-1942 2025-02-11: candidates, section-33BC
- central-bank-act-1942 2025-02-11: candidates, section-2
- central-bank-act-1942 2025-02-11: unexplained, section-33AM, schedule-4
- health-act-2007 2025-02-15: consolidated late (annotation gives 2017-12-31), section-8, schedule-2
- central-bank-act-1942 2025-02-27: candidates, section-33AK
- central-bank-act-1942 2025-02-27: candidates, section-33AN
- central-bank-act-1942 2025-02-27: candidates, section-33BC
- central-bank-act-1942 2025-02-27: unexplained, section-33AM, section-33ANG, schedule-4
- central-bank-act-1942 2025-02-28: consolidated late (annotation gives 2022-22-29), schedule-2
- road-traffic-act-1968 2025-03-01: unexplained, section-56, schedule-1
- value-added-tax-consolidation-act-2010 2025-03-06: candidates, section-2
- value-added-tax-consolidation-act-2010 2025-03-06: unexplained, section-85, section-85B
- roads-act-1920 2025-03-27: candidates, section-12
- road-traffic-act-1994 2025-03-27: candidates, section-35
- road-traffic-act-1994 2025-03-27: candidates, section-41
- roads-act-1920 2025-03-27: unexplained, section-8
- road-traffic-act-1961 2025-03-31: candidates, section-56A
- road-traffic-act-2002 2025-03-31: candidates, section-2
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-03-31: candidates, regulation-198A
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-03-31: candidates, regulation-60K
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-03-31: candidates, regulation-52HJ
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-03-31: candidates, regulation-14, regulation-15, regulation-16
- freedom-of-information-act-2014 2025-03-31: candidates, schedule-1
- road-traffic-act-1961 2025-03-31: unexplained, section-69A
- air-pollution-act-1987 2025-03-31: unexplained, schedule-2
- road-traffic-act-1961 2025-04-01: consolidated late (annotation gives 1994-12-02), section-50
- coroners-act-1962 2025-04-02: candidates, section-49A
- criminal-justice-surveillance-act-2009 2025-04-02: candidates, section-7, section-8, section-11
- road-traffic-act-2010 2025-04-02: candidates, section-81
- national-vetting-bureau-children-and-vulnerable-persons-act-2012 2025-04-02: candidates, schedule-2
- houses-of-the-oireachtas-inquiries-privileges-and-procedures-act-2013 2025-04-02: candidates, section-9
- freedom-of-information-act-2014 2025-04-02: candidates, schedule-1
- coroners-act-1962 2025-04-02: unexplained, schedule-1
- children-act-2001 2025-04-02: unexplained, section-45, schedule-2
- criminal-justice-act-2007 2025-04-02: unexplained, section-27, section-46
- criminal-justice-victims-of-crime-act-2017 2025-04-02: unexplained, section-36
- children-act-2001 2025-04-03: consolidated late (annotation gives 2007-03-01), section-257D
- road-traffic-act-2010 2025-04-03: candidates, section-9
- road-traffic-act-2010 2025-04-03: consolidated late (annotation gives 2024-05-31), section-9
- value-added-tax-consolidation-act-2010 2025-04-03: candidates, section-46
- irish-nationality-and-citizenship-act-1956 2025-04-07: unexplained, section-11A
- irish-nationality-and-citizenship-act-1956 2025-04-11: unexplained, section-19
- building-control-regulations-1997 2025-05-01: candidates, regulation-5
- building-control-regulations-1997 2025-05-01: candidates, regulation-7
- building-control-regulations-1997 2025-05-01: candidates, regulation-11
- international-protection-act-2015 2025-05-01: unexplained, section-16
- medical-practitioners-act-2007 2025-05-06: unexplained, section-7
- medical-practitioners-act-2007 2025-05-07: consolidated late (annotation gives 2025-05-06), section-58
- medical-practitioners-act-2007 2025-05-07: candidates, section-2
- medical-practitioners-act-2007 2025-05-07: consolidated late (annotation gives 2025-05-06), section-2
- financial-services-and-pensions-ombudsman-act-2017 2025-05-09: candidates, section-62
- residential-tenancies-act-2004 2025-05-16: consolidated late (annotation gives 2022-06-11), section-40
- residential-tenancies-act-2004 2025-05-16: candidates, section-34
- residential-tenancies-act-2004 2025-05-16: consolidated late (annotation gives 2022-06-11), section-34
- residential-tenancies-act-2004 2025-05-16: candidates, section-20
- residential-tenancies-act-2004 2025-05-16: consolidated late (annotation gives 2021-07-09), section-20
- road-traffic-act-1961 2025-05-19: candidates, section-42
- road-traffic-act-1961 2025-05-19: candidates, section-22, section-23D, section-35
- road-traffic-act-1961 2025-05-19: unexplained, section-4
- merchant-shipping-safety-convention-act-1952 2025-06-01: candidates, section-3
- merchant-shipping-safety-convention-act-1952 2025-06-01: candidates, section-22, section-36
- merchant-shipping-act-1894 2025-06-01: unexplained, section-433, section-445, section-537, section-542, section-543, section-565, section-566, section-585, section-598
- merchant-shipping-safety-convention-act-1952 2025-06-01: unexplained, section-19
- competition-act-2002 2025-06-01: unexplained, section-15AU
- national-tourism-development-authority-act-2003 2025-06-01: unexplained, schedule-2
- communications-regulation-premium-rate-services-and-electronic-communications-infrastructure-act-2010 2025-06-01: unexplained, section-8, section-13
- planning-and-development-act-2000 2025-06-18: candidates, section-50B
- planning-and-development-housing-and-residential-tenancies-act-2016 2025-06-18: unexplained, schedule-1
- land-development-agency-act-2021 2025-06-18: unexplained, section-1
- planning-and-development-housing-and-residential-tenancies-act-2016 2025-06-19: candidates, section-3
- planning-and-development-housing-and-residential-tenancies-act-2016 2025-06-19: consolidated late (annotation gives 2025-06-18), section-3
- planning-and-development-act-2000 2025-06-19: unexplained, section-105A, section-143
- residential-tenancies-act-2004 2025-06-21: consolidated late (annotation gives 2021-01-11), section-9
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-06-24: candidates, regulation-8, regulation-155, regulation-174
- social-welfare-consolidated-supplementary-welfare-allowance-regulations-2007 2025-06-24: candidates, regulation-36
- social-welfare-consolidated-supplementary-welfare-allowance-regulations-2007 2025-06-24: unexplained, regulation-3, schedule-4
- central-bank-act-1942 2025-06-30: candidates, section-57A
- central-bank-act-1942 2025-06-30: candidates, section-33AK
- local-government-act-2001 2025-07-03: unexplained, schedule-14A
- local-government-act-2001 2025-07-04: consolidated late (annotation gives 2014-07-01), section-66H
- companies-act-2014 2025-07-07: candidates, section-1598
- value-added-tax-consolidation-act-2010 2025-07-08: unexplained, section-85, section-85B
- value-added-tax-consolidation-act-2010 2025-07-09: candidates, schedule-1
- value-added-tax-consolidation-act-2010 2025-07-09: consolidated late (annotation gives 2024-11-12), schedule-1
- central-bank-act-1942 2025-07-15: unexplained, section-33AM, section-33ANG
- companies-act-2014 2025-07-15: unexplained, section-7, section-325, section-558ZO, section-587, schedule-4
- central-bank-act-1942 2025-07-16: consolidated late (annotation gives 2016-09-16), section-33AN
- finance-local-property-tax-act-2012 2025-07-21: candidates, section-35
- finance-local-property-tax-act-2012 2025-07-21: unexplained, section-17
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-07-29: candidates, regulation-3
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-07-29: candidates, regulation-182
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-07-29: candidates, regulation-217
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-07-29: candidates, regulation-222, regulation-232
- merchant-shipping-safety-convention-act-1952 2025-07-29: unexplained, section-19
- social-welfare-consolidated-occupational-injuries-regulations-2007 2025-07-29: unexplained, schedule-2, schedule-3A, schedule-6
- central-bank-act-1942 2025-08-01: candidates, section-33BC
- central-bank-act-1942 2025-08-01: unexplained, section-33AM
- environmental-protection-agency-act-1992 2025-08-01: unexplained, section-81A
- customs-act-2015 2025-08-01: unexplained, section-2, section-12B, schedule-2
- central-bank-act-1942 2025-08-02: candidates, section-33AK
- central-bank-act-1942 2025-08-02: consolidated late (annotation gives 2025-02-27), section-33AK
- central-bank-act-1942 2025-08-02: candidates, section-33BC
- central-bank-act-1942 2025-08-02: consolidated late (annotation gives 2025-08-01), section-33BC
- planning-and-development-act-2000 2025-08-06: candidates, section-34
- planning-and-development-act-2000 2025-08-06: candidates, section-289, section-290, section-291, section-295
- planning-and-development-act-2000 2025-08-06: candidates, section-177AA
- planning-and-development-act-2000 2025-08-06: unexplained, section-23, section-177AB
- planning-and-development-act-2000 2025-08-07: consolidated late (annotation gives 2010-01-04), section-31A, section-31F
- planning-and-development-act-2000 2025-08-07: consolidated late (annotation gives 2014-06-01), section-22A, section-25A, section-27A
- planning-and-development-act-2000 2025-08-07: consolidated late (annotation gives 2014-06-01), section-23
- irish-aviation-authority-act-1993 2025-08-07: candidates, schedule-2
- national-oil-reserves-agency-act-2007 2025-08-08: candidates, section-44K
- national-oil-reserves-agency-act-2007 2025-08-08: consolidated late (annotation gives 2022-07-15), section-44K
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-09-09: candidates, regulation-196, regulation-201
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-09-09: unexplained, regulation-56A, regulation-79, regulation-140E, regulation-143, regulation-167A, regulation-186, schedule-1, schedule-5, schedule-6, schedule-6A, schedule-7, schedule-11, schedule-17
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-09-10: consolidated late (annotation gives 2012-02-13), regulation-78, schedule-7A
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2025-09-10: consolidated late (annotation gives 2025-03-31), regulation-52HJ
- road-traffic-act-1961 2025-09-23: candidates, section-26
- road-traffic-act-1961 2025-09-23: consolidated late (annotation gives 2017-04-13), section-26
- road-traffic-act-1961 2025-09-23: candidates, section-40
- road-traffic-act-1961 2025-09-23: consolidated late (annotation gives 2022-07-27), section-40
- central-bank-act-1971 2025-09-29: candidates, section-2
- central-bank-act-1971 2025-09-29: unexplained, section-31G, section-31H, section-31I
- workplace-relations-act-2015 2025-09-30: candidates, schedule-1
- workplace-relations-act-2015 2025-09-30: consolidated late (annotation gives 2024-09-02), schedule-1
- workplace-relations-act-2015 2025-09-30: candidates, schedule-6
- workplace-relations-act-2015 2025-09-30: consolidated late (annotation gives 2024-09-02), schedule-6
- roads-act-1993 2025-10-02: candidates, section-2
- roads-act-1993 2025-10-02: candidates, section-51AA
- planning-and-development-act-2000 2025-10-02: candidates, section-177T
- local-government-act-2001 2025-10-02: candidates, section-2
- local-government-act-2001 2025-10-02: candidates, section-66B, section-66C
- water-services-no-2-act-2013 2025-10-02: candidates, section-2
- planning-and-development-act-2000 2025-10-02: unexplained, section-20
- value-added-tax-consolidation-act-2010 2025-10-08: candidates, section-46
- road-traffic-traffic-and-parking-regulations-1997 2025-10-09: candidates, regulation-46
- road-traffic-traffic-and-parking-regulations-1997 2025-10-09: candidates, regulation-4
- sale-of-goods-act-1893 2025-10-10: unexplained, long-title
- road-traffic-act-1961 2025-11-05: candidates, section-26
- road-traffic-act-1961 2025-11-05: consolidated late (annotation gives 2017-04-13), section-26
- planning-and-development-act-2000 2025-11-13: consolidated late (annotation gives 2010-08-19), section-171A
- planning-and-development-act-2000 2025-11-13: consolidated late (annotation gives 2011-09-21), section-177A, section-177O
- planning-and-development-act-2000 2025-11-13: consolidated late (annotation gives 2021-07-16), section-11D
- planning-and-development-act-2000 2025-11-13: consolidated late (annotation gives 2025-06-18), section-147
- planning-and-development-act-2000 2025-11-13: candidates, section-177T
- planning-and-development-act-2000 2025-11-13: consolidated late (annotation gives 2018-10-22), section-177T
- child-and-family-agency-act-2013 2025-11-26: unexplained, schedule-2
- health-and-social-care-professionals-act-2005 2025-12-02: consolidated late (annotation gives 2025-12-01), schedule-3
- statute-of-limitations-1957 2025-12-09: unexplained, schedule-1
- civil-registration-act-2004 2025-12-10: candidates, section-22
- civil-registration-amendment-act-2014 2025-12-10: candidates, section-6
- civil-registration-act-2004 2025-12-10: unexplained, section-44E, section-44F, schedule-2
- civil-registration-amendment-act-2014 2025-12-10: unexplained, section-19, section-36
- planning-and-development-act-2024 2025-12-11: unexplained, schedule-7
- industrial-relations-act-1946 2025-12-18: unexplained, section-12, section-52
- value-added-tax-consolidation-act-2010 2025-12-23: candidates, section-15
- planning-and-development-act-2000 2025-12-31: candidates, section-94
- planning-and-development-act-2000 2025-12-31: candidates, section-177S
- local-government-act-2001 2025-12-31: candidates, schedule-14A
- civil-registration-act-2004 2025-12-31: candidates, section-66
- housing-miscellaneous-provisions-act-2009 2025-12-31: candidates, section-2
- national-asset-management-agency-act-2009 2025-12-31: candidates, section-4
- urban-regeneration-and-housing-act-2015 2025-12-31: candidates, section-3
- electricity-regulation-act-1999 2025-12-31: unexplained, long-title
- planning-and-development-act-2000 2025-12-31: unexplained, section-171, section-177, section-177N
- local-government-act-2001 2025-12-31: unexplained, schedule-4, schedule-5
- water-services-act-2007 2025-12-31: unexplained, section-70K, schedule-1
- housing-miscellaneous-provisions-act-2009 2025-12-31: unexplained, schedule-2
- land-and-conveyancing-law-reform-act-2009 2025-12-31: unexplained, schedule-1, schedule-2
- national-asset-management-agency-act-2009 2025-12-31: unexplained, schedule-3
- child-care-act-1991 2026-01-01: candidates, section-58D
- child-care-act-1991 2026-01-01: candidates, section-58A
- child-care-act-1991 2026-01-01: candidates, section-58B, section-58F, section-58K
- national-oil-reserves-agency-act-2007 2026-01-01: candidates, section-44J
- national-oil-reserves-agency-act-2007 2026-01-01: candidates, section-44I
- national-oil-reserves-agency-act-2007 2026-01-01: candidates, section-44G
- national-oil-reserves-agency-act-2007 2026-01-01: candidates, section-44A
- national-oil-reserves-agency-act-2007 2026-01-01: candidates, section-44C
- road-traffic-act-2010 2026-01-01: candidates, section-22
- value-added-tax-consolidation-act-2010 2026-01-01: candidates, schedule-3
- value-added-tax-consolidation-act-2010 2026-01-01: candidates, section-120
- value-added-tax-consolidation-act-2010 2026-01-01: candidates, section-115
- value-added-tax-consolidation-act-2010 2026-01-01: candidates, section-86
- finance-local-property-tax-act-2012 2026-01-01: candidates, section-132
- workplace-relations-act-2015 2026-01-01: candidates, section-2
- workplace-relations-act-2015 2026-01-01: candidates, section-41
- workplace-relations-act-2015 2026-01-01: candidates, schedule-5
- child-care-act-1991 2026-01-01: unexplained, section-24A, section-35L
- health-insurance-act-1994 2026-01-01: unexplained, schedule-1
- social-welfare-consolidated-contributions-and-insurability-regulations-1996 2026-01-01: unexplained, schedule-A
- broadcasting-act-2009 2026-01-01: unexplained, section-2D, section-17, section-18, section-46J, section-116, section-186, schedule-1
- road-traffic-act-2010 2026-01-01: unexplained, section-65, section-66
- value-added-tax-consolidation-act-2010 2026-01-01: unexplained, section-85, section-85A
- qualifications-and-quality-assurance-education-and-training-act-2012 2026-01-01: unexplained, section-61, schedule-3
- finance-local-property-tax-act-2012 2026-01-01: unexplained, section-20, schedule-1
- workplace-relations-act-2015 2026-01-01: unexplained, schedule-2, schedule-7
- social-welfare-consolidated-occupational-injuries-regulations-2007 2026-01-06: unexplained, regulation-20, schedule-6
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2026-01-21: candidates, regulation-8
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2026-01-21: candidates, regulation-174
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2026-01-21: candidates, regulation-155
- social-welfare-consolidated-supplementary-welfare-allowance-regulations-2007 2026-01-21: candidates, regulation-36
- social-welfare-consolidated-claims-payments-and-control-regulations-2007 2026-01-21: unexplained, long-title, regulation-79, regulation-140, regulation-140A, regulation-171, regulation-172, schedule-1, schedule-5, schedule-6, schedule-6A, schedule-7, schedule-8, schedule-11, schedule-17
- greyhound-industry-act-1958 2026-02-05: candidates, section-2
- irish-horseracing-industry-1994 2026-02-05: candidates, section-2
- consumer-credit-act-1995 2026-02-05: candidates, section-93
- consumer-credit-act-1995 2026-02-05: candidates, section-116, section-144
- consumer-credit-act-1995 2026-02-05: unexplained, schedule-2, schedule-7, schedule-8
- central-bank-act-1942 2026-02-10: candidates, section-2
- central-bank-act-1942 2026-02-10: candidates, schedule-2
- central-bank-act-1942 2026-02-10: candidates, section-33ANF
- central-bank-act-1942 2026-02-10: candidates, section-33AN
- central-bank-act-1942 2026-02-10: candidates, section-33ANE
- central-bank-act-1942 2026-02-10: unexplained, schedule-3, schedule-4, schedule-5, schedule-6, schedule-7, schedule-8, schedule-9, schedule-10
- central-bank-reform-act-2010 2026-02-10: unexplained, schedule-1, schedule-2, schedule-3
- immigration-act-2004 2026-02-17: consolidated late (annotation gives 2016-03-10), section-6
- health-and-social-care-professionals-act-2005 2026-02-17: unexplained, section-96, section-97, schedule-4
- building-control-act-1990 2026-02-25: candidates, section-8
- residential-tenancies-act-2004 2026-02-28: candidates, section-22
- residential-tenancies-act-2004 2026-02-28: candidates, schedule-2
- residential-tenancies-act-2004 2026-03-01: candidates, section-4
- residential-tenancies-act-2004 2026-03-01: candidates, section-12
- residential-tenancies-act-2004 2026-03-01: candidates, section-35
- residential-tenancies-act-2004 2026-03-01: candidates, section-34
- residential-tenancies-act-2004 2026-03-01: candidates, section-136, section-151
- residential-tenancies-act-2004 2026-03-01: candidates, section-16
- residential-tenancies-act-2004 2026-03-01: candidates, section-19
- residential-tenancies-act-2004 2026-03-01: candidates, section-39A
- health-insurance-act-1994 2026-03-02: consolidated late (annotation gives 2012-12-26), schedule-4
- health-insurance-act-1994 2026-03-02: consolidated late (annotation gives 2023-04-01), section-11C
- nursing-homes-support-scheme-act-2009 2026-03-13: candidates, schedule-1
- nursing-homes-support-scheme-act-2009 2026-03-13: unexplained, long-title, section-19, section-22, section-23, section-26, section-40, section-49
- maritime-area-planning-act-2021 2026-03-13: unexplained, schedule-12
- road-traffic-act-1961 2026-03-16: candidates, section-3
- road-traffic-act-1961 2026-03-17: consolidated late (annotation gives 2011-11-28), section-26
- criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2026-03-26: unexplained, schedule-2
- health-insurance-act-1994 2026-04-01: unexplained, schedule-3
- taxi-regulation-act-2013 2026-04-01: unexplained, section-21, section-35
- inland-fisheries-act-2010 2026-04-03: unexplained, section-77, schedule-2, schedule-3, schedule-6
- planning-and-development-act-2000 2026-04-04: unexplained, section-31AI, section-31AJ
- central-bank-supervision-and-enforcement-act-2013 2026-04-10: unexplained, schedule-2, schedule-3, schedule-4
- children-and-family-relationships-act-2015 2026-04-20: unexplained, section-147
- charities-act-2009 2026-04-22: unexplained, section-88B
- central-bank-act-1942 2026-05-01: candidates, section-33BC
- protection-of-employees-employers-insolvency-act-1984 2026-05-05: candidates, section-7
- finance-local-property-tax-act-2012 2026-05-07: unexplained, schedule-1
- environmental-protection-agency-act-1992 2026-05-08: candidates, section-3
- environment-miscellaneous-provisions-act-2011 2026-05-08: candidates, section-4
- environmental-protection-agency-act-1992 2026-05-08: unexplained, section-88
- road-traffic-act-1961 2026-05-13: unexplained, section-4, section-34
- planning-and-development-act-2024 2026-05-18: unexplained, section-9, schedule-7
- health-and-social-care-professionals-act-2005 2026-05-28: unexplained, schedule-3
- national-treasury-management-agency-amendment-act-2014 2026-05-29: unexplained, section-39, section-40, schedule-1, schedule-2
- protection-of-employees-employers-insolvency-act-1984 2026-06-08: candidates, section-6
- protection-of-employees-employers-insolvency-act-1984 2026-06-08: candidates, section-1
- protection-of-employees-employers-insolvency-act-1984 2026-06-08: unexplained, section-4F
- irish-nationality-and-citizenship-act-1956 2026-06-12: candidates, section-16A
- child-care-act-1991 2026-06-12: candidates, section-32
- illegal-immigrants-trafficking-act-2000 2026-06-12: candidates, section-5
- immigration-act-2004 2026-06-12: candidates, section-4
- immigration-act-2004 2026-06-12: candidates, section-1
- social-welfare-consolidation-act-2005 2026-06-12: candidates, section-246
- international-protection-act-2015 2026-06-12: candidates, section-21
- childcare-support-act-2018 2026-06-12: candidates, section-1
- immigration-act-1999 2026-06-12: unexplained, schedule-1
- broadcasting-act-2009 2026-06-12: unexplained, schedule-3
- central-bank-act-1942 2026-06-15: candidates, section-33ANF
- child-care-act-1991 2026-06-23: candidates, section-27, section-28, section-33
- children-act-2001 2026-06-23: candidates, section-71
- national-vetting-bureau-children-and-vulnerable-persons-act-2012 2026-06-23: candidates, schedule-1
- children-first-act-2015 2026-06-23: candidates, schedule-2
- child-care-act-1991 2026-06-23: unexplained, section-24A, section-35G, section-35L
- workplace-relations-act-2015 2026-06-29: candidates, schedule-5
- workplace-relations-act-2015 2026-06-29: candidates, schedule-1
- workplace-relations-act-2015 2026-06-29: candidates, section-41
- workplace-relations-act-2015 2026-06-29: candidates, schedule-6
- workplace-relations-act-2015 2026-06-29: candidates, section-36
- industrial-relations-act-1990 2026-06-29: unexplained, schedule-6
- workplace-relations-act-2015 2026-06-29: unexplained, schedule-7
- central-bank-act-1971 2026-07-10: candidates, section-11
- central-bank-act-1971 2026-07-10: candidates, section-2
- central-bank-act-1971 2026-07-10: candidates, section-7
- central-bank-act-1971 2026-07-10: candidates, section-10
- central-bank-act-1971 2026-07-10: candidates, section-9CA, section-9CB
- ministers-and-secretaries-amendment-act-2011 2026-07-13: unexplained, section-9
- official-languages-act-2003 2026-07-15: unexplained, section-2
- child-care-act-1991 2026-07-21: candidates, section-35D
- guardianship-of-infants-act-1964 2026-07-21: unexplained, section-6BA, section-6BB, section-12B, section-12C, section-12D, section-12E, section-12F, section-12G, section-12H, section-12I, section-12J
- firearms-act-1925 2026-07-23: candidates, section-2
- building-control-regulations-1997 2026-07-27: candidates, regulation-20A
- building-control-regulations-1997 2026-07-27: candidates, regulation-9
- building-control-regulations-1997 2026-07-27: candidates, regulation-20F
- building-control-regulations-1997 2026-07-27: candidates, regulation-7
- central-bank-act-1942 2026-07-31: candidates, section-33AK
- central-bank-act-1942 2026-07-31: candidates, section-2
- communications-regulation-act-2002 2026-07-31: candidates, section-10
- freedom-of-information-act-2014 2026-07-31: candidates, schedule-1
- central-bank-act-1942 2026-08-01: candidates, schedule-2
- central-bank-act-1997 2026-08-01: candidates, section-28
- value-added-tax-consolidation-act-2010 2026-08-01: candidates, section-59
- value-added-tax-consolidation-act-2010 2026-08-01: candidates, section-64
- value-added-tax-consolidation-act-2010 2026-08-01: candidates, section-94
- central-bank-act-1997 2026-08-01: unexplained, section-36F, section-36G
- national-asset-management-agency-act-2009 2026-08-01: unexplained, schedule-3
- irish-bank-resolution-corporation-act-2013 2026-08-01: unexplained, schedule-1
- extradition-act-1965 2026-08-10: candidates, section-27
- social-welfare-consolidation-act-2005 2026-08-10: candidates, schedule-5
- criminal-justice-act-2006 2026-08-10: candidates, section-99
- road-traffic-act-1961 2026-08-12: candidates, section-62
- international-criminal-court-act-2006 2026-09-01: candidates, section-2
- firearms-act-1925 2026-09-01: unexplained, section-24, section-25
- criminal-justice-forensic-evidence-and-dna-database-system-act-2014 2026-09-01: unexplained, section-127
- residential-tenancies-act-2004 2026-09-14: candidates, section-96
- residential-tenancies-act-2004 2026-09-14: candidates, section-19
- national-treasury-management-agency-amendment-act-2014 2026-09-22: unexplained, section-49H, section-49L, section-49Q, section-49AA
- social-welfare-consolidation-act-2005 2026-10-01: unexplained, section-13, section-21, section-29, section-30B, section-30F

## Dates

Author and committer dates are noon in Dublin on the `In-force:` day: UTC+1 from the last Sunday in March to the day
before the last Sunday in October (`start <= day < end`), UTC otherwise, written out in the builder because the build
machine has no time-zone database. No day in this corpus is before 1970. The committer is
`Lexifina <ireland-law@lexifina.com>`. The documentation commit is dated the day the PDFs were retrieved.

## Limits

1. The history starts at the earliest revision the Commission publishes, not at enactment.
2. Between two revisions the text of each provision is known only at the two ends: two laws changing one provision in
   that interval cannot be separated.
3. Schedules are tables; their cells are read in the order the PDF holds them, which is not always the order a reader
   sees. A schedule is compared across revisions as the letters and digits it contains.
4. English only; the Revised Acts are in English.

## People and models

The builder, checker and tests were written by an AI agent (Claude, Anthropic, model Opus 5.5) working for Lexifina, under
the instructions of Lexifina's staff. No AI model wrote, summarised or edited legal text, and no model runs at build
time: the commit messages quote the Commission's annotations and are otherwise fixed templates.

## Prior art

- The Law Reform Commission's Revised Acts and its classified list of legislation.
- The electronic Irish Statute Book (irishstatutebook.ie), with each act's legislation directory ("affected by").
- legalize-dev (github.com/legalize-dev), law as git repositories for several countries.
