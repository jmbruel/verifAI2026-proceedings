# VERIF-AI 2026 Proceedings Workspace

This repository manages the full production lifecycle for the **VERIF-AI 2026** proceedings. VERIF-AI 2026 is a workshop held in **Villebrumier, France, 8–11 March 2026**, organized by the **LASER Foundation**. The proceedings will be published as a volume in Springer's **Lecture Notes in Computer Science (LNCS)** series. The workspace covers 25 accepted papers, from collecting camera-ready submissions through producing the final Springer submission package.

---

## Repository Layout

```
verifAI2026-proceedings/
├── README.md                          # This file — overview and editorial workflow
├── .gitignore                         # Excludes PDF/image binaries; tracks source files
├── acceptedPapers.md                  # Authoritative list of 25 accepted papers (read-only)
│
├── tracking/
│   ├── paper-tracking.md              # Per-paper status table (25 rows, updated throughout lifecycle)
│   └── compliance-rules.md            # Criteria applied during compliance checks (CR-1 to CR-5)
│
├── front-matter/
│   ├── preface.md                     # Preface stub — fill placeholders before submission
│   └── organization-pages.md          # Committee roles stub — fill placeholders before submission
│
├── submission/
│   ├── toc.csv                        # Table of Contents for Springer (Springer template columns)
│   └── springer-checklist.md          # 17-item pre-submission checklist
│
└── papers/                            # Drop zone for camera-ready PDFs and source files
    └── .gitkeep                       # Keeps directory in git; PDFs are ignored, source files tracked
```

**Data flow:** `acceptedPapers.md` is the single source of truth for paper identity (title, authors, submission ID). `tracking/paper-tracking.md` is the single source of truth for per-paper production status. Information collected there (page counts, LTP dates, compliance results) flows outward to populate `submission/toc.csv` and to satisfy `submission/springer-checklist.md`.

---

## Editorial Workflow

Work through these steps in order. Update `tracking/paper-tracking.md` as each step is completed for each paper.

1. **Request a volume number.** Contact `anna.kramer@springer.com` as soon as collection begins. If the total page count exceeds 500 pages, request two volume numbers. You will need the volume number to name per-paper submission folders (see step 9).

2. **Send author instructions.** Send each corresponding author the LNCS author formatting instructions and the **LNCS-specific Licence-to-Publish (LTP) form**. No other Springer agreement applies. Digital signatures are not acceptable — a wet (ink) signature is required on every LTP.

3. **Receive camera-ready submissions.** For each paper, receive the camera-ready PDF and all source files (`.tex`, `.bib`/`.bbl`, and images for LaTeX papers; `.docx` for Word papers). Drop them in `papers/`. Update `tracking/paper-tracking.md`: set Camera-Ready Received and Source Files Received to the date received (YYYY-MM-DD format).

4. **Run compliance checks.** For each paper, evaluate all five rules in `tracking/compliance-rules.md` (CR-1 through CR-5). Update the Compliance Check column to `Pass` or `Fail`. If `Fail`, add a blockquote failure note immediately below the affected table row explaining which rules failed and what action was taken.

5. **Collect signed LTPs.** Receive the signed LTP from the corresponding author of each paper. Update the Licence-to-Publish Signed column to the date received. Verify the LTP bears a wet signature and that the corresponding author on the LTP matches the corresponding author on the paper header.

6. **Paginate accepted papers.** Determine the page count for each paper; update the Page Count column in `tracking/paper-tracking.md`. Then assign starting page numbers and fill in the Starting Page column in `submission/toc.csv`.

7. **Complete the ToC CSV.** Fill in Corresponding Author Name, Corresponding Author Email, and Submission Folder Number (see step 9 for the naming convention) in `submission/toc.csv` for each paper.

8. **Add Part Titles to the ToC CSV.** Group papers by topic (not by conference session) and enter topical section headings in the Part Titles column of `submission/toc.csv`.

9. **Prepare per-paper submission folders.** Name each folder using the Springer convention: `<volume-number><4-digit-starting-page>`. For example, a paper starting on page 15 of volume 16456 goes in folder `164560015`. Place the camera-ready PDF and all source files for that paper inside the folder.

10. **Finalize front matter.** Replace all placeholder text in `front-matter/preface.md` and `front-matter/organization-pages.md`. Search for `PLACEHOLDER` to confirm no stubs remain.

11. **Work through the submission checklist.** Open `submission/springer-checklist.md` and tick every item. Do not send the package until all 17 items are checked.

12. **Submit to Springer.** Zip all per-paper folders (label the zip with the volume number), prepare a separate unzipped directory containing only the PDFs of all papers, and send the complete package to Springer. Allow **8–10 weeks** from receipt for publication. If printed copies are needed at the event, files must arrive at Springer **10 weeks before the conference start**.

---

## Key Contacts

| Contact | Email | Role |
|---------|-------|------|
| Anna Kramer | anna.kramer@springer.com | Volume number requests; primary Springer contact for filing |
| Ronan Nugent | ronan.nugent@springer.com | Volume editor arrangement exceptions (contact if volume editors ≠ PC Chairs) |
| LNCS Editorial | lncs@springer.com | Open Choice queries |

---

## Important Constraints

**Page limit.** The LNCS soft limit is **16 pages** per paper. Flag papers above 16 pages; do not automatically reject up to approximately 18 pages without first contacting the authors. Contact the Springer editor for any paper of **30 or more pages**.

**Licence-to-Publish.** Authors must sign the **LNCS-specific LTP form** — no other Springer agreement applies. **Digital signatures are not acceptable**; a wet (ink) signature is required on every LTP.

**Keynote abstracts.** Abstracts of keynote talks without accompanying full papers belong in the **Front Matter**, not in the main proceedings (per Section 4.2 of the Springer editor guidelines). They do not appear in the ToC CSV.

**Folder naming convention.** Each per-paper submission folder must be named `<volume-number><4-digit-starting-page>` with no separator between the two parts. The front matter has its own folder. All folders are zipped into a single archive labelled with the volume number.

**Source files.** Springer requires source files alongside the PDF for every paper. `.tex`, `.bib`, `.bbl`, and `.docx` files are **not** git-ignored and should be committed when received.

**Front-matter templates.** The LaTeX and Word templates for front matter (preface, organization pages, etc.) are available from the volume editors' website at <http://bit.ly/2HaWmko>.
