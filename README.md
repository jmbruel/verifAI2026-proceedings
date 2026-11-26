# VERIF-AI 2026 Proceedings Workspace

This repository manages the full production lifecycle for the **VERIF-AI 2026** proceedings. VERIF-AI 2026 is a workshop held in **Villebrumier, France, 8–11 March 2026**, organized by the **LASER Foundation**. The proceedings will be published in Springer's **Lecture Notes in Computer Science (LNCS)** series as **Volume 17411** (`LNCS 17411`, **Edition ID 696960**). The workspace covers 24 accepted papers, from collecting camera-ready submissions through verifying LaTeX sources, checking pagination locally, and producing the final Springer submission package.

---

## Repository Layout

```
verifAI2026-proceedings/
├── README.md                          # This file — overview, editorial & build workflow
├── .gitignore                         # Excludes paper PDFs/ZIPs and LaTeX build artefacts; tracks sources
├── instructions.md                    # Springer acceptance email & volume editor instructions
├── acceptedPapers.md                  # Authoritative list of 24 accepted papers (read-only)
├── llncs.cls                          # Springer LNCS LaTeX class (v2.26, self-contained)
├── proceedings.tex                    # Local pdfpages assembly harness (front matter + 24 paper stubs)
├── Makefile                           # Build targets: front-matter, paper, papers, proceedings, clean
│
├── tracking/
│   ├── paper-tracking.md              # Per-paper status table (24 rows, 10 status columns)
│   ├── compliance-rules.md            # Criteria applied during compliance checks (CR-1 to CR-5)
│   └── author-emails.md               # Draft follow-up emails for missing/non-compliant papers
│
├── front-matter/
│   ├── preface.md                     # Preface draft — fill placeholders before submission
│   ├── organization-pages.md          # Committee roles draft — fill placeholders before submission
│   ├── preface.tex                    # LNCS Preface LaTeX source (matches frontmatter_sample.pdf)
│   ├── organization-pages.tex         # LNCS Organization Pages LaTeX source
│   └── front-matter.tex               # Standalone front-matter LaTeX master
│
├── submission/
│   ├── toc.csv                        # Table of Contents for Springer (7 Springer template columns)
│   └── springer-checklist.md          # Pre-submission checklist (aligned with Springer Sect. 11)
│
├── springer-files/                    # Official Springer guidelines, LTP form, ToC template & samples
│
└── papers/                            # Per-paper folders: p<sub-id>/ -> renamed to <volNNNN>/
    └── .gitkeep                       # Keeps directory in git; documents naming & git rules
```

**Data flow:** `acceptedPapers.md` is the single source of truth for paper identity (title, authors, submission ID). `tracking/paper-tracking.md` is the single source of truth for per-paper production status. Information collected there (page counts, LTP dates, compliance and compilation results) flows outward to populate `submission/toc.csv` (and `springer-files/Table_of_Contents_template.xlsx`) and satisfy `submission/springer-checklist.md`.

---

## Editorial Workflow

Work through these steps in order. Update `tracking/paper-tracking.md` as each step is completed for each paper.

1. **Request a volume number.** Contact `anna.kramer@springer.com` as soon as collection begins. Per `instructions.md` and Springer Guidelines Sect. 3.4, if the total page count exceeds **700 pages**, request two volume numbers. Inform Springer if post-event revisions were permitted (affects volume subtitle) and prepare peer-review/acceptance statistics for Crossmark.

2. **Send author instructions.** Send each corresponding author the LNCS author formatting instructions (`springer-files/Springer_Instructions_for_Authors_of_Proceedings_CS.pdf`), the Springer Nature Code of Conduct (`springer-files/Publisher's_Code_of_Conduct_for_Book_Authors.pdf`), and the **LNCS-specific Licence-to-Publish (LTP) form** (`springer-files/SNCS_ProceedingsPaper_LTP_ST_SN_Switzerland.docx`). No other Springer agreement applies. Digital signatures are not acceptable — a wet (ink) signature is required on every LTP.

3. **Receive camera-ready submissions.** For each paper, create `papers/p<submission-id>/` (e.g., `papers/p1992/`) and place the camera-ready PDF (`paper.pdf`) and all source files (`.tex`, `.bib`/`.bbl`, and figures for LaTeX papers; `.docx` for Word papers) inside. Update `tracking/paper-tracking.md`: set Camera-Ready Received and Source Files Received to the date received (`YYYY-MM-DD`).

4. **Compile LaTeX papers & run compliance checks.** Verify each LaTeX paper builds cleanly in its own folder via `make paper DIR=papers/p<sub-id>` (or `make papers`) and record `Compilation Status` (`OK`, `Error`, or `N/A` for Word papers). Evaluate all five rules in `tracking/compliance-rules.md` (CR-1 through CR-5) and update `Compliance Check` to `Pass` or `Fail`. Record any failures or build errors in a blockquote note immediately below the affected row.

5. **Collect signed LTPs.** Receive the signed LTP from the corresponding author of each paper and store it inside that paper's folder. Update `Licence-to-Publish Signed` to the date received. Verify the LTP bears a wet signature and that the corresponding author matches the paper header.

6. **Paginate accepted papers & check local assembly.** Record each paper's page count in `tracking/paper-tracking.md`. Uncomment each ready paper's `\includepaper` line in `proceedings.tex` and run `make proceedings` to generate a local preview PDF with Table of Contents and sequential page numbers. Fill in `Starting Page` in `submission/toc.csv`.

7. **Complete the ToC and Author Index notes.** Fill in `Corresponding Author Name`, `Corresponding Author Email`, and `Submission Folder Number` (once the volume number is confirmed) in `submission/toc.csv`, and transfer to `springer-files/Table_of_Contents_template.xlsx` if needed. Prepare the list of non-straightforward author names (`Given Name; Family Name`) for Springer's Author Index.

8. **Add Part Titles to the ToC and `proceedings.tex`.** Group papers by topic (not by conference session; no session numbering) and enter topical section headings in `submission/toc.csv` and the `\part{}` markers of `proceedings.tex`.

9. **Rename per-paper submission folders.** Once the volume number is assigned, rename each folder from `papers/p<sub-id>/` to `<volume-number><4-digit-starting-page>` (e.g., `164560015` for a paper starting on page 15 of volume 16456). Each folder must contain the paper's source files, PDF, signed LTP, and optional Alt Text Excel file.

10. **Finalize front matter.** Replace all `PLACEHOLDER` / `TODO` text in `front-matter/preface.md`, `front-matter/organization-pages.md`, `front-matter/preface.tex`, and `front-matter/organization-pages.tex`. Run `make front-matter` to verify the compiled front-matter PDF.

11. **Work through the submission checklist.** Open `submission/springer-checklist.md` and tick every item. Do not send the package until every item is verified.

12. **Submit to Springer via the Manuscript Submission Portal.** Zip all `17411<4-digit-starting-page>` folders together with the `frontmatter` folder (`17411.zip`, not `.tar`), prepare the complete manuscript PDF (`proceedings.pdf`) and/or separate unzipped chapter PDFs, confirm third-party rights and content finality (no content changes after upload except minor proof corrections), and upload all files with the completed production questionnaire/ToC via the passwordless [Edition 696960 portal](https://bookmanuscriptsubmission.public.springernature.app/link/bookmanuscriptsubmission/696960-Bertrand.Meyer%40inf.ethz.ch). *(Note: the portal link is tied to `Bertrand.Meyer@inf.ethz.ch` — if submitting on his behalf, confirm authorization including the third-party rights declaration.)* Allow **8–10 weeks** from receipt for publication.

---

## Compilation & Local Assembly Workflow

Springer compiles and typesets each paper independently from its own folder (`CS_Editors_Proceedings_guidelines.pdf`, Sect. 5.6) and does **not** want a single merged `.tex` source. Accordingly, the build setup has two complementary stages:

1. **Independent per-paper verification (`make paper` / `make papers`):** Compiles each LaTeX paper inside its own `papers/<folder>/` directory with `TEXINPUTS=../../:` so it uses the root `llncs.cls` without package or macro collisions across papers.
2. **Local volume preview (`make proceedings`):** Compiles `proceedings.tex`, which includes the LNCS front matter and assembles each paper's compiled/camera-ready PDF via `pdfpages` (`\includepaper`), generating an LNCS-formatted Table of Contents and verifying pagination.

```bash
make front-matter                 # Compile front-matter/front-matter.tex -> front-matter/front-matter.pdf
make paper DIR=papers/p1992       # Compile one LaTeX paper independently (optional MAIN=file.tex)
make papers                       # Compile all LaTeX paper folders under papers/*/
make proceedings                  # Assemble local proceedings.pdf (front matter + pdfpages)
make clean                        # Clean root and front-matter build artefacts
make clean-papers                 # Clean LaTeX build artefacts inside papers/*/ (keeps PDFs & sources)
```

If a paper fails to compile, set its `Compilation Status` to `Error` in `tracking/paper-tracking.md`, record the error in a blockquote failure note below the row, contact the corresponding author with the log, and leave its `\includepaper` line commented out in `proceedings.tex` until resolved.

---

## Key Contacts

| Contact | Email | Role |
|---------|-------|------|
| Sindhu Ramachandran | sindhu.ramachandran.consultant.1@springernature.com | Manuscript submission & production coordination (Volume 17411, Edition ID 696960) |
| Anna Kramer | anna.kramer@springer.com | Volume number requests; primary Springer LNCS editorial contact |
| Ronan Nugent | ronan.nugent@springer.com | Responsible editor; volume editor arrangement exceptions (if volume editors ≠ PC Chairs) |
| LNCS Editorial | lncs@springer.com | Open Choice / Open Access queries |

---

## Important Constraints

**Page limits & minimums.** Full papers should be **≥ 12 pages**, short papers **≥ 6 pages**, with at least **2/3 full papers** overall. Any paper **< 4 pages** is moved to back matter and not indexed on Springer Nature Link. The soft upper limit is **20 pages** (flag 21–22 pages; contact Springer for papers **≥ 30 pages**). A single volume holds at most **700 pages** (request two volume numbers if exceeded).

**Licence-to-Publish.** Authors must sign the **LNCS-specific LTP form** (`springer-files/SNCS_ProceedingsPaper_LTP_ST_SN_Switzerland.docx`) — no other Springer agreement applies. **Digital signatures are not acceptable**; a wet (ink) signature is required on every LTP, and each signed LTP goes inside its paper's submission folder.

**PC-member paper cap & review disclosure.** No PC Chair, PC member, or volume editor may co-author more than **2 papers** in the volume, and the Preface must explain how PC-coauthored papers were objectively reviewed.

**Keynote abstracts.** Abstracts of keynote talks without accompanying full papers belong in the **Front Matter**, not in the main proceedings (Springer Guidelines Sect. 3.4). They do not appear in `submission/toc.csv`.

**Folder naming convention.** Each per-paper submission folder must be named `<volume-number><4-digit-starting-page>` with no separator (e.g., `164560015`). Front matter goes in its own `frontmatter` folder. All folders are zipped into a single `.zip` archive labelled with the volume number.

**Source files.** Springer requires all source files alongside the PDF for every paper. `.tex`, `.bib`, `.bbl`, figure images (`.png`/`.jpg`/`.eps`), and `.docx` files are **not** git-ignored and should be committed when received.

**Front-matter templates.** Official LaTeX and Word templates for front matter are available from the volume editors' website at <http://bit.ly/2HaWmko>.
