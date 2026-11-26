# Springer Submission Checklist

Pre-submission checklist for the VERIF-AI 2026 LNCS proceedings (**Volume 17411**, **Edition ID 696960**; aligned with `instructions.md`, `springer-files/CS_Editors_Proceedings_guidelines.pdf` Sect. 11, and Springer's portal submission email from Sindhu Ramachandran). Work through every item in order and tick each checkbox before uploading the final package to Springer.

> **Timing & Portal Note:** Springer's submission email lists **October 1, 2026** as the originally planned delivery date (coordinate promptly with `sindhu.ramachandran.consultant.1@springernature.com`), and production requires **8–10 weeks** from receipt of the complete file set. Upload via the passwordless [Manuscript Submission Portal (Edition ID 696960)](https://bookmanuscriptsubmission.public.springernature.app/link/bookmanuscriptsubmission/696960-Bertrand.Meyer%40inf.ethz.ch). Do not upload until every item below is ticked — accepted manuscripts are considered **final** after submission (no content, authorship, or corresponding-author changes possible, except minor proof corrections).

---

## Papers

- [x] **All camera-ready PDFs received** — confirm that a PDF has been received for every one of the 24 papers and that the "Camera-Ready Received" column in `tracking/paper-tracking.md` shows `Yes` or a received date for all 24 rows. *(24/24 received as of 2026-11-25.)*
- [x] **All source files received** — confirm that the accompanying LaTeX source files (`.tex`, `.bib`/`.bbl`, images/figures) or Word source file (`.docx`) have been received for every paper and that the "Source Files Received" column in `tracking/paper-tracking.md` shows `Yes` or a received date for all 24 rows. *(24/24 received as of 2026-11-25.)*
- [ ] **All compliance checks pass and LaTeX papers compile** — confirm that `Compliance Check` is `Pass` and `Compilation Status` is `OK` (or `N/A` for Word papers) for all 24 rows in `tracking/paper-tracking.md`, and run `make proceedings` to verify local PDF assembly and pagination. *(24/24 compile OK; 19/24 Pass, 5 pending fixes.)*
- [x] **All papers use the LNCS template** — confirm that every camera-ready paper was produced with either the official LNCS LaTeX template (`llncs.cls`) or the official LNCS Word template. Reject any `.docm` files; authors must resave as `.docx` before this item can be ticked. *(All 24 papers use `llncs.cls`.)*
- [ ] **Page counts meet Springer length rules** — confirm every paper is at least **4 pages** (papers < 4 pages are moved to back matter and not indexed — verify Paper #2 Extended Abstract), short papers ≥ 6 pages, full papers ≥ 12 pages with **at least 2/3 full papers**, soft limit ≤ 20 pages, and Springer contacted for any paper ≥ 30 pages.

---

## Licence-to-Publish

- [ ] **LNCS-specific LTP with wet signature received for all 24 papers** — confirm that the signed Licence-to-Publish agreement for each paper uses the attached LNCS-specific form (`springer-files/SNCS_ProceedingsPaper_LTP_ST_SN_Switzerland.docx`, not any other Springer agreement) and bears a handwritten (wet) signature. Place each signed LTP inside its paper's submission folder.
- [ ] **Corresponding author on each LTP matches the paper header** — confirm that the name of the corresponding author on every signed LTP matches the single corresponding author marked on that paper's header (and email address) exactly. Any mismatch invalidates the LTP; request a corrected copy before ticking this item.

---

## Table of Contents & Author Index

- [ ] **All fields complete in `submission/toc.csv` (and Springer Excel template)** — confirm every row has a non-empty Starting Page, Corresponding Author Name, Corresponding Author Email, and Submission Folder Number. Transfer to `springer-files/Table_of_Contents_template.xlsx` (or supply in an equivalent electronic format) for Springer.
- [ ] **Topical Part Titles section headings added** — confirm that papers in `submission/toc.csv` (and `proceedings.tex`) have been grouped by topic (not by conference session, with no session numbering) and that meaningful Part Titles section headings have been entered.
- [ ] **Non-straightforward author names list prepared** — compile a list (`Given Name; Family Name`) for authors with complex surnames, particles, suffixes, or non-Western order (verify e.g. `Lefevre Louis` in Paper #6, Sub. ID `4854`), and confirm identical spelling across all papers for multi-paper authors.

---

## Front Matter

- [ ] **Preface finalized (Markdown and LaTeX/PDF)** — confirm that `front-matter/preface.md` and `front-matter/preface.tex` contain no `PLACEHOLDER` or `TODO` markers, are written in American English past tense, cover scope, review process, acceptance statistics, and **how PC-coauthored papers were objectively handled** during review, and compile cleanly via `make front-matter`.
- [ ] **Organization pages finalized (Markdown and LaTeX/PDF)** — confirm that `front-matter/organization-pages.md` and `front-matter/organization-pages.tex` contain no `PLACEHOLDER` markers, list PC members and reviewers alphabetically by surname with university and country only (no departments/labs, no bios/photos), and compile cleanly via `make front-matter`. Include both front-matter source and PDF in the `frontmatter` folder for Springer.

---

## Springer Administration

- [x] **Volume number requested from Springer** — contact `anna.kramer@springer.com` to request the LNCS volume number as soon as collection begins. **Assigned: LNCS 17411** (confirmed 2026-11-25). Rename paper folders to `17411<4-digit-page>` and fill Submission Folder Numbers in `submission/toc.csv` once final paper ordering & page counts are locked.
- [x] **Two volume numbers requested if total page count exceeds 700 pages** — sum the Page Count column in `tracking/paper-tracking.md`. Per `instructions.md` and Springer Guidelines Sect. 3.4, if the total exceeds **700 pages**, request two volume numbers from `anna.kramer@springer.com`. *(Single volume confirmed: 388 paper pages / 406 total pages ≤ 700; LNCS 17411.)*
- [ ] **Post-event revision subtitle & peer-review statistics communicated** — inform Springer whether authors were given the opportunity to revise papers after the March 2026 workshop (affects volume subtitle, e.g., *"Revised Selected Papers"*), and provide peer-review process & acceptance statistics requested with the volume number (for SpringerLink / Crossmark).
- [ ] **PC-member 2-paper cap verified** — confirm that no PC Chair, PC member, or volume editor co-authored more than 2 papers in the volume (Springer Guidelines Sect. 3), and that any volume-editor ≠ PC-Chair exception was approved by Ronan Nugent (`ronan.nugent@springer.com`).
- [ ] **4-week free access opt-in and copy order estimate communicated** — notify Springer when sending files whether to enable the optional 4-week free online access via the workshop website, and provide an estimate of any print/online proceedings copies needed (with shipping/billing addresses and VAT number if ordering print copies).
- [ ] **Open Choice / Open Access list submitted (if applicable)** — if any individual papers opt for Open Choice (or full-volume Open Access), provide the list, invoicing addresses, and CC-BY LTP agreements at least **3 weeks before** the file deadline (`lncs@springer.com`).
- [ ] **All contributing authors notified of Springer Nature Code of Conduct & Books Publishing Policies** — draw all authors' attention to the [Springer Nature Code of Conduct](https://www.springernature.com/gp/authors/book-authors-code-of-conduct) (`springer-files/Publisher's_Code_of_Conduct_for_Book_Authors.pdf`) and confirm adherence to Springer's [Books Publishing Policies](https://www.springernature.com/gp/policies/book-publishing-policies).
- [ ] **Third-party rights confirmation verified for portal declaration** — confirm whether any paper reproduces third-party copyrighted figures, tables, or excerpts and that all required third-party permissions have been obtained (covered by authors' LTP Clause 5(a)(iv) warranties) so the mandatory third-party rights declaration on the submission portal can be completed accurately.
- [ ] **Proxy-submission authorization confirmed (if submitting on Bertrand Meyer's behalf)** — the passwordless submission portal (`Edition ID 696960`) is tied to `Bertrand.Meyer@inf.ethz.ch`; per Springer's instructions, anyone submitting on Bertrand Meyer's behalf must have explicit authorization to act for him, including making the third-party rights declaration.
- [ ] **Content finality verified across all 24 papers** — confirm all manuscripts, author lists, and front matter are final (no content changes are permitted after portal upload except minor proof corrections).
- [ ] **Per-paper folder naming convention and contents verified** — confirm each paper has its own folder named `17411<4-digit-starting-page>` (e.g., `174110001`) containing its original source files (`.tex`/`.bib`/`.bbl`/figures or `.docx`), compiled PDF, signed LTP, and any Alt Text Excel file; plus a `frontmatter` folder. Zip all folders together (`.zip`, not `.tar`) labelled `17411.zip`.
- [ ] **Complete manuscript PDF and/or individual chapter PDFs prepared** — Springer's portal requires either a single PDF of the complete manuscript (`proceedings.pdf`) OR individual PDFs of each chapter (and LNCS guidelines request a separate unzipped PDF-only directory alongside the main `.zip`).
- [ ] **Production Word file / supporting questionnaire completed** — confirm that full names (including middle initials), full postal addresses (with postal codes), and ORCIDs for all volume editors have been entered in the Production Word file / supporting production questionnaire requested by Springer.
- [ ] **Final package uploaded to Springer Manuscript Submission Portal** — upload `17411.zip`, PDF(s), signed LTPs, ToC, and supporting files via the [Edition 696960 portal](https://bookmanuscriptsubmission.public.springernature.app/link/bookmanuscriptsubmission/696960-Bertrand.Meyer%40inf.ethz.ch) (no password needed) and contact `sindhu.ramachandran.consultant.1@springernature.com` with any questions or updated delivery timing.
