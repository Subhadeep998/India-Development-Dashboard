<a href="https://subhadeep998.github.io/India-Development-Dashboard/">
  <img src="assets/banner.svg" alt="India Development Dashboard — by Subhadeep Aditya" width="100%">
</a>

<p align="center">
  <a href="https://subhadeep998.github.io/India-Development-Dashboard/"><img src="https://img.shields.io/badge/%F0%9F%93%8A%20open-live%20dashboard-FF9933?style=for-the-badge&labelColor=0D0F12" alt="Open the live dashboard"></a>
</p>

<p align="center">
  <a href="https://github.com/Subhadeep998/India-Development-Dashboard/actions/workflows/daily.yml"><img src="https://img.shields.io/github/actions/workflow/status/Subhadeep998/India-Development-Dashboard/daily.yml?style=flat-square&label=daily%20update&labelColor=0D0F12" alt="Daily update"></a>
  <img src="https://img.shields.io/badge/updated-{{UPDATED_BADGE}}-4CC38A?style=flat-square&labelColor=0D0F12" alt="Last updated">
  <img src="https://img.shields.io/badge/data-World%20Bank%20%C2%B7%20IMF%20%C2%B7%20PIB-00CCBB?style=flat-square&labelColor=0D0F12" alt="Data sources">
  <a href="https://github.com/Subhadeep998/India-Development-Dashboard/stargazers"><img src="https://img.shields.io/github/stars/Subhadeep998/India-Development-Dashboard?style=flat-square&color=E6B85C&labelColor=0D0F12" alt="Stars"></a>
</p>

<p align="center"><b>India's economy, industry, environment and people — in one live, free dashboard.</b><br>
<sub>GDP and national income from the World Bank, growth forecasts from the IMF, and the day's news for every topic from official government sources only (PIB, DD News, All India Radio, MyGov, RBI) — refreshed automatically twice a day.</sub></p>

<p align="center">
  <a href="https://subhadeep998.github.io/India-Development-Dashboard/#economy">📈 Economy</a> ·
  <a href="https://subhadeep998.github.io/India-Development-Dashboard/#industry">🏭 Industry</a> ·
  <a href="https://subhadeep998.github.io/India-Development-Dashboard/#environment">🌿 Environment</a> ·
  <a href="https://subhadeep998.github.io/India-Development-Dashboard/#education">🎓 Education & Scholarships</a> ·
  <a href="https://subhadeep998.github.io/India-Development-Dashboard/#culture">🎭 Arts & Culture</a> ·
  <a href="https://subhadeep998.github.io/India-Development-Dashboard/#food">🌾 Food & Agriculture</a>
</p>

---

## 🇮🇳 India at a glance

{{KPIS}}

<sub>Last refreshed: {{UPDATED}} · Annual figures in current US$ from the World Bank; the forecast is the IMF World Economic Outlook.</sub>

---

## 📊 The big trends

<table>
  <tr>
    <td width="50%"><img src="assets/charts/gdp.svg" width="100%" alt="India GDP trend"></td>
    <td width="50%"><img src="assets/charts/growth.svg" width="100%" alt="India real GDP growth with IMF projections"></td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/charts/gni-per-capita.svg" width="100%" alt="India GNI per capita"></td>
    <td width="50%"><img src="assets/charts/manufacturing.svg" width="100%" alt="Manufacturing share of GDP"></td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/charts/co2.svg" width="100%" alt="India CO2 emissions"></td>
    <td width="50%"><img src="assets/charts/renewables.svg" width="100%" alt="Renewable energy share"></td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/charts/education.svg" width="100%" alt="Higher-education enrolment"></td>
    <td width="50%"><img src="assets/charts/cereal-yield.svg" width="100%" alt="Cereal yield"></td>
  </tr>
</table>

<p align="right"><a href="https://subhadeep998.github.io/India-Development-Dashboard/"><b>Explore 27 indicators interactively →</b></a></p>

---

## 📰 Today across India — official sources

{{NEWS}}

---

## 🏛️ Government schemes, at a glance

| Area | Start here |
|:--|:--|
| 🎓 **Scholarships** | [National Scholarship Portal](https://scholarships.gov.in) · [PM Vidyalaxmi (education loans)](https://pmvidyalaxmi.co.in) · [INSPIRE](https://online-inspire.gov.in) · [PM Research Fellowship](https://pmrf.in) · [AICTE Pragati & Saksham](https://www.aicte-india.org) |
| 🎭 **Arts & culture** | [Ministry of Culture](https://www.indiaculture.gov.in) · [CCRT scholarships for young artists](https://ccrtindia.gov.in) · [Sangeet Natak Akademi](https://www.sangeetnatak.gov.in) · [Lalit Kala Akademi](https://lalitkala.gov.in) |
| 🌾 **Food** | [National Food Security Act](https://nfsa.gov.in) · [PM-KISAN](https://pmkisan.gov.in) · [PM-POSHAN](https://pmposhan.education.gov.in) · [Eat Right India](https://eatrightindia.gov.in) · [e-NAM](https://enam.gov.in) |
| 🌿 **Environment** | [National Clean Air Programme](https://prana.cpcb.gov.in) · [PM Surya Ghar](https://pmsuryaghar.gov.in) · [PM-KUSUM](https://pmkusum.mnre.gov.in) · [Mission LiFE](https://missionlife-moefcc.nic.in) |
| 🏭 **Industry** | [Make in India](https://www.makeinindia.com) · [PLI schemes](https://www.investindia.gov.in/production-linked-incentives-schemes-india) · [Startup India](https://www.startupindia.gov.in) · [PM Gati Shakti](https://pmgatishakti.gov.in) |
| 📈 **Economy** | [Union Budget](https://www.indiabudget.gov.in) · [RBI](https://www.rbi.org.in) · [MoSPI](https://www.mospi.gov.in) · [GST Council](https://gstcouncil.gov.in) |

> Scheme rules, amounts and deadlines change — always confirm on the official portal before applying.

---

## ⚙️ How it works

```mermaid
flowchart LR
  WB[World Bank API<br/>27 indicators] --> B[scripts/build.py]
  IMF[IMF DataMapper<br/>growth forecasts] --> B
  PIB[PIB releases<br/>official policy news] --> B
  GN[DD News · AIR · MyGov · RBI<br/>official news only] --> B
  B --> D[docs/ — interactive dashboard<br/>GitHub Pages]
  B --> C[assets/charts — SVG charts]
  B --> R[README — this page]
  A[GitHub Actions<br/>03:01 + 07:41 IST] --> B
```

- **Runs twice a day** (03:01 and 07:41 IST), away from GitHub's busy hours — if one run is delayed or dropped, the second catches up.
- **Never goes blank:** if a source is down, the last good data is kept.
- **All sources are free and official.** Official sources only — no general media. Only headlines and links are stored — click through to read the original reporting.

> Independent educational project; not affiliated with the Government of India, the World Bank or the IMF.

---

<p align="center">
  ⭐ <b>Star</b> to bookmark · 👤 <a href="https://github.com/Subhadeep998"><b>Follow @Subhadeep998</b></a><br>
  <sub>Built by <a href="https://www.subhadeepaditya.in">Subhadeep Aditya</a> — healthcare intelligence analyst and LL.B. student · Kolkata, India</sub>
</p>
