# VERIF-AI 2026 — Paper Tracking Table

This table is the single source of truth for per-paper production status. Update it as each stage is completed. Paper identity (title, authors, submission ID) is drawn from `acceptedPapers.md` and should not be changed here unless correcting a transcription error.

| # | Sub. ID | Title | Authors | Camera-Ready Received | Source Files Received | Page Count | Licence-to-Publish Signed | Compliance Check |
|---|---------|-------|---------|----------------------|----------------------|------------|--------------------------|-----------------|
| 1 | 1992 | From Verification to Herding: Exploiting Software's Sparsity of Influence | Tim Menzies and Kishan Ganguly | No | No | — | No | Pending |
| 2 | 3744 | Abductive Vibe Coding (Extended Abstract) | Logan Murphy, Aren A. Babikian and Marsha Chechik | No | No | — | No | Pending |
| 3 | 7252 | Do AI models help produce verified bug fixes? | Li Huang, Ilgiz Mustafin, Alessandro Schena, Marco Piccioni, Bertrand Meyer and Reto Weber | No | No | — | No | Pending |
| 4 | 1613 | Modeling and Analysis of Non-Deterministic Executions of LLM-Based Agents via Finite Automata | Armel Fedoung Sanou, Badr Youakim and Fabrice Mourlin | No | No | — | No | Pending |
| 5 | 3719 | Formalizing and validating properties in Asmeta with Large Language Models | Andrea Bombarda, Silvia Bonfanti, Angelo Gargantini and Nico Pellegrinelli | No | No | — | No | Pending |
| 6 | 4854 | Automatic Generation of Executable Script from MBT Scenario | Jessy Colonval, Fabrice Bouquet, Lefevre Louis, Antoine Perrotin, Éléa Jacquin, Antoine Chevrot and Frédéric Dadeau | No | No | — | No | Pending |
| 7 | 5373 | Large Language Models and Language Server Protocol: a match made in context | Alessandro Schena, Ilgiz Mustafin and Julia Kotovich | No | No | — | No | Pending |
| 8 | 5640 | Neuroforger: certified violation witnesses for smart contracts verification via LLMs | Enrico Lipparini and Massimo Bartoletti | No | No | — | No | Pending |
| 9 | 9569 | Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability | Shirley Yu and Ruben Martins | No | No | — | No | Pending |
| 10 | 4668 | Trustworthy Machine Learning Across the Lifecycle: A Synthesis of Current Methods | Leonel Gamvou Taklai, Jonathan Roy, Fehmi Jaafar and Sylvain Hallé | No | No | — | No | Pending |
| 11 | 5808 | An Empirical Study on Generating Proven-to-be-Correct Dafny Programs | Liam O'Reilly, Filippos Pantekis, Markus Roggenbach and Mukesh Tiwari | No | No | — | No | Pending |
| 12 | 6356 | Requirement-Based Testing: Enhancing Reinforcement Learning with Game Theory | Ocan Sankur, Thierry Jéron, Nicolas Markey, David Mentré and Reiya Noguchi | No | No | — | No | Pending |
| 13 | 8595 | Adaptive Random Testing of Online Machine Learning Programs: Application to Opportunistic Software Composition | Maxence Demougeot, Sylvie Trouilhet and Jean-Paul Arcangeli | No | No | — | No | Pending |
| 14 | 4215 | SecretFan: Synthesizing Realistic Data without Breaking Privacy | Laura Plein, Alexi Turcotte, Arina Hallemans and Andreas Zeller | No | No | — | No | Pending |
| 15 | 6194 | AI-augmented MBSE: from vibe-modeling to assisted verification and validation | Anca-Miruna Constantin, Christian Koumlah-Mbey, Ileana Ober and Iulian Ober | No | No | — | No | Pending |
| 16 | 7035 | Improving Verified Constraint Satisfaction in Differentiable Logics | Thomas Flinkow and Rosemary Monahan | No | No | — | No | Pending |
| 17 | 6470 | Probabilistic Behavior Synthesis with Language Models for Autonomous Vehicle Testing | Sol Zilberman and Betty Cheng | No | No | — | No | Pending |
| 18 | 8405 | Validating Multi-Model AI-Generated Acceptance Criteria in Requirements Engineering | Mateen Abbasi, Petri Ihantola, Tommi Mikkonen and Niko Mäkitalo | No | No | — | No | Pending |
| 19 | 9130 | Co-Evolutionary Challenges: When Software Engineering Meets Artificial Intelligence | Maha Moujahed, Maxence Demougeot, Mohamed Mahdi, Maryam Assmar, Alain Giorgetti, Gabriela Gonzalez-Saez, Nicolas Hili, Yves Ledru, Meriem Ouederni and Sylvie Trouilhet | No | No | — | No | Pending |
| 20 | 9536 | ReqFusion: A Multi-Provider Framework for Automated PEGS Analysis Across Software Domains | Muhammad Khalid, Oriol Manuel and Yilmaz Uygun | No | No | — | No | Pending |
| 21 | 6273 | Towards an Evaluation of LLM's Prior Knowledge for Test Case Generation | Gabriela Gonzalez-Saez, Yves Ledru and Nicolas Hili | No | No | — | No | Pending |
| 22 | 2745 | A Typed Intermediate Representation for Neurosymbolic Formalization and Verification of Stock Index Methodologies | Dmitrii Zorin | No | No | — | No | Pending |
| 23 | 3747 | Automated evaluation of test requirements generation with LLMs | Dorine Tabary, Éléa Jacquin, Fabrice Bouquet and Frédéric Dadeau | No | No | — | No | Pending |
| 24 | 5626 | Learning-Infused Formal Reasoning: From Contract Synthesis to Artifact Reuse and Formal Semantics | Arshad Beg, Diarmuid O'Donoghue and Rosemary Monahan | No | No | — | No | Pending |
| 25 | 7106 | VERIFAI Energy Management Systems | Maha Moujahed, Souheil El Alimi and Meriem Ouederni | No | No | — | No | Pending |

---

## Failure Note Convention

When the Compliance Check column is set to `Fail`, add a blockquote on the line immediately below the affected table row using this format:

```
| 7 | 5373 | Large Language Models and Language Server Protocol: a match made in context | Alessandro Schena, Ilgiz Mustafin and Julia Kotovich | 2026-04-15 | 2026-04-15 | 18 | No | Fail |
> **Failure note (#7):** CR-1: Paper exceeds 16-page soft limit (18 pages). Returned to authors 2026-04-16.
```

Cite the specific compliance rule(s) that failed (CR-1 through CR-5). Once the author corrects the issue and resubmits, reset Compliance Check to `Pending` while the revised submission is under review.
