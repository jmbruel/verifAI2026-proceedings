# Springer Submission Checklist

Pre-submission checklist for the VERIF-AI 2026 LNCS proceedings. Work through every item in order and tick each checkbox before sending the final package to Springer.

> **Timing note:** Springer requires **8–10 weeks** from receipt of the complete, correct file set to publish the proceedings. If printed copies are needed at the conference, all files must arrive at Springer **10 weeks before the conference start date** (8–11 March 2026, so no later than **early January 2026**). Do not send the zip until every item below is ticked — late changes after submission are not possible.

---

## Papers

- [ ] **All camera-ready PDFs received** — confirm that a PDF has been received for every one of the 25 papers and that the "Camera-Ready Received" column in `tracking/paper-tracking.md` shows `Yes` or a received date for all 25 rows.
- [ ] **All source files received** — confirm that the accompanying LaTeX source files (`.tex`, `.bib`/`.bbl`, images) or Word source file (`.docx`) has been received for every paper and that the "Source Files Received" column in `tracking/paper-tracking.md` shows `Yes` or a received date for all 25 rows.
- [ ] **All compliance checks pass** — confirm that the "Compliance Check" column in `tracking/paper-tracking.md` shows `Pass` for all 25 papers. No paper may remain `Pending` or `Fail` at submission.
- [ ] **All papers use the LNCS template** — confirm that every camera-ready paper was produced with either the official LNCS LaTeX template (`llncs.cls`) or the official LNCS Word template. Reject any `.docm` files; authors must resave as `.docx` before this item can be ticked.

---

## Licence-to-Publish

- [ ] **LNCS-specific LTP with wet signature received for all 25 papers** — confirm that the signed Licence-to-Publish agreement for each paper uses the LNCS-specific LTP form (not any other Springer agreement). Each LTP must bear a handwritten (wet) signature; digital signatures are not acceptable and render the LTP invalid.
- [ ] **Corresponding author on each LTP matches the paper header** — confirm that the name of the corresponding author on every signed LTP matches the corresponding author marked on that paper's header exactly. Any mismatch invalidates the LTP; request a corrected copy before ticking this item.

---

## Table of Contents

- [ ] **All fields complete in `submission/toc.csv`** — confirm that every row in the ToC CSV has a non-empty Starting Page, Corresponding Author Name, Corresponding Author Email, and Submission Folder Number. No field may be blank at submission.
- [ ] **Topical Part Titles section headings added** — confirm that papers in `submission/toc.csv` have been grouped by topic (not by conference session) and that appropriate Part Titles section headings have been inserted in the `Part Titles` column.

---

## Front Matter

- [ ] **Preface finalized** — confirm that `front-matter/preface.md` contains no placeholder text (search for `PLACEHOLDER`). All narrative sections (Scope and Aims, Review Process, Acceptance Statistics, Acknowledgements, Volume Editors) must be completed.
- [ ] **Organization pages finalized** — confirm that `front-matter/organization-pages.md` contains no placeholder text (search for `PLACEHOLDER`). All committee roles must be populated with real names, affiliations, and countries.

---

## Springer Administration

- [ ] **Volume number requested from Springer** — contact `anna.kramer@springer.com` to request the LNCS volume number as soon as collection begins. Do not finalize Submission Folder Numbers in the ToC CSV or name any paper folders until the volume number is confirmed.
- [ ] **Two volume numbers requested if total page count exceeds 500 pages** — sum the Page Count column in `tracking/paper-tracking.md`. If the total exceeds 500 pages, request two volume numbers from `anna.kramer@springer.com` before proceeding.
- [ ] **4-week free access opt-in decision communicated to Springer** — notify Springer when sending the files whether you wish to enable the optional 4-week free access offer for conference participants via the conference website. This opt-in must be communicated at submission time.
- [ ] **All contributing authors notified of Springer Nature Code of Conduct** — draw all authors' attention to the Springer Nature Code of Conduct at https://www.springernature.com/gp/authors/book-authors-code-of-conduct before final submission.
- [ ] **Per-paper folder naming convention verified** — confirm that every paper's submission folder is named using the convention `<volume-number><4-digit-starting-page>` (e.g., for a paper starting on page 15 of volume 16456, the folder is named `164560015`). One additional folder is required for the front matter. All folders are zipped into a single zip file labelled with the volume number.
- [ ] **Separate unzipped PDF-only folder prepared** — confirm that a separate, unzipped directory containing only the PDFs of all 25 papers has been prepared alongside the main zip file, as required by Springer.
- [ ] **Volume editor ORCIDs included in the Production Word file** — confirm that the ORCIDs for all volume editors have been entered in the Production Word file sent by Springer together with the volume number.
